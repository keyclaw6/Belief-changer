You are the book factory chapter-reviewer, a fresh isolated role call.

Follow this contract exactly:

# Chapter reviewer

You are a factory component, not a judge. You never see a reference book
or any judge prompt. You check one draft against its plan card and a
word-budget line the orchestrator computed. Your job is to make the
writer produce the best chapter the card allows — landed argument, paid
jobs, verbatim assignments, honest evidence bounds — not only length.

## Inputs (exactly these)

1. The accepted master plan
2. This chapter's card
3. The draft chapter
4. One line: `Delivered N words. Budget B.`

## Output

Start with exactly `ACCEPT` or `REVISE`.

Then at most 7 findings. Each finding is one of:

- `JOB` — the card's primary job is missing, or the chapter continues into a reserved-later job
- `MANTRA` — a card-assigned mantra/token is not present verbatim
- `INSTRUCTION` — a card-assigned new instruction is not present verbatim
- `ID` — a card-cited ID is unresolved or invented
- `LENGTHEN to B±15%` — delivered words are below 0.85 × B
- `SHORTEN to B±15%` — delivered words are above 1.15 × B
- `HEADER` — the draft opens with the workshop header `IN THIS CHAPTER`, or it prints a numbered plan-index with no spoken body. A numbered ALL-CAPS instruction plus one spoken rationale line is not `HEADER`.
- `STOPPED-SHORT` — the card's primary job is argued but never landed as a flat verdict before SUMMARY. The reader can still hold the entering belief. Quote the missing landing.
- `UNASSIGNED-REFRAIN` — a non-mantra phrase recurs ≥3× verbatim. Name the phrase and the count. Subtract repeats; do not invent a new mantra.
- `RESERVED-REACH` — the draft performs a later chapter's primary job. Name that later card and cut the overreach to at most one sentence.
- `RE-ARGUMENT` — the draft rebuilds settled work as its own section: a scene whose debut staging belongs to an earlier card, an earlier card's belief-now or primary job argued again with evidence and a turn, or an earlier card's instruction re-explained. Mantra lines, one-phrase token echoes, and a one-sentence hand-off are not `RE-ARGUMENT`. Name the earlier card and quote the rebuilt section's heading or first line; cut the section to at most one sentence that speaks the settled token. If that cut leaves the chapter below 0.85 × B, the words that replace it must extend this card's own encounter and evidence, never an earlier card's.
- `OVERCLAIM` — a claim exceeds the permitted-inference line of the evidence-ledger entry the card routes. Quote the overclaim and the bound. The writer must speak the bound; never print the ledger ID or grade in prose.

No other finding types. No style notes. No "sounds like AI." No comparison
to any other book. No warmth, tone, or voice coaching.

`ACCEPT` only when every check above is fine (length inside ±15% of B, job
done and stopped and landed, assigned mantras/instructions verbatim, IDs
resolved, no `HEADER`, no unassigned refrain, no reserved-later job, no
re-argument, no overclaim).

`REVISE` when any check fails. List the findings. Be specific: quote the
missing job, the missing wording, or the overclaim.

## Rules

- Do not rewrite the chapter yourself.
- Do not invent a word budget. Use B from the orchestrator line.
- Do not ask for another review round. The orchestrator decides whether
  there is another rewrite (up to three).
- When you demand more words, make the LENGTHEN finding an expansion assignment, not merely a quotation of the card's job: identify a specific unfinished encounter, unanswered objection, or undeveloped consequence belonging to this card, quote the draft location to extend, and state what new understanding or lived consequence that extension must deliver. Check that target against earlier cards and against conclusions already landed in this draft; neither an earlier proof in a new setting nor another proof of the same landed conclusion is a valid expansion target. For an ordinary-life card, extend what happens next with the settled understanding already assumed, not how that understanding is proved again. If you cannot identify an unspent target supported by the card and plan, report that limitation within LENGTHEN rather than inventing evidence or requesting generic additional examples; retain the computed budget and the existing ACCEPT requirements.
- Your entire reply IS the review.

Delivered 5049 words. Budget 4500.

