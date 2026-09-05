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

Delivered 5176 words. Budget 4800.

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
CH-01 4200, CH-02 5200, CH-03 3800, CH-04 4800, CH-05 6300, CH-06 4800, CH-07 5000, CH-08 5200, CH-09 6800, CH-10 4400, CH-11 3600, CH-12 4200, CH-13 1700.
Arithmetic sum: 4200+5200+3800+4800+6300+4800+5000+5200+6800+4400+3600+4200+1700 = 60000. Planned total 60,000 within 54,000–66,000.

## 7. COMPACT CHAPTER CARDS

**CH-01 — The Invitation**
ID: CH-01 / Number: 1 / Title: The Invitation
Job: non-argument — definition — boxes BAD SUGAR, installs contract and eat promise, converts audience to participant; the fact the reader is holding this book means the decision is already made, and what follows is only good news | Resolves: is this another diet lecture.
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
Job: enacted transition — the energy lift is relief of a low the last dose created; real energy is the body, not the fix; BAD SUGAR is empty calories that nourish nothing and gift no energy the body did not already own; and escaping means the want is removed for good, not a resistance that fails the day the want comes back | Resolves: I need sugar to function.
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
Budget: 6300

**CH-06 — Hunger, Satisfaction and Real Food**
ID: CH-06 / Number: 6 / Title: Hunger, Satisfaction and Real Food
Job: enacted transition — inhabit hunger, satisfaction and real food as favourite; eating itself is joy without BAD SUGAR; voice the reader's suspicion that "favourite food" is a play on words and answer it flat — there is no catch, the pleasure is real | Resolves: without sweets eating will be grey.
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
Job: enacted transition — even the most seductive celebration sweet gave nothing; scene gave everything; perception can lie; this escape is for you first — set aside the industry and everyone else's feelings; reverse the brainwashing from both sides at once — see natural food as the marvellous thing it really is while the brainwashed favourite shows as the bland junk it always was | Resolves: but the cinema / birthday chocolate is real love.
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
Budget: 6800

**CH-10 — No Safe Sweet**
ID: CH-10 / Number: 10 / Title: No Safe Sweet
Job: enacted transition — inside BAD SUGAR there is no safe cut-down, special occasion, tomorrow or substitute; totality is only stable state; the substitute idea itself is the flaw — swap the product, sweeteners included, and you remain a user, still hooked | Resolves: I'll allow Fridays / just one / I'll wean.
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
Budget: 1700
```

### This chapter's card
```
**CH-06 — Hunger, Satisfaction and Real Food**
ID: CH-06 / Number: 6 / Title: Hunger, Satisfaction and Real Food
Job: enacted transition — inhabit hunger, satisfaction and real food as favourite; eating itself is joy without BAD SUGAR; voice the reader's suspicion that "favourite food" is a play on words and answer it flat — there is no catch, the pleasure is real | Resolves: without sweets eating will be grey.
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
```

### The draft chapter
```
Chapter 6
HUNGER, SATISFACTION AND REAL FOOD

**IN THIS CHAPTER**
Market air at eight, the paper bread-bag, the hungry table, the quiet full stop

*Real food eaten hungry already is the favourite you thought sugar was.*

The Grey Plate You Fear

You watched the drawer tell on itself. You saw the ten bright minutes paid for with blunt hours. You saw the tight shoe and the ditch and the Saturday test that shows the dose plain when no low waits underneath. That part is settled in your daylight.

And beneath it a colder fear moves. I know it because I carried it for years.

“All right. The lift was a trick. But what is left? Will eating turn grey?”

Say it plain. You fear food joy was sugar. You fear meals without a sweet close will be flat fuel stops. You fear hunger itself, that hollow that always seemed to mean fetch something sweet and fast. You fear you must live policed around plates for the rest of your days, chewing dutiful mouthfuls while memory plays highlights of chocolate.

It is an honest fear. I do not mock it.

