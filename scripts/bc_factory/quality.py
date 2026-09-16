"""Whole-book edits and deterministic screening. Screens are review queues, not truth or efficacy proofs."""
from __future__ import annotations
import copy
import re
from .common import exact_keys, nonempty, require, version

FRONT_FIELDS = ("title", "reader_goal", "limits", "safety")
FRONT_LABELS = {"title": "title", "reader_goal": "Reader's chosen goal",
                "limits": "Scope and limits", "safety": "Important safety information"}


def base_front_matter(brief: dict, plan: dict) -> dict:
    """Brief/plan-derived generated prose, keyed by repairable field."""
    return {"title": plan["title"],
            "reader_goal": brief["reader_goal"],
            "limits": plan["limits"],
            "safety": brief.get("safety_advisory") or ""}


def apply_front_repairs(base: dict, operations: list, round_no: int) -> tuple[dict, list]:
    """Validate and apply exact-anchored front-matter repairs. Required safety
    text can be narrowed but never deleted or emptied."""
    front = dict(base)
    repairs = []
    for op in operations:
        if not isinstance(op, dict) or op.get("op") != "front":
            continue
        exact_keys(op, {"op", "field", "old", "new", "reason"}, label="front-matter repair")
        require(op["field"] in FRONT_FIELDS, f"Front-matter field not repairable: {op.get('field')}")
        require(op["field"] in front, "Front-matter base missing field")
        require(op["old"] == front[op["field"]], "Front-matter anchor does not match current text")
        require(isinstance(op["new"], str) and bool(op["new"].strip()), "Front-matter replacement must be nonempty; required safety text cannot be deleted")
        require(op["new"] != op["old"], "Front-matter repair must change the text")
        nonempty(op.get("reason"), "Front-matter repair reason")
        front[op["field"]] = op["new"]
        repairs.append({"field": op["field"], "old": op["old"], "new": op["new"],
                        "reason": op["reason"], "round": round_no})
    return front, repairs


def split_operations(operations: list) -> tuple[list, list]:
    """Separate chapter operations from front-matter repairs."""
    require(isinstance(operations, list), "Editor operations must be a list")
    return ([o for o in operations if isinstance(o, dict) and o.get("op") != "front"],
            [o for o in operations if isinstance(o, dict) and o.get("op") == "front"])


def edit_book(chapters: list[dict], response: dict) -> list[dict]:
    exact_keys(response, {"schema_version", "operations", "explanation"}, label="book editor")
    version(response)
    nonempty(response["explanation"], "Editorial explanation")
    require(isinstance(response["operations"], list), "Editor operations must be a list")
    result = copy.deepcopy(chapters)
    def get(cid: str) -> dict:
        hits = [c for c in result if c["id"] == cid]
        require(len(hits) == 1, f"Editor refers to missing/nonunique chapter {cid}")
        return hits[0]
    for op in response["operations"]:
        require(isinstance(op, dict) and "op" in op, "Invalid editorial operation")
        nonempty(op.get("reason"), "Editorial operation reason")
        if op["op"] == "replace":
            exact_keys(op, {"op", "chapter", "old", "new", "reason"})
            c = get(op["chapter"])
            nonempty(op["old"], "Replacement anchor")
            require(isinstance(op["new"], str), "Replacement must be text")
            require(c["text"].count(op["old"]) == 1, "Editorial anchor must occur exactly once")
            c["text"] = c["text"].replace(op["old"], op["new"], 1)
            nonempty(c["text"], "Edited chapter")
        elif op["op"] == "remove":
            exact_keys(op, {"op", "chapter", "reason"})
            result.remove(get(op["chapter"]))
        elif op["op"] == "move":
            exact_keys(op, {"op", "chapter", "before", "reason"})
            c, target = get(op["chapter"]), get(op["before"])
            require(c is not target, "Cannot move chapter before itself")
            result.remove(c)
            result.insert(result.index(target), c)
        elif op["op"] == "merge":
            exact_keys(op, {"op", "first", "second", "title", "reason"})
            first, second = get(op["first"]), get(op["second"])
            require(first is not second, "Cannot merge a chapter with itself")
            first["title"] = nonempty(op["title"], "Merged title")
            first["text"] += "\n\n" + second["text"]
            first["source_chapters"] += second["source_chapters"]
            first["claim_map"] += second["claim_map"]
            result.remove(second)
        else:
            require(False, f"Unknown editorial operation: {op['op']}")
    require(bool(result), "An editor cannot remove the entire book")
    return result


KIND_LABELS = {"research": "Research synthesis", "lived_experience": "First-person report",
               "authority": "Official or organizational guidance", "illustration": "Illustration"}


