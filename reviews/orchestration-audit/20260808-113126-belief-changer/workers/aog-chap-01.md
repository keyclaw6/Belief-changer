# Worker shard — AOG-CHAP-01 (chapter-writing entity reviewer)

- Reviewer: GPT-5.6 Terra medium sub-agent (nickname Fermat), read-only
- Scope: chapter-writer.md, .pi/agents/chapter-writer.md, style-guide.md writer-facing portions, writer config, PROGRAM writing/refusal path
- Entities reviewed: 20 grouped/full — 19 PASS, 1 candidate

## Candidate

### CAND-AOG-CHAP-01-001 — Writer reasoning and temperature are declared but not enforceably dispatched (MATERIAL-RISK, MEDIUM/HIGH)

Evidence:
- loop/config.yaml:2-3,11-16 declares sole authority + writer parameters (reasoning high, temperature 0.7)
- loop/PROGRAM.md:37-39 "no value elsewhere overrides config"; :41-54 orchestrator spawns thin .pi roles per configured route
- .pi/agents/chapter-writer.md:1-16 pins only `model` — no reasoning/temperature/endpoint/no-cap dispatch
- repo-wide search: writer_reasoning/writer_temperature appear only in config.yaml; run_preflight.sh reads only judge params

Mismatch: declared writer reasoning/temperature have no repository consumer in the spawn path. Causal mechanism: changing config values does not change the actual chapter-writer spawn; calibration trace can attribute output to parameters that were not applied. Reachable: any campaign testing writer-temperature/reasoning hypothesis. Impact: invalidates reproducibility and causal attribution for expensive whole-book iterations.

## Passes
- Four runtime inputs match PROGRAM §3 exactly; ch-01 previous-context exception correct
- Refusal format coherent with PROGRAM error handling (no chapter file; refusal traced; INCONCLUSIVE)
- Missing-mantra and unresolvable-ID refusals route upstream to `plan`
- "Check the one job" is agent self-check, not deterministic validation — no conflict with zero-deterministic-validation rule
- Removed commissioner/chapter-reviewer loop leaves no active writer-stage dependency; style-guide.md:570,576 "reviewer/chapter reviewer" references are historical/generic prose (judges perform those checks now)
- Refusal owner vocabulary broader than stage labels but coherent as upstream defect classification

## Integrity
- No files written; no services called.
