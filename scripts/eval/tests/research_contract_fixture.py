"""Small rights-clean corpus sealed only through production validator builders."""
import hashlib
import json
from pathlib import Path

import validate_research_contract as RC


BELIEFS = (
    "Checking now keeps me safe.",
    "A quick look only takes a moment.",
    "Checking settles my unease.",
    "I might miss something important.",
)
SAFETY = "Acute distress and medical concerns go to a qualified professional."
PERSONAS = ("P-01", "P-02", "P-03")
LANE_BANKS = (
    ("COUNTER_CORPUS", 1), ("COUNTER_CORPUS", 2),
    ("LIVED_EXPERIENCE", 3), ("LIVED_EXPERIENCE", 4),
    ("SCIENCE_MECHANISM", 7), ("SCIENCE_MECHANISM", 8),
    ("INDUSTRY_CULTURE", 5), ("INDUSTRY_CULTURE", 6),
    ("DIALECT_SENSORY", 9), ("DIALECT_SENSORY", 10),
)


def _sha(value):
    return hashlib.sha256(value).hexdigest()


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _brief(beliefs=BELIEFS, target_behavior="Compulsive checking"):
    subordinate = "\n".join(f'- "{belief}"' for belief in beliefs[1:])
    return f"""# Brief â€” Checking

## Target behavior
{target_behavior}

## Intended reader
An adult who wants freedom from {target_behavior.casefold()}.

## Fork decisions
- **Outcome (Fork 2):** freedom from {target_behavior.casefold()}
- **Void (Fork 5):** ordinary life is the clean baseline
- **Science weight (Fork 3):** bounded evidence only
- **Villain (Fork 4):** name the behavior-specific trap honestly
- **Inner state (Fork 1):** discomfort without shame

## Destination
Calm freedom from {target_behavior.casefold()}.

## Exclusions
Diagnosis, treatment, and unrelated behavior.

## Safety perimeter
{SAFETY}

## Primary false belief
- "{beliefs[0]}"

## Subordinate beliefs
{subordinate}
"""


def _packet(number, lane, bank, beliefs=BELIEFS,
            target_behavior="Compulsive checking"):
    source = f"S-{number:03d}"
    evidence = "E-001"
    quote = (f"I need to check this now, example {number}."
             if target_behavior == "Compulsive checking" else
             f"I notice the {target_behavior.casefold()} cue now, example {number}.")
    excerpt = f"Distinct cue {number}. {quote} Unease {number} follows."
    content_hash = _sha(excerpt.encode("utf-8"))
    url = f"https://source-{number}.example.test/report"
    permitted = f"Distinct cue {number} and unease {number} support only this reported expectation."
    prohibited = f"Example {number} does not establish prevalence, diagnosis, or treatment effect."
    grade = "CONTESTED" if bank in (7, 8) else "n/a"
    testimonial = ("QUALIFIED; numbers=one account; sensory=unease; authority_conflict=none"
                   if bank == 10 else "NOT_CANDIDATE")
    return f"""# {source} â€” Sealed fixture source {number}

- **Source ID:** {source}
- **URL:** {url}
- **Title:** Sealed fixture source {number}
- **Source type:** {'study' if bank in (7, 8) else 'report'}
- **Retrieved (UTC):** 2026-07-23T00:00:00Z
- **Access / license basis:** fixture-owned public verification text
- **Excerpt / redistribution basis:** fixture text may be retained and redistributed
- **Required attribution:** Fixture author {number}
- **Retention / deletion sensitivity:** durable fixture; not deletion-sensitive
- **Privacy / personal-data basis:** synthetic fixture; no personal data retained
- **Discovery lane:** {lane}
- **Source family:** fixture-family-{number}
- **Author / organization:** Fixture author {number}
- **Fetched URL:** {url}
- **Fetched content SHA-256:** {content_hash}
- **Corroboration count:** 1
- **Story identity:** fixture-story-{number}
- **Study lineage:** fixture-lineage-{number}
- **Study design / class:** bounded fixture {'mechanism' if bank in (7, 8) else 'report'}
- **Deletion sensitivity:** NOT_DELETION_SENSITIVE
- **Personal-data retention:** NONE
- **Disposition:** ACCEPTED

## Minimum retained excerpt

### C-001

- **Locator:** fixture paragraph {number}
- **Capture method:** fixture-owned text
- **Content SHA-256:** {content_hash}

```text
{excerpt}
```

## Evidence items

### {evidence}

- **Kind:** EXACT_QUOTE
- **Text:** {quote}
- **Excerpt ID:** C-001
- **Locator:** fixture paragraph {number}
- **Persona tags:** {'; '.join(PERSONAS)}
- **Bank slots:** Bank {bank}
- **Evidence grade:** {grade}
- **Use / limits:** {permitted} {prohibited}
- **Brief beliefs:** {'; '.join(beliefs)}
- **Style slots:** {'; '.join(sorted(RC.SLOTS))}
- **Safety relevance:** {SAFETY}
- **Situation:** Distinct cue {number}
- **Emotion:** unease {number}
- **Grade rationale:** fixture-bounded observation
- **Scope:** this retained fixture only
- **Counterevidence:** no broad claim is made
- **Permitted inference:** {permitted}
- **Prohibited inference:** {prohibited}
- **Testimonial qualification:** {testimonial}
""", {"number": number, "source": source, "locator": f"{source}#{evidence}", "quote": quote,
          "permitted": permitted, "prohibited": prohibited, "grade": grade,
          "bank": bank}


