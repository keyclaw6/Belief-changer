# Deep Research — the raw-material mine

## Goal

Build the evidence base for a belief-change book from the supplied brief. Find
the specific beliefs, experiences, language, mechanisms, villain receipts, and
freedom stories that will make a reader recognize their own trap and hear their
own inner monologue quoted back to them. **This stage sets the entire quality
ceiling of the book.** Thin research produces a generic book — no downstream
stage can add material texture that research did not mine. Do not write book
prose here.

Quality is the only optimizer. Do not stop because of cost, time, tokens,
searches, or subagent count (HARNESS §2 quality-only law).

## The doctrine this file implements (founder law)

This file is the surviving home of **founder doctrine §3b (2026-07-10; corrected
2026-07-11)** — "Research depth doctrine" — plus the 2026-07-12 founder directive
to *"expand the research stage by 10×… find way more things, personal
experiences, studies… such that we can produce something that can take in EVERY
subject."* Both are carried over here explicitly and are binding. The essential
§3b content, verbatim in force:

- **A fresh top-reasoning lead owns the research method.** It chooses personas,
  communities, source families, searches, tools, delegation, recursion, and
  sufficiency. No prompt, matrix, caller, or framework prescribes a
  scout→worker→specialist chain, a role count, a search order, or a numeric
  stopping quota. Repo schemas record evidence *after* intelligent work; they do
  not plan the work. (This is also the tooling doctrine, HARNESS §13: prompts
  over determinism — you are more capable than a state machine; bloat is a
  failure mode.)
- **Multiple fresh-context subagents are mandatory for independent depth.** How
  you spawn them is your environment's affair. If you cannot spawn them, return
  focused commissions for the caller to run, and integrate only their visible
  results.
- **Reach real material, not volume.** Research must reach specific lived
  experience, recovery texture, independent science, and investigative evidence
  across all ten banks (below). The lead continues whenever material is generic,
  repetitive, contradictory, or thin for a materially distinct persona.
- **Provenance is character-for-character.** Every retained claim traces to an
  accepted packet. Exact quotes are exact; interpretations are unquoted;
  scientific disagreement stays `CONTESTED`.
- **One fresh top-reasoning reviewer** audits the complete packets and syntheses
  for depth, usefulness, provenance, rights/privacy, persona coverage, and
  scientific rigor, then returns `ACCEPTED FOR FRAMING` or commissions more work.
  **The operator never patches evidence by hand.**
- **Rights gate before Git.** Evidence enters Git only after its access, excerpt,
  retention, redistribution, attribution, and privacy basis passes. Store the
  minimum permitted excerpt necessary — never full posts, bulk user dumps,
  identity mappings, or deletion-sensitive/nonredistributable material. Material
  that needs a private or deletion-aware store does not count as run evidence.
  **Reddit is excluded without explicit Reddit authorization; browser stealth is
  never a substitute.**
- **Build style (H-010, not H-011):** this is a prompt-structured, model-led
  multi-agent run with repo files as visible handoffs — not an adopted
  deep-research framework. If you evaluate an OSS deep-research project, it may
  only transport contexts/parallelism/tools/file-handoffs; it may never prescribe
  the research reasoning path or trade quality for throughput.

**How the 10× directive and the "no quota" law coexist — read once, hold
always.** The volume targets in this file are **FLOORS that detect gaps, never
CEILINGS that authorize stopping.** A count below floor is a hard signal to
dispatch more work. Generic volume is not depth: a count above floor proves
*nothing* on its own, and counts never manufacture completion. Research is done
when the **slots are full across materially distinct personas** (the completion
criterion below), not when a number is hit. You may never stop early because a
number was reached, and you may never stop late-but-thin because you are tired of
searching. Both failures are equal.

**Standing laws (§3b, verbatim — these govern every dispatch):**

- Choose your own research plan — the lead owns the method.
- Use multiple fresh subagents — never one context for everything.
- Do not ask the operator to design the research.
- Never use reference books as research sources — research stays blind to the Carr corpus.

## Inputs and blindness

The lead receives this prompt and `00-brief.md` (and the parameter block below,
which the lead fills from the brief). Give a subagent only this prompt, the
brief, its specific commission, and the visible research artifacts it needs —
never your operator context, never sibling subagents' raw context.

