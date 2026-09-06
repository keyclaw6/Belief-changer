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

Delivered 5133 words. Budget 5200.

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

The Saturday aisle with bright packs and cartoon eyes; the till ambush and the kitchen mirror; the dashboard bulb that must not be unscrewed; the open cell door and the pacing lion

*You did not grow this want. It was built in you — and the fears that hold you were built with it.*

### THE AISLE THAT KNOWS YOUR NAME

Walk it with me on an ordinary Saturday, trolley light, list short.

You came for bread and milk. You know the shape of this shop blindfold. Fruit to the left, bread at the back, milk along the cold wall. And still the walk takes twenty minutes longer than the list, because the middle miles were drawn to slow you.

Look low where small eyes look. Cartoon tigers, dancing biscuits, smiling bars with arms and legs. Look high where tired adult eyes look. Gold letters, craft paper, words like energy, natural, protein, light. Look at the ends of every aisle where the brightest stacks sit like altars. Look at the till where, after all your sensible choosing, small bars wait in a final ambush at hand height, sized for one more unwitnessed dose on the way to the car.

We tell ourselves we chose this. We, the Saturday shoppers with wills of iron at work and soft hands at the till. We who swore no packet today and hear the rustle in the boot before we turn the corner.

Ask from inside that trolley, investigator to investigator.

Did you wake as a child asking for a white crystalline powder stirred into water — or did bright packets find you before you could read, at birthdays, at school gates, on television between cartoons?

Did your grandmother keep a cupboard of wrapped bars — or did your mother learn it from adverts and pass it on as love, and you pass it on as normal?

If the want were yours by nature, why does it need three thousand reminders a day to stay alive — billboards, jingles, sponsored sport, cinema tubs, office jars, till trays?

One honest answer runs through all three. The want did not rise from your belly. It was planted, watered, lit from every side till it looked like appetite.

The fact is flat: desire for BAD SUGAR was manufactured. Laboratories learned the exact sweetness that makes the mouth ask again before the swallow ends. Designers dressed the dose as friend. Sellers placed it where choice is weakest — by the queue, by the school run, by the tired hour. You were not weak in that aisle. You were outgunned in that aisle.

We were all conned there, week after week, by men who never meet us and know us better than we know ourselves.

It does plenty TO you. It does nothing FOR you in that aisle. Keep that beside every bright pack and the glow dies.

### SWEETNESS BY DESIGN

I want you to see the build clearly, because vague blame changes nothing and clear seeing changes everything.

First, the mouth was measured. Not your mouth, thousands of mouths. Spoon after spoon, dial up, dial down, till the needle stopped at the point where pleasure tips into wanting more rather than enough. Too little and you notice nothing. Too much and you push the cup away. At the middle point you take another sip without deciding. That middle point has a trade name in the trade journals. I will not lend it poetry here. Call it what it is in plain shopping language: the sweetness that keeps the hand moving.

Ask with a pack in your palm.

Does plain hunger ever ask for a second bowl before the first is swallowed — or does only the engineered dose ask while the mouth is still full?

Does an apple sharpen and then settle you — or does the bright drink sharpen and then sharpen again till the bottle is gone and the hand looks for more?

Did you ever hear a child say one peach was too little and ten peaches too little — or does that bottomless arithmetic belong only to packets?

One answer fits your own kitchen. Hunger closes. The design forbids closing.

Second, the eye was tutored. Colour that shouts across a hall. Crinkle that promises from two rooms away. Characters that grow up with your children and sit on their pillows. Health words borrowed for junk — real fruit pictures on boxes that never saw an orchard, farm kitchens printed on plastic that never saw a farm. Ubiquity doing the quietest work of all: when every shelf, every station, every party holds the same dose, the abnormal reads as normal and the questioning mind goes to sleep.

We call that normal. We say everyone takes it. We say a birthday without a tower of icing is not a birthday, an evening at the pictures without a tub is not an evening, a tired driver without a bright bottle is not safe. None of those sentences were born in you. Each was placed, repeated, paid for.

