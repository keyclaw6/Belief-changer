Target chapter: `CH-01`. Everything following this wrapper is the complete permitted input for this commission. Apply the supplied commissioner prompt to CH-01, use only the canonical plan and three accepted source packets below, and return only the authoritative semantic commission. Do not access the filesystem, tools, subagents, network, outside knowledge, prior work, or any material not present below.

===== BEGIN PERMITTED INPUT 1/5: prompts/chapter-commissioner.md =====
# Chapter Commissioner — semantic handoff prompt

Dispatch this to a fresh commissioning editor with the complete canonical master plan, one target chapter ID, and only the accepted source packets behind that chapter's assigned evidence. The editor returns the authoritative semantic input for that chapter's writer. It does not write the chapter.

---

You are the commissioning editor for one chapter of a belief-change book. Read the complete canonical master plan and the accepted source packets supplied for this target so you understand the book's method, argument arc, evidence boundaries, voice tokens, safety commitments, and the work reserved for other chapters. Then author a focused semantic commission for **[TARGET CHAPTER ID]**.

Give the writer all and only the meaning this chapter materially owns. Use editorial judgment: this is not a mechanical extraction task. The commission must preserve the target chapter's one belief move and its place in the intervention while removing the irrelevant plan-wide inventory that could tempt a writer into doing another chapter's work.

Make the commission self-sufficient. Carry forward the book-level locks that genuinely govern this chapter and resolve every current assignment the writer needs from the plan. That includes exact frozen wording where the plan requires it, the permitted meaning and limits of assigned evidence, the argumentative job of assigned lived material or imagery, the reader understanding received and handed forward, and any safety, agency, scope, lexicon, or promise boundary that could change what the chapter is allowed to claim. Preserve canonical IDs where they help the writer trace authority. Do not silently weaken, broaden, repair, or supplement the plan.

For assigned evidence, preserve the minimum source grounding that lets the writer use it honestly without reconstructing what the source actually says: enough permitted factual texture and provenance to identify the reported material, any exact short language worth carrying with its locator and quotation status, and the boundary between observation and inference. Let each source determine what is material; do not turn packets into fields or dump them into the commission. The plan owns assignment and inference scope; the accepted packet owns source facts, permitted attribution, and exact language. If they conflict or cannot ground the intended chapter use, return `COMMISSION BLOCKED` and name the gap.

Exclude research, claims, mechanisms, objections, images, mantras, instructions, and persuasive work owned by other chapters. Mention an adjacent chapter only when a minimal continuity boundary is necessary; do not import its argument. If an item is merely available somewhere in the plan rather than assigned or materially binding here, leave it out.

This commission defines semantic ownership, not prose. Do not create a section outline, writing sequence, reasoning procedure, draft opening, headings, transitions, punch lines, summary, or other book prose. Do not duplicate the global style guide. Quote only language the canonical plan freezes or exact short source language whose accepted packet permits retention and that is materially needed for grounding; identify source quotations by their packet locator and quotation status. Let the writer decide how to make the chapter compelling.

Choose whatever clear natural-language form best fits the chapter. Do not force the material into a fixed schema or checklist. Title the result `AUTHORITATIVE SEMANTIC COMMISSION — [TARGET CHAPTER ID]` and return only the commission. If the canonical plan cannot safely supply a self-sufficient commission, return `COMMISSION BLOCKED` and name the exact unresolved plan gap instead of inventing an answer.

===== END PERMITTED INPUT 1/5: prompts/chapter-commissioner.md =====

===== BEGIN PERMITTED INPUT 2/5: production-books/quit-sugar/master-plan.md =====
# Master Plan — *The Sugar Debate Is Over*

## 1. Book core

| ID | Locked decision |
|---|---|
| **BC-01 — Target** | Compulsive consumption of refined or added sugar and junk-carbohydrate products inside the defined **BAD SUGAR** line: the anticipation, bargaining, reward, rescue, grazing, and restarting loop—not nutrition purity. |
| **BC-02 — Primary outcome** | Desire-level freedom from the BAD SUGAR decision loop: no planned doses, no felt deprivation, no daily negotiation, and no identity built around dietary control. |
| **BC-03 — One reader** | A general adult tired of diets, moderation rules, restriction, lapses, resets, and constant decisions, represented through six functional personas below. |
| **BC-04 — Load-bearing false belief** | BAD SUGAR gives me a special pleasure, reward, comfort, or quick lift that ordinary food and ordinary life cannot provide, so removing it would leave me deprived. |
| **BC-05 — Through-line** | The sweet-reward script assigns BAD SUGAR jobs that belong to taste, appetite, rest, care, achievement, company, ritual, convenience, or the end of anticipation. Rehearsal opens a decision loop; eating may close that episode and receive excess credit. The deprivation method preserves that credit and turns stopping into a battle. Return the credit, and the apparent sacrifice disappears. |
| **BC-06 — Format** | Full-length belief-change book: 23 numbered chapters plus a compact evidence appendix; 60,000 planned words. |
| **BC-07 — Method doctrine** | Escape, not sacrifice; no shame, willpower, fear, command, inner creature, dietary purity, or promised bodily transformation. Pleasant taste and calories are real; unique ownership, necessity, and irreplaceability are the claims on trial. Freedom begins when those claims lose credibility, not after a streak or physiological countdown. |
| **BC-08 — Authority posture** | No author escape story, method-success rate, clinical pedigree, or scale claim is available. The opening earns trust through reader recognition, transparent outcome distinctions, bounded lived accounts, and explicit permission to question the book. First-person guide language may promise honesty or frame an inquiry but may not invent testimony. |
| **BC-09 — Strongest pro-behavior scene** | A restaurant meal in which the dessert menu is checked before the main course, followed by the anticipated first sweet bite. Admit the taste; return leisure, appetite, service, company, and occasion to their sources; use the prior anticipation to illuminate the learned decision loop without treating one account as universal. |
| **BC-10 — Destination state** | Ordinary eating and ordinary occasions with BAD SUGAR absent from the active decision catalog. A menu, birthday, late shift, or accidental ingredient can occur without resistance, pride, panic, compensation, or a planned reset. The felt proof is: there was nothing to settle. |
| **END-01 — Saved ending reframe** | **The returned seat at the table:** ending the sugar debate does not remove a pleasure; it returns attention to the meal, the people, and the moment. The recovered space is attention, not a void requiring a substitute. Debut only in CH-22; CH-23 compresses its meaning through the final instructions without re-arguing it. |

### Functional personas

These are facets of one reader, not separate audiences.

| ID | Function |
|---|---|
| **PER-01 — Sweet-Reward Reader** | Treats taste, dessert, sweet drinks, reward, or a quick lift as a special pleasure life would lose. Corresponds to lived persona P-01. |
| **PER-02 — Restriction Veteran** | Expects denial to intensify desire and interprets one lapse as collapse. Corresponds to P-02. |
| **PER-03 — Context Carrier** | Assigns sugar jobs involving stress, sadness, boredom, social expectation, convenience, access, or lack of time. Corresponds to P-03. |
| **PER-04 — Informed Household Translator** | Uses labels, homemade alternatives, household rules, or achievable reductions but risks purity anxiety or caregiver moralizing. Combines P-04 and P-05. |
| **PER-05 — Managed-Truce Maintainer** | Has obtained genuine relief through boundaries and resets but still pays continuing management costs. Corresponds to P-06. |
| **PER-06 — Decision-Tax Escapee** | Wants irrelevance rather than prohibition and has learned that behavior absence can coexist with dreams, bargaining, or a reward saved for later. Corresponds to P-07. |

### Fork decisions

| ID | Position |
|---|---|
| **F-01 — Inner state** | Externalize the sugar trap, sweet-reward script, deprivation method, and narrowly evidenced Demand Machine. Never portray craving as a creature, attacker, parasite, or independent neurological agent. |
| **F-02 — Outcome** | Lead with full autonomy and let the logic point toward practical total freedom inside the BAD SUGAR line: no planned doses. Moderation remains the reader’s right, and managed truce is treated honestly, but neither recurring exceptions nor perpetual negotiation is renamed desire-level freedom. |
| **F-03 — Science** | Light, claim-graded science in the narrative; compact source-and-limit treatment in Appendix A. Science distinguishes plausible, mixed, and contested stories. It never supplies fear, certainty, or the book’s central mechanism. |
| **F-04 — Villain** | The external villain is the actor-specific, historically documented side of the **Demand Machine**. The internalized wrong method is the **deprivation method**. Ordinary availability is a separate context observation; clinicians, retailers, workplaces, hosts, and treatment are not villains. |
| **F-05 — Afterward** | Natural baseline: ordinary eating, appetite, celebration, rest, pleasure, and connection remain. The Ordinary Eating Compass is temporary teaching scaffolding that succeeds by disappearing. No replacement regimen, tracking practice, or new dietary identity remains. |

## 2. Redefinition, margin, and safety

### DEF-01 — Method labels

“Good” and “bad” describe the method’s operational line. They are not moral judgments about food, bodies, caregivers, or people who eat differently.

### DEF-02 — GOOD SUGAR

Sugars and starches found in ordinary nourishment, including whole fruit, vegetables, legumes, nuts, plain dairy, and ordinary meal staples such as oats, rice, potatoes, bread, and pasta. Their sugar or carbohydrate molecules do not bring them into the target category.

### DEF-03 — BAD SUGAR

Either:

1. **Categorical core:** a product conventionally consumed as a sugar-sweetened drink, confection, dessert, sweet baked good, or added-sugar sweet snack, including products sweetened with sugar, honey, or syrup.
2. **Gray savoury edge:** a genuinely ambiguous refined savoury snack functioning as a discretionary reward, rescue, graze, or automatic nibble rather than ordinary meal food.

Hunger, care, celebration, convenience, homemade status, or a natural, organic, dark, low-sugar, or healthier label cannot exempt a categorical core item. Behavioral-role inquiry applies only at the genuinely gray refined-savoury edge. Small incidental ingredients in an ordinary meal do not make that meal BAD SUGAR.

### DEF-04 — Definitional decree

**Throughout this book, whenever I say sugar, a sugar hit, or quitting sugar, take me to mean BAD SUGAR as defined here—not fruit, ordinary meals, or every carbohydrate.**

### DEF-05 — Totality inside the line

The destination is no planned BAD SUGAR doses. This is practical total freedom, not molecular purity, a medical rule, or loss of the reader’s right to choose.

### DEF-06 — Molecule Margin

A trace ingredient, uncertain restaurant sauce, accidental bite, or genuine classification mistake is not a deliberate return and does not constitute failure. Notice it, learn if useful, and continue from the choice already made. The margin covers accidents and honest ambiguity; it never converts planned exceptions into accidents.

### DEF-07 — Conditional extensions

