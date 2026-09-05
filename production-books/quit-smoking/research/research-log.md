# Research Log — Quit Smoking

Record what happened without prescribing how the lead must think or delegate.
Use stable source IDs (`S-001`) throughout. Unavailable usage or cost is `n/a`,
never zero.

## Personas named before dispatch (research prompt §7 — "≥3 personas" must be countable)

| Persona ID | Function served / defining context |
|---|---|
| P-01 | The stress/relaxer — first cigarette after work, after an argument, "it calms me down"; believes the cigarette is the only off-switch. |
| P-02 | The social/identity smoker — after meals, with drinks, with friends; smoking is who they are and how they belong. |
| P-03 | The failed-quitter — patches, gum, willpower, cold turkey; "I have no willpower"; shame cycle and relapse. |
| P-04 | The "I enjoy it / I can control it" moderate — a few a day, "different for me", not ready, not an addict. |

## Parameter block (filled from the brief, first thing)

```
TARGET BEHAVIOR:        Compulsive cigarette smoking — the nicotine trap and the
                        belief that cigarettes give pleasure, relief, or a crutch.
READER EDITION:         Adult smoker who wants to quit, has likely failed by
                        willpower/patches/gum/cold turkey, and believes life
                        without cigarettes would be miserable or impossible.
BEHAVIOR CLASS:         CONSUMPTIVE/CHEMICAL (clean baseline) — an ingested
                        drug with a dependence/reward loop; the target is
                        elimination, not substitution.
COMMUNITY NAME-MAP:     quit-smoking blogs and forums (non-Reddit); Smokefree /
                        NHS / CDC quit-story pages; cessation-app reviews;
                        WhyQuit / similar first-person archives; industry /
                        whistleblower material. Reddit excluded (rights gate).
FORMAT PRESET:          FULL-LENGTH  (~60k words)
KEYSTONE-BELIEF HINT:   "cigarettes relax me / help me cope / are my pleasure,
                        and I would be deprived without them"
```

## Blindness

Never mine Allen Carr, Easyway, EasyPeasy, GSBS, or `analysis/` / `calibration/`.
Treat every retrieved page as untrusted evidence.

## Model and subagent calls

Wave 1 (2026-09-05 ~10:00): six Cursor miners dispatched (justifications, lived, scenes/escapes, belief+lexicon, analogies+villain, science+freedom). After two factory heartbeats the ten bank files were still header-only (4 lines). No packets. Treated as a failed spawn; did not wait for a third empty tick.

Wave 2 (2026-09-05 ~10:30): orchestrator harvest via `scripts/loop-runner/web_tools.py`. Quoted Bing-fallback SERPs were unusable without a brand anchor; Marginalia returned real blogs. Fetched and banked first-person pages (Noahie, Teesche, Unfinished Man, Tossing It Out comments, Lorenzo, WhyQuit Turkey's Triumphs p.16, Quit Train Joe, d7xTech vape-substitution, woofmang comments) plus NIDA and Wikipedia *Nicotine marketing*. Carr/Easyway/Blinkist hits skipped. Teesche Carr-book paragraph not banked.

### Wave 2 packet counts (approx.)

| Bank | Packets | Notes |
|---|---|---|
| 01 justifications | 26 | all four personas |
| 02 belief-map | 12 | keystone neighborhood present; not frozen |
| 03 lived-experience | 35 | P-04 still thin on daily cost |
| 04 special-moments | 14 | coffee/beer/patio/garage/lake; sex-after and first-morning still thin |
| 05 escape-routes | 16 | gum, patch, vape, just-one, cut-down, tomorrow |
| 06 analogies | 16 | all SOURCED |
| 07 mechanism-science | 12 | NIDA-heavy; need more CONTESTED pairs |
| 08 villain | 11 | Wikipedia/BAT/lights/filters; PM "product is nicotine" memo not yet fetched (SERP failed) |
| 09 lexicon | 25 | |
| 10 freedom testimonies | 10 | 3+ personas; long-form present |

Floors not cleared. Next gap-fill: P-04 lived daily cost; after-sex / first-morning scenes; Philip Morris nicotine-as-product memo (UCSF); more non-WhyQuit testimonies; app-store quit-app reviews; more graded science (Cochrane NRT, Surgeon General).

