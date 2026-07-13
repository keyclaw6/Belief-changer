# method-integrity Specification

## Purpose
The non-negotiable rules that bind every writing agent: Carr-fidelity framing (warm to the reader, harsh to the trap, scares at full force then disowned), willpower-free logic, original content only, evidence grading, source traceability, and the medical-safety advisory. A book that violates any of these has failed regardless of polish.
## Requirements
### Requirement: Carr-fidelity framing
The method works because it reframes the behavior as escaping a trap, not being lectured or shamed. Every generated chapter must address the reader exactly as Carr does: warm to the person, harsh to the trap and the willpower method, commanding with cheerful certainty, delivering assigned hard facts at full force and then explicitly disowning fear as the motivator. Every generated chapter SHALL frame the behavior as an external trap the reader is escaping and SHALL NOT shame or moralize the reader; hard or frightening material SHALL be delivered at Carr's full amplitude and then disowned, never softened or omitted.

#### Scenario: A chapter moralizes the reader
WHEN a chapter frames the reader's behavior as a personal failing, weakness, or sin
THEN the chapter is rejected by the reviewer
AND the writer must revise to reframe the behavior as an external trap the reader is escaping.

#### Scenario: A scare is left standing as the motivator
WHEN a chapter delivers fear, disgust, or hard-fact material and ends the move on that fear as the reason to change
THEN the chapter is rejected
BECAUSE the method changes belief, not mood — the scare does its perception work and is then explicitly disowned (scare-then-disown).

#### Scenario: An assigned scare is softened or skipped
WHEN the master plan assigns hard-hitting material and the chapter hedges, softens, or omits it
THEN the chapter is rejected
BECAUSE omitting the scare Carr would have delivered is register infidelity — the factory matches Carr's amplitude, not a sanitized version of it.

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
The method stays non-medical but must route real physical risk out of scope, exactly as the reference corpus does (e.g. *Good Sugar Bad Sugar*'s boxed note routing diabetes/blood-pressure medication to the reader's doctor). Where a book's behavior touches medication or a health condition whose management could be affected by stopping, the book SHALL carry a boxed practical-safety advisory directing medical specifics to a qualified professional, kept outside the belief argument. The Carr-fidelity framing mandate SHALL NOT be used to override or omit this advisory.

#### Scenario: A medication-relevant behavior omits the safety advisory
WHEN a book addresses a behavior whose cessation could affect medication or a managed health condition, and no boxed practical-safety advisory routing medical specifics to a professional is present
THEN the master plan (and any affected chapter) is rejected
AND the advisory must be added, kept outside and separate from the belief-change argument.
