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

Delivered 4640 words. Budget 5000.

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

### The draft chapter
```
Chapter 14
FREE FOR GOOD

*You gave up nothing, because there was nothing there to keep.*

### THE ASHTRAY WAS ALREADY EMPTY

Look at it plainly one last time.

That farewell table held a stained tip, a grey length of ash, a sour end that stung the mouth. No ceremony in the taste. No gift in the fingers. We watched it burn down because we had decided to watch closely, and what we saw was paper and weed and a chemical nudge calling itself comfort.

The ashtray was already empty — you were the one who kept refilling it, and now you have put the habit down like a borrowed coat that was never yours.

Does that picture shock you? It should settle you. For years we filled the glass tray ourselves, dose after dose, and then stared at the pile and said the tray made us do it. We paid for the doses. We lit them. We carried them to mouth. The tray never asked. The coat never owned us. We wore what was handed to us when we were too young to check the fit, and we kept wearing it long after it stank and burned holes in the lining.

What did it ever do for the hours you gave it?

It does plenty TO you. It does nothing FOR you.

Ask it straight, and let your own days answer. Did it mend the quarrel? Did it finish the report? Did it make the food taste richer, the drink warmer, the company kinder? Did the night on the patio turn on the lit end, or on the laughter and the lights and the warm air and the friends pulling their chairs close? You know the answer because you have lived both sides of it now. The work was yours. The laugh was yours. The night was yours.

It never fixed the itch. It caused it.

That is why mornings once began with cough and hurry, and afternoons broke into forty-minute slices, and evenings ended at a back door with a coat still on. Not because life is hard, but because a small nudge kept tapping the ribs and calling itself need. We lived for years stale, breathless and chained, and called the chain a prop.

We were conned out of choice, you and I. The first sticks were taken to look grown, to belong, to try. Then the nudge arrived, and the talk around us gave it a name that was false — pleasure, crutch, friend, break. That talk was the Smokescreen, and while it stood, we kept feeding the nudge and calling the feeding ours. The place we lived in had a name too. You have left the nicotine trap behind for good.

If the old voice pipes up, “Just one to prove I am over it,” what would that one prove? That one lit end ever gave anything? That the tray was ever full on its own? You have watched the trick from inside and outside. There is nothing to test.

### WHAT YOU KEEP WHEN A THOUGHT DRIFTS BY

A thought will drift by. A smell on a coat in a queue. A hand half-lifting after food. A laugh from a doorway where others stand with lit ends.

Let it come. You do not debate it. You label it and stay with the day you are in.

Say to yourself in plain words what you now know, and keep these lines as your own.

If doubt whispers that life may feel flat, answer that you have nothing to lose and everything to gain.

You stepped out of it easily, immediately and permanently, not over months, not by inches.

If a faint stir moves in the chest, know it for what it is, an empty, slightly restless, slightly edgy little tug, nothing more, a dying echo that means no gap needs filling.

That stir is only the Nipper losing interest. Unanswered, it fades. It cannot pull a hand to a pack.

There is no torn middle any longer. The long pull between fear of coping and fear of missing is done, the tug-of-war of fear is over because neither rope belongs to it now — not fear of coping, not fear of missing. Both ropes were its own talk.

And the whole keeping is simple. All you have to do is follow all the instructions.

I smoked through deadlines and drives and nights out, and I believed each lit end steadied me. I know how loud the old accent can sound in its old livery. I also know what a morning tastes like when the mouth tastes of toothpaste and nothing else, what food tastes like when the tongue is left to its work, what a walk feels like when the legs choose the length. Yours now. Take a sip of water. Keep the hands in the work they were in. The thought passes, and the street you are on stays yours.

Pity the lit ends you see, never envy them. You do not stand outside something warm. They stand inside something cold, feeding a nudge and watching the burn. You walk past the shelter with collar up and pocket light, and the ride is only a ride, and lunch is eaten to the end.

### THE POCKET STAYS LIGHT

Check what you carry.

Phone and keys. Coins for bread and milk. Hands that hold hammer, pen, mug, wheel, rail, paper, keyboard, and rest flat on the desk doing nothing at all when the job is done. Coat that smells of bus and office and cold at midday, of rain and chips and diesel on the way home, of cupboard and night in the morning. Kitchen that ticks back into order when hands stay with it to the end. Lamp on. Shoes off. Talk that carries without help.

Nothing tapping. Nothing counting. Nothing to feed before starting.

That is the proof you hand from one ordinary hour to the next. Not thunder. The quiet receipt of reaching the end of a meeting without once thinking of the door. Of finishing a drive without checking the mirror for a place to stop. Of closing a drawer and finding nothing in it that taps.

### SUMMARY

- Mornings belong to kettle and street, not to lighting before living.
- Food tastes of itself when the tongue is left to its work, finished when hunger is finished.
- A pause is legs and eyes and air, not paper standing beside it taking the bow.
- The shop glass stays where it is while the basket holds what you came for.
- A faint stir in the chest means no gap needs filling.
- One lit end never proved anything except the talk that sold it.
- Evenings hold food and talk and company exactly as they are.

Keep this picture. These are the lines that brought you here:

1. KEEP AN OPEN MIND
Give this book a fair hearing and it will free you.
2. DON'T STOP OR CUT DOWN YET
Smoke as normal until your last cigarette.
3. BEGIN BY FEELING GREAT TO BE ESCAPING
There is no doom here, only freedom ahead.
4. FOLLOW ALL THE INSTRUCTIONS
All you have to do is what this book asks.
5. IGNORE ANY ADVICE THAT CONFLICTS WITH THIS BOOK
Let this argument finish before you borrow another.
6. DISREGARD ANYONE WHO QUIT BY WILLPOWER
Their struggle was the method, not you.
7. REFUSE TO BE INFLUENCED BY OTHER SMOKERS
Watch them with clear eyes and keep your own judgment.
8. TRUST YOUR BODY TO BREATHE AND TASTE
Your body knows freedom without being taught.
9. SEE THE SELLER BEHIND THE SMOKE
Remember who built the trap and why.
10. MEET THE BEST CIGARETTE HEAD-ON
Let the favourite prove it gives nothing.
11. NEVER ALLOW JUST ONE OR A SPECIAL ONE
One keeps the trap alive.
12. SMOKE YOUR FINAL CIGARETTE AND KNOW YOU ARE FREE
Close the trap with joy, not sadness.

Go out now and get on with enjoying your life.

### THE FIRST MONDAY WITHOUT A TIMETABLE

Monday comes with its ordinary noise, and you meet it with light hands.

Alarm. Cold floor. Kettle. The same bus with fogged windows. The same desk with the same pile. Nothing in the morning asks for a fee first. You pour tea and drink it standing by the window, and the steam thins into the light, and the house ticks, and you go out with phone and keys and nothing tapping the ribs.

At work the phone rings and the inbox fills and a job runs late. You answer what needs answering. You square papers with the palm of your hand. You carry a folder from desk to shelf and lay it flat. When legs want standing, you stand. You walk to the window and look for thirty seconds at roofs and gulls and washing hung two streets over. You drink water. You go back in when you are ready, and the pause ends because you decide the pause has done its job.

Someone at eleven says, “Coming out for air?” You smile and say, “I will stretch my legs in a minute,” and you do, by the front step where the air moves, with both hands holding a mug. No watching a burn. No nursing it to make it last. No hurrying it because the boss is looking. The length of the walk is yours to choose. Five minutes or fifteen. Past the park or past the station.

Lunch holds. You walk in for food because you are hungry. Ham and cheese, or soup in a pot, or the salad box with extra chicken. The basket holds what you came for. The till dings. The drawer opens and shuts. You pay and take the coins and drop them where they belong. No second purchase. No sums about box and sandwich both.

Find your bench. Sit down and open what you bought. Let the paper crackle. Salt. Butter. The sharp edge of cheese. Water lifting the mouth clear for the next bite. Eat to the end. Fold the paper. Push the crumbs into a pile with your thumb. Sit a minute with shoulders where they are, not pulled up toward ears waiting for the next gap. That unchased minute is what afternoons are made of now.

The afternoon moves hinge by hinge. The drawer opening and shutting. The pen uncapped and capped. The chair pushed back and pulled in. Answer the short email first to clear the deck. Two lines. Sent. Stand to file and feel the floor cold through shoes on the way to the cabinet. Walk to the printer and back while pages warm and drop. Talk to the person two desks down about the delivery date and the missing invoice, and laugh if there is something to laugh at while you stand there.

By four the light thins. You feel tired in the honest way food and work and hours bring. Tired eyes. Tired feet. A head full of words. Take a sip and stand and let legs take the weight a minute. The day closes the way days close — last email sent, drawer shut, chair pushed in.

On the way home you go in for milk and bread. The queue is longer now, with school bags and tired feet. The glass stands behind the till and stays there. You keep what you came for — carton cold in hand, loaf warm under arm. Walk out with both hands holding the evening. The street smells of rain on warm pavement and chips from the corner shop and diesel from the bus pulling away. Your coat smells of your day. That is how coats should smell at six o'clock.

Home is the same rooms with the same light. Bag on the table. Milk away. Bread in the bin. Shoes changed. Hands washed with hot water and soap. Sit five minutes with tea before supper, because legs like sitting after standing all day. Then chopping and hearing the knife on the board. Onion sweetening in oil. Sit to eat while it is hot. Chew. Drink water. Have seconds if still hungry. Push the plate away when hunger is finished. Scrape. Stack. Wash the pan while still warm. Wipe the board. Put leftovers in the tub for tomorrow. Sweep crumbs into palm and tip them into the bin.

Then sit. Lamp on. Shoes off. Cushion pulled to back. Hold tea with both hands and drink it while hot enough to warm palms. Watch the programme you always watch. Answer the message you missed at lunch. Talk about the day in plain sentences. Fold the washing that sat on the chair since morning.

Teeth brushed. Face washed. Bed turned down. House going quiet room by room as you go through switching lights off the way you switch off any finished work. No doorway chosen. No pocket weight checked. The night outside the window is still yours — rest, breath, sleep ahead — held now without the hourly tap.

That is Monday. Tuesday will be Tuesday. Wednesday will bring its own rain. Each ordinary hour hands its proof to the next, and you collect the receipts without counting them.

### THE FIRST HARD HOUR AND THE FIRST GOOD LAUGH

The hard hour will come, because hard hours come to people who never lit a dose in their lives.

A bill larger than expected. A phone call with a sharp voice on the other end. A deadline moved forward. A child crying at midnight with a temperature. A car that will not start on a wet morning. Life does what life does, and your chest tightens the way chests tighten when news lands.

Watch what happens now.

Before, the hand moved before thought, and the papers sat untouched while the tip burned, and the problem waited in the same place when the ash fell. Now the papers sit where you left them, and you sit where you are, and you deal with the thing itself. Pick up the phone and say the difficult sentence. Write the figure in the margin with the date beside it. Put the long report into three piles — done, doing, waiting — and square the done pile. Call the garage. Hold the small hot forehead with the back of your hand. Do the next small true thing.

If a picture drifts by in your old accent — doorway, break, “this would be easier with one” — you recognise the old uniform and stay with the day you are in. You have nothing to lose and everything to gain by staying. You label the line as talk from years of wearing a borrowed coat, and you keep the hands in the work they were in. Take a sip of water. Keep listening till the other person finishes the sentence. The pull loses interest when unanswered, and one morning you notice the morning asked nothing at all.

I know that half-lift of the hand after food, that slide of eyes to pocket in a queue. It lived in my mouth for years, so of course it pipes up in its old voice. I do not argue with it. I stay with the conversation, the task, the street I am on. The thought passes, and the street stays mine.

And the good laugh comes too, because good laughs come often when you stay for them.

A birthday with candles and bad singing. A football result going your way in the last minute. A friend telling a story badly and laughing before the end. A sunny Saturday with washing on the line and a queue at the ice-cream van. You laugh with mouth and chest and eyes, and the laugh carries without help. No stepping out halfway. No watching the clock through the pudding. No doing sums about whether one is left for after.

When friends light up by the door, you pity the lit ends, never envy them. You do not stand outside something warm. They stand inside something cold, feeding a nudge and watching the burn. You hold your drink with both hands if the evening is cool. You pull your chair a little closer where the talk is. You stay till the story ends, because there is no tip to finish before you go in.

That late-night patio with friends and drinks holds its laughter without asking for anything laid over it. The lights strung above. The chairs scraping. The talk rolling. You walk home with collar up and pocket light, and the ride is only a ride, and the night air tastes of night air.

### THE FIRST TRIP, THE FIRST PARTY, THE FIRST QUIET SUNDAY

The weeks widen, and each widening brings its own ordinary proof.

The first long drive. Tank full. Radio on. Both hands on the wheel, drumming thumbs to the song. Window down an inch for the cool. For years the right hand at those lights would have been out managing a tip, left hand tight, eyes on the mirror for ash. Now the hands stay where they belong, and the song plays to the end. You stop when you want coffee, not when a tip burns down. You stretch legs at the services, wash face with cold water, drink coffee while hot, watch lorries pull in and out. The road holds together without a cut in the middle. You arrive with fingers smelling of nothing but wheel and coffee, and the boot holds what you packed, and the day at the other end starts on time.

The first party. Dress chosen. Shoes polished. Taxi booked. Room warm with talk and music and plates going round. Someone bums cigs by the back step and laughs, “One won't hurt, come on.” You smile with clear eyes and keep your own judgment. “I don't do that any more,” you say, in the same tone you would use to refuse a second pudding — plain, kind, finished. No lecture. No preaching. No dragging a fresh view back into argument. You turn back to the room where the food is. You eat what you like and dance if dancing happens and talk till the taxi hoots. The night is yours from first hello to last goodbye, not cut into slices.

The first quiet Sunday. No plans. Paper unread. Rain on the glass. You potter. Kettle. Toast. Second tea. Put one pile of washing away and leave one for tomorrow. Mend the drawer that sticks. Walk to the shop for a paper and an apple. Sit on the low wall and watch the street go by, and what strikes you is how long lunch is when you stay inside it. The pie takes the time the pie takes. The apple takes the time the apple takes. The street takes its own time, and you have time to watch it.

The first holiday. Case packed. Passport checked. Coach to the airport with seats booked by the window. Queues. Announcements. Small plastic trays through the scanner. Hours in the air with a book and a nap and a meal eaten to the end, tasting of salt and bread and juice. No watching the clock for the wind end. No counting whether the box will last the flight. Arrival with eyes tired from travel and mouth tasting of water, and the sea doing what the sea does. Sun on shoulders. Sand in shoes. Talk that carries without help.

Through each of these you carry the same light pocket. Phone and keys. Coins for bread and milk. Hands that hold rail, paper, mug, wheel, and rest flat when the job is done. Coat that smells of your morning, of bus and office and cold, never of a wind end. That lightness stops being news and starts being normal, the way breathing through the nose is normal after a cold clears. You stop checking for it. You live inside it.

If doubt ever whispers on a tired evening that life may feel flat without little parties laid over it, you answer with what you own. You stepped out easily, immediately and permanently. Your body knows freedom without being taught. It breathes and tastes on its own. Food tastes of itself. Coffee tastes of coffee itself, hot and a little bitter and milky at the edges. Water lifts the mouth clear. Air moves where smoke used to push through. Shoulders sit lower now than they did between doses, because there is no next gap to watch for.

### THE MONTHS THAT STACK UP QUIETLY

Money stays where money should stay, and that is a bonus, never the motive.

You notice the drawer that once held foil and lighters holds batteries and stamps. The shelf by the back door that once held a tray grey with ash holds keys and a plant that needs watering. The car smells of upholstery and apples. Curtains keep no score. The dentist nods at pink gums. The stairs take breath without the shallow sip and the cough to clear. These are quiet facts, arriving without fanfare, stacking month on month.

You do not count days. Freedom is not a staircase where each step must be tallied. You are free as of your last stubbed end, and each week proves the same freedom in a new room. The first month without a timetable. The second month with a cold that passes like colds pass. The third month with a promotion interview handled in plain voice. The sixth month with a winter coat pulled from the cupboard smelling of cupboard and night, nothing else.

People will ask how you did it. Tell them short and warm, and leave the door open without pushing them through it.

“I saw it did nothing for me, so I stopped, and I am glad.” That is enough. Let visible living do what arguing cannot. Do not preach on doorsteps. Preaching breeds defence in friends and drags a fresh view back into debate. If they ask more, lend them your own plain sentences — mornings with kettle steam, lunches eaten to the end, walks chosen for their own sake. If they scoff, disregard anyone who quit by willpower and told you struggle was the price. Their struggle was the method, not you. Watch other smokers with clear eyes and keep your own judgment. You know that livery too well to walk behind it.

I smoked through deadlines and drives and nights out, and I believed each lit end steadied me. I keep that memory kindly, not as a chain but as a reminder why I speak warmly to people still inside it. We were all conned, you and I, by talk that named a nudge as pleasure. While that talk stood, we fed the nudge. Now the talk has fallen, and the feeding has stopped with it.

If a faint stir ever moves in the chest in month four or month fourteen — a smell on a coat in a lift, a hand half-rising before thought — know it for what it is, an empty, slightly restless, slightly edgy little tug, nothing more. That stir is only the Nipper losing interest. Unanswered, it fades. It cannot pull a hand to a pack. Stay with the conversation, the task, the street you are on. Take a sip of water. The thought passes, and the street stays yours.

There is no torn middle any longer. The tug-of-war of fear is over because neither rope belongs to it now. Not fear of coping. Not fear of missing. Both ropes were its own talk. All you have to do is follow all the instructions, and you have followed them, one by one, to this ordinary life.

### WHAT TO DO WITH THE REST OF YOUR LIFE

So what now?

Now you live.

Mornings with kettle steam and cold lino underfoot. Shop queues with baskets holding what you came for. Desks with piles that shrink under hands. Walks with both hands holding the evening. Tables with talk that carries without help. The days ahead are not tests. They are hours with shape and weight, and you will live them through to the evening without a timetable cutting them into slices.

Change nothing else in life to prove anything. Keep coffee if you like coffee. Keep tea if you like tea. Keep the seat by the window where you always sit. Keep the bench, the wall, the corner of the canteen where light falls across the table. Freedom does not need a new uniform. It needs the old days lived exactly as they are, with each ordinary hour handing its proof to the next.

Look out as the bus pulls off. Shops with shutters half up. A man hosing pavement outside the bakery. School bags bouncing. Nothing in you waiting for the stop where you once got off early to stand at the wind end. You ride past that stop and stay seated, and the ride is only a ride.

Stand a second outside the shop with bag in hand and let the street settle. Vans double-parked. Pigeons working crumbs by the bench. The chemist sign swinging. Air smelling of rain and chips and diesel and fresh bread from two doors down. Your coat smelling of your morning, of bus and office and cold. That is how coats should smell at midday.

Eat to the end. Fold the paper. Drink the last of the water. Sit a minute with back against the bench. When you stand, you stand because you have finished, not because a tip has burned down. Pick up rubbish. Put bottle in the bin. Your fingers smell of bread and salt. They smell of what you just held. That is all they need to smell of.

Go back in through the door you always use. Hold it for the person behind you. Stamp feet if wet. Put bag down where you always put it. You smell of street and lunch, not of a wind end. That is not a small detail. Coats and curtains keep the score long after we have stopped noticing.

Evenings hold food and talk and company exactly as they are, with old pictures arriving pre-labelled and left to pass. Lamp on. Shoes off. Tea held with both hands. Programme watched. Message answered. Talk in plain sentences — queue, bench, invoice, bus pulling away. Windows locked and bins taken to the step for morning. Teeth brushed. Face washed. Bed turned down. House going quiet room by room.

When an old picture drifts by in your own accent, you recognise the old uniform and stay with the day you are in.

Keep these lines as your own for good. If doubt whispers, you have nothing to lose and everything to gain. You came out easily, immediately and permanently. A faint stir is only an empty, slightly restless, slightly edgy little tug. That stir is only the Nipper losing interest. The talk that fed it was the Smokescreen. The place you left has a name, the nicotine trap, and you have left it behind for good. There is no torn middle, the tug-of-war of fear is over. The whole keeping is simple. All you have to do is follow all the instructions. The ledger is short. It does plenty TO you. It does nothing FOR you. It never fixed the itch. It caused it. You lived for years stale, breathless and chained, and now you live unchained in clean air.

The ashtray was already empty — you were the one who kept refilling it, and now you have put the habit down like a borrowed coat that was never yours. Leave the tray empty. Leave the coat on its hook. Walk out with light pocket and both hands free for the life that was always yours.

YIPPEE! I'M FREE!
```