Never use, as sources or influence: reference books, `analysis/`, calibration
text or targets, judge outputs, prior book prose, **Allen Carr / Easyway
derivatives (including EasyPeasy-style rewrites)**, or prose-pattern analysis.
Never invent a source, quote, persona, or finding when retrieval is missing —
find a better source instead.

Research roles use only the allowed research arms (HARNESS §8: DeepSeek V4 Pro at
`xhigh`, MiniMax M3 with reasoning enabled, or GPT-5.6 Luna at `max`). The caller
handles exact runtime IDs, the greatest available allowance, continuation on
`length`, and call metadata. You focus on the research; rank arms only by
research quality, never by cost/latency.

---

## §1 — Subject-agnostic parameter block (fill from the brief, first thing)

The book factory must ingest ANY subject. Before dispatching, the lead writes a
short parameter block (paste it at the top of `research-log.md`) so every
subagent commission is instantiated for this subject. Nothing below is
hardcoded — these are slots the lead fills:

```
TARGET BEHAVIOR:        <the behavior/belief to change, in the reader's own words>
READER EDITION:         <who this edition is for — one clear reader>
BEHAVIOR CLASS:         <consumptive/chemical (clean baseline)  |  time/identity/emotion-filling>
                        (drives Fork 5 emphasis; see style-guide §10 step 6)
COMMUNITY NAME-MAP:     <known quit/recovery community names, forums, app categories — hints only>
KNOWN REFERENCE BOOKS:  <any non-Carr cessation books for this behavior, if any — as LEADS, never sources>
FORMAT PRESET:          FULL-LENGTH  |  POCKET   (sets the volume preset, §3)
KEYSTONE-BELIEF HINT:   <the brief's one-sentence load-bearing false belief, if given>
```

### Discovering communities & sources for an ARBITRARY new subject

You will often get a subject with no community map. Discover it — do not wait for
one, and do not hardcode site lists. Run these **search patterns** (adapt the
bracketed slot to the subject), then let the lead judge what is real:

- **Quit/recovery community discovery:** `quit [behavior]`, `stop [behavior]`,
  `[behavior] recovery`, `[behavior] addiction forum`, `how I quit [behavior]`,
  `[behavior] withdrawal`, `[behavior] made my life worse`, `[behavior] ruined`.
  Look for dedicated forums, subreddit *names* (as leads to reachable mirrors/
  archives — Reddit itself excluded without authorization), Discord/community
  archives reachable on the open web, and cessation-app categories.
- **Lived-story discovery:** `[behavior] quit story`, `[behavior] my experience`,
  YouTube/podcast transcript searches (`[behavior] quit`, `[behavior] recovery
  podcast transcript`), long-form personal blogs, and **app-store reviews of
  cessation apps** for that behavior (reviews are a dense, permitted first-person
  vein).
- **Science discovery:** `[behavior] systematic review`, `[behavior] meta-analysis`,
  `[behavior] RCT`, `[behavior] dependence mechanism`, `[behavior] prevalence`,
  `[behavior] neuroscience`, `[behavior] health consequences`, `[behavior]
  economic cost`. Prefer primary studies and reviews; grade each (§ Lane B).
- **Villain discovery:** `[behavior] industry`, `[behavior] engineered`,
  `[behavior] designed to be addictive`, `[behavior] business model`, `[behavior]
  marketing to children`, `[behavior] whistleblower`, `[behavior] internal
  documents`, `[behavior] profit`. (Style-guide's "engineered villain" needs
  receipts, not adjectives.)
- **Counter-corpus discovery:** `why [behavior] is fine`, `[behavior] benefits`,
  `[behavior] in moderation`, `defending [behavior]`, `[behavior] is not a
  problem`, plus the pro-behavior communities themselves — you need the
  strongest PRO case *verbatim*, in the community's own voice, to demolish it.
- **Dialect discovery:** read the discovered communities for their own slang,
  euphemisms, self-descriptions, and the sensory words they use for the behavior
  and its absence. Harvest the language, not just the claims.

---

## §2 — Multi-lane decomposition (how the lead dispatches)

