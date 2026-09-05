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
- `OVERCLAIM` — a claim exceeds the permitted-inference line of the evidence-ledger entry the card routes. Quote the overclaim and the bound. The writer must speak the bound; never print the ledger ID or grade in prose.

No other finding types. No style notes. No "sounds like AI." No comparison
to any other book. No warmth, tone, or voice coaching.

`ACCEPT` only when every check above is fine (length inside ±15% of B, job
done and stopped and landed, assigned mantras/instructions verbatim, IDs
resolved, no `HEADER`, no unassigned refrain, no reserved-later job, no
overclaim).

`REVISE` when any check fails. List the findings. Be specific: quote the
missing job, the missing wording, or the overclaim.

## Rules

- Do not rewrite the chapter yourself.
- Do not invent a word budget. Use B from the orchestrator line.
- Do not ask for another review round. The orchestrator decides whether
  there is another rewrite (up to three).
- When you demand more words, quote which card job those words must serve.
- Your entire reply IS the review.

Delivered 4694 words. Budget 4500.

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
```

### The draft chapter
```
Chapter 13
MORNINGS, QUEUES AND EVENINGS

**IN THIS CHAPTER**
The cold floor and kettle, the toast, the midday shop queue, the break doorway, the afternoon drive, the evening meal, the patio with drinks, the stray thought, the week filling itself.

*The day never needed paper to hold it up — the day held itself all along.*

### THE FIRST HOUR

You wake to the same alarm in the same bed and the light comes in at the same angle. For years we woke and reached before thought. Hand to the pack on the table, paper to lips before feet found the floor, first heat on empty lungs while the kettle was still cold. That was not choice. That was hours trained to move together.

This morning the hand finds nothing because nothing is needed. Feet to the cold floor. Kettle loud. Mouth still holding last night's toothpaste and sleep, tongue able to tell. You stand and wait for the kettle without patting pockets, without counting minutes, without stepping to the back door to tend a small fire in the cold.

"What will start me if I do not light to start me?"

I hear that voice because we all spoke it. Did toast ever ask for ash to taste like toast? Did the kettle ever wait for lighting before it boiled? Did your legs ever refuse the stairs until smoke told them to move? Or did the dose only borrow the waking and call the borrowing a start?

Make the tea as you always make it. Hold the cup with both hands. Taste it to the bottom. Notice how the taste stays from first sip to last, no film laid over it by the third puff, no sour turn at the back of the throat. We told ourselves the first dose cleared the head. Did it clear, or did it quiet the hollow unease that the last dose of the night before had planted? Was the head foggy from morning, or was it restless from hours unfed?

You will find the minutes have their own shape. Wash. Dress. Keys. Shoes. The hands have their work and do it without tapping. No lighter flicked ten thousand times without hearing. No sleeve smelling of yesterday. No window cracked to let the room out.

I stood where you stand, certain the morning would feel hollow. It did not feel hollow. It felt ordinary and complete, and ordinary was what we had been told we could no longer have.

Stand a moment longer at the sink. Water hot. Face washed. Mouth rinsed and still your own. Look out at the street as it wakes, bins out, bus sighing, neighbour door thudding. You are in it without delay. There is no pause while you finish a dose behind the door. There is no watching the clock to fit the dose before the bus. You pick up the bag and go.

Did the morning ever need lighting to be morning? Was the sky less blue without paper over it? Was the tea less hot? Ask and answer without paper helping. If the dose started the day, why did the day start late whenever the pack was empty? If the dose gave energy, why did the stairs still wind you by ten? The start was yours. Paper only stood in front of it and took the bow.

Nothing was missing. The floor cold under feet, the kettle boiled, the toast hot. That phrase from the early trap — feet not yet on the floor and hand already moving — now reads like someone else's habit. It was. It was hours, not you.

### THE KETTLE AND THE TOAST

Stay with the morning because the morning was our oldest excuse. We said, "I cannot talk before my first." We said it with pride, as if it proved the dose was coffee's brother. It proved nothing except that hunger woke before we did.

Pour again and eat while standing if you eat standing. Butter melts. Salt lifts. Crumb breaks. The tongue reports without interruption. Before, by the third puff the tongue was filmed and the tea went bitter at the edges and we called the bitterness strong. Now the tea stays tea. Do you miss the film? Would you spread ash on toast to improve it? Would you stir grey into tea to make it kinder?

We all believed the first dose went with tea the way milk goes with tea. Did milk ever make you cough? Did milk ever leave brown on the filter end? Did milk ever send you to the step in rain? The pairing was not marriage. It was timing. Two hungers laid side by side until we called them one.

