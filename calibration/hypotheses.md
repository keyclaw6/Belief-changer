# Hypothesis Ledger — factory calibration

The science log of the calibration loop. One entry per hypothesis; the operator updates statuses every run (HARNESS §6). Amendments to method assets are only legitimate as tests of a ledgered hypothesis. **REFUTED requires an examined autopsy (HARNESS §10) — mechanism + evidence, never a preemptive burial.**

**Entry format:**

```
## H-NNN — <short name>            [PROPOSED | TESTING run-NNN | SUPPORTED | REFUTED | RETIRED]
- Gap: <observed/expected failure — mechanism, not resemblance to the reference>
- Lever: <the ONE generic asset or config + the change>
- Prediction: <which metric/judge dimension moves, direction>
- Result: <what happened; run refs; if REFUTED: the autopsy (WHY, with evidence)>
```

Seeded by the harness builder (2026-07-10) as starting capital — derive priorities from run-001's diagnosis; statuses and new entries are yours (operator). Constants, not hypotheses: writer = Opus 4.6 reasoning-none (founder-FIXED); the anti-repetition context law; the mantra law.

---

# Research stage

## H-026 — explicit caller/role capability boundary       [TESTING bootstrap-pilot]
- Gap: bootstrap call `gen-1783695448-rncCEIxtMXRtDVRaHkwv` spent $0.0170415 then stopped before the assignment matrix because the bare Luna submodel could neither inspect its invisible OpenRouter request metadata nor write the caller's repository, even though both had already been handled externally.
- Lever: `prompts/research-agent.md` assigns endpoint preflight, response metadata, and artifact persistence to the caller; lead/workers return artifact-ready blocks when direct file tools are absent.
- Prediction: the identical prompt+brief Luna `max` lead call returns provisional personas and a bounded pre-collection matrix instead of a tool-access refusal.
- Result: RP-000 blocked with zero sources/cells. The correction removed that refusal mechanism: later Luna traces planned the artifact, and DeepSeek RP-003/RP-005 returned artifact-ready matrices without demanding endpoint/file tools. The mechanism is supported across those calls, but the prediction named a visible Luna artifact and Luna exhausted its output caps; keep TESTING until the clean bounded Luna worker arm either returns an artifact or reproduces the refusal.

## H-027 — self-contained assignment rows                 [REFUTED bootstrap-pilot]
- Gap: DeepSeek lead call RP-003 returned 42 planned cells, but repeated `same` shorthand made later rows non-reconstructable and it selected an eating-disorder community despite that population being a brief non-goal.
- Lever: `prompts/research-agent.md` requires every row to repeat its full scope/query/model fields, validates named communities, and treats brief non-goals as research-scope exclusions.
- Prediction: the exact-input DeepSeek `xhigh` rerun contains no shorthand, no excluded population, and passes the pre-collection matrix gate without operator repair.
- Result: RP-005 removed `same` shorthand and excluded clinical populations, but still grouped Banks 1–5/9/10 in single cells and hid conditional supplemental communities in queries. Autopsy: the lever named field repetition but did not explicitly define a one-bank/one-scope row, so the model preserved compactness along an unguarded axis. The matrix remained non-dispatchable; see `calibration/pilots/deep-research-bootstrap.md`. Corrected as H-028 rather than silently widening H-027 after its outcome.

## H-028 — one-bank, one-scope matrix cells               [TESTING bootstrap-pilot]
- Gap: RP-005 is readable but cannot serve as the file boundary: grouped bank cells cannot hold per-bank yield/verdict, and fallback communities make the assignment's source scope mutable after dispatch.
- Lever: `prompts/research-agent.md` requires exactly one numeric bank and one fixed community/source family per row; every fallback/follow-up is a separately declared row.
- Prediction: the next allowed lead call returns only single-bank/single-scope rows with no `same`, bank ranges, conditional supplements, vague source families, or excluded populations.
- Result: The first MiniMax call was aborted on brief contamination and has no outcome. Clean call `gen-1783697696-Q9YjzSVhZnKRHPJSDLfz` planned one-bank rows but expanded 6 personas × 2 communities into 91 rows and exhausted 30,000 completion tokens before emitting the matrix ($0.03696534; 28,286 reasoning tokens). Its visible plan supports H-028's atomicity mechanism, but no matrix rows were returned, so the full no-shorthand/no-fallback prediction remains untested. H-029 corrects the adjacent source-semantics and output-bounding failure; the next complete lead artifact tests both hypotheses.

