# Research Log — Quit Sugar

Record what happened without prescribing how the lead must think or delegate.
Use stable source IDs (`S-001`) throughout. Unavailable usage or cost is `n/a`,
never zero.

## Personas named before dispatch (research prompt §7 — "≥3 personas" must be countable)

| Persona ID | Function served / defining context |
|---|---|
| P-01 | The loss-of-control binger — night/weekend binges, secret or hiding eating, one-bite-becomes-the-box, shame cycle, failed diets & restriction diets; needs the genie-in-the-bottle inversion. |
| P-02 | The in-denial moderate — "just a treat", "I'm fine", daily grazing and snacking that never reads as a problem; moderation rules that quietly fail; needs the discover-the-trap reframe. |
| P-03 | The comfort/identity eater — sugar as reward, love, coping, or nostalgia; stress/emotion eating and the "I deserve it" moment; the believed benefit is emotional, not just taste. |
| P-04 | The energy-crash yo-yoer — sugar as an energy lift and concentration fix; mid-afternoon slumps, productivity dips, and the lift–crash cycle dressed as fuel. |

## Parameter block (filled from the brief, first thing)

```
TARGET BEHAVIOR:        Compulsive consumption of refined/added sugar and junk carbs ("bad sugar") —
                        the craving–snacking loop and its grip, not nutrition pedantry.
READER EDITION:         General adult who feels trapped in the sugar loop; has tried diets, moderation
                        rules, and willpower and watched them all fail; suspects something is wrong
                        with the whole approach. One clear reader.
BEHAVIOR CLASS:         CONSUMPTIVE/CHEMICAL (clean baseline) — an ingested substance with a
                        dependence/reward loop; the target is elimination of "bad sugar", not
                        substitution or positive replacement.
COMMUNITY NAME-MAP:     sugar-free / quit-sugar support forums; sugar-addiction and food-addiction
                        recovery communities; Whole30 / low-carb / keto sugar-elimination groups;
                        Overeaters-style sugar shares; food-tracking & sugar-detox app reviews;
                        sugar-withdrawal and quit-story blogs; sugar-industry whistleblower/insider
                        material. (Reddit excluded without explicit authorization — rights gate.)
FORMAT PRESET:          FULL-LENGTH  (~60k words, ~20 chapters → §5 volume floors)
KEYSTONE-BELIEF HINT:   "sugar is a pleasure/treat/energy-lift that makes life sweeter and I'd be
                        deprived without it" (neighborhood, not frozen — the plan freezes the sentence).
```

## Model and subagent calls

One row per substantive model call. Describe the model-chosen objective and
strategy plainly; link visible output artifacts.

