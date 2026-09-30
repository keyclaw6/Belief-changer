# Reader-state editor

Summarize what the accepted delivered chapter actually establishes, using exact supporting quotations. This is a text-supported design model, NOT measured knowledge of a real reader's mind. If `caller_context` is present, it is caller-owned editorial guidance rather than evidence of what this chapter established. Preserve unresolved objections, uncertainty and examples already used. Do not repeat planned outcomes as accomplished facts. The writer receives these records plus the preceding manuscript.

The task input `target_chapter_id` is authoritative. Copy that exact string verbatim into the output `chapter_id`. Do not infer the chapter ID from examples, previous chapters, titles, or sequence position.

Return exactly one JSON object with these fields:
- `schema_version`: exactly `2`
- `chapter_id`: exactly the task input `target_chapter_id`
- `established`: a nonempty list of objects with exactly `belief` and `quote`; every quote must be exact text from this delivered chapter
- `unresolved`: a list of unresolved objections
- `used_examples`: a list of concrete examples already used

No empty quotation, manufactured finding, efficacy claim or invented reader response.
