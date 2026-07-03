# publishing spec

## ADDED Requirements

### Requirement: Founder-gated publication
A book reaches the published state (`books/` or the future site) only after founder review. A book is not published by an agent run alone.

#### Scenario: An agent attempts to publish
WHEN an agent run proposes to mark a book published or move it to `books/`
THEN the action is blocked
AND the founder must review and approve publication.

### Requirement: Published immutability
Published book artifacts are immutable. Corrections to a published book produce a new version, not an in-place edit.

#### Scenario: A published book needs correction
WHEN a correction is needed for an already-published book
THEN a new version is produced (versioned, with a public changelog)
AND the prior version is not edited in place.
