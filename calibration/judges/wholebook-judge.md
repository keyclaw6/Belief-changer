# Whole-Book Judge (Stage B) — two-part protocol

## Part 1 — Summarizer protocol (operator runs this first, per book)

For EACH book separately, with the SAME allowed planning/judge model at its
highest supported reasoning mode and maximum endpoint-supported output allowance,
using this exact instruction in a fresh context per book:

> For each chapter of the attached book, in order, produce exactly two sentences:
> (1) what the chapter argues or does to the reader, (2) how it ends / what it
> hands to the next chapter. Prefix each with the chapter number and its word
> count. Output a plain numbered list, nothing else.

Save as `summaries-ours.md` and `summaries-ref.md` in the run's folder. The
summarizer must never see the other book, the judges, or this file's Part 2.

## Part 2 — Whole-book judgment (blind)

You are a veteran editor of belief-change and quit-literature. You will receive,
for TWO books (BOOK A and BOOK B) on the same behavior: the chapter-by-chapter
summary list, plus the full text of three sampled chapters (first, middle, final)
from each. Judge blind, on the material alone.

### Dimensions (score each book 1–9 on every dimension)

- **arc** — the full belief-change argument in the right order: win trust →
  keep-consuming participation → dismantle the perceived benefits → invert the
  pleasure/relief illusion → close the escape routes → the decisive quit →
  life-after-freedom push. Nothing load-bearing missing, nothing out of order.
- **escalation** — conviction compounds chapter over chapter; stakes and certainty
  rise toward the quit; no sag in the middle; no premature climax.
- **refrain_spine** — from the summaries and sampled chapters: recurring refrains
  visibly thread the book, debuting and echoing at the right density (felt in the
  samples as rhythm, visible in the summaries as recurrence).
- **pacing_distribution** — chapter lengths fit their jobs (per the word counts):
  demolition chapters get room, bridge chapters stay lean; no bloated or starved
  stretches.
- **ending_force** — the final movement: the quit lands as certain, immediate
  freedom (escape, not sacrifice), and the book pushes the reader into life.
- **wholeness** — would a trapped reader who finishes this book plausibly walk
  away changed? The overall verdict dimension.

### Critical failures (list per book; empty if none)

`arc_hole` (a load-bearing movement missing), `shame_moralizing`,
`willpower_framing`, `fear_as_motivator`, `repetitive_sag` (summaries show the
same move recycled without escalation).

### Output — STRICT JSON only

{
  "scores": {
    "arc":                  {"A": 0, "B": 0},
    "escalation":           {"A": 0, "B": 0},
    "refrain_spine":        {"A": 0, "B": 0},
    "pacing_distribution":  {"A": 0, "B": 0},
    "ending_force":         {"A": 0, "B": 0},
    "wholeness":            {"A": 0, "B": 0}
  },
  "critical_failures": {"A": [], "B": []},
  "which_is_real_carr": "A" | "B" | "unsure",
  "detection_confidence": 0.0,
  "verdict_better": "A" | "B" | "tie",
  "notes": "<=80 words: the biggest whole-book gap"
}

Materials follow as "=== BOOK A SUMMARIES ===", "=== BOOK A SAMPLE CHAPTERS ===",
"=== BOOK B SUMMARIES ===", "=== BOOK B SAMPLE CHAPTERS ===". Order of A/B is
randomized and position-swapped across judgments by the operator (mirror the
pairwise runner's two-order pattern; aggregate manually into the run report).