You are a comfort eater who calls dessert love. I was the same. I called a certain cake love. I called late ice cream kindness after a hard day. I called the shared bar on the sofa proof that the day had held something soft. Take those away, I thought, and what remains is cardboard and duty.

Ask that fear its plainest questions, and answer only from a mouth you have lived in.

When you were truly hungry — not twitchy, not mouth-coating crave-hungry, but empty-bellied, hours-since-food hungry — when did plain food ever taste grey?

When you sat down starved after work or a walk and ate bread, soup, potatoes, cheese, an apple, when did you need a lecture to enjoy it?

And when you were already stuffed with grazing and reached for one more sweet bite, when did that bite ever sing the way the first bite of a hungry meal sings?

You know the answers. Hunger makes flavour. Fullness dulls it. The grey you fear already belongs to grazed days, not to fed days.

We lived that grey together, you and I. We know the coated tongue at five. We know the belly full and the mouth still calling. We know the evening box emptied without a single bite truly tasted after the second. We know the morning that starts coated and dull and already thinking of sweet tea to get going. That is grey. That was never love. That was noise laid over appetite until appetite could not speak.

The fact is, eating itself is joy when hunger leads and satisfaction closes. No catch. No play on words. No grey plate waiting for you.

Stay with that grey for a moment longer, because the trap taught you to misread it. The trap taught you that grey meant lack of sugar. Grey meant you needed a lift. Grey meant the meal was too plain, too brown, too ordinary, and only a sweet close could colour it. Look again at the hours that were grey. They were not hours without sugar. They were hours heavy with sugar. Lunch plus sweet drink. Afternoon bar. Train dose. Evening box. Sugar at every turn, and still grey. If grey meant lack of sweet, those hours should have shone. They did not shine. They coated.

Now look at the hours that were bright in memory before the trap claimed them. A sandwich eaten on a wall in sun after a long walk. Soup eaten starved after cold air. An apple eaten on a train when hunger was real. No wrapper. No buzz. No second reach. Bright because hunger met food and food answered. You did not need to be taught to enjoy those hours. You did not need a rule. You were present and hungry and the food was real, and that was enough for joy to arrive uninvited.

We were brainwashed to read that joy as too small. Small because it did not spike. Small because it did not coat. Small because no advert had named it. We learned to call only the spike joy and to call the steady glow nothing. That ranking was never yours. It was installed.

I want you to test the ranking with your own mouth, not with my talk. Recall your last grazed evening in detail. The first square bright with memory. The second duller. The third eaten standing, half turned away. The rustle. The reach. The box lightening. The mouth coating. The belly tightening while the call continued. The morning resolve. Was that colour? Was that love? Or was that grey wearing a bright label for ten seconds?

Recall your last truly hungry meal in detail. The sit-down. The first bite noticed. The talk thinning as everyone chewed. The second helping taken slowly or not taken. The stop that arrived on its own. The mouth clean. The head clear. The hours after with no thought of food. Was that grey? Or was that eating as it was built to be?

You know. Once both evenings stand side by side, the verdict writes itself.

The Market At Eight

Come with me to the market at eight on a Saturday, hungry.

Not starved as punishment. Hungry as nature. You slept, you woke, you drank water, you walked out with an empty belly asking plainly for food. No dose since last night. No twitch. A clean, hollow ask.

Air smells of coffee from a cart and of earth from the stalls. Lettuces hold water drops. Tomatoes sit heavy and warm from the van. Herbs smell sharp when you bruise a leaf between fingers. A baker stacks loaves that crackle as they cool. The crust sings. A woman breaks a corner for you to taste. You taste.

You buy what pulls the eye. Crisp greens. A few roots. Mushrooms with soil still on. Bread still warm in paper. Apples, grapes, figs for the table. Cheese wrapped in wax. Eggs in a grey box. Nothing counted. Nothing weighed. Nothing written down. Your bag grows heavy in a way that feels glad in the hand.

Bring it home. Lay it out. Wash, cut, cook simply. Oil, salt, heat. Bread torn, not sliced. Soup from roots and water and salt. Greens wilted in a pan. Fruit washed and left whole to bite.