def reader_locator(locator: str) -> str:
    """Reader-facing retrieval note: keep method/provenance, drop internal envelope/ledger filenames."""
    text = re.sub(r"\s*[;,]?\s*(?:retrieval\s+)?envelope\s+\S+?\.json", "", locator)
    text = re.sub(r"\s*[;,]?\s*ledger\s+\S+?\.json", "", text)
    text = re.sub(r"\(\s*[;,]", "(", text)
    text = re.sub(r"[;,]\s*\)", ")", text)
    text = re.sub(r"\(\s*\)", "", text)
    return re.sub(r"\s+", " ", text).strip()


def assemble_book(brief: dict, research: dict, plan: dict, chapters: list[dict],
                  front_matter: dict | None = None) -> str:
    n = brief["narrator"]
    if n["mode"] == "informed_author":
        author_note = "This book is an evidence-informed explanation, not the personal recovery story or clinical practice of its narrator. Illustrative scenes are not testimonials."
    else:
        author_note = f"Author: {n['name']}. Verified author-specific claims: " + "; ".join(c["claim"] for c in n["allowed_claims"])
    fm = dict(base_front_matter(brief, plan))
    if front_matter is not None:
        for key, value in front_matter.items():
            require(key in FRONT_FIELDS, f"Front-matter field not repairable: {key}")
            fm[key] = value
    sections = [f"# {fm['title']}", "## About this book", author_note,
                f"Reader's chosen goal: {fm['reader_goal']}",
                "This book does not guarantee a particular outcome. Its arguments remain open to evidence and to the reader's considered judgment.",
                f"Scope and limits: {fm['limits']}"]
    if brief["scope_exclusions"]:
        sections.append("Outside scope: " + "; ".join(brief["scope_exclusions"]))
    if fm["safety"]:
        sections += ["## Important safety information", fm["safety"]]
    for i, c in enumerate(chapters, 1):
        sections += [f"## {i}. {c['title']}", c["text"].strip()]
    sections += ["## Source notes", "Source notes distinguish reports, research, and illustrations. Inclusion is not a claim that a source proves every inference in this book."]
    for num, e in enumerate(research["sources"], 1):
        sections.append(f"{num}. {KIND_LABELS.get(e['kind'], e['kind'])} — {e['source']}\nRetrieval: {reader_locator(e['locator'])}\nScope: {e['population']}\nSupported use: {e['permitted_inference']}")
    return "\n\n".join(sections).rstrip() + "\n"


def screen(text: str) -> list[dict]:
    # Deliberately conservative. Negations and quoted objections need semantic triage.
    findings: list[dict] = []
    def add(kind: str, quote: str, explanation: str) -> None:
        findings.append({"id": f"screen-{len(findings)+1:03d}", "kind": kind, "quote": quote, "explanation": explanation})
    tests = [
        ("authority", r"\bI (?:have (?:sat with|helped|treated|cured)|cured|treated)\b[^.!?\n]{0,150}", "Check narrator-specific evidence; invented practice/experience is not permitted."),
        ("outcome_guarantee", r"\b(?:easily,? immediately,? and permanently|will (?:never|permanently)|guarantee(?:d|s)? (?:success|freedom|recovery))\b[^.!?\n]{0,120}", "Check universal outcome claim, including promises exempted by older prompts."),
        ("inventory_leak", r"\b(?:ADV-\d+|CA-SAFE|P-\d{2}|EV-\d{2}|IN THIS CHAPTER:)\b", "Check for planning identifiers/template residue in reader prose."),
    ]
    for kind, pattern, explanation in tests:
        for match in re.finditer(pattern, text, flags=re.I):
            add(kind, match.group(0), explanation)
    tokens = re.findall(r"\b[A-Z][A-Z]+(?: [A-Z][A-Z]+){0,2}\b", text)
    words = len(text.split())
    if words and len(tokens) / words > 0.025:
        add("capital_density", tokens[0] if tokens else "", "Capitalized term density is high; inspect mechanical repetition, not just acronym legitimacy.")
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    freq: dict[str, int] = {}
    for s in sentences:
        if len(s.split()) >= 7:
            freq[s] = freq.get(s, 0) + 1
    for s, n in freq.items():
        if n >= 4:
            add("repetition", s, f"Exact sentence occurs {n} times. Determine whether each return advances an objection.")
    return findings


def overlap_screen(text: str, references: dict[str, str], n: int = 12) -> list[dict]:
    """Optional mechanical overlap detector. Not a plagiarism/legal clearance judgment."""
    require(n >= 8, "Overlap window too short")
    words = re.findall(r"\w+", text.lower())
    index = {tuple(words[i:i+n]) for i in range(max(0, len(words)-n+1))}
    found = []
    for name, ref in references.items():
        rw = re.findall(r"\w+", ref.lower())
        hits = {tuple(rw[i:i+n]) for i in range(max(0, len(rw)-n+1))} & index
        if hits:
            found.append({"reference": name, "matched_windows": len(hits), "requires_review": True})
    return found
