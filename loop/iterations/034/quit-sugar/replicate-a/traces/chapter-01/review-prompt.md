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

Delivered 3147 words. Budget 4200.

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
```

### The draft chapter
```
Chapter 1
THE INVITATION

**IN THIS CHAPTER** — The kitchen cupboard still full, the boxed meaning of BAD SUGAR, my own sweet years, the plain meal eaten hungry, the reading contract.

*This is not another lecture about food — this is good news about sweetness, and you can take it in exactly as you are.*

### THE CUPBOARD IS STILL FULL

You are holding this book for a reason.

Do you want to get out of the sweet loop? Of course you do — that is why you picked it up. And do you also worry that life without sweet treats would be greyer, flatter, harder? Of course you do — that is why you have not walked out already.

Both things are true at once. That does not make you weak. It does not make you foolish. It makes you exactly the reader I wrote this for.

I know how you come to me. Half-hoping, half-scoffing. You have tried the diets. You have tried the rules. No biscuits in the week. Only at weekends. Only dark. Only a little. Only when you have been good. You have watched each clever rule collapse in the same quiet way. Then you told yourself the comfort story: I like my treats, I choose this, leave me alone.

Let me ask you plainly. If you truly chose this, if you truly liked it on your own terms, why would you need a book about it? If a man loves his morning walk, does he buy a book called How To Stop Walking? Does he hide the evidence? Does he promise himself on Sunday night that Monday will be different?

We tell ourselves we choose it. Then we know that strange moment when the hand is already in the packet before any clear decision was made. No blame in that. A fraud was worked. That is all I will say about it here. The full picture comes in its own place. For now, keep one honest question beside you: who is in charge when that happens — you, or the sweet?

You do not need to answer yet. You do not need to change anything yet. Your cupboard can stay exactly as it is while you read these first pages. I am not here to take food from your mouth. I am here to show you something you have not been shown.

You suspect the whole approach you were given was wrong. You are right. It was wrong. Not because you failed it, but because it failed you. Every white-knuckle week, every forbidding list, every Monday restart — that was never your fault. This time is different because this is not that method at all.

Too good to be true? That was my reaction too when I first heard it. I thought: there is no way out of this that is not miserable. I thought: food people like me do not get to feel normal around sweets. I was wrong, and I am glad I was wrong. You will be glad too.

I make you no gloomy forecast. I lay no burden on your shoulders. What follows is only good news.

### WHAT I MEAN WHEN I SAY SUGAR

We need clear terms or we will talk past each other. When people say sugar they mean ten different things and argue about all of them at once. I will not do that to you.

In this book one line divides the subject. Learn it now and you will never be confused again.

> BAD SUGAR means refined sugar and added free sugars and junk processed carbs and starchy snack-carbs eaten as sweet hits. That includes sugary drinks, confectionery, biscuits, cakes, pastries, desserts, sweetened cereals, sweetened yoghurts, sauces loaded with added sugar, and the handfuls of crisps and white crackers and similar grazing doses that act the same way in the day. When this book says sugar, take it to mean BAD SUGAR.
>
> Natural sugars sealed inside whole fruit and vegetables and plain meals as cooked and eaten are not the target. They belong to real food. They stay.

Read that box twice. It matters.

I am not talking about an apple. I am not talking about a plain potato in a meal, or carrots from the market, or milk as it comes. I am talking about doses. Little packets of lift-and-drop engineered to be quick, sweet, and gone — the bar, the can, the biscuit, the bowl of frosted stuff that leaves you hunting an hour later.

There is no healthy level of that sought here. There is no clever allowance that keeps it precious. Inside this line, zero sought is the only stable place. That sounds stark on page one. It will sound kind by the end. You will see why with your own eyes, not because I told you to believe it.

One plain human note while we define terms. If you live with diabetes or pre-diabetes, take medication that affects blood sugar or appetite, are pregnant, live with an eating disorder past or present, or have any medical condition where changing what you eat could carry risk, talk to your clinician before changing anything and follow their advice first.

That note sits outside our argument. Our work together is belief. Your clinician holds care of your body. I hold to that order without exception.

With the line drawn, hear the decree that carries it: when this book says sugar, take it to mean BAD SUGAR. Every page from here on speaks inside that line. Nothing outside it is judged. Nothing you need is threatened.

Does that narrow the field? Yes. Does that make the job smaller and clearer? Yes. You are not being asked to quarrel with food itself. You are being invited to look straight at one narrow con inside food and see it for what it is.

### I WAS THE LAST PERSON TO BELIEVE THIS

I did not write this as a theorist. I lived it.