## H-029 — lean primary matrix and source semantics       [TESTING bootstrap-pilot]
- Gap: a formally atomic matrix can still be unusable when persona overlap and preemptive multi-community duplication create 91 rows before any yield is observed.
- Lever: `prompts/research-agent.md` defines a source as a distinct URL/document, starts with the smallest distinct 3–4 personas, plans one primary community row per persona/bank, and adds communities only as measured follow-ups.
- Prediction: the next clean allowed lead returns a complete artifact with 3–4 personas, single-bank/single-scope rows, no shorthand/fallbacks, and no output-cap truncation.
- Result: pending clean DeepSeek V4 Pro `xhigh` lead call.

## H-009 — researcher-model arms (cost/depth bake-off)   [TESTING bootstrap-pilot]
- Gap: research is the highest-token stage; unknown which model mines communities and synthesizes banks best per dollar.
- Lever: manifest only, always top reasoning — R1 `deepseek/deepseek-v4-pro` (`xhigh`) · R2 `minimax/minimax-m3` (reasoning enabled; no effort ladder reported) · R3 GPT 5.6 Luna (`max`).
- Prediction: measurement; expect the long-context low-cost arms to lead cost-per-slot-filled, with verbatim provenance and synthesis quality the open questions.
- Result: Contaminated preflight calls are excluded. First clean broad-lead result: MiniMax reasoning-enabled returned no complete matrix at a 30k cap ($0.03696534; 28,286 reasoning tokens) because it planned 91 rows. This is orchestration-yield evidence only, not the bounded equal-assignment source-yield result; clean DeepSeek lead and all three bounded worker arms remain pending.

## H-010 — multi-subagent research vs one long prompt    [PROPOSED]
- Gap: a single agent with a long prompt searches shallowly, samples few communities, and paraphrases quotes (founder-observed pattern).
- Lever: research-lead prompt spawns focused sub-researchers (per community, per persona, per bank slot) that return verbatim yield; lead merges into banks. Single-long-prompt = baseline arm.
- Prediction: multi-subagent wins bank-slot coverage, unique-community count, and verbatim-quote yield at equal spend.
- Result: —

## H-011 — adopt/tune an OSS deep-research framework     [TESTING — source audit NO-GO]
- Gap: building deep research from scratch may duplicate solved work (parallel source connectors, dedup, fact-check layers).
- Lever: evaluate against the H-010 prompt-structured build: `langchain-ai/open_deep_research` (`408da44`), `RobertoDeLaCamara/Research-Agent` (`b30eed2`), and `extracurricular-ai/open-deep-research-with-web-ui` (`9c3da13`).
- Prediction: per §13 doctrine, adopt ONLY if it beats the prompt-structured approach on bank coverage/quote yield at equal spend — expect the prompt-structured build to win on fit, the OSS on connector breadth.
- Result: 2026-07-10 source audit: NO-GO for run-001 adoption. All three lack the community × persona × bank-slot schema, quote-to-raw-source verification, factory file outputs, and complete top-reasoning OpenRouter config. LangChain offers useful generic fan-out but needs all five core modules changed; Research-Agent's "Reddit" support is one site-search and its evaluator sees synthesis rather than sources; the smolagents fork has no Reddit/forum connector and carries UI/media/session machinery. Each would require a core rewrite plus dependencies, so H-010 is the run-001 baseline. Keep LangChain only as a future equal-assignment arm if prompt handoffs fail or orchestration becomes a measured bottleneck; no quality claim is yet refuted.

## H-012 — persona research quotas                        [PROPOSED]
- Gap: research banks skew toward the loudest persona (young heavy users), starving framing's persona set and the future splitting seams.
- Lever: research-agent prompt — per-persona minimum yield quotas (items + quotes per persona) before research may close.
- Prediction: framing personas cite ≥N items each; Stage B persona notes stop being thin; warmth/click steadier across sampled chapters.
- Result: —

## H-013 — dedicated community-lexicon harvester          [PROPOSED]
- Gap: the two-register lexicon sheet (style guide Part B) is only as good as the community's own words; generic research yields generic lexicon.
- Lever: research-lead spawns one sub-researcher solely for lexicon: the community's words for the behavior, the shame, the quitting, the freedom — with frequency notes.
- Prediction: lexicon sheet passes the "reader's inner voice" stress test; voice + warmth win-rates rise.
- Result: —

# Plan stage

