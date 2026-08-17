# Handoff — Continue the auto-tuning loop, baseline (iteration 000)

Written 2026-08-17, plain-language. Read `loop/PROGRAM.md` + `docs/AUTO-TUNING-LOOP.md` if you want the dry rules; this file tells you where we are and what to do next.

## What we're doing

Running the **baseline run** of the book-factory auto-tuning loop on branch `campaign-001`.
Stage order: research → plan → write all chapters → judge → analyze traces → record results.

## Where we actually are

- **Research is ~90% mined but NOT finished.** Ten banks exist under
  `production-books/quit-sugar/research/banks/` with ~994 evidence packets.
- **Synthesis NEVER ran.** `lived-experience.md` and `scientific-evidence.md` are still empty templates.
- **Nothing from the run is committed to git** — all banks are untracked files. The prior session died mid-task and never saved. Fix that first: **commit a checkpoint.**

## What's broken / needs fixing before going further (in order)

1. **Commit what we have.** Banks + `research-log.md` + `web_tools.py` + `state.md` are all uncommitted on `campaign-001`. Commit now so a crash can't lose it again. **(Do this first!)**
2. **Clean bank-09.** `bank-09-lexicon.md` lines 262–399 are garbage — a sub-agent dumped its own chain-of-thought ("GO GO GO. Emit.") into the file. Delete those lines; the real lexicon is lines 1–261.
3. **Two spec violations to patch before acceptance:**
   - Bank-07 is ~88% from the PMC domain. Rule: no lane may draw >50% of entries from a single domain. Run a quick gap-fill for a few non-PMC institutional sources.
   - Bank-02 has zero P-04 persona packets. Rule: every slot across ≥3 personas. Gap-fill some P-04 entries.
4. **Finish the research stage:**
   - Fill the audit tables in `research-log.md` (they're all blank).
   - Write the two synthesis files from the banks (`lived-experience.md`, `scientific-evidence.md`).
   - Build `sources/` ledger files for the cited URLs.

## Order of operations after that

Research done + committed → **Planning**: spawn plan-writer sub-agent → it writes `master-plan.md` → plan-reviewer until it says "fit to write from" → build `loop/reference-alignment.md`.
Then **Writing**: one chapter at a time (`chapter-01.md` …) with the writer role (Muse Spark via `http://127.0.0.1:3050/`, key in `~/.commandcode/auth.json`, `max_tokens` must be large or it returns empty content).
Then **Judging** → **trace analysis** → **record into `loop/results.tsv`** → mark iteration 000 done in `loop/state.md`.

## Warnings — what bit us last time

- **Commit after every logical stage.** The whole failure was: work happened, nothing was saved, session died.
- **Sub-agents can spew their thinking into files** (see bank-09). Always verify the tail of a sub-agent-written file.
- **Muse Spark returns `content: null` when `max_tokens` is small.** Always pass a big budget.
- **Search engines are flaky from this machine** — `scripts/loop-runner/web_tools.py` was patched (Marginalia-first + Bing fallback). Don't nuke that file.
- Follow the `.partial` → rename convention for chapter files (write `chapter-01.md.partial`, rename when complete).

## Checkpoint files

- `loop/state.md` — the live status file, updated at every stage boundary.
- `loop/results.tsv` — results table (currently just a header row).
- `loop/learnings.md` — lessons file (currently empty).
- `production-books/quit-sugar/research/` — the banks + synthesis files.
- Branch is `campaign-001`; commit there. Only `main` gets merged/preflight pieces.