We in our house lived the roller coaster. Morning promise, mid-morning slip, afternoon top-up, evening hunt. I told myself the same lines you tell yourself. I need sugary somethings to get me through. A treat when you feel you deserve one. I have managed to be good this week, so one will not hurt. Then one hurt in the only way that matters: it woke the want again.

I was not a fool about other things. I could organize a kitchen, run a day, keep promises to other people. Around BAD SUGAR I made promises at night and broke them by morning and called that my character. It was not my character. I had been taught to read the whole thing backwards.

I tried what you tried. Lists on the fridge. Smaller packs — as if a smaller cage makes a trap kinder. No sweets in the house — then the walk to the shop in the rain. Skipping meals to be good — then eating standing up at the cupboard with the door open. Each collapse added another layer of shame, and shame never once made the next day easier. Shame made the next night secret.

What changed me was not a new rule. It was a new seeing. A friend who had walked out of the same loop asked me three quiet questions over a plain lunch. I could not answer one of them honestly without conceding the point. I laughed because I was caught. Then I felt light for the first time in years around food, not because I had fought hard, but because I had understood something simple.

I had believed BAD SUGAR lifted me, rewarded me, helped me through. I saw, hour by hour, that the lift made the low and the reward took more than it gave. The fact is, I had mistaken the ending of a discomfort for a gift. Once seen, it could not be unseen.

I did not need to be persuaded twice. I did not need to count days. The want fell away because the belief holding it fell away. Eating stayed. Hunger stayed. Meals stayed. Only the tug around sweets went quiet.

I tell you this not to impress you but to remove one fear: that this book was written by someone who never knew the 10 p.m. hunt. I knew it. I knew the rustle that sounds too loud in a quiet house. I knew the arithmetic of I will make up for it tomorrow. I knew the bright packet that promises comfort and delivers a short buzz and a longer flatness.

Since then I have sat with hundreds of sweet users and watched the same light go on. Not the strained light of a person holding their breath. The clear light of a person who sees the trick and cannot be tricked in the same way again.

You do not have to take my word for any of this. In fact I ask you not to take my word. Take your own observation as we go. Question what you think you know. Test each claim against your own afternoons and evenings. The truth does not need your belief to be true. It only needs your attention for a little while.

### THIS IS NOT A DIET

Let me settle the fear that brought you here braced.

Is this another diet lecture? No. It is the other way around.

A diet tells you what to weigh, what to count, when to stop, how to punish yourself back into line. It puts you at war with hunger and calls that health. It makes food precious by forbidding it, then blames you when the forbidden calls louder. With the willpower method, there is no finish line. There is only the next test.

I will not do any of that to you.

You will not count. You will not weigh. You will not go hungry. You will not earn food by being good. You will not pay for food by feeling bad. There is no good week to protect and no bad night to confess. Those are cage bars, not care.

Here is our eating contract, and I want you to feel its weight. We eat because we are hungry. We stop because we are satisfied. We enjoy real food as favourite. No punishment enters the room.

Eat what you want, when you are hungry, stop when you are satisfied, and never punish yourself again.

Read that again slowly. That is not a trick sentence. It is the whole basis of a normal eater, and it is yours by nature. Watch a small child with a peach when hunger leads. Hungry, eager, juice on the chin — then mid-bite, done, off to play. No counting. No guilt. No negotiation with the peach. The body led, satisfaction closed the meal, life went on. We were all built to eat that way. BAD SUGAR taught us to eat by the clock of craving. We return to the body clock now.

But, you say, without sweets eating will be grey. Fruit is sugar too so nothing matters. Everyone eats it so it must be fine. I hear you. Those are honest objections and each gets its own room later. For now notice their shape. They all assume the pleasure you love lives inside the packet. What if the pleasure lives in hunger met, in a meal savoured, in company, in a morning mouth that tastes clearly? What if the packet was only ever sneaking a ride on joys that were never its own?

I am not asking you to believe that yet. I am asking you to allow the question. Picture a lunch where your attention stays on the meal and you feel free to stop when your body has had enough. Warm bread, market vegetables, fruit with its own clean sweetness, eaten hungry and left when satisfied. No tug after. No arithmetic. That picture is not a dream diet. It is ordinary eating remembered.

You will not be deprived of food. You will not be deprived of joy in food. The method here adds nothing to your plate and takes no meal away. It removes only the doses that kept hunger confused and satisfaction out of reach.

So lay down the dread you brought to page one. Cast aside all feelings of doom and gloom. There is no need to be miserable here. You are not about to be shrunk, scolded, or starved. You are about to investigate one belief and find it false — and investigation is an exciting adventure only if you allow it to be plain and honest.

