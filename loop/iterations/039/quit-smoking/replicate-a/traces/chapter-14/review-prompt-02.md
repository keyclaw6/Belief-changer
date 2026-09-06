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
- `HEADER` — the draft opens with the workshop header `IN THIS CHAPTER`, or presents a plan-inventory entry instead of an earned spoken command. For each numbered instruction outside the final photographable recap, check that this card assigns it as NEW and that the immediately preceding argument makes its particular imperative the reader's warranted next conclusion; a generic rationale line does not establish either condition. Quote the header and the passage that should earn it. If it is an assigned echo rather than a new instruction, require the frozen words to remain verbatim as a brief spoken sentence in the current context, without an inventory number or a new-instruction announcement. If it is a new instruction, preserve its number and exact imperative, but replace the generic lead-in or rationale with the concrete connection to the argument already made; do not rebuild an earlier proof or announce the instruction's ordinal in words. A numbered command that meets these conditions, and the final photographable instruction recap, are not HEADER.
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

Delivered 5592 words. Budget 5000.

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
OUT THE DOOR WITH EMPTY HANDS

*There was never anything in the paper to miss, and what you put down was never yours.*

### WHAT YOU CARRY NOW

You came to this book braced for a lecture and a hard winter. I know that brace because I wore it myself for years, lighting with one hand while turning pages about lighting with the other.

Look what you carry instead.

You doubted the promise on the first page. You read on, and you found you have nothing to lose and everything to gain. That was not flattery. A con takes and calls it giving. Seeing the taking leaves no hole behind.

What happened since happened easily, immediately and permanently. Not by strain. Not by counting days. By seeing. We talked, you looked, the credit moved to where it belonged — to food, to pause, to company, to night air — and the paper was left with nothing of its own to stand on.

All you have to do is follow all the instructions. You did. That is why the mornings now run straight through, why the shop is only a shop, why the phone call is heard to the end. Keep that sentence in your pocket. When doubt taps later, answer with it first.

Did the paper ever cook the supper? Did it sign the papers on the desk? Did it hold the laugh together on the patio? You know the answer because you lived those rooms without it and they were whole.

I stood where you stand now, with an empty pocket and a clear tongue after years of paper between the knuckles. I remember the shuffle, the cough to earn the day, the coffee rinsed through sour. We all lived that shuffle. The shuffle taught us what the shuffle was: not character, not need, not nature. A timetable hired out by the hour.

You carry no timetable now. You carry a clear tongue, open hands, a pocket with keys, phone, coins. You carry a kettle that boils for tea, a cup washed without stepping away, a counter wiped in one minute because no second job pulls you to the step. You carry a desk left square for tomorrow, a mug washed beside other mugs, a bus ride that runs straight to your stop. Small things. They were always small. That is why they prove so much.

When the old line floats over — that one lit the moment, that one paid the work — you do not debate it. You have seen the accounts. Food tasted of food when paper stayed out of it. Pause cleared the head by standing and looking away. Company held by voices and faces, not by what burned between fingers. Night air went all the way down without catching. The rider only hired the hour and taxed the next.

So keep what you carry in view. The promise held. The seeing held. The sentence holds: All you have to do is follow all the instructions.

### WHAT YOU LEFT BEHIND

We lived for years inside the nicotine trap. We did not choose it daily. We were conned into the first ones on phoney information, then the trap removed the choosing and sold it back to us as pleasure.

We fed the Nipper with every dose. Small creature. A puff fed it for minutes, then it asked again. We mistook its asking for hunger, for nerves, for need of company. It was only asking to be fed.

We lived behind the Smokescreen that called a dose a friend, a pause, a reward. That smoke told us the tube steadied the hand after the row, paid the finished paragraph, seasoned the night. The row sat untouched after the ash fell. The paragraph was work done well. The night was sun, leisure, company. The tube was only sneaking a ride.

That hollow in the chest was only an empty, slightly restless, slightly edgy little tug. Not grief. Not need of leaf. The tug of a dying ask.

It does plenty TO you. It does nothing FOR you. Yellow on the fingers, sour under mint, cough to earn the day, arithmetic at every till — plenty TO. Calm that left the problem papers exactly where they lay, taste shortened at the crust, air cut short on the stairs — nothing FOR.

It never fixed the itch. It caused it. Each dose quieted for minutes the want the last dose had lit, then guaranteed the next low.

