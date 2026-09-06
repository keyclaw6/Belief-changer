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

Delivered 4650 words. Budget 4500.

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
```

### The draft chapter
```
Chapter 7
THE ITCH IT PRETENDS TO SCRATCH

*You were never lifted above normal — you were dropped below it, then put briefly back.*

### THE METER YOU FEED ALL DAY

Leave the drawer shut. We stay with the hands as they are today, still lighting, and we watch one ordinary day the way you would watch a warden on her round.

Morning. Feet have not found the floor before the hand finds the pack. First dose on empty lungs. Shoulders drop. Head clears a little. You call it waking up.

Second dose with coffee. Third on the way to work. Fourth after the sharp email. Fifth because the bus is late. Sixth because the bus came. By noon you have fed it six times and thought nothing of it. By night you will have fed it twenty times and called each feeding something different — break, reward, calm, company, pause, think.

I have lived that count. I once lit without remembering lighting, found a fresh dose burning in the tray while another burned between my fingers. We all did that. That is not choice. That is feeding.

See it as it is. A dose arrives in the lungs and the nicotine runs to the brain within seconds, and for minutes the edginess quiets. Then the quiet fades. The acute effect wears off quickly, so the mind calls for another to keep the feeling up and to hold the edginess down. That is the whole day: lift, fade, feed. Lift, fade, feed.

Picture a parking meter on a grey street. You drop in a coin. The needle jumps. You walk away feeling paid up. Ten minutes later you look back and the needle is falling. Twenty minutes and the red shows again. You hurry back with another coin, and another, all day. The meter never stays full. It was built not to stay full.

Your day is that street. Each dose drops a coin. The needle jumps toward normal and you read the jump as pleasure. Then within minutes the needle sinks and the hand moves for another coin. No coin ever buys the street. It only rents the needle for a little while.

Ask yourself, and answer plainly:

If each dose truly lifted you, why did the lift never last the morning?
If each dose truly fixed anything, why did the same hunger return before the ash had cooled?

You know the answer because you watched it today. The hunger returned because the dose guarantees its return. That is how the nicotine trap keeps time — not by giving, but by taking and renting back.

If you live with a medical condition or take prescribed medicine, speak to your own clinician for your own care — I say it once, so we can look clearly.

We called the meter by twenty names to avoid seeing it was one meter. Morning dose we called waking the lungs. Coffee dose we called clearing the head. Walk dose we called stretching the legs. Email dose we called steadying the nerves. Late-bus dose we called killing time. Bus-came dose we called settling in. Night dose we called rounding off. Twenty names for one act. The hand did the same thing each time. The mouth did the same thing. The lungs took the same smoke. The brain took the same chemical in the same seconds. Only the story changed.

Watch the sameness underneath the stories. At seven the kitchen is cold and the kettle has not boiled and you stand in a shirt with the door cracked and the first smoke bites. At ten the office is warm and the screen glows and the smoke sits beside the mug. At one the cafe clatters and the smoke mixes with frying. At six the car park is damp and the smoke mixes with rain. Different rooms. Same lift. Same fade. Same reach. If the dose truly belonged to coffee, why did it belong to rain? If it truly belonged to waking, why did it belong to midnight? A thing that is needed for everything is needed for nothing. It is only the meter asking for coins wherever you happen to stand.

I stood where you stand. I told myself the morning one woke me, the mid-morning one helped me think, the after-lunch one closed the meal, the afternoon one broke the drag, the evening one marked the end of work, the late one helped me unwind. Six friends. Then I watched a day when coffee never came, lunch never came, work never came — a Sunday of rain with no appointments — and the six friends came anyway, at the same hours, with the same tug between. No coffee to close. No work to break. Only the interval. Only the fall of the needle and the hand moving. That Sunday taught me what no lecture could: the stories were clothes hung on the same peg.

Count your own Sunday. Pick the day with least reason. Flu day in bed. Long train with no stop. Day of waiting in a corridor. The doses still came. The hand still searched the pocket. The mind still said now. What coffee did that dose close? What stress did that dose carry? None. The interval had elapsed. The previous coin had worn thin. The tug had woken. The story arrived a second later to dress it decently.

