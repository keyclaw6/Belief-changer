## Failure evidence
Iter-007 voice 1/20 PASS (19/20 FAIL) — regression from iter-006 5/20 after style-guide craft ban. Trap-question literal count improved 17→3 chapters, but voice lane still FAIL cluster-wide: judges still flag "reads like AI / factory scaffolding, research-report register, persona codes, and meta-commentary persist" and generic AI tell leakage across 19 chapters. Belief holds 20/20 PASS, so voice is now the blocking systemic cluster with near-full spread despite the ban. Book-arc remains FAIL (timing/re-litigation) but does not block belief.

## Root cause
Trace analysis + learnings tail: factory owns correct negative constraint (style-guide §9 craft ban + Gate 4 persona strip) but `meta/muse-spark-1.2-contributor` writer_model does not adhere to bans. Iter-005 silent-execution ban → voice 0/18, iter-006 reviewer gate → 5/20, iter-007 style-guide ban → 1/20 show prompt-surface edits mutate but do not close the class because the model ignores "do not surface" instructions while `prompts/chapter-writer.md` Binding craft still names the device ("trap question", etc.) speakably. Remaining causal lever is not another prompt wording but the execution route that respects negative instructions.

## Targeted fix
One file: `loop/config.yaml`

Replace the Writer model line:
```yaml
# BEFORE
writer_model: meta/muse-spark-1.2-contributor
writer_fallback_model: meta/muse-spark-1.2
```
```yaml
# AFTER
writer_model: meta/muse-spark-1.2
writer_fallback_model: meta/muse-spark-1.2
```
Keep `writer_endpoint: https://ai-gateway.vercel.sh/v1/chat/completions`, `writer_auth_env: AI_GATEWAY_API_KEY`, `writer_route: vercel` unchanged. This makes the primary writer the non-contributor fallback variant (PROGRAM §1 coded fallback) that the harness maps to stricter instruction-adherence; no other file or field changed.

**Why this component:** Three strikes on `chapter-writer.md` Binding craft (001,005) and one on `style-guide.md` (007) prove adding/subtracting ban wording cannot close voice when the contributor model ignores bans; `master-plan-reviewer-v2.md` Gate 4 already strips card literals — the only untried causal surface is the model route itself that executes those bans.

## Predicted impact
What will improve: Voice Cluster 6 will close because the same 007 style-guide §9 ban + Gate 4 that cut trap-question 17→3 will now be adhered to for scaffolding/meta-commentary/research-register; contributor-specific craft leakage should drop from 19/20 FAIL toward ≤8/20 FAIL.
What might regress: Non-contributor may be slightly less fluent on long-form narrative continuity; possible 1–2 chapter dip in image-density if model over-applies bans (mitigated because prose constraints are unchanged, only adherence improves).
How we'll know it worked: Voice judge on next full rewrite no longer quotes factory diction in opening passages and trap-question stays ≤3/20 while overall voice PASS rises from 1/20 to ≥8/20 with belief remaining 20/20; book-arc FAIL may persist unchanged (expected — not targeted this iteration).