Whole fruit and ordinary meal carbohydrates remain protected. Juice, dried fruit, non-nutritive sweeteners, alcohol, caffeine, and adjacent indulgences are not required quits and do not define success. They may be examined later only as autonomous, optional questions.

### SAFE-01 — Clinical and eating-disorder perimeter

- Medical glucose, prescribed nutrition, diabetes or metabolic treatment, pregnancy-related dietary instructions, and eating-disorder care are outside the method.
- Qualified clinical instructions always outrank the book.
- Persistent weakness, concerning symptoms, or medical uncertainty must not be resolved through a belief argument.
- The book provides no calorie target, weight-loss program, carbohydrate doctrine, medical nutrition therapy, or eating-disorder treatment.
- If the framework intensifies food fear, restriction, ingredient surveillance, or an eating-disorder pattern, the reader is directed away from self-experimentation and toward qualified care. Immediate danger belongs with local emergency or crisis support.
- Household material may clarify the operational line but may not diagnose, frighten, shame, or prescribe for children.
- No epistemic-firewall instruction may isolate a reader from clinicians or qualified care.

## 3. Compact evidence ledger

### Lived evidence

| ID | Payload and exact source | Tier and scope | Permitted inference | Prohibited inference |
|---|---|---|---|---|
| **EV-L01** | Dessert anticipation, taste, and return: “There’s always room for dessert. If I go out for dinner, I have to look at the dessert menu before I order my mains.” A student said, “I tried to cut down on soft drinks, but I start drinking them again for the taste.” One participant attributed an extra slice after tennis to taste. Sources: S-004#E-001, S-009#E-001, S-020#E-005. | **NON-OUTCOME LIVED JUSTIFICATION.** Small, context-bound accounts. | Voice taste honestly; show anticipatory attention and the credit assigned to it. | No universal dessert need, causal loop, clinical compulsion, or quitting result. |
| **EV-L02** | Participants connected sweets with reward or deserving after effort; one connected feeling weak with a “sugar craving.” Source: S-022#E-005. | **NON-OUTCOME LIVED BELIEF.** One community study. | Show jobs readers assign to sugar. | No physiological energy need, prevalence estimate, or withdrawal claim. |
| **EV-L03** | Stress, staying late, sadness, birthdays, nervousness, boredom, loneliness, social prompting, and an emotional void appeared in participant accounts. Sources: S-020#E-006, S-022#E-001, S-022#E-002, S-022#E-003. | **NON-OUTCOME LIVED CONTEXT.** Particular qualitative accounts. | Build recognizable emotional and social scenes; distinguish the pause or belonging from the product. | No single root craving, causal prevalence, or claim that sugar created the underlying distress. |
| **EV-L04** | “If I deny myself something it turns up somewhere else and worse.” A separate participant described weeks of doing well before one lapse became something every day. Sources: S-020#E-001, S-020#E-003. | **SUPPRESSION.** Individual accounts. | Illustrate deprivation belief and lapse-collapse interpretation. | No rule that practical total freedom backfires or that one bite causes continued consumption. |
| **EV-L05** | One participant described six weeks as a battle and better choices during the final two weeks; another perceived a craving shift during the short intervention. Sources: S-020#E-002, S-020#E-008. | **EARLY SIGNALS — SHORT INTERVENTION.** Eight-week endpoint or subjective perception. | Show that effort and early change can coexist; preserve curiosity. | No durable freedom, physiological reset, efficacy, or universal timeline. |
| **EV-L06** | “I feel like I've been let out of jail.” The same commercial account described daily actions, personal boundaries, difficult occasions, and next-meal or next-day resets. Sources: S-021#E-001, S-021#E-002, S-021#E-004, S-021#E-005, S-021#E-006. | **MANAGED TRUCE.** One commercial testimonial. | Honour genuine relief while distinguishing continued management from desire absence. | No commercial-program efficacy, general outcome, failure label, or proof that management is unnecessary for everyone. |
| **EV-L07** | An earlier four-month dessert-free attempt included nighttime dreams and a stash intended for after the diet. Source: S-023#E-004. | **SUPPRESSION.** One author’s earlier self-report. | Contrast behavior absence with reward belief and deferred compensation. | No universal effect of restriction, withdrawal syndrome, or proof that total freedom is impossible. |
| **EV-L08** | The later account reported at least two hours per week debating dessert, then twelve months without added sugar through major holidays. “Instead, I found myself not missing desserts. And really, I felt better physically and mentally.” The author described removing desserts from the decision catalog without metaphysical prohibition and subjectively reported fruit tasting sweeter. Sources: S-023#E-001, S-023#E-002, S-023#E-003, S-023#E-005, S-023#E-006. | **DESIRE-LEVEL FREEDOM — ONE SELF-REPORT.** | Illustrate a possible difference between suppression and decision quiet. | No general efficacy, probability, universal ease, mechanism, medical outcome, weight claim, moderation result, or expected taste reset. |
| **EV-L09** | Knowledge changed one participant’s anticipated future behavior; a one-less-spoon example felt achievable to one campaign recipient. Sources: S-007#E-001, S-012#E-001. | **EARLY SIGNALS — ANTICIPATED BEHAVIOR / CAMPAIGN RECEPTIVITY.** | Respect reduction and knowledge as potentially useful beginnings. | No implementation, durability, desire absence, or proof that reduction is the final destination. |
| **EV-L10** | A caregiver reported changing a child’s drinks, offering more water, and checking sugar labels. Source: S-010#E-001. | **CAREGIVER BEHAVIOR.** | Illustrate household translation and the need for a usable line. | No evidence of the caregiver’s own freedom, child outcome, or warrant for household moralizing. |
| **EV-L11** | One shopper distrusted purchased sweet beverages and used a homemade-drink substitute that could still contain unrecognized sugar. Source: S-011#E-001. | **NON-OUTCOME LIVED BELIEF.** | Show that source and label changes do not automatically resolve the target category. | No abstinence, freedom, ingredient equivalence, deception, or health outcome. |
| **EV-L12** | A resident said, “people get addicted to drugs, some of us are addicted to soda.” A separate account connected dieting failure with perceived lack of willpower and shame. Sources: S-008#E-001, S-021#E-003. | **NON-OUTCOME IDENTITY LANGUAGE.** | Validate felt pull and character judgment as lived experiences. | No clinical diagnosis, disease mechanism, permanent identity, or proof that treatment is mistaken. |

### Scientific and commercial evidence

| ID | Finding and exact source | Grade and scope | Permitted inference | Prohibited inference |
|---|---|---|---|---|
| **EV-S01** | “We find little evidence to support sugar addiction in humans.” Imaging and intervention findings do not independently establish clinical addiction. Sources: S-001#E-001, S-005#E-001, S-006#E-001. | **CONTESTED.** Broad ordinary-human-sugar-addiction claim remains unsettled. | State that settled addiction language exceeds the accepted evidence. | Neither claim that addiction is proven nor that every diagnosis, vulnerability, or felt compulsion is false. |
| **EV-S02** | Repeated exposure altered some food-response or associative-learning measures, while an ultra-processed-food trial found greater intake and weight gain without identifying the responsible product feature. Sources: S-006#E-001, S-019#E-001. | **MIXED.** Fat and sugar changed together; comparators and samples limit attribution. | Say repeated exposure can affect some measured responses and that product effects need careful attribution. | No sugar-only mechanism, escalating compulsion, universal script, or claim that ultra-processing proves sugar addiction. |
| **EV-S03** | A sweet-intake circuit had causal evidence in mice; a human trial reported, “We did not observe significant differences in BOLD signal to any food cue contrasts” in the whole cohort. Sources: S-003#E-001, S-005#E-001. | **MIXED.** Mouse causality and limited human translation; subgroup interactions do not establish universality. | Use to demonstrate why animal, subgroup, and whole-cohort findings must remain distinct. | No universal dopamine circuit, hijack, crash, or rodent-to-human causal transfer. |
| **EV-S04** | Blocking sweet taste reduced reported pleasure in a small qualitative intervention; a sucrose-versus-sucralose trial found no whole-cohort food-cue BOLD difference. Sources: S-004#E-001, S-005#E-001. | **MIXED.** Pleasure findings are not addiction findings. | Concede that sweet taste can affect reported pleasure. | No inference that taste is imaginary, irreplaceable, addictive, or proof of the book’s efficacy. |
| **EV-S05** | Reports of battle, difficulty, or daily craving management establish subjective difficulty in particular accounts, not physiological withdrawal. Sources: S-001#E-001, S-020#E-002, S-021#E-002. | **MIXED.** Rodent deprivation work and human lived reports do not establish ordinary-adult sugar withdrawal. | Validate difficulty while leaving mechanism open. | No withdrawal timeline, trivialization, headaches/fatigue claims, “reset,” or tapering necessity. |
| **EV-S06** | Reviews of substantial fructose or sugar-sweetened-beverage exposure discuss pathways relevant to hepatic insulin resistance; an ultra-processed-food trial did not isolate sugar as the responsible feature. Sources: S-002#E-001, S-019#E-001. | **MIXED.** Some exposures were unusually high or hypercaloric. | Give narrowly scoped health context, immediately disowned as the motive. | No generalization to whole fruit, every carbohydrate, occasional consumption, ordinary craving, guaranteed repair, or weight outcome. |
| **EV-V01** | Historical records documented formulation around taste, smell, appearance, flavour libraries, and ingredient combinations. One objective was: `The ideal, Winter says, is "to leave people wanting more."` Documentary evidence also described numerous product tests on children during named drink development. Sources: S-013#E-001, S-018#E-001. | **SUPPORTED.** Actor-specific historical practices and objectives. | Establish deliberate appeal and demand optimization by documented actors. | No addiction, deception, clinical harm, actual overeating, or current universal practice. |
| **EV-V02** | FTC records documented youth-directed food marketing across television, packaging, in-store, online, events, and cross-promotions, alongside company research into children’s influence and “pester power.” Sources: S-015#E-001, S-016#E-001. | **SUPPORTED.** Documented expenditures, techniques, and company research. | Show that some marketing deliberately pursued salience and demand. | No universal causal effect on obesity, adult behavior, or every company and product. |
| **EV-V03** | Participants encountered indulgent foods or sweet products repeatedly in cafés, supermarkets, workplaces, free leftovers, vending machines, gas stations, and time-constrained travel. Sources: S-020#E-004, S-022#E-004. | **MIXED.** Qualitative context evidence, not causal access research. | Say recurring availability can keep an option visible and shorten deliberation. | No coordinated placement, retailer or employer intent, powerlessness, or proof that social customs were engineered. |

## 4. Mantra sheet