That is the order every time. First the tug wakes. Then the mind looks round for a reason that sounds human. Bus late will do. Bus come will do. Good news will do. Bad news will do. Silence will do. Noise will do. The mind is a quick tailor. It can cut a reason from any cloth in half a second. We mistook the tailoring for truth because we never watched the order. Watch the order once and you cannot mistake it again.

### FIFTY MINUTES WITH NOTHING CHANGED

Stay inside one interval now. Not the whole day. One gap between two consecutive doses, watched minute by minute, while the outer world does not move.

Take the fifth because the bus is late. Sixth because the bus came. By noon you have fed it six times and thought nothing of it. Let us think something of it. Let us stay at that stop and refuse to look away.

It is 8:47. Cold bites the ears. Timetable board says 8:38 delayed. Three other people stamp feet. A pigeon walks the shelter edge. Your phone shows no new message. You light the fifth. Draw. The smoke hits fast. Within seconds the nicotine is up and the edginess quiets. Shoulders drop an inch. Jaw unclenches. You think, good, I can wait now. The pigeon, the board, the cold — all a shade more bearable.

Nothing outside has changed. The board still says delayed. The cold still bites. The phone still shows nothing. Only the inside has shifted toward normal for a little while.

It is 8:50. Three minutes since lighting. The dose is stubbed. You stand a little easier. You check the board though you know it. You pull the coat closer. Talk comes easily to the man beside you about the late bus. You think the dose helped you cope with waiting.

It is 8:53. Six minutes. The talk thins. You look down the road though no bus shows. Attention will not quite settle. A faint hollowness moves under the ribs. Hands want an errand. You shift weight. You blame the cold.

Nothing outside has changed. Same board. Same road empty. Same three people. Same phone dark. Only the inside has slipped a notch.

It is 8:56. Nine minutes. The hollowness sharpens a fraction. You glance at the pack without deciding to glance. You tell yourself you only check the time. The pigeon annoys you now. The man’s voice annoys you faintly. You re-read the same headline twice. You call it impatience with the bus.

Ask, and answer honestly: what bus? The bus was late at 8:47 when you felt patient. The bus is late at 8:56 when you feel edged. Same bus. Same lateness. Same cold. The only thing that moved is the coin wearing thin.

It is 8:59. Twelve minutes. The tug is unmistakable now, though still small. Empty. Fidgety. Slightly edgy attention that will not rest on the headline or the road. Fingers tap the pocket. You do not yet say you want a dose. You say the wait is getting to you. You say you need to do something with your hands.

It is 9:03. Sixteen minutes. You are watching the bend in the road harder than the bend deserves. Every car that is not a bus irritates. You rehearse what you will say at work about being late though no one will ask. The mind hunts for a story because the tug has no story of its own. It only says, feed me soon.

It is 9:07. Twenty minutes. The bus still has not come. You light the sixth because the bus came? No. The bus has not come. You light because the interval has run out. The hand finds the pack before thought finishes. Draw. Within seconds the quiet returns. Shoulders drop. The bend in the road looks ordinary again. You think, that helped me wait.

Did it help you wait? The wait is the same wait. The road is the same road. The board still says delayed. The only wait that was helped was the wait the previous dose created — the wait between coins while the needle fell.

Stay with that sameness until it stings. At 8:47 the world was bearable for minutes after the coin. At 8:56 the same world was unbearable though nothing in the world had moved. At 9:07 the same world is bearable again for minutes after the next coin. Three readings of one world. The world did not change three times. The coin changed. Up, down, up. The mind credited the up to the dose and blamed the down on the bus, the cold, the morning, the character of the day. It never blamed the down on the up that came before it.

That is the half we had not yet seen. We had seen that each dose only puts you briefly back toward where a non-smoker lives all day without coins. We had not yet seen that the brief putting-back is itself the maker of the next fall. The coin does not only rent the needle. It wears the needle. As the chemical clears in minutes, the body notes the absence and complains in its small voice. That complaint is the next tug. No coin, no complaint. Coin, then complaint when the coin fades. Every lift lays the track for the next dip. Every quiet plants the next noise.

