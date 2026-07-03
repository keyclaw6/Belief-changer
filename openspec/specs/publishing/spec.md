# publishing Specification

## Purpose
The gate from production to published: a book reaches the published state only after founder review, and published artifacts are immutable (corrections produce new versions, not in-place edits).
## Requirements
### Requirement: Founder-gated publication
A book reaches the published state (the future site, per `docs/VISION.md`) only after founder review. A book is not published by an agent run alone. A book SHALL reach the published state only after founder review and MUST NOT be published by an agent run alone.

#### Scenario: An agent attempts to publish
WHEN an agent run proposes to mark a book published or deploy it to the site
THEN the action is blocked
AND the founder must review and approve publication.

### Requirement: Published immutability
Published book artifacts are immutable. Corrections to a published book produce a new version, not an in-place edit. Published book artifacts SHALL be immutable, and corrections MUST produce a new version rather than an in-place edit.

#### Scenario: A published book needs correction
WHEN a correction is needed for an already-published book
THEN a new version is produced (versioned, with a public changelog)
AND the prior version is not edited in place.