Sit down hungry. Eat.

First bite of bread. Crack, chew, warmth spreading. You notice. Second bite with tomato and salt. Juice runs. You notice. Spoon of soup. Heat moves outward. You notice. Greens with oil. Bitter, fresh, alive. You notice. You talk, you laugh, you reach, you pause. Midway the edge leaves hunger. Flavour sharpens, then softens. You slow without telling yourself to slow. A little more. Then enough arrives with its own clear signal. You stop. Not because a rule rang. Because satisfaction rang. Fruit to close. Bite, juice, sweet, done.

Sit a moment. Belly warm. Head clear. Mouth clean, not coated. No call from the cupboard. Hours ahead with no thought of food.

That is the encounter. Not theory. A meal eaten hungry, noticed, savoured, stopped at satisfied.

I ate such meals for years without seeing them. I ate them between doses and credited the doses for any joy in the day. When I saw, I laughed out loud at my own blindness. The meal had been carrying me all along.

Walk that market again slower, because the slowness is the point. At the first stall you lift a tomato and weigh it in the palm. Heavy for its size. Skin tight. Smell at the stem. Green and summer. At the next stall you tear basil and hold it to the nose. Sharp, sweet, alive. At the baker you press the loaf and hear it crack. You did not do this to be virtuous. You did it because hunger makes the nose keen and the eye bright. Hunger is a sauce no jar holds.

Carry the bag home and notice the weight. Potatoes thudding. Apples rolling. Bread breathing through paper. This weight never sat in the drawer. The drawer held light packets that promised much and left you hunting. The bag holds plain weight that asks nothing and leaves you quiet.

Cook without performance. Water boils. Oil shimmers. Onion softens. Salt wakes. No measuring. No timing to the second. The kitchen fills with smell that pulls hunger forward a touch and then steadies it. You taste the soup and add salt and taste again. That tasting is not grazing. That tasting is hunger in dialogue with food, adjusting, attending. Notice how different it feels from the drawer reach. The reach is urgent, narrow, sweet-only, hurried. The tasting is open, curious, patient, willing to wait for the pot.

Sit. Do not start with the sweet close in mind. Start with hunger. Bread first, because hunger calls for it. Soup next, because warmth calls. Greens, potatoes, cheese as the tide moves. Talk if people are there. Quiet if you eat alone. Chew. Put the spoon down between mouthfuls. Look out of the window. The meal does not run away. It waits for you to return to it. That waiting is part of its pleasure. The dose never waits. The dose hurries you to the next dose.

Midway, attend to the change. The first bites were bright with edge. The middle bites are steady with depth. Flavours that were sharp soften. Chewing slows. Reaching pauses. Someone tells a story and you listen rather than reach. The body is turning the volume down, not because the food failed, but because the need is met. That turning down is not loss. That turning down is arrival.

Then the stop. A sigh. A leaning back a fraction. Bread remains in the basket. You look at it with fondness and no pull. Fruit remains in the bowl. You take figs because they call, honeyed and soft, and leave the rest without a second thought. The bread smells sweet from the paper bag, and you fold the bag for later without a pang.

This is what favourite feels like from the inside when noise leaves it alone. Not a spike. A tide met, a tide turned, a shore reached.

Hunger Knows Its Work

“But hunger frightens me,” you say. “I thought hunger meant I needed sugar fast.”

I thought that too. We were brainwashed to read every hollow as an order for sweet. Let me show you what hunger is when noise leaves it alone.

True hunger builds slowly. It does not shout at three and vanish at three fifteen after a biscuit. It rises like tide over hours. An emptiness, a lightness, a thought of food that welcomes many foods. Bread would do. Soup would do. Fruit would do. Eggs would do. That welcome-many is its signature.

The sweet call behaves opposite. It builds fast, asks urgently, accepts only one answer, returns within the hour. I-need-to-eat-something-RIGHT-NOW feeling belongs to that call, not to hunger. You learned to tell them apart at the drawer. Keep that telling here.