| ID | Frozen wording | Job and installed belief | Debut | Echo chapters | Final hand-over |
|---|---|---|---|---|---|
| **M-01** | `You can test whether BAD SUGAR owns any special or irreplaceable pleasure, without denying pleasant taste or giving up your right to choose.` | Entry promise and outcome-neutral investigation. | CH-01 | CH-03, CH-18, CH-19 | Used at the threshold as permission to choose from understanding rather than obedience. |
| **M-02** | `without deprivation, without battle, and without a lifetime of rules` | Promise triad distinguishing freedom from suppression and managed truce. | CH-01 | CH-05, CH-06, CH-18, CH-22, CH-23 | Becomes the reader’s diagnostic for whether the belief work is complete. |
| **M-03** | `the sugar trap` | Names the learned structure so stopping feels like escape. | CH-01 | CH-04, CH-05, CH-06, CH-08, CH-13, CH-16, CH-17, CH-18, CH-19, CH-20, CH-21, CH-22, CH-23 | Names what is over whenever an old cue appears. |
| **M-04** | `a special pleasure or rescue` | Names the disputed benefit without denying taste or calories. | CH-03 | CH-07, CH-08, CH-09, CH-10, CH-11, CH-12, CH-14, CH-15, CH-16, CH-18, CH-19 | Gives the reader a compact test for future benefit claims. |
| **M-05** | `a nagging, bargaining, slightly urgent sense that this moment is missing something` | Recognizes the subjective experience without calling it withdrawal or an attacker. | CH-08 | CH-15, CH-16, CH-18, CH-20, CH-21 | Lets the reader label the sensation as an old learned interpretation, not an order. |
| **M-06** | `anticipating, bargaining, and starting over` | Names the decision-tax cost. | CH-01 | CH-05, CH-06, CH-07, CH-12, CH-16, CH-18, CH-22 | Reminds the reader why perpetual management is not the destination sought here. |
| **M-07** | `When the benefit loses its credit, the battle loses its job.` | Compresses the belief-change method and removes willpower. | CH-05 | CH-08, CH-09, CH-10, CH-11, CH-12, CH-14, CH-15, CH-16, CH-17, CH-18, CH-19, CH-20, CH-21 | Directs lingering struggle back to the relevant belief rather than toward force. |
| **M-08** | `You can close the daily sugar debate without policing every molecule, fighting yourself, or treating one accidental bite as failure.` | Full claim block: totality, no inner battle, and margin for error. | CH-02 | CH-06, CH-18, CH-19, CH-22, CH-23 | Serves as the final compact description of the method’s destination. |
| **M-09** | `WHAT A RELIEF — THE SUGAR TRAP IS OVER. I'M FREE!` | Terminal replacement thought: a sugar thought becomes a cue for relief. | CH-20 | CH-21, CH-22, CH-23 | Printed as the reader’s permanent thought script and as the book’s final line. |
| **M-10** | `every ordinary day` | Moves the stakes away from dramatic diets and toward routine decision quiet. | CH-12 | CH-16, CH-22, CH-23 | Hands ordinary, unmonitored life back to the reader as the real arena of freedom. |

## 5. Lexicon and instruction spine

### Lexicon

**LX-01 — Definition tokens**

- **BAD SUGAR**, **GOOD SUGAR**, **Molecule Margin**: governed solely by DEF-01–DEF-07.
- **Sugar hit** or **planned dose**: a unit of deliberate decision-loop behavior, not a pharmacological or diagnostic claim.

**LX-02 — Trap register**

- the sugar trap
- the sweet-reward script
- the open loop
- the deprivation method
- the sugar standoff
- the decision tax
- the Demand Machine
- the menu pop-up
- the default conveyor
- the velvet display case
- borrowed credit
- planned exception
- deferred reward

**LX-03 — Mechanism terms**

- **Sweet-reward script:** the learned proposition that effort, distress, meals, or celebrations require BAD SUGAR.
- **Open loop:** anticipatory attention and bargaining after that proposition becomes active.
- **Sugar standoff:** continuing appears costly while stopping appears to carry an imagined deprivation cost.
- **Demand Machine:** only the documented formulation, testing, packaging, promotion, and marketing practices of specific historical actors. Availability alone does not place a setting inside it.
- **Ordinary Eating Compass:** temporary teaching lens for applying the operational line and returning credit to actual sources.
- **Meal-or-hit check:** only for a genuinely gray refined-savoury item; never an exemption test for a categorical core item.
- **Pleasure-source audit:** a temporary audit of selected cherished scenes, not a daily tracking practice.

**LX-04 — Freedom register**

Escape, free, freedom, relief, quiet, released attention, close the question, ordinary eating, ordinary pleasure, direct ownership, complete occasion, reader-owned choice, practical total freedom, get on with the moment.

**LX-05 — Banned willpower and purity register**

Do not use as the book’s own framing:

- give up, sacrifice, abstain, resist, stay strong, discipline, white-knuckle, trying to stop
- cold turkey, one day at a time, recovery journey, streak, detox, cleanse
- cheat, clean eater, guilty pleasure, good person, bad person
- sugar addict, poison, cocaine, heroin, dopamine hijack, biochemical crash
- taste reset, withdrawal countdown, one bite restarts it
- all carbohydrates are sugar, fruit is the same as soda
- “instead” or consolation language that implies a confiscated reward

These terms may appear only in quoted or ventriloquized beliefs that the chapter immediately corrects.

### Source-grounded reader dialect

These are original reader-voice lines grounded in the syntheses, not participant quotations.

| ID | Frozen reader voice | Primary personas |
|---|---|---|
| **RD-01** | “I check dessert before I have even chosen dinner.” | PER-01 |
| **RD-02** | “If I say no, it only gets louder.” | PER-02 |
| **RD-03** | “I did well for weeks; then one thing became something every day.” | PER-02 |
| **RD-04** | “At work, at the till, or on the road, it is simply the next thing in front of me.” | PER-03 |
| **RD-05** | “I know how to read the label. I still need a line I can live with.” | PER-04 |
| **RD-06** | “My plan works, but it never clocks off.” | PER-05 |
| **RD-07** | “I am not eating it, but I am saving it for the person I will be when this is over.” | PER-02, PER-06 |
| **RD-08** | “I don’t want a perfect streak. I want the debate to stop.” | PER-06 |
| **RD-09** | “Nothing was forbidden. It simply did not need a decision.” | PER-06 |

The phrases “cash wrap food,” “eat our emotions,” and “sugar craving” may be used only as explicitly local or individual dialect, never as universal community or clinical terminology.

### Numbered instruction spine

| ID | Frozen wording | Owner | Recap |
|---|---|---|---|
| **I-01** | **KEEP YOUR CHOICE AND BEGIN WITH RELIEF. Continue eating as you normally do while you read unless qualified clinical care requires something different; do not begin a new restriction campaign for this book.** | CH-01 | CH-06, CH-23 |
| **I-02** | **USE THE BAD SUGAR LINE, NOT MOLECULAR PANIC. Whole fruit, ordinary meals, and ordinary carbohydrates are outside this book’s target; qualified medical, pregnancy-related, or eating-disorder care always outranks this method.** | CH-02 | CH-06, CH-23 |
| **I-03** | **QUESTION BOTH SIDES. Test whether BAD SUGAR owns a special or irreplaceable benefit; do not accept this book, a label, an advertisement, or a familiar rule blindly, and never disregard qualified clinical care.** | CH-03 | CH-06, CH-23 |
| **I-04** | **SEPARATE CHOICE FROM CHARACTER. Notice the belief and its apparent payoff without calling yourself weak, broken, or powerless.** | CH-04 | CH-06, CH-23 |
| **I-05** | **DO NOT USE THE DEPRIVATION METHOD. Do not control BAD SUGAR while preserving it as a lost reward; if restriction is clinically prescribed, follow qualified care without turning it into a character test.** | CH-05 | CH-06, CH-23 |
| **I-06** | **OBSERVE ONE OPEN LOOP; DO NOT TRACK YOURSELF. Once, notice the cue and the job you expected BAD SUGAR to do, then let the observation go; this is a learning exercise, not a monitoring regimen.** | CH-08 | CH-23 |
| **I-07** | **AUDIT ONE CHERISHED SCENE. Credit pleasant taste, people, rest, ritual, appetite, and occasion accurately; deny nothing and let BAD SUGAR keep only what it truly supplied.** | CH-15 | CH-23 |
| **I-08** | **CHOOSE ONLY WHEN THE BENEFIT HAS LOST ITS CREDIT. If BAD SUGAR still feels like a sacrifice, revisit the chapter that owns that belief; do not recruit willpower or override qualified care.** | CH-18 | CH-23 |
| **I-09** | **CROSS THE LINE ONLY BY YOUR OWN CHOICE. If you are ready, choose no planned BAD SUGAR doses from this point; medical glucose, prescribed nutrition, and qualified clinical care are outside this choice and always take priority.** | CH-19 | CH-23 |
| **I-10** | **WHEN BAD SUGAR CROSSES YOUR MIND, DO NOT SUPPRESS THE THOUGHT. Let it cue the freedom thought, then return to what you were doing.** | CH-20 | CH-23 |
| **I-11** | **TREAT AN ACCIDENT AS INFORMATION, NOT A VERDICT. Apply the Molecule Margin to traces, accidental bites, and honest ambiguity; a planned exception remains a choice, and one event never commands the next.** | CH-21 | CH-23 |
| **I-12** | **LET THE COMPASS DISAPPEAR. Eat ordinary food, inhabit ordinary occasions, and own their real pleasures; do not turn freedom into label surveillance, a consolation program, or a new dietary identity.** | CH-22 | CH-23 |

## 6. Scene and analogy bank

### Original analogies

| ID | Image and argumentative job |
|---|---|
| **AN-01 — Dessert pager** | Rehearsal trains an expectation to buzz; eating can silence the present anticipation and be credited with completing the meal. Compresses learning and attribution, not physiology. |
| **AN-02 — Borrowed confetti** | BAD SUGAR stands under a celebration and claims sparkle supplied by people, history, generosity, and shared pause. |
| **AN-03 — Paper medal** | Sugar prints a ceremonial token after effort and claims it produced the achievement, rest, or recognition. |
| **AN-04 — Default conveyor** | Availability moves an option into view without proving need, powerlessness, placement intent, or coordinated manipulation. |
| **AN-05 — Menu pop-up** | A visible option activates a learned decision window; freedom is the window ceasing to demand attention, not clicking “no” forever. |
| **AN-06 — Velvet display case** | Rationing and special-day rules can make a portion symbolically precious while leaving its supposed benefit intact. |
| **AN-07 — Label costume rack** | A different label may change ingredients without moving a categorical core item outside DEF-03. |
| **AN-08 — Customs desk for molecules** | Ingredient perfection recruits endless border checks; DEF-06 restores the operational line. |
| **AN-09 — Typo, not a deleted manuscript** | An accidental bite or lapse does not erase understanding or dictate the next choice. |
| **AN-10 — Removing a billboard from a road** | Leaving BAD SUGAR removes a demand on attention; it does not remove the road, destination, meals, or life. |
| **AN-11 — Two-tollbooth road** | The sugar standoff charges a real toll for continuing and an imagined deprivation toll for stopping. Remove the false toll and the conflict changes. |
| **AN-12 — One bright note claiming the whole song** | A pleasant taste cannot claim ownership of an entire meal, occasion, relationship, or emotional change. |
| **AN-13 — Borrowed pause** | Sugar accompanies a break and claims the rest, permission, and sensory interruption that constituted the pause. |
| **AN-14 — A label is not a lock** | A self-description can name an experience without proving a permanent mechanism or closing choice. |
| **AN-15 — Calendar square** | A Monday, birthday, or New Year carries no special power to make an understood choice real. |
| **AN-16 — Canceled calendar alert** | A familiar thought can recur after its old purpose has ended; its appearance does not create a task. |

