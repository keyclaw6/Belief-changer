# Dry Run — Founder Hypothesis Inbox

**Loop:** auto-research loop, revisions `main` @ afca11f.
**Scope:** PROGRAM §4 Step 1 + `loop/inbox/README.md` + `loop/prompts/hypothesizer.md`.
**Mode:** read-only simulation. No files edited, no model calls made.

Relevant normative facts held fixed:
- `loop/inbox/` is scanned only for `.md` files other than `README.md` (§4 Step 1).
- Every iteration that runs writes a learnings entry to `loop/learnings.md`,
  including on REVERT (§4 Step 7). `learnings.md` is a normal hypothesizer input.
- `loop/inbox/used/` is currently empty (no prior pickups at this rev).
- `loop/state.md` read as baseline (Iteration 000). This dry run reasons forward
  from §4 Step 1 only; no iteration state is mutated here.

---

## (a) Well-formed founder note — one change, has Change / Because / Prediction

**Setup:** founder drops
`2026-08-12-shorten-instructions.md` in `loop/inbox/` with a `# Hypothesis:` line
and the three fields `**Change:**` / `**Because:**` / `**Prediction:**`, naming a
single editable file and a single change.

**Trace (source of each directive):**

| # | Step | Directive (file → cite) | Result |
|---|------|------------------------|--------|
| 1 | Scan inbox | "If `loop/inbox/` holds any `.md` file other than `README.md`, the founder has proposed a hypothesis — test it before any machine-generated one, oldest file first." (PROGRAM §4 Step 1) | Note detected as founder hypothesis; README excluded |
| 2 | Validate | "Validate the oldest file against `loop/inbox/README.md`." (PROGRAM §4 Step 1.1). README requires Change/Because/Prediction, one hypothesis per file. | Note is single-file, single-change, all three fields → valid |
| 3 | Route to hypothesizer (not orchestrator) | "Otherwise feed it to the hypothesizer (not the orchestrator) as the hypothesis source, alongside the normal inputs" (PROGRAM §4 Step 1.2) | Founder note routed to hypothesizer as source |
| 4 | Normal inputs incl. learnings | Hypothesizer contract: "Your inputs: Trace analysis; **Learnings** — `loop/learnings.md`; Current factory state" (hypothesizer.md → Your inputs). PROGRAM Step 1.2 "alongside the normal inputs" | `learnings.md` is among inputs, so never-repeat guard has data |
| 5 | Never-repeat + one-change guards | "so its never-repeat and one-causal-change guards still apply." (PROGRAM §4 Step 1.2); "Check learnings first. Never repeat a hypothesis that already failed." (hypothesizer.md → Rules) | Guard applies to the founder-sourced hypothesis |
| 6 | Produce 4-field hypothesis | "Your job: propose ONE causal change..." (hypothesizer.md header); `Predicted impact` etc. | Hypothesizer returns 4-field (Failure evidence / Root cause / Targeted fix / Predicted impact) |
| 7 | Save before move | "Save the hypothesizer's 4-field response as `loop/iterations/NNN/hypothesis.md` with `source: founder inbox`, and only then move the inbox file to `loop/inbox/used/NNN-<name>.md` (write the hypothesis first — never move before it is recorded)." (PROGRAM §4 Step 1.3) | Ordering is explicit: hypothesis.md written with `source: founder inbox`, then inbox file renamed to `used/NNN-<name>.md` |

**Verdict (a): COMPLETES.** The founder-note → hypothesizer (with learnings) →
4-field hypothesis.md → move-to-used/ flow is fully specified, with write-before-move
enforced and the never-repeat/one-change guards explicitly applied to inbox input.

**Footnote risk (improve, non-blocking):**
- Validation (Step 1.1) checks only "vague or multi-change." The README format
  shows `# Hypothesis:` + `**Change:**`/`**Because:**`/`**Prediction:**` as a
  *message format*, and no check verifies that `**Change:**` targets an editable
  file (§1 list). A well-formed-looking note that proposes changing, e.g., a
  judge or a `production-books/` artifact would pass validation and flow to the
  hypothesizer. The hypothesizer's one-causal-change rule ("One causal change in
  one editable file", hypothesizer.md → Rules) is the only guard left, and it is
  a soft prompt rule, not a deterministic gate.

