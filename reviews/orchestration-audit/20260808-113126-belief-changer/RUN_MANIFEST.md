# RUN MANIFEST — agent-orchestration-auditor

- **Run ID:** 20260808-113126-belief-changer
- **Repository root:** /home/kab/Belief-changer
- **Repository name:** Belief-changer
- **Branch / commit:** main @ f9ceda5 ("refactor(loop): zero deterministic validation in the factory")
- **Baseline status:** clean working tree (no staged/unstaged/untracked changes at start)
- **Start time:** 2026-08-08T11:31:26Z
- **Audit root:** `reviews/orchestration-audit/20260808-113126-belief-changer/`
- **Applicable repository instruction files:** `AGENTS.md` (on-disk), `docs/VISION.md`, `docs/BOOK-FACTORY-VISION.md`, `docs/AUTO-TUNING-LOOP.md`, `loop/PROGRAM.md`, `loop/config.yaml`
- **Lead agent:** Codex coding agent (this session); skill root `/tmp/aog-skills-mqOugl/agent-orchestration-auditor`
- **Sub-agent mechanism:** native sub-agent spawn; reviewers run as GPT-5.6 Terra medium, read-only (explicit instruction: no writes, no commits)
- **Concurrency:** pi subagent extension caps MAX_PARALLEL_TASKS=MAX_CONCURRENCY=10 (founder-set); audit fan-out is lead-controlled in waves
- **Read-only commands used:** git status/log/remote; rg/cat file reads; systemctl --user status commandcode-proxy; read-only GET probes to local loopback services (127.0.0.1:3050/v1/models, 127.0.0.1:10100) — no credentials exercised, no POST, no external side effects
- **Scope:** research stage and book-writing stage (planning + chapter writing) of the factory, including orchestration glue, routing config, and cross-stage handoffs. Judges/trace-analyzer/hypothesizer are consumers only (referenced, not entity-reviewed).
- **No production side effects were exercised.**
- **Final source-integrity comparison:** pending (Phase 9)
- **Intended final commit:** `audit(orchestration): 20260808-113126-belief-changer`
- **Git commit prerequisite:** available — repo is Git-backed on `main`, no config/signing/hook changes needed