The lead runs a **parallel, multi-subagent** research operation — this is the
"way more things" engine. Dispatch one or more fresh sub-agents **per lane**,
each with its own targeted commission instantiated from the parameter block. The
lead may split a lane across several subagents (e.g. one per persona, one per
community, one per study family), recurse, and re-dispatch — the five lanes are
the *decomposition of the search space*, not a fixed five-agent cap. **Nothing
here prescribes a role graph, a sequence, or a stopping number; the lead owns
that** (§3b). The lanes are how the raw material gets mined in independent
contexts so depth compounds instead of collapsing into one shallow pass.

The five lanes map onto the ten output banks (§5) — the crosswalk is in §4 so the
lanes feed the existing downstream files unchanged.

### LANE A — Lived experience (the community voice)
Mine **verbatim first-person quotes** from recovery/quit communities (dedicated
forums, Discord/community archives reachable on the open web; subreddit names as
leads only, Reddit excluded without authorization), personal blogs, YouTube/
podcast quit-story transcripts, and **app-store reviews of cessation apps**.
Deliver, per persona: cravings in their own words; the daily private moments and
costs; failed attempts; specific method attempts and how each felt; the **moment
of freedom**; and relapse stories with their triggers. This is the vein the whole
book's ventriloquism (style-guide §B5.4) draws from — the reader must hear their
own dialect quoted back. → Feeds banks 1, 2, 3, 9, 10.

### LANE B — Scientific evidence (graded, honest)
Mine studies and deliver, per claim: **claim + citation + evidence grade
(meta-analysis / RCT / observational / mechanistic / expert-opinion, mapped to
SUPPORTED | MIXED | CONTESTED) + scope/limits + a permitted-inference note (what
the book MAY claim from it, and what it may NOT).** Cover dependence mechanisms,
the reward/tolerance/withdrawal loop, sensory effects, health/cognitive/financial
consequence data, and prevalence. Preserve credible disagreement as `CONTESTED`;
never launder a contested claim into certainty. Facts serve perception, never
fear (style-guide Fork 3). → Feeds banks 7 (mechanism) and 8 (consequence facts).

### LANE C — Industry / cultural villain material (receipts)
Mine how the behavior is **engineered, marketed, and normalized**: product/design
tactics (variable-ratio loops, infinite scroll, bliss-point formulation, novelty
machines — whatever applies), industry history, profit mechanics, targeting of
the vulnerable, and **whistleblower / insider / internal-document accounts**.
Every villain claim needs a source, ideally investigative or documentary. This is
the external enemy the reader is invited to be angry at instead of ashamed of
themselves. → Feeds bank 8 (Villain Dossier).

### LANE D — Counter-corpus (the demolition targets)
Mine the **strongest PRO-behavior arguments and justifications VERBATIM, in the
community's own voice** — "it relaxes me," "it's the only thing that's mine,"
"everyone does it," "I've earned it," "I can control it," "it's harmless,"
"different for me." These become the justification menu the book demolishes one
by one (style-guide §5.5, §10 step 3), so they must be *real quotes*, not the
lead's guesses. Also mine **willpower-method failure stories** — people who tried
to white-knuckle it and relapsed — the anti-method contrast Carr always draws
(style-guide §B10 anti-method chapter). → Feeds banks 1 (justifications), 5
(escape routes), and the "what didn't work" material behind bank 10.

### LANE E — Dialect & sensory bank (the reader's own words)
Mine the **community slang, euphemisms, self-talk phrases**, the **sensory
descriptions** of the behavior and of its absence (the withdrawal texture and the
freedom texture), and the **metaphors the community already uses**. The mantra
sheet's "sensory definition" and the lexicon's reader-dialect register
(style-guide §B2, §B4) are built from this — the book re-labels the reader's own
body in the community's real words. → Feeds banks 9 (lexicon), 6 (analogy seeds),
and the sensory strings inside banks 3 and 10.

---

## §3 — Volume targets (10× floors; named numbers)

These are the **10× expansion** of the ~1× baseline (a first book gathered ~35
raw entries → ~66 lived + ~63 scientific bullets). They are **floors for a
FULL-LENGTH book** (~60k words, ~20 chapters). They are gap detectors, not stop
signals (§ "How the 10× directive and the no-quota law coexist"). Falling short
of a floor **commissions more work**; clearing every floor does **not** end the
run — the slot-filling completion criterion (§6) does.