Third, the hour was wired. Morning bar for the commute. Mid-morning biscuit for the meeting. Afternoon lift for the slump. Evening box for the sofa. Night square for the teeth-brushing hour. The clock became a menu written by someone else, and the mouth learned to water on time.

Ventriloquise your own shopping voice and hear the training in your accent:

"It's normal. Everyone has something sweet. Our family has always had a sweet tooth. A house without treats is not a home."

I print those lines because they are yours and mine. We all spoke them at tills while the till smiled back.

Hear them truly now: those are not observations. Those are scripts rehearsed till they sound like thought.

If everyone takes it, does that make it chosen — or does that prove how widely the net was thrown?

If your family always kept it, does that prove blood — or does that prove the net was thrown two generations ago and never lifted?

If a house without packets feels bare, is the bareness in the house — or in the eye taught to read bare shelves as unkind?

One straight line cuts all three. Common does not mean natural. Old does not mean yours. Everywhere does not mean necessary. It means manufactured, thoroughly, brilliantly, at your expense.

You live inside the Sugar Trap while common reads as proof. You see the build the moment common reads as evidence of the con.

### NOT YOUR NATURE

Here the mirror talks, and the mirror lies with your own voice.

"I am the addictive type. Others can take one square. I feel like i cant stop once I start. My personality, my genes, my childhood. That is why diets always collapse on me."

I honour that ache by printing it whole. We have all stood at the empty box before the swallow ended and read character from cardboard. We called a triggered binge proof of self. We called an evening at home proof for life.

Hear the inversion flat, stated as settled fact: those shared traits are the result of the loop, not the cause of it.

Ask from your own box evenings.

Did you show this frantic hand with plain meals — chasing soup, unable to stop at bread, haunted by apples at midnight — or did the loss of stop arrive only with bright doses?

Did the child you were eat a peach hungrily, stop mid-bite, run off to play with juice on the chin — or did that child hoard and hide and bargain only after packets entered the house?

If the type made the trap, why do clean weeks show a different type — calmer hands, quieter cupboards, hunger that opens and closes — in the same skin, same genes, same childhood?

One answer closes the file. The behaviour made the personality you blame. Take the dose out of the day and the frantic self thins with it.

Now widen the lens, because shame loves the lie that you are uniquely broken.

Ask around with honest questions about highly palatable food — loss of stop, craving, use despite regret — and around one adult in seven says yes often enough to look caught, and around one child in eight, a tally much like drink and tobacco. That does not hand you a label. It lifts one. You were never a rare weak will. You were one of millions answering the same bells.

The sciences argue over names for this, and I will not tidy that argument to sound clever. Where sweet comes and goes on a clock, bingeing and craving grow loud in animal rooms. Where access never breaks, the same signs stay quiet. That tells you about pattern, not about destiny. It is no proof of a lifelong sentence on you, and it is no permission to keep dosing. It tells what your own diet years told — restriction by day, permission by night, the roller coaster driven by timetable rather than by character.

Add the lived creep you already know. The square that once closed the evening now only opens it. The small bar becomes the shared bag becomes the family size, not because joy grew but because the mouth learned to ask louder for less return. Wrapper rustle firing before the bite. Smell from a bag opened two rooms away moving the feet. Clock-time gnaw at eight, at three, at the film titles. That firing is learned wiring, not fate written in blood. Bells rung often turn heads. Bells cannot lift feet.

So hear the verdict that ends this mirror room in one short line:

The type did not build the want. The want built the type.

Hold that beside every memory of the emptied box and shame has nowhere to stand. Warmth for you, harshness for the makers. You were trained, timed, cued, measured. Training can be seen. Seen training loses command.

### THE DASHBOARD BULB

I owe you awe before I owe you warning, because only awe makes warning bearable.

Your body is a precision machine. Not a metaphor machine, a working one. It builds its own steady fuel from plain meals, it reads hollow and full to the ounce, it steadies breath and beat while you sleep, it tells you in plain signals what it needs — pull low for food, dry mouth for water, heavy lids for bed, dull head for air and movement. No dial lies for long in a clean system. Hunger points at food and then releases you. Satisfaction arrives as looseness and quiet mouth. That is the authority you met at the market table, and it has never left you. It was only talked over.