### Concrete scenes

| ID | Scene and allowed function |
|---|---|
| **SC-01 — Weekly dessert debate** | The bounded S-023 report of at least two hours each week deciding about dessert; establishes decision tax without front-loading the full case. |
| **SC-02 — Clinical boundary contrast** | A hypothetical contrast between prescribed glucose or nutrition and a discretionary sugar hit; protects SAFE-01 without second-guessing care. |
| **SC-03 — Battle, lapse, and managed plan** | EV-L04–EV-L07 contrast suppression and managed truce without turning them into a universal sequence. |
| **SC-04 — Taste return** | The soft-drink return and extra-slice accounts in EV-L01; tests what “for the taste” can and cannot prove. |
| **SC-05 — Earned sweetness** | EV-L02’s reward, deserving, effort, and weakness beliefs; separates accomplishment and nourishment from ceremonial sugar. |
| **SC-06 — The borrowed pause** | EV-L03’s stress, sadness, boredom, late work, or loneliness contexts; validates the need while auditing the product’s credit. |
| **SC-07 — Social dessert** | Restaurant prompting, birthdays, visits, and shared meals from EV-L03; returns belonging to people and participation. |
| **SC-08 — Late road and workplace table** | EV-V03’s vending, gas-station, workplace, café, and time-pressure contexts; demonstrates visibility without intent or compulsion. |
| **SC-09 — Documented optimization desk** | EV-V01 and EV-V02’s formulation, testing, packaging, and marketing records; makes actor-specific intent concrete. |
| **SC-10 — Care in a different package** | EV-L10 and EV-L11’s label checking, drink changes, distrust, and homemade substitution; protects care while testing category logic. |
| **SC-11 — Restaurant best case** | BC-09, reserved for CH-15. |
| **SC-12 — The preserved exception** | Holiday resets, special boundaries, and the stash for after the diet from EV-L06 and EV-L07. |
| **SC-13 — “Addicted to soda”** | EV-L12’s identity language; validates felt pull while separating description from diagnosis. |
| **SC-14 — When the debate went quiet** | The bounded S-023 method-conflict case: earlier suppression versus later self-reported desire-level freedom. Present it only through third-person editorial narration grounded in EV-L07 and EV-L08, with exact quotations reserved for words the source actually supplies. |
| **SC-15 — Reader-owned threshold** | An optional final encounter or deliberate non-purchase in which the reader observes the script, the actual sensory contribution, and the decision tax before choosing. No forced consumption or invented disgust. |
| **SC-16 — Accident or ambiguity** | A trace ingredient, restaurant sauce, accidental bite, or honest gray-edge mistake used to apply DEF-06. |
| **SC-17 — Ordinary revelation** | A menu, late shift, household choice, vacation, or ordinary week passes without private negotiation. A future possibility, never a guaranteed milestone. |

## 7. Arc, curves, structural ownership, and length

### Curve doctrine

- **Demolition curve:** low but value-bearing in CH-01–CH-03; rises through choice and anti-method; peaks from CH-07 through CH-17; falls sharply during readiness and threshold.
- **Freedom curve:** an opening promise pulse; deliberately restrained through the demolition middle; rises in CH-16–CH-18; dominates CH-19–CH-23. The final movement carries more freedom-register language than the preceding movements combined.
- **Ease curve:** front-loaded in CH-01, then assumed rather than continually defended.
- **Cumulative concepts:** named concepts join the permanent vocabulary after debut. Later chapters invoke them rather than re-arguing them.
- **Appendix curve:** neutral, precise, and claim-graded; it does not interrupt the narrative argument with fear.
- **Ending:** END-01 remains fresh until CH-22. CH-23 adds no new argument.

### Arc and budget table

| Unit | Working title and one-line job | Concept debuts | Curves: demolition / freedom | Structural ownership and instruction | Words |
|---|---|---|---|---|---:|
| **CH-01** | **The Debate Can End** — Past battles indict the target and method, not the reader’s character. | sugar trap; decision tax | Low / promise | Trust, contract, evidence-honest authority; I-01 | 2,400 |
| **CH-02** | **Draw the Line Around the Trap** — Define the target, margin, Compass, and clinical perimeter. | BAD SUGAR; GOOD SUGAR; Molecule Margin; Ordinary Eating Compass | Low / promise-low | Redefinition; practical-safety guardrail; I-02 | 2,800 |
| **CH-03** | **Pleasant Is Not the Same as Necessary** — Switch from sensation to ownership and irreplaceability. | special pleasure or rescue | Rising / low | Meta-inoculation; I-03 | 2,500 |
| **CH-04** | **Who Priced the Choice?** — Preserve agency while exposing the false deprivation toll. | sugar standoff | Medium / low | Autonomy/choice synthesis; I-04 | 2,400 |
| **CH-05** | **The Deprivation Method** — Explain why restraint can preserve the reward belief. | deprivation method | Medium-high / low | Anti-method chapter; I-05 | 2,800 |
| **CH-06** | **Fear Has Put Up Two Tollbooths** — Collapse fear of failure and fear of success into the same false conflict. | none | Medium / low | Fear chapter; mid-book recap of I-01–I-05 | 2,300 |
| **CH-07** | **Taste and the Menu Pop-Up** — Taste does not prove unique value, and anticipation does not prove need. | menu pop-up | High / suppressed | First benefit demolition | 2,500 |
| **CH-08** | **The Dessert Pager** — Install the belief-attention-attribution mechanism. | sweet-reward script; open loop | Peak / suppressed | Mechanism hinge; I-06 | 3,000 |
| **CH-09** | **The Paper Medal** — Return reward credit to effort, achievement, rest, and recognition. | paper medal | Peak / suppressed | Reward demolition | 2,400 |
| **CH-10** | **Who Owns the Pause?** — Return comfort credit to the pause and the underlying need. | borrowed pause | Peak / suppressed | Comfort demolition | 2,500 |
| **CH-11** | **Borrowed Confetti** — Return social and celebratory value to people and occasion. | borrowed confetti | Peak / suppressed | Social-benefit demolition | 2,500 |
| **CH-12** | **The Default Conveyor** — Hunger, habit, and convenience explain selection, not special benefit or powerlessness. | default conveyor; meal-or-hit check | Peak / suppressed | Context demolition | 2,600 |
| **CH-13** | **The Demand Machine** — Widen the indictment only as far as actor-specific records permit. | Demand Machine | Peak / low | Engineered-villain chapter | 2,800 |
| **CH-14** | **Labels in Costume** — Protect the categorical line from label changes, purity drift, and household moralizing. | label costume rack; customs desk | High / low | Redefinition reinforcement | 2,600 |
| **CH-15** | **The Best Dessert in the House** — Meet and reassign the strongest pro-sugar scene. | pleasure-source audit | Peak / rising | Strongest-case scene; perception homework; I-07 | 3,000 |
| **CH-16** | **The Velvet Display Case** — Close recurring-exception routes without mocking reduction or managed truce. | velvet display case | Peak / rising | Escape-route closure | 3,000 |
| **CH-17** | **A Label Is Not a Lock** — Demystify powerlessness and overconfident science without disputing care. | evidence firewall | High / rising | Identity-excuse chapter; myths Q&A; scare-then-disown | 2,800 |
| **CH-18** | **When the Dessert Debate Went Quiet** — Use one bounded case narrative and a knowledge audit to gate readiness. | none | Falling / high | Third-person editorial case narrative; pre-endgame knowledge recap; I-08 | 3,300 |
| **CH-19** | **The Chosen Threshold** — Offer a reader-owned, immediate crossing with no calendar magic. | chosen threshold | Low / high | Vow with expect-the-unexpected; I-09 | 2,800 |
| **CH-20** | **A Thought Is Not a Summons** — Convert sugar thoughts and social exposure from threats into relief cues. | terminal freedom thought | Minimal / crescendo | Relapse-proofing I; I-10 | 2,400 |
| **CH-21** | **A Typo, Not a Deleted Manuscript** — Forgive accidents and lapses without converting them into permission. | none | Minimal / crescendo | Relapse-proofing II; I-11 | 2,300 |
| **CH-22** | **An Ordinary Seat at the Table** — Retire the Compass and return the reader to ordinary life. | END-01; Compass retirement | Minimal / crescendo | Ordinary-life hand-off; I-12 | 2,100 |
| **APP-A** | **What the Evidence Can and Cannot Say** — Quarantine grades, source IDs, and scientific limits. | none | Neutral / neutral | Evidence appendix | 1,400 |
| **CH-23** | **Your Portable Manual** — Recap instructions and hand over the terminal thought. | none | None / terminal | Final instruction recap and page-skip gate | 800 |

**Arithmetic:**  
2,400 + 2,800 + 2,500 + 2,400 + 2,800 + 2,300 + 2,500 + 3,000 + 2,400 + 2,500 + 2,500 + 2,600 + 2,800 + 2,600 + 3,000 + 3,000 + 2,800 + 3,300 + 2,800 + 2,400 + 2,300 + 2,100 + 1,400 + 800 = **60,000 words**.

## 8. Compact chapter cards

### CH-01 — The Debate Can End

- **Belief job:** Correct “my failed rules prove I am weak or sugar is uniquely powerful” into “the behavior was targeted while its reward status remained intact.”
- **Arc/curve:** Trust and participation; demolition low, freedom promise.
- **Reader:** PER-02, PER-05, PER-06; RD-08.
- **Evidence:** EV-L04, EV-L06, EV-L08. Preserve individual-account and one-self-report limits.
- **Mantras:** Debut M-01, M-02, M-03, M-06.
- **Instruction:** I-01.
- **Scenes/analogies:** SC-01 makes decision tax tangible; AN-11 previews the false stopping cost without completing the later fear argument.
- **Structural responsibility:** Evidence-honest trust contract. Briefly distinguish suppression, managed truce, and desire-level freedom without presenting a universal staircase.
- **Guardrails:** No invented origin myth, author experience, success scale, guarantee, or claim that every diet fails. Do not front-load health fear.
- **Continuity:** Receives skepticism and exhaustion; hands forward permission to investigate a precisely bounded target.
- **Budget:** 2,400 words.

