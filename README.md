# Belief-Changer — truth-first factory v2

An original belief-change book factory: deep source-traceable research → evidence review → argument planning → chapter writing/review with actual manuscript state → whole-book editing → assembled-publication audit → calibrated experiments → explicitly approved immutable releases.

**Status:** software upgrade with offline tests; no validated v2 champion or measured reader-effectiveness result. Historical campaign-001 manuscripts and iterations 000–050 are preserved, not silently rewritten or relabeled as validated output.

## Start here

Requires Python 3.11+; no third-party Python packages for runtime/tests.

```bash
bash scripts/check.sh
python3 scripts/factory.py demo --output /tmp/belief-changer-v2-demo
python3 scripts/factory.py --help
```

The demo uses synthetic responses and makes no model calls. Its outputs cannot be promoted. See **docs/FACTORY-V2.md** for the complete workflow, provider setup, schemas, revision rules and release gates. **docs/EXPERIMENTS-AND-READERS.md** covers controlled ablations, human calibration and reader pilots. **docs/UPGRADE-MAP.md** maps audit findings to implementation/tests and states remaining empirical work.

## What changed

Frozen, content-hashed runs replace mutable live plans. Strict shared schemas replace marker-string acceptance. Missing work cannot print successful completion. Reviewer caps remain failures. Output guarantees and narrator credentials are evidence-checked. Original prose and argument quality replace author indistinguishability. Blinded, order-reversed, independent judging and calibrated promotion preserve a champion instead of allowing experimental drift.

Default generator route names are preserved in factory/config.json. Independent evaluator configuration is intentionally unset until explicitly selected. `--allow-paid` is required for model execution. No live provider requests are part of tests/CI.

Credentials are local only; copy `.env.example` and configure your environment or existing encrypted local dotenvx setup. The download archive omits `.env`, private keys, caches and `.git`. Third-party research/reference assets retain their existing rights; their presence is not a license grant.

Operational authority: AGENTS.md → docs/FACTORY-V2.md and loop/PROGRAM.md. Old operating instructions are under archive/campaign-001-runtime/ for historical audit only.