BAD SUGAR talks over it by laying noise on the dials and then selling you the noise as information.

The fact is a daily sweet habit points toward lower mood later rather than lifting mood now, in men followed over years where the order was checked and the low did not summon the dose first. I state that without dressing it as a sentence on you. It does not diagnose you. It does not promise gloom if you dosed yesterday or brightness if you skipped today. If you live with low mood, with diabetes or pre-diabetes, with medicine that touches blood sugar or appetite, pregnant, with an eating disorder past or present, or any condition where food change carries risk, your clinician leads and this book stays belief work only. For the ordinary reader the meaning is narrower and still cutting: the treat that claimed to mend the day is linked with days gone flatter afterward — flat, foggy and never satisfied — not mended.

Ask with the dashboard in view.

Does a car run better when you unscrew the oil light — or does the engine run darker while the dash looks brighter for a mile?

Does a tired afternoon mend when the mouth is flooded sweet — or does the dial go quiet for ten minutes while the load lands later as fog and second reach?

If the dose fixed feeling, why do the most dosed weeks leave you the dullest-eyed, and the cleanest mornings leave you the brightest-nosed?

One answer fits all three. The feeling was information. The dose unscrewed the bulb.

Picture it concrete. You drive home at dusk, low fuel lamp glowing amber. You could stop for fuel. Or you could twist the bulb out and praise the dark dash for looking calm. Sweet does the second. It covers pull, tiredness, thirst, stale air, need for supper, need for bed, under a brief buzz that reads as fixed while the tank stays low. An hour later the lamp glows again through the tape, louder, joined by jaw-buzz and hand-search. You twist again. Round and round. The praise belongs to the twist, never to the drive.

The makers love unscrewed bulbs. A driver who reads lamps keeps driving clean. A driver who tapes lamps buys tape for life. Every advert that calls a bar energy, comfort, love, reward, teaches the hand to reach for pliers rather than for food, water, rest, company, air.

You know the deferred load in your own accounts. Teeth that paid for sweet coating. Afternoons that paid for morning flood. Evenings that paid for afternoon lift. Wallet, time, attention paid in small coins daily till the jar is light. Feeling fine through it proves nothing about load. Water warms so slowly the swimmer never notices till the boil. I do not want you to act from fright at that water. Fright never kept anyone clear. I want you to see the build so clearly that fear has no work left — only sight, and sight held in an ordinary shop.

Hear the verdict for the dashboard in plain words:

Feelings inform. Doses blind.

Keep that beside every 3pm reach and the reach reads backwards. Mouth asks sweet. Body asks supper, water, air, rest. Answer the body and the mouth quiets. Answer the mouth and the body asks louder later. That is not will. That is instrumentation honoured.

A seatbelt waits in the car for the accidental jolt, not for steering into walls. Your body likewise rides over a crumb unplanned without ruin. Mind must not steer into the wall on purpose. More of that wall belongs to a later room. Keep the bulb screwed tight tonight.

### THE OPEN DOOR AND THE PACING LION

Now we touch the fear that keeps good shoppers dosing after they see the build. Name it truly and it thins. Leave it unnamed and it rules.

You feel pulled both ways at once. Part of you wants the aisle to lose its command. Part of you dreads life past the till — grey food, bare birthdays, failure broadcast, success that leaves you a stranger to yourself. Wanting and dreading in the same chest, hour after hour. That pull has a name you will use for life. It is the tug-of-war of craving and fear.

I give you that phrase as a tool, not as poetry. Craving pulls one arm: just one square to close the day properly, sugary somethings to get me through. Fear pulls the other arm: fail and prove you are hopeless, succeed and lose your sweet self for the rest of your life. Both ropes burn. Both feel like wisdom. Neither is yours.

See the two fears apart, because they wear different masks and share one owner.

