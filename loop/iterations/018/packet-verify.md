# Packet verify — iteration 018

Verified against `grok-packet.md`, `change.diff`, `hypothesis.md`, and live repo state (`git diff` in `/home/kab/quit-sugar-iter-018`).

## Check 1 — diff scope

**PASS**

- `git diff --name-only`: only `prompts/chapter-writer.md`
- `git diff --stat -- prompts/`: `prompts/chapter-writer.md | 2 +-` → 1 insertion, 1 deletion, one file
- Working tree: no other modified tracked files; `loop/iterations/018/` untracked only

## Check 2 — SEARCH/REPLACE line

**PASS**

Packet REPLACE (expected NEW line, exactly once):

```
  mantra, or device-code strings, no beat names, no trap-question or Socratic-trap prefixes, no chapter-number callbacks
```

Found once at `prompts/chapter-writer.md` line 64 — byte-for-byte match (two leading spaces; straight ASCII quotes and hyphens).

Old SEARCH without the clause (`no beat names, no chapter-number callbacks` with no trap prefix in between): **0 occurrences**.

`change.diff` hunk matches packet SEARCH/REPLACE exactly.

## Check 3 — 014 KEEP preservation

**PASS**

- `prompts/style-guide.md` vs `4cac0ae` (014 KEEP): **0 diff lines** (identical)
- style-guide still contains:
  - `Ask, don't assert.` (§5.8)
  - `Pose the question whose only honest answer dismantles the belief` (§5.8)
  - `trap questions whose only honest answer concedes the point` (§9)
- chapter-writer.md (014 W1 unedited): `land one short verdict` present (line 46)
- Anatomy item 5: `the numbered ALL-CAPS spoken imperative` (line 124) — not `spoken headline` (0 matches)

## Check 4 — NO-GO absent from diff

**PASS**

`change.diff` is a single hunk in `prompts/chapter-writer.md` only. None present in diff or resulting writer text:

| NO-GO item | In 018 diff? |
|---|---|
| echo-ID-only | no |
| echo-density | no |
| evidence-ID-only | no |
| instruction-headline | no |
| job-ownership | no |
| W3 | no |
| `**Ask.** The question is the next sentence` | no |
| stop on the verdict sentence | no |
| style-guide edits | no |
| anatomy item 5 change | no |

## Check 5 — hypothesis alignment

**PASS**

- One causal change: never-surface `trap-question or Socratic-trap prefixes` in writer never-surface list
- One file, one line (`hypothesis.md` targeted fix)
- Plan regen: **no** — reuse 014 15-chapter plan
- Research: **reuse**

## Overall

**PASS**