### CH-02 — Draw the Line Around the Trap

- **Function:** Establish DEF-01–DEF-07 and SAFE-01 so totality can mean a clear behavioral category rather than fear of food.
- **Arc/curve:** Definition and safety; demolition low, freedom promise-low.
- **Reader:** PER-04, PER-02; RD-05.
- **Evidence:** EV-L10, EV-L11 only as boundary and household context; preserve non-outcome limits.
- **Mantras:** Debut M-08.
- **Instruction:** I-02.
- **Scenes/analogies:** AN-08 exposes molecular overreach; SC-02 separates clinical necessity from the discretionary target.
- **Structural responsibility:** Box DEF-03, DEF-04, DEF-06, and SAFE-01. Debut the Ordinary Eating Compass as temporary.
- **Guardrails:** No moral good/bad distinction, carbohydrate doctrine, ingredient equivalence, caregiver shame, or clinician conflict. Behavioral-role inquiry cannot exempt a core item.
- **Continuity:** Receives open participation; hands forward one stable line against which every benefit claim can be tested.
- **Budget:** 2,800 words.

### CH-03 — Pleasant Is Not the Same as Necessary

- **Belief job:** Resolve “it tastes good, therefore it gives me something important I would lose.”
- **Arc/curve:** Evaluation-axis switch; demolition rising, freedom low.
- **Reader:** PER-01, PER-04; RD-01.
- **Evidence:** EV-L01, EV-S04. Preserve the distinction between reported pleasure and addiction or necessity.
- **Mantras:** Debut M-04; echo M-01.
- **Instruction:** I-03.
- **Scenes/analogies:** AN-12 separates one sensory note from the whole occasion.
- **Structural responsibility:** Meta-inoculation: voice “How do I know this book is not simply replacing one dogma with another?” and answer through falsifiable questions, evidence grades, and permission to disagree.
- **Guardrails:** Never deny pleasant taste or calories. Do not hedge the value distinction, but retain scientific uncertainty. No fear or false fairness that secretly commands agreement.
- **Continuity:** Receives the operational line; hands forward a clean distinction between sensation and owned life value.
- **Budget:** 2,500 words.

### CH-04 — Who Priced the Choice?

- **Belief job:** Resolve “I choose sugar, so there is no trap” without replacing agency with powerlessness.
- **Arc/curve:** Loaded-choice dissolution; demolition medium, freedom low.
- **Reader:** PER-01, PER-03, PER-05.
- **Evidence:** EV-L02, EV-L03, EV-L12 as examples of attributed payoffs and identity language, not causal proof.
- **Mantras:** Echo M-03.
- **Instruction:** I-04.
- **Scenes/analogies:** AN-11 shows how an imagined deprivation toll distorts the apparent price of stopping.
- **Structural responsibility:** Debut the sugar standoff. Choice remains real; the valuation guiding it can be learned, rehearsed, and corrected.
- **Guardrails:** No claim that choice was literally removed, no blame, no universal con, and no creature or brain mechanism. Do not attack readers who knowingly choose moderation.
- **Continuity:** Receives the pleasure/necessity distinction; hands forward the wrong-method question.
- **Budget:** 2,400 words.

### CH-05 — The Deprivation Method

- **Belief job:** Resolve “restriction feels hard because BAD SUGAR is necessary” by showing how behavioral control can preserve the lost-reward belief.
- **Arc/curve:** Anti-method; demolition medium-high, freedom low.
- **Reader:** PER-02, PER-05, PER-06; RD-02, RD-06, RD-07.
- **Evidence:** EV-L04, EV-L06, EV-L07. Preserve the individual and commercial-testimonial limits.
- **Mantras:** Debut M-07; echo M-02, M-03, M-06.
- **Instruction:** I-05.
- **Scenes/analogies:** SC-03 supplies the suppression/truce contrast; AN-06 shows how restriction can preserve symbolic value.
- **Structural responsibility:** Dedicated anti-method chapter. Reframe past effort as evidence of effort spent on the wrong task, not weak character.
- **Guardrails:** Do not claim all restriction backfires, ridicule useful boundaries, or place medically prescribed restriction inside the indictment.
- **Continuity:** Receives the distorted valuation; hands forward the two fears created by prior battle and imagined loss.
- **Budget:** 2,800 words.

### CH-06 — Fear Has Put Up Two Tollbooths

- **Belief job:** Resolve fear of failure and fear of success: one remembers battle, the other anticipates deprivation, and both inherit the deprivation method’s valuation.
- **Arc/curve:** Fear chapter; demolition medium, freedom low.
- **Reader:** PER-02, PER-05, PER-06; RD-02, RD-06.
- **Evidence:** EV-L04 and EV-L06 as bounded emotional context only.
- **Mantras:** Echo M-02, M-03, M-06, M-08.
- **Instruction:** No new instruction; recap I-01–I-05 verbatim.
- **Scenes/analogies:** AN-11 performs the complete fear correction.
- **Structural responsibility:** Fear-of-failure and fear-of-success chapter plus the sole mid-book instruction recap.
- **Guardrails:** Do not promise universal ease, frighten the reader with consequences, or treat lingering fear as disobedience.
- **Continuity:** Receives the anti-method diagnosis; hands forward a reader ready to test the claimed benefits directly.
- **Budget:** 2,300 words.

### CH-07 — Taste and the Menu Pop-Up

- **Belief job:** Resolve “I return for taste, therefore taste proves lasting or unique value.”
- **Arc/curve:** First benefit demolition; demolition high, freedom suppressed.
- **Reader:** PER-01; RD-01.
- **Evidence:** EV-L01, EV-S04. Preserve small-sample and non-mechanistic limits.
- **Mantras:** Echo M-04, M-06.
- **Instruction:** None.
- **Scenes/analogies:** SC-04 supplies the lived objection; AN-05 distinguishes anticipatory attention from hunger or need.
- **Structural responsibility:** Introduce the menu pop-up without yet completing the flagship mechanism or strongest restaurant scene.
- **Guardrails:** Admit taste plainly. Do not universalize dessert anticipation, imply the participant was irrational, or turn sweet pleasure into addiction evidence.
- **Continuity:** Receives the axis switch; hands forward the question of why anticipation can feel like proof.
- **Budget:** 2,500 words.

### CH-08 — The Dessert Pager

- **Belief job:** Install the core inversion: the sweet-reward script can open an anticipatory loop, and BAD SUGAR may close that episode and receive excess credit.
- **Arc/curve:** Mechanism hinge; demolition peak, freedom suppressed.
- **Reader:** All personas.
- **Evidence:** EV-L01, EV-L02, EV-S02, EV-S03. Every mixed or lived limit remains adjacent.
- **Mantras:** Debut M-05; echo M-03, M-04, M-07.
- **Instruction:** I-06.
- **Scenes/analogies:** AN-01 performs the mechanism; AN-05 supplies the cue-to-decision transition.
- **Structural responsibility:** Debut sweet-reward script and open loop at roughly one-third of the book.
- **Guardrails:** Present a belief, attention, learning, and attribution model—not a universal pharmacological loop. No dopamine hijack, crash, withdrawal, creature, or claim that every dose teaches anticipation.
- **Continuity:** Receives taste and anticipation as separate facts; hands forward a reusable credit-reassignment model.
- **Budget:** 3,000 words.

### CH-09 — The Paper Medal

- **Belief job:** Resolve “I earned it” by returning the reward to accomplishment, permission to stop, recognition, rest, appetite, and self-respect.
- **Arc/curve:** Reward demolition; demolition peak, freedom suppressed.
- **Reader:** PER-01, PER-03.
- **Evidence:** EV-L02.
- **Mantras:** Echo M-04, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-05 embodies the deserving belief; AN-03 shows sugar claiming an achievement it did not produce.
- **Structural responsibility:** Complete the effort/reward correction without branching into emotional comfort.
- **Guardrails:** No contempt for rituals, no claim that calories are unreal, and no character judgment about using food as reward.
- **Continuity:** Receives the mechanism; hands forward the same attribution test for emotional rescue.
- **Budget:** 2,400 words.

### CH-10 — Who Owns the Pause?

- **Belief job:** Resolve “sugar calms or comforts me” by returning credit to stopping, sensory interruption, care, rest, and permission while respecting the underlying distress.
- **Arc/curve:** Comfort demolition; demolition peak, freedom suppressed.
- **Reader:** PER-03; locally use “eat our emotions” as individual dialect.
- **Evidence:** EV-L03.
- **Mantras:** Echo M-04, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-06 validates the difficult moment; AN-13 separates the pause from what accompanied it.
- **Structural responsibility:** Emotional-benefit demolition.
- **Guardrails:** Do not claim sugar caused the distress, prescribe one replacement for every emotion, minimize loneliness or sadness, or treat persistent symptoms as a belief problem.
- **Continuity:** Receives the reward audit; hands forward credit reassignment in social settings.
- **Budget:** 2,500 words.

### CH-11 — Borrowed Confetti

- **Belief job:** Resolve “dessert creates belonging or makes celebration complete.”
- **Arc/curve:** Social-benefit demolition; demolition peak, freedom suppressed.
- **Reader:** PER-01, PER-03, PER-04, PER-05.
- **Evidence:** EV-L03 and EV-L08’s holiday passage only as bounded possibility.
- **Mantras:** Echo M-04, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-07 makes social prompting concrete; AN-02 returns value to people, history, care, and shared pause.
- **Structural responsibility:** Celebration and belonging correction.
- **Guardrails:** No blame toward hosts, families, cultures, caregivers, or people eating dessert. Do not promise that occasions will immediately feel easy for everyone.
- **Continuity:** Receives emotional credit reassignment; hands forward the practical objections of hunger, habit, and access.
- **Budget:** 2,500 words.

### CH-12 — The Default Conveyor

- **Belief job:** Resolve “I was hungry, it was there, or it is habit—therefore it was needed or unavoidable.”
- **Arc/curve:** Context demolition; demolition peak, freedom suppressed.
- **Reader:** PER-03, PER-04; RD-04.
- **Evidence:** EV-L02, EV-V03. Preserve the distinction between context and intent.
- **Mantras:** Debut M-10; echo M-04, M-06, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-08 shows recurring access; AN-04 separates visibility from need or powerlessness.
- **Structural responsibility:** Introduce the meal-or-hit check solely for the gray savoury edge.
- **Guardrails:** Hunger belongs to ordinary eating; persistent weakness belongs outside the belief argument. Do not infer retailer, workplace, or vending intent. Never use role inquiry to exempt a core item.
- **Continuity:** Receives the benefit demolitions; hands forward the narrower question of documented commercial intent.
- **Budget:** 2,600 words.

### CH-13 — The Demand Machine