Think of the meter again, but closer. You drop a coin at 8:47 and the flag lifts. The mechanism that lifts the flag is the same mechanism that lets it fall. The spring cannot hold. By design it unwinds. You do not pay for parking and then pay again because parking is pleasant. You pay again because the first payment expires. The expiry is not an accident of the street. It is the product sold. A parking company that sold a day for a penny would sell once. A company that sells ten minutes for a pound sells all day. The short life of the quiet is not a flaw in the dose. It is the business of the dose.

Your body clears the chemical fast. The acute effect dissipates quickly. That fast clearing is why the hand moves twenty times. If the effect lasted, the hand would move once. The brevity drives the repetition. The repetition is then read as proof of value — I do it so often, it must do so much — when the repetition is proof of expiry.

Ask the interval itself:

If the fifth truly settled you, why did the same stop unsettle you nine minutes later with nothing changed but minutes?
If the sixth truly gave patience, why did patience arrive only after impatience that arrived only after the fifth faded?
Who would call a coat good that warms for ten minutes and then makes you colder than before you put it on, all day, every day?

You know the honest answers. The fifth did not fail because the bus was very late. It faded because fading is what it does. The sixth did not succeed because the bus at last came. It quieted for minutes what the fifth’s fading had woken. The bus is innocent. The cold is innocent. The morning is innocent. The interval is guilty, and the interval is the product.

Watch one more turn of the same screw, because this is where the trap locks. At 9:07 after the sixth, you feel almost normal. Almost like the man beside you who never smoked and has waited the same twenty minutes reading the same board without once checking his pocket. For minutes you share his state — at a cost of a coin. Then yours begins to fall and his does not. By 9:20 you will be edgy and he will still be reading. By 9:30 you will be hunting reasons and he will still be waiting. You paid to visit his normal for ten minutes, and the visit itself ensured you would leave it. He stays where he is for nothing. You leave where you visited because visiting is leaving in advance.

That leaving in advance is the guarantee. Not a risk. Not a maybe. While the outer situation sits still — same shelter, same board, same road — the inner needle moves on its own clock: up in seconds, down in minutes, tug by the quarter hour. Typical. Not identical to the second for every body. Some feel the slide at seven minutes, some at twenty. The shape holds. Up fast, down fast, call for another. The brief return carries its own ending inside it like a coin carries its own wearing thin.

We wore tight shoes all day for the pleasure of loosening them every hour. We drank salt water all day for the pleasure of wetting the mouth for a minute. We paid the meter all day for the pleasure of seeing the flag up for minutes. Each pleasure was real as a feeling and false as a gift. Felt, yes. Given, no. Rented, then removed, then rented again.

### AN EMPTY, SLIGHTLY RESTLESS TUG, NOT A NEED

“But I feel it in my body,” you say. “A gnaw. A fidget. Surely that proves I need it, that stopping will be agony for weeks.”

I welcome that doubt, because your body is telling the truth and the Smokescreen is mistranslating it.

What you feel in the gap is small. What you feel is an empty, slightly restless, slightly edgy little tug. Hollow under the ribs. Attention that will not settle. Hands that want an errand. That is all.

That tug is the Nipper. A trivial physical creature, already dying when unfed. It complains when its feed is late, the way a hungry ear complains — not agony, but nag. We mistook the nag for need because a big story taught us its language.

The Smokescreen taught you to read it as need. The big story above said: this tug means you cannot cope, cannot think, cannot be yourself without a dose. The little tug below only said: feed me soon.

Smokers often find the sharpest edge comes a day or two after the last dose, then it eases over a few weeks. Typical. Not identical for every body. Not weeks of torture. A short, restless peak that passes, not proof that the dose was your real self.

Feel the difference now. Recall the worst gap you sat through yesterday — the meeting that ran long, the train with no smoking car, the cinema with the lights down. The tug rose. You fidgeted. You watched the clock. Then you lit, and for minutes the tug went quiet. You said, you see, it calmed me.

It did not calm you. It fed the Nipper, so the Nipper stopped tugging for a little while. The problem papers sat untouched. The late bus stayed late. The nerves about money stayed exactly where they were. Only the tug quieted, because only the tug had been answered.

Think of the cinema in full. Lights down. Story on screen. Twenty minutes in, the tug stirs. You shift. You think the seat is hard. Forty minutes, the tug nags. You think the film drags. Sixty minutes, you watch the exit sign more than the faces. You tell yourself you need air. Interval comes. You hurry out, light in the cold with the crowd, draw fast, feel the quiet wash for minutes. You go back in and think, now I can enjoy the film.

