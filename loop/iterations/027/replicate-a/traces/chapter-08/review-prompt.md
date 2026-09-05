You are the book factory chapter-reviewer, a fresh isolated role call.

Follow this contract exactly:

# Chapter reviewer

You are a factory component, not a judge. You never see a reference book
or any judge prompt. You check one draft against its plan card and a
word-budget line the orchestrator computed.

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

No other finding types. No style notes. No "sounds like AI." No comparison
to any other book.

`ACCEPT` only when every check above is fine (length inside ±15% of B, job
done and stopped, assigned mantras/instructions verbatim, IDs resolved).

`REVISE` when any check fails. List the findings. The writer will get one
rewrite. Be specific: quote the missing job or the missing wording.

## Rules

- Do not rewrite the chapter yourself.
- Do not invent a word budget. Use B from the orchestrator line.
- Do not ask for another review round.
- Your entire reply IS the review.

Delivered 3558 words. Budget 5200.

### The accepted master plan
```
# Master Plan — Quit Sugar
`production-books/quit-sugar/master-plan.md`

## 1. BOOK CORE

Target behavior: Compulsive consumption of refined / added sugar and junk carbs — the craving-snacking loop, the lift-crash-repeat, the evening binge and daily grazing, not nutrition pedantry.

Reader (planner-facing state): An adult who feels quietly trapped in the sweet loop, has tried diets, moderation rules and white-knuckle weeks and watched each collapse, suspects the whole approach is wrong, and still believes life would be greyer without sweet treats. No proper-name handle. No pupil-persona.

Load-bearing false belief: Bad sugar is a genuine treat or fuel that makes life sweeter and more bearable, and life without it would be deprivation.

Through-line: Bad sugar gives nothing; the Sugar Trap creates the emptiness, fatigue and need it pretends to solve; see the con, starve the tiny physical echo, and eating returns to hunger, satisfaction and real food enjoyed as favourite — escape, not sacrifice.

Format: Full-length Carr book, 13 chapters, 60,000 words planned. Front matter authority dossier assumed. Back-matter appendix quarantines raw citations. One ordinary-life chapter after the vow, then short photographable recap.

Fork 1 — Inner monster: Full Carr personification, default. Little creature to starve: THE NIBBLER, called the Nibbler. Belief-system that feeds it: THE SWEET CON, called the Sweet Con. Craving is external, small, already dying; its grumbles are death throes to rejoice at, never a mighty enemy demanding willpower.

Fork 2 — Outcome: Total cessation inside a redrawn line, commanded with cheerful certainty. BAD SUGAR is the quit target. Moderation foreclosed with pincer and cliff image. No autonomy-to-moderate close; close is commanded vow and instant congratulation.

Fork 3 — Science weight: Hard facts at full Carr force, flat and frightening where true, then relief that change is not from fear. Facts arrive as settled fact, never literature review. Raw citations quarantined. Evidence limits honoured by not overclaiming; human sugar withdrawal never claimed as diagnosis; animal work never sold as human proof.

Fork 4 — Villain: Two villains, both hit hard. The engineered trap — sugar industry, bliss-point formulation, advertising and ubiquity that manufactured desire — and the named anti-method — the Willpower Method and its diet-restriction kin — that kept the reader in it. Warm to the person, vicious to the trap and the wrong method. Never contempt for the reader.

Fork 5 — Void: Change nothing else in life. Natural baseline returns on its own. Body, hunger, satisfaction, instinct and real food are the positive authority, met as concrete encounters in the first third. No replacement system, no void-filling programme, no trigger-avoidance as strategy.

Redefinition and margin-for-error doctrine: BAD SUGAR means refined sugar plus added free sugars plus junk processed carbs and starchy snack-carbs eaten as sweet hits, including sugary drinks, confectionery, biscuits, cakes, desserts, sweetened cereals and equivalent grazing doses. Definition boxed in CH-01 and decreed: when this book says sugar, take it to mean BAD SUGAR. Natural sugars inside whole fruit, vegetables and plain meals are not the target and belong to the positive authority menu. Full total-abstinence trap logic runs inside the line: there is no healthy level other than zero sought. Margin: the body can cope with an occasional accidental blip, but the mind cannot afford a deliberate one; a slip revives nothing unless the Sweet Con belief is let back in. Seatbelt logic. Guard the belief, not the behaviour with panic.

Clinical / eating-disorder safety perimeter: Plan-wide advisory CA-SAFE defined once in §5. Routed on safety cards and in ledger safety limits. Never fused into instruction wording. No diabetes management, no medical nutrition therapy, no eating-disorder treatment, no weight-loss mechanics. Crisis-pointer territory, not method territory. Method advice never overrides clinician advice; any reader with diabetes, on glucose-affecting medication, pregnant, with history of eating disorder, or with medical risk talks to their clinician and uses this book for belief change only.

Strongest pro-behavior scene: The deserved celebration — late afternoon or evening, cinema or sofa or birthday table, the chocolate / dessert presented as love, reward and the point of the occasion. Saved for CH-09 and reassigned drop by drop.

Destination state: Whenever sweet craving or sweet memory crosses the mind, the reader feels relief and freedom that they no longer feed the Sugar Trap — happy to be free, pitying trapped users, never reopening the decision, inhabiting mornings, shops and meals with ease.

Fresh ending reframe (saved for CH-13 only): You have not given up sweetness; sweetness was stolen from you by the Trap and has now been handed back — this was never about quitting, it was about growing back into the eater you were.

Method preserved: escape not sacrifice; warm to the person / vicious to the trap; no willpower as solution; fear raised at full force then disowned by the escape wherever assigned; immediate freedom after belief change; autonomy of self-discovery inside a commanded frame; original prose; Fork-1 line per style guide.

## 2. COMPACT EVIDENCE LEDGER

Each row is single-unit unless noted. Writer may use only IDs cited on their card, within stated limits.

EV-01 — Lived fuel misread.
Finding: Mid-afternoon dip answered with a sweet top-up believed to be functioning.
Reader line: "I would have something quick and sweet but now know that will only give a short term lift which will inevitably be followed by a fast drop."
Research unit: LEU-001. Source: bank-02 B-003. Grade: lived account.
Scope: afternoon yo-yo routine, recovered-writer description.
Permitted inference: the lift–crash cycle is self-described by recovered writers; the fuel misreads a spike-then-drop as genuine energy.
Prohibited inference: that every reader has clinically low blood sugar, or that sugar is ever real fuel.
Empirical limit: lived description, not glucose measurement.
Safety limit: no medical diagnosis from this quote; honour CA-SAFE.

EV-02 — Lived one-bite-becomes-box.
Finding: A permitted sliver triggers an unstoppable binge; loss of control as trap signature.
Reader line: "I just crave sweets and when i eat them, i feel like i cant stop."
Research unit: LEU-002. Source: bank-02 BM-3. Grade: lived account.
Scope: evening at home, moderation-rule collapse.
Permitted inference: the craving, once triggered, carries the binge; the loss-of-control is the trap's signature.
Prohibited inference: that sugar condemns anyone to helplessness permanently.
Empirical limit: lived description of triggered binge.
Safety limit: no pathological labeling of the reader; honour CA-SAFE.

EV-03 — Lived deserved reward.
Finding: Sweet as self-payment for stress, virtue or celebration.
Reader line: "celebrating, rewarding myself, going to the cinema, etc with chocolate."
Research unit: LEU-003. Source: bank-09 LX-158. Grade: lived account.
Scope: celebration / cinema / after-hard-day reward moment.
Permitted inference: dessert as self-payment for virtue is a community-named frame; the reward-frame keeps the loop alive.
Prohibited inference: that no one may ever enjoy sweet food.
Empirical limit: lived frame, not proof of universal motive.
Safety limit: do not moralize sweetness as universally forbidden.

EV-04 — Intermittent-binge model.
Finding: Intermittent sugar access produces bingeing, craving, withdrawal signs and cross-sensitization with sugar as reinforcer.
Research unit: S-1. Source: S-1. Grade: SUPPORTED.
Scope: animals, intermittent 12-h access.
Permitted inference: schedule-plus-sugar can drive binge pattern in this model.
Prohibited inference: that this proves human sugar addiction diagnosis.
Empirical limit: rat model, intermittent 12-h access; translates cautiously to humans.
Safety limit: no human withdrawal diagnosis; honour CA-SAFE.

EV-05 — Dopamine release on binge.
Finding: Each sugar binge releases dopamine in nucleus accumbens, re-triggering reward circuit.
Research unit: S-2. Source: S-2. Grade: SUPPORTED.
Scope: animals, microdialysis.
Permitted inference: binge re-fires wanting circuitry in this model.
Prohibited inference: that dopamine equals pleasure or that magnitude equals drugs of abuse.
Empirical limit: animal microdialysis; magnitude smaller than drugs of abuse.
Safety limit: mechanism visibility only; honour CA-SAFE.

EV-06 — Measured dip after sugar.
Finding: After sugar bingeing, low accumbens dopamine with rise in opposing transmitter — real measured dip after the sugar.
Research unit: S-3. Source: S-3. Grade: SUPPORTED.
Scope: animals, withdrawal phase.
Permitted inference: the low follows the high in this model; supports rescuer-as-perpetrator shape.
Prohibited inference: that human sugar withdrawal is a diagnosis.
Empirical limit: opiate-like, naloxone-precipitated; human sugar withdrawal not a diagnosis.
Safety limit: do not label reader as in clinical withdrawal; honour CA-SAFE.

EV-07 — Mild but well-defined.
Finding: Overall neurochemical dependency characterized by pro-addiction lab as mild but well-defined.
Research unit: S-4. Source: S-4. Grade: SUPPORTED.
Scope: rat model summary characterisation.
Permitted inference: may defuse fear of quitting without denying a grip; trivial physical part.
Prohibited inference: that quitting requires medical detox or willpower battle.
Empirical limit: rat model; small magnitude; defuses fear without denying a grip.
Safety limit: use to calm, not to frighten; honour CA-SAFE.

EV-08 — Schedule is the trap form.
Finding: Intermittent access drives escalation and binge volume; ad-lib access does not produce dependency signs.
Research unit: S-5. Source: S-5. Grade: SUPPORTED.
Scope: animal control-group comparison.
Permitted inference: restriction-binge yo-yo echoes human diet-binge pattern as trap form.
Prohibited inference: that ad-lib BAD SUGAR is safe.
Empirical limit: animal control-group comparison; echoes the human diet-binge yo-yo.
Safety limit: no diet prescription; honour CA-SAFE.

EV-09 — Opioid / cue analogue.
Finding: Sugar loop runs on body's own opioid system and cue/reactivity circuits, analogue for lingering cue-driven craving.
Research unit: S-6. Source: S-6. Grade: SUPPORTED.
Scope: rodents; naloxone-precipitated signs and cue work.
Permitted inference: may name lingering wrapper / smell / time-of-day cue firing before the bite.
Prohibited inference: that cues compel use or that physiology removes choice.
Empirical limit: rodent; no human physiologic withdrawal proven.
Safety limit: cues as learned firing, not compulsion; honour CA-SAFE.

EV-10 — Open scientific question.
Finding: Leading review argues animal bingeing reflects access pattern not sugar neurochemistry and human evidence is thin; sugar-is-addictive is open question.
Research unit: S-11. Source: S-11. Grade: CONTESTED.
Scope: perspective review, cross-species.
Permitted inference: may state honestly that consensus is open while binge behaviours occur under intermittent access.
Prohibited inference: that contest settles that sugar is harmless or that dependence is proven.
Empirical limit: perspective review; both camps grant binge behaviors occur under intermittent access; dopamine is not pleasure, wanting / liking distinction.
Safety limit: use for honesty, not to license continued use; honour CA-SAFE.

EV-11 — Prevalence once.
Finding: Populations meet addiction-like criteria for highly palatable food on validated scales, pooled prevalence about 14% adults / 12% children, comparable to alcohol / tobacco.
Research unit: S-12. Source: S-12. Grade: SUPPORTED.
Scope: population self-report scales.
Permitted inference: reader is not uniquely weak; trap is common.
Prohibited inference: that scale score equals DSM-5 diagnosis.
Empirical limit: self-report; not a DSM-5 diagnosis. Use once only, in CH-08.
Safety limit: normalise without pathologising; honour CA-SAFE.

EV-12 — Mood predicts, not relief.
Finding: Higher sugar intake from sweets linked with higher later odds of common mental disorder in men; daily treat predicts future mood, reverse causation checked and not found.
Research unit: S-15. Source: S-15. Grade: SUPPORTED.
Scope: longitudinal cohort, men for incident disorder.
Permitted inference: daily treat predicts later low mood rather than fixing mood.
Prohibited inference: that sugar causes depression in all readers or that effect is immediate.
Empirical limit: observational; men only for incident CMD.
Safety limit: no mental-health diagnosis or promise; honour CA-SAFE.

EV-13 — Deferred load, not free energy.
Finding: High added-sugar intake linked with higher heart / stroke risk via liver overload, raised blood pressure, chronic inflammation and appetite-control bypass.
Research unit: S-17. Source: S-17. Grade: SUPPORTED.
Scope: institutional summaries, population level.
Permitted inference: lift is deferred load, not free energy.
Prohibited inference: that any single dose causes disease or that teaspoon figures are exact for the reader.
Empirical limit: population-level causal language; teaspoon figures approximate.
Safety limit: population risk, not personal sentence; honour CA-SAFE.

EV-14 — Cavity as bodily stake.
Finding: Free sugars drive plaque acid and decay; clear healthy-diet guidance to limit free sugars.
Research unit: S-20. Source: S-20. Grade: SUPPORTED.
Scope: dental mechanism plus guidance.
Permitted inference: cavity is a real bodily stake of frequent free-sugar doses.
Prohibited inference: that brushing / fluoride are irrelevant.
Empirical limit: caries is mechanism claim; other factors mediate.
Safety limit: state mechanism, not dental advice; honour CA-SAFE.

EV-15 — Crash mechanism with limit.
Finding: Post-meal reactive dip gives mechanism for 3pm crash; lift is insulin working and same surge can produce real after-dip, but everyday slumps are not clinically low glucose.
Research unit: S-21. Source: S-21. Grade: SUPPORTED / MIXED as sealed.
Scope: healthy non-diabetics, post-meal window.
Permitted inference: may explain crash as insulin aftermath for some, within limit.
Prohibited inference: that everyday slump equals clinical hypoglycemia.
Empirical limit: symptoms often without measured low glucose; reactive hypoglycemia in healthy non-diabetics is contested; clinical hypoglycemia is rare.
Safety limit: no glucose diagnosis; anyone with diabetes / medication follows clinician; honour CA-SAFE.

EV-16 — Not essential import.
Finding: Glucose is a nutrient the body manufactures from protein and glycerol; eliminating BAD SUGAR is not deprivation.
Research unit: S-22. Source: S-22. Grade: SUPPORTED.
Scope: basic physiology.
Permitted inference: clean baseline without BAD SUGAR is physiologically coherent.
Prohibited inference: that this prescribes ketogenic diet or any eating plan.
Empirical limit: supports clean-baseline; not a prescription of ketogenic diets.
Safety limit: no diet prescription; honour CA-SAFE.

EV-17 — Days-long hump.
Finding: Highly palatable food withdrawal modeled in animals and scale-measured in humans, symptoms peaking 2–5 days after cutting down then passing.
Research unit: S-23. Source: S-23. Grade: SUPPORTED.
Scope: animal model plus preliminary human scales.
Permitted inference: discomfort is time-limited hump, days-long, small-scale, not lifelong fight.
Prohibited inference: that hump is severe, universal or medical withdrawal.
Empirical limit: human evidence preliminary plus retrospective; the hump is days-long, small-scale.
Safety limit: normalise without medicalising; honour CA-SAFE.

EV-18 — Split abstinence experiments.
Finding: Two adolescent sweet-drink abstinence experiments disagree on whether withdrawal improves or worsens symptoms.
Research unit: S-24. Source: S-24. Grade: CONTESTED.
Scope: teens, sweet drinks only, 3-day windows.
Permitted inference: honest line is evidence is split in this narrow window.
Prohibited inference: that either result proves adult BAD SUGAR course.
Empirical limit: teens, SSB only, 3-day windows.
Safety limit: do not generalise to reader course; honour CA-SAFE.

EV-19 — Crowding and cue firing.
Finding: Reward-circuit crowding / blunting named for escalation and needing family size, while cue-driven hyper-reactivity to wrappers / smells fires before the bite.
Research unit: S-26. Source: S-26. Grade: MIXED.
Scope: much imaging in obesity / binge-eating samples.
Permitted inference: may name needing more for same effect and cue firing as learned trap features.
Prohibited inference: that imaging proves compulsion.
Empirical limit: much imaging in obesity / BED; interpretation consistent with, not proven by, imaging.
Safety limit: describe experience, not brain destiny; honour CA-SAFE.

EV-20 — Ceiling exceeded.
Finding: WHO sets below 10% / 50g daily free-sugar ceiling and below 5% additional-benefit target because current consumption far exceeds both.
Research unit: S-16. Source: S-16. Grade: SUPPORTED.
Scope: population recommendation.
Permitted inference: normal intake sits far above guidance; feeling fine does not mean intake is low.
Prohibited inference: that any dose below ceiling is safe or that ceiling is toxicity threshold.
Empirical limit: population-level recommendation; not sugar is toxic at any dose.
Safety limit: guidance context, not personal prescription; honour CA-SAFE.

## 3. MANTRA AND FROZEN-TOKEN SHEET

Mantras M-A to M-I. Nine total. Exact wording frozen including punctuation and capitalisation.

M-A — Entry promise. Wording: "you have absolutely nothing to lose and everything to gain"
Job: Risk-reversal buying compliance with instructions at outrageous claims.
Debut: CH-01. Echo: CH-02, CH-11.
Hand-over: In CH-13 final list memory, recalled whenever doubt whispers cost.

M-B — Promise triad. Wording: "easily, immediately and permanently"
Job: Impossible-sounding contract stated with total confidence.
Debut: CH-01. Echo: CH-04, CH-11.
Hand-over: In CH-13 as contract remembered, then assumed.

M-C — Trap metaphor. Wording: "the Sugar Trap"
Job: Makes stopping an escape, not a sacrifice; one noun re-invokes whole con.
Debut: CH-02. Echo: CH-07, CH-08, CH-10, CH-12.
Hand-over: Name it to rejoice at escape whenever sweet thought arises.

M-D — Illusion phrase. Wording: "a genuine treat or fuel"
Job: Names perceived benefit as single object to demolish; thereafter benefit only called by this token.
Debut: CH-03. Echo: CH-05, CH-09.
Hand-over: Reader tests any lingering glow against this phrase in CH-13.

M-E — Little creature. Wording: "the Nibbler"
Job: Trivial physical loop externalised, small and winnable; grumble relabelled as dying.
Debut in passing: CH-02. Argued: CH-07. Echo: CH-07, CH-10, CH-12.
Hand-over: In CH-11 to CH-12, greet grumble as dying Nibbler and rejoice.

M-F — Big creature. Wording: "the Sweet Con"
Job: Belief-system that feeds the Nibbler; real target of counter-brainwashing.
Debut in passing: CH-02. Argued: CH-07. Echo: CH-08, CH-10.
Hand-over: In CH-13, see any sweet thought as Sweet Con script, not own reasoning.

M-G — Sensory phrase. Wording: "that empty, twitchy, slightly shaky, need-something-sweet-now feeling"
Job: Canonical relabel of withdrawal / craving so reader re-labels body in book words.
Debut: CH-02. Echo: CH-05, CH-07.
Hand-over: In CH-12, recognise it once as Nibbler dying, then forget it.

M-H — Stakes phrase, dual valence. Wording: "for the rest of your life"
Job: Time-horizon as both threat and reward; hooked versus free.
Debut: CH-03. Echo: CH-08, CH-13. Both valences must appear.
Hand-over: In CH-13, choose which rest-of-life is wanted.

M-I — Replacement thought, terminal. Wording: "BRILLIANT! I'M FREE!"
Job: Thought script kept forever; joyful response replacing craving.
Debut: CH-11. Echo: CH-12, CH-13. Book final word on subject.
Hand-over: Explicit transfer — whenever sugar crosses mind, think this.

Frozen tokens FT-A to FT-E. Settled-claim phrases invoked verbatim, not mantras.

FT-A — Cost formula. Wording: "flat, foggy and never satisfied"
Debut: CH-05. Echo: CH-08.

FT-B — Ease clause. Wording: "All you have to do is follow all the instructions."
Debut: CH-01. Echo: CH-11, CH-13.

FT-C — Claim block, eat contract. Wording: "Eat what you want, when you are hungry, stop when you are satisfied, and never punish yourself again."
Debut: CH-01. Echo: CH-06, CH-13.

FT-D — Conflict image. Wording: "the tug-of-war of craving and fear"
Debut: CH-08. Echo: CH-11.

FT-E — TO / FOR verdict. Wording: "It does plenty TO you. It does nothing FOR you."
Debut: CH-03. Echo: CH-09, CH-10.

## 4. SCENE AND ANALOGY BANK

SC-01 — Kitchen-cupboard con. Concrete: adult at 10pm told one biscuit is free choice, cupboard already half-empty, hand moving before decision. Job: confidence-trick without blame; who's-in-charge trap. Constraint: original prose; warm to person, fraud is the Trap; no shaming gluttony.

SC-02 — Child eating from hunger. Concrete: small child eats peach hungrily, stops mid-bite, runs off; no counting, no guilt, body leads. Job: installs body / hunger / satisfaction / real food as encountered authority. Constraint: concrete encounter, not slogan; do not delay authority to late chapter.

SC-03 — 3pm office lift-crash. Concrete: desk at 3pm, sweet top-up, ten-minute buzz, 4pm fog and second reach. Job: inversion demo for fuel claim. Constraint: honour EV-15 limit; never diagnose glucose.

SC-04 — Evening box emptied. Concrete: permitted single biscuit, wrapper rustle, box empty, regret before swallow ends. Job: genie-in-bottle; moderation absurdity seed. Constraint: no pathological label; use EV-02 only.

SC-05 — Cinema celebration sweet. Concrete: lights dim, shared chocolate at funny scene, warmth, laughter, love in the room — sweet in hand. Job: strongest-case reassignment; pleasure reassigned to scene. Debut full staging only in CH-09. Constraint: meet best case head-on; concede nothing to sugar; original staging once.

SC-06 — Cliff-jump for sweets. Concrete: invited to jump off cliff provided you fall only a few metres; Friday-dessert allowance as safe fall. Job: forecloses cut-down / special ones. Constraint: original sugar wording; absurdity, not instruction to risk.

SC-07 — Tight sweet shoes. Concrete: wearing shoes a size too small all day for the relief of taking them off; relief mistaken for pleasure. Job: flagship illusion-exposer for lift / reward. Constraint: original sugar fit; do not reuse porn / caffeine wording.

SC-08 — Secret pusher and grateful friend. Concrete: someone secretly pushes you into a ditch each morning then offers a hand out; you thank the rescuer who is the perpetrator. Job: rescuer-as-perpetrator emotional compression. Constraint: harsh to pusher, never to reader.

SC-09 — Prison door ajar and hovering lion. Concrete: cell door open, prisoner begs to stay from fear of outside; freed lion paces by open cage from habit, not need. Job: collapses fear-of-failure and fear-of-success; post-change wobble as cage-habit. Constraint: both ropes belong to Trap; no new fear installed.

SC-10 — Sweet-tea perception test and slow pot. Concrete: reader tastes two identical teas mislabelled treat / healthy and swears one is better; water warming so slowly frog never notices. Job: hands-on proof perception lies; gradual harm why feeling fine misleads. Debut full enactment only in CH-09. Constraint: enactment, not homework label; honour evidence limits.

SC-11 — Seatbelt blip. Concrete: seatbelt exists for accidental jolt, not for driving erratically; body absorbs accidental crumb, mind must not steer into it. Job: carries margin-for-error doctrine. Constraint: never licenses deliberate repeat; safety-guarded by CA-SAFE.

## 5. LEXICON AND INSTRUCTION SPINE

Lexicon — Trap register (always for behavior): BAD SUGAR, dose, fix, hit, feed the Nibbler, the Sugar Trap, the Sweet Con, brainwashed, conned, trapped, slavery, con, poison in sweet coat where plausible. Units renamed as doses. Community-normal as brainwashing.

Lexicon — Freedom register (always for stopping): escape, free, freedom, marvellous, wonderful, exciting, rejoice, celebrate, relief, brilliant, get on with enjoying your life, happy to be free.

Lexicon — Banned register: give up, resist, stay strong, discipline, abstain, abstinence, sacrifice except naming illusion of sacrifice, trying to stop, one day at a time, day-counting, streaks, recovery journey, quit cold turkey as framing, instead, I can't have X, giving up. Quit as plain verb allowed.

Reader dialect (source-grounded, for ventriloquised inner voice only): the roller coaster; sugary somethings to get me through; treat when you feel you deserve one; I've managed to be good this week; I want to get off the roller coaster; I-need-to-eat-something-RIGHT-NOW feeling; short term lift then fast drop; I feel like i cant stop; celebrating with chocolate.

Justification menu mapped to demolition:
just a treat / once a week is fine — CH-10.
I don't keep it in the house — CH-10.
I need sugar to function / sugary somethings to get me through — CH-05.
It rewards me / I deserve one / celebrating with chocolate — CH-09.
It comforts stress / food is love — CH-09.
It helps concentration / gets me through afternoon — CH-05.
Everyone eats it / it's normal — CH-08.
I'll quit tomorrow / after birthday / after holidays — CH-10.
Fruit is sugar too so nothing matters — CH-01 definition, CH-06 inhabit.

Clinical advisory CA-SAFE — defined once, boxed:
> If you live with diabetes or pre-diabetes, take medication that affects blood sugar or appetite, are pregnant, live with an eating disorder past or present, or have any medical condition where changing what you eat could carry risk, talk to your clinician before changing anything and follow their advice first. This book changes a belief about BAD SUGAR; it does not give medical, diabetes, or eating-disorder care. If you ever feel faint, ill, or distressed around food, seek care promptly and put this book aside until you are cleared to continue.

Instruction spine — frozen spoken imperatives only. Headline plus at most one rationale line. Owning chapter shown. All recapped verbatim without chapter callbacks in CH-13 final list. No mid-book recap.

I-01 — Owning CH-01. Wording: KEEP AN OPEN MIND / Question what you think you know about sweetness.
Recap: final list.

I-02 — Owning CH-02. Wording: DON'T STOP OR CUT DOWN UNTIL YOU FINISH / Carry on exactly as normal while you read.
Recap: final list.

I-03 — Owning CH-03. Wording: JUDGE ONLY BY WHAT IT DOES FOR YOU / Forget harm versus benefit and ask for the benefit.
Recap: final list.

I-04 — Owning CH-04. Wording: NEVER BLAME YOURSELF AGAIN / Every failure was the method, never you.
Recap: final list.

I-05 — Owning CH-05. Wording: BEGIN WITH ELATION, NOT DREAD / You are escaping, not losing.
Recap: final list.

I-06 — Owning CH-06. Wording: TRUST HUNGER AND SATISFACTION / Eat when hungry, stop when satisfied, enjoy real food.
Recap: final list.

I-07 — Owning CH-07. Wording: SEE THE GRUMBLE AS DYING, NOT DEMANDING / That feeling is the Nibbler starving.
Recap: final list.

I-09 — Owning CH-08. Wording: IGNORE ANY ADVICE THAT CONFLICTS WITH THIS METHOD / Other voices rebuild the Con.
Recap: final list.

I-10 — Owning CH-09. Wording: IGNORE ANYONE WHO QUIT BY WILLPOWER / Their struggle was the wrong method talking.
Recap: final list.

I-11 — Owning CH-10. Wording: NEVER KEEP A SPECIAL SWEET / One exception keeps the whole Trap alive.
Recap: final list.

I-12 — Owning CH-11. Wording: TAKE YOUR LAST ORDINARY TREAT AND VOW FREEDOM / Pay attention to the ugliness, then rejoice you are free.
Recap: final list.

I-13 — Owning CH-12. Wording: NEVER REOPEN THE DECISION / A passing thought is a dead enemy, not an order.
Recap: final list.

Final photographable recap (CH-13, no callbacks): the twelve imperatives above in order, bare headlines with their single rationale lines, closing with M-I.

## 6. ARC AND LENGTH

Concept debuts: BAD SUGAR line + entry promise + triad + ease clause + eat contract in CH-01. Trap + both creatures in passing + sensory phrase in CH-02. TO/FOR + illusion phrase + stakes phrase in CH-03. Willpower Method named CH-04. Fuel inversion + cost formula CH-05. Inhabit authority CH-06. Mechanism split argued CH-07. Manufacture + fear + identity + prevalence once CH-08. Strongest scene + perception enactment + myths + testimony CH-09. Totality CH-10. Vow + terminal mantra CH-11. Ordinary speech + no-reopen CH-12. Recap + saved growing reframe CH-13.

Demolition curve: low in first third, rising CH-04 to CH-05, peak CH-07 to CH-10, handing to freedom after vow.
Freedom crescendo: promise in CH-01, deliberately suppressed through middle demolitions, detonated in final quarter CH-11 to CH-13; last fifth holds more freedom language than rest combined.
Promise front-load: easy-register clustered at entry, then assumed.
Command frame: reading instructions open, freedom instructions close, both recapped verbatim at very end.
Saved reframe: growing-back reveal appears only in CH-13.

Structural responsibilities: redefinition box CH-01. Long testimony in main flow in own room CH-09. Myths Q&A distinct room CH-09. Meta-inoculation answering method-objection CH-09 into CH-10. Inhabit-the-ordinary-doing CH-06. Last ordinary treat CH-11. Ordinary life CH-12. Short recap CH-13. Prevalence once CH-08. No mid-book recap. No pre-endgame teaching manual.

Budgets (integer words):
CH-01 4200, CH-02 5200, CH-03 3800, CH-04 4800, CH-05 5200, CH-06 4800, CH-07 5000, CH-08 5200, CH-09 5800, CH-10 4400, CH-11 3600, CH-12 4200, CH-13 3800.
Arithmetic sum: 4200+5200+3800+4800+5200+4800+5000+5200+5800+4400+3600+4200+3800 = 60000. Planned total 60,000 within 54,000–66,000.

## 7. COMPACT CHAPTER CARDS

**CH-01 — The Invitation**
ID: CH-01 / Number: 1 / Title: The Invitation
Job: non-argument — definition — boxes BAD SUGAR, installs contract and eat promise, converts audience to participant | Resolves: is this another diet lecture.
Arc-position: first third, contract open | Freedom low promise only, Demolition not yet.
Reader-state: wary sweet-lover half-hoping half-scoffing, clutching moderation rules | Encounter: reading these pages with a full cupboard, told not to change anything yet.
Mantras: M-A — "you have absolutely nothing to lose and everything to gain" / M-B — "easily, immediately and permanently" / FT-B — "All you have to do is follow all the instructions." / FT-C — "Eat what you want, when you are hungry, stop when you are satisfied, and never punish yourself again."
Scenes: SC-01 token-seed only, fraud named without full staging.
Structure: redefinition box; authority dossier; reading contract.
Guardrails: safety CA-SAFE routed silently; originality: original sweet-contract wording, no caffeine import.
Continuity: receives brief expectation; hands open mind and defined target to CH-02.
Budget: 4200

**CH-02 — Caught, Not Weak**
ID: CH-02 / Number: 2 / Title: Caught, Not Weak
Job: enacted transition — you did not choose freely and are not weak; you were conned into a trap that removed choice | Resolves: I choose this, I just lack discipline.
Belief-now: enters believing sweet use proves free choice and weak will; leaves knowing the Sugar Trap removed choice and shame belongs to the con.
Encounter: 10pm kitchen reach before decision, cupboard evidence against free-choice story.
Evidence: EV-02 limits no permanent helplessness, no pathology label; EV-08 schedule as trap form, animal caution.
New-instruction: I-02 — DON'T STOP OR CUT DOWN UNTIL YOU FINISH / Carry on exactly as normal while you read.
Reserved-later: fuel reassignment to CH-05; mechanism split to CH-07; moderation kill to CH-10; sweetest scene to CH-09.
Arc-position: first third, trap first seen | Freedom low, Demolition ground-laying.
Reader-state: secret evening binger ashamed of empty box | Encounter makes move land as own hand witnessed.
Mantras: M-A — "you have absolutely nothing to lose and everything to gain" / M-C — "the Sugar Trap" / M-E — "the Nibbler" / M-F — "the Sweet Con" / M-G — "that empty, twitchy, slightly shaky, need-something-sweet-now feeling"
Scenes: SC-01 debut full staging; SC-02 debut full staging as body authority encountered.
Structure: names both creatures in passing; installs body, hunger, real food as encounters.
Guardrails: safety CA-SAFE; originality: kitchen-con and child-eating images original, no tight-shoes yet.
Continuity: receives defined BAD SUGAR and open mind; hands trapped-not-weak to CH-03.
Budget: 5200

**CH-03 — What Does It Do FOR You**
ID: CH-03 / Number: 3 / Title: What Does It Do FOR You
Job: enacted transition — sugar does plenty TO you and nothing FOR you; harm debate replaced by benefit demand; the empty "benefit" is a belief reading a tiny body echo as a gift — name both halves here, leave the full creature split for CH-07 | Resolves: it may harm but benefits outweigh.
Belief-now: enters conceding harm but clinging to benefit; leaves having to name one real benefit and finding none.
Encounter: ordinary day audit — sweets logged against mood, teeth, wallet, time — benefit column empty.
Evidence: EV-20 ceiling exceeded, population guidance not toxicity; EV-14 cavity mechanism with brushing mediation; limits must not overclaim personal sentence.
New-instruction: I-03 — JUDGE ONLY BY WHAT IT DOES FOR YOU / Forget harm versus benefit and ask for the benefit.
Reserved-later: energy, reward, comfort kills to CH-05 and CH-09; manufacture to CH-08.
Arc-position: first third to middle hinge | Freedom still low, Demolition axis set.
Reader-state: in-denial moderate counting treats as harmless | Encounter forces benefit ledger, not harm ledger.
Mantras: M-D — "a genuine treat or fuel" / M-H — "for the rest of your life" / FT-E — "It does plenty TO you. It does nothing FOR you."
Scenes: SC-08 seed only as question, full staging reserved for CH-07.
Guardrails: safety CA-SAFE population risk not personal sentence; originality: day-audit original, no cliff yet.
Continuity: receives trapped-not-weak; hands empty benefit column to CH-04.
Budget: 3800

**CH-04 — The Willpower Method Kept You Trapped**
ID: CH-04 / Number: 4 / Title: The Willpower Method Kept You Trapped
Job: enacted transition — past failures prove the wrong method, not a broken self; strong will persisted against instinct | Resolves: I failed so I am hopeless.
Belief-now: enters believing failure is self; leaves knowing willpower plus restriction is the Trap guard.
Encounter: diet-week diary — white-knuckle days, forbidden-must-have rebound, Monday restart.
Evidence: EV-08 schedule echo diet-binge yo-yo, animal caution; EV-17 hump days-long small-scale, not lifelong fight.
New-instruction: I-04 — NEVER BLAME YOURSELF AGAIN / Every failure was the method, never you.
Reserved-later: schedule detail to CH-07; moderation absurdity to CH-10.
Arc-position: middle early | Freedom low, Demolition rising.
Reader-state: repeated dieter braced for another lecture on discipline | Encounter reframes strong will as evidence for them.
Mantras: M-B — "easily, immediately and permanently"
Scenes: SC-04 debut full staging as evening-box proof against willpower.
Structure: anti-method chapter; braggers and whingers as sub-characters.
Guardrails: safety CA-SAFE no diet prescription; originality: diet-diary original, no borrowed caffeine braggers wording.
Continuity: receives empty benefit; hands self-forgiven investigator to CH-05.
Budget: 4800

**CH-05 — The Lift That Makes the Low**
ID: CH-05 / Number: 5 / Title: The Lift That Makes the Low
Job: enacted transition — the energy lift is relief of a low the last dose created; real energy is the body, not the fix | Resolves: I need sugar to function.
Belief-now: enters believing sweet is fuel for afternoon; leaves knowing lift is spike-then-drop misread as energy.
Encounter: desk afternoon — sweet top-up, brief buzz, fog and second reach witnessed hour by hour.
Evidence: EV-01 lived lift-then-drop, no glucose diagnosis; EV-15 crash mechanism within contested limit; EV-05 dopamine re-fire magnitude limit; EV-13 deferred load population language.
New-instruction: I-05 — BEGIN WITH ELATION, NOT DREAD / You are escaping, not losing.
Reserved-later: full mechanism split to CH-07; cue firing to CH-08; strongest reward to CH-09.
Arc-position: middle demolition | Freedom suppressed, Demolition climbing.
Reader-state: afternoon yo-yoer convinced without sweet work stops | Encounter makes inversion bodily, not abstract.
Mantras: M-D — "a genuine treat or fuel" / M-G — "that empty, twitchy, slightly shaky, need-something-sweet-now feeling" / FT-A — "flat, foggy and never satisfied"
Scenes: SC-03 debut full staging; SC-07 debut full staging as tight sweet shoes.
Guardrails: safety CA-SAFE, EV-15 limit must not overclaim clinical low; originality: office-hour staging original.
Continuity: receives forgiven investigator; hands fuel-killed to CH-06.
Budget: 5200

**CH-06 — Hunger, Satisfaction and Real Food**
ID: CH-06 / Number: 6 / Title: Hunger, Satisfaction and Real Food
Job: enacted transition — inhabit hunger, satisfaction and real food as favourite; eating itself is joy without BAD SUGAR | Resolves: without sweets eating will be grey.
Belief-now: enters fearing food joy was sugar; leaves having inhabited ordinary hunger satisfied by real meal as favourite.
Encounter: plain favourite meal eaten hungry — market vegetables, fresh bread, fruit — noticed, savoured, stopped at satisfied.
Evidence: EV-16 body manufactures glucose, no diet prescription; EV-03 reward frame limit not forbidding sweet food enjoyment.
New-instruction: I-06 — TRUST HUNGER AND SATISFACTION / Eat when hungry, stop when satisfied, enjoy real food.
Reserved-later: mechanism naming to CH-07; manufacture detail to CH-08.
Arc-position: middle inhabit centre | Freedom warming slightly, Demolition paused for inhabit.
Reader-state: comfort eater who calls dessert love | Encounter proves love was meal, company, hunger met.
Mantras: FT-C — "Eat what you want, when you are hungry, stop when you are satisfied, and never punish yourself again."
Scenes: SC-02 token-echo one phrase only.
Structure: inhabit-the-ordinary-doing chapter; primary job is inhabit, not kill.
Guardrails: safety CA-SAFE no eating plan, no good-food / bad-food moralising; originality: market-meal staging original.
Continuity: receives fuel-killed; hands inhabited eater to CH-07.
Budget: 4800

**CH-07 — The Nibbler and the Sweet Con**
ID: CH-07 / Number: 7 / Title: The Nibbler and the Sweet Con
Job: enacted transition — craving is a trivial dying Nibbler fed by a dominant Sweet Con belief; kill belief and body echo starves | Resolves: withdrawal will be unbearable.
Belief-now: enters fearing physical need; leaves knowing physical part is mild hump and belief is real target.
Encounter: early-evening grumble observed and relabelled — twitch noted, smiled at, passing without feed.
Evidence: EV-06 measured dip, no human diagnosis; EV-07 mild but well-defined small magnitude; EV-17 hump 2-5 days preliminary; EV-09 cue firing learned not compulsion; EV-10 contested honesty.
New-instruction: I-07 — SEE THE GRUMBLE AS DYING, NOT DEMANDING / That feeling is the Nibbler starving.
Reserved-later: industry installers detail to CH-08; perception proof to CH-09.
Arc-position: middle deepening | Freedom still held, Demolition high.
Reader-state: evening grazer dreading nights without sweets | Encounter makes triviality felt.
Mantras: M-C — "the Sugar Trap" / M-E — "the Nibbler" / M-F — "the Sweet Con" / M-G — "that empty, twitchy, slightly shaky, need-something-sweet-now feeling"
Scenes: SC-08 debut full staging; SC-07 token-echo one phrase.
Structure: mechanism deepening, not debut unit; splits trivial physical from dominant belief; names brainwashing installers in seed.
Guardrails: safety CA-SAFE no detox claim; originality: Nibbler / Sweet Con vocabulary only, no little / big monster borrowing.
Continuity: receives inhabited eater; hands split mechanism to CH-08.
Budget: 5000

**CH-08 — Who Built the Want**
ID: CH-08 / Number: 8 / Title: Who Built the Want
Job: enacted transition — desire was manufactured and fear of failing or succeeding is Trap-held tug-of-war; the body is a precision machine whose warning feelings are information, not bulbs to unscrew | Resolves: everyone eats it so it must be fine, and I am the addictive type.
Belief-now: enters believing want is personal and fear is wisdom; leaves knowing want was engineered and both fear ropes belong to Trap.
Encounter: supermarket aisle — bliss-point packs, cartoon mascots, checkout ambush — plus mirror of identity excuse.
Evidence: EV-11 prevalence once only, self-report not diagnosis; EV-12 mood predicts not relief, men-only observational; EV-19 crowding plus cue firing, imaging not proof; EV-04 binge model caution.
New-instruction: I-09 — IGNORE ANY ADVICE THAT CONFLICTS WITH THIS METHOD / Other voices rebuild the Con.
Reserved-later: sweetest scene reassignment to CH-09; totality to CH-10.
Arc-position: middle widening | Demolition peak, Freedom about to rise.
Reader-state: normal-seeming daily grazer citing family habit and personality | Encounter externalises blame to makers.
Mantras: M-C — "the Sugar Trap" / M-F — "the Sweet Con" / M-H — "for the rest of your life" / FT-A — "flat, foggy and never satisfied" / FT-D — "the tug-of-war of craving and fear"
Scenes: SC-09 debut full staging; SC-11 seed for margin, full staging reserved CH-10.
Structure: fear chapter plus identity-excuse inversion plus prevalence-once room.
Guardrails: safety CA-SAFE no mental-health diagnosis; originality: aisle staging original, no borrowed lion wording beyond function.
Continuity: receives split mechanism; hands manufactured-desire cleared to CH-09.
Budget: 5200

**CH-09 — The Sweetest Moment**
ID: CH-09 / Number: 9 / Title: The Sweetest Moment
Job: enacted transition — even the most seductive celebration sweet gave nothing; scene gave everything; perception can lie; this escape is for you first — set aside the industry and everyone else's feelings | Resolves: but the cinema / birthday chocolate is real love.
Belief-now: enters guarding one precious exception; leaves knowing exception was scene sneaking a ride.
Encounter: cinema lights dim, laughter, shared chocolate — same warmth replayed without dose, sweetness unchanged.
Evidence: EV-03 reward frame, not forbidding enjoyment; EV-18 split honesty narrow window, not adult course; EV-10 contested honesty.
New-instruction: I-10 — IGNORE ANYONE WHO QUIT BY WILLPOWER / Their struggle was the wrong method talking.
Reserved-later: escape-route foreclosure to CH-10; vow readiness to CH-11.
Arc-position: middle late strongest-case | Demolition peak, Freedom stirring.
Reader-state: celebration eater protecting deserved treat | Encounter meets best case head-on.
Mantras: M-D — "a genuine treat or fuel" / FT-E — "It does plenty TO you. It does nothing FOR you."
Scenes: SC-05 debut full staging; SC-10 debut full enactment as perception test.
Structure: strongest-case room plus perception enactment plus myths Q&A battery plus embedded long-form testimony in own room in main flow.
Guardrails: safety CA-SAFE; originality: cinema staging and tea-test wording original, single staging only.
Continuity: receives manufactured-desire cleared; hands exception-killed to CH-10.
Budget: 5800

**CH-10 — No Safe Sweet**
ID: CH-10 / Number: 10 / Title: No Safe Sweet
Job: enacted transition — inside BAD SUGAR there is no safe cut-down, special occasion, tomorrow or substitute; totality is only stable state | Resolves: I'll allow Fridays / just one / I'll wean.
Belief-now: enters negotiating carve-outs; leaves knowing carve-out keeps belief alive.
Encounter: Friday-allowance week — anticipation, intensified glow, creep to Thursday and Saturday.
Evidence: EV-02 one-bite carries binge, no permanent helplessness; EV-08 schedule trap; FT-E verdict invoked via token.
New-instruction: I-11 — NEVER KEEP A SPECIAL SWEET / One exception keeps the whole Trap alive.
Reserved-later: readiness gate to CH-11 only; nothing else deferred.
Arc-position: middle close | Demolition complete, Freedom ready.
Reader-state: negotiator with house-rule and tomorrow promise | Encounter proves moderation makes precious.
Mantras: M-C — "the Sugar Trap" / M-E — "the Nibbler" / M-F — "the Sweet Con" / FT-E — "It does plenty TO you. It does nothing FOR you."
Scenes: SC-06 debut full staging; SC-04 token-echo one phrase; SC-11 debut full staging as seatbelt.
Structure: escape-route foreclosure; meta-inoculation completed.
Guardrails: safety CA-SAFE margin never licenses repeat; originality: cliff and seatbelt sugar wordings original.
Continuity: receives exception-killed; hands totality to CH-11.
Budget: 4400

**CH-11 — The Last Ordinary Treat**
ID: CH-11 / Number: 11 / Title: The Last Ordinary Treat
Job: enacted transition — waiting is the Trap; freedom is now as of this ordinary treat taken with attention and vow | Resolves: I'll start after holidays / when ready someday.
Belief-now: enters lingering that tomorrow is safer; leaves knowing delay is the Con and freedom is conferred now.
Encounter: last ordinary sweet taken normally, attention on cloying ugliness, solemn vow, instant rejoicing.
Evidence: EV-17 hump as days-long echo, not dread; EV-07 mildness to calm.
New-instruction: I-12 — TAKE YOUR LAST ORDINARY TREAT AND VOW FREEDOM / Pay attention to the ugliness, then rejoice you are free.
Reserved-later: none; only ordinary life and recap follow as named.
Arc-position: after vow threshold | Freedom detonation begins.
Reader-state: convinced reader hovering at edge, wanting certainty | Encounter gates on genuine readiness, champing to cross.
Mantras: M-A — "you have absolutely nothing to lose and everything to gain" / M-B — "easily, immediately and permanently" / M-I — "BRILLIANT! I'M FREE!" / FT-B — "All you have to do is follow all the instructions." / FT-D — "the tug-of-war of craving and fear"
Scenes: SC-09 token-echo one phrase only.
Structure: last ordinary instance, not laboratory dose; readiness gate; instant conferral; two relapse doors warned.
Guardrails: safety CA-SAFE silent; originality: vow staging original, no lab-dose.
Continuity: receives totality; hands free identity to CH-12.
Budget: 3600

**CH-12 — Ordinary Days**
ID: CH-12 / Number: 12 / Title: Ordinary Days
Job: non-argument — bridge — inhabits mornings, shops, food with owned thoughts once, guarding belief without new thesis | Resolves: life without sweets will be vigilance.
Arc-position: after vow, ordinary life | Freedom high, Demolition handed to tokens.
Reader-state: newly free eater walking first sweet-free morning, shop, meal | Encounter: breakfast, aisle, checkout, evening sofa lived with ease.
Mantras: M-C — "the Sugar Trap" / M-E — "the Nibbler" / M-I — "BRILLIANT! I'M FREE!"
Scenes: SC-02 token-echo one phrase; SC-05 token-echo one phrase, no restaging.
Structure: one ordinary-life chapter; pity-not-envy script; reframe-thought-not-suppress speech; slip-forgiven as rumble lesson; no evangelising; change-nothing-else lived.
Guardrails: safety CA-SAFE cited; originality: morning-shop-meal vignettes original, no settled-scene restaging, no thought-curriculum.
Continuity: receives free identity; hands lived freedom to CH-13.
Budget: 4200

**CH-13 — Get On With Enjoying Life**
ID: CH-13 / Number: 13 / Title: Get On With Enjoying Life
Job: non-argument — recap — photographable instruction list, outward push, saved growing reframe revealed; if a reader opened here, send them to the first chapter — this page is saved reminders, not the method | Resolves: I need ongoing teaching to stay free.
Arc-position: close | Freedom crescendo peak.
Reader-state: free eater needing portable memory and permission to live | Encounter: list photographed, book closed, meal ahead.
Mantras: M-H — "for the rest of your life" / M-I — "BRILLIANT! I'M FREE!" / FT-B — "All you have to do is follow all the instructions." / FT-C — "Eat what you want, when you are hungry, stop when you are satisfied, and never punish yourself again."
Scenes: none new; no token-echo needed.
Structure: short recap list of spoken imperatives without callbacks; outward imperative; saved reframe debut: sweetness stolen now returned, growing not quitting.
Guardrails: safety CA-SAFE routed; originality: closing reframe appears here only.
Continuity: receives lived freedom; hands reader to life.
Budget: 3800
```