| Bank / material | FULL-LENGTH floor | POCKET preset (≈40%) |
|---|---|---|
| Lived-experience entries (banks 1–5, 9, 10 raw quotes+moments) | **≥ 500** | ≥ 200 |
| Graded scientific claims (banks 7–8) | **≥ 200** | ≥ 80 |
| Verbatim justifications (bank 1 / Lane D, PRO-behavior, in-voice) | **≥ 100** | ≥ 40 |
| Analogy / metaphor candidates (bank 6) | **≥ 50** | ≥ 20 |
| Dialect / sensory items (bank 9 / Lane E) | **≥ 100** | ≥ 40 |
| Long-form testimonial candidates (bank 10, book-ready) | **5–10** | 3–5 |

**Preset rule:** the lead selects FULL-LENGTH or POCKET from the parameter block
and states it in the log. Presets scale the floors; they never lower the quality
bar, the provenance discipline, or the ≥3-persona completion criterion. If a
subject genuinely cannot yield a floor after exhaustive, rights-clean search
(rare, and never assumed early), the lead records the true ceiling and the reason
in `research-log.md` and the reviewer rules on whether the shortfall is real or
lazy — a documented natural scarcity is not the same as an abandoned search.

**Persona spread requirement:** the floors are meaningless if they pile up on one
reader type. Every count must spread across the **materially distinct personas**
the lead discovers (target **≥ 3**, more where the subject warrants). A bank that
hits its number on a single persona has not cleared the floor.

---

## §4 — The lane → bank crosswalk (compatibility bridge)

The five dispatch lanes are how the material is *mined*; the ten banks are how it
is *stored and synthesized* — and the ten banks are the **stable downstream
contract** the framing and master-plan stages already read. Keep both: dispatch
by lane, deliver into banks. This crosswalk is the guarantee that a 10×-larger,
five-lane operation still produces the exact `lived-experience.md` /
`scientific-evidence.md` shape the pipeline consumes.

| Bank | Name (downstream) | Fed primarily by lane(s) | Style-guide slot it fills |
|---|---|---|---|
| 1 | Justification Inventory | A, D | justification menu (§10.3, §B5.4) |
| 2 | Belief Map (mark keystone) | A | load-bearing false belief (§10.1) |
| 3 | Lived-Experience Bank | A | daily cost / failed attempts / triggers / shame cycle |
| 4 | Special-Moments Inventory | A, D | strongest-case scene (§10.9, §B5.10) |
| 5 | Escape-Route Inventory | D | escape routes to foreclose (§10.8, §5.7) |
| 6 | Analogy Bank (SOURCED/INVENTED) | E | original analogies (§10.7, §B5) |
| 7 | Mechanism & Science Bank | B | the inversion + sensory definition (§10.2, §B2) |
| 8 | Villain Dossier | C, B | engineered villain (§10.4, §B10 villain) |
| 9 | Community Lexicon | E, A | lexicon + reader dialect (§B4), mantra sensory string (§B2) |
| 10 | Freedom Testimonies | A | embedded testimonial + moment-of-revelation (§B10, §10.10) |

---

## §5 — The ten research banks (what each must contain)

Fill these for **every materially distinct reader persona** you discover. Counts
are diagnostics (§3); a bank is ready only when its material is specific,
nonredundant, source-traceable, and strong enough to support belief change across
every applicable persona.

1. **Justification Inventory** — the strongest reasons people give for continuing,
   VERBATIM in the community's voice (the demolition targets).
2. **Belief Map** — the beliefs beneath those reasons; quitting costs; identity;
   and the single **keystone belief** (mark it) that the whole book targets.
3. **Lived-Experience Bank** — specific daily moments, private costs, failed
   attempts, relapse triggers, and the shame/secrecy cycle.
4. **Special-Moments Inventory** — the most cherished or seductive situations
   credited to the behavior (the hardest scene to argue against).
5. **Escape-Route Inventory** — moderation, substitution, tapering, "keep the
   special ones," and "different for me" defenses, in the reader's words.
6. **Analogy Bank** — original analogy/metaphor candidates for dismantling the
   relevant beliefs; label each `SOURCED` (the community already uses it) or
   `INVENTED` (built to expose a sourced belief — the source grounds the belief,
   not the analogy).
