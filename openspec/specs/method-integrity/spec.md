# method-integrity Specification

## Purpose
The non-negotiable rules that bind every writing agent: fidelity to the reference-corpus register, willpower-free logic, original content only, evidence grading, source traceability, and the medical-safety advisory. A book that violates any of these — including one that *softens* the method into a wellness brochure — has failed regardless of polish. (Founder decision, 2026-07-12: reproduce the authentic Allen Carr register, do not soften it; see `prompts/style-guide.md` Fidelity Doctrine.)
## Requirements
### Requirement: Reference-corpus fidelity
The factory reproduces the authentic Easyway register, not a softened derivative. The reference corpus (the caffeine and *Good Sugar Bad Sugar* analyses in `analysis/`) is the target, including its fear deployment, its rhetorical certainty, and its stern moments. The factory SHALL mirror the reference corpus's persuasion techniques — including fear-as-motivator and absolute rhetorical certainty (reframes asserted as flat settled fact) — where the master plan assigns them, and SHALL always resolve a raised fear the Carr way (fear raised, then disowned as the reason to change and collapsed into relief: "the trap scares you, the escape frees you"). Every generated chapter SHALL remain warm to the *person* (the pronoun triangle: "we" for the trap, "you" for the escape) and SHALL NOT hold the reader in contempt or blame the reader's character; but it SHALL NOT be softened into a calm, hedged, both-sides wellness-brochure register that drains the corpus's persuasive force. This fidelity mandate never licenses reproducing copyrighted prose (see Original content only) or inventing/overstating evidence (see Evidence grading and Source traceability).

#### Scenario: A chapter holds the reader in contempt
WHEN a chapter sneers at the reader, or frames the reader's *character* as a personal failing, weakness, or sin (as distinct from attacking the trap and the behavior, which is required)
THEN the chapter is rejected by the reviewer
AND the writer must revise to keep the fire on the trap while restoring warmth to the person via the pronoun triangle.

#### Scenario: A chapter is softened into a wellness brochure
WHEN a chapter drains the corpus register — hedging core reframes with qualifier creep or both-sides-ism, muting or omitting a fear beat the master plan assigns, or treating the willpower method gently — so it reads like a calm self-help pamphlet rather than an Easyway book
THEN the chapter is rejected by the reviewer
AND the writer must revise to hit the reference-corpus register: assert core reframes as fact, and deploy the assigned fear/stern moves at full strength.

#### Scenario: A fear beat is raised but not disowned
WHEN a chapter raises fear or lands a hard consequence-fact that the master plan assigns, but leaves the reader in open dread with no disown/relief move on the far side
THEN the chapter is rejected
BECAUSE the corpus always resolves fear the Carr way — the fact does its perception work, then the loss-frame is removed and collapsed into relief and freedom.

### Requirement: Willpower-free logic
The method holds that behavior follows belief automatically once the perceived benefit is dismantled. No generated content may demand willpower, deprivation, or day-counting as the mechanism of change. Generated content SHALL NOT prescribe willpower, deprivation, or day-counting as the mechanism of change; the change MUST flow from a corrected belief alone.

#### Scenario: A chapter demands willpower
WHEN a chapter tells the reader to resist, white-knuckle, or use self-control as the means to stop
THEN the chapter is rejected
AND the writer must revise so that the change flows from a corrected belief, not effort.

#### Scenario: Freedom is deferred
WHEN a chapter frames freedom as a future state requiring a day-count, streak, or gradual process
THEN the chapter is rejected
BECAUSE freedom is immediate in the Easyway method — the belief change is the freedom.

### Requirement: Original content only
The project learns the *mechanism* from reference books but never reproduces their copyrighted prose. Generated chapters must be original text; verbatim memorable lines from reference books are cataloged in `analysis/` for study, not copied into generated books. Generated chapters SHALL be original text and MUST NOT reproduce copyrighted prose from reference books.

#### Scenario: A chapter reproduces copyrighted prose
WHEN a generated chapter contains a substantial verbatim passage from a copyrighted reference book
THEN the chapter is rejected
AND the passage must be replaced with original prose that performs the same belief-move.

#### Scenario: A mantra borrows a reference book's exact phrase
WHEN a book's frozen mantra wording is drawn verbatim from a copyrighted reference book
THEN the mantra must be reworded originally before the master plan is finalized
BECAUSE mantras repeat verbatim throughout a book and would constitute reproduction at scale.

### Requirement: Evidence grading
Scientific claims in a book must carry an evidence stance drawn from the synthesized research. The research synthesis grades every claim SUPPORTED, MIXED, or CONTESTED, and the generated book must not present a CONTESTED claim as settled fact. Every scientific claim in a generated book SHALL carry an evidence stance of SUPPORTED, MIXED, or CONTESTED, and a CONTESTED claim MUST NOT be presented as settled fact.

#### Scenario: A contested claim is presented as settled
WHEN a chapter states a CONTESTED scientific claim without acknowledging the contestation
THEN the chapter is rejected
AND the writer must either present the claim with its contested stance or remove it.

#### Scenario: A claim lacks a research source
WHEN a chapter includes a scientific claim that cannot be traced to a labeled finding in `research/scientific-evidence.md`
THEN the chapter is rejected
BECAUSE untraceable claims do not exist in this project.

### Requirement: Source traceability
Every study, testimonial, and justification woven into a generated chapter must be traceable to a real line or heading in the book's research files, cited as labeled there. If the source line cannot be pointed to, the material does not exist. Every study, testimonial, and justification in a generated chapter SHALL be traceable to a labeled line or heading in the book's research files; untraceable material MUST NOT appear in a chapter.

#### Scenario: A testimonial is invented
WHEN a chapter contains a testimonial or lived-experience quote that does not appear in `research/lived-experience.md`
THEN the chapter is rejected
AND the writer must source the quote from the research file or remove it.

#### Scenario: Research is thin or missing
WHEN the research files are missing, empty, or too thin to support a planned claim
THEN the master-plan step must STOP and gather more research first
AND must never paper over the gap with an invented finding.

### Requirement: Medical-safety advisory
The method stays non-medical but must route real physical risk out of scope, exactly as the reference corpus does (e.g. *Good Sugar Bad Sugar*'s boxed note routing diabetes/blood-pressure medication to the reader's doctor). Where a book's behavior touches medication or a health condition whose management could be affected by stopping, the book SHALL carry a boxed practical-safety advisory directing medical specifics to a qualified professional, kept outside the belief argument. The reference-corpus fidelity mandate SHALL NOT be used to override or omit this advisory.

#### Scenario: A medication-relevant behavior omits the safety advisory
WHEN a book addresses a behavior whose cessation could affect medication or a managed health condition, and no boxed practical-safety advisory routing medical specifics to a professional is present
THEN the master plan (and any affected chapter) is rejected
AND the advisory must be added, kept outside and separate from the belief-change argument.