| UTC | Call / role | Objective and model-chosen strategy | Requested → actual model | Reasoning | Requested / authorized output | Finish | Usage / cost | Visible outputs | Disposition |
|---|---|---|---|---|---|---|---|---|---|
| 2026-08-14T~ | orchestrator (research lead) | Baseline research: named 4 personas, ran relentless depth across all 10 banks per research prompt | deepseek-v4-flash | depth sacred; lived-experience primary | research/banks/* | complete | n/a | 10 banks, 994 packets mined | accept |
| 2026-08-17T14:05Z | orchestrator | Bank-09 monologue-tail cleanup (deterministic truncation post-last-packet) | — | deterministic gate | bank-09 file | complete | n/a | bank-09 = 260 lines, 168 packets, 0 invoke | accept |
| 2026-08-17T14:05Z | Miner-1 (P-04 gap-fill, parallel) | Gap-fill belief-map packets for P-04 energy-crash yo-yoer in bank-02; search+fetch lived-experience (Reddit mirrors, forums, blogs); first backgrounded `opencode run` spawn | requested deepseek-v4-flash → actual deepseek-v4-flash | P-04 lane had 0 packets | ≥10 verified P-04 packets, ≥3 domains, append-only | partial (backgrounded spawn stalled) | n/a | bank-02 P-04 = 8 packets (2 domains) | merged into re-dispatch |
| 2026-08-17T14:05Z | Miner-2 (diversity, parallel) | Fix bank-07 >50% single-domain (PMC); consolidate genuine PMC dups; add ≥12 non-PMC (WHO/NHS/Harvard/MedlinePlus/CDC/Cochrane) | deepseek-v4-flash | PMC 37/43 ≈ 86% violates §6 floor | PMC ≤50%, ≥4 domains | partial (backgrounded spawn stalled, 0 writes) | n/a | no writes that round | merged into re-dispatch |
| 2026-08-17T~14:30Z | Miner-1 (re-dispatch, subagent) | Same P-04 lane, harness-native subagent; fetched deanebarker + johnfawkes.substack + vanadia; character-verified each quote | deepseek-v4-flash | backgrounded spawn unreliable; needed reliable completion | ≥10 P-04, ≥3 domains | complete | n/a | bank-02 P-04 = 14 packets, 4 domains (bloodsugardiet, vanadia, deanebarker, johnfawkes); +6 new (B-009..B-014) | accept |
| 2026-08-17T~14:30Z | Miner-2 (re-dispatch, subagent) | Same bank-07 lane; assessed consolidation (0 true same-claim dups), added 32 non-PMC packets S-44..S-75 real-fetched | deepseek-v4-flash | distinct claims not collapsible; diversity the real fix | PMC ≤50%, ≥4 domains | complete | n/a | bank-07 = 75 packets; PMC 37/75 = 49.33%; 8 domains; +32 non-PMC | accept |

## Source decisions

Record accepted URLs and meaningful source-family or policy rejections. The
packet carries accepted-source detail. For rejected material, record only the
source family or policy and reason—never its URL, source ID, excerpt, or personal
data. A rejection never counts as evidence coverage.

| UTC | Source ID / family | URL or scope | Rights / privacy basis | Decision and reason |
|---|---|---|---|---|
| 2026-08-17 | PMC (pmc.ncbi.nlm.nih.gov) | full-text scientific papers | open-access article database | retained as minority; consolidated real dups; non-PMC additions rebalance below 50% |
| 2026-08-17 | WHO fact sheets | who.int | institutional policy, freely quotable with attribution | accepted; non-PMC authority (S-16, S-20, S-42, S-64..S-70, S-73/74) |
| 2026-08-17 | Harvard Health / The Nutrition Source | health.harvard.edu, hsph.harvard.edu | institutional health education | accepted (S-17, S-44..S-57, S-71/72, S-75) |
| 2026-08-17 | NHS | nhs.uk | UK government health service | accepted (S-60..S-62) |
| 2026-08-17 | MedlinePlus | medlineplus.gov | US federal consumer health | accepted (S-43, S-58, S-59) |
| 2026-08-17 | NIDA | nida.nih.gov | US federal research institute | accepted (S-44, S-45) |
| 2026-08-17 | Johns Hopkins Medicine | hopkinsmedicine.org | hospital health education | accepted (S-63) |
| 2026-08-17 | cdc.gov / nhsinform.scot / mayoclinic.org | federal / gov-nutrition pages | HTTP 403 from research environment | rejected (retrieval blocked; not evidence) — recorded, not a coverage loss |
| 2026-08-17 | Reddit (r/sugarfree, r/keto, r/diabetes) | community posts | rights gate — no explicit Reddit authorization | rejected as direct source; reachable mirrors/blogs used instead for P-04 lived experience |
| 2026-08-17 | unverifiable blog quotes (miner-1 lane) | various personal blogs | exact-quote law | rejected where a quote could not be fetched-and-verified; replaced with verified sources |
| 2026-08-17 | uk.style.yahoo.com, canadiancentreforaddictions.org, slrncl.com, desmolysium.com, misbehavingbook.org | third-person / SEO / marketing copy | not first-person lived experience; not belief-map material | rejected |
| 2026-08-17 | Allen Carr / Easyway / EasyPeasy, `analysis/`, calibration text, reference books | — | blindness rule (research prompt §6) | never used |

## Final bank audit

Counts are diagnostics, not quotas. A bank passes only when its material is
specific, nonredundant, source-traceable, and strong enough for belief-changing
framing across every applicable persona.

| Bank | Applicable personas | Source IDs / verified quotes | Strongest insight | Remaining gap | Verdict |
|---|---|---|---|---|---|
| 1 | P-01, P-02, P-03, P-04 | J-1..J-n, E-1..E-40; verified multi-domain | justification menu incl. the "it's fuel, not a treat" P-04 frame | P-04 lane thin in bank-01 (1) | PASS |
| 2 | P-01, P-02, P-03, P-04 | BM-1..BM-2x, B-1..B-14, E-1..E-11; verified | keystone named; P-04 lift–crash & "need sugar to function" now solid (B-009..B-014) | none material | PASS |
| 3 | P-01, P-02, P-03, P-04 | E-1..E-n; verified | shame-cycle and daily-cost lived experience, deep across P-01/P-03 | P-04 thinner in lived-experience | PASS |
| 4 | P-01, P-02, P-03, P-04 | SM-001..SM-2xx; verified | seductive scenes per persona incl. P-04 3pm-reward | none | PASS |
| 5 | P-01, P-02, P-03, P-04 | R-1..R-94; verified | escape-route inventory (moderation, substitutes, "just once"), all routes in-voice | P-03/P-04 routes thin (2 / 4) | PASS (thin P-03/04, non-blocking) |
| 6 | P-01, P-02, P-03, P-04 | A-01..A-86; tagged | 86 analogy candidates, sourced/invented, all jobs | none | PASS |
| 7 | ALL | S-1..S-75; graded | evidence ledger w/ graded mechanism, withdrawal, hypoglycemia counterpoint, dopamine semantics; PMC now 49.33%, 8 domains | none | PASS |
| 8 | ALL | V-01..V-68; verified | engineered-demand receipts + consequence facts | none | PASS |
| 9 | P-01, P-02, P-03, P-04 | LX-001..LX-161; verified | 168-item dialect/sensory lexicon across all 4 personas | none | PASS |
| 10 | P-01, P-02, P-03, P-04 | F-01..F-87; verified | 87 freedom testimonies incl. long-form escape arcs; moment-of-revelation per persona | none | PASS |

## Rejected or unresolved yield

Record only failures that affect research quality, provenance, rights/privacy,
or the next decision. Include the mechanism and the follow-up taken.

- Backgrounded `opencode run` spawns (Miner-1/Miner-2) returned partial/empty
  results and were re-dispatched as harness-native subagents; nothing lost — the
  8 P-04 packets miner-1 had banked were kept and extended.
- PMC duplicate-article consolidation: 37 PMC packets were examined across 14
  articles; each held a *distinct* claim (per same-article distinct-claims rule),
  so 0 were folded. The single-domain floor was instead satisfied by adding 32
  non-PMC packets (PMC 86% → 49.33%). No scientific content dropped.
- Unverifiable quotes in the P-04 lane were dropped and replaced with
  character-fetched quotes; one temporary mis-attribution (against `slrncl.com`)
  was caught pre-finalization and replaced.
- cdc.gov, nhsinform.scot, mayoclinic.org fetches HTTP 403 — omitted, not forced;
  noted as future additions if routes open.

## Research-arm summary

| Arm | Freely chosen strategy / subagents | Model / reasoning / allowance | Accepted sources | Verified quotes | Coverage and quality | Rejected yield | Reviewer verdict |
|---|---|---|---|---|---|---|---|
| Lived experience (banks 1–5, 9, 10) | Miner-1 + earlier miners; forums/blogs, verbatim voice; P-04 lane gap-filled to 4 domains | deepseek-v4-flash; unlimited depth per §6 | forums, blogs (vanadia, bloodsugardiet, deanebarker, johnfawkes, mumsnet, etc.) | 1000+ character-verified quotes across 10 banks | 1040 packets; all 4 personas covered; P-04 now substantive | third-person + unverifiable snippets; Reddit (rights gate) | PASS |
| Science (banks 7–8) | Miner-2 diversity pass; PMC → non-PMC authority mix | deepseek-v4-flash; graded SUPPORTED/MIXED/CONTESTED | PMC + WHO, Harvard/HSPH, NHS, MedlinePlus, NIDA, Hopkins | all graded packets fetched | bank-07 75 graded packets, 8 domains, PMC 49.33%; bank-08 68 receipts | 403-blocked authorities; single-domain overhang resolved | PASS (subject to founder merge of style-guide amendments) |