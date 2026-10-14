---
name: chalkboard-explainer
description: Plan and prompt short vertical "chalkboard explainer" videos and ads, where a bare forearm writes and sketches in white chalk on a real classroom chalkboard in one continuous static shot while a voice explains, generated with an AI video model (Wan, Seedance, Kling, Veo, Gemini Omni or similar). Use when the user asks for a chalkboard explainer, chalkboard ad, blackboard video, myth-busting or listicle explainer drawn on a board, or a native-looking educational ad. Produces the concept, board layout, voiceover, drawing timeline, reference-image prompt, model-ready video prompts and a frame-by-frame QC pass that checks the chalk only appears under the hand.
---

# Chalkboard Explainer

Build a 20 to 30 second vertical video of someone teaching on a real classroom chalkboard. One static shot, no cuts. A bare forearm writes and sketches in white chalk. A question goes up top, a common myth gets crossed out, a short numbered list appears with a small icon next to each point, and one underlined line closes it.

It looks like a lesson, not an ad. That is why it holds attention.

This skill teaches the structure, not a fixed prompt. Understand why each part works, then design a new board for the user's topic.

## The one quality bar

**Chalk only appears under the hand.** Every new stroke grows at the point where the chalk touches the board, with the hand on top of it. Text that appears beside the hand, ahead of it, or by itself breaks the illusion instantly.

Speed is not the main enemy. In good examples the hand writes fast, but the writing edge is always hidden under the hand, so the eye never sees a letter appear from nothing. The prompt and the plan are built around that: one element at a time, the hand never leaves the element it is drawing, and every element finishes before the next one starts.

## Why the format works

1. **The title is a question the viewer already asked.** "BELLY FAT?" in quotes reads like their own search. They stay for the answer.
2. **A myth gets crossed out early.** Striking through what they believed is a pattern break and earns authority in the first seconds.
3. **The numbered list is a progress bar.** Once "1." appears, viewers count along to the last number.
4. **Every point gets a tiny icon.** A plate, an egg, a dumbbell. The board becomes a cheat sheet people screenshot and bookmark.
5. **One underlined line ends it.** A single takeaway, written last and underlined, is what the viewer remembers. In an ad, this line or the voice right after it carries the offer.
6. **It looks like a classroom.** One locked-off shot, white chalk only, matte board, bare forearm, a calm voice. Nothing about it signals advertising.

## Workflow

### 1. Intake

Get, or infer and confirm in one line:

- Topic, offer (if any) and audience.
- The question the audience types or asks about this problem.
- The myth they believe.
- Runtime (default 25 s), video model, and voice (age, accent, tone, language).

### 2. Propose concepts

Give 2 or 3 concepts, three lines each:

- Title question.
- Myth to cross out.
- List of 3 points (4 for 30 s), each with its icon, plus the underlined closing line.

Let the user choose before writing anything else.

### 3. Design the board

Fixed layout that reads in one second on a phone:

```
        'TITLE?'
  [doodle]      1. POINT    (icon)
                2. POINT    (icon)
  MYTH          3. POINT    (icon)
  (crossed out) 4. POINT    (icon)

       CLOSING LINE
       ____________
```

Rules:

- **White chalk only.** Meaning comes from crossing out, circling, arrows and underlining, not colour.
- **Max 3 words per line, capitals.** Keep each point on one line where the board has room; in testing, the second line of a wrapped point tended to jump in at once instead of being written.
- **3 list points for 20 to 25 s, at most 4 for 30 s.** With more, models start dropping a point and skipping a number. Single-digit list numbers are fine. No other numbers, prices, percentages, logos or brand names on the board.
- **Icons are line drawings of one object**, 1 to 2 seconds each. Describe each icon so it cannot be confused with another ("a fish hook with a barb, not a light bulb"); models swap similar small icons.
- **Cross out with a big X of two thick lines**, not a single thin stroke. A thin line disappears on a phone screen.
- **One doodle** at most (a before/after, a simple figure, an object), 2 to 3 seconds.
- Leave margin around everything. The board should still look uncrowded when full.

### 4. Write the voiceover

About 2.2 to 2.6 spoken words per second (55 to 65 words for 25 s). Calm, like a teacher who likes the topic, with an "okay" or "honestly". The voice names each point as the hand writes it. The last spoken line lands while the closing line is underlined.

### 5. Build the drawing timeline

List every element in drawing order with a start and end time: title, doodle, myth, cross-out, then each number, point and icon, then the closing line and underline. One element at a time. No gaps longer than a second, because a still hand on a board looks frozen.

Write it as JSON in the format of `examples/ad-fatigue.plan.json` and run:

```bash
python3 scripts/check_plan.py plan.json --prompt prompt.txt
```

The checker flags elements that are drawn too fast to hide under a hand, overlaps, gaps, lines that are too long, numbers on the board, speech that is too fast, and prompts over the model's character limit. Fix every `FAIL` before generating.

### 6. Reference image

Generate one empty-board image with any image model and reuse it for every video in the series, so the board, the light and the arm stay the same. Prompt template in `references/prompts.md`.

### 7. Generate

- **One-shot route (default).** One continuous clip of the full runtime with the reference image attached. Needs a model that does 20 to 30 s in one clip (Wan 3.0, Seedance 2.5). Use the compact template; Wan 3.0 rejects prompts over 5,000 characters.
- **Extend route.** For models that stop at 8 to 15 s: generate the first part, then extend from its last frame with the next part of the timeline. Cut points must fall between two elements, never inside one, and the camera must not move.

Templates for both routes are in `references/prompts.md`. In the final-board paragraph, state the exact number of list points and add "never skip or repeat a number".

### 8. QC, frame by frame

Watching at normal speed hides mistakes. Extract frames at 4 fps around each element:

```bash
ffmpeg -ss START -t SECONDS -i video.mp4 -vf "fps=4,scale=240:-1,tile=8x2" -frames:v 1 check.jpg
```

Pass criteria:

- [ ] Every new stroke appears under or right at the chalk tip, with the hand on it.
- [ ] Nothing appears in a part of the board the hand is not touching.
- [ ] Each element is finished before the hand moves to the next one.
- [ ] Nothing already written changes, moves or disappears.
- [ ] Every word is spelled right in the final frame, every list point is there, and the numbers run without gaps.
- [ ] Each icon is the object that was asked for.
- [ ] The camera never moves and there are no cuts.
- [ ] Only the forearm and hand are visible. Five fingers, chalk always in the hand.
- [ ] The voice sounds like a person in a classroom, with chalk taps and scratches.

On a fail, regenerate. If one element keeps appearing on its own, shorten its text, give it more time, or move it later in the timeline so the hand arrives first.

## Output to the user

Deliver in this order, nothing else:

1. Chosen concept.
2. Final board as a text sketch.
3. Voiceover.
4. Drawing timeline and the `check_plan.py` result.
5. Reference image prompt.
6. Video prompt for their model, ready to paste.
7. The QC checklist.

## Guardrails

- Do not reuse another creator's script or board verbatim. Use the structure to build a new one.
- Health, money and legal topics: no claims the user cannot back up, on the board or in the voice.
- If the user's model or account limits are unknown, say which route you assumed.