Look back at how we stood outside doorways in rain: stale, breathless and chained. Warm to us, always — we were trapped, not weak — harsh to the need that made us hide from partner and kids and spray the coat before hello.

That pull from both sides was the tug-of-war of fear. Fear of lighting for life. Fear of life without lighting. Both ropes were held by the same hands. When the credit moved, both ropes fell at once.

We all knew the hiding. Febreeze on the coat, mints in the pocket, garage door half up, window cracked while water boiled behind. A divided self: daylight talk inside, yard habit outside. Choice would never need hiding. A trap does. We hid because we were caught, not because we were bad.

We all knew the counting. Will this box last the evening, will I need to come back in rain, where will I stand to blunt the walk home. Arithmetic at every till. The shelf behind the till glowed with printed boxes in a row and we read that glow as provision. It was a timetable. Milk, bread, change, door — that was provision. The box only hired the walk and soured the mouth underneath.

I do not blame us for the years. We were not weak-willed. We were wilful enough to persist in something that went against every instinct — breath, taste, money, time, hiding — because the smoke told us we needed it. Strong will, wrong address. Now the address has changed.

Leave that doorway in memory where it belongs. You do not need to revisit it to prove anything. The proof is in the kettle, the cup, the queue, the pan, the phone, the programme, the window, the bed. All lived through edge to edge, with nothing burned out of the middle.

### THE TABLE AND THE TRAY

Remember that farewell table where you stubbed the last tube with full attention on the stain and the ash and the stale end.

No laboratory tasting. No extra smoke to prove anything. You looked at what was actually there, you finished it, you put it out. The room smelled of garlic and washing liquid again.

Here is what that table showed, plain:

the ashtray was already empty — you were the one who kept refilling it, and now you have put the habit down like a borrowed coat that was never yours.

A borrowed coat never kept you warm. It hung heavy, smelled of other rooms, made you check the pockets before you could leave the house. You wore it so long you thought it was your shape. It was never your shape. Your shoulders, your hands, your tongue, your breath were yours before the first dose and are yours now.

Wash the tray. Put it high on the shelf. Let it sit there empty. It needs no hiding and no guarding. It is glass. You are done with refilling it.

I washed mine and put it up where I see it when I reach for a bowl. Not as a test. As furniture. Glass does not ask. The shelf holds bowls, jars, a chipped jug for spoons. The tray sits among them with nothing in it. Some days I do not notice it. Some days I notice it and grin. Both are fine. Noticing and not noticing both say the same thing: nothing is owed.

That table was ordinary. Plate pushed aside, cup in reach, light on over the cooker. You did not dress it for ceremony. You paid attention. Yellow stain, grey ash, sour end. The paper did not season the hour. The hour seasoned itself — supper cooked, kitchen warm, house ticking as houses tick when heating cools. You put the tube out and the hour stayed whole.

Keep that picture. When a faint tap comes later, hold it beside the tap. Stain, ash, sour end beside hollow, offer, old line. One is what was there. The other is smoke talking. You know which is which because you looked with open eyes at the table and saw.

### THE CARD ON THE FRIDGE — FIRST SIX

Photograph these. Keep them where the eye lands while the kettle boils.

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

### THE CARD ON THE FRIDGE — SECOND SIX

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

### MORNING KETTLE WITH THE CARD IN VIEW

Live those rooms all the way through. Wash the cup. Wipe the counter. Put the coins in the dish.

Tomorrow the alarm goes. Light at the curtain. Feet to the cold lino. The card sits on the fridge at eye level while the kettle clicks.

You fill the kettle, switch it on, stand while it warms. No patting of pockets before you stand. No counting in the box to see if there are enough to get you to the shops. The pocket holds keys, phone, coins. Nothing else rides beside them.

The kettle clicks off. You pour. Steam lifts off the cup and touches your face. You hold the cup with both hands. The hands lie still round the warmth. They do not tap, they do not hunt, they do not shield anything from wind. They hold.

Take the cup to the window. Open the crack a finger's width. Morning air comes in. Drink. First sip tastes of what is in the cup. Second sip tastes of what is in the cup. Tongue clear from sleep and staying clear. Toast goes in. Butter melts into the holes. Bread, salt, butter to the crust. For years the edges shortened under sour. This morning nothing shortens.

Read the card while you drink. Not as study. As a glance. KEEP AN OPEN MIND. You did. DON'T STOP OR CUT DOWN YET. You kept to that while you read. BEGIN BY FEELING GREAT TO BE ESCAPING. No doom here. FOLLOW ALL THE INSTRUCTIONS. That sentence carried you to the table where you put the last tube out.