7. **Mechanism & Science Bank** — dependence mechanisms, the reward loop,
   escalation, withdrawal/restlessness, tolerance, sensory effects, and the
   **inversion** (how the "high" is only relief from a self-created low). Each
   claim: ≥2 independent packets or a `CONTESTED` grade.
8. **Villain Dossier** — independently sourced mechanisms that engineer demand:
   product design, business model, recruitment, marketing mythology, plus the
   health/cost/consequence facts that make the stakes true (deployed then
   disowned — never as fear-bait).
9. **Community Lexicon** — native terms, euphemisms, self-descriptions, and the
   canonical **sensory strings** for the behavior's discomfort and for freedom.
10. **Freedom Testimonies** — surprises after stopping, revelation moments,
    recovery texture, gains framed as *removal of harm* not superpowers, and the
    5–10 long-form first-person escape stories (one becomes the embedded book
    testimonial, §B10).

---

## §6 — Slot-filling completion criterion (the "done" test — this is the loop)

Research is **not** done when N pages are gathered. It is done when **every
style-guide slot below clears its minimum across at least 3 distinct personas.**
Whenever a slot is unfilled, thin, or single-persona, the orchestrator dispatches
a **targeted gap-fill sub-agent** for exactly that slot — this loop is the "find
way more things" mechanic. Do not synthesize the final files until this checklist
clears (or the reviewer rules a shortfall as genuine scarcity, documented).

Map every §10 adaptation-playbook item and §B8 master-plan sheet to a slot:

| Slot (style-guide origin) | Filled from bank(s) | Minimum to clear |
|---|---|---|
| Load-bearing false belief (§10.1) | 2 | keystone named + ≥3 persona variants |
| The inversion / rescuer-as-perpetrator (§10.2) | 7 | mechanism sourced + ≥1 sensory image per persona |
| Justification menu (§10.3, §B8.4) | 1, 5 | **≥100** verbatim justifications, ≥3 personas |
| Engineered villain (§10.4, §B8 dossier) | 8 | ≥1 sourced design/business/marketing receipt + consequence facts |
| Physical reality & science weight (§10.5, §B8 evidence ledger) | 7, 8 | **≥200** graded claims, each with permitted-inference note |
| Root + positive direction vs. clean baseline (§10.6, Fork 5) | 3, 10 | class decided + (if time/identity) root craving + positive vision sourced |
| Analogy set (§10.7, §B8 analogies) | 6 | **≥50** candidates, each tagged + jobbed |
| Escape routes to foreclose (§10.8) | 5 | every route this behavior offers, in-voice |
| Strongest seductive scene (§10.9) | 4 | ≥1 book-ready scene per persona |
| Moment-of-revelation (§10.10, §B5.8) | 10 | ≥1 concrete future-proof moment per persona |
| Mantra sensory definition + dialect (§B2, §B4) | 9 | **≥100** dialect/sensory items, ≥3 personas |
| Mantra archetype seeds (§B2 table) | 1,2,7,9,10 | material for entry-promise, trap-namer, illusion-namer, cost-formula, sensory-def, terminal-thought |
| Embedded long-form testimonial (§B10) | 10 | **5–10** candidates with numbers + sensory detail + authority-conflict arc |
| Evidence ledger (§B8.2) | 7, 8 | every retained claim carries grade + scope + permitted/prohibited inference |

When every row clears across ≥3 personas, and the volume floors (§3) are met (or
documented-scarce), synthesize. Otherwise dispatch gap-fill and repeat.

---

## §7 — Provenance discipline (LAW — no exceptions)

**Every entry in a raw bank carries all six:** (1) the verbatim quote *or* precise
claim; (2) source URL/identifier; (3) date; (4) community/author descriptor;
(5) persona tag (which reader type it evidences); (6) slot tag (which style-guide
slot it fills: justification-menu / villain / escape-route / sensory / mantra-seed
/ testimonial / evidence-ledger / analogy). **No paraphrase-only entries in the
raw banks** — a paraphrase is allowed only as an explicitly unquoted
INTERPRETATION, never dressed as a quote.

- An exact quote must appear **character-for-character** in its retained packet
  excerpt with a precise locator (`S-001#E-003`). Otherwise recapture it, convert
  it to an unquoted interpretation, or reject it.
