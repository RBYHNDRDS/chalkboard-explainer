# Chalkboard Explainer

A portable AI skill for planning and prompting chalkboard explainer videos: one static shot of a real classroom chalkboard, a bare forearm writing in white chalk, a question at the top, a myth crossed out, a short numbered list with a tiny icon per point, and one underlined takeaway.

It looks like a lesson, not an ad, and the chalk looks handwritten.

A demo video made with the bundled example plan will be added here.

## Why it is built this way

The format only works if the chalk looks written by the hand on screen. AI video models tend to give up on that and pop whole words onto the board next to the hand, and viewers spot it at once.

What matters is not writing slowly but writing where the hand is: every new stroke has to grow under the chalk, one element at a time. This skill plans a drawing timeline around that rule, and `scripts/check_plan.py` checks it before you spend a credit.

## What it does

- Proposes 2 or 3 concepts for your topic: title question, myth to cross out, 3 to 5 points with icons, closing line.
- Lays out a board that reads in one second on a phone.
- Writes a calm, natural voiceover that names each point as it is written.
- Builds a drawing timeline, one element at a time.
- Checks the timeline for writing speed, overlaps, gaps, long lines, numbers on the board, speech rate and prompt length.
- Writes a reference-image prompt and a ready-to-paste video prompt, for one-shot models and for models that need extending.
- Ends with a frame-by-frame QC checklist.

## Included files

- `SKILL.md`: the full workflow and rules.
- `references/prompts.md`: reference-image prompt, one-shot template and extend template.
- `references/models.md`: clip lengths, limits and what we learned in testing.
- `scripts/check_plan.py`: drawing-timeline and prompt-length checker.
- `examples/ad-fatigue.plan.json`: an example drawing timeline that passes the checker.
- `examples/ad-fatigue.prompt.txt`: the matching ready-to-paste prompt.
- `agents/openai.yaml`: optional metadata for OpenAI-compatible skill hosts.

## Requirements

- An AI video model with native audio. Wan 3.0 or Seedance 2.5 for one 20 to 30 s clip; Kling, Veo or Gemini Omni with the extend route.
- Any image model for the reference image.
- Python 3.8 or newer for the checker (standard library only).
- `ffmpeg` for the frame-by-frame QC step.

The script makes no network requests and reads no credentials.

## Install

```bash
git clone https://github.com/RBYHNDRDS/chalkboard-explainer.git
```

For Claude Code:

```bash
mkdir -p "${HOME}/.claude/skills"
ln -s "${PWD}/chalkboard-explainer" "${HOME}/.claude/skills/chalkboard-explainer"
```

For Codex and other agents that scan `~/.agents/skills`:

```bash
mkdir -p "${HOME}/.agents/skills"
ln -s "${PWD}/chalkboard-explainer" "${HOME}/.agents/skills/chalkboard-explainer"
```

### ChatGPT, Gemini or any other chat assistant

Paste the contents of `SKILL.md` into a new chat (or into a custom GPT or Gem's instructions), then paste `references/prompts.md` below it. Run the checker yourself, or ask the assistant to keep to these limits:

- one element at a time, no overlaps, no pauses longer than a second,
- at most about 6 letters per second for any line of text,
- max 3 words per line, no numbers on the board except single-digit list numbers.

## Use it

```text
Use $chalkboard-explainer for my topic: why most people's sourdough doesn't rise.
25 seconds, I'm using Wan 3.0.
```

Then check the plan:

```bash
python3 scripts/check_plan.py plan.json --prompt prompt.txt
```

## Credit

The chalkboard explainer ad format was popularised on X by [@spwfeijen](https://x.com/spwfeijen). This skill is an independent breakdown of why the format works and how to make AI-generated chalk writing hold up.

## License

MIT. See `LICENSE`.