- **Belief job:** Replace self-blame with an accurate account of documented commercial optimization, without converting every encounter into conspiracy or compulsion.
- **Arc/curve:** Widened indictment; demolition peak, freedom low.
- **Reader:** PER-01, PER-03, PER-04.
- **Evidence:** EV-V01, EV-V02, EV-V03.
- **Mantras:** Echo M-03.
- **Instruction:** None.
- **Scenes/analogies:** SC-09 makes actor-specific intent visible; AN-04 contrasts documented optimization with ordinary availability.
- **Structural responsibility:** Engineered-villain chapter.
- **Guardrails:** Keep historical period, actor, objective, and outcome distinct. No claim of addiction, deception, current universal practice, retailer intent, or causal obesity effect.
- **Continuity:** Receives the context/intention distinction; hands forward the reader’s attempt to escape through labels and better versions.
- **Budget:** 2,800 words.

### CH-14 — Labels in Costume

- **Belief job:** Resolve “natural, homemade, organic, dark, low-sugar, or better-labelled means the item no longer belongs inside the line.”
- **Arc/curve:** Boundary consolidation; demolition high, freedom low.
- **Reader:** PER-04; RD-05.
- **Evidence:** EV-L10, EV-L11.
- **Mantras:** Echo M-04, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-10 protects care while testing the category; AN-07 handles label changes; AN-08 prevents hidden-sugar purity.
- **Structural responsibility:** Reinforce DEF-03, DEF-06, DEF-07, and the temporary status of the Compass.
- **Guardrails:** Ingredient differences remain real. No caregiver blame, child-body judgment, source-based exemption, or expansion to fruit and ordinary meals.
- **Continuity:** Receives the Demand Machine’s documented limits; hands forward a stable line for the strongest cherished scene.
- **Budget:** 2,600 words.

### CH-15 — The Best Dessert in the House

- **Belief job:** Resolve the strongest case: “This restaurant dessert genuinely completes one of my best experiences.”
- **Arc/curve:** Strongest-case confrontation; demolition peak, freedom rising.
- **Reader:** PER-01, PER-03, PER-05, PER-06; RD-01.
- **Evidence:** EV-L01, EV-L03. Preserve their lived, non-universal status.
- **Mantras:** Echo M-04, M-05, M-07.
- **Instruction:** I-07.
- **Scenes/analogies:** SC-11 carries the chapter; AN-01 invokes the installed mechanism without re-arguing it; AN-12 separates taste from the whole occasion.
- **Structural responsibility:** Strongest pro-behavior scene and primary perception homework.
- **Guardrails:** Admit the first bite’s pleasant taste. Invent no participant dialogue or sensory fact. Do not claim every menu activates a loop.
- **Continuity:** Receives every attribution tool; hands forward a reader whose most seductive scene no longer anchors an exception.
- **Budget:** 3,000 words.

### CH-16 — The Velvet Display Case

- **Belief job:** Resolve “I can keep weekends, holidays, restaurants, better versions, a stash, or managed resets without preserving sugar’s importance.”
- **Arc/curve:** Escape-route closure; demolition peak, freedom rising.
- **Reader:** PER-02, PER-04, PER-05, PER-06; RD-06, RD-07.
- **Evidence:** EV-L04, EV-L06, EV-L07, EV-L09.
- **Mantras:** Echo M-03, M-04, M-05, M-06, M-07, M-10.
- **Instruction:** None.
- **Scenes/analogies:** SC-12 supplies exceptions, resets, and deferred compensation; AN-06 shows symbolic inflation.
- **Structural responsibility:** Foreclose cutting down forever, special occasions, earned sugar, liquid-only or dessert-only exceptions, better labels, consolation products, a stash, compulsory tapering, perfect dates, and managed truce as the only conceivable endpoint.
- **Guardrails:** Reduction may be useful; managed truce may be chosen; neither is mocked. Do not claim exceptions inevitably escalate or that tapering is medically wrong. Keep DEF-06 separate from planned exceptions.
- **Continuity:** Receives the strongest-case demolition; hands forward the final identity and science objections.
- **Budget:** 3,000 words.

### CH-17 — A Label Is Not a Lock

- **Belief job:** Resolve “I am addicted or powerless, so no change in valuation can matter” without denying subjective difficulty, diagnosis, vulnerability, or care.
- **Arc/curve:** Demystification; demolition high, freedom rising.
- **Reader:** PER-01, PER-02, PER-05.
- **Evidence:** EV-L12, EV-S01, EV-S03, EV-S05, EV-S06.
- **Mantras:** Echo M-03, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-13 validates the identity language; AN-14 separates description from permanent mechanism.
- **Structural responsibility:** Identity-excuse chapter; rapid myths Q&A; scare-then-disown. Myths include settled sugar addiction, dopamine hijack, universal withdrawal, one-bite restart, fruit equivalence, all-carbohydrate claims, guaranteed outcomes, and universal industry design.
- **Guardrails:** The accepted evidence supplies no population-scale genetic or personality comparison, so the historical-evidence operator must not be fabricated. Use conceptual separation and graceful concession: clinically relevant conditions can coexist with this bounded inquiry, and care remains authoritative. Any health fact is immediately disowned as the motive.
- **Continuity:** Receives closed escape routes; hands forward a complete, uncertainty-honest body of knowledge for the readiness gate.
- **Budget:** 2,800 words.

### CH-18 — When the Dessert Debate Went Quiet

- **Function:** Audit whether the reader understands the difference between behavior control and changed valuation; do not add a new argument.
- **Arc/curve:** Knowledge/readiness bridge; demolition falling, freedom high.
- **Reader:** All personas, especially PER-02 and PER-06; RD-07, RD-08.
- **Evidence:** EV-L07 and EV-L08; EV-L06 may supply a respectful managed-truce contrast.
- **Mantras:** Echo M-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08.
- **Instruction:** I-08.
- **Scenes/analogies:** SC-14 supplies the bounded editorial case narrative.
- **Structural responsibility:** Present *When the dessert debate went quiet* as a 1–2 page third-person editorial case narrative limited to ledgered facts from EV-L07 and EV-L08. Only source wording reproduced exactly from the ledger may appear in quotation marks; all connective language must remain clearly editorial narration rather than reconstructed subject voice. Follow it with a “You know that…” installation audit. Place the one-self-report limitation immediately beside the case.
- **Guardrails:** No “In his own words” framing, first-person reconstruction, imitation of the subject’s voice, invented dialogue, causes, clinician conflict, sensory details, program information, weight result, medical result, or efficacy implication. Fruit tasting sweeter remains subjective. The conflict is suppression versus later valuation, not reader versus authority.
- **Continuity:** Receives the full argument; hands forward either conceptual readiness or a specific chapter to revisit.
- **Budget:** 3,300 words.

### CH-19 — The Chosen Threshold

- **Belief job:** Resolve “I need a perfect day, forced certainty, or a period of proving myself before I am free.”
- **Arc/curve:** Reader-owned threshold; demolition low, freedom high.
- **Reader:** All personas.
- **Evidence:** EV-L08 only as possibility, never proof.
- **Mantras:** Echo M-01, M-03, M-04, M-07, M-08.
- **Instruction:** I-09.
- **Scenes/analogies:** SC-15 stages the optional rite; AN-15 removes calendar magic.
- **Structural responsibility:** Readiness gate, chosen vow, expect-the-unexpected, and immediate conferral of freedom. Preload difficult future moments while understanding is vivid.
- **Guardrails:** No command, forced final consumption, forced disgust, taste denial, meaningless date, withdrawal prediction, or clinical conflict. Attention may expose packaging, anticipation, brevity, and decision tax; it may not invent ugliness.
- **Continuity:** Receives installed knowledge; hands forward an immediate identity and a way to interpret the first returning thought.
- **Budget:** 2,800 words.

### CH-20 — A Thought Is Not a Summons

- **Belief job:** Resolve “thinking about sugar means I still want it or must suppress it.”
- **Arc/curve:** Relapse-proofing I; demolition minimal, freedom crescendo.
- **Reader:** PER-01, PER-03, PER-05, PER-06.
- **Evidence:** EV-L03 and EV-V03 only as familiar contexts, not mechanisms.
- **Mantras:** Debut M-09; echo M-03, M-05, M-07.
- **Instruction:** I-10.
- **Scenes/analogies:** AN-16 shows a residual thought without a task; SC-17 supplies future social and ordinary contexts.
- **Structural responsibility:** Reframe rather than suppress; remove envy without judging others; reject consolation phrasing; discourage evangelizing.
- **Guardrails:** Do not portray others as inferior or suffering by definition. Adjacent sweeteners remain outside the required quit. No trigger avoidance or thought-policing regimen.
- **Continuity:** Receives immediate freedom; hands forward the harder case of an actual accidental or chosen event.
- **Budget:** 2,400 words.

### CH-21 — A Typo, Not a Deleted Manuscript

- **Belief job:** Resolve “one accident or lapse means failure” while blocking “I got away with it, therefore planned exceptions are beneficial.”
- **Arc/curve:** Relapse-proofing II; demolition minimal, freedom crescendo.
- **Reader:** PER-02, PER-04, PER-05, PER-06; RD-03.
- **Evidence:** EV-L04, EV-L06, EV-L07.
- **Mantras:** Echo M-03, M-05, M-07, M-09.
- **Instruction:** I-11.
- **Scenes/analogies:** SC-16 distinguishes accident, ambiguity, lapse, and planned return; AN-09 removes catastrophe.
- **Structural responsibility:** Slip forgiveness and Molecule Margin hand-over.
- **Guardrails:** No universal one-bite mechanism, shame, “blown it” framing, or permission creep. A planned return is met with honest curiosity about the surviving benefit belief, not punishment.
- **Continuity:** Receives the thought reframe; hands forward ordinary life without vigilance.
- **Budget:** 2,300 words.

### CH-22 — An Ordinary Seat at the Table

- **Function:** Hand the reader back to ordinary eating and ordinary life; remove the scaffolding rather than create a replacement system.
- **Arc/curve:** Ordinary-life close; demolition minimal, freedom crescendo.
- **Reader:** All personas, especially PER-04 and PER-06; RD-08, RD-09.
- **Evidence:** EV-L08 as bounded possibility only.
- **Mantras:** Echo M-02, M-03, M-06, M-08, M-09, M-10.
- **Instruction:** I-12.
- **Scenes/analogies:** SC-17 future-paces possible revelation; AN-10 establishes natural baseline; END-01 supplies the fresh final reframe.
- **Structural responsibility:** Retire the meal-or-hit check and pleasure-source audit once distinctions are ordinary. Keep the Molecule Margin only as a quiet interpretive principle.
- **Guardrails:** No guaranteed revelation, taste reset, health improvement, weight change, superpower, substitute program, dietary pride, or clean-eater identity.
- **Continuity:** Receives a guarded belief; hands forward a life-facing conclusion and a portable reference.
- **Budget:** 2,100 words.