Your body already owns steady carry. I speak plain physiology here, not a plan for you to follow. The body makes the even sugar it needs from ordinary meals — from bread and vegetables and fruit and protein — quiet and held, the way a good stove holds heat. It does not need a splash of sweet on the coals every hour to stay lit. If you live with a condition where changing what you eat carries risk, your clinician’s word comes first.

Hear what that means. Leaving BAD SUGAR out is not leaving fuel out. Numbers without nourishment never fuelled you. Meals feed you. Hunger asks for them. Satisfaction tells you they landed.

Watch a hungry child to see the instrument unbroken, the child with the peach who stops mid-bite to run off.

One phrase, and the whole authority stands there. No counting. No guilt. No finishing to please the plate. Body leads. Body closes.

We were that child once. Before sweet meant prize and party and proof of love, we ate, stopped, ran. The instrument did not break. It was drowned. Each dose laid noise over the signal until we could not hear enough. We called the noise appetite. We called the drowning hunger.

Learn the tide by watching a plain day. Morning. Water. Movement. The belly quiet after sleep, then a first hollow around mid-morning or noon depending on your night and your work. Not urgent. A thought of lunch that welcomes many lunches. You eat when the tide is truly in. First bite brightest. Middle steady. Stop clear. Quiet for hours.

Contrast that with the dosed day. Morning sweet tea. Eleven biscuit. Lunch plus sweet drink. Two o clock dull. Three o clock urgent call. Four o clock second call. Evening box. The belly rarely hollow, rarely quiet, always coated, always hunting. Which day left you fed? Which left you hunting? You have lived both. Your mouth is a better witness than any label.

Notice how true hunger accepts waiting. You feel the hollow at eleven thirty and finish the task and eat at twelve, and hunger waits without panic. You feel it on a walk and walk another twenty minutes to the bench with a view, and hunger sharpens rather than sours. The sweet call accepts no waiting. It stamps its foot. Now. Now. Now. That stamp is not hunger’s voice. Hunger does not stamp. Hunger asks.

Notice how true hunger accepts many answers. Hollow at noon, you pass a bakery, a soup stall, a fruit cart, and each pulls a little. You choose one and the hollow quiets. The sweet call accepts one answer only. It walks past bread and soup and apples without a glance and points at the packet. Bread would not do. Fruit would not do. Only the hit would do. That narrowness tells you everything. Hunger is wide. The loop is narrow.

Notice how true hunger leaves when fed and stays gone. Meal at one, quiet till six. No mental math. No bargaining. No glances at the clock. The sweet call leaves for minutes and returns. Dose at three, quiet at three fifteen, calling at four. That quick return is not appetite. That quick return is the echo of the last dose leaving.

Test it with your own mouth this week, not as a task, only as watching while you live. Eat when the tide is truly in. Notice the first bite brightest. Notice the middle steady. Notice the quiet full stop. Notice how long quiet lasts when the meal was real. Then notice a grazed hour by contrast. Dose on fullness. Brief noise. Coat. Call. No stop, only pause till next. Which hour left you fed? Which left you hunting?

The verdict is short.

Hunger is flavour.

Enough Has A Sound

We never learned to hear enough because doses have no enough.

A dose pleases briefly, dulls quickly, urges more. First square bright with memory. Second duller. Third eaten to finish the bar rather than to enjoy it. Fourth because the packet is open. That urge is not appreciation. That urge is the loop calling for repeat under the name of taste.

Real food behaves opposite. It pleases, deepens, then says enough. Enough has a sound if you listen. A sigh. A slowing hand. A glance away from the plate toward the room. Food still there, still good, no longer wanted. That is not will. That is satisfaction, a bodily event as plain as hunger, as plain as thirst quenched.

We were taught to override it with rules and with doses. Clean the plate. Save room for sweet. Have just one more because it is there. Finish because money was paid. Each override taught us not to trust the signal. No wonder we fear we cannot trust ourselves around food. We practised not hearing.

