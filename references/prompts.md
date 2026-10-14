# Prompt templates

Replace every `{{PLACEHOLDER}}`. Describe what a camera would see, not what the video should achieve.

## 1. Reference image (any image model)

Make it once and reuse it as the start frame for every video in the series.

```text
Vertical 9:16 phone photo of a real matte dark green school chalkboard filling almost the whole frame, thin light aluminium frame, a sliver of cream wall around it. The board is empty apart from a faint grey haze of old erased chalk, a few soft eraser swipes in the lower half and a light dusting of chalk powder along the bottom edge. No glare, flat even classroom light. {{ARM: e.g. a woman's bare forearm}} enters from the right edge holding a short stick of white chalk with its tip touching the board near the top left: {{SKIN AND HAND DETAILS: e.g. natural skin with fine arm hair, visible tendons on the back of the hand, short unpainted nails}}, a little white chalk dust on the fingertips, {{ONE ACCESSORY: e.g. a thin silver bracelet}}. Only the forearm and hand are visible, no face, no shoulder, no body. Shot on an iPhone rear camera on a tripod, straight on, sharp focus across the board, slightly cool white balance, light grain in the dark green, mild compression.
```

Attach it as the **start frame** where the model supports one. The video then begins on exactly this framing, which keeps the static shot locked.

## 2. One-shot route (default)

A filled-in prompt for 25 s is about 3,000 characters, well inside Wan 3.0's 5,000 limit. See `examples/ad-fatigue.prompt.txt` for a complete one.

```text
{{DURATION}}-second vertical 9:16 iPhone video of a real classroom chalkboard lesson. One continuous static shot on a tripod, straight on, the whole board in frame. No cuts, no zoom, no camera movement. Real footage, not an ad, not AI. Match the uploaded reference image: same matte dark green chalkboard, frame, light and forearm.

VISIBILITY: only her bare forearm and hand, entering from the right edge. Never face, head, shoulder or body.

CHALK: white chalk only. Dry, slightly grainy lines with tiny gaps, a little chalk dust falling. Capital letters, slightly uneven, simple line drawings.

HOW SHE WRITES: one element at a time, in the order below. Chalk appears only exactly at the tip of the chalk, with her hand on top of the line being drawn; nothing appears anywhere her hand is not. She finishes each element before moving to the next. Once drawn, nothing moves, changes or disappears.

SEQUENCE (with her voice):
{{FOR EACH ELEMENT: START-ENDs: POSITION: WHAT SHE DRAWS. She says: "..."}}
{{LAST: she lowers the chalk and her hand moves out of frame to the right.}}

FINAL BOARD: {{ONE OR TWO SENTENCES: what is where on the finished board}}. Plenty of empty board around everything.

VOICE: {{VOICE}}, calm and warm, like a teacher who likes the topic. Natural pauses that follow the chalk, no announcer tone. Recorded on the phone in a quiet classroom: chalk taps and scratches, slight room echo.

AVOID: cuts, camera movement, face or body, text appearing by itself or all at once, letters fading in or appearing ahead of the chalk, words changing after being written, misspelled words, coloured chalk, whiteboard, marker, glossy surface, computer font, extra fingers, chalk leaving the hand, AI voice, studio audio, animation, cartoon.
```

## 3. Extend route (models capped at 8 to 15 s)

Split the timeline between two elements, never inside one. Generate part 1 with the reference image as start frame. For each next part, extend from the previous clip, or use its last frame as the start frame, with:

```text
{{PART LENGTH}}-second continuation of the same static chalkboard shot. The camera does not move. Continue exactly from the start frame.

ALREADY ON THE BOARD (do not change, move or erase any of it): {{EVERYTHING DRAWN SO FAR, with positions}}

SEQUENCE:
{{ONLY THE ELEMENTS FOR THIS PART, same format as the one-shot route, times starting at 0}}

Same chalk, same forearm, same voice: {{VOICE}}. Chalk only appears at the tip of the chalk under her hand.

AVOID: cuts, camera movement, anything already on the board changing, text appearing by itself or ahead of the chalk, coloured chalk, AI voice.
```

Join the parts on the frame where one element ends and the next begins. With a locked camera the join is invisible.