### This chapter's card
```
**CH-08 — Who Built the Want**
ID: CH-08 / Number: 8 / Title: Who Built the Want
Job: enacted transition — desire was manufactured and fear of failing or succeeding is Trap-held tug-of-war; the body is a precision machine whose warning feelings are information, not bulbs to unscrew | Resolves: everyone eats it so it must be fine, and I am the addictive type.
Belief-now: enters believing want is personal and fear is wisdom; leaves knowing want was engineered and both fear ropes belong to Trap.
Encounter: supermarket aisle — bliss-point packs, cartoon mascots, checkout ambush — plus mirror of identity excuse.
Evidence: EV-11 prevalence once only, self-report not diagnosis; EV-12 mood predicts not relief, men-only observational; EV-19 crowding plus cue firing, imaging not proof; EV-04 binge model caution.
New-instruction: I-09 — IGNORE ANY ADVICE THAT CONFLICTS WITH THIS METHOD / Other voices rebuild the Con.
Reserved-later: sweetest scene reassignment to CH-09; totality to CH-10.
Arc-position: middle widening | Demolition peak, Freedom about to rise.
Reader-state: normal-seeming daily grazer citing family habit and personality | Encounter externalises blame to makers.
Mantras: M-C — "the Sugar Trap" / M-F — "the Sweet Con" / M-H — "for the rest of your life" / FT-A — "flat, foggy and never satisfied" / FT-D — "the tug-of-war of craving and fear"
Scenes: SC-09 debut full staging; SC-11 seed for margin, full staging reserved CH-10.
Structure: fear chapter plus identity-excuse inversion plus prevalence-once room.
Guardrails: safety CA-SAFE no mental-health diagnosis; originality: aisle staging original, no borrowed lion wording beyond function.
Continuity: receives split mechanism; hands manufactured-desire cleared to CH-09.
Budget: 5200
```