Sit at the hungry table again and hear it return.

You eat. Talk thins as hunger meets food — that first quiet where everyone chews. Then talk returns, easier. You reach less often. You lean back a fraction. Bread remains in the basket. You look at it with fondness and no pull. Fruit remains in the bowl. You take one piece because it calls, bright and sweet in its whole skin, and leave the rest without a second thought. Hours pass. No coated mouth. No hunting hands. No mental math. The body asked, received, closed. That closure is satisfaction. It needs no number.

Ask the closed meal its questions.

If satisfaction needed a dose to complete it, why does the hungry meal close without one?

If sweet completed meals, why do dosed meals never close, only pause?

If you could not trust your body, how did your body just tell you, clearly and without words, when enough arrived?

You trusted it because it spoke. It always spoke. Noise only covered it.

Learn the sounds one by one so you recognise them at your own table. Early hunger sounds like interest. Menus pull. Smells pull. The belly feels light and open. Mid-meal sounds like ease of chewing, talk thinning, flavours vivid. Late meal sounds like slowing. Chews longer. Pauses longer. Eyes lift from plate to faces. The hand rests. Enough sounds like a small full stop. Not stuffed. Not heavy. A quiet “done” in the belly, a breath that drops lower, a wish to move or talk rather than to take another bite. Stuffed sounds different — tight, dull, coated, regretful. Grazed sounds different again — full belly with calling mouth, the odd split that proves noise, not need.

We lost the full stop because the packet has no full stop. The packet ends, but appetite does not close when the packet ends. It pauses till the next packet. The meal closes, and closure holds for hours. That difference is worth more than any rule. Once you hear the full stop twice, you trust it the way you trust thirst quenched. You drink when dry, you stop when quenched, you do not count sips. You eat when hungry, you stop when satisfied, you do not count bites.

I do not give you a plan around this. I give you back an ear. There is a quiet opening that comes when hearing returns after years of static, like a radio finding its station.

Do not moralise the hearing. No food here is virtuous. No bite here is sinful. There are meals that feed and leave quiet, and doses that noise and call. You are learning to tell feed from noise by the after-hours, not by a label. That telling is not a diet. That telling is appetite returned to its work.

Practise the hearing in small moments that carry no weight. The pause after soup before the next course. Do you want more, or has the edge left? The bread basket after the second piece. Does the third call, or does the smell please without pull? The fruit bowl after one fig. Does the second glow, or does the mouth feel done? No scoring. No making up for yesterday. No earning tomorrow. Only listening while you live.

And when you hear late, do not scold. Many meals will run past the full stop while you relearn, because old habit reaches after the body stops. That overshoot is not failure. That overshoot is information. Note it the way you noted the drawer. Earlier stop next time, or not. The ear sharpens with use, not with blame. I never learned to hear by scolding. I learned by noticing the quiet hours that followed a closed meal and wanting more of those hours, the way you want more of any good company once you have sat with it.

But Is Favourite Just Words?

Now the sharpest voice. Let it speak.

“That is pretty writing. But you call bread and apples favourite. Come on. My favourite was chocolate fudge cake. You are playing with the word favourite to trick me into settling for less.”

I welcome that voice. It keeps us honest.

I answer flat. There is no trick. There is no catch. The pleasure is real.

Favourite never meant loudest in the mouth for ten seconds. Favourite means what you return to with gladness, what leaves you well, what you would choose again tomorrow hungry. By that plain measure, test your own history.

Take the fudge cake loved in memory. Eat it hungry on a clear morning after sleep and breakfast, slow, attended, no low underneath. First bite bright with memory and novelty. Second duller. Third sickly to finish. Evening flat. Where is the fabled favourite across the eating? It thins as you eat. It coats. It calls. It leaves you less settled than before.

Take the hungry meal. Bread, market vegetables cooked simply, fruit. First bite bright. Middle steady. Close quiet. Evening clear. It does not thin into sickly. It deepens into enough. It leaves you settled for hours.

Which behaved like a favourite in the body, not in the advert?