First fear wears failure paint. If I try and fall at the first party, better not to try. If the box empties again, let it empty without witnesses. If clear sight needs effort, I have no effort left after years of diet weeks.

Second fear wears success paint. If I ever walk past the till unmoved, who will I be at cinemas, at Christmas, at my own table? You hear the Sweet Con whisper that brightness lives in packets and a life past packets will be grey, dutiful, thin-mouthed, watching others glow while you count. Better the known ditch than the unknown plain.

Both fears feel personal. Both are installed.

Stand with me at the prison corridor.

A cell door stands ajar, light from the hall falling across the bunk. The man inside has paced that square for years. He knows every stain, every cold corner, every hour by the rattle of trays. The guard is gone. No lock holds. And when you beckon him out, he begs to stay. Outside is too wide, he says. Outside I will fail. Outside I will be no one. Give me the known walls. His terror is sincere. His reading is false. Every bar he fears outside is a shadow cast by inside.

Now cross the yard to the cage.

A lion paces by an open gate, dust in the sun, gate wide since morning, keeper vanished. The beast walks the old square — four paces, turn, four paces — not from hunger, not from chain, only from years of walking that square when the gate was shut. Passers think the pacing proves need for bars. The pacing proves habit haunting muscle after need ended.

You are both figures in one body, and neither figure proves you need the Trap.

The prisoner begging to stay is your fear of failure and your fear of success talking with one mouth. Stay, it says, or you will fall. Stay, it says, or you will vanish. Both speeches belong to the Sweet Con that fed you through the bars for years. The cell taught the dread of the hall. The hall never earned it.

The lion pacing the old square is your hand at eight o'clock, your feet at the till, your eyes at the advert tear. Four paces to cupboard, turn, four paces back, gate open all the while. That pacing is not proof of nature. It is training echoing after use ended. Watch it a few evenings and the feet forget the square.

Ask inside that corridor, because corridor answers flat.

If the cell protected you, why did years inside leave you flatter each year, more gnawed, more secret?

If the cage fed you, why did the gate need to stand open for you to notice you were pacing rather than eating?

If outside were grey, why do clean mornings taste louder, talk run warmer, hunger close kinder — why does the hall smell of bread while the cell smells of wrappers?

One answer fits all three. The ropes never belonged to wisdom. They belonged to the builder. Cut the belief and both arms fall loose at once.

This is why the dread of failing and the dread of succeeding arrive together. A single owner pulls both ends to keep you still. Name the owner and the stillness ends. You live inside the Sugar Trap while fear reads as counsel. You read counsel as con the moment both ropes show one hand.

Hold the other valence beside the threat, because time cuts both ways and you must choose which cut you want. Dosing, crashing, craving, hiding boxes, counting treats, restarting Mondays for the rest of your life — that is one rest-of-life on offer, and the Trap signs it with your hand. Mornings with clean pull, shops walked without ambush, meals closed at satisfied, evenings with talk unbroken for the rest of your life — that is the other rest-of-life, already waiting past the open door.

Hear the verdict for the corridor in one short line:

Both ropes belong to the Trap.

Keep that beside every wobble and wobble reads as echo, not order. Prisoner fear proves bars, not need. Lion pacing proves training, not hunger. Gate open. Hall lit. Feet yours.

### OTHER VOICES WILL REBUILD IT

With the build seen and the ropes owned, one danger remains standing, polite, concerned, certain it helps.

Other voices.

They will come the moment you talk of leaving the loop. Some love you. Some sell to you. All speak from inside the same training and call it sense.

"I've managed to be good this week, so one small treat when you feel you deserve one cannot hurt."

"Just allow the natural ones, the dark ones, the Friday ones. Control is maturity."

"You need sugary somethings to get you through the afternoon or your brain will stall."

"Short term lift then fast drop is just life. Everyone rides the roller coaster. I want to get off the roller coaster sounds dramatic."

"Cut down slowly. Keep it in the house for the children. Avoid the aisle if you must, count days, be careful at parties."

