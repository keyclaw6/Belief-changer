# Source of Truth — auto-research loop (dry-run audit)

Audited revision: `main` @ afca11f. Target: the LOOP orchestration (not book
content). In scope: `loop/PROGRAM.md`, `loop/state.md`, `loop/inbox/`,
`loop/ledger.md`, `loop/results.tsv`, `loop/learnings.md`,
`scripts/loop-runner/research_reuse.sh`, plus the loop-facing parts of
`AGENTS.md` and `docs/AUTO-TUNING-LOOP.md`.

## Declared precedence (from the repo)

1. `AGENTS.md` — constitution; points at the two locks below.
2. `docs/AUTO-TUNING-LOOP.md` — founder-locked North Star (mission/invariants).
   "No agent may weaken or reinterpret away" it.
3. `loop/PROGRAM.md` — sole operational runbook. Self-locked: "Never edit this
   PROGRAM.md. The loop follows it." (Founder authorized this session's edits.)
4. `loop/config.yaml` — sole model/route/parameter authority.
5. Role prompts under `prompts/` + `loop/prompts/` + `loop/judges/` — the
   tuning surface / contracts.

## Normative facts the dry runs must hold

- One causal change per iteration (§5).
- Whole book every iteration; research reused unless research/brief/config
  changed (§4 Step 3; `research_reuse.sh`).
- Decision valid only when every judge report completed (§4 Step 6).
- Recovery: `loop/state.md` Status (IDLE|IN PROGRESS) + results.tsv rule +
  marker cross-check (§0).
- Iterations run in git worktrees; only KEEP promotes to the campaign branch
  (§1 State discipline, §4 Step 6/7).
- Runner is patient: waits on `.exit`/content markers, no fixed timeout, stuck
  judged from traces (§4 Step 3).