---

## (b) Vague or multi-change note → validated then handed back, loop falls through

**Setup:** founder drops `2026-08-12-make-it-better.md` that either (i) has no
actionable Change/Because/Prediction (vague) or (ii) names multiple changes /
multiple files.

**Trace (source of each directive):**

| # | Do-not-guess guard | Directive (file → cite) | Result |
|---|--------------------|------------------------|--------|
| 1 | Validate | "Validate the oldest file against `loop/inbox/README.md`." (PROGRAM §4 Step 1.1) | Fails: vague or multi-change |
| 2 | Reject without guessing | "If it is vague or multi-change, do NOT guess: move it to `loop/inbox/used/REJECTED-NNN-<name>.md`, note the defect to the founder, and fall through to the hypothesizer below." (PROGRAM §4 Step 1.1) | File moved to `used/REJECTED-NNN-...`; defect noted to founder; **no inference from the vague content** |
| 3 | Fall through to hypothesizer | "...and fall through to the hypothesizer below." (PROGRAM §4 Step 1.1); "If the inbox is empty, spawn the `hypothesizer` sub-agent..." (PROGRAM §4 Step 1) | Loop proceeds to machine-generated hypothesis (Step 1 "If the inbox is empty" → the reject moved the note out, so inbox is empty for this processing and the machine hypothesizer runs) |

**Verdict (b): COMPLETES.** The rejection is deterministic (do-not-guess), the
REJECTED-prefixed `used/` destination is exact, the founder is engaged, and the
fall-through to the hypothesizer is explicit.

**Footnote (cosmetic mismatch):** `loop/inbox/README.md` says the orchestrator
will "hand it back with what to sharpen" while PROGRAM §4 Step 1.1 says "move it
to `loop/inbox/used/REJECTED-...`, note the defect." PROGRAM is authoritative and
the README is inside the scan-eligible directory, so it is a prompt-facing file
whose wording differs slightly from the runnable PROGRAM semantics. Both agree on
do-not-guess; only the "hand back vs archive-as-REJECTED" phrasing differs. Also,
because the note is *moved* (not returned in place), the "what to sharpen" advice
reaches the founder only via the orchestrator's note-to-founder, not by leaving
the file discoverable in `inbox/`.

---

## (c) Multiple notes present — is oldest-first defined and unambiguous?

**Setup:** `loop/inbox/` holds two or three non-README `.md` notes.

**Trace:**

| # | Question | Directive (file → cite) | Assessment |
|---|----------|------------------------|------------|
| 1 | Global precedent | "test it before any machine-generated one, oldest file first." (PROGRAM §4 Step 1) | Ordering relative to machine hypotheses: before them ✓ |
| 2 | Within-inbox order | "in the order they arrived (oldest file first)." (README.md → Rules); "Validate the oldest file ... (PROGRAM §4 Step 1.1) | Ordering principle stated: oldest first ✓ |
| 3 | Sort key | what encodes "oldest"? (nothing pins it) | **UNDEFINED.** Neither PROGRAM nor README pins the filesystem attribute (file mtime, ctime, inode, or filename date prefix). README's example name embeds a date (`2026-08-12-…`), which *hints* filename-date ordering, but no rule compels it. A coding agent's `ls` sort (name/mtime) can disagree with arrival order. |
| 4 | Multi-note processing loop | does one iteration test all notes, or just the oldest? (nothing defines it) | **UNDEFINED.** Step 1.1 validates "the oldest file" (singular). On rejection it "fall[s] through to the hypothesizer" — it does not say "then validate the next-oldest." On acceptance, Step 1.3 moves only that one file. Nothing states whether surviving sibling notes wait for the *next iteration* or are drained in the same iteration. |

**Verdict (c): COMPLETES-WITH-RISK.** "Oldest first, before machine hypotheses"
is stated, but it is not *unambiguous*: the sort key for "oldest" is unspecified,
and the single-note-vs-drain-all processing semantics over multiple notes is
undefined. Two plausible agents could order the same inbox differently (mtime vs
filename date), and one could leave a valid older sibling untested while testing a
newer note. **Recommendation:** pin "oldest" to a specific key (e.g., filename
date-prefix, else file mtime) and state whether one iteration loops over all
inbox notes or consumes exactly one per iteration.