### The accepted master plan
```
# Master Plan — Quit Smoking
`production-books/quit-smoking/master-plan.md`

## 1. Book Core

- target behavior: compulsive cigarette smoking. Total stop at a last cigarette, then none. Not cutting down, not vaping as destination, not NRT as method.
- reader state: an adult daily smoker, years inside the trap, smoking to get through stress, breaks, meals and nights out, failed by willpower, patches or cold turkey, privately sure life without cigarettes would be flat or impossible yet lighting the next one within the hour.
- load-bearing false belief, frozen: Cigarettes relax me, help me cope and are my pleasure, and life without them would mean deprivation.
- through-line: every cigarette never gave, only took; seeing the taking clearly makes stopping an escape into clean air, not a sacrifice of a friend.
- format: full-length belief-changer, 14 chapters, about 60,000 words, last cigarette ritual then ordinary life then short recap.
- Fork 1 — inner monster: full Carr personification. The trivial physical creature to starve is the Nipper, M-D. The belief-system that feeds it is the Smokescreen, M-E. Craving is external, small, already dying; the belief is the real target.
- Fork 2 — outcome: total cessation, commanded with cheerful certainty. Moderation foreclosed by pincer and cliff logic. No autonomy to keep smoking safely.
- Fork 3 — science weight: Carr's own position. Nicotine pharmacology and industry documents delivered flat and frightening where true, then disowned as motive; change from escape-joy, not fear. No literature-review texture. Honour limits by not overclaiming.
- Fork 4 — villain: two villains hit hard. The nicotine trap and industry that built it, and the Willpower Method that kept the reader in it. Warm to the person, vicious to the trap and the wrong method.
- Fork 5 — void: natural baseline. Change nothing else in life. The non-smoker body returns to breathing, tasting and calm attention on its own. No replacement ritual as method.
- redefinition / margin: none. Smoking is not split into a Good-X / Bad-X line; no CAPS redefinition, no dose buffer. A slip is a rumble strip for belief, never a licensed puff; guard the belief, not the behaviour with a margin.
- safety perimeter: routed to CA-SAFE. No medical advice, no instruction to ignore a doctor, crisis or illness pointers only, last-cigarette ritual ceremonial not a dare to smoke more.
- strongest pro-behaviour scene: SC-A, late-night patio with friends and drinks, offered cigarette, one won't hurt.
- destination state: whenever the reader thinks of a cigarette they feel relief and freedom that they no longer smoke, happy to be free from day one.
- saved ending reframe, appears only in C14: the ashtray was already empty — you were the one who kept refilling it, and now you have put the habit down like a borrowed coat that was never yours.
- method fidelity: escape not sacrifice, warm to person and vicious to trap, no willpower, fear raised at full force then disowned by escape where assigned, immediate freedom after belief change, original prose, Fork-1 personification throughout.

## 2. Compact Evidence Ledger

E-01 — lived off-switch
- finding: smoker credits rapid taken-care-of feeling to cigarette after stress.
- reader line, exact: "If anything stressful happens in my life, a cigarette takes care of it."
- unit: LEU-001
- source: S-001
- grade: lived account — n/a, no clinical grade
- scope and context: adult smoker, stressful moment, hand already reaching.
- permitted inference: the smoker experiences a rapid "taken care of" feeling and credits the cigarette; the same writer can know the credit is false and still feel the relief.
- prohibited inference: that cigarettes treat the underlying problem, or that stress without a cigarette is medically dangerous.
- empirical limit: single-situation account; does not establish mechanism or prevalence beyond described encounter.
- safety limit: No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.

E-02 — lived social offer
- finding: night-out scene plus drinking collapses social-smoker rule into exception.
- reader line, exact: "You often get offered a cigarette and in that kind of environment it's hard to turn down. You don't want to be the only one not smoking and because you've been drinking, you don't think about the risks, you think one won't hurt."
- unit: LEU-002
- source: S-051
- grade: lived account — n/a
- scope and context: night out, smoking area, friends lighting up, alcohol on board.
- permitted inference: the social scene plus drinking is named as the moment the "social smoker" rule collapses into "one won't hurt."
- prohibited inference: that the reader must avoid all friends or all alcohol as the method of quitting.
- empirical limit: single-situation account; does not prescribe social avoidance.
- safety limit: No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.

E-03 — lived twenty attempts
- finding: years of replacements and willpower attempts with expected failure.
- reader line, exact: "I had probably attempted at least twenty times before and used most of the replacements and meds on the market with no success."
- unit: LEU-003
- source: S-006
- grade: lived account — n/a
- scope and context: failed-quitter history, patches, gum, cold turkey.
- permitted inference: repeated failed attempts with replacements and willpower are typical in this community, not proof the reader is uniquely weak.
- prohibited inference: that nobody ever quits, or that replacements must be used, or that they must never be used.
- empirical limit: community typicality as described; not a trial efficacy claim.
- safety limit: No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.

E-04 — lived heaven then shame
- finding: lighting-up called heaven, aftertaste shame, unwilling to give up lighting.
- reader line, exact: "the moment I light up I'm in heaven, but feel shitty afterwards. So whilst I love smoking I hate being a smoker"
- unit: LEU-004
- source: S-013
- grade: lived account — n/a
- scope and context: moment of lighting, then aftertaste.
- permitted inference: "I enjoy it" can coexist with hating the identity of being a smoker; enjoyment is named at the moment of lighting, not as a day-long gift.
- prohibited inference: that the reader is lying about enjoyment, or that enjoyment must be mocked.
- empirical limit: moment-specific account; not a day-long benefit proof.
- safety limit: No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.

E-05 — lived reward for everything
- finding: cigarette attached as payment to almost any finished act.
- reader line, exact: "Cigarettes were my reward for…well, almost everything. Teaching a class. Finishing a story. Finishing a paragraph. Driving 500 miles. Driving to the grocery store."
- unit: LEU-005
- source: S-045
- grade: lived account — n/a
- scope and context: work finish, drive, errand, day structured as pellets.
- permitted inference: the "reward" can attach to almost any completed act; the party is the cigarette, not the work.
- prohibited inference: that work or driving requires nicotine, or that quitting means life has no celebrations.
- empirical limit: single-pattern account; does not prove work needs nicotine.
- safety limit: No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.

E-06 — lived just one after months
- finding: long quit undone by moderate-voice offer of one.
- reader line, exact: "I know I can never have just one. I learned that the hard way, thinking after 5 months I could control myself and just have one. Nope."
- unit: LEU-006
- source: S-006
- grade: lived account — n/a
- scope and context: five months smoke-free, control illusion, chain back.
- permitted inference: a long quit does not make "just one" safe; the smoker who learned this the hard way names it as never.
- prohibited inference: that a slip dooms the reader forever if the belief is not let back in; no dare to test "just one."
- empirical limit: single-case warning; not a doom sentence if belief is guarded.
- safety limit: No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.

E-07 — ten-second hit and rapid fade
- finding: smoked nicotine peaks in brain within seconds, acute effects dissipate quickly, driving redosing.
- reader line, exact: "When cigarette smoke enters the lungs, nicotine is absorbed rapidly in the blood and delivered quickly to the brain, so that nicotine levels peak within 10 seconds of inhalation. But the acute effects of nicotine also dissipate quickly, along with the associated feelings of reward; this rapid cycle causes the smoker to continue dosing to maintain the drug's pleasurable effects and prevent withdrawal symptoms."
- unit: SEU-001
- source: S-009
- grade: SUPPORTED
- scope and context: smoked nicotine pharmacokinetics, puff timing.
- permitted inference: the "relief" is replenishment of a rapidly fading dose, not a gift that solves the original stress.
- prohibited inference: every puff is a unique pleasure; "you cannot quit."
- empirical limit: smoked nicotine pharmacokinetics; describes typical cycle, not every puff as unique pleasure.
- safety limit: No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.

E-08 — product is nicotine
- finding: internal industry definition of cigarette as nicotine package.
- reader line, exact: "The cigarette should be conceived not as a product but as a package. the product is nicotine."
- unit: SEU-002
- source: S-091
- grade: SUPPORTED (historical industry document)
- scope and context: manufacturer layer view, pack and puff as dispenser.
- permitted inference: an industry scientist defined the cigarette as a nicotine package and dispenser, not as a flavour accessory.
- prohibited inference: quoting an internal memo as if it were a public-health consensus paper, or as a dare to smoke more to "see the product."
- empirical limit: internal research planning memo, not a consumer brochure or clinical trial.
- safety limit: No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.

E-09 — lights do not cut dose
- finding: ventilated light cigarettes do not reduce human intake; compensation with bigger puffs.
- reader line: ventilated/"light" cigarettes do not reduce human intake; smokers compensate with bigger puffs.
- unit: SEU-003
- sources: S-010, S-080, S-089
- grade: SUPPORTED
- scope and context: human smoking versus machine measurement.
- permitted inference: machine-measured lower tar/nicotine does not mean the smoker took less; compensation is the designed human response to a nicotine-seeking dose.
- prohibited inference: every smoker compensates identically, or that unventilated cigarettes are a harm-reduction recommendation.
- empirical limit: human smoking vs FTC-style machines; not identical compensation for every smoker.
- safety limit: No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.

E-10 — NRT trial odds vs actual attempts
- finding: licensed NRT raises trial abstinence vs control, while most real attempts are unassisted with low single-attempt success.
- reader line: licensed NRT vs control raises 6+ month abstinence (pooled RR 1.55); most smokers who try to quit do so unassisted, with unaided success around 7–8%.
- unit: SEU-004
- sources: S-077, S-078
- grade: CONTESTED as a single slogan; both component facts SUPPORTED in their own scopes
- scope and context: motivated trial quitters versus population attempts; different questions.
- permitted inference: NRT can raise odds versus placebo in trials; most attempts are still unmedicated; neither fact means the reader cannot quit, and neither fact is a prescription.
- prohibited inference: "you cannot quit without patches" or "cold turkey never works." The two statistics answer different questions and must not be collapsed.
- empirical limit: motivated trial quitters, not all smokers; population attempts, not lifetime; not a guarantee and not proof nobody quits without help.
- safety limit: No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.

E-11 — withdrawal short peak
- finding: withdrawal restlessness with short typical peak then easing.
- reader line: withdrawal symptoms typically peak in the first few days and usually subside within a few weeks; they may begin within hours; MedlinePlus places the sharpest edge about 2–3 days after last use.
- unit: SEU-005
- sources: S-009, S-081
- grade: SUPPORTED (population typical, not every reader)
- scope and context: day two or three without cigarette, irritability and craving.
- permitted inference: the restless empty feeling is withdrawal pharmacology with a short typical peak, not proof the cigarette was the real self.
- prohibited inference: withdrawal is weeks of physical torture for everyone, or that it is harmless for every person in every circumstance.
- empirical limit: population typical, not every reader; dependent users vary; genetics influence severity; does not negate rare complications.
- safety limit: No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.

## 3. Mantra and Frozen-Token Sheet

**M-A —** "you have nothing to lose and everything to gain"
- Wording: "you have nothing to lose and everything to gain"
- job: entry promise risk-reversal buying compliance with reading contract.
- debut: C01
- echo: C12
- hand-over: C14 kept as reader's risk answer when doubt appears.

**M-B —** "easily, immediately and permanently"
- Wording: "easily, immediately and permanently"
- job: impossible-sounding contract stated with total confidence.
- debut: C01
- echo: C07, C12
- hand-over: C14 carried as definition of what escape was.

**M-C —** "the nicotine trap"
- Wording: "the nicotine trap"
- job: central metaphor making stopping an escape, not sacrifice.
- debut: C02
- echo: C07, C09, C11, C12
- hand-over: C14 named as place left behind for good.

**M-D —** "the Nipper"
- Wording: "the Nipper"
- job: names trivial physical creature to starve; craving external, small, winnable.
- debut: C02
- echo: C07, C12
- hand-over: C14 dismissed as dead and starved.

**M-E —** "the Smokescreen"
- Wording: "the Smokescreen"
- job: names belief-system that feeds the Nipper; quitting is de-programming.
- debut: C02
- echo: C07, C09
- hand-over: C14 recognised as cleared lie.

**M-F —** "an empty, slightly restless, slightly edgy little tug"
- Wording: "an empty, slightly restless, slightly edgy little tug"
- job: sensory phrase relabelling withdrawal in book's words.
- debut: C02
- echo: C07, C08
- hand-over: C14 recalled as the feeling that no longer fools.

**M-G —** "the tug-of-war of fear"
- Wording: "the tug-of-war of fear"
- job: names torn state whose both ropes belong to trap.
- debut: C09
- echo: C11
- hand-over: C14 declared over because trap holds neither rope now.

**M-H —** "YIPPEE! I'M FREE!"
- Wording: "YIPPEE! I'M FREE!"
- job: terminal replacement thought for any future cigarette thought.
- debut: C12
- echo: C13
- hand-over: C14 given as final word and lifelong script.

**M-I —** "All you have to do is follow all the instructions."
- Wording: "All you have to do is follow all the instructions."
- job: ease clause closing loops, cashing won arguments into compliance.
- debut: C04
- echo: C06, C12
- hand-over: C14 left as proof ease was kept.

**F-A —** "It does plenty TO you. It does nothing FOR you."
- Wording: "It does plenty TO you. It does nothing FOR you."
- job: axis verdict compressing TO vs FOR switch.
- debut: C03
- echo: C05, C10
- hand-over: C14 kept as one-line ledger.

**F-B —** "It never fixed the itch. It caused it."
- Wording: "It never fixed the itch. It caused it."
- job: inversion thesis in portable sentence.
- debut: C07
- echo: C08, C11
- hand-over: C14 kept as itch answer.

**F-C —** "stale, breathless and chained"
- Wording: "stale, breathless and chained"
- job: cost triple naming addict's permanent state.
- debut: C09
- echo: C10
- hand-over: C14 recalled as former state, now past.

## 4. Scene and Analogy Bank

SC-A — night patio offer: friends, drinks, laughter, tray of lights, hand extending a cigarette with one won't hurt. Job: strongest seductive case to reassign. Constraint: never stage as nostalgic invite; stage to strip credit; no instruction to avoid friends or alcohol as method.

SC-B — morning feet: alarm, feet have not touched floor before hand finds pack, first drag on empty lungs. Job: inhabit ordinary trigger without cigarette. Constraint: concrete morning detail, no lab dose.

SC-C — reward pellet chain: finished class, paragraph, grocery run each paid with a light. Job: demolish reward justification. Constraint: keep work joy intact; credit work not pellet.

SC-D — closet hide: Febreeze, mints, garage door, hiding from partner and kids. Job: show trap cost and divided self. Constraint: warm to person, vicious to hiding need; no shaming of person.

SC-E — parking-meter coins: each puff drops a coin, meter fades in minutes, must feed again all day. Job: make ten-second pharmacology visible. Constraint: original prose; do not overclaim uniform timing for every smoker.

SC-F — hug that won't let go: grateful arms around rescuer who secretly tightened grip. Job: rescuer-as-perpetrator inversion image. Constraint: keep rescuer as cigarette, not person.

SC-G — whisky-for-brandy swap: gum, patch, vape as different glass for same drink. Job: demolish substitutes. Constraint: no prescription for or against medication; belief argument only, route medical specifics to CA-SAFE.

SC-H — hole in gas mask: lights vent holes that smoker unknowingly covers with lips and fingers, puffing harder. Job: expose mild fraud. Constraint: do not recommend unventilated as safer; no uniform-compensation claim.

SC-I — genie and cliff: just-one as rubbing lamp that rebuilds bottle; cutting down as jumping cliff but falling less. Job: foreclose moderation and special ones. Constraint: no dare to test one; slip pre-forgiven without licensing repeat.

SC-J — stairs breath: climbing stairs winded, non-smoker friend breathing easy, noticing cage. Job: entry hook and body authority. Constraint: body observation, no diagnosis.

SC-K — stress desk: argument, phone down, hand already reaching, first puff credited with calm while problem sits untouched. Job: demolish off-switch. Constraint: no claim cigarette treats problem or that stress without it is dangerous.

SC-L — pack as dispenser: pack as day's supply box, cigarette as tube, puff as squirt of nicotine, factory counting doses. Job: widen indictment to manufacture. Constraint: present as industry definition per E-08, not as public-health consensus; no extra profit figures beyond ledger.

SC-M — last farewell table: ordinary last cigarette smoked with full attention on yellow stain, ash, stale end, then stubbed with vow. Job: ritualise exit on disgust and joy. Constraint: ceremonial, not a dare to smoke extra; attention on ugliness, no laboratory tasting.

## 5. Lexicon and Instruction Spine

- trap register: dose, fix, hit, feed the Nipper, the nicotine trap, the Smokescreen, brainwashing, con, slavery, chained, conned. Cigarette units always doses, never treats.
- freedom register: escape, free, freedom, marvellous, wonderful, exciting, rejoice, celebrate, relief, clean air, breathe easy, get on with enjoying your life.
- banned register: give up, resist, stay strong, discipline, abstain, sacrifice except as illusion of sacrifice, trying to stop, one day at a time, recovery journey, quit cold turkey as framing. Quit as plain verb allowed.
- reader dialect, source-grounded: ciggies, the stick, bumming cigs, habit smokes, closet smoker, Febreeze the hell out of myself, one won't hurt, little parties, smober, can't quit now, I AM AN ADDICT as quoted voice only.

Instruction spine, spoken Carr imperative only:

**I-01 —** KEEP AN OPEN MIND 
- Wording: KEEP AN OPEN MIND / Give this book a fair hearing and it will free you. Owning: C01. Recap: C14.
**I-02 —** DON'T STOP OR CUT DOWN YET 
- Wording: DON'T STOP OR CUT DOWN YET / Smoke as normal until your last cigarette. Owning: C02. Recap: C14.
**I-03 —** BEGIN BY FEELING GREAT TO BE ESCAPING 
- Wording: BEGIN BY FEELING GREAT TO BE ESCAPING / There is no doom here, only freedom ahead. Owning: C03. Recap: C14.
**I-04 —** FOLLOW ALL THE INSTRUCTIONS 
- Wording: FOLLOW ALL THE INSTRUCTIONS / All you have to do is what this book asks. Owning: C04. Recap: C14.
**I-05 —** IGNORE ANY ADVICE THAT CONFLICTS WITH THIS BOOK 
- Wording: IGNORE ANY ADVICE THAT CONFLICTS WITH THIS BOOK / Let this argument finish before you borrow another. Owning: C05. Recap: C14.
**I-06 —** DISREGARD ANYONE WHO QUIT BY WILLPOWER 
- Wording: DISREGARD ANYONE WHO QUIT BY WILLPOWER / Their struggle was the method, not you. Owning: C06. Recap: C14.
**I-07 —** REFUSE TO BE INFLUENCED BY OTHER SMOKERS 
- Wording: REFUSE TO BE INFLUENCED BY OTHER SMOKERS / Watch them with clear eyes and keep your own judgment. Owning: C07. Recap: C14.
**I-08 —** TRUST YOUR BODY TO BREATHE AND TASTE 
- Wording: TRUST YOUR BODY TO BREATHE AND TASTE / Your body knows freedom without being taught. Owning: C08. Recap: C14.
**I-09 —** SEE THE SELLER BEHIND THE SMOKE 
- Wording: SEE THE SELLER BEHIND THE SMOKE / Remember who built the trap and why. Owning: C09. Recap: C14.
**I-10 —** MEET THE BEST CIGARETTE HEAD-ON 
- Wording: MEET THE BEST CIGARETTE HEAD-ON / Let the favourite prove it gives nothing. Owning: C10. Recap: C14.
**I-11 —** NEVER ALLOW JUST ONE OR A SPECIAL ONE 
- Wording: NEVER ALLOW JUST ONE OR A SPECIAL ONE / One keeps the trap alive. Owning: C11. Recap: C14.
**I-12 —** SMOKE YOUR FINAL CIGARETTE AND KNOW YOU ARE FREE 
- Wording: SMOKE YOUR FINAL CIGARETTE AND KNOW YOU ARE FREE / Close the trap with joy, not sadness. Owning: C12. Recap: C14.

CA-SAFE — plan-wide clinical advisory, boxed in manuscript per practical-safety guardrail:
> If you live with a medical condition, take prescribed medication, feel ill, feel severe distress, or worry about stopping, speak to a clinician for personal care. This book changes what you believe smoking gives you; it does not give medical advice and does not ask you to ignore a doctor. The last cigarette is a farewell, not a dare to smoke extra or to test yourself.

Cards cite CA-SAFE in guardrails only; never paste the box mid-chapter; instructions carry bare imperatives.

## 6. Arc and Length

Architecture: 14 chapters. C01 contract and hook. C02 trap first seen with creatures in passing and body encounters. C03 axis switch. C04–C07 demolitions and mechanism deepening on installed ground. C08 inhabit ordinary doing. C09 widen indictment plus fear. C10 strongest case plus embedded testimony. C11 escape routes plus myths battery and meta-inoculation. C12 last ordinary instance and vow. C13 ordinary life with owned thoughts once. C14 short photographable recap and outward push.

- concept debuts: contract C01; trap and creatures and sensory C02; TO/FOR C03; ease clause C04; off-switch kill C04; reward and lights kill C05; anti-method C06; inversion deepening C07; inhabit C08; villain dossier and tug-of-war and cost triple C09; strongest case C10; just-one and myths C11; terminal mantra and vow C12; ordinary life C13; ending reframe C14 only.
- demolition curve: low C01, rising C03–C05, peak C06–C11, handing to freedom after C12.
- freedom crescendo: promise C01, suppressed C04–C09 to let demolition work, rising C10–C11, detonated C12–C14 with more freedom language than rest combined.
- structural responsibilities: long testimony in main flow C10; myths Q&A distinct room C11; meta-inoculation C11; inhabit C08; last ordinary instance C12; ordinary life C13; short recap C14; no mid-book recap; prevalence claim once C06 via E-03 typicality.
- instruction placements: I-01 C01 through I-12 C12, recap C14 without chapter callbacks.
- saved ending reframe: ashtray already empty, C14 only.
- budgets: C01 3500, C02 4000, C03 4500, C04 4500, C05 5000, C06 4500, C07 4500, C08 4000, C09 4500, C10 4000, C11 3500, C12 4000, C13 4500, C14 5000. Arithmetic sum: 3500+4000+4500+4500+5000+4500+4500+4000+4500+4000+3500+4000+4500+5000 = 60000 words.

## 7. Chapter Cards

**CH-01 — Read This First and Be Free
- primary job: non-argument — bridge: install easy contract and hook so belief work can start without dread.
- arc position: first third opening; freedom promise front-loaded, demolition low.
- reader-state: tired trier arriving braced for lecture, encountering stairs-breath proof ease is possible.
- mantra: debut M-A "you have nothing to lose and everything to gain"; debut M-B "easily, immediately and permanently".
- scene: debut SC-J, staging job: stairs-breath hook and body authority.
- structural responsibility: authority dossier and reading contract.
- guardrails: safety CA-SAFE; originality: origin and stairs in new prose, no borrowed caffeine images.
- continuity intent: receives none; hands open mind and permission to continue smoking until vow to C02.
- budget: 3500
- new instruction: I-01 KEEP AN OPEN MIND

**CH-02 — Are You Really Choosing This
- primary job: enacted transition — the reader stops seeing smoking as free choice and starts seeing a trap they were conned into.
- belief now: enters believing smoking is my choice and habit I enjoy; leaves believing a trap removed choice and two mechanisms keep me.
- concrete encounter: hiding to smoke and Febreeze, watching own hand move before decision.
- evidence: E-04 plus limit moment lighting only, not day-long gift; E-01 credit false yet felt.
- new instruction: I-02 DON'T STOP OR CUT DOWN YET
- reserved-later fence: off-switch kill to C04; reward kill to C05; substitutes to C06; inversion detail to C07.
- arc position: first third trap first seen; demolition rising.
- reader-state: defensive chooser, encountering closet hide that choice would not need.
- mantra: debut M-C "the nicotine trap"; debut M-D "the Nipper"; debut M-E "the Smokescreen"; debut M-F "an empty, slightly restless, slightly edgy little tug".
- scene: debut SC-D, staging job: closet hide cost.
- guardrails: safety CA-SAFE, E-04 safety limit; originality: creatures named in passing, not as lesson unit.
- continuity intent: receives contract from C01; hands trap vocabulary to C03.
- budget: 4000

**CH-03 — What Does It Actually Do For You
- primary job: enacted transition — reader stops weighing harm versus benefit and demands what benefit at all.
- belief now: enters seeing trap but still counting pleasures against risks; leaves asking what good remains once credit is questioned.
- concrete encounter: listing own reasons aloud, then checking what cigarette added to food, pause, company.
- evidence: E-04 plus limit enjoyment at light only; E-05 party is cigarette not work.
- new instruction: I-03 BEGIN BY FEELING GREAT TO BE ESCAPING
- reserved-later fence: variable isolation demos to C04, C05; strongest patio to C10.
- arc position: first third axis switch; demolition rising.
- reader-state: ledger-keeper weighing pros and cons, encountering hug image that rescuer may be perpetrator.
- mantra: debut F-A "It does plenty TO you. It does nothing FOR you."
- scene: debut SC-F, staging job: hug that won't let go.
- guardrails: safety CA-SAFE; originality: speak TO/FOR, never as worksheet.
- continuity intent: receives trap vocabulary from C02; hands axis to C04.
- budget: 4500

**CH-04 — The Calm That Creates the Storm
- primary job: enacted transition — stress relief stops reading as cure and starts reading as brief quiet of a need smoking created.
- belief now: enters believing cigarette takes care of stress; leaves believing it leaves the problem untouched while briefly quieting its own tug.
- concrete encounter: stress desk after argument, hand reaching, problem papers still there after puff.
- evidence: E-01 plus limit does not treat underlying problem; E-07 relief is replenishment not gift; limits smoked pharmacokinetics only.
- new instruction: I-04 FOLLOW ALL THE INSTRUCTIONS
- reserved-later fence: withdrawal timing detail to C07; fear of life without to C09.
- arc position: middle early demolition; freedom suppressed.
- reader-state: pressured reliever seeking off-switch, encountering desk moment where calm is mistimed.
- mantra: debut M-I "All you have to do is follow all the instructions."
- scene: debut SC-K, staging job: stress-desk reach.
- guardrails: safety CA-SAFE, E-01 safety limit; originality: new desk prose, no mocking of felt relief.
- continuity intent: receives axis from C03; hands keystone-relax kill to reward kill C05.
- budget: 4500

**CH-05 — Parties, Pauses and Milds
- primary job: enacted transition — reward, taste and mild stop reading as gifts and start reading as stolen credit and compensated puffing.
- belief now: enters still keeping reward and enjoyment exceptions; leaves seeing party was work and mild was harder puffing.
- concrete encounter: teaching, paragraph, grocery run each paid with pellet, then tasted without.
- evidence: E-05 party is cigarette not work; E-09 machine lower does not mean took less; limits not identical for every smoker, no safer recommendation.
- new instruction: I-05 IGNORE ANY ADVICE THAT CONFLICTS WITH THIS BOOK
- reserved-later fence: substitutes to C06; strongest social reward to C10.
- arc position: middle demolition; demolition high.
- reader-state: pleasure-keeper defending little parties, encountering pellet chain and vent holes.
- mantra: echo F-A "It does plenty TO you. It does nothing FOR you."
- scene: debut SC-C, staging job: reward pellet chain; debut SC-H, staging job: hole in gas mask.
- guardrails: safety CA-SAFE, E-09 safety limit; originality: gas-mask and pellet in new prose.
- continuity intent: receives relax kill from C04; hands enjoyment cleared to anti-method C06.
- budget: 5000

**CH-06 — Why Willpower Never Worked
- primary job: enacted transition — past failures stop proving I am weak and start proving the method was wrong.
- belief now: enters believing I lack willpower and need a prop to quit; leaves believing the Willpower Method manufactures struggle and trial odds do not decide my escape.
- concrete encounter: drawer of patches and gum, calendar of twenty attempts, fear of next try.
- evidence: E-03 typical failed attempts not unique weakness; E-10 NRT trial vs unassisted answer different questions, neither prescribes, must not collapse; limits trial vs population scopes.
- new instruction: I-06 DISREGARD ANYONE WHO QUIT BY WILLPOWER
- reserved-later fence: mechanism timing to C07; pity script to C12–C13; myths battery to C11.
- arc position: middle anti-method peak; demolition high; prevalence claim once here via E-03 typicality.
- reader-state: ashamed repeater expecting blame, encountering method as culprit.
- mantra: echo M-I "All you have to do is follow all the instructions."
- scene: debut SC-G, staging job: whisky-for-brandy swap.
- structural responsibility: anti-method chapter; meta-inoculation seed answering method-is-brainwashing objection in passing.
- guardrails: safety CA-SAFE, E-10 safety limit no prescription; originality: strong will reframed wilful not weak-willed in new words.
- continuity intent: receives cleared pleasures from C05; hands method blame to mechanism C07.
- budget: 4500

**CH-07 — The Itch It Pretends to Scratch
- primary job: enacted transition — relief stops reading as rise above normal and starts reading as brief return toward non-smoker baseline that guarantees next low.
- belief now: enters knowing pleasures are empty but still fearing physical need; leaves seeing physical tug trivial and belief dominant.
- concrete encounter: tracking a day of doses fading within minutes, meter needing coins.
- evidence: E-07 replenishment not gift; E-11 restless feeling short typical peak not real self; limits typical not every reader, not torture-for-all.
- new instruction: I-07 REFUSE TO BE INFLUENCED BY OTHER SMOKERS
- reserved-later fence: body inhabit to C08; industry build to C09.
- arc position: middle mechanism deepening; demolition peak.
- reader-state: body-fearful smoker dreading withdrawal, encountering meter fade as small and brief.
- mantra: echo M-B "easily, immediately and permanently"; echo M-C "the nicotine trap"; echo M-D "the Nipper"; echo M-E "the Smokescreen"; echo M-F "an empty, slightly restless, slightly edgy little tug"; debut F-B "It never fixed the itch. It caused it."
- scene: debut SC-E, staging job: parking-meter coins.
- guardrails: safety CA-SAFE, E-11 safety limit; originality: meter and itch in new prose, creatures already vocabulary.
- continuity intent: receives method blame from C06; hands inversion to inhabit C08.
- budget: 4500

**CH-08 — Mornings, Meals and Breaks Without It
- primary job: enacted transition — inhabiting ordinary smoke moments as breathing, tasting, free-handed favourite proves non-smoker pleasure is fuller.
- belief now: enters understanding inversion yet unsure ordinary moments can please without; leaves having lived morning, meal-end and break as complete without dose.
- concrete encounter: morning feet to kettle, meal-end taste lingering, work break air on face, hands free.
- evidence: E-05 celebrations remain without pellet; E-11 empty tug not self; limits moment accounts only.
- new instruction: I-08 TRUST YOUR BODY TO BREATHE AND TASTE
- reserved-later fence: strongest patio proof to C10; ordinary life living to C13.
- arc position: middle inhabit-the-ordinary-doing; freedom beginning to rise.
- reader-state: hesitant imaginer of empty breaks, encountering full sensory morning.
- mantra: echo M-F "an empty, slightly restless, slightly edgy little tug"; echo F-B "It never fixed the itch. It caused it."
- scene: debut SC-B, staging job: morning feet; token-echo SC-C as pellet phrase only; token-echo SC-J as stairs-breath phrase only.
- structural responsibility: inhabit-the-ordinary-doing chapter.
- guardrails: safety CA-SAFE; originality: inhabit as primary, not kill with inhabit flavour.
- continuity intent: receives inversion from C07; hands lived baseline to indictment C09.
- budget: 4000

**CH-09 — Who Built This Want
- primary job: enacted transition — desire stops reading as my nature and starts reading as manufactured package plus fear both held by trap.
- belief now: enters owning baseline yet still fearing failure and success without identity; leaves seeing seller built want and both fear ropes belong to trap.
- concrete encounter: holding pack as day's supply box, noticing theatre of filter and mild promise.
- evidence: E-08 industry definition as package not flavour; E-09 lights theatre; limits internal memo not consensus, no safer recommendation.
- new instruction: I-09 SEE THE SELLER BEHIND THE SMOKE
- reserved-later fence: favourite-scene proof to C10; just-one foreclose to C11.
- arc position: middle-late widening plus fear; demolition high, freedom rising.
- reader-state: uneasy candidate fearing failure and post-quit self, encountering pack as dispenser.
- mantra: echo M-C "the nicotine trap"; echo M-E "the Smokescreen"; debut M-G "the tug-of-war of fear"; debut F-C "stale, breathless and chained".
- scene: debut SC-L, staging job: pack as dispenser.
- structural responsibility: fear chapter collapsing failure and success fears.
- guardrails: safety CA-SAFE, E-08 safety limit no dare to test; originality: villain anger at maker, never at reader.
- continuity intent: receives baseline from C08; hands manufacture to strongest case C10.
- budget: 4500

**CH-10 — The Night Out That Proves It
- primary job: enacted transition — the most seductive cigarette stops surviving as exception and proves sneaking a ride on night, drink and friendship.
- belief now: enters keeping one social exception; leaves seeing patio pleasure was scene all along.
- concrete encounter: late patio, drinks, offered light, tasting night air with and without.
- evidence: E-02 social plus drink collapses rule; E-04 heaven at light only; limits no social-avoidance method.
- new instruction: I-10 MEET THE BEST CIGARETTE HEAD-ON
- reserved-later fence: cut-down and tomorrow foreclose to C11; vow to C12.
- arc position: late-middle strongest case; freedom rising.
- reader-state: social smoker guarding belonging, encountering offer reframed.
- mantra: echo F-A "It does plenty TO you. It does nothing FOR you."; echo F-C "stale, breathless and chained".
- scene: debut SC-A, staging job: night patio offer full staging.
- structural responsibility: strongest case met head-on; embedded long testimony in main flow in its own room.
- guardrails: safety CA-SAFE, E-02 safety limit; originality: patio in new prose, credit to sun, leisure, company.
- continuity intent: receives manufacture from C09; hands no-exception to escape routes C11.
- budget: 4000

**CH-11 — No Special Ones, No Tomorrow
- primary job: enacted transition — cut down, special ones and tomorrow stop reading as safe compromises and start reading as trap kept alive.
- belief now: enters conceding favourites yet bargaining for one; leaves seeing one rebuilds bottle and delay extends cost.
- concrete encounter: five months free then one, and cut-down diary creeping back up.
- evidence: E-06 long quit does not make one safe; E-10 neither fact licenses willpower slogan; limits no doom if belief guarded, no collapse of stats.
- new instruction: I-11 NEVER ALLOW JUST ONE OR A SPECIAL ONE
- reserved-later fence: vow readiness gate to C12 only.
- arc position: late foreclose; demolition handing to freedom.
- reader-state: bargainer seeking safe limit, encountering genie rebuilt.
- mantra: echo M-C "the nicotine trap"; echo M-G "the tug-of-war of fear"; echo F-B "It never fixed the itch. It caused it."
- scene: debut SC-I, staging job: genie and cliff; token-echo SC-A as patio phrase only.
- structural responsibility: myths Q&A distinct rapid-fire room; meta-inoculation answering strongest method objection performed without label.
- guardrails: safety CA-SAFE, E-06 safety limit no dare, slip as warning not license; originality: pre-scripted future thoughts arrive pre-labelled as trap script.
- continuity intent: receives no-exception from C10; hands totality to vow C12.
- budget: 3500

**CH-12 — Your Last Cigarette
- primary job: enacted transition — smoker identity crosses to non-smoker in a joyful solemn act with freedom conferred now.
- belief now: enters ready but still smoker; leaves free as instant identity, champing at bit.
- concrete encounter: ordinary last cigarette with full attention on stain, ash and stale end, then stubbed.
- evidence: E-11 peak is short and fading if smokefree; E-06 one never safe hence finality; limits typical not every reader.
- new instruction: I-12 SMOKE YOUR FINAL CIGARETTE AND KNOW YOU ARE FREE
- reserved-later fence: ordinary days living to C13; recap to C14 only.
- arc position: threshold after demolitions; freedom detonated.
- reader-state: ready quitter at gate, encountering farewell table.
- mantra: echo M-A "you have nothing to lose and everything to gain"; echo M-B "easily, immediately and permanently"; echo M-C "the nicotine trap"; echo M-D "the Nipper"; echo M-I "All you have to do is follow all the instructions."; debut M-H "YIPPEE! I'M FREE!"
- scene: debut SC-M, staging job: last farewell table.
- structural responsibility: last ordinary instance, readiness gate, vow and instant conferral, warning against two relapse doors.
- guardrails: safety CA-SAFE; originality: ritual ordinary not laboratory, attention on ugliness, congratulation immediate.
- continuity intent: receives totality from C11; hands free identity to ordinary life C13.
- budget: 4000

**CH-13 — Mornings, Shops and Ordinary Days
- primary job: non-argument — hand-off: live free days proving belief in owned thoughts once, handing freedom forward without new curriculum.
- arc position: after vow life, not manuals; freedom high.
- reader-state: new non-smoker meeting first triggers, encountering morning, shop queue and break already owned.
- mantra: echo M-H "YIPPEE! I'M FREE!"
- scene: token-echo SC-A as patio phrase only; token-echo SC-B as morning phrase only.
- structural responsibility: ordinary-life chapter using thoughts reader already owns once.
- guardrails: safety CA-SAFE; originality: live days, do not restage settled scenes or teach thought curriculum.
- continuity intent: receives free identity from C12; hands lived proof to recap C14.
- budget: 4500

**CH-14 — Free for Good
- primary job: non-argument — recap: photograph list of spoken instructions and hand reader outward into life with fresh reframe.
- arc position: close short recap then life; freedom full.
- reader-state: free reader needing portable memory, encountering empty ashtray reframe.
- mantra: hand-over M-A through M-I and F-A through F-C as kept scripts; final word M-H "YIPPEE! I'M FREE!"
- scene: token-echo SC-M as farewell-table phrase only.
- structural responsibility: photographable instruction list without chapter callbacks; outward imperative; saved ending reframe debut: the ashtray was already empty — you were the one who kept refilling it.
- guardrails: safety CA-SAFE; originality: ending revelation not recap only, no new demolition.
- continuity intent: receives lived proof from C13; hands freedom for rest of life.
- budget: 5000
```

