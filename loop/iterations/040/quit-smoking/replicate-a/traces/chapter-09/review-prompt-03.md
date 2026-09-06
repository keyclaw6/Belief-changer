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

Delivered 4402 words. Budget 4500.

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
```

### The draft chapter
```
Chapter 9
THE HAND THAT LIT YOUR FIRST ONE

**IN THIS CHAPTER** — the pack in the palm, the count to midnight, the filter with holes, the pull both ways, the stale stairs

*That want was never yours; it was built, boxed and sold to you.*

### THE BOX IN YOUR PALM

Pick up your pack and hold it flat in the palm for a moment.

Not to smoke it. To look at it.

Twenty white tubes in a row. Foil. Cellophane that crackles. The click of the lid. We learned to love that click the way a child loves a sweet tin opening. Clean. Smart. Ours.

Look longer.

That box is a day's supply box. Count it. If you smoke twenty a day, that box is measured to run out by night. If you smoke thirty, you buy the larger box or you buy twice.

Follow that counted box from full to empty and you will see whose timetable you have been living on.

Morning. Seven o'clock. The box is fat. It sits square in the palm, heavy, the foil unbroken or newly opened. You tap one out and the rest stand shoulder to shoulder. Plenty. No worry. The first three go almost without counting — one with the kettle, one with the coat on, one at the bus stop or in the car with the window cracked. By eight the row has a gap at the front like missing teeth. You barely notice. Full still reads as full.

Nine o'clock. Work. The box has moved from coat to desk drawer to shirt pocket. You take one on the hour because the hour asks. Ten o'clock, another. Eleven, another. Each time the lid clicks. Each time the foil rustles a little less because there is less to hold it up. By mid-morning you have made a dent you can feel with the thumb. The box is lighter. It rattles when you shake it. You push the remaining tubes to the front with a finger so the next one comes easy.

Midday. You open for the after-food dose and you see it plainly for the first time that day: half gone. Ten left. Ten smoked. The morning ate half the box without a single decision you would call a decision. You count without meaning to count. Ten left for the whole afternoon and evening. Will it last? You do the small arithmetic every smoker knows. Four in the afternoon. Three in the evening. Two after supper. One before bed. That leaves none spare. You tell yourself you will be careful. You tell yourself the evening will be quiet.

One o'clock. Two o'clock. The careful plan lasts an hour. The hand moves at the old times. The box thins. Three o'clock, you tip it and look inside instead of just taking. Four o'clock, you feel the weight before you open, weighing by hand whether there are four or three. Five o'clock, you count by touch through the cardboard. There is a particular softness to a pack with three left — it bends at the corners, it loses its square pride. It no longer clicks. It whispers.

Evening. Supper done. Two left. You smoke one and know there is one left and the night is still long. The talk at the table, the programme on the television, the phone call, the drink — each carries its old hour with it. You start to bargain. If I have the last one now, I will enjoy the programme more. If I save it, I will sleep better knowing it is there. You save it. You put the pack in the pocket and feel that single tube through the cloth like a coin you must not spend.

Nine o'clock. The want comes. You touch the pocket. One left. You decide to hold. Ten o'clock. The want comes harder. You take the last one out and look at it. You roll it between finger and thumb. You tell yourself this is choice, pleasure, reward for the day. You light it standing at the door and you smoke it slower than the others, down to the stain, because after this there is nothing.

Then there is nothing. Empty box, crushed in the fist. And the panic starts.

Every smoker knows that panic. It is not in the lungs. It is in the hands and the chest and the eyes on the clock. Shops shut? How far is the garage? Who is still up? Can I borrow from next door without looking desperate? You have stood in rain at eleven at night outside a shut shop, coat over pyjamas, telling yourself you will just check if the machine works. You have knocked on a neighbour's door for milk you did not need because you hoped to see a pack on the side. You have bummed one from a stranger with a joke to cover the begging, and walked away promising yourself you will pay him back tomorrow and hating the thankfulness in your own voice.