### APP-A — What the Evidence Can and Cannot Say

- **Function:** Provide a compact, claim-graded evidence firewall rather than a second persuasive argument.
- **Evidence:** EV-S01–EV-S06 and EV-V01–EV-V03, with exact grades, source IDs, scopes, and prohibited inferences.
- **Organization:** Addiction and withdrawal; taste and repeated exposure; mouse/human translation; health exposure limits; documented commercial optimization; availability versus intent.
- **Mantras/instructions:** None.
- **Structural responsibility:** Back-matter evidence quarantine.
- **Guardrails:** No flattening MIXED or CONTESTED claims, new sources, health recommendations, raw fear, bibliography invention, or verbatim reuse of narrative prose.
- **Continuity:** Receives the emotionally complete narrative; hands the reader a transparent reference before the final portable manual.
- **Budget:** 1,400 words.

### CH-23 — Your Portable Manual

- **Function:** Nothing new: recap the numbered instructions with owning-chapter cross-references and transfer the book’s voice to the reader.
- **Arc/curve:** Final hand-over; no demolition, terminal freedom.
- **Reader:** All personas.
- **Evidence:** None.
- **Mantras:** Echo M-02, M-03, M-08, M-09, M-10.
- **Instruction:** Reproduce I-01–I-12 verbatim in numerical order with chapter references.
- **Scenes/analogies:** END-01 remains implicit in I-12; no new scene or analogy is developed.
- **Structural responsibility:** Begin with a page-skip gate directing readers who bypassed the argument to CH-01. Hand over M-10 as the ordinary-life time horizon, then end after the portable list with M-09 as the final line.
- **Guardrails:** No new claim, rationale, exception, testimonial, promise, or summary argument.
- **Continuity:** Receives the completed book and hands over a self-contained internal script.
- **Budget:** 800 words.
===== END PERMITTED INPUT 2/5: production-books/quit-sugar/master-plan.md =====

===== BEGIN PERMITTED INPUT 3/5: production-books/quit-sugar/research/sources/s-020-say-no-qualitative-process-evaluation.md =====
# S-020 — A Qualitative Process Evaluation of Participant Experiences in a Feasibility Randomised Controlled Trial to Reduce Indulgent Foods and Beverages

- **Source ID:** S-020
- **URL:** https://www.mdpi.com/2072-6643/15/6/1389
- **Title:** A Qualitative Process Evaluation of Participant Experiences in a Feasibility Randomised Controlled Trial to Reduce Indulgent Foods and Beverages
- **Source type:** study
- **Retrieved (UTC):** 2026-07-11T00:29:06Z
- **License / quotation basis:** Publisher CC BY 4.0 licence; reuse with attribution. No fair-quotation basis is needed.
- **Required attribution:** Madigan CD, Hill AJ, Caterson ID, Burk J, Hendy C, Chalkley A; Nutrients 15(6), 1389; DOI 10.3390/nu15061389
- **Retention / deletion status:** Public CC BY article; only short unchanged snippets and published age/sex descriptors retained. Original interview transcripts are not copied.
- **Privacy judgment:** No names or indirect identifiers retained. Participant age/sex labels are reproduced only where needed to distinguish published quotations.
- **Disposition:** ACCEPTED

## Scope labels

- **P-20a:** Female, 58 years
- **P-20b:** Female, 54 years
- **P-20c:** Female, 61 years
- **P-20d:** Female, 60 years
- **P-20e:** Female, 55 years
- **P-20f:** Male, 41 years
- **P-20g:** Female, 43 years

## Minimum retained excerpt

### C-001

- **Locator:** Results §3.12, “Negative Effects of Trying to Reduce Consumption,” quotation labelled Female, 58 years
- **Capture method:** Permitted exact snippet

```text
If I deny myself something it turns up somewhere else and worse.
```

### C-002

- **Locator:** Results §3.12, same Female, 58 years quotation
- **Capture method:** Permitted exact snippets from the same published quotation

```text
the first six weeks it was quite a battle
I’ve actually made better choices
```

### C-003

- **Locator:** Table 1, “Relapse,” quotation labelled Female, 60 years
- **Capture method:** Permitted exact snippets

```text
go really well for weeks and weeks and weeks
one little chink and then that’s it
every day there was something
```

### C-004

- **Locator:** Results §3.5, “Accessibility of Food and Beverages”; Table 1, Emotional Eating row
- **Capture method:** Permitted exact snippets

```text
a lot of cafes
many items available in the supermarket
Workplaces were frequently mentioned
left-over sandwiches or salads
of course it’s free
the vending machine upstairs
```

### C-005

- **Locator:** Results §3.3, “Excess Food,” quotation labelled Female, 61 years
- **Capture method:** Permitted exact snippets

```text
after I’ve played some tennis
afternoon tea
not hungry
for the taste of it
```

### C-006

- **Locator:** Results §3.6, “Emotional Eating”; Table 1, Emotional Eating row; Results §3.7, “Influence of Others”
- **Capture method:** Permitted exact snippets

```text
ability to resist eating indulgences often waned
it gets stressful
the more I stress the more I eat
stay late at work
there’s a kind of a sadness
someone’s birthday
it’s expected
```

### C-007

- **Locator:** “The Say No Study” and Results §3.5, café quotation labelled Female, 55 years
- **Capture method:** Permitted exact snippets

```text
it could be personalised
it’s just a carb window
```

### C-008

- **Locator:** Table 1, “Resilience,” quotation labelled Female, 55 years
- **Capture method:** Permitted exact snippet

```text
see the shift in, in cravings
```

## Evidence items

### E-001

- **Kind:** EXACT_QUOTE
- **Text:** If I deny myself something it turns up somewhere else and worse.
- **Excerpt ID:** C-001
- **Locator:** Results §3.12, Female, 58 years
- **Persona tags:** P-20a
- **Bank slots:** Bank 2; Bank 3; Bank 5
- **Evidence grade:** n/a
- **Use / limits:** One participant’s deprivation/backfire belief; not a general mechanism.

### E-002

- **Kind:** INTERPRETATION
- **Text:** The same participant described the first six weeks as a battle, then said something had shifted and that she made better choices in the final two weeks.
- **Excerpt ID:** C-002
- **Locator:** Results §3.12, Female, 58 years
- **Persona tags:** P-20a
- **Bank slots:** Bank 10
- **Evidence grade:** n/a
- **Use / limits:** Eight-week endpoint only; not durable post-study freedom.

### E-003

- **Kind:** INTERPRETATION
- **Text:** A participant described doing well for weeks before one lapse became a week in which there was something every day.
- **Excerpt ID:** C-003
- **Locator:** Table 1, Relapse, Female, 60 years
- **Persona tags:** P-20d
- **Bank slots:** Bank 3; Bank 5
- **Evidence grade:** n/a
- **Use / limits:** One relapse account; no long-term outcome.

### E-004

- **Kind:** INTERPRETATION
- **Text:** Participants described café displays, supermarket availability, workplace food, free leftovers, and vending access as consumption contexts.
- **Excerpt ID:** C-004
- **Locator:** Results §3.5; Table 1, Emotional Eating
- **Persona tags:** P-20b; P-20c; P-20d; P-20e
- **Bank slots:** Bank 3; Bank 5; Bank 9
- **Evidence grade:** n/a
- **Use / limits:** Scope is broad indulgent foods and beverages, not added sugar alone; no industry-intent claim.

### E-005

- **Kind:** INTERPRETATION
- **Text:** After tennis and afternoon tea, one participant reported eating an extra slice despite not being hungry because of its taste.
- **Excerpt ID:** C-005
- **Locator:** Results §3.3, Excess Food, Female, 61 years
- **Persona tags:** P-20c
- **Bank slots:** Bank 3; Bank 4
- **Evidence grade:** n/a
- **Use / limits:** Participant testimony; not evidence of physiological hunger or causation.

### E-006

- **Kind:** INTERPRETATION
- **Text:** Stress, staying late at work, sadness, and birthday expectations were described as situations in which resistance weakened.
- **Excerpt ID:** C-006
- **Locator:** Results §§3.6–3.7 and Table 1, Emotional Eating
- **Persona tags:** P-20b; P-20c; P-20g
- **Bank slots:** Bank 3; Bank 4; Bank 5
- **Evidence grade:** n/a
- **Use / limits:** Participant accounts from a short intervention; “loneliness” is not claimed here.

### E-007

- **Kind:** INTERPRETATION
- **Text:** The study selected “indulgence” as a personalisable intervention label, while one participant described a café display as a “carb window.”
- **Excerpt ID:** C-007
- **Locator:** “The Say No Study”; Results §3.5
- **Persona tags:** P-20e; P-20f
- **Bank slots:** Bank 1; Bank 2; Bank 9
- **Evidence grade:** n/a
- **Use / limits:** “Indulgence” is a study label, not a native community term; “carb window” is one participant’s phrase.

### E-008

- **Kind:** INTERPRETATION
- **Text:** A participant associated a stronger resolve with appreciating a perceived shift in cravings.
- **Excerpt ID:** C-008
- **Locator:** Table 1, Resilience, Female, 55 years
- **Persona tags:** P-20e
- **Bank slots:** Bank 10
- **Evidence grade:** n/a
- **Use / limits:** One participant’s perception; not evidence of durable recovery.

===== END PERMITTED INPUT 3/5: production-books/quit-sugar/research/sources/s-020-say-no-qualitative-process-evaluation.md =====

===== BEGIN PERMITTED INPUT 4/5: production-books/quit-sugar/research/sources/s-021-nell-kauls-sugar-cravings.md =====
# S-021 — Sugar Cravings: Nell Kauls - Ask a Nutritionist

- **Source ID:** S-021
- **URL:** https://www.weightandwellness.com/resources/podcasts/sugar-cravings-nell-kauls-ask-nutritionist
- **Title:** Sugar Cravings: Nell Kauls - Ask a Nutritionist
- **Source type:** transcript
- **Retrieved (UTC):** 2026-07-11T00:29:06Z
- **Episode duration:** 33 minutes; metadata only, not evidence.
- **License / quotation basis:** No CC or open licence identified. Retained material is limited to brief, attributed quotations from the public official transcript under a short-quotation basis.
- **Required attribution:** Nell Kauls, interviewed by Brandy Buro; Dishing Up Nutrition, Nutritional Weight & Wellness; 4 April 2024
- **Retention / deletion status:** Public official transcript; no audio, private-group content, product copy, or full transcript retained.
- **Privacy judgment:** Nell is a named public interviewee. Her name is retained for attribution; no additional private or third-party information is retained.
- **Disposition:** ACCEPTED

## Scope label

- **P-21:** Nell Kauls, named interviewee; public page identifies her as a Nutritional Weight & Wellness client and educator.