What changed in the film? Nothing. Same actors. Same plot. Same seat. What changed was the tug fed, then fading again before the credits. The first half was spoiled not by a bad film but by an unfed tug. The second half was not improved by a good dose but by a tugged quieted for a little while. A non-smoker sat through both halves on one seat with one mind. You sat through two different films with one story: up, down, up.

Think of the long meeting. Agenda moves. Voices drone. At minute thirty the tug stirs and you call it boredom. At minute fifty you call it irritation with the chairman. At minute seventy you call it hunger. Three names for one nag. Break comes. Corridor. Lighter. Minutes of quiet. Back in, the chairman sounds almost wise for ten minutes. Then the names return. Boredom. Irritation. Hunger. The chairman is innocent. The agenda is innocent. The interval is guilty.

Ask your own body, and let it answer without the translator:

Did the tug ever twist you double, lay you shaking, burn with fever? Or did it only nag, fidget, hollow, edge attention?
Did it ever stop you lifting, walking, talking, laughing? Or did it only tint those acts grey until fed?
Did food lose taste for weeks when unfed, or did mouth and nose go on tasting while the mind said taste needs smoke?

You know the answers. The tug is too small to stop a life and too persistent to be ignored while believed. Believed, it rules the day. Seen, it shrinks to what it is: a dying complaint from a creature that lives only on coins.

I have sat that complaint out. So have millions who never thought they could. The first day the tug talks at the old hours — after food, with coffee, at the door — because hours were its feeding times. The second or third day it talks loudest, then its voice thins. Over a few weeks it forgets the hours. Typical, not a promise stamped to the hour for every body. Some feel little more than fidget. Some feel edgy for days and then light-headed and then oddly clear. None feel what the Smokescreen paints: endless torment that only a dose can end. The painting is the business. The tug is the paint.

Separate the two keepers once and for all. Below, the Nipper, small, physical, already starving when you stop feeding. Above, the Smokescreen, vast, learned, whispering that the small complaint means loss of calm, focus, pleasure, self. Starve the below by not feeding. Starve the above by not believing. The below dies in days to weeks. The above dies the moment you see it. Both deaths are quiet. Neither needs force.

### IT NEVER FIXED THE ITCH. IT CAUSED IT.

Think of a man who wears a tight band on his arm all day to scratch an itch. The band itches. He scratches through the cloth and sighs, ah, quiet. He scratches harder at noon and calls it pleasure. By night his arm is raw, and he thanks the scratching for getting him through the day.

Would you call him cured? Would you say the scratching gave him anything?

We wore the band. Every dose tightened it for the next gap, then scratched it for minutes.

We lit to steady nerves the last dose had edged. We lit to clear a head the last dose had fogged. We lit to end a craving only the previous dose could have planted. Each time we credited the rescuer. Each time the rescuer was the perpetrator in disguise.

The fact is flat. The dose never rose above the baseline of a man who never smoked. It only dragged us a little low, then lifted us a little toward normal, then dropped us again a little lower. A non-smoker lives at normal for nothing. We paid all day to visit it for minutes.

Scratch this one place until you see it, because once seen it cannot be unseen.

That is how the nicotine trap holds millions without walls. Small tug below. Big story above. Coin, quiet, fade, call. Day after day.

That is why you can walk away from it easily, immediately and permanently — not because you are strong, but because there is nothing to miss. A scratch that causes its own itch is not a pleasure to mourn. It is a con to lay down.

It never fixed the itch. It caused it.

Hold that sentence where you can reach it. When the tug stirs at the old hour, hear the sentence before the story. When the hand half-moves, hear the sentence before the pocket. When memory paints one golden dose — sun, laughter, coffee steam — hear the sentence before the painting dries. The painting leaves out the fade. The sentence puts the fade back in.

Ask the golden dose to show its papers:

Where did the calm of that best dose live — in the tobacco, or in the ending for minutes of the edginess the previous dose left?
Where did the pleasure live — in the smoke, or in the quieting of a nag that a non-smoker never carried into that sun?
What did the dose add to sun, leisure, company that sun, leisure, company did not already hold?