“I need one or I won't sleep.”

You say it, I have said it, we have all said it at midnight with an empty box in the hand. So ask it plainly, with the crushed box still in your fist:

Did your body run out of something it was born with, or did their box run out on their schedule?
Did midnight make you sleepless, or did the timetable make midnight fearful?
If the want was your nature, why does it keep shop hours?

You know. A hungry man does not panic because the packet is empty; he hungers because the belly is empty, packet or no packet. A smoker panics because the packet is empty, belly full, evening warm, bed ready, nothing wrong except the count has reached zero. The distress follows the supply, not the body. That is not appetite. That is a refill alarm built into a portable dispenser.

See the hands that set the count. A pack of twenty is not an accident of paper folding. It is a day's rations for a twenty-a-day customer, cut to burn for so many minutes, each drag sized to carry its squirt of nicotine into the lungs and up to the brain within seconds, then fade within minutes so the next is asked for. They measured puff volume in laboratories while we were still at school. They weighed how hard a human pulls, how long a tube should last, how many tubes keep a customer returning daily for decades without dying too fast to pay. Then they wrapped the arithmetic in foil and called it mine.

I know this is hard to accept, but look at whose hands made it so.

In an internal planning memo, one of their own scientists put the design in plain words: the cigarette should be conceived not as a product but as a package. The product is nicotine.

Not flavour. Not company. Not adulthood. A package. The paper, the filter, the brand, the gold band — the packet around a drug dose. They built a dispenser you carry in the shirt pocket, and they taught you to call the dispenser a pleasure.

Did you invent that box?
Did you decide that a tube of paper should carry a drug to your brain in ten seconds?
Did you teach your own throat to want smoke before you ever smoked?

You know. Nobody is born asking for burning leaves. We were all non-smokers once, breathing, tasting, coughing when smoke drifted near. Then the posters, the films, the older boys at the gate, the break-room laugh, the father at the table with smoke curling from his fingers — a thousand pictures said: grown, calm, together, in control, with one of these. We tried the first. It burned. It made us dizzy and sick. And the big story said: persist, you will learn to enjoy it. So we persisted until the throat went numb and the brain learned the loop.

Take that teaching forward into the self you fear losing, because that is where it still holds you.

Before you ever drew willingly, you had already learned how a smoker stands. You had seen him on the late patio with friends and drinks, head back laughing, hand lifted with something lit in it as if the laugh needed the lift. You had seen him at the work door at ten and three, shoulder to the frame, with the huddle around him, talking low while the rest stayed inside. You had seen him push back from the table after a meal, tap the pack, step out with the click, while the plates still sat warm. You had seen him behind the wheel with the elbow out, after an argument with the phone down, with a drink in the evening, at grief, at bills, at waiting. Everywhere a grown life pressed, there he stood with the answer in his fingers.

No child dreams of cough. What we dreamed was the stance. Grown. Calm. Together. In control. Amused. A man who knows what to do with his hands while others talk. A woman who can close a meal and open the night. We fitted that stance long before we fitted the smoke. We rehearsed it in the mirror of every film and doorway before the first vile puff ever touched the throat.

And the first puff was vile. Ask your own throat. It burned. It choked. Eyes watered. Head spun. If the stance had been nature, nature would have welcomed it. Nature spat it out. What overruled the throat was not the body. It was the pictures. The pictures said: persist and you will become him. So we coughed and persisted until numbness let us wear the stance without gagging, and then we called the numbness enjoyment.

Now watch where that old fitting reappears as fear.

When you picture succeeding and feel a hollow, what picture comes? You on that same patio with empty hands, not knowing where to put them while others laugh. You at that same doorway with nothing lifted, standing oddly while the huddle talks. You at that same table with no step out to mark the close, lingering while others rise. You on that long drive, after that row, with that drink, with nothing in the fingers — flat, dull, missing, not quite yourself. That missing self is not yourself. It is the dressed self they fitted on you before you ever smoked. The stance came first. The drug was sewn inside the stance to keep you paying for the clothes.

