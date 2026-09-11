# Factory subjects

Same factory files (writer, reviewer, style-guide, plan-skill). Different
brief, research, plan, reference, alignment. One book per subject per
iteration (replicate-a). Founder 2026-09-05: K1.

| slug | Reference | Alignment | Moves |
|---|---|---|---|
| `quit-sugar` | `calibration/reference/gsbs` | `loop/reference-alignment-quit-sugar.md` | `loop/reference-moves-quit-sugar.md` |
| `quit-smoking` | `calibration/reference/easyway-smoking` | `loop/reference-alignment-quit-smoking.md` | `loop/reference-moves-quit-smoking.md` |

Write (auto-research starts a factory conversation per subject; it does not
itself write chapters):

```bash
dotenvx run -f .env -- opencode run --dir "$PWD" --agent factory \
  --model opencode-go/muse-spark-1.3-contributor --variant xhigh --auto \
  "Read prompts/factory-orchestrator.md. SLUG=quit-sugar ITER=NNN REPLICATE=a. Research is on disk. Plan loop then chapter loops until FACTORY DONE."
```

Judge:

```bash
dotenvx run -f .env -- env BC_REPO="$PWD" ITER=NNN SLUG=quit-sugar REPLICATE=a \
  REF_DIR="$PWD/calibration/reference/gsbs" \
  ALIGNMENT="$PWD/loop/reference-alignment-quit-sugar.md" \
  MOVES="$PWD/loop/reference-moves-quit-sugar.md" \
  python3 -u scripts/loop-runner/judge_replicate.py
```

Smoking swaps `SLUG=quit-smoking`, `REF_DIR=.../easyway-smoking`, and the
`-quit-smoking` alignment/moves files. One judge runner at a time.
