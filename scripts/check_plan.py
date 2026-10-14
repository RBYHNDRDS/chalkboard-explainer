#!/usr/bin/env python3
"""Check a chalkboard-explainer drawing timeline before generating video.

Usage:
    python3 scripts/check_plan.py plan.json [--prompt prompt.txt] [--model wan3_0]

Exit code 1 when any check fails. No network access, no dependencies.
"""

import argparse
import json
import re
import sys

# Letters per second. Calibrated on two observed clips: a convincing
# chalkboard clip wrote about 8 to 9 letters/s with the writing edge always
# under the hand; a failed whiteboard clip popped words in at about 24/s.
WARN_LETTERS_PER_SECOND = 6.0
FAIL_LETTERS_PER_SECOND = 10.0
MIN_SECONDS = {"doodle": 1.5, "icon": 0.6, "mark": 0.4}
MAX_GAP_SECONDS = 1.0
MAX_WORDS_PER_LINE = 3
MAX_WORDS_PER_SECOND_SEGMENT = 3.5
MAX_WORDS_PER_SECOND_TOTAL = 2.7
LIST_NUMBER = re.compile(r"^\s*\d\.\s*")

# Known prompt-length limits, in characters. Extend as models change.
PROMPT_LIMITS = {
    "wan3_0": 5000,
}


def letters(text):
    return sum(ch.isalpha() for ch in text)


def words(text):
    return len(re.findall(r"[A-Za-z0-9']+", text))


def check(plan, prompt_text=None, model=None):
    results = []

    def add(level, msg):
        results.append((level, msg))

    duration = float(plan.get("duration", 0))
    elements = plan.get("elements", [])
    if not elements:
        add("FAIL", "plan has no elements")
        return results
    if not duration:
        add("FAIL", "plan has no duration")
        return results

    list_points = 0
    prev_end = 0.0
    for i, el in enumerate(elements, 1):
        start, end = float(el["start"]), float(el["end"])
        kind = el.get("type", "text")
        content = el.get("content", "")
        label = f"element {i} ({start:g}-{end:g}s, {kind} '{content[:30]}')"
        length = end - start

        if length <= 0:
            add("FAIL", f"{label}: zero or negative length")
            continue
        if start < prev_end - 0.01:
            add("FAIL", f"{label}: overlaps the previous element, one hand draws one thing at a time")
        elif start - prev_end > MAX_GAP_SECONDS:
            add("WARN", f"{label}: {start - prev_end:.1f}s pause before it, a still hand looks frozen")
        prev_end = max(prev_end, end)
        if end > duration + 0.01:
            add("FAIL", f"{label}: ends after the {duration:g}s runtime")
        if not el.get("position"):
            add("WARN", f"{label}: no position, the model will place it wherever it likes")

        if kind == "text":
            body = LIST_NUMBER.sub("", content)
            if LIST_NUMBER.match(content):
                list_points += 1
            rate = letters(content) / length
            if rate > FAIL_LETTERS_PER_SECOND:
                add("FAIL", f"{label}: {letters(content)} letters in {length:g}s ({rate:.1f}/s), "
                            "too fast to stay under the hand")
            elif rate > WARN_LETTERS_PER_SECOND:
                add("WARN", f"{label}: {rate:.1f} letters/s, keep the hand on the writing edge")
            for line in body.split("/"):
                if words(line) > MAX_WORDS_PER_LINE:
                    add("FAIL", f"{label}: '{line.strip()}' has more than {MAX_WORDS_PER_LINE} words "
                                "on one line, wrap it with '/'")
            if re.search(r"\d", body):
                add("FAIL", f"{label}: contains a number, only single-digit list numbers are safe")
        elif kind in MIN_SECONDS and length < MIN_SECONDS[kind]:
            add("FAIL", f"{label}: a {kind} needs at least {MIN_SECONDS[kind]:g}s")

    if duration - prev_end > 1.5:
        add("WARN", f"drawing ends at {prev_end:g}s, {duration - prev_end:.1f}s of an idle board at the end")
    max_points = 3 if duration <= 25 else 4
    if list_points > max_points:
        add("WARN", f"{list_points} list points in {duration:g}s, models start skipping points "
                    f"above {max_points}")
    elif list_points and list_points < 3:
        add("WARN", f"{list_points} list points, 3 reads best")

    total_words = 0
    for seg in plan.get("dialogue", []):
        start, end = float(seg["start"]), float(seg["end"])
        n = words(seg.get("text", ""))
        total_words += n
        if end > start and n / (end - start) > MAX_WORDS_PER_SECOND_SEGMENT:
            add("FAIL", f"dialogue {start:g}-{end:g}s: {n} words, too fast to say naturally")
    if total_words / duration > MAX_WORDS_PER_SECOND_TOTAL:
        add("WARN", f"{total_words} spoken words in {duration:g}s, aim for "
                    f"{MAX_WORDS_PER_SECOND_TOTAL * duration:.0f} or fewer")

    model = model or plan.get("model")
    if prompt_text is not None:
        limit = PROMPT_LIMITS.get(model)
        if limit and len(prompt_text) > limit:
            add("FAIL", f"prompt is {len(prompt_text)} characters, {model} accepts {limit}")
        elif limit:
            add("OK", f"prompt is {len(prompt_text)} of {limit} characters for {model}")
        else:
            add("OK", f"prompt is {len(prompt_text)} characters (no known limit for {model})")

    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("plan")
    ap.add_argument("--prompt", help="text file with the video prompt to length-check")
    ap.add_argument("--model", help="model id, overrides the plan's model")
    args = ap.parse_args()

    with open(args.plan, encoding="utf-8") as f:
        plan = json.load(f)
    prompt_text = None
    if args.prompt:
        with open(args.prompt, encoding="utf-8") as f:
            prompt_text = f.read()

    results = check(plan, prompt_text, args.model)
    for level, msg in results:
        print(f"{level:4}  {msg}")
    failed = any(level == "FAIL" for level, _ in results)
    if not any(level != "OK" for level, _ in results):
        print("OK    timeline passes")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