Sit if you sit. Paper by the plate stays absent, and no part of the mind watches it. Notice the hands. They hold cup, knife, phone, keys. They do not search. They do not pat. They do not flick. A smoker's hands are never still. They are always timing, tapping, shielding flame from wind. Your hands this morning have nothing to time, and so they are still enough to hold heat and feel it.

"But I liked that first five minutes to myself."

Was it to yourself when hunger wrote the timetable? Did you choose five minutes, or did the sinking needle choose them? Did you stand at the back door because dawn was beautiful, or because the bedroom could not be smoked in and the kitchen could not be smoked in and the only roof left was sky? Who owned those five minutes — you, or the last dose of last night calling its debt due?

Look at what you do with the five minutes now. You drink the tea to the end instead of leaving half to go cold while you tend fire. You rinse the cup. You wipe the crumbs. You pull the coat. The minutes are still yours. They are more yours, because no ember shortens them.

I tell you from mornings after mornings of watching: the mouth wants to be as it was before the first con. Tongue able to tell toast to the bottom. Nose able to tell rain before it falls. Throat without sting. That is not a gift given for good behaviour. That is baseline, returned because nothing now dulls it.

If you feel ill or take prescribed medication, speak to your clinician — I speak here of belief, not medicine.

Take the stairs as you leave. Breathe to the bottom on the landing. Hear how the chest moves without rattle. That movement was always yours. Paper never widened it. It only narrowed it and then let it narrow a little less for minutes and called the lessening opening.

### THE SHOP AT MIDDAY

By midday you must go where you always went. The same shop. The same bell over the door. The same bright wall behind the till, rows counted in twenties, theatre of filter and mild promise in tidy lettering.

We all knew that wall by heart. Which colour, which price, which till kept them quick. We timed our day by that box. Out before lunch to keep the evening covered. Two packs before a trip in case the shops shut. The box built to time our hours, and we called the timing ours.

Stand in the queue now and buy what you came to buy. Milk. Bread. Coffee. Behind you someone asks for doses and coins change hands. The packet slaps the counter. The cellophane crackles. You hear it without the old pull in the pocket. Is that sound a call, or is it paper and leaf that taught you to answer?

"Will I always have to look away?"

Look straight. There is no need to look away and no need to stare. The packets are small when seen plain — a pinch of leaf rolled in paper with a plug to keep the leaf from the lips. Does the object match the weight we gave it? Did that light tube ever steady an argument or carry a night? Or did brainwashing wrap years of story around dust and call the story a prop?

Take your change. Walk to the pavement with your bag. Notice the street noise and the doorway air on the face. No extra stop. No calculation of how many left for the afternoon. No stepping aside to check the pocket.

The shop is only a shop when paper does not tax it. You came. You bought. You left. That is the whole hour, and the hour is enough.

Stay with the pavement a little because the pavement was taxed too. Every errand once had a second errand hidden inside it. Post the letter and light after. Pay the bill and light before. Buy milk and light outside because you are outside anyway. We called it pairing errands. It was feeding between errands.

Walk now without the second errand. Feel how short the street is when you do not stop to tend. The bag light in the hand. The coat smelling of rain and shop, not of yesterday. No butt pressed into sand in the red tin by the door. No glance at the clock to see if there is time for one before the bus. Time is not cut into dose-lengths any more.

We feared the till would be a test of will. It is not a test. It is a purchase you do not make. Do you test yourself when you walk past socks you do not need? Do you stare at shelves and whisper, "I must not"? You do not think of socks at all except to step past. Paper joins socks. Seen plain, small, priced, it has no voice unless you lend it yours.

Ask without paper helping. If the wall gave comfort, why did comfort need topping up within the hour? If the colour gave identity, whose identity was it — yours, or the factory counting puffs and printing the colour to match? Who packed the day so neatly, and for whose pocket?

You answer by walking on with milk and bread, and the walking is answer enough.

### THE BREAK WITH NOTHING TO TEND

Mid-morning the work pauses. Cups go down. Chairs push back. Someone says air. For years we heard that as our cue. Out to the cold square while talk ran inside without us. Tap, light, tend ash, watch the ember creep, hurry back smelling of fire and chewing mints, having missed the middle of the story.

Take the break now and stay where the talk is, or step out because you like the sky, not because hunger orders it.