Ask that evening picture plainly:

Did you fear losing laughter, or losing the lifted hand the posters taught you to lift while laughing?
Did you fear losing the pause, or losing the doorway stance the break-room taught you to take while pausing?
Did you fear losing the meal, or losing the tap-and-step the table taught you to perform after eating?

You know. The laugh, the pause, the meal were there before the costume. The costume was added by other hands and then stitched to the skin by hourly dosing until you mistook stitching for skin. Fear of succeeding is fear of stepping out without the suit they lent you. But the suit was never yours. The shoulders underneath are still your own, still grown, still able to stand, laugh, pause, eat, drive, answer, grieve, with hands that have plenty to hold.

See who holds that suit now. The same hand that counted the box to run out by night counted the pictures to run for life. One hand measured puff and yield to build the hunger. The other hand measured poster and film and doorway to dress the hunger as you. The hunger makes you buy. The costume makes you stay bought. Both ropes run back to that one counting hand. The seller holds the costume.

You are looking straight at the nicotine trap.

That is not an insult. We were conned out in the open, by men in suits who measured puff volume and nicotine yield while we were still at school. They needed a customer who would return every hour for decades. They built him. They built you and me as customers, and then they told us we had chosen.

Ask the pack in your hand:

If this was your nature, why did the first one taste vile?
If this was your choice, why does the hand move before you decide?
If this was your pleasure, why must you carry the supply or panic?

A man who truly loves Stilton does not panic when the shop is shut. He waits. He does not step into rain at midnight to beg a lump from a stranger. Want that makes you hide, beg, Febreeze your coat, lie to your children — that was never appetite. That was a package doing its job.

They built the hunger. They sold you the bite. And when you see the pocket as carrying their package on their schedule, something loosens in the chest. The hourly call stops reading as my need and starts reading as their refill bell. The midnight panic stops reading as proof I cannot cope and starts reading as proof the dispenser emptied on time. You do not argue with a bell. You stop carrying it.

### THE THEATRE OF LIGHT AND MILD

Then, when cough and stain began to trouble us, they brought out the second trick.

The white tip. The gold ring. The words light and mild. The tiny holes around the filter you can see if you hold it to the light.

We believed we had found the sensible version. Same ritual, less harm. A cleaner smoke. My uncle smoked lights and told me, with complete kindness, that he had switched to protect his chest.

Look at that filter with clear eyes.

Those vents were drilled to dilute the smoke measured by a machine. A machine takes small, even puffs and reads lower numbers. A human does not smoke like a machine. Many of us cover those little holes with lips and fingers without ever knowing it. Many pull harder for the missing hit, draw deeper, hold longer. Not every smoker does it in exactly the same way — hands differ, lungs differ, days differ — but the human response runs the other way from the machine's. The machine sips. The man drags.

I watched myself do it. I held a light between thumb and forefinger square over the vents, drew until my cheeks hollowed, held it down, and called it smoother. Smoother only meant I had worked harder to get much of the same squirt. The theatre let me keep smoking while telling myself I had cut the risk. Machine-measured lower does not mean the smoker took less.

“But surely lights are a step down?”

That is the voice. So answer it with the filter in front of you:

Did the holes stop the hand moving every hour, or did the hour still call?
Did mild stop the morning cough and the yellow on the fingers, or only give them a paler name?
Who drilled those holes — you, for your health, or they, for your doubt?

You know because your own day knows. Doubt quieted. Dosing did not. The design did exactly what a package must do when the customer grows afraid: keep the drug coming while changing the costume.

That voice is the Smokescreen.

I am not asking you to be angry at yourself for believing it. Be angry where anger belongs. Warm to you, always; harsh to the trick. A decent person believed decent-sounding words printed on a decent box. The box was never decent. It was a dispenser dressed as a choice, and the mild was paint on the dispenser.