A faint hollow taps after the kettle clicks and says, hold something. Hear it with clear eyes. It is an empty, slightly restless, slightly edgy little tug. Not a command. Not you reasoning. The old script talking, pre-labelled. Let it come, name it for what it is, and I grin inside and say YIPPEE! I'M FREE!

Say it at the window and feel how true it is. Mean it from the belly. The thought arrives, the shout answers, the moment proves itself whole.

Wash the cup. Hot water, cloth, upturn on the drainer. Wipe crumbs into the palm, tip them in the bin. Wipe the counter. Small jobs taking a minute, and the minute is whole. No hand reaches for the tray while the other wipes. No thought of stepping out to the step while toast cools. Toast does not cool while you are gone, because you are not gone.

Dress. Keys, phone, coins. Pull the door. Hall smells of soap and toast. Coat smells of cupboard and rain from yesterday. It does not smell of last night's doorway.

Walk to work, to the bus, to the car. Pavement damp after rain. Bins out. Kitchen fan humming somewhere. Breathe through the nose and the air goes all the way down without catching. No cough to clear a path for it. Chest asks for nothing first.

This is the second kettle, and the third, and the twentieth. Each proves what the first showed. Body wakes the way it woke before the first tube you ever lit: thirsty for water, hungry for food, glad of light. Leaf only borrowed that gladness and charged for the loan. Now no loan runs. Pour, hold, drink, eat, wash, dress, go.

### THE SHOP, THE TILL, THE WALK HOME

You step in for milk on the way home. Bell over the door pings. Strip light hums. Queue shuffles forward in coats.

The shelf behind the till glows with printed boxes in a row. You see them because they are there. The person ahead asks for his brand. Assistant turns, slides the box across, takes the coins. Plastic wrap crackles. Faint stale sweetness off his coat as he passes to the door. You remember wearing that smell. We all wore it.

You stand with your milk in your hands. Carton cold through fingers. Pocket holds keys, phone, coins. No box soft at the corners. No timetable ticking toward the next doorway.

Pay. Take change. Feel coins warm in the palm for a second before they go back in the pocket. Walk out with open hands. Bell pings behind you.

Notice how short the errand is when no second errand hides inside it. In the old days the shop was never just the shop. It was the shop plus the check: will this box last the evening, will I need to come back in rain. We did arithmetic at every till. You do no arithmetic now. Milk, bread, change, door. Pavement outside is the same pavement. Walk home leaves toothpaste and cold air in the mouth, and nothing sour underneath.

I did that walk for years with the first one lit outside the door. First pull to take the edge off the sour the last one left. We called the edge fresh air and blamed the street. You walk it now with nothing lit and nothing blunted, and the street is only the street: traffic, wet leaves, somebody's chips, rain coming on.

Read the card again on the fridge when you get in. REFUSE TO BE INFLUENCED BY OTHER SMOKERS. Watch them with clear eyes and keep your own judgment. TRUST YOUR BODY TO BREATHE AND TASTE. Your tongue told you at the window this morning. SEE THE SELLER BEHIND THE SMOKE. That glow behind the till was built to glow. Remember who built the trap and why, then put the milk in the fridge and get on with the pan.

Put the milk in the fridge. Put the bread in the bin. Put the coins in the dish by the door. Kitchen as you left it this morning. Cup upturned, counter wiped. No tray to move aside before you can chop. No ash dusting the rim of anything.

If a tap comes at the till — memory of buying, hand remembering the slide of the box — hear it as script. Pre-labelled. Not you reasoning. Name it, pity the huddle outside the doorway that still answers it, and answer from the belly: YIPPEE! I'M FREE!

That shout is yours to keep. Thought arrives, shout answers, errand stays whole.

### THE DOORWAY, THE WORK, THE BUS

Mid-morning the screen blurs. Mid-afternoon the phone goes down hard. Shoulders up round the ears. Head full.

Stand. Stretch. Arms up, neck rolled, back cracked. Walk to the doorway with a cup or with nothing at all.

Cold air on the face. Street sounds go on. Traffic, pigeons on the wire, shutters of the shop across half down. Lean on the frame. Watch light change on brick opposite. Drink tea tasting of tea. Do nothing for ten minutes that needs a name.

I took these pauses for years with paper and without, and I tell you what stayed. What made the pause sweet was standing, moving, looking away, letting the head clear while the body breathed. Papers sat inside exactly where you left them, whether you burned something in the doorway or not.