Hear each line truly. Each rebuilds, brick by brick, the Sweet Con we just pulled down. Each calls the dose friend, need, reward, nature, maturity, kindness. Each hands the Nibbler fresh voice after we starved its old one. The kindest voice can lay the heaviest brick when it speaks from training rather than from sight.

I speak as one who listened too long. I collected advice like coupons — diet sheets, expert columns, well-meaning friends who quit by clenching and wore their clench like honour. Every coupon kept the question open. An open question is a fed Nibbler. A fed Nibbler rings bells. Bells obeyed rebuild belief. Belief rebuilt refills aisles.

Ask from inside that noise, because noise answers flat.

If their advice opened a way out, why did years of it leave the aisle stronger and your hands softer?

If one small deserved dose closed anything, why did deserved weeks run the heaviest boxes?

If slow cutting taught control, why did control need re-teaching every Monday while clean sight holds without lessons?

One answer fits all three. Advice that keeps the dose alive keeps the builder alive, however kind the mouth.

You have already paid for other maps. Diet weeks that blamed you. Rules that made packets precious. Counts that kept sweetness crowned as prize. This room hands you a different rule, spoken plain, to be used the hour the next voice knocks with a coupon and a smile.

You know now that want was engineered pack by pack, hour by hour, till common read as natural. You know the type excuse reads backwards — loop made self, not self made loop — and millions answer the same bells. You know the bulb must stay screwed, feelings read as fuel gauges rather than orders for sweetness. You know both fears pull from one hand. With that sight settled, to re-open the argument each time a new expert speaks is to hand the trowel back to the builder.

So when the till friend, the column, the well-meaning quitter of the hard way leans in, hear the training inside the kindness and do not follow it into debate. Pity the pacing, never yourself for hearing it. Hold the corridor, the dashboard, the aisle as seen. Let their packets stay theirs.

Live that minute all the way through, because the rule is only real when hands, mouth and feet stay yours inside noise.

Take the till first, Saturday ten to five. Lights high, belt squeaking, your trolley with bread, milk, greens, soap. Your friend wheels alongside, basket loaded, boy tugging her sleeve for a striped bar at hand height. She laughs, tired, kind, and turns to you with love in her voice:

"Go on. You've been good this week. One little treat when you feel you deserve one. We all need something to get us through."

The boy watches. The cashier beeps. The bar sits bright at your elbow, close enough to touch without reaching. Old years would have taken it to prove kindness, to prove normal, to close the female talk with sugar on top.

Stand there with sight held. Hands stay on the trolley handle, cool metal under palms. You feel the handle, you feel feet in shoes, you feel belly quiet after lunch, not hollow, not calling. Mouth pictures the sweet flood for three seconds and then pictures the papered mouth an hour later, unprompted, because the dashboard stays screwed. You do not correct her. You do not quote a book. You smile the way you smile at a neighbour praising a ditch you once thanked.

You say, warm, short: "Not for me today. We have plenty at home." The boy hears plenty and runs his car along the trolley edge. Your friend shrugs, drops the bar back for her own basket, talks on about school shoes. No pause. No sting. The belt moves. You pay. You push out with bread smelling through paper.

Mark what did not happen. No argument about health. No speech about design or bulbs or cages. No reopening of whether one small deserved dose might close anything. The question stayed shut while talk went on. Pity did the work that proof never could — you saw wiring in her tired kindness, training in her generosity, the old bell ringing in her hand toward her boy, and you wished her hall lit without needing to say so. The tug in your chest loosened while the belt beeped, because both ropes showed one hand and neither rope got a pull.

Feet out to the car park. Boot open. Bags in. Rustle of plastic, cold air, keys. The aisle behind glass looks loud and small at once. Quiet follows you, not as achievement counted, but as noise absent.

Take the party next, Thursday eight, kitchen crowded, birthday table sagging. Plates, cups, candles relit, laughter. A neighbour you like pushes a paper plate toward you, gold cake, icing high, and says it with a grin that expects joining:

"We do Fridays here. Just the good ones. Dark, little, proper. You can handle one. Control is what grown people do."

