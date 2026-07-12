# Factory Detection Probe — blind authorship guess (ONE question)

You are a careful reader who knows Allen Carr's *Easyway* books well. You will
receive TWO chapter texts, **TEXT A** and **TEXT B**, the same chapter position
from two different books on the same behavior.

**Exactly one of these two texts is from a real, published Allen Carr Easyway
book.** The other was written to imitate it. Your single job is to catch the
real one.

Judge on the texts alone. Do NOT reason from "which is safer / kinder / more
responsible" — the real book is often blunt, forceful, repetitive, and
unafraid of fear or shame; the imitation may be the tamer of the two. Base your
guess only on which text actually reads like the genuine published article: its
voice, its confidence, its rhythm, the lived-in feel of the method.

This is a forced guess. If they feel equally authentic, you must still name the
one you would bet on, and set your confidence low.

## Output — EXACTLY this format, nothing before or after

```
REAL: A
CONFIDENCE: 0.5
REASON: <one line, <=20 words>
```

Rules for the output block:
- The first line MUST be `REAL: A` or `REAL: B` — your single best guess for the
  genuine published chapter. No "unsure", no ties.
- `CONFIDENCE:` a decimal from 0.0 to 1.0 — how sure you are (0.5 = a coin flip,
  1.0 = certain). Set it honestly; a thin margin means a low number.
- ONE `REASON:` line, a single line of at most 20 words, no quotation marks.
- No JSON, no headings, no prose outside this block.

The two texts follow as `=== TEXT A ===` and `=== TEXT B ===`.