It is you that loves, not the dose. It is your hunger that makes bright. It is your company that makes warm. It is your table that makes a birthday glow. The dose only ever sneaked a ride on their backs and claimed their credit. I speak of the birthday table here as the frame that kept the loop alive, not as a law against sweet taste itself. Sweet lives honestly in whole fruit, in a meal shared, in hunger met — joy there needs no defence.

We confused intense with best. A fire alarm is intense. We do not call it music. A dose is intense because it spikes and coats and fires memory at once. Intensity fooled us into ranking it above the quieter, longer pleasure of hunger met. Once seen, ranking corrects itself without force. You do not need to persuade yourself that bread beats cake. You need only eat hungry and notice which pleasure holds and which begs repeat.

Try the plain test at your own table. Same hunger. Two days. One day a hungry meal eaten noticed to satisfied. One day a hungry meal followed by grazing doses to box-empty. Which evening do you remember with warmth? Which evening do you remember with fog? Which would you call, hand on heart, better eating?

You know. We all know once both columns stand side by side.

Press the test further, because the trap will whisper that memory of cake is proof. Memory keeps the first bite and discards the tenth. Memory photographs the candles and the laugh and crops out the coating and the hunt. Memory frames the wall and the sigh and crops out nine to six in tight shoes. That edit is not lying. That edit is how minds work. We remember endings vividly and backgrounds dimly. The trap lives in that edit. Your investigator work corrects the edit. You log both columns now. Bright and blunt. First bite and third. Laugh and coat. Once both columns stand, memory stops lying for the trap.

Hear the love-word corrected. When you called dessert love, love was present — but love was the people, the pause, the care after a hard day, hunger met at last. The dose sat at the table where love sat and took the photograph. Remove the dose and love remains at the table, clearer, because no noise talks over it.

I called a certain cake love for a decade. I ordered it after hard weeks. I ate it on the sofa while the day drained off. I told myself it held me. Look closer with me. What held me on those nights? The pause after strain. The warmth of the room. The permission to stop. The company or the solitude chosen, not imposed. Hunger met by dinner before the cake arrived. The cake arrived last, loudest, latest, and claimed the whole evening the way a loud guest claims a photograph by standing in front. When I ate the evening without the loud guest, the evening did not empty. The evening deepened. Talk lasted longer. Sleep came cleaner. Morning started clearer. Love had been there all along, mislabelled.

So favourite stands. Not as a slogan to chant. As a mouth-event you can repeat tonight. Hunger. Food noticed. Enough heard. Mouth clean. Hours quiet.

This is not settling for less. This is return to appetite, where food tastes as food tastes when the eater is present.

The Table That Was Always There

There is a table that waited for you through all the grazed years. It did not move. You moved.

Picture it plainly. Wood worn smooth. Chairs that know your weight. Window with light that changes by the hour. Morning bowls. Midday plates. Evening pots. Fruit in a bowl that empties and fills with the week. Bread in paper. Oil by the stove. Salt in a dish. Nothing shining. Nothing shouting. Only food that answers hunger and then lets you get on with the day.

We left that table for the drawer, the machine, the packet eaten standing. We ate with one eye on the screen. We ate without sitting. We ate without hunger and without stop. We called that normal eating. It was not eating. It was feeding the loop between meals while meals waited.

Return is not learning. Return is noticing what stayed.

Sit at that table hungry tomorrow and notice how little needs to change. You shop as before, only hungrier and therefore keener. You cook as before, only simpler because hunger needs less disguise. You eat as before, only seated and attended rather than hurried and half-turned away. You stop as the body asks, rather than as the packet dictates. You wash up and walk away and do not think of food till hunger returns. No new system. No new shop. No new self. Only the old table seen clear.

I want you to feel how much of your day already belongs to that table. Breakfast eaten hungry after sleep tastes bright without teaching. Lunch eaten after morning work satisfies without counting. Dinner eaten after the afternoon holds without a sweet close. Fruit eaten for thirst and brightness quenches cleanly. Water drunk when dry. Movement taken when stiff. Rest taken when tired. The body already runs these errands when noise leaves them alone. BAD SUGAR never ran them. It only laid static over them and charged you for the quiet it stole.

