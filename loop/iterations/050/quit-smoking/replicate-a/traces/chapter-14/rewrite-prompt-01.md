# Rewrite prompt 01 — CH-14 ITER 050 smoking (replicate-a)

Contract: prompts/chapter-writer.md only (plan-card contract, fresh role).
Inputs:
1. Plan CH-14: loop/iterations/050/quit-smoking/replicate-a/traces/plan.md
2. Card: loop/iterations/050/quit-smoking/replicate-a/traces/chapter-14/chapter-card.md
3. Style: prompts/style-guide.md (050, no fragments: no fragment chains of 3+, no sensory catalogue paragraph with no belief verb)
4. Previous: loop/iterations/050/quit-smoking/replicate-a/traces/chapter-13/response.md
5. Draft: loop/iterations/050/quit-smoking/replicate-a/traces/chapter-14/draft.md
6. Review: loop/iterations/050/quit-smoking/replicate-a/traces/chapter-14/review-01.md

Task: REWRITE full chapter from draft, fixing exactly the 2 FRAGMENT runs as complete conversational sentences carrying a finite belief verb, preserving all frozen tokens (M-B, F-B, M-H, I-12 + rationale), SA-06 staging, E-06/E-11 limits, and all other draft prose byte-identical:
- Fix 1 (ARE YOU READY): "No party. No crisis. ..." -> 4 complete "There is ..." sentences.
- Fix 2 (NEVER JUST ONE): "Only tonight. Only with drinks. ..." -> 4 complete "It says ..." sentences.
Output: loop/iterations/050/quit-smoking/replicate-a/traces/chapter-14/rewrite-01.md (via .partial+rename).