Keep the pause and let paper stay out of it. Go back in when ready. Sit. Meet papers with hands that can type, lift, hold. Head clearer because you stood and looked away, not because anything was lit. Shoulders drop because you rolled them on the way to the door.

We all called that doorway a break and thought the break had two parts: legs plus light. It had one part. Legs. Air. Looking away. The light only hired out the ten minutes and charged you the next fifty wanting the next hire.

Your ten minutes now are not hired. They are yours from edge to edge. Spend them watching clouds cross an aerial, hearing the kettle in the office kitchen click off, feeling the cup warm your palms. Then spend the next hour on the work itself, with no eye on the clock for when you can step out again. Clock is only the clock. It tells you when lunch is, when the post comes. It does not tell you when you may breathe.

The last hour comes the way the middle hours came. Light thinning at blinds. Chairs scraping. Printer coughing out last pages. Finish the piece you are on. Do not leave it half-done to slip out and come back dulled. Stay with it to the end of the paragraph, to the end of the column, to the knot in the wire tied off properly. Save. Close the lid. Stack papers square. Put folder back on the shelf where it lives. Twelve minutes belonging to the work itself. No part of you already outside while hands tidy inside.

Wash the mug. Hot tap, brush, upturn on the rack beside others. Wipe your square of desk. Push chair in. Small lift in the chest when a desk is left clear for tomorrow. For years we cut that lift short. We cleared in a hurry, coat half on, bag over shoulder, eyes on the door, because the box in the pocket called the next move. Desk got a shove, mug left filmed, folder left open. Tonight nothing pulls from behind. Desk left as you like to find it.

Coat on. Scarf wound. Bag packed. Say goodnight to the room. Someone at the next desk lifts his head and says he is stepping down to the yard. Nod and smile and keep lacing shoes. We all knew that nod from the other side. Quick arithmetic behind eyes, counting who is going, whether enough time before the bus, whether rain too hard. You do no arithmetic. Zip the bag. Pick up the milk list from under the paperweight. Walk to the stairs with him as far as the landing and part at the push-bar without a second thought.

Push the bar. Door gives. Outside air meets you all at once. Dusk coming down blue over the car park. Wet tarmac shining under lamps. Sound of tyres on the far road. Bus shelter with scratched plastic glowing. Walk across with collar up. Steps making small splashing sound they always made in November. No hand goes to the pocket on the way across. No stop under the canopy to light before the walk to the stop. Walk to the stop is only the walk to the stop.

Bus comes with windows fogged. Tap and climb and take the seat over the wheel where you can see out. Heater ticks under seat. Driver calls good evening to a woman with shopping. Doors sigh shut. Off past lit shops, past chip shop with fan blowing out, past school railings with leaves banked against them. Watch street go by without narrating it. Stop, start. Bell. Doors. Someone gets on shaking an umbrella. Someone gets off with a child asleep on his shoulder.

For years that ride had a frame round it too. One smoked fast outside work so the ride could be borne. One planned for the minute after getting off, lit at the shelter while bus pulled away. We rode with one eye on the timetable and one eye on the box, getting off a stop early when the want got loud so we could walk and burn at the same time, arriving home with cold fingers and a mouth that needed rinsing before hello. We called it winding down after work. It only cut the ride in two and taxed both ends.

Tonight the ride runs straight through. Sit to your stop. Feel warm heater at shins. Hear bell for your corner and stand when it rings. Down steps. Boots on wet pavement. Shop on the corner pulling shutter half down. Cat crossing under a car. Your street with lamps just lit and windows yellow behind curtains. Walk it without blunting it. Chips, rain, wet leaves, someone's coal fire. Mouth holds toothpaste from morning and cold from the ride, and nothing sour underneath.

Keys out before the gate. New small detail and you notice it because old detail is gone. For years hands at the gate performed same fumble: keys in one hand, tube in the other, bag slipping, trying to shield a glow in wind while turning a lock. Key missed. Bag slipped. Hello inside waited while you finished outside. Tonight one hand holds bag, other holds key. Key goes in first time. Lock turns. Hall light on. House smells of morning soap and bread left in the bin.

Push door shut behind with heel. Bag down. Coat off. Hook it. Thud of bag on mat and click of hook are the hinge the whole day turns on. Morning kettle to doorway pause to last hour to bus ride to this mat. None sliced out. None hired. Day has run from edge to edge into one uncut length.

