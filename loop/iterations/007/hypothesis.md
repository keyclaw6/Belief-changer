## Failure evidence
Cluster 1 Speakable craft labels — systemic (17/20 chapters `trap question`; C01 `ease-operator`), leak scan corroborated. Voice-emotion still 15/20 FAIL on residual craft-label distance; headline literals closed but this class persists. Evidence: C02 `"Let me ask you the trap questions that only have one honest answer"`; C18 `"Do you feel the trap question?"`; C01 line 158 `"ease-operator"` at instruction peak (Gap 2); iteration-006 leak scan 17 chapters vs Gate 4 PASS on cards. Previous hypothesis predicted full closure of Cluster 6 — verdict PARTIALLY CLOSED, plan-card layer closed, writer execution layer not.

## Root cause
Trace Analysis 006 Section 1 attributes residual to **writer-prompt + style-guide**, not cards. Cards sanitized: `traces/chapter-02/chapter-card.md` line 16 `Devices: ask the disarming question…` (no literal), reviewer rounds 2-3 PASS on Gate 4. Contradiction remains at runtime: `prompts/chapter-writer.md` line 54 bans `no internal drafting or craft labels` but lines 44 and 92-93 require `trap questions, killer-line pair, future-pacing, fact-assertion` by name (same contradiction in `traces/chapter-02/system.txt` 44-54 vs 92-93). Parallel source `prompts/style-guide.md` injected via `traces/chapter-02/user.txt` lines 1156, 1169, 1278 uses `trap question` as method vocabulary, priming model to surface the label despite the ban. Factory asks model to execute a named device while forbidding its name.

## Targeted fix
**File: `prompts/style-guide.md` — one causal change, subtraction-preferred.**

Replace the canonical speakable craft-label instructions with execute-silently behavioral instructions and delete exact duplicates. Do not edit `prompts/chapter-writer.md` in this iteration.

1. Replace every literal method label in Part B Prose Engine / §5-§7 toolkit and §9 where the guide names devices:

```diff
- trap question / trap questions
+ the disarming one-answer question (execute silently — never write the label "trap question" in reader prose)

- ease-operator
+ the way the substance eases the discomfort it itself created (never write the factory term "ease-operator")

- killer-line / killer-line pair, future-pacing, fact-assertion, argue-to-compress
+ the compressed verdict line (2-sentence) / the lived future moment / the plain fact stated without label / the compressed reframe (execute silently — never write the craft labels "killer-line, future-pacing, fact-assertion, argue-to-compress" in reader prose)
```

2. Delete exact duplicate occurrences of those literals in the same file and add single overriding ban in §9 Guardrails:

> **Speakable craft ban:** Never surface factory method vocabulary in reader prose — do not write `trap question, ease-operator, killer-line, future-pacing, fact-assertion, argue-to-compress` or persona handles. Execute the behavior described, do not name the device.

This supersedes current style-guide text that teaches `trap question` by name as method vocabulary at lines 1156, 1169, 1278. No other file touched.

**Why this component:** Writer-prompt already has 2 strikes on silent-execution (001 evidence-honesty, 005 Binding craft — REVERT, 0/18→5/20 only) and reviewer Gate 4 already closed the card layer (persona P-xx and `killer-line/future-pacing` now zero). The surviving source quoted by the trace is style-guide runtime injection, a fresh surface with zero strikes that Gate 4 cannot sanitize and that contradicts the writer-prompt ban — fixing it removes the model’s only remaining literal prime for this class.

## Predicted impact
**What will improve:** Cluster 1 will close because neither cards nor style-guide nor writer ban-contradiction primes the literal; `trap question` leak scan should drop 17/20 → 0, `ease-operator` C01 → 0, headline 005 literals remain closed. Voice-emotion PASS should rise from 5/20 toward majority (Cluster 1 is the pervasive residual gap across FAIL chapters).

**What might regress:** Nothing on belief-mechanic (20/20) or reader-journey (18/20) — behavior unchanged, only label surface removed. If replacement phrasing is too vague, disarming questions could weaken slightly in 1-2 chapters.

**How we'll know it worked:** `grep -r "trap question" loop/iterations/007/traces/` and reader files returns zero; voice judgments no longer quote craft-label gaps; C01 no `ease-operator`; persona-code remains 0.

Check learnings: not repeating 001, 002-004 plan-skill re-argument, 005 writer Binding silent-execution, or 006 Gate 4; this is new surface (style-guide) targeting the mutated writer-prompt contradiction identified in 006.