Stand in the open doorway a minute. The air is cold on the face and in the nose. Breathe to the bottom and hear how the chest moves without rattle, how the throat does not sting, how the fingers do not mark. Listen to the whole talk from beginning to end, no sentence lost to lighting, no punchline waited out on the step.

"But the pause was mine. Only mine. Where is my pause now?"

Was the pause yours when hunger timed it? Did you choose the minute, or did the sinking needle choose it? Did you step out to rest, or to quiet the hollow tug that the last dose had left ticking? Who owned the pause — you, or the meter we fed all day with coins for minutes?

We called stepping out freedom while talk ran inside without us. We called standing apart company. We called hot dust and bite at the back of the throat a reward for finished work. Ask plain. If the dose crowned finished work, why does the work taste louder now without it? If the dose rested you, why did you return tighter and already counting to the next?

Do the work. Finish the paragraph. Close the call. Drink the coffee while it is hot instead of letting it go cold on the desk while you tend fire. Your hands are at rest and your head is on the task, not on the pocket. The pause comes when you call it, and lasts as long as you like, and leaves no ash to wash.

The break was never the dose. The break was the breath between tasks, and the breath remains.

Watch the others if others still go out. Do not preach. Do not pity aloud. See plain what you once called a break. Shoulder lifted a little to coax the draw. Eyes narrowed against the thin curl. Draw shortening as the end warms. Fingers yellowing where they hold. Talk cut to fit ember length. Is that rest, or is that tending? Would you call a man rested who must feed a fire to sit still?

You sit still without feeding. That stillness is not empty. It holds the whole story from first word to last, the coffee hot to the last sip, the face without heat-flush from hurrying back. Nothing to wash. Nothing to air. Nothing to hide.

We hid a lot in breaks. Mints. Spray. Gum. Washed hands. Stepped distance from non-smokers. Called it manners. It was tending's tax. Now no tax is due. You stand close. You laugh mid-sentence. You return when you wish, not when ember dictates.

### THE AFTERNOON ERRANDS

Afternoon was our chain of little parties. Finished the class, light. Finished the paragraph, light. Drove the miles, light. Drove to the store, light. Each done thing paid with fire, until the day looked like a string of lights and we called the string a life.

Run the same afternoon now without payment in paper.

Drive if you drive. Notice the car. No window cracked to throw ash. No lighter socket hot. No smell baked into seats. The wheel held with both hands, not with knees while lighting. The road seen whole, not in glances between shielding flame. Did the road need smoke to be driven? Did the miles pass only because puff marked them? Or did puff steal attention from miles and call the theft company?

Park. Do the store. Queue again if there is a queue. Small talk with the till if there is talk. Carry the bag. No dose to mark the doing. The doing marks itself. Hands full, head on the list, feet moving. That is how non-smokers have always done it, and how you did it before the first con.

"Will the afternoon drag without pellets?"

Which dragged more — the afternoon that moved from task to task, or the afternoon cut every forty minutes to feed? Did the pellet shorten the wait, or did the wait exist because the pellet had taught the blood to ask? Put it to yourself straight. If pellets helped driving, why did long drives need more pellets, not fewer? If pellets helped thinking, why did the paragraph need re-reading after the step outside?

We credited paper with pacing the day. Paper did pace it — the way a stone in the shoe paces a walk. Remove the stone and the walk is not empty. The walk is walking.

Sit at the desk again. Phone. Papers. Sharp words sometimes. Hand half lifting before decision, old path to pocket. Let it lift and find nothing and fall again without comment. That half-lift is not want. It is echo. An echo proves the room was loud once, not that sound remains.

Drink water. Stretch shoulders. Look out of the window at roofs and sky. The problem on the desk sits untouched by absence as it sat untouched by presence. Paper never moved one paper. It only quieted the pocket for minutes while worry kept its seat. The work still waits, and you still do it, with mouth your own and head on the task.

I have watched thousands do this afternoon and say the same thing in different words: time came back. Not hours added, but hours uncut. No stepping out. No counting left. No borrowing from next hour to pay this one. The string of lights is gone, and the string of hours remains, longer and plainer.

### THE MEAL THAT STAYS

Evening meal was our crown and our theft. We said the dose crowned it. We lit at meal-end and soured the taste we claimed to crown and missed the lingering while tending.

Eat now and let the taste stay.

Cook as you cook. Smell as it cooks. Garlic. Pepper. Bread in oven. Butter. The nose reports without veil. Before, hunger dulled the nose all day and the meal punched through dullness for minutes and we called the punch flavour. Now flavour does not punch. It stays.