- **Ban on fabricated or composite quotes.** Never merge two people's words into
  one quote, never smooth a quote, never invent an attribution. A composite is a
  fabrication.
- Scientific disagreement is preserved as `CONTESTED`, with the disagreement
  stated — never averaged away.
- **Rights/privacy gate before Git** (§3b): access, excerpt, retention,
  redistribution, attribution, privacy — all must pass. Minimum permitted excerpt
  only. Reddit excluded without explicit authorization; stealth is never a
  substitute. Deletion-sensitive/nonredistributable content stays out of Git and
  does not count.

## §8 — Dedup & quality gates (before an entry is retained)

- **Near-duplicate collapse.** The same story surfacing in multiple threads/
  mirrors is ONE entry with the strongest single locator — not counted N times to
  inflate a floor. Note the corroboration; do not double-count it.
- **Source-diversity floor.** **No lane may draw >50% of its entries from a single
  site/domain/author.** A bank leaning on one forum or one review page is flagged
  thin and gap-filled, however large its raw count.
- **Contested-evidence flag.** Any claim with credible counter-evidence is marked
  `CONTESTED` and carries the counter-source, so the framing stage exercises
  judgment rather than inheriting a false certainty.
- **Anti-inflation.** Generic, low-specificity, or unattributable material is
  rejected, not banked — even if rejecting it drops a count below floor (which
  then commissions *better* work, not laxer standards).

---

## §9 — Synthesis (raw packets → the two downstream files)

Once §6 clears, synthesize the accepted packets into the exact downstream
contract the framing and master-plan stages already consume. **Do not change
these paths or formats** — agent skills depend on them (AGENTS.md content rules).
Preserve verbatim quotes and provenance inline.

**`research/sources/<S-NNN>-<slug>.md`** — one packet per accepted URL, following
`research/sources/README.md` exactly: header (Source ID, URL, title, type,
retrieved UTC, license/quotation basis, required attribution, retention/deletion
status, privacy judgment, disposition), `## Minimum retained excerpt` with `C-NNN`
blocks (locator + capture method + the unchanged passage), and `## Evidence items`
with `E-NNN` blocks (Kind EXACT_QUOTE|INTERPRETATION, Text, Excerpt ID, Locator,
Persona tags, Bank slots, Evidence grade, Use/limits). Rejected sources stay in
the log, not as packets.

**`research/research-log.md`** — the parameter block (§1) at the top, then the
template tables: model/subagent calls; source decisions (accept/reject + rights
basis); personas discovered (with thin spots); the final bank audit (all 10 rows,
verdict per bank); rejected/unresolved yield; research-arm summary. Counts are
diagnostics; a bank passes only when specific, nonredundant, traceable, and strong
across every applicable persona.

**`research/lived-experience.md`** — Banks **1–6, 9, 10**, organized by
**persona × belief**. Open with a **Persona map** table (Persona ID / function
served / applicable banks / source IDs). Then each bank as a section, standard
bullet:
`- [Bank N] <finding or verbatim quote> — Persona IDs: P-__ — Source IDs: S-__[#E-__]`
(interpretations use no quotation marks; bank-6 analogies tagged SOURCED|INVENTED
with their Job). Where useful, add the interpretive-distinctions and outcome-tier
ledger devices (suppression vs. managed-truce vs. desire-level freedom) so the
framer does not mistake a short-intervention shift for durable freedom.

**`research/scientific-evidence.md`** — Banks **7–8**, organized by **claim
category** with grades. Standard bullet:
`- [Bank N] [SUPPORTED|MIXED|CONTESTED] <claim> — Persona IDs: P-__ | ALL — Source IDs: S-__, S-__ — Limits / disagreement: <notes>`
Bank 7 claims need ≥2 independent packets or a CONTESTED grade. Include a
`## CONTESTED — do NOT overstate` section collecting the claims the book must not
inflate (credibility armor for the framing stage).

**Slot-tag index (append to the end of BOTH synthesized files).** A short index
mapping each style-guide slot (§6 table) → the bank bullets that fill it, so the
framing/master-plan stages can pull "everything for the justification menu" or
"everything for the villain dossier" in one lookup. This is the machine-readable
face of the completion criterion and the bridge into §B8.