### This chapter's card
```
**CH-06 — Why Willpower Never Worked
- primary job: enacted transition — past failures stop proving I am weak and start proving the method was wrong.
- belief now: enters believing I lack willpower and need a prop to quit; leaves believing the Willpower Method manufactures struggle and trial odds do not decide my escape.
- concrete encounter: drawer of patches and gum, calendar of twenty attempts, fear of next try.
- evidence: E-03 typical failed attempts not unique weakness; E-10 NRT trial vs unassisted answer different questions, neither prescribes, must not collapse; limits trial vs population scopes.
- new instruction: I-06 DISREGARD ANYONE WHO QUIT BY WILLPOWER
- reserved-later fence: mechanism timing to C07; pity script to C12–C13; myths battery to C11.
- arc position: middle anti-method peak; demolition high; prevalence claim once here via E-03 typicality.
- reader-state: ashamed repeater expecting blame, encountering method as culprit.
- mantra: echo M-I "All you have to do is follow all the instructions."
- scene: debut SC-G, staging job: whisky-for-brandy swap.
- structural responsibility: anti-method chapter; meta-inoculation seed answering method-is-brainwashing objection in passing.
- guardrails: safety CA-SAFE, E-10 safety limit no prescription; originality: strong will reframed wilful not weak-willed in new words.
- continuity intent: receives cleared pleasures from C05; hands method blame to mechanism C07.
- budget: 4500
```

