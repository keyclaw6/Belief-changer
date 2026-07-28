# Judge Panel

Three judges evaluate our chapters against the real GSBS book.
Each judge has a different lens. All three run on every chapter.

## Panel composition

| Judge | File | Lens |
|-------|------|------|
| Belief-Change Mechanic | `belief-mechanic.md` | Does the argument change the belief? |
| Voice & Emotion | `voice-emotion.md` | Does it feel like Carr? |
| Reader Journey | `reader-journey.md` | Would a real reader be moved? |

## Usage

Each judge receives:
1. The judge prompt (from this directory)
2. Our chapter text
3. The real GSBS chapter text (from `calibration/reference/gsbs/`)

Chapter N maps to reference file N+2 (offset 2 for front matter).

## Calibration

The judges are tuned separately by the founder. The loop does NOT edit
judge prompts during iterations. If the judges are wrong, that's a
founder-level fix.