If a tap comes on the bus — seat over the wheel where you used to plan the shelter light — hear it as script. It never fixed the itch. It caused it. The thought arrives, the shout answers: YIPPEE! I'M FREE!

### SUPPER, PHONE, EVENING STRETCH

Evening comes the way it always came. Bag down. Coat off. Fridge open. Light on over the cooker.

Chop. Onion, pepper, garlic. Board thumps under knife. Oil heats and spits. Stir and steam lifts pepper into nose and makes you sneeze once. Laugh at yourself. Taste sauce off spoon. Salt. Heat. Tomato. Add pinch more salt and taste again. Taste there from first lick to swallow, with no fur on tongue to rinse through.

For years supper had a frame round it. One before to mark end of work. One after to mark plate done. We stood at the back door while pan cooled and sauce skinned, blowing thin smoke into dark while food waited and dulled. We called those the meal ones and said they rounded the food. They only interrupted it and taxed taste at both ends.

Tonight no frame. Pan, spoon, plate. Carry plate to table. Sit. Eat while hot. Hear fork on plate. Mop last sauce with bread and bread tastes of bread and sauce to last bite. Push plate away and taste stays clear behind it.

Phone rings. Old hour for old call: mate, brother, mother, voice that used to mean stepping out with cordless to yard while plate sat and voice half-listened through pulls.

Answer at the table. Stay at the table. Talk with plate pushed aside and cup in reach.

“How are you doing then?”

Tell him about the day. Bus late. Queue. Sauce just made. Listen about his boiler, his kid's teeth, match on Saturday. Call lasts twenty minutes. Your end all there. No stepping out mid-sentence to stand in rain. No holding phone with shoulder while other hand cups and shields. No coming back in with thread lost and asking him to say it again.

I know those yard calls. We all made them. Half an ear on voice, half an ear listening for pull to finish, coming back in with cold fingers and sour mouth and pretending we had heard. Tonight you hear. Tonight you are where the voice thinks you are: at table, unhurried, with nowhere to get to before call ends.

When you hang up, kitchen still warm from cooker. Plate waits to be washed. Nothing else waits. No box to check. No last one before bed to fit in. Evening has not been divided into before and after. It has run straight through, pan to plate to phone, and hours left to spend as you choose.

Wash plate. Hot water, brush, rack. Wipe board. Put knife back in block. Put leftovers in tub for tomorrow. Evening jobs close the meal the way lid closes pan. No tray to empty. No window to open wide to clear room before sleep. Room smells of garlic and washing-up liquid. That is what a kitchen smells of after supper when nothing has been burned in it.

Seven to ten used to be timetabled. We knew the timetable by heart. One after supper. One with the programme. One in the adverts. One before bed to see us through the night. We watched the clock more than the screen, shifting in the chair as hour hand moved, timing trip to door so we would not miss the turn.

Tonight clock is only furniture.

Sit. Programme comes on. Watch it all the way through. Nobody pauses you from inside. Nobody leans you toward the door in the adverts. Adverts come and go and you get up for water because you want water, not because water is an excuse to stand where paper can be lit.

Notice the chair. Sit in it differently. Not perched on edge ready to rise. Not twisted to keep one eye on pocket. Sit back. Feet up. Cup at elbow. Hands empty in lap or round cup. For years those hands performed a hundred small jobs in an evening: patting, flicking, shielding, hunting trays, holding mints, spraying coats before bed. Watch how quiet they are now. They lie still. They do not miss the work.

Later walk to the window before bed. Open it a crack. Smell the night. Rain, bins, cold stone. For years window was a place to blow smoke through while listening for footsteps in hall. Now a place to breathe through. Difference not small in living, though only a second to do: mouth empty, chest open, night coming in.

Lock window. Turn latch on door. Turn off front room light. House ticks as houses tick when heating cools. No last check of box by bed. No glass of water put out to rinse a morning mouth you already know will be sour. Morning mouth will be clear because night mouth is clear.

This is what untimed time feels like from inside. Not grand. Not loud. Just uncut. Evening running from supper to bed without being sliced into hourly hires is longer than you remember evenings being. Get to end of programme and still time to read ten pages. Read ten pages and still time to stand at window. Stand at window and still time to write list for tomorrow. Hours have not stretched. They have stopped being taxed.

If a tap comes in the adverts — old cue to step out — hear it as script. MEET THE BEST CIGARETTE HEAD-ON. Let the favourite prove it gives nothing. It does plenty TO you. It does nothing FOR you. Thought arrives, shout answers: YIPPEE! I'M FREE!