### HOW WE DO THIS TOGETHER

A book can be read two ways. One way keeps the reader at arm's length: interesting, arguable, easy to close. The other way makes the reader a partner: testing, noticing, answering back. I need the second reader. That reader is you.

We do this in a simple order that has worked again and again. You read with an open mind. You do not prejudge. You let each point land before you argue with it. You try each small observation in your own day. That is the whole labour. There is no hard part hidden behind it.

All you have to do is follow all the instructions.

That clause is not small talk. It is the contract that makes the rest work. Think of a combination lock. Miss one number and the door stays shut, not because you are weak, but because one piece was missed. This book is that lock. Each instruction is one number. Turn them all and the door opens. Skip one and you rattle the handle and blame your hands.

Why should you trust that? Because of the shape of the promise I make now, flat and without hedge.

First, the risk. You risk nothing by reading on with an open mind. You keep your cupboard. You keep your meals. You keep your routines. No one asks you to perform. Read on with that open mind, because you have absolutely nothing to lose and everything to gain.

Second, the manner. I do not offer you a long struggle crowned years from now. I mean that you can leave BAD SUGAR behind easily, immediately and permanently.

Those three words sound outrageous together. Easily? After all the failed weeks? Immediately? Without a slow wean? Permanently? Without looking back? I state them together on purpose, with total confidence, because halves of them keep people trapped. Easily without immediately becomes tomorrow. Immediately without permanently becomes a break. Permanently without easily becomes a sentence. Together they describe what happens when belief changes rather than behaviour is bullied.

I know this is hard to accept. I welcome that doubt. Bring it with you and test it. Have you ever avoided watching a film that did not interest you — no effort, no count, no brave face? That is what it is like when a want is gone rather than held down. No effort is needed not to do what you do not want to do.

Think of stepping out of a stuffy room into cool morning air. That clean change is the kind of escape I am pointing toward. One breath and you know where you are. No one needs to coach you to keep breathing once the air is clear.

You may ask: will I not feel I am losing something? Only while the old belief speaks. A belief that BAD SUGAR is a genuine comfort makes leaving feel like loss. Show that belief false and leaving feels like what it is: the end of an irritation. The fact is, there is nothing in the packet that hunger, company, rest, or a real meal does not hold better without the drop that follows.

So here is our frame, stated once and kept. We fell into this together — we were all taught the same sweet lines as children, we all learned to pay ourselves in doses. You walk out of it personally, on your own seeing, at your own pace of understanding. I lend you my eyes for a while. You lend me your honesty. That exchange has opened this lock for others. It will open it for you.

### WHAT I ASK BEFORE WE BEGIN

I ask one thing at the start, and I ask it as a direct instruction, not as advice you may take or leave. Everything later rests on it.

If you read with a closed mind, every page will sound like someone trying to take something from you. If you read with an open mind, the same pages sound like someone handing something back. The pages do not change. The mind does. Bring the mind that can be changed by truth.

Question your fondest certainty about sweetness as you would question a story told to you as a child by people who meant well but did not know. Did you decide, after calm thought, that sweet doses help you function? Or did you find the idea waiting for you in adverts, in kitchens, in kindnesses, and never think it over? The fact is, we never thought it over when we found it. Now we think it over together.

Will you do that? Will you let your own afternoons give evidence? Watch the hour after a sweet top-up, not with fear, but with curiosity. Notice the brief buzz, then the fog, then the second reach. Notice the evening box that was meant to hold one and holds none. Notice the morning mouth. You are not collecting sins. You are collecting facts. Facts are kind here. They point one way.

I promise you this as one who walked the same floor. Follow the reading as laid, keep the eating contract as spoken, and the rest arrives in its own order. You do not need to be brave beyond honesty. You do not need to be strong beyond attention. Bring attention and honesty and the book does the heavy lifting.

Then at the close of this opening, take the first number of the lock and turn it.

1. KEEP AN OPEN MIND
Question what you think you know about sweetness.

**SUMMARY**

- This is not a diet and not a lecture; no counting, no hunger, no punishment enters this method.
- BAD SUGAR has a fixed meaning in this book, and natural food stays outside it and stays yours.
- You picked up this book because part of you already wants out; that want is clear sight, not weakness.
- A fraud was worked on all of us around sweets; seeing it removes blame and returns choice.
- Eating stays as nature built it: hunger leads, satisfaction closes, real food is enjoyed as favourite.
- The way forward is simple reading with an open mind; the door opens when every part is turned.
```
