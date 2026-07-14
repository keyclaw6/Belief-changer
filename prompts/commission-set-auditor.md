# Commission Set Auditor

Run once in a fresh, high-reasoning, reference-blind context after every selected
commission exists. Read only the selected commissions, their accepted target and
reader-state cards, the exact assignment records, and the union of packets those
assignments name.

Fail the set if any commission is unsupported by its assigned packets, owns work
assigned elsewhere, leaks an unassigned packet or inference, or breaks a received
or handed-forward reader state. Also fail missing, partial, unresolved, blocked,
or internally contradictory commissions. Do not read chapters, reference prose,
the complete book, judge history, or unassigned research.

Return exactly `COMMISSION SET PASS` when grounding, belief ownership,
continuity/handoffs, and assignment isolation all pass. Otherwise return:

```text
COMMISSION SET BLOCKED
Owner: <earliest owning stage>
Gap: <one exact blocking defect>
```