Once you see the paint, you cannot unsee it. The filter stops reading as protection and starts reading as stagecraft. The pack stops reading as mine and starts reading as theirs. And a strange thing happens in the chest when stagecraft is seen: the want loosens, because want was holding onto a picture that is no longer there.

Ask one more plain thing, because this is where they keep you longest. When you worried about cough, did they offer a way out of the cage, or a paler cage? When you worried about smell on the coat, did they offer clean air, or a whiter filter to hide behind? A seller who profits from the chain does not file the chain thinner to free you. He paints it silver so you will wear it longer. That is not care. That is maintenance of a customer.

See it, and the mild stops flattering you. You smoked harder through smaller holes to chase the same quiet, paid the same money for the extra work, and thanked the hand that drilled the holes for caring. The hand was never caring. It was counting. Count the holes, count the puffs, count the boxes per year, and you count their arithmetic, not your pleasure.

### PULLED BOTH WAYS AT ONCE

Under the want sits something else you have hardly named, and we must name it now because it holds many smokers more tightly than any dose.

Two fears. Opposite directions. Same neck.

One pulls forward: “What if I fail?” You have lit after vows before. You have told a partner this is the time and then stepped to the garage. You picture trying again, wanting badly at ten in the morning, snapping at noon, lighting by night, and having to say you failed again. Shame burns at the thought. So part of you says: better not try than try and prove I cannot.

The other pulls backward: “Who will I be if I succeed?” The patio laugh without the hand doing something. The break with empty hands. The meal closed without the step out. The long drive, the argument, the drink, the grief — all without the old prop. You picture yourself flat, dull, missing, not quite yourself at the table. So part of you says: better to keep the fault I know than lose the self I know.

“I cannot quit now. Too much stress. Too much pleasure at stake.”

I hear you. I said both in one day for years. Morning: I will fail, so wait. Evening: I will lose me, so wait. Wait is the trap talking in two voices.

So test both ropes with plain questions, here, with the pack still in sight:

If you failed before with patches and grit and counting days, did you fail — or did the method fail you by leaving the belief intact?
If the self you fear losing smokes every hour, coughs on stairs, hides in garages, pays for its own leash — is that your nature, or your costume?
If both fears tell you to keep buying, whose business do they serve — yours, or the hand that fills the box?

You know. The method that made stopping feel like loss guaranteed the struggle, then blamed you for struggling. And the self you mourn never existed before the first dose taught you to miss it. A child at a wedding dances, eats, laughs, stays late, remembers everything, with no dose in hand. That child was you before the package found you. Nothing true is lost when paint washes off.

See whose hands hold both ropes. Fear of failing keeps you from stepping out. Fear of succeeding keeps you from wanting out. Both fears were installed by the same seller: first make the customer doubt his own will, then make him doubt his own life without the product. Tell him quitting is hard and he will dread the attempt. Tell him life without will be empty and he will dread the result. A customer pulled both ways does not move. He buys again.

That is why the dread feels so personal and is so impersonal. You think: I am weak, I am hooked, I am not ready. The factory thinks: dose on schedule, doubt on schedule, repeat customer. Your midnight arithmetic — will three last till morning, will the shop open at seven, will she lend me two — is their business plan running in your head with your voice over it. You call it my worry. It is their till ringing.

Follow that thought into the day you fear most. You picture a row at work, a bill, a sick child, and you with nothing in the hand. You picture snapping, crying, failing. Look closer at the picture. Who put the empty hand in it? You have faced rows, bills, illness with a dose in the hand and still snapped, cried, shook. The dose never took the row away. It only paused the tug while the row waited on the desk. The fear of coping without is fear of coping without the pause, not fear of the row itself. Remove the tug and the row remains exactly what it was — to be answered, paid, nursed — with clear hands.