## H-005 — planner-model arms                             [PROPOSED — REVISED 2026-07-10]
- Gap: unknown which model plans this book architecture best. (Supersedes the writer-arms version: founder fixed the writer to Opus 4.6 reasoning-none.)
- Lever: manifest only, always top reasoning — P1 GPT 5.6 Sol (OpenRouter `max` or pinned native Codex `ultra`) · P2 Gemini 3.1 Pro (`high`) · P3 Grok 4.5 (`high`). Opus is chapter-writer-only. Same inputs, same prompts.
- Prediction: measurement; judged by plan-review cycles to "fit to write from" + downstream chapter judge scores off each plan.
- Result: —

## H-007 — planner reasoning effort                       [RETIRED — founder-fixed 2026-07-10]
- Gap: a reasoning-effort sweep was proposed before the founder fixed every allowed non-writer model to its top supported reasoning mode.
- Lever: none — configuration is now a constant, not a calibration variable.
- Prediction: retired without a model call; no quality claim was tested or refuted.
- Result: Superseded by the fixed top-reasoning rule in HARNESS §8.

## H-001 — explicit per-chapter word budgets              [PROPOSED]
- Gap: nothing in the plan template forces chapter lengths, so book length is emergent, not planned (HARNESS §7 requires planned).
- Lever: master-plan prompt — curve map assigns every chapter a word budget summing to 0.9–1.1× target; each chapter spec carries its budget.
- Prediction: total_words ratio into ±15%; per-chapter deviations < ±20%.
- Result: —

## H-016 — reference-shaped length curve vs uniform       [PROPOSED]
- Gap: real Carr books breathe — long demolition chapters, short bridge chapters; uniform budgets may read as mechanical pacing.
- Lever: master-plan prompt — operator supplies numeric curve targets (chapter-length distribution shape, from reference-metrics.json aggregates; pipeline stays text-blind) vs flat budgets, both summing to target.
- Prediction: pacing_distribution and flow rise under shaped curve at equal total length.
- Result: —

## H-014 — belief-state trajectory in the plan            [PROPOSED]
- Gap: chapter specs say what a chapter DOES, not what the reader BELIEVES after it — so escalation is implicit and drifts.
- Lever: master-plan prompt — a belief ledger line per chapter: "after ch N the reader believes …"; reviewer checks the trajectory is monotonic toward the quit.
- Prediction: click and escalation (Stage B arc judge) rise; fewer mid-book sag flags.
- Result: —

## H-015 — per-chapter "objection to kill"                [PROPOSED]
- Gap: chapters argue FOR conclusions but under-address the reader's live counter-thought, so the click doesn't land for skeptical readers.
- Lever: master-plan prompt — each chapter spec names the single strongest reader objection it must dissolve (sourced from the justification menu / research banks).
- Prediction: click win-rate rises; judge notes stop citing "asserted, not argued".
- Result: —

## H-017 — mantra debut front-loading                     [PROPOSED]
- Gap: if debuts spread evenly, late chapters debut new refrains with no runway to compound — the spine feels thin at the end.
- Lever: master-plan prompt — schedule guidance: majority of mantra debuts in the first ~40% of chapters; the back half echoes and escalates.
- Prediction: refrain_spine + ending_force rise at Stage B; mantra_discipline unchanged at Stage A.
- Result: —

## H-002 — chapter-opening variety rule                   [PROPOSED]
- Gap: writers converge on one opening move (typically a question) when the spec doesn't forbid it; judges read template smell.
- Lever: master-plan prompt — structural slots record each chapter's opening MOVE (scene / assertion / question / callback / instruction), no two consecutive alike.
- Prediction: flow and voice win-rates rise; no objective metric regresses.
- Result: —

## H-004 — explicit hand-over hooks in the plan           [PROPOSED]
- Gap: previous-chapter-only context gives local continuity, but chapter ENDINGS under-set the next chapter's opening promise.
- Lever: master-plan prompt — every chapter spec carries "opens from:" and "hands to:" one-liners; reviewer checks the pair.
- Prediction: flow rises; whole-book escalation rises at Stage B.
- Result: —

# Writer stage (model FIXED — these tune how it writes)

## H-003 — echoes land at argumentative peaks             [PROPOSED]
- Gap: scheduled mantra echoes placed as paragraph-end garnish read as pasted rhythm, not conviction.
- Lever: chapter-writer prompt — an echo lands where the argument it compresses has just been re-earned (post-demolition beat), never as a section sign-off by default.
- Prediction: mantra_discipline win-rate rises with schedule compliance unchanged.
- Result: —