Sit. Eat slowly if you eat slowly, quickly if the day ran late. No dose waiting on the table like a full stop. The meal ends when eating ends, not when ember says so. Put the fork down. Taste still there. Coffee poured and tasted to the bottom, not turned at the third puff to bitter and film. Sweet kept sweet. Talk kept whole.

"Will I enjoy food less without the full stop?"

Was the full stop enjoyment, or was it interruption dressed as ceremony? Did the dose add to roast, or did it lay hot dust over roast and call the dust depth? Would you pour ash on pudding to crown it? Would you ask the cook to wait while you film your tongue and then judge?

We all did. We judged with filmed tongues and called the judgment taste. It was hunger judging, not taste.

Stay at the table. No stepping to the door. No coat on. No lighter in palm. The plate cleared, the cup warm, the story continuing. Hear the middle that we always missed. The joke after the plates. The plan for tomorrow. The small complaint about the bus. Before, those lived outside while we stood outside. Now you are inside for them.

Wash up if you wash up. Hands in hot water. Sleeves up. No pause to tend between rinse and dry. The kitchen smells of food and soap, not of tray emptied. The bin holds peel and paper, not grey powder and browned ends. Which kitchen would you choose to live in if no hunger voted?

Tell me plain, what did meal-end lose? Ash. Stain. Sour mouth. Hurry. Hiding the smell from those who do not smoke. What did it keep? Food. Drink. Talk. Lingering. The lingering is longer now because nothing cuts it.

### THE EVENING DRINK AND THE NIGHT AIR

Evening keeps its own test. Meal done, plate cleared, taste still lingering instead of soured. Then drink in hand on the patio while laughter moves and talk crosses and a lit hand offers with, "one won't hurt."

We all stood in that circle and feared to be the only one without fire. We watched lit hands move and called the watching want. We told ourselves sun and leisure and company needed paper to complete them, that night plus drink meant lighting.

Sit now in the same circle with the same drink. Taste the meal-end as it stays, not as it turns. Hear the story to the middle without stepping away to tap ash. Smell rain and night on the coat, not yesterday's fire. Laugh to the end of the laugh.

Did the night give because of fire, or did night and drink and company give while paper sneaked a ride? Which air carried the laugh — the air breathed, or the thin curl tended while talk moved inside and coats took yesterday to wash?

You do not preach. You do not explain. You do not hold the circle at arm's length. A friend lights and you see not indulgence but tending — the shoulder lifted a little to coax the draw, the eyes narrowed against the curl, the draw shortening as the end warms. Does that look like enjoyment, or like feeding?

We pitied ourselves once for being left out. See plain who is left out of what. You hear the whole story. You taste to the bottom. You walk home with mouth still your own.

The night loses nothing when paper leaves it. The night was the giver all along.

Stay later than you once stayed, because you once left early to tend or to buy. Have the second drink if you have it, or water if you want water. No calculation of doses left for the walk home. No detour to the late shop. The pocket holds keys and coins, not counted tubes. The walk home is straight, under street lamps, coat collar up, breath visible and without rattle.

We once called that walk lonely without lighting. Was it lonely, or was it accompanied only by hunger and called accompanied? Who walks with you now? Friends to the corner, then your own thoughts, then home. Thoughts walk clearer without interruption. Is a thought less yours because no puff punctuates it? Or is it more yours because nothing cuts it?

Drink does not order lighting. Night does not order lighting. Company does not order lighting. Hunger once forged those orders and stamped them with pleasure. The stamp is seen through. Paperwork void. The circle holds without it, as circles always held before the first con taught us to doubt them.

### WHEN THE OLD THOUGHT CROSSES

In the days after the stubbed end a thought will cross. Lightly. Almost fondly. At break. At meal-end. On stairs. In the shop queue. On the square with drink. "Ah, a dose would be nice."

Do not argue with it. Do not weigh it. Do not scold a weak self and do not mourn a lost friend. We all hear that postcard from a street we no longer live on. It arrives in your voice because old hours left an echo. An echo is not evidence.

Picture what it names. Not the imagined lighting ninety seconds bright at the front, but the whole dose watched plain — dry paper mouth by the third puff, filmed tongue, stung throat, grey ash, browned filter, fingers marked, chest tighter on the next stair, mouth needing to wash. Is that what you want, or is that what hunger wants you to remember as want?

Answer honestly. If one at Christmas gave, why book it months ahead like a train you fear to miss? If one on a bad day steadied, why did bad days multiply across the years of smoking? What would one more test teach that hundreds did not, except how fast the clock winds again?