You know, because you have watched the interval with nothing changed outside. The sun did not change in nine minutes. The company did not change. The coffee did not change. The tug changed. Up, down, up. Credit the sun for sun. Credit company for company. Credit the dose for the tug and the fade, which are its only works.

### WHEN OTHER HANDS LIFT, KEEP YOUR OWN EYES

This seeing will be tested in the cheapest place: beside other smokers.

You will stand at a door and watch a hand lift a dose to a mouth and the face soften for a moment as the meter needle jumps. The old voice will speak at once in your dialect:

“Look, it does something for him. One won’t hurt. Just join in.”

Watch with clear eyes and you will see something else. You will see a man drop a coin and mistake the jump for a gift. You will see the needle already falling while he exhales. You will see him ten minutes later, edgy again, reaching again. You will see yourself as you were — not enjoying a pleasure, but quieting for minutes a tug the last dose left behind.

Do not envy that round. There is no rising in his shoulders dropping, only a brief return toward where you already stand without feeding. He is not rising. He is renting.

Stay with that picture through the whole break. Do not argue. Do not preach. Do not walk to the cold corner to prove anything. Keep your hands on what they hold — mug, paper, wheel — and let the huddle do what huddles do while believing what you no longer believe. Their lighting does not vote on your seeing. Your seeing was earned in your own day, your own meter, your own arm, and no lifted hand across a table can un-earn it.

Picture it near. Work door. Cold air. Three coats. Lighter clicks. Laughter that is really about work and weather and football, with smoke riding along. You stand with your mug, part of the talk, not part of the coins. One lifts and sighs as the quiet hits. Ten minutes later he shifts, checks his pocket, half-listens while watching the door. Another lights off his stub. Chain of coins, chain of fades, all inside one chat about football. The chat held the warmth. The coins held the interruptions.

Picture it nearer. Table. Drinks. Friend pushes the pack across. Smile. “Go on.” Your hand does not move because your eye has moved. You see the offer for what it is: not company, not calm, not a moment, but a fresh itch with a minute’s scratch inside it. You smile back, stay in the talk, lift your glass, answer the story that was interrupted. No lecture. No line drawn. The pack sits there, talking loudly to those who still hear it, silent to you.

Ask yourself while they light:

Did his first draw change the joke that made you laugh, or did the joke change you while the draw only quieted his gap?
Did her shoulders drop because the night is kind, or did the night stay kind while her tug paused for minutes?
If their doses truly gave, why must they leave the table again so soon to feed again?

You know. The night gives. The drink, the lights, the company give. The dose takes and rents back. To join them now would not be to join the night. It would be to leave the night for the meter, then pay to visit the night for minutes, then leave again.

Keep your own judgment hour by hour and the test becomes proof. Each lifted hand that once would have pulled you now pushes you clearer: there goes a coin, there goes a brief quiet, there goes the fade, there goes the next reach. You do not need to count his reaches to feel superior. You only need to not mistake his jump for a gift you lack. What he visits for minutes, you inhabit without paying — the normal mouth, the steady hands, the attention that can stay with a face without checking a pocket.

If the voice says, you are missing out standing here with empty hands, answer with your interval. Empty hands held a mug through fifty minutes with nothing changed outside and everything explained inside. Empty hands are not missing a pleasure. They are missing a fade. Who mourns a fade?

That is why other smokers lose their vote. Not because you fight them. Not because you avoid them. Because you see them. Braggarts about pleasure and groaners about need speak the same old story from different ends of the shelter. Both still believe the jump is a gift. You have watched the jump fall minute by minute while the bus never came. Belief cannot survive watching. Watching is the end of believing.

I-07 — REFUSE TO BE INFLUENCED BY OTHER SMOKERS
Watch them with clear eyes and keep your own judgment.

SUMMARY
- A day of doses was one flag lifted and falling, not twenty separate gifts.
- Between two doses the outer scene stayed still while the inner quiet wore thin on its own clock.
- The brief quiet carried its own ending, and the ending called for the next dose.
- The feeling in the gap was a small hollow nag with a short peak, not a picture of my nature.
- Lighting quieted only the nag and left street, bus, work and money exactly as they were.
- Other hands lifting showed the same lift and fade, and gave no reason to light with them.
```