Follow the other fear into the evening you fear most. You picture laughter without the click, a drink without the step out, yourself standing oddly with nothing to do. Look closer. Who put the oddness in? The evening holds talk, food, music, cold air, friends. The oddness is only the old errand missing — leave to light, leave to finish. When the errand goes, the evening does not gape. It closes up around talk and stays warm longer because nobody keeps leaving it. The self you fear losing is the self who kept leaving.

That pull both ways is the tug-of-war of fear.

I do not want you to act from fright at what they did. I want you to see it so clearly that fright drops away. Walk the street tomorrow with nothing in the pocket and the morning doing its work, and that walk is your first taste of escape. No rope in either hand. Only air, and legs, and a head that no longer argues with itself.

Notice what happens when both ropes are seen in one pair of hands. The shame of past attempts thins. You did not fail because you are faulty. You failed because you pulled with all your strength on a rope they held at both ends. The dread of future days thins. You do not face a life of missing. You face ordinary days with the tug unfed for a short while and then gone from the reckoning. The customer who does not move because he is pulled both ways moves the moment he sees one hand holds both ends. He lets go, not by strength, but by seeing.

### STALE MOUTH, SHORT BREATH

Let us speak plainly about what the package leaves on the body, because soft words here would be another kindness that kills.

Morning mouth like an ashtray licked clean. Nose dull by noon so food needs salt and sauce to shout through. Throat clearing in meetings. Stairs taken in two goes while a man who never smoked climbs talking. Clothes aired, windows opened, mints chewed, the small constant housekeeping of hiding. Sleep shallow, waking grey, the first hour spent coaxing lungs that spent the night trying to sweep themselves.

This is not a lecture. This is what we live. If you are ill or worried about stopping, speak to your clinician for your body; here we deal with belief.

And belief must name the state without perfume: mouth stale in the morning, breath short on the stairs, leash short all day — stale, breathless and chained.

Hold that picture without flinching, then set beside it what you watched yesterday in kettle, plate and doorway. Water that wets. Heat that warms. Taste that lingers when left alone. Legs that loosen with walking. Eyes that clear with distance. Lungs that fill to the bottom without teaching. The body never forgot its trade. It swept, tasted, breathed, woke, settled, carried — under the coating, through the coating, despite the coating.

So which is you?

Is the cough you? Or the breath underneath that coughs to clear?
Is the dull nose you? Or the nose that still finds rain and bread when left uncoated for an hour?
Is the fidget at the old hour you? Or a small hollow asking for its coin while you go on talking, washing, walking?

The package needs you to mistake its marks for your nature. Take the marks away and nature stands there, older than any brand, ready to do its work without topping or marking. Soup tastes longer, stairs take less bargaining, mornings hold together, and you meet them as proof of freedom returning to the body.

I am not asking you to stop because the picture frightens you. Fright never released anyone; it only tightened the grip. I am asking you to stop because the picture is false and the life underneath is yours. See the seller, see the stagecraft, see both ropes in his hands — and gladness does the rest. There is nothing true to lose and a whole ordinary day to take back.

You do not need his box to wake, to taste, to pause. You need eyes that no longer credit the thief with the house he robbed.

Look once more at the pack in the palm. It is not a friend. It is not a part of you. It is their package with your money inside it. Remember whose hands built it and why they built it that way, and keep that seeing with you into the next room where your favourite will try to prove otherwise.

I-09 — SEE THE SELLER BEHIND THE SMOKE
Remember who built the trap and why.

SUMMARY
- The want did not grow in me; it was taught by pictures and kept by dosing.
- The box is a measured day's supply, and the tube is paper around a drug squirt.
- The count from full to empty each day was their timetable, not my appetite.
- Panic at an empty pack was the refill bell ringing, not proof I need it.
- Lights and milds changed the costume while the hourly call stayed the same.
- Fear of failing and fear of succeeding both pull for the seller, not for me.
- The stale mouth and short breath were marks of the package, not marks of my nature.
```
