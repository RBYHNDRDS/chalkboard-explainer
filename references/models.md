# Model notes

Specs change every few months. Check the model's own page before relying on a number here. Last checked October 2026 via Higgsfield's model catalogue.

| Model | Max clip | Start frame | Native audio | Route | Notes |
|---|---|---|---|---|---|
| Wan 3.0 | 30 s | yes | yes | One-shot | Prompt limit 5,000 characters. Turn on "thinking" for better prompt following. |
| Seedance 2.5 | 30 s | yes | yes | One-shot | 1080p is an upscale from 720p. Has a cheap 480p draft mode. |
| Kling 3.0 | 15 s | yes | yes | Extend, 2 parts | |
| Gemini Omni Flash 1.1 | 10 s, extend to 40 s | yes | yes | Extend, 3 parts | Exact on-screen text is a known weak spot. |
| Veo 3.1 | 8 s | yes | yes | Extend, 3 to 4 parts | |

## What we learned in testing

- **Text appears where the hand is not.** This was the main failure in our first tests (a whiteboard variant of this format). At about 24 letters per second the model stopped writing and started popping whole words in next to the hand.
- **Speed alone is not the problem.** A convincing chalkboard clip we studied wrote about 8 to 9 letters per second, but the writing edge was always under the hand, so no letter ever appeared from nothing. `scripts/check_plan.py` warns above 6 and fails above 10 letters per second for that reason.
- **Wan 3.0 followed board content more closely than Seedance 2.5** in a side-by-side test (right words, right marks, right places), at a third of the credits for a 30 s draft. Seedance invented an extra line and swapped a cross for a tick.
- **Too many list points get dropped.** A 25 s chalkboard run with four numbered points and icons skipped point 2 and numbered the rest 1, 2, 4. It also drew a light bulb where a fish hook was asked for. The skill now limits the list to three points for 25 s, states the exact count in the prompt and describes icons so they cannot be confused. That fix is being verified.
- **Colour is unreliable.** Both models drew doodles in the wrong colour. This format uses white chalk only, which removes the problem.

A handful of tests is not a benchmark. Run one short test on your own model before producing a batch.
