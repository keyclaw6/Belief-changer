# Grounded batch audit — run-012 R1

**Batch result: MATERIAL DEFECT — 3/3 chapters**

Three independent fresh `gpt-5.6-sol` contexts at `ultra` reasoning each received the complete canonical plan, one frozen source-grounded commission, only that chapter's assigned accepted packets, and the frozen R1 candidate. They received no reference text, judge material, metrics, competing draft, other chapter audit, or run outcome.

| Chapter | Verdict | Material findings | Raw decision |
|---|---|---:|---|
| C-01 | MATERIAL DEFECT | 13 | `grounded-chapter-01-r1.md` |
| C-02 | MATERIAL DEFECT | 6 | `grounded-chapter-02-r1.md` |
| C-03 | MATERIAL DEFECT | 8 | `grounded-chapter-03-r1.md` |

The defects span source attribution and identity, invented participant circumstances, unsupported prevalence and counterfactual outcomes, mechanism and efficacy inflation, conversion of a plan-authored reader voice into testimony, unassigned evidence imports, reserved-chapter argument, instruction ownership, clinical priority, and household safety. The exact candidate passages and controlling authority boundaries remain in the three raw decisions.

All three commissions had already passed the frozen pre-prose source-fidelity gate. Material evidence invention appears in all three first drafts. The batch therefore satisfies H-049's preregistered causal-refutation condition: faithful, adequately concrete commissions followed by material invention in at least two first drafts.

This is a causal fidelity result, not a blind product-quality judgment. The objective product gate has separately failed, and the product verdict remains unjudged until the controlled Stage-A v2 panel is recorded.

## Native call record

| Chapter | Thread | Input | Cached input | Output | Reasoning output |
|---|---|---:|---:|---:|---:|
| C-01 | `019f51eb-7545-75c2-97ae-cb9cd7e7a06c` | 39,212 | 8,960 | 25,124 | 23,308 |
| C-02 | `019f51eb-7544-76e1-a35b-51b55cfcf2f7` | 41,698 | 8,960 | 30,902 | 29,675 |
| C-03 | `019f51eb-7554-7203-9fd0-178821a82061` | 43,082 | 8,960 | 23,982 | 21,754 |
| **Total** | — | **123,992** | **26,880** | **80,008** | **74,737** |

Each `.raw.jsonl` has exactly one `thread.started`, one `turn.started`, one final `agent_message`, and one `turn.completed`; the final agent message matches its `.md` decision byte-for-byte after trailing-newline normalization.

## Infrastructure note

The first CLI preflight for each chapter placed the global `-a never` flag after `codex exec`. All three exited 2 before inference with the same parser error; no thread was created. Their stderr is preserved under `infrastructure/grounded-audit-chapter-*-preflight.stderr.log`. The calls were then dispatched once with the corrected global-flag position and the same frozen prompt hashes. The successful calls emitted harmless local state-database fallback and file-watcher warnings to their `.stderr.log`; none used a helper or filesystem material, and all completed normally.