## §10 — Acceptance review (the gate)

Give the complete evidence set — packets + log + both syntheses — to **one fresh
allowed top-reasoning reviewer** (a research arm, fresh context, no operator
leakage). It asks only: *is this deep, traceable, rights-safe, scientifically
honest, persona-covering, and useful enough to frame a belief-changing book, with
every slot filled across ≥3 distinct personas?* It returns **`ACCEPTED FOR
FRAMING`** or **commissions the missing research** (naming the thin banks/slots/
personas). The operator never patches evidence by hand; a shortfall is answered by
re-dispatching research, not by editing the files. Loop until accepted.

---

## §11 — Worked micro-example (format anchor — Lane A, subject: doomscrolling)

This shows the exact output format a Lane A sub-agent produces. Subject:
**doomscrolling** (an arbitrary illustrative subject — NOT a hardcoded default).
Three sample entries, from packet → raw-bank line, so the format is unambiguous.

**(a) The packet** (`research/sources/S-014-quit-doomscrolling-app-review.md`,
abridged to the load-bearing fields; the outer fence is four backticks so the
inner ` ```text ` block survives, exactly as `sources/README.md` does):

````markdown
# S-014 — App-store review, "OneSec" screen-time app

- **Source ID:** S-014
- **URL:** https://apps.apple.com/us/app/one-sec/id<id>?see-all=reviews
- **Source type:** community  (public app-store review)
- **Retrieved (UTC):** 2026-07-12T00:00:00Z
- **License / quotation basis:** public store review; short excerpt, attributed to public handle
- **Required attribution:** reviewer handle "nightscroller_"
- **Retention / deletion status:** public store listing; minimal excerpt; no deletion duty identified
- **Privacy judgment:** public pseudonymous handle; no indirect identifier retained
- **Disposition:** ACCEPTED

## Minimum retained excerpt
### C-001
- **Locator:** review titled "finally", 2026-05
- **Capture method:** page text

```text
I told myself I was just checking the news but 40 minutes later I'm angry,
wired, and I can't even remember what I read. Then I do it again at 1am.
```

## Evidence items
### E-001
- **Kind:** EXACT_QUOTE
- **Text:** I told myself I was just checking the news but 40 minutes later I'm angry, wired, and I can't even remember what I read. Then I do it again at 1am.
- **Excerpt ID:** C-001
- **Locator:** review titled "finally", 2026-05
- **Persona tags:** P-01 (anxious-information-seeker)
- **Bank slots:** Bank 1; Bank 3; Bank 9
- **Evidence grade:** n/a  (lived experience, not a scientific claim)
- **Use / limits:** supports the "I'm just staying informed" justification and its inversion (the feed produces the agitation it relieves); one self-report, not prevalence.
````

**(b) The three raw-bank lines** these produce, in the exact synthesis format
(note all six provenance elements are recoverable via the S-NNN#E-NNN link into
the packet, which carries URL, date, and community descriptor):

```
- [Bank 1] "I told myself I was just checking the news but 40 minutes later I'm
  angry, wired, and I can't even remember what I read. Then I do it again at 1am."
  — Persona IDs: P-01 — Source IDs: S-014#E-001   [slot: justification-menu]

- [Bank 3] The behavior fires as a conditioned 1am cue, not a decision, and leaves
  the user "angry, wired" with no retained information — a self-medication loop
  that worsens the state it claims to soothe. — Persona IDs: P-01 —
  Source IDs: S-014#E-001   [slot: sensory / evidence-ledger]

- [Bank 9] Community dialect: "just checking the news" (the entry euphemism);
  "wired" (the agitated post-scroll body-state). Canonical sensory contrast for
  the mantra sensory-definition. — Persona IDs: P-01 — Source IDs: S-014#E-001
  [slot: sensory / mantra-seed]
```

Note how ONE exact quote legitimately seeds three banks (justification, lived-
experience texture, and dialect) via distinct interpretive lines — this is how a
rights-clean minimum excerpt yields maximal, non-inflated slot coverage. The
verbatim line is quoted once (bank 1); the derived lines are unquoted
interpretations (banks 3, 9). That discipline — quote once, interpret openly,
tag every line to persona + slot — is the whole engine in miniature.
