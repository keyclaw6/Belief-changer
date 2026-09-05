# Factory subjects

Same factory files (writer, reviewer, style-guide, plan-skill). Different
brief, research, plan, reference, alignment. One book per subject per
iteration (replicate-a). Founder 2026-09-05: K1.

| slug | Reference | Alignment | Moves |
|---|---|---|---|
| `quit-sugar` | `calibration/reference/gsbs` | `loop/reference-alignment-quit-sugar.md` | `loop/reference-moves-quit-sugar.md` |
| `quit-smoking` | `calibration/reference/easyway-smoking` | `loop/reference-alignment-quit-smoking.md` | `loop/reference-moves-quit-smoking.md` |

Write:

```bash
dotenvx run -f .env -- env BC_REPO="$PWD" ITER=NNN SLUG=quit-sugar REPLICATE=a \
  python3 -u scripts/loop-runner/write_replicate.py
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