def _unit(unit_id, belief, record):
    number = record["number"]
    return f"""### {unit_id}

- **Situation:** Distinct cue {number}
- **Reader wording:** "{record['quote']}"
- **Implicated belief:** "{belief}"
- **Persona IDs:** {'; '.join(PERSONAS)}
- **Emotion:** unease {number}
- **Permitted inference:** {record['permitted']}
- **Prohibited inference:** {record['prohibited']}
- **Style slots:** {'; '.join(sorted(RC.SLOTS))}
- **Safety boundary:** {SAFETY}
- **Source locator:** {record['locator']}
- **Evidence grade:** {record['grade']}
"""


def _persona_map(sources):
    rows = ["## Persona map", "",
            "| Persona ID | Function served / defining context | Applicable beliefs | Applicable banks | Source IDs |",
            "|---|---|---|---|---|"]
    contexts = ("urgent work interruption", "quiet evening habit", "family availability worry")
    for persona, context in zip(PERSONAS, contexts):
        rows.append(f"| {persona} | {context} | ALL | 1,2,3,4,5,6,7,8,9,10 | {', '.join(sources)} |")
    return "\n".join(rows)


def _authority(book):
    root = Path(book).resolve().parents[1]
    return {
        "prompt": {"path": "prompts/research-agent.md",
                   "sha256": _sha((root / "prompts/research-agent.md").read_bytes())},
        "evidence_editor": {"path": "prompts/research-evidence-editor.md",
                            "sha256": _sha((root / "prompts/research-evidence-editor.md").read_bytes())},
        "configuration": {"path": "loop/config.yaml",
                          "sha256": _sha((root / "loop/config.yaml").read_bytes())},
        "sanitized_receipt_hashes": [_sha(b"sealed-fixture-receipt")],
    }