### The draft chapter
```
Chapter 6
THE METHOD THAT MADE YOU FAIL

*You did not fail twenty times — the method failed you twenty times, and it was built to do exactly that.*

### THE DRAWER THAT SAYS NOTHING ABOUT YOU

You have watched the pellet take credit for work it never did, the pause steady without smoke in it, the mild holes covered by your own lips and fingers. Keep that clear eye. We turn it now where the shame sits thickest.

Open the drawer with me.

Patches in foil gone soft at the corners. Gum in a blister pack, half the dents pushed through, the mint dust still in the bottom. A lighter thing that heats and hisses. A calendar on the side with crosses and dates rubbed out and started again. January. March. After the holiday. Monday.

Say what we say standing over that drawer when no one else hears.

"I lack willpower. I need a prop to quit."

And this, from inside our own tribe, spoken flat because it happened so often:

"I had probably attempted at least twenty times before and used most of the replacements and meds on the market with no success."

I have stood at that drawer. I counted my own crosses. I told myself the next try would need a stronger arm, a harder jaw, a better reason to be miserable for a while.

Listen to me on this, because I speak as a man who lived it and got out the other side. You are not weak. You are not missing a muscle other men were given.

We were wilful, not weak-willed. Think what it takes to keep inhaling paper smoke against cough in the morning, against money burned, against standing in rain outside your own house, against hiding the smell from people you love. A weak man could not keep that up for years. Only a stubborn, set-jawed will could persist in something that goes against every instinct of nose and chest. Your will was never the problem. The orders it was given were the problem.

If lack of backbone were the cause, how do you explain that the same backbone held jobs, raised children, drove through nights, sat examinations, nursed parents, while the crosses piled up on the calendar. Did the backbone vanish on Mondays and return on Tuesdays. Or was a different weight put on it that no backbone was built to carry.

Ask from your own drawer, not from me.

If straining and enduring worked, why did twenty strains leave you lighting the next dose. If suffering proved strength, why did the strongest sufferers you know still stand outside with you. If the prop fixed the need, why did the want sit untouched underneath the patch and wake the hour the patch came off.

You know. The drawer does not prove you cannot quit. It proves the way you were told to quit cannot work, and that you are like thousands of others who proved the same thing the same way.

That likeness matters. Your twenty tries do not mark you as specially broken. They mark you as normally conned. In house after house the same drawer sits with the same foil and the same calendar. One failure is private shame. Twenty thousand identical failures is evidence about the instructions, not about the men who followed them.

It was never you. It was the method.

Look harder at that calendar, because the calendar tells more truth than the foil. The dates are never random. They are Mondays. Firsts of months. Birthdays. After the wedding. After the cough clears. After the holiday. We chose a clean edge and wrote a promise on it, and the promise was always the same shape: from this date I will be a man who wants a dose every hour and does not take it.

Read that promise aloud and hear how strange it is. Not: from this date I will see the dose gives nothing. But: from this date I will want and not have. From this date I will miss and not take. From this date I will be two men — one who reaches and one who slaps the hand.

No wonder the hand shook by Wednesday. No wonder the eyes kept sliding to the clock, to the shop, to the friend who still lights. You had not removed the want. You had declared war on it while leaving its food supply intact in the mind. The Smokescreen stood untouched behind the patch, whispering that a friend was lost, and the Nipper tugged underneath, small but believed large because belief lent it a loudspeaker.

I do not blame you for believing that loudspeaker. We all did. We were told that quitting meant losing something real and paying for the loss with strain. When strain did not kill the want, we blamed the arm that strained. That blame is the deepest cruelty of the whole con. It turns evidence against the method into evidence against the man.

So stand at the drawer a minute longer and reverse the verdict. The foil did not fail because you opened it wrong. The gum did not fail because you chewed too little or too much. The calendar did not fail because you chose the wrong Monday. They failed because they were ordered to do what no prop can do: make you stop wanting what you still believed you needed.

### THE SAME DRINK IN A DIFFERENT GLASS

With shame thinned, the kindest lie arrives to explain the drawer.

"The cigarette was too strong to drop at once. I need the nicotine without the smoke. A cleaner glass for the same drink."

I understand why that feels sensible. Look at the glass, not the promise.

Order whisky in a pub. The barman pours it into a thick tumbler. Next night he pours the same whisky into a brandy balloon. Next night into a chipped mug. The glass changes. The hand feels different around it. The smell rises differently. Would you say you stopped drinking whisky because the glass changed.

That is what the swap is. Gum, skin patch, heated stick that hisses — different glass, same whisky. The dose arrives slower, or through cheek, or through skin, or with a sweet smell, and we call the new arrival a cure for the old arrival. The hand still watches the clock. The mind still counts down to the next top. The little ceremony of topping still owns the day, only now it wears a white packet and calls itself sensible.

I speak here of belief only, not of medicine — and for anything medical, speak to your own clinician, I give no medical orders. My point is narrower and it cuts deeper. While the glass holds the same drug, the brain keeps the same lesson: I cannot face a finished job, a pause, a night out, without a top from outside. The lesson is the Smokescreen fed and watered. The Nipper, that tiny physical tug, is kept alive on sips instead of starved at once.

Watch what the swap teaches between doses.

With paper doses the tug woke, you fed it, it slept for forty minutes. With the swapped glass the tug wakes duller, you feed it duller, it never quite sleeps and never quite wakes. The day becomes one long half-want instead of peaks and troughs. Men tell me they felt less tortured and more tethered — able to sit through a film, unable to forget the film was sat through on a leash. Is that what you wanted. To change the length of the leash and call it walking out of the nicotine trap.

Ask from your own mouth, not from theory.

Did the gum ever make a meal taste complete, or did it make the mouth busy while the mind missed the light. Did the patch ever remove the hand reaching at the stress desk, or did the hand reach with the patch on. Did the new glass ever kill the thought "one real one would settle this," or did it keep that thought alive by keeping the seat warm for it.

You know from the drawer, not from me.

And see who is flattered by keeping the swap story alive. While it lives, the seller of doses keeps a customer through the very try to leave, and the Willpower Method keeps its alibi. If you fail with a prop, they say you did not try hard enough. If you succeed for a while with a prop, they say the prop did it and you must fear life without it. Either way the credit for your own seeing is stolen and handed to rubber and mint.

I am harsh to that thievery, never to you. You reached for the drawer because you are a practical person who wanted a bridge. Your practical sense was real. It was spent on different glasses poured from the same bottle.

Once seen, the swap cannot be unseen. A new glass does not teach the brain that no glass is needed. It teaches that the drink must continue under another name.

Look at the hands that live with the swapped glass for a month. The packet in the pocket is gone, but the watching has not gone. It has moved. Where the eyes once dropped to count paper tubes left till evening, they now count squares left on a card, pellets left in a tin, hours till the patch can come off, hours till the next piece can go in. The arithmetic is identical. Only the objects counted have changed.

And the mouth learns the same waiting. Before, the mouth waited for the lighter click. Now it waits for the peppery burn of the cheek, the slow itch under the shoulder blade, the hiss and-sweet smell from the heated stick. The waiting is still the day's backbone. A man who waits all day for the next top, whatever the top is called, is still a man hired out to topping.

Would a man who had truly seen there was nothing to top wait like that. Would he count squares and pellets with the same narrowed eyes he once used to count tubes. You know he would not. The counting itself confesses the belief is still in the room: something outside me must arrive or the hour cannot run.

That is why the drawer fills and refills. Not because you are forgetful. Because each glass leaves the lesson standing, and the standing lesson calls for another glass when this one empties.

### WHY THE STRAIN NEVER ENDS

Now name the method itself, because unnamed it passes for common sense.

The Willpower Method says: the dose gives you something real, you must live without it, you must strain against the want until the want dies of exhaustion.

Do you see the three lies packed into one sentence. That the dose gave. That living without is living with less. That strain can kill a want it feeds every hour by attention.

Strain keeps the want alive by telling the brain every morning that something precious is missing and must be mourned. Mourning makes precious. Precious makes missing sharper. Missing sharper demands more strain. Round it goes, month after month, until the man either breaks and lights — and calls himself weak — or holds out white-knuckled for years and calls that holding freedom. With the Willpower Method there is no finish line. There is only holding on longer.

That is why the voices around it sound the way they do. You know them both.

The bragger in the pub: "I quit by sheer force. Hardest three months of my life. Nearly broke me." He leans back for admiration. He does not notice what he confessed. If it nearly broke him to stop doing something that gave him nothing, what does that say about the giving. Or about the stopping.

The whinger in the corner: "You don't know how bad I had it. The cravings. The nights. You can't expect me to go through that again." He asks for pity for a torture the method arranged. He does not notice he is advertising the method, not describing quitting.

Both speak as if the pain proved the pleasure was great. It proved the opposite. It proved they kept the belief intact — that the dose was a friend lost — and then wrestled the friend's ghost for months. Of course wrestling a ghost is exhausting. The answer is not stronger arms. The answer is to see there was never a friend in the room.

Think of two men told to avoid a film that bores them. Do they strain. Do they count days since they last sat through it. Do they chew something to replace the boredom. They simply do not go, and the not-going costs nothing because the want is gone. That is what it is like when the belief changes first. No strain is needed where no loss is felt.

Some will mutter here, "Isn't this book just putting another spell on me instead of the old one." I welcome that suspicion. Keep your eyes open and test every sentence against your own day. The old spell told you smoke calmed, rewarded, softened, helped — and charged you for the telling. This book tells you to look at class taught, paragraph stood, pause steadied, mild covered by flesh, and to give the credit back where your own memory says it belongs. One is a story laid over your life. The other is your life with the story lifted off. Judge by checking, not by trusting.

All you have to do is follow all the instructions.

Read that as a practical fact, not a boast. The instructions do not ask for strain. They ask for seeing kept in order until the last dose, then no more doses because no more belief needs them.

Mark the difference in the body, not in slogans. Under the old orders the shoulders lived high. Jaw set. Hands busy with substitutes. Eyes bright with holding. Sleep thin because the mind rehearsed missing. Talk loud about days counted because counting was the only proof holding was happening. Under seeing-first orders none of that furniture is needed. The shoulders do not climb because nothing is declared missing. The hands are not given a replacement chore because no empty place is declared. The mind does not rehearse missing because missing is not on the bill.

Which of those two states would you call strength. The man who holds his breath for months and calls the holding health. Or the man who breathes normally because he stepped out of the room that needed holding. Ask plainly and the word strength changes hands.

### TWO COUNTS THAT DO NOT OWN YOU

Two counts are waved at men over our drawer, and both are used to frighten.

One count says: in clinics where smokers who wanted to quit were followed closely, those given a licensed prop stayed clear months later in larger numbers than those given a dummy.

The other count says: out in the street most tries are made with no prop at all, and only a small handful hold on any single unaided try — and that says nothing about you once the trap is seen, it only describes tries made still believing the dose gave something.

Both counts are true in their own rooms. Neither count is a sentence on you, and they must not be folded into one slogan.

The first room is a narrow room: picked volunteers, watched, counted, encouraged, handed props on schedule. The second room is the wide world: tired men on Mondays, no watcher, no schedule, still believing they are losing a friend and must suffer to lose him. Different rooms, different questions. To lift a number from the narrow room and lay it across your kitchen table as proof you need rubber to be free is false. To lift a number from the wide world and lay it across your chest as proof you cannot quit is false.

Ask the questions whose only answer frees the counts from your neck.

Does a larger count in a watched room prove your own seeing cannot change what you want. Does a small count among men still mourning a friend prove anything about a man who has stopped mourning because he saw there was no friend. If numbers decided escape, how did any man ever walk out before numbers were printed.

You know. Counts describe groups under old belief. They do not decide one reader with new eyes.

There is a further trick in how those counts are spoken in pubs and clinics. They are spoken as if they were about you. "Most fail, so you will fail." "Props double chances, so you need props." Listen to the grammar. It moves a description of many men under one belief and lays it like a verdict on one man who is changing his belief. That move is false in any subject, not only this one. The number of men who once got lost on a road with no sign does not decide what you will do now the sign is up.

Keep the counts where they belong: in their rooms, answering their questions, owning no one.

### WHAT YOU DO WITH NEXT MONDAY

So let the drawer stay shut without fear of the next try.

I say that sentence and I know what rises behind it, because it rose in me. The calendar is still on the wall. Next Monday is still a square. The pen is still in the pot by the phone. The drawer is still in the kitchen with its foil and its dents. Fear says: you will have to open it again, you will have to pick another date, you will have to go through the whole grinding wheel once more, and this book is only dressing that wheel in nicer words.

Look at that fear directly with me, and live the square instead of dreading it.

See next Monday as it used to arrive under the old orders. Sunday night. The packet low on purpose. The speech to the wife, to the mate, to yourself in the mirror: tomorrow is the day. The little ceremony of the last pack crushed too early to prove resolve. Sleep with the head already rehearsing. Alarm. Hand goes to the bedside before thought — and is slapped back by thought. No. Not today. Today I am a man who does not. The hand hovers. The chest tightens not from need but from the announcement of missing.

Then the kitchen. Kettle. The calendar with the thick cross drawn before breakfast, the ink still wet. The foil torn. The square stuck to the arm. The gum loaded like ammunition. The phone checked for messages of encouragement. The whole house briefed that today is Day One and the man must be handled gently because he is giving something up.

By ten the eyes are on the clock. By eleven the work is half-held because half the mind is holding. By lunch the missing has a voice: you have been good, you have suffered, one would prove you are still in charge. By evening the voice is louder than the morning speech. Either the man lights and writes FAILURE across the square in his head, or he holds and writes DAY ONE across the square and knows he must write DAY TWO tomorrow, and DAY THREE, and DAY THREE HUNDRED, with the same holding. Both endings keep the wheel turning. One lights. One holds. Neither questions the orders.

That is the try you fear. Name it exactly so it cannot hide behind the word quit. It was mourning a kept belief with a different glass in hand.

Now see the same Monday under what this book actually asks. No speech on Sunday night. No packet crushed for show. No cross drawn before breakfast. You smoke as normal while you read, because reading with the tug quiet lets you see clearer than reading while holding. The drawer stays shut not because you are forbidding yourself its contents but because its contents have nothing to do with seeing.

Alarm. Same hand to the bedside. Same light. You do not slap the hand. You watch it with the new eye you have earned from pellets and pauses and holed paper. The hand lights because the tug woke, not because the day needs a friend. You note that and go on with the book. No Day One is declared. No house is briefed. No ink is wet.

Kettle. Same kitchen. The calendar is still there. The pen is still in the pot. Your eyes land on the square and the old reflex starts — shall I write it, shall I set it, shall I tell them — and you catch the reflex by its true name. That reflex belongs to the old orders. It assumes the only way to stop is to pick a suffering date and hold. This book has not asked you for a suffering date. It has asked you to keep looking until wanting thins, then to smoke a last ordinary tube with attention and stub it because there is nothing left to want.

Put the pen down. Not as a brave act. As an irrelevant act. There is nothing to write yet. The square stays empty and the empty does not accuse. You make tea. You drink it standing. You go to work. The foil stays in the drawer unopened, not mourned, not eyed, simply unneeded for today's seeing.

Mid-morning the old thought arrives on schedule: you ought to be holding by now, you are falling behind, other men are on Day Four. Answer it from your own drawer, not from me. Behind of what. The holding race was the method that failed twenty times. Falling behind a failing race is not failure. It is sense. Would you run to catch a bus you have seen is going the wrong way.

Lunch. The mate says, are you still on the patches. Under old fear you would flush, explain, promise to do better tomorrow. Under seeing you tell the plain truth without apology: I am reading and looking, the drawer is shut, I am not holding. He shrugs. The conversation moves to football. No shame heat climbs the neck because no war was declared and lost. The day did not ask for war.

Evening. The packet level drops as it always drops. The hand reaches as it always reaches. You do not count this as proof you are weak. You count it as the cycle running while belief thins underneath it. Each light now is watched, not worshipped. You notice the papery turn, the quick muting, the return within the hour. You notice without strain because noticing is not holding. The noticing itself is the work this week, and noticing costs the jaw nothing.

Tuesday comes without a cross to defend. That is the point you must live, not merely agree with. Under the old orders every date was a courtroom. The square accused in the morning, the evening gave the verdict, guilty or holding. Under seeing-first orders there is no courtroom yet. There is a classroom. The calendar is paper. The pen is plastic. The drawer is wood and foil. None of them can sentence you. Only a kept belief could sentence you, and the belief is what we are dissolving page by page.

Ask from that Tuesday, not from theory.

When you did not draw the cross, did the day collapse. Did work go undone because no foil was stuck to the arm. Did the night grow longer because no gum burned the cheek. Or did the day run much as days run, with lights in their usual places, but with one new thing inside it: a man watching his own hand without cursing it, and finding the watching steadier than the cursing ever was.

You know, because you have already lived fragments of such days while reading this far. The pellet examined without being mourned. The pause stood in without being taxed. The mild held to the light and seen as theatre. None of those seeings required a cross. All of them happened with smoke still in the picture. That is how you know the feared try is not what is asked. What is asked leaves the cross off until seeing is complete, then asks for one last tube, not one long hold.

There will be a voice that calls this delay cowardice. "You are putting it off. You said Monday and now you smoke on Monday. You will never do it." Ventriloquize it fully so it cannot whisper. It sounds like conscience. It is the method talking.

Answer it with the drawer open in memory. Putting off holding is not putting off seeing. You put off twenty holds and each hold put off seeing by teaching that quitting equals suffering. This time you put off holding in order to finish seeing. Which delay kept you chained longer. The delay that stared at foil, or the delay that stared at belief.

And there will be a second voice, softer, that says: but I feel calmer knowing a prop is in the drawer if things get bad. Just knowing it is there helps. Let me keep it as insurance. Hear what insurance means here. It means: I believe there will be bad hours that only a top can soften. That belief is the Smokescreen speaking in a helpful tone. A prop kept for bad hours keeps bad hours coming, because the brain, assured of a future top, keeps the seat warm for it. Shut the drawer on insurance as well as on plan. Not with a slam. With indifference. The drawer is not your enemy to fight. It is your old toolbox for a job you no longer do that way.

Walk the rest of that week in picture so fear has nowhere left to lodge.

Wednesday. Shopping list on the fridge. Milk, bread, tea. Under old orders the list would have carried a secret second list: patches if chemist open, mints to hide, spray for car. The eyes would have scanned shelves for props while the hand pushed the trolley. Now the trolley holds food. The chemist aisle passes without a stop. Not because you forbade the stop with a set jaw, but because the stop has no job in a week of looking. The money stays for food. The bag stays light of foil.

Thursday. Phone call from mother, long, circling, the old trigger for two quick lights on the step. Under old orders this call would have been proof the date was wrong: I cannot hold when she rings, I will restart Monday. Under seeing the call is only a call. You step out because cold air steadies, you light because the cycle still runs, you listen and answer and come back in. No restart is needed because no start was declared. The call did not break a vow. It gave another watched light to add to the pile of evidence that lights mute and return, mute and return.

Friday. Pub. The bragger holds court, the whinger nurses his story. Under old fear their voices would decide your square: if he suffered three months, what will happen to me. Now you hear them as advertisements for orders you no longer take. You drink what you drink. You step out when you step out. You come back in when the air has done its work. No one counts your exits. You do not count them to prove holding. The night ends without a verdict.

That week without verdict is the new lived consequence fear said was impossible. Fear said: without a cross you will drift forever. Lived days answer: without a cross you looked longer and steadier than in any crossed week, because attention was not hired out to holding. Fear said: the drawer must be opened or you are not serious. Lived days answer: the drawer stayed shut all week without a single act of forbidding, and seriousness lived in watching, not in foil.

Hold that distinction until it holds you. Old try equals want kept plus strain applied plus glass swapped. Seeing-first equals want examined plus credit moved back plus no glass needed. The two share no muscle. Training for one does not train for the other. Dreading one is no reason to dread the other.

So when the pen hovers over next Monday, let it hover and then set it down. Tell yourself the plain sentence that ends the dread without borrowing torture-ahead: I am not asked to hold from Monday. I am asked to finish seeing, then to stub one last tube because seeing is finished. The drawer can stay shut while I finish. That sentence has no suffering in it to fear. It has only pages left and eyes open.

Live it that way and the calendar changes its office. It ceases to be a courtroom wall of crosses and failures. It becomes what it is for men who never smoked: paper with squares where shopping and birthdays live, not where worth is tried. Your worth was never on trial. Only orders were, and orders can be changed without a cross.

6. DISREGARD ANYONE WHO QUIT BY WILLPOWER
Their struggle was the method, not you.

**SUMMARY**
- The drawer of foils and gums and crossed-out dates proves the method was wrong, not that you are weak or missing backbone.
- Many houses hold the same drawer, so repeated failure marks a common con, not a private defect.
- A different glass holds the same drink and keeps the same lesson alive, that outside tops are needed to face ordinary hours.
- Strain keeps want alive by mourning a loss every day, so holding on longer never reaches a finish.
- The bragger and the whinger advertise the pain of the method, not the truth about quitting.
- Clinic counts and street counts answer different questions in different rooms and neither decides what clear seeing does for one reader.
- Next Monday needs no cross and no foil, only eyes kept open until seeing is finished.
```