---

## (d) Inbox note repeats an already-REVERTED hypothesis — does the guard catch it?

**Setup:** the campaign has a prior REVERTED iteration `iter-NNN` whose hypothesis
is recorded in `loop/learnings.md` (Step 7 appends on REVERT). The founder now
drops a well-formed inbox note proposing the same causal change, possibly reworded.

**Trace:**

| # | Question | Directive (file → cite) | Assessment |
|---|----------|------------------------|------------|
| 1 | Is the reverted record in the hypothesizer's input? | Learnings format: "The loop never repeats a failed hypothesis... appends here" (learnings.md header); REVERT iterations DO append (§4 Step 7). Hypothesizer input #2 = `loop/learnings.md` (hypothesizer.md → Your inputs) | YES — learnings.md holds the prior REVERT and is a normal input even when the source is the founder note (Step 1.2 "alongside the normal inputs") |
| 2 | Does the guard apply to inbox input? | "so its never-repeat and one-causal-change guards still apply" (PROGRAM §4 Step 1.2, explicitly about founder notes); "Check learnings first. Never repeat a hypothesis that already failed. If a similar approach was tried and reverted, explain why THIS time is different" (hypothesizer.md → Rules) | YES — the guard is explicitly asserted to apply to the founder-sourced hypothesis |
| 3 | Is the guard *deterministic*? | (no validation machinery anywhere; PROGRAM §1: "There is NO deterministic validation in the pipeline") | NO — enforcement is a prompt-level instruction to an LLM sub-agent. It must *recognize* the replay despite possible rewording and then either decline or justify the re-attempt. Nothing structurally compares the inbox note against `learnings.md`. |

**Verdict (d): COMPLETES-WITH-RISK.** Feeding the note through the hypothesizer
*does* put the guard in a position to catch a reverted replay — `learnings.md`
(containing the REVERT record) is passed alongside the founder note, and Step 1.2
explicitly re-affirms that the never-repeat guard applies to inbox input. But the
guard is soft: it relies on the LLM recognizing a reworded replay and, even when
recognized, the rule *permits* a re-attempt if the model justifies "why this time
is different." There is no deterministic block, so a replay *echoing verbatim* is
almost certainly caught, but a *semantically same / differently-worded* one is
caught only to the extent the model's learnings-check succeeds. **If** the 
reverted hypothesis was never written to `learnings.md` (e.g., the iteration
ended INCONCLUSIVE before Step 7 of BEFORE any learnings entry, or learnings was
edited non-append-only), the guard has nothing to check against and the replay
would pass through — this is mitigated because PROGRAM asserts REVERT always
records a learnings entry (§4 Step 6/7).

---

## Summary of verdicts

| Scenario | Verdict | Key risk |
|----------|---------|----------|
| (a) well-formed note → hypothesizer → hypothesis.md → used/, guard applied | **COMPLETES** | no check that `Change:` targets an editable file |
| (b) vague/multi-change note → REJECTED-, no guess, fall-through | **COMPLETES** | README "hand it back" vs PROGRAM "archive REJECTED" cosmetic mismatch |
| (c) multiple notes → oldest-first | **COMPLETES-WITH-RISK** | sort key for "oldest" undefined; single-note vs drain-all not defined |
| (d) reverted replay caught by guard | **COMPLETES-WITH-RISK** | guard is prompt-level/soft, not deterministic |

**BLOCKED:** none.
**UNDEFINED:** (within (c)) the sort key for "oldest" and whether multiple inbox
notes are drained in one iteration vs one-per-iteration.

## Open questions for the founder/orchestrator

1. What exactly does "oldest file" mean — filename date prefix, `mtime`, or
   creation order? Pin a key (and a tie-break).
2. If two valid notes sit in the inbox, does one iteration test only the oldest
   (deferring the rest to later iterations) or drain all inbox notes oldest-first
   before falling back to the machine hypothesizer? If only the oldest, a rejected
   oldest can starve a valid sibling.
3. Should a deterministic replay check be added — e.g., compare the inbox note's
   `**Change:**` against `learnings.md` change strings — or is the prompt-level
   "check learnings first" guard the intended ceiling? (Current design gives the
   LLM the data and the instruction, but no hard block.)