Teeth. Face. Socks off. Light off. Bed cold at edges and warm in middle where you lie. Pillow smells of pillow. Mouth tastes of toothpaste and nothing underneath. For years last taste before sleep was sour under mint, and first thought on waking was where box sat. We slept with a timetable beside the bed and called it habit.

Lie now with nothing beside bed but water and alarm. Body settles. Shoulders, hips, jaw. Day runs back through head without being searched for gaps: kettle, bus, queue, doorway, pan, phone, programme, window. Every room occupied all the way through. Nothing stepped out of. That is why day feels longer in memory and shorter in living. You were in it throughout.

Sleep comes the way sleep comes when nothing is asking. Breath slows. Thoughts thin. Street goes quiet outside and then louder once as a car passes and then quiet again. Turn on side. Hands rest open on sheet. They do not reach in sleep. They have nothing to reach for.

### THE OPEN DOOR TO THE STREET

Morning comes. Alarm. Light at the curtain a shade paler than yesterday. Feet to lino. Kettle on.

Second kettle proves what first showed. Tongue clear from sleep. Cup in open hands. Toast tasting of toast to crust. Pocket with keys, phone, coins. Door pulled with hall smelling of soap. No cough to earn the day. No hunt before water boils. Live second morning the way you lived first. Pour, hold, drink, eat, wash, dress, go. Shop will open when you pass it. Doorway at work there when you need air. Supper waits in fridge as leftovers in tub. Phone may ring at table again. Evening will run uncut again. Bed cold at edges and warm in middle again.

Day after day. Not counted. Not measured toward some distant point where you will finally be something. You are something now, and days only show it more plainly as they pass.

Saturday comes with its own test. Laugh across a patio table with glasses sweating is planned, and someone asks who is coming. You type back with both thumbs. Coming. No small calculation about where you will stand over there, whether you will need to bring enough, whether you will have to slip away mid-laugh. You will sit at the table for as long as the laugh lasts, and get up when the laugh is done.

On the night, friends, drinks, laughter, tray of lights, hand extending with one won't hurt. Hear both with clear eyes. Neither is you reasoning. Both are old script talking, pre-labelled.

We all heard that script for years and mistook it for our own voice. We said the stick seasoned the night, paid the finished paragraph, steadied the hand after the row. Night was sun, leisure, company. Paragraph was work done well. Row still there after ash fell. Tube only ever sneaking a ride on kettle, food, pause, company, night air. Kettle, food, pause, company, night air remain. Rider gone.

When thought crosses mind now, do not argue with it and do not try to not think it. Let it come, name it for what it is. NEVER ALLOW JUST ONE OR A SPECIAL ONE. One keeps the trap alive. SMOKE YOUR FINAL CIGARETTE AND KNOW YOU ARE FREE. You closed the trap with joy at that farewell table, not sadness. The tray sits washed and empty on the shelf. The borrowed coat stays put down.

Watch smokers huddle outside a doorway with pity, not envy — they are still timed, still soured, still divided between daylight talk and yard habit. It does plenty TO you. It does nothing FOR you. You are not missing. They are.

I stood where you stand now, with empty pocket and clear tongue, and I tell you the street outside is only the street. Traffic, wet leaves, chips, rain coming on. Yours to walk without blunting.

Push the bar. Open door to street. Walk into next ordinary hour with empty hands, clear tongue and pocket with no timetable in it. Supper, phone, bed, next light — all yours, all whole, all lived through to the edge.

Now get on with enjoying your life.

YIPPEE! I'M FREE!

**SUMMARY**
- The promise held: nothing was lost and the change was by seeing, kept by keeping the instructions in view.
- The trap is left behind: the small feeder starved, the smoke that fed it cleared, the hollow named for what it was.
- The ledger is closed: plenty was done TO the body and breath, nothing was ever done FOR calm, taste, work or company.
- The itch answer holds: the dose lit the want it briefly quieted, and the old torn feeling belonged wholly to the trap.
- The former state is past: timed, soured and divided days have given way to mornings, shops, pauses, supper and sleep lived through edge to edge.
- The table proved it: the tray sits washed and empty, refilled no longer, the borrowed coat put down.
- The twelve lines stay on the fridge as photographed, to be read as written and kept as spoken.
- Any faint tap or offered pack is the old script talking, answered at once with YIPPEE! I'M FREE!
```