def write_sealed_research(book, *, preset="POCKET", beliefs=BELIEFS,
                          target_behavior="Compulsive checking"):
    """Write and return one fully production-validated seal in ``book``."""
    if preset not in RC.FLOORS:
        raise ValueError("preset must be POCKET or FULL-LENGTH")
    if not isinstance(beliefs, (tuple, list)) or len(beliefs) != 4 \
            or any(not isinstance(belief, str) or not belief.strip()
                   for belief in beliefs):
        raise ValueError("fixture beliefs must contain exactly four nonempty strings")
    beliefs = tuple(beliefs)
    book = Path(book).resolve()
    if book.parent.name != "production-books":
        raise ValueError("fixture book must use <operation>/production-books/<slug>")
    operation = book.parents[1]
    repository = Path(RC.__file__).resolve().parents[1]
    for relative in ("prompts/research-agent.md", "prompts/research-evidence-editor.md",
                     "loop/config.yaml"):
        target = operation / relative
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((repository / relative).read_bytes())
    sources = book / "research/sources"
    sources.mkdir(parents=True, exist_ok=True)
    for path in sources.glob("*.md"):
        path.unlink()
    for name in ("research-coverage.json", "research-review.json",
                 "research-seal.json", "research-log.md",
                 "lived-experience.md", "scientific-evidence.md"):
        path = book / "research" / name
        if path.exists():
            path.unlink()
    _write(book / "00-brief.md", _brief(beliefs, target_behavior))
    records = []
    for number, (lane, bank) in enumerate(LANE_BANKS, 1):
        text, record = _packet(number, lane, bank, beliefs, target_behavior)
        _write(sources / f"S-{number:03d}-sealed-fixture.md", text)
        records.append(record)
    persona = _persona_map([record["source"] for record in records])
    units = "\n".join(_unit(f"LEU-{number:03d}", belief, records[number - 1])
                       for number, belief in enumerate(beliefs, 1))
    science_unit = _unit("SEU-001", beliefs[0], records[4])
    lived_lines = []
    science_lines = []
    for record in records:
        line = (f"- [Bank {record['bank']}] "
                f"{'[' + record['grade'] + '] ' if record['bank'] in (7, 8) else ''}"
                f"{record['quote']} â€” Persona IDs: {'; '.join(PERSONAS)} â€” "
                f"Source IDs: {record['locator']}")
        (science_lines if record["bank"] in (7, 8) else lived_lines).append(line)
    _write(book / "research/lived-experience.md",
           "# Lived Experience\n\n" + persona +
           "\n\n## Intervention-ready evidence units\n\n" + units +
           "\n## Evidence banks\n\n" + "\n".join(lived_lines) + "\n")
    _write(book / "research/scientific-evidence.md",
           "# Scientific Evidence\n\n## Intervention-ready evidence units\n\n" + science_unit +
           "## Evidence banks\n\n" + "\n".join(science_lines) + "\n")
    _write(book / "research/research-log.md",
           f"# Research log\n\nFORMAT PRESET: {preset}\n\nAll fixture calls are captured and no-network.\n")
    attempts = _sha(b"bounded-fixture-attempts")
    initial = RC.build_coverage(book, preset)
    requests = [{"floor": gap["target"], "attempts_sha256": attempts,
                 "demonstrated_ceiling": initial["floors"][gap["target"]]["actual"]}
                for gap in initial["gaps"] if gap["kind"] == "floor"]
    coverage = RC.build_coverage(book, preset, requests)
    _write(book / "research/research-coverage.json",
           json.dumps(coverage, sort_keys=True, separators=(",", ":")) + "\n")
    authority = _authority(book)
    candidate = RC.candidate_identity(book, authority)
    waivers = []
    for request in requests:
        waiver = {**request, "finding": "bounded fixture ceiling accepted for deterministic testing"}
        waiver["finding_sha256"] = RC._finding_hash(waiver)
        waivers.append(waiver)
    verdict = {"status": "PASS", "checks": {name: "PASS" for name in RC.REVIEW_CHECKS},
               "gaps": [], "scarcity_waivers": waivers}
    provenance = {"kind": "captured-native-test-double",
                  "judge_identity": "research-evidence-editor", "model": "captured-test",
                  "reasoning_effort": "bounded", "fresh_ephemeral_context": True,
                  "thread_id": "sealed-fixture-thread", "input_sha256": _sha(b"fixture-input"),
                  "output_schema_sha256": _sha(b"fixture-schema"),
                  "usage": {"input_tokens": 1, "output_tokens": 1}}
    task_sha = _sha(b"fixture-task")
    verdict_sha = RC._sha_json(verdict)
    review = {"schema": RC.SCHEMA, "status": "PASS", "task_sha256": _sha(b"fixture-task"),
              "candidate_sha256": candidate, "verdict_sha256": verdict_sha,
              "editor_provenance": provenance,
              "editor_receipt_sha256": RC._sha_json({
                  "task_sha256": task_sha, "verdict_sha256": verdict_sha,
                  "provenance": provenance}),
              "gaps": [], "checks": verdict["checks"], "scarcity_waivers": waivers}
    _write(book / "research/research-review.json",
           json.dumps(review, sort_keys=True, separators=(",", ":")) + "\n")
    seal = RC.build_seal(book, authority)
    _write(book / "research/research-seal.json",
           json.dumps(seal, sort_keys=True, separators=(",", ":")) + "\n")
    report = RC.inspect_research(book, require_seal=True)
    if not report["ok"]:
        raise AssertionError("sealed research fixture failed production validation: " +
                             "; ".join(report["blockers"]))
    return report


def chapter_binding(report, evidence_id, unit_id):
    """Return the exact assignment value derived from a sealed fixture report."""
    unit = report["inventory"]["units"][unit_id]
    return {"seal_sha256": report["seal_identity"], "needs": {evidence_id: {
        "unit_ids": [unit_id], "locators": list(unit["locators"]),
        "required_limits": sorted((
            f"Permitted inference: {unit['permitted_inference']}",
            f"Prohibited inference: {unit['prohibited_inference']}",
        )), "safety": [unit["safety"]],
    }}}


def evidence_row(report, evidence_id, unit_id):
    """Render the exact canonical plan row for one fixture unit."""
    unit = report["inventory"]["units"][unit_id]
    return (f"| {evidence_id} | sealed fixture finding | {unit_id} | "
            f"{', '.join(unit['locators'])} | {unit['evidence_grade']} | fixture scope | "
            f"{unit['permitted_inference']} | {unit['prohibited_inference']} |")