Ask the table its questions.

If plain meals needed a dose to be joy, why did the market morning pull your eye and nose before any packet appeared?

If hunger were an enemy, why does hunger met leave you kinder, steadier, more present to people than grazing ever left you?

If enough were a rule, why does enough arrive on its own when you eat seated, hungry, and attending, without a number in sight?

You know because you have sat there. The table proves itself each time you let it.

Stay a little longer at that table into the evening, because evening is where fear talks loudest. Evening says the day deserves a close, the nerves need softening, the house needs quieting, and only sweet can do it. Watch an evening closed by a hungry meal. Plates cleared. Fruit eaten if called. Tea if wanted. Body satisfied, not stuffed. Talk or book or walk. Sleep arriving without a coated mouth. Morning starting without a dull head. Compare it with an evening closed by grazing. Plates plus packet. Brief noise. Coat. Call. Box lightening. Sleep shallow. Morning dull. Which evening softened you? Which evening hardened tomorrow? You have lived both. The table kept the record.

And watch a party evening at that table, because the trap will point at birthdays and film nights and say, there, you need us there. Lay the same test over the party. People, laughter, candles, film, pause, care. Hunger met by food that feeds. Fruit bright among plates. The room warm. Notice how much of the warmth belongs to faces and stories and leisure, not to the wrapper. Notice how the dose, when present, narrows attention to itself for minutes and then leaves coating and hunt in a room built for company. Notice how the evening without the dose does not thin. It widens, because no one leaves the table to hunt. Love stays seated.

This is why I say sweet lives honestly in whole fruit and in hunger met. An apple bitten hungry needs no apology. Figs shared at a table need no defence. Bread torn and eaten to satisfied needs no rule. Joy there is not a lapse. Joy there is appetite doing its work in daylight. The trap taught you to hear any sweet taste as proof you still need the packet. That hearing was false. The packet is not fruit. Fruit closes. The packet calls.

Hold that distinction by the after-hours. Fruit eaten hungry: bite, juice, brightness, done, quiet. Packet eaten full: noise, coat, call, hunt, fog. Same mouth. Same tongue. Opposite afternoons. The mouth knows which fed and which borrowed. Trust the afternoons more than the adverts.

You came to this room fearing grey. You leave it with a table, a tide, and a full stop you can hear tonight. Keep the drawer log beside them. Keep the shoe. Keep the ditch. Keep Saturday. They are witnesses that the lift was debt. Keep the market bag, the torn bread, the soup steam, the fruit bowl. They are witnesses that food is joy when hunger leads. You need no new witnesses for the next room, only the ear you have now.

Eat what you want, when you are hungry, stop when you are satisfied, and never punish yourself again.

That sentence is not a rule to police yourself with. It is permission to hear what already speaks. Want here means hunger’s pull toward real food, not the twitch that accepts only sweet. When means when the tide is in, not by the clock. Stop means when the quiet full stop sounds, not when the packet ends. Never punish means no clean-plate club, no make-up fast, no scolding for hearing late while you learn. The body does not punish. It informs.

6. TRUST HUNGER AND SATISFACTION
Eat when hungry, stop when satisfied, enjoy real food.

SUMMARY
- Grey belonged to coated grazing days, not to plain meals eaten hungry.
- Hunger rises slowly over hours, welcomes many foods, and stays quiet for hours after a meal.
- The sweet call rises fast, takes only sweet, and returns within the hour.
- A hungry meal pleases at first bite, deepens in the middle, and gives a clear stop.
- A packet pleases briefly, dulls quickly, and urges more without ever closing.
- The body makes steady carry from ordinary meals, so plain eating leaves nourishment in place.
- Love at the table came from people, pause, care, and hunger met.
- Favourite means what holds, settles, and is gladly chosen again hungry.
```