Other hands hold plates. Other mouths chew. The smell of warm sugar and candles fills the room. Old years would have taken to prove manners, to avoid the stare, to keep the evening sweet on top of sweet.

Stay there with sight held. Hands hold tea, warm cup between both palms. You feel the heat, you feel feet on lino, you feel belly banked from supper, mouth quiet, not buzzing. The picture of the first bite comes — soft, bright — and passes in four seconds while someone tells the school-run story and everyone laughs. You do not lecture the table. You do not name traps or cons. You answer the kindness, not the claim.

You say: "That looks grand on you. I am well with my tea." You ask about the candles, where she found the tall ones. She laughs, turns, cuts for the boy. Talk rolls on. Your cup warms hands that tear nothing, fold nothing, hide nothing. Feet stay where they stood. Mouth drinks tea and talks, tastes tea and lemon, needs no cover.

Mark what did not happen. No tally of whether dark counts, whether Friday counts, whether little counts. No weighing of natural against junk. The line stays whole while laughter goes on. Pity again, silent — you see the lion pacing the old square in every polite push, the prisoner begging others to stay so staying feels normal, and you wish them hall air without saying so. The tug loosens in company, because craving and fear showed one owner and neither got obedience.

Coats later. Door air cold. Goodnights. Pavement home under lamps. Mouth clean on the walk. Hunger will pull for breakfast, not for packets. The table behind you stays warm in memory, and none of the warmth belonged to the plate you did not lift.

Take the morning paper next, Friday seven, kitchen table, kettle just boiled. Column open, expert photo smiling, headline promising sense. You read while tea steams:

"Keep a little in the house for the children or they will binge elsewhere. Taper slowly. Learn your triggers and steer round the aisle. Track your days."

Old years would have clipped that coupon and kept the question open till Monday. New sight reads training inside print.

Sit there with sight held. Hands round tea, toast browning, radio low. You feel the chair under you, feet flat, belly pulling low and clean for breakfast, pointing at eggs and bread. The words try to unscrew the bulb — tiredness means dose, children mean house stocked, caution means counting. You watch the try without obeying it. You fold the paper, not in anger, in finished business. You butter toast. You eat hungry. You stop at looseness. The column stays folded under the fruit bowl while the day starts.

Mark what did not happen. No letter written in the head. No fresh research planned. No weighing whether tapering beats stopping or whether avoidance beats sight. The question stayed shut while toast crackled. Pity again — you see a kind voice paid to rebuild walls, a bell rung in newsprint, and you wish the writer hall light without following him back to the cell. The tug loosens at the table, because noise ended without debate and quiet took its place.

Three rooms, one minute each, same shape. Till, table, paper. Lean-in, pity, hands still, mouth talking on, feet staying, noise ending, quiet remaining. No new proof added. Corridor held as seen — gate open, pacing recognised as habit. Dashboard held as seen — belly pull honoured, mouth buzz left to thin. Aisle held as seen — bright packs recognised as build, common recognised as net thrown wide.

That is what holding ends in the social hour. Not a win argued. Not a craving beaten. A tug unfed while ordinary doing goes on — beeping, laughing, buttering — till the aisle behind glass, the plate on the table, the column under the bowl lose command and turn small. The want stays built out there. It no longer builds in you.

I-09 — IGNORE ANY ADVICE THAT CONFLICTS WITH THIS METHOD
Other voices rebuild the Con.

SUMMARY
- The want for bright doses was placed by design, sweetness tuned to keep the hand moving.
- Ubiquity taught the eye to read packets as normal, love, celebration and home.
- The frantic hand at the box is training showing, character was blamed for a loop effect.
- Millions answer the same bells, the mirror lie of unique weakness falls.
- Daily sweet habit points toward flatter mood later, the dose covers dials rather than mending days.
- The body reads hollow and full cleanly when noise is not laid over the signals.
- Fear of falling and fear of shining pull from one owner, both ropes tighten to keep stillness.
- An open gate needs no pacing, an ajar door needs no begging, habit echoes after need ends.
- Kind advice that keeps a dose alive rebuilds the training, sight held keeps the build down.
```