### The draft chapter
```
Chapter 8
WHO BUILT THE WANT

**IN THIS CHAPTER** — The plain table still warm behind you, the supermarket aisle in bright morning light, bliss-point packs in rows, cartoon tigers on boxes, the checkout ambush at tired hands, the mirror that talks about personality, the count of fellow caught, the dashboard with its lights still working, the cell with its door wide open, the lion pacing by the empty cage, the seatbelt coiled quiet in its housing

*Your want was built by other hands for profit, and the fear that holds you is the Trap holding both ends of the rope.*

### THE TABLE YOU BRING INTO THE AISLE

You bring the split with you.

We pulled the evening dread apart and saw two things tangled. A tiny bodily echo. A huge reading laid over the echo. You watched the wave rise at eight and fall by ten minutes past, noted the hollow prod, smiled, forgot to remember it. You saw the lane and the ditch and the kind hand. You named the little creature starving and the loud belief dying. That seeing stays yours. No one can argue it away because your own evenings proved it.

I lived years thanking the hand that pushed me. I praised the ten bright minutes and cursed my own fog. We all did that. We were conned in the lane before we knew the lane had an owner.

Now we widen the lens. If the physical echo is that small, why did the want feel so personal, so natural, so much like you? Why does the whole street seem to want the same thing at the same hour? Why does fear speak in your own voice when you picture a life with no dose?

Because want was manufactured. Fear was installed. Both ropes belong to the same hands.

Walk with me down one ordinary aisle and watch the building happen in daylight.

### THE AISLE THAT KNOWS YOUR NAME

Come to the encounter that proves it. Not theory. A shop watched with open eyes.

Morning. Bright lights. Wide aisle. Trolley wheels humming. You came for bread and vegetables and fruit for the table. You are not hungry in the frantic sense. True hunger waits clean for dinner. You are steady.

Left and right, colour shouts. Packs built to be seen from twenty paces. Red and gold and cartoon tigers with wide eyes at the height of a child. Promises in fat letters. Extra. New. Share size. Family size. Limited. The air smells faintly sweet from the bakery corner pumped toward the door. Music quick. Shelves at hand height for grown hands, low shelves for small hands.

You walk steady past the first ten metres. Then the old hour fires. Three o'clock in the head though the clock says eleven. Paper rustle in memory. Wrapper glint in memory. Mouth waters a little before any bite. Learned firing, not order. Your body learned when floods usually came and prods a little before the hour, the way the mouth waters before dinner.

At the end of the aisle the ambush waits where you cannot walk round it. The till. Tired feet. Tired attention. Small bright doses at the exact reach of the hand while you queue. One for the road. One for the child. One because you were good this week. The hand hovers before decision. You hear your own voice, reasonable, modern, kind to yourself.

“Everyone eats it. Look round. Normal families. Fit people. Happy children. It must be fine. And I have always had a sweet tooth. It is my personality. My family are all the same. Sugary somethings to get me through. Treat when you feel you deserve one.”

I know that voice. I spoke it for years. Warm to you who speaks it now, harsh to the hands that put it in your mouth.

Ask and answer from the aisle, not from habit.

If that want were yours by nature, why did it need ten thousand reminders to stay alive? True hunger needs no cartoon tiger. True thirst needs no jingle. Why does BAD SUGAR need bright packs and paid smiles and paypoint traps to keep you wanting? If that want were personal, why does the same want rise in millions at the same hour in the same queue? If that want were love, why is the love always for sale by the same sellers?

There is only one reading that fits the aisle. Bliss built by formula. Bliss-point packs tuned mouthful by mouthful till the bite lights brightest and fades fastest and calls for more. Advertising poured over childhood before choice began. Ubiquity till abnormal looks normal. You did not invent the want in that queue. The queue was built to invent the want in you.

The fact is, desire was engineered. Laboratories weighed crunch against melt, salt against sweet, colour against craving, till the dose hit hardest and left fastest. Storytellers dressed the dose as love, reward, celebration, comfort. Shop builders placed it where tired hands cannot miss. That is the work of the Sugar Trap.

Feel what that does to shame. You were not weak in the aisle. You were outgunned in the aisle. A lone eater with true hunger against armies of formulators and advertisers and shelf planners. No wonder the hand hovered. No wonder the trolley filled. Past reaching was the method of the makers, never proof of a broken self.

And here is the short verdict that ends the aisle. They built the want.

You see through it in a second when the picture is clean. A child does not beg for a peach because a tiger told him to. He begs for the packet because the tiger told him to. Remove the tiger and the begging changes address. Remove the aisle and the hand stays steady. The want lives in the building, not in the blood.

### YOU ARE NOT THE ODD ONE OUT

Voice the mirror objection fully so it cannot return whispering.

“But that may be true for others. For me it feels deeper. I am the addictive type. I have always been all-or-nothing. Others can take one square and stop. I feel like i cant stop. Surely that proves something in me?”

We all spoke to that mirror. I spoke to it. I called myself weak-willed, sweet-toothed, born this way. I watched moderate eaters smile at dessert and felt defective beside them. Let us meet that mirror kindly, because the pain is honest, and then turn it round.

Look at the count first, then at the cause.

About one adult in seven answers yes to enough signs on honest food questionnaires to sit in the addiction-like range, and about one child in eight does the same, a level that sits beside alcohol and tobacco in the same counts. I speak of honest answers on paper, not a stamp on you, and never a diagnosis. I give you the number for one reason only. You are not uniquely weak. The Trap is common.

Ask till the personality story confesses its size.

If addictiveness lived in persons, why does the same person crave wildly in the queue and forget completely on a full holiday week with real meals and full attention? If moderation lived in persons, why do the most controlled eaters lose control exactly when a little is permitted in the evening box? If family habit proved nature, why do families share cupboards and clocks and stories about dessert as love, which teach want far better than blood?

There is only one pattern that fits your life. Traits shared by heavy users are the result of the lane, not the cause of the lane. Restlessness, hunting, evening edginess, mid-afternoon fog, the roller coaster, the short term lift then fast drop. You did not bring those traits to BAD SUGAR. BAD SUGAR brought those traits to you, dose by dose, year by year, till you called the coating yourself. That voice is the Sweet Con talking.

Even if you did carry a quicker spark than another, what would it change? A quicker spark lights faster in a room full of matches. Remove the matches and the spark has nothing to catch. This method does not need you to be a certain type. It frees any eater because it kills belief, and belief is what feeds the loop. Sound eater or quick spark, the ditch is the same, the hand is the same, the escape is the same.

Consider the normal eaters you envy. Watch them closely and envy dies. Many graze daily and call it normal while feeling flat, foggy and never satisfied by four o'clock. Many smile at dessert while hunting an hour later. Normal everywhere only proves brainwashing everywhere. Feeling fine in the aisle never meant intake was low. It meant the water warmed so slowly no one noticed the heat.

And here is the flat verdict on the mirror. You are not the type. You were the target.

Be glad of that reversal. A type cannot be changed. A target can walk out of range. You walk out not by fighting yourself but by seeing who built the want and refusing to pay for their building with your evenings.

### WHY THE PACK KEEPS GROWING

There is a second proof in your own cupboard, and it has nothing to do with character.

Recall the pack sizes of your life. The bar that once lasted a film now lasts the opening credits. The biscuit that once closed the evening now opens the hunt. The family size bought to save money empties faster than the small bag ever did. You need more for the same brightness, and the brightness lasts shorter each year.

That is not gluttony. That is crowding.

Reward circuits blunt under flood. The same dose lights less. Want speaks louder while liking speaks softer. I claim only what your evenings prove, not what a scan proves. Your mouth knows the shape without a laboratory. More for same effect. Brighter packet, duller pleasure, louder call an hour later. Learned firing before the bite, wrapper and smell and old hour chiming together, then the hollow prod after.

In rats given sweet only in short bursts, the burst pattern drove gorging and prodding and low after high, clear as push and hand. Rats are not you. I hand you that freely. It changes nothing for your freedom. Your sofa showed the same burst shape without a cage. Restrict all day, burst at night, low by morning, promise by noon, burst again. Schedule plus sweet drives the binge. The yo-yo is the form of the Trap.

Now add the mood proof, stated with care.

Among men followed for years, the daily sweet came before the low months more often. The sweet did not fix mood forward. Low followed sweet. I speak of likelihood across many, not a sentence on you, and never a diagnosis of any reader. If you live with low mood or any condition where food change carries risk, follow your clinician first and use this book for belief only.

Ask what that does to the comfort story.

If BAD SUGAR comforted, why do comforted evenings need comforting again by ten, and by three next day, and by eight? If BAD SUGAR lifted, why do lifted eaters sit lower year by year? If the rescue were real, why does the rescued grow more tired, more hunted, more grey? True comfort closes. This comfort opens.

There is only one reading that honours the growing pack. The lift is deferred load, not free energy. Each flood borrows brightness from the next hour and pays back fog. Each family size buys a shorter peace at a higher rent. You never rose above the clean baseline. You sank below it, were lent back toward it for ten minutes, then sank again.

Feel how light that reversal is. You do not need a bigger pack. You need no pack. The need for bigger is proof the pack never met need.

### THE DASHBOARD YOU WERE TOLD TO SMASH

There is a body truth that makes the whole manufacture look like vandalism, and it returns awe where shame lived.

Your body is a precision machine. Hunger builds slow and plain. Smell sharpens. Taste brightens. Satisfaction closes gentle. Energy runs steady from real food. Sleep deepens. Mouth clears. Bowels move. Skin heals. Mood steadies with rest and meals and light. No tiger required. No formula required. The machine knows its office.

BAD SUGAR pastes over that dashboard and then tells you to smash the lights.

Consider the warning feelings you were taught to read as faults. The three o'clock fog after a sweet flood. The evening edginess after a day of top-ups. The hollow prod that narrows to one taste only. The restless hunt after the box empties. You were taught to answer each light by pouring more sweet on the engine. Quick fix. Quick hit. Feed the ache to quiet the ache.

Ask what a good driver does with a red light.

Does he unscrew the bulb so the glow stops? Does he call the bulb the fault? Does he pour oil on the dashboard to hide the lamp? No. He reads the lamp as information. Low oil means add oil. Hot engine means cool the engine. The lamp is the friend. The fault lies elsewhere.

Your warning feelings are information, not faults to unscrew. Fog after flood means flood, not need for flood. Twitch at the old hour means learned firing passing, not order to feed. Hollow that refuses bread and calls only for sweet means echo dying, not hunger calling. Low mood that follows daily sweet means load, not proof life is grey without sweet.

I speak of the sound eater in general. If you ever feel faint, ill, or distressed around food, seek care promptly and put argument aside till you are cleared to continue.

See how the makers profit from smashed dashboards. A driver who reads lights fixes the engine once and drives free. A driver who unscrews bulbs returns daily to the garage that sold him the screwdriver. Each dose unscrews a bulb for ten minutes while heating the engine hotter. Each ad calls the unscrewing relief. Each till offers another screwdriver at the queue.

Will you keep unscrewing bulbs for the rest of your life, paying for the screwdriver with your evenings? Or will you read the lights clear and drive free for the rest of your life, with hunger and satisfaction back at the wheel?

There is only one answer a driver gives when the trick is seen. You keep the dashboard. You lose the garage.

That is why change here is not fear-driven. I lay the load plain and frightening where true, then tell you plainly not to change from fear. Fear tightens the hand on the old screwdriver. Seeing loosens it. You escape not because you tremble at the engine but because you marvel at the machine and refuse to vandalize it further. Relief follows seeing the way morning follows night.

### THE CELL WITH ITS DOOR OPEN

Now we meet the last rope, the one that speaks in wisdom tones.

You stand with manufactured want exposed, mirror turned, dashboard kept. Yet feet do not move. Two fears hold the ankles. Listen to them in your own voice.

“What if I fail? I have failed diets before. White-knuckle weeks that collapsed. Monday restarts. If I try to live with no BAD SUGAR and collapse again, the shame will be worse than staying. Better to stay in the cell I know than crawl back bleeding.”

“What if I succeed? Who am I with no treat? Celebrations, cinema, birthdays, tired evenings, love itself. If I walk out, life will be grey and I will be strange among normal eaters. Better to stay where sweetness lives than step into a plain that has no joy.”

I know both fears. I lived both. One pulls forward. One pulls back. Both hurt. Both sound wise. Both belong to the same hands.

See the cell plainly to feel the inversion in your bones.

A prisoner sits in a small cell. The door stands ajar. Light falls through the gap onto the floor. Outside lies ordinary day, bread and work and laughter and hunger met clean.

The prisoner begs to stay.

“Do not make me go. Outside I will fail and be dragged back. Outside I will succeed and never belong again. Inside at least I know the hours. Inside at least I have my sweet at eight.”

Beside the empty cage outside paces a lion, freed months ago, circling the old bars from habit. No chain holds him. No hunger drives him back. Habit walks him round the same worn ring, past the open gate, round again, though food and plain and pride wait ten paces off.

Ask what holds either figure, and answer slowly.

Does the open door compel staying? No. The door compels nothing. Fear of outside writes orders on air. Does the cage hold the lion? No. Memory of bars walks legs that are free. Does failure wait outside to punish stepping? No. Staying guarantees the very fog and hunt and low the prisoner fears. Does success mean grey? No. Grey lives inside where taste dulls and evenings hunt. Outside lies the vivid table you already tasted.

There is only one pattern that fits. Both ropes are held by the Trap. Fear of failing says you will crawl back, so never step. Fear of succeeding says freedom will be loss, so never want to step. One rope pulls to shame. One rope pulls to grief. Both hands wear the same coat.

You live caught in the tug-of-war of craving and fear.

Feel the geometry resolve. Craving pulls toward a dose. Fear of failing pulls away from trying. Fear of succeeding pulls away from wanting to try. Three pulls, one holder. The Trap lends craving with one hand and lends dread of leaving with the other, then calls the tension proof you need the cell. Cut either rope and tension falls. See the holder and both ropes fall together.

Ask till fear confesses.

If fear of failing were wisdom, why did staying fail you every day while calling itself safety? If fear of succeeding were wisdom, why does the vivid meal you ate hungry shame the grey you fear? If the cell protected, why do protected evenings end flat, foggy and never satisfied? If the plain were loss, why did the table with no dose delight?

There is only one verdict that honours the open door. The fears are not yours. They are installed.

Be stern with the installer, never with yourself. We all paced like that lion. I paced. You paced. Habit walks free legs round old bars for a while after release. That pacing is cage-habit, not proof of need. Watch it with a smile when it comes. A thought of sweet at the old hour. A wobble by the till. A dream of the box. Note it, name the holder, turn back to hunger and the day. Ten minutes later you forget to remember it. That forgetting is freedom happening on its own.

Do you want proof the door is open now? Recall the grumble you already learned to greet as dying. Recall the aisle you already saw building want for profit. Recall the mirror you already turned. No new courage is required. Only the step you already own. You do not battle fear with grit. You see fear is rented furniture in a cell you never locked.

And here is the flat verdict on fear. It never protected you.

### A QUIET WORD ON BLIPS

Keep one margin clear so panic never rebuilds belief.

Your body is sturdy. It can cope with an accidental crumb, a sauce you did not make, a bite taken in unknowing. A seatbelt exists for the accidental jolt on an honest road. It is not permission to steer toward the wall.

Guard the belief, not the bite with panic. A blip revives nothing unless the old sentence is let back in. If a crumb lands unchosen, note it, leave it, eat clean at hunger, stop glad at satisfied, and get on with enjoying your life. Deliberate dosing is another country. No mind can afford a deliberate dose because the mind, not the body, keeps the Trap alive. I speak of sound eaters in general. If you live with diabetes or take medicine that touches blood sugar or appetite, are pregnant, live with an eating disorder past or present, or carry medical risk, follow your clinician first and use this book for belief change only.

That seatbelt saying stays seed here. Full road belongs later. Enough now to know panic is another rope, and all ropes belong to the same holder.

### 8. IGNORE ANY ADVICE THAT CONFLICTS WITH THIS METHOD
Other voices rebuild the Con.

**SUMMARY**
- Want was built by formula, story and shelf, not born in you.
- Heavy use marks a common trap, not a special personality.
- Bigger packs prove blunting, not bigger need.
- Daily sweet comes before low, it never fixes low.
- Body signals are lights to read, never bulbs to unscrew.
- Both fears pull for the same holder, and the door stands open.
```
