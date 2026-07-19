"""Exact six-call H-F01 RF21/RF22 native contract."""
import re

IDS = ("rf21-plan", "rf21-plan-review", "rf22-commission-01",
       "rf22-commission-02", "rf22-commission-03", "rf22-audit")
ROLES = ("integrated reader-journey planner", "independent planning-family reviewer",
         "chapter commissioning editor", "chapter commissioning editor",
         "chapter commissioning editor", "commission-set auditor")
LADDER = {"stage_a": "quit-sugar opening parity against offset-matched GSBS",
    "stage_b": "RF-30 complete quit-sugar book parity",
    "stage_c": "RF-31 untouched caffeine with zero generic tuning",
    "order": ["RF-25", "RF-30", "RF-31"]}
REQUIRED = ("assumptions received", "entering belief", "leaving belief", "situation",
    "reader wording", "permitted mechanism", "emotional turn", "empirical limits",
    "safety limits", "handoff", "assumptions handed forward", "reserved work")
SOURCE = ("situation", "reader wording", "permitted mechanism", "empirical limits")
TEXT = {"type": "string"}

def _object(properties):
    return {"type": "object", "properties": properties,
            "required": list(properties), "additionalProperties": False}
def _array(items): return {"type": "array", "items": items}
def _assignment():
    statuses = _object({name: {"type": "string", "enum": ["EXACT_QUOTE", "INTERPRETATION"]}
                        for name in SOURCE})
    evidence = _object({"locator": TEXT, "values": _object({name: TEXT for name in SOURCE}),
                        "statuses": statuses, "provenance": TEXT})
    return _object({"chapter": {"type": "string", "enum": ["C-01", "C-02", "C-03"]},
        "required": _object({name: TEXT for name in REQUIRED}),
        "resolved_ids": _array(_object({"id": TEXT, "value": TEXT})),
        "assigned_evidence": _array(evidence), "frozen_tokens": _array(TEXT),
        "forbidden": _array(TEXT)})
PLAN_SCHEMA = _object({"brief": TEXT, "framing": TEXT, "master_plan": TEXT,
                       "assignments": _array(_assignment())})
REVIEW_SCHEMA = _object({"framing_review": TEXT, "master_plan_review": TEXT})
COMMISSION_SCHEMA, AUDIT_SCHEMA = _object({"commission": TEXT}), _object({"verdict": TEXT})

def spec(index, route, command, book):
    actors = ("hf01-rf21-sol-planner", "hf01-rf21-luna-reviewer",
        "hf01-rf22-sol-commissioner-01", "hf01-rf22-sol-commissioner-02",
        "hf01-rf22-sol-commissioner-03", "hf01-rf22-sol-auditor")
    outputs = ((f"{book}/00-brief.md", f"{book}/framing.md", f"{book}/master-plan.md"),
        (f"{book}/framing-review.md", f"{book}/master-plan-review.md"),
        *((f"{book}/commissions/chapter-{number:02d}.md",) for number in (1, 2, 3)),
        ("commission-set-audit.json",))
    inputs = (("style-guide", "brief", "framing", "lived-synthesis", "scientific-synthesis"),
        ("rf21-plan-output", "brief", "framing", "lived-synthesis", "scientific-synthesis"),
        *(("accepted-plan", "chapter-card", "reader-state", "assigned-packets") for _ in range(3)),
        ("three-commissions", "three-cards", "three-assignments", "assigned-packet-union"))
    prefix = "developmental_reviewer" if index == 1 else "planner"
    model, reasoning = route[f"{prefix}_model"], route[f"{prefix}_reasoning"]
    return {"id": IDS[index], "actor": actors[index], "role": ROLES[index], "model": model,
        "route": route[f"{prefix}_route"], "reasoning": reasoning, "fresh_context": True,
        "reference_blind": True, "output_identities": list(outputs[index]),
        "input_contract": {"kind": "exact-authority-bound-inputs", "members": list(inputs[index])},
        "command": command(model, reasoning)}

def assignments(root, rows, arm_paths):
    chapters = {"C-01", "C-02", "C-03"}
    if not isinstance(rows, list) or {row.get("chapter") for row in rows if isinstance(row, dict)} != chapters:
        raise ValueError("assignments must name the exact three chapters")
    candidate, source_root = arm_paths(root)["control"]["candidate"], arm_paths(root)["control"]["book"] / "research/sources"
    index = {}
    for path in source_root.glob("*.md"):
        match = re.search(r"^- \*\*Source ID:\*\* (S-\d{3})$", path.read_text(encoding="utf-8"), re.M)
        if match: index[match.group(1)] = path.relative_to(candidate).as_posix()
    result = {}
    for row in rows:
        evidence = {item["locator"]: {key: item[key] for key in ("values", "statuses", "provenance")}
                    for item in row["assigned_evidence"]}
        sources = {locator.split("#", 1)[0] for locator in evidence}
        if not evidence or not sources <= index.keys() or len(evidence) != len(row["assigned_evidence"]):
            raise ValueError(f"{row['chapter']}: assigned source locator is missing or ambiguous")
        authority = {"target": row["chapter"], "required": row["required"],
            "resolved_ids": {item["id"]: item["value"] for item in row["resolved_ids"]},
            "assigned_evidence": evidence, "frozen_tokens": row["frozen_tokens"],
            "forbidden": row["forbidden"]}
        result[row["chapter"]] = {"packets": [index[source] for source in sorted(sources)],
                                  "authority": authority}
    return result