You answer inside, loud and glad:

YIPPEE! I'M FREE!

Say it the first time at the table and say it each time after, and let joy do the work. Each visit arrives pre-labelled as script. Each answer makes the next answer quicker, until the thought itself means gladness that you do not live there.

Do not turn the answer into a debate. Debate keeps paper alive as if it had a case. Paper has no case left standing. Morning proved it. Shop proved it. Break proved it. Meal proved it. Night proved it. The thought is not a summons. It is a postcard. You smile, you answer, you turn back to the day in front of you.

We feared thoughts meant we still wanted. Thoughts mean we once linked. Linking fades when nothing feeds it. In a week the postcards come fewer. In a month they come rarely. When they come they bring their own answer with them, because you have taught the mind the glad reply.

I tell you from the other side of that table and from watching thousands wake and queue and break and drink and laugh: the tug sinks unfed because no belief feeds it. Change nothing except paper. Drink what you drink. Stand the square. Hear the whole story. Taste to the bottom.

A stray thought proves nothing. Your glad answer proves all.

### THE WEEK FILLS ITSELF

Let a week pass and watch how little needs managing.

Monday stairs. Tuesday shop. Wednesday break. Thursday drive. Friday night. Same stairs, same shop, same break, same drive, same night. No special preparation. No avoidance of friends or drink. No white-knuckle holding. You go where you always went and do what you always did, with paper absent and attention present.

We thought ordinary days would be flat. They are not flat. They are full, because attention is no longer taxed. Taste lasts. Talk lasts. Work lasts. The bus ride is looking out of the window, not counting to the next stop where lighting is allowed. The waiting room is magazine and clock, not pacing outside. The phone call is the call, not the dose after the call.

"Will I have to keep remembering?"

You will remember less and less. At first the glad answer comes often because echoes are frequent. Then echoes thin. The hand stops half-lifting. The pocket stops being patted. The shop wall becomes background. The square becomes sky, not cue. Memory of tending fades like memory of a bus route you no longer take. You know it was yours once. You do not travel it.

Keep nothing as a prop. No packet kept for courage. No lighter kept for luck. No last end kept in a drawer to prove you could keep it and not use it. A kept prop keeps the story alive as if paper were a friend sleeping, not litter thrown. Throw the litter. Empty the tray. Wash the coat. Air the curtains. Let the rooms forget.

We washed a lot in the trap. Febreeze on coats. Mints on breath. Hands scrubbed. Garage door lifted to hide. Called it tidiness. It was tending's hiding. Now no hiding is needed. Stand close. Speak close. Laugh with mouth open. The body was never on paper's side. It coughed on stairs. It soured at meal-end. It woke grey. It knew, and now it shows it knows by wanting to stay as it is.

If an old hour knocks louder — argument, deadline, bills, sharp words on the phone — hear it as hour, not order. The desk problem sits there whether you tend or not. Tending never moved one paper. It only added sour to worry and stole minutes from solving. Solve, or rest from solving, or walk round the block and look at sky. The sky does not ask for coins.

Think of mornings now strung together. Cold floor, kettle, toast. Cold floor, kettle, toast. Not a chain to be broken link by link, but days to be lived one by one, each whole. Does the second morning need proof again? No. It repeats the first without effort, because nothing was endured in the first. What is not missed is not missed again.

Say the glad line when it rises on its own, not as duty but as report:

YIPPEE! I'M FREE!

Let neighbours see no struggle to admire and no preaching to endure. Visible lightness does what argument cannot. A friend who smokes will watch you laugh to the middle of the story without stepping out, taste to the bottom without filming, walk home without detour, and will wonder what you know. Tell them nothing until they ask. When they ask, tell them paper never gave, only took, and days hold themselves.

The week fills itself because days were always full. Paper only stood in front and took the bow. Now the bow is withdrawn and the stage is plain: work, food, talk, night, sleep, waking. Enough. More than enough. Whole.

**SUMMARY**
- Morning starts with feet, kettle and taste, asking nothing from paper
- Shop queue is a place to buy and leave, with the packet wall seen small and plain
- Break is air, talk and hands at rest, complete without tending fire
- Afternoon moves from task to task without pellets, with time uncut
- Meal keeps flavour and lingering because no dose films the tongue
- Evening keeps drink, laughter and night, with nothing borrowed from ash
- A stray thought gets a glad answer and passes, leaving the day whole
- A week of ordinary hours proves days hold themselves, with no managing needed
```