## H-018 — best-of-2 drafts, reviewer picks               [PROPOSED]
- Gap: single-draft chapters inherit one sampling path's tics; the reviewer can only patch, not choose.
- Lever: loop config — writer produces 2 independent drafts (same inputs); reviewer picks the stronger, then iterates it.
- Prediction: judge scores rise ~0.5+ mean; cost ×2 at write stage — evaluate value per dollar honestly.
- Result: —

## H-019 — regenerate-with-addendum vs revise             [PROPOSED]
- Gap: iterative revision accumulates drift (patched prose reads patched; earlier tics survive edits).
- Lever: loop config — on reviewer feedback, regenerate the chapter fresh with the feedback appended to the spec, instead of editing the prior draft.
- Prediction: fewer cycles to ACCEPT; higher voice scores on accepted chapters.
- Result: —

## H-020 — sampling temperature sweep                     [PROPOSED]
- Gap: default sampling may be too hot (voice wobble) or too cold (flat, listy) for this register; untested.
- Lever: manifest only — writer temperature {default, −0.2, −0.4} on the same chapter specs.
- Prediction: measurement; watch voice win-rate vs within-book repetition count moving in opposite directions.
- Result: —

## H-021 — one-pass vs sectioned chapter writing          [PROPOSED]
- Gap: writing a chapter in sections (continue-from) plants seams; but one-pass may lose the spec's beat structure in long chapters.
- Lever: chapter-writer protocol — full-chapter single pass vs section-by-section continuation, same specs.
- Prediction: one-pass wins flow at ≤3k words; sectioned may win only above that (which shaped budgets, H-016, make rare).
- Result: —

# Review stage

## H-006 — reviewer criteria aligned to judge dimensions  [PROPOSED]
- Gap: chapter reviewer can ACCEPT chapters that pairwise judges then score low — the two measure different things.
- Lever: chapter-reviewer prompt — add the six judge dimensions as explicit accept criteria (without naming judges or the reference).
- Prediction: fewer wasted writer↔reviewer cycles; higher judge scores per accepted chapter.
- Result: —

## H-022 — two-pass review (method, then prose)           [PROPOSED]
- Gap: one combined checklist lets prose polish mask method violations (and vice versa) — attention splits.
- Lever: chapter-reviewer protocol — pass 1 judges method integrity + spec fidelity only; pass 2 judges prose only; both must accept.
- Prediction: post-ACCEPT critical failures drop to zero; cycles rise slightly, quality per cycle rises more.
- Result: —

# Loop & evaluation

## H-023 — judge ensemble size vs verdict stability       [PROPOSED]
- Gap: 12 judgments per Stage A run may be too noisy to steer by (win-rate swings between identical candidates).
- Lever: eval config — same candidate judged at 12 vs 24 judgments; compare win-rate variance.
- Prediction: pick the cheapest ensemble whose verdict is stable within ±0.05; expect 12 to suffice with 2 families.
- Result: —

## H-024 — detection probe as leading indicator           [PROPOSED — analysis-only]
- Gap: unknown which gate metric moves first as quality converges; steering by a lagging metric wastes runs.
- Lever: none — ledger analysis across runs: does real-Carr detection accuracy falling precede win-rate gains?
- Prediction: detection drops before win-rate rises (judges stop *knowing* before they stop *preferring*).
- Result: —

# Tooling

## H-008 — tooling adoption (scripts vs framework)        [PROPOSED — operator's decision]
- Gap: operator orchestration may bottleneck on sub-call management (fresh contexts, retries, parallel sub-researchers) as runs scale.
- Lever: HARNESS §13 — prompts/handoffs first; a runner or framework (Agents SDK / PI fork) only after a prompt-level fix has failed twice, autopsied.
- Prediction: adopt only if it measurably cuts run wall-time or error rate; log what it replaced.
- Result: —

## H-025 — MLflow at full depth                           [PROPOSED — operator's decision, all-or-nothing]
- Gap: cross-run diagnosis from raw git JSON may consume operator time as runs accumulate.
- Lever: HARNESS §10 — adopt MLflow in FULL depth (GenAI tracing of every sub-call, params/metrics/artifacts per run, prompt-registry for method-asset versions, comparison UI; local store, gitignored) — or not at all. Decide by ~run-003.
- Prediction: adoption pays if time-to-diagnosis per run drops visibly; git stays canonical either way.
- Result: —