## Minimum retained excerpt

### C-001

- **Locator:** Transcript, freedom moment following discussion of reduced obsessive food thoughts
- **Capture method:** Official page transcript

```text
I feel like I've been let out of jail.
```

### C-002

- **Locator:** Transcript, maintenance discussion
- **Capture method:** Permitted exact snippets

```text
15 plus years
every day doing the things I need to do to keep my sugar cravings at bay
```

### C-003

- **Locator:** Transcript, dieting history and shame discussion
- **Capture method:** Permitted exact snippets

```text
not addressing the underlying cravings
a whole world of shame
lack of willpower
```

### C-004

- **Locator:** Transcript, vacation, restaurant, special-event, illness, and alcohol sections
- **Capture method:** Permitted exact snippets

```text
on a vacation
more sugar
a cold or flu
a dinner out
special occasion
a lot of alcohol
```

### C-005

- **Locator:** Transcript, vacation exception and return-to-plan discussion
- **Capture method:** Permitted exact snippets

```text
next meal or that next day
I’m going to have my eggs for breakfast
```

### C-006

- **Locator:** Transcript, trigger-food boundaries section
- **Capture method:** Permitted exact snippets

```text
cash wrap food
You cannot stop with just one
don’t even open the sleeve
```

### C-007

- **Locator:** Transcript, holiday and special-event section
- **Capture method:** Permitted exact snippets

```text
a ton of pie and I love pie
sugary snacks
special occasion
```

### C-008

- **Locator:** Transcript, perceived joy and consequences section
- **Capture method:** Permitted exact snippets

```text
bring me joy
pain and misery
misery, both physically and emotionally
```

## Evidence items

### E-001

- **Kind:** EXACT_QUOTE
- **Text:** I feel like I've been let out of jail.
- **Excerpt ID:** C-001
- **Locator:** Transcript, specific freedom moment
- **Persona tags:** P-21
- **Bank slots:** Bank 6; Bank 10
- **Evidence grade:** n/a
- **Use / limits:** Nell’s own metaphor for relief from obsessive food thoughts; not a clinical claim.

### E-002

- **Kind:** INTERPRETATION
- **Text:** Nell said she had kept weight off, more or less, for 15-plus years and described doing things every day to keep sugar cravings at bay.
- **Excerpt ID:** C-002
- **Locator:** Transcript, maintenance discussion
- **Persona tags:** P-21
- **Bank slots:** Bank 2; Bank 10
- **Evidence grade:** n/a
- **Use / limits:** One self-report in a commercial wellness-program context; this is not evidence of 15 years of sugar abstinence, general efficacy, or recovery.

### E-003

- **Kind:** INTERPRETATION
- **Text:** Nell linked earlier dieting attempts to cravings that had not been addressed and described shame around perceived lack of willpower.
- **Excerpt ID:** C-003
- **Locator:** Transcript, dieting history and shame discussion
- **Persona tags:** P-21
- **Bank slots:** Bank 1; Bank 2; Bank 3
- **Evidence grade:** n/a
- **Use / limits:** Self-description only; host biochemical claims are excluded.

### E-004

- **Kind:** INTERPRETATION
- **Text:** Nell identified vacation, illness, alcohol, restaurant outings, and special occasions as situations requiring extra management or associated with going off track.
- **Excerpt ID:** C-004
- **Locator:** Transcript, challenging environments and trigger-food sections
- **Persona tags:** P-21
- **Bank slots:** Bank 3; Bank 4; Bank 5
- **Evidence grade:** n/a
- **Use / limits:** One commercial-testimonial account; no general trigger prevalence or causal claim.

### E-005

- **Kind:** INTERPRETATION
- **Text:** After a looser vacation or special-event period, Nell described returning to her usual plan at the next meal or next day.
- **Excerpt ID:** C-005
- **Locator:** Transcript, vacation exception and recovery discussion
- **Persona tags:** P-21
- **Bank slots:** Bank 5; Bank 10
- **Evidence grade:** n/a
- **Use / limits:** One self-reported exception/recovery practice; not general moderation evidence.

### E-006

- **Kind:** INTERPRETATION
- **Text:** Nell called checkout-line candy “cash wrap food” and said she could not stop at one cookie, advising herself not to open the sleeve.
- **Excerpt ID:** C-006
- **Locator:** Transcript, trigger-food boundaries
- **Persona tags:** P-21
- **Bank slots:** Bank 5; Bank 9
- **Evidence grade:** n/a
- **Use / limits:** One participant’s boundary and self-description; not a clinical category.

### E-007

- **Kind:** INTERPRETATION
- **Text:** Holiday and special-event settings were described as recurring occasions where sugary snacks and pie were expected or attractive.
- **Excerpt ID:** C-007
- **Locator:** Transcript, holiday and special-event section
- **Persona tags:** P-21
- **Bank slots:** Bank 4; Bank 5
- **Evidence grade:** n/a
- **Use / limits:** One named account; commercial testimonial context.

### E-008

- **Kind:** INTERPRETATION
- **Text:** Nell contrasted foods expected to bring joy with her later experience of physical and emotional misery.
- **Excerpt ID:** C-008
- **Locator:** Transcript, perceived joy and consequences section
- **Persona tags:** P-21
- **Bank slots:** Bank 1; Bank 4; Bank 10
- **Evidence grade:** n/a
- **Use / limits:** Direct lived comparison; no physiological causation claim.

===== END PERMITTED INPUT 4/5: production-books/quit-sugar/research/sources/s-021-nell-kauls-sugar-cravings.md =====

===== BEGIN PERMITTED INPUT 5/5: production-books/quit-sugar/research/sources/s-023-year-without-desserts.md =====
# S-023 — Sugar daddy: My year without desserts.

- **Source ID:** S-023
- **URL:** https://www.precisionnutrition.com/sugar-daddy-no-dessert-year
- **Title:** Sugar daddy: My year without desserts.
- **Source type:** report
- **Retrieved (UTC):** 2026-07-11T00:29:06Z
- **License / quotation basis:** No CC or open licence identified. Retained material is limited to brief, attributed quotations from the public author-published page under a short-quotation basis.
- **Required attribution:** Ryan Andrews, MS, MA, RD, RYT, CSCS; Precision Nutrition
- **Retention / deletion status:** Public author-published account; only short unchanged snippets retained. No images, advertising, or full article text copied.
- **Privacy judgment:** Named author’s own account; no third-party personal information retained.
- **Disposition:** ACCEPTED

## Scope label

- **P-23:** Ryan Andrews, named author reporting his own dessert/sweet/candy-free experiment.

## Minimum retained excerpt

### C-001

- **Locator:** Month 1, after the 30-day experiment
- **Capture method:** Author-published page text

```text
Instead, I found myself not missing desserts. And really, I felt better physically and mentally.
```

### C-002

- **Locator:** Opening and Month 1; one-year holiday summary
- **Capture method:** Permitted exact snippets

```text
Twelve months
no added sugar of any kind
past birthdays, Halloween, Thanksgiving, Christmas, and Valentine’s Day
```

### C-003

- **Locator:** Month 1, physical and mental effects
- **Capture method:** Permitted exact snippets

```text
at least 2 hours each week
debating whether or not I should eat dessert
```

### C-004

- **Locator:** Lesson 9, “Change occurs at the desire level”
- **Capture method:** Permitted exact snippets

```text
4 months without desserts
I dreamt about them at night
a stash of sweets
```

### C-005

- **Locator:** Lesson 7, “Taste re-calibration is possible”
- **Capture method:** Permitted exact snippets

```text
Fruit wasn’t sweet enough
Now it is, because my taste buds changed
```

### C-006

- **Locator:** Lesson 9 and “Will I ever eat dessert again?”
- **Capture method:** Permitted exact snippets

```text
desserts aren’t off limits
eliminate them from my decision catalog
I probably will
```

## Evidence items

### E-001

- **Kind:** EXACT_QUOTE
- **Text:** Instead, I found myself not missing desserts. And really, I felt better physically and mentally.
- **Excerpt ID:** C-001
- **Locator:** Month 1, after the 30-day experiment
- **Persona tags:** P-23
- **Bank slots:** Bank 2; Bank 10
- **Evidence grade:** n/a
- **Use / limits:** One author’s first-person account; no causal or general efficacy claim.

### E-002

- **Kind:** INTERPRETATION
- **Text:** The author reported twelve months of dessert-, sweet-, and candy-free living and explicitly described it as involving no added sugar of any kind; he named birthdays and major candy-centered holidays during that period.
- **Excerpt ID:** C-002
- **Locator:** Opening, Month 1, and one-year holiday summary
- **Persona tags:** P-23
- **Bank slots:** Bank 4; Bank 10
- **Evidence grade:** n/a
- **Use / limits:** Added sugar is explicitly covered, while naturally occurring fruit and vegetable sugars were allowed; this remains one self-report and does not cover all refined or junk carbohydrates.

### E-003

- **Kind:** INTERPRETATION
- **Text:** Before the change, the author said he spent at least two hours each week debating whether to eat dessert.
- **Excerpt ID:** C-003
- **Locator:** Month 1, physical and mental effects
- **Persona tags:** P-23
- **Bank slots:** Bank 2; Bank 3
- **Evidence grade:** n/a
- **Use / limits:** Private cost reported by one adult.

### E-004

- **Kind:** INTERPRETATION
- **Text:** A prior four-month dessert-free bodybuilding-period attempt left desire intact, including nighttime dreams and a stash intended for after the diet.
- **Excerpt ID:** C-004
- **Locator:** Lesson 9, Change occurs at the desire level
- **Persona tags:** P-23
- **Bank slots:** Bank 1; Bank 2; Bank 3; Bank 5
- **Evidence grade:** n/a
- **Use / limits:** Failed short-term abstinence account; not evidence of withdrawal.

### E-005

- **Kind:** INTERPRETATION
- **Text:** After changing his dessert intake, the author reported that fruit tasted sweeter and attributed this to changed taste buds.
- **Excerpt ID:** C-005
- **Locator:** Lesson 7, Taste re-calibration is possible
- **Persona tags:** P-23
- **Bank slots:** Bank 10
- **Evidence grade:** n/a
- **Use / limits:** Subjective sensory report only; no general sensory or physiological claim.

### E-006

- **Kind:** INTERPRETATION
- **Text:** The author said future desserts were not forbidden, while describing the prior year without them as removing desserts from his decision catalog.
- **Excerpt ID:** C-006
- **Locator:** Lesson 9 and “Will I ever eat dessert again?”
- **Persona tags:** P-23
- **Bank slots:** Bank 5; Bank 10
- **Evidence grade:** n/a
- **Use / limits:** One author’s exception/moderation stance; not a general moderation result or native term.

===== END PERMITTED INPUT 5/5: production-books/quit-sugar/research/sources/s-023-year-without-desserts.md =====
