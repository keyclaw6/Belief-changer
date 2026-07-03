# languages spec

## ADDED Requirements

### Requirement: English-first
Books are authored in English first. English is the default and baseline language; no additional language is produced until a spec change adds it. Books SHALL be authored in English first, and no additional language MUST be produced until a spec change adds it.

#### Scenario: A book is begun
WHEN a new book is started
THEN it is authored in English
AND no translation or non-English native generation is produced without a prior languages spec change.

### Requirement: Adding a language is a spec change
Each additional language is introduced by an explicit openspec change. For each language, the change decides per book whether the target is translation of the English book or native generation, and establishes the one frozen translation per mantra (mantras are repeated verbatim, so each mantra gets exactly one frozen translation per language). Each additional language SHALL be introduced by an explicit openspec change, and that change MUST record per book whether the path is translation or native generation and MUST establish exactly one frozen mantra translation per language.

#### Scenario: A language is proposed
WHEN a new language is proposed for a book
THEN an openspec change under `openspec/changes/<slug>/` is authored
AND the change records, for each affected book, whether the path is translation or native generation
AND the change establishes the frozen per-mantra translation wording.

#### Scenario: A mantra is translated ad hoc
WHEN a translation run paraphrases a mantra differently across chapters
THEN the translation is rejected
BECAUSE mantras repeat verbatim and must have exactly one frozen wording per language.
