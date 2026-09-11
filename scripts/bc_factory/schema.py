"""One authoritative contract shared by role prompts, parsers and gates."""
from __future__ import annotations
import re
from urllib.parse import urlparse
from .common import exact_keys, identifier, nonempty, require, version

DIMENSIONS = ("argument", "recognition", "progression", "voice", "emotional_movement", "economy")
CHECKS = ("truth", "attribution", "safety", "originality", "scope", "argument", "continuity", "completeness")
FINDINGS = frozenset({
    "JOB", "EVIDENCE", "OVERCLAIM", "AUTHORITY", "SAFETY", "ORIGINALITY", "SCOPE",
    "CONTINUITY", "REPETITION", "FRAGMENT", "HEADER", "INSTRUCTION", "ID", "MANTRA",
    "STOPPED-SHORT", "UNASSIGNED-REFRAIN", "RESERVED-REACH", "RE-ARGUMENT", "LENGTHEN", "SHORTEN",
})
ROLES = ("evidence-reviewer", "planner", "plan-reviewer", "writer", "chapter-reviewer",
         "state-editor", "book-editor", "final-auditor")
REVIEW_ROLES = {"evidence-reviewer", "plan-reviewer", "chapter-reviewer", "final-auditor"}
EXTERNAL_ROLES = {"evidence-reviewer", "final-auditor", "pair-judge"}


def finding_types(text: str) -> list[str]:
    """Strict legacy diagnostic helper. New production roles use JSON reviews."""
    found = []
    for line in text.splitlines():
        token = line.strip().split(maxsplit=1)[0].rstrip(":") if line.strip() else ""
        if token in ("ACCEPT", "REVISE", "BLOCKED") or not token:
            continue
        if re.fullmatch(r"[A-Z][A-Z-]+", token):
            require(token in FINDINGS, f"Unknown review finding: {token}")
            found.append(token)
    return found


def validate_brief(b: dict) -> None:
    exact_keys(b, {"schema_version", "subject", "title", "audience", "reader_goal", "target_belief",
                   "target_kind", "outcome_mode", "risk_level", "safety_advisory", "narrator", "scope_exclusions"}, label="brief")
    version(b)
    identifier(b["subject"])
    for key in ("title", "audience", "reader_goal", "target_belief"):
        nonempty(b[key], key)
    require(b["target_kind"] in ("habit", "consumption", "belief", "skill", "other"), "Unknown target kind")
    require(b["outcome_mode"] in ("abstain", "reduce", "reframe", "learn", "decide"), "Unknown outcome mode")
    require(b["risk_level"] in ("low", "health", "high"), "Unknown risk level")
    require(isinstance(b["safety_advisory"], str), "safety_advisory must be text")
    if b["risk_level"] != "low":
        nonempty(b["safety_advisory"], "Health/high-risk safety advisory")
    require(isinstance(b["scope_exclusions"], list) and all(isinstance(x, str) and x for x in b["scope_exclusions"]), "scope_exclusions must be a text list")
    n = b["narrator"]
    exact_keys(n, {"mode", "name", "allowed_claims"}, label="narrator")
    require(n["mode"] in ("informed_author", "verified_person"), "Untruthful narrator mode")
    require(isinstance(n["name"], str) and isinstance(n["allowed_claims"], list), "Invalid narrator")
    if n["mode"] == "informed_author":
        require(not n["allowed_claims"], "An informed-author narrator cannot claim personal credentials/history")
    else:
        nonempty(n["name"], "Verified person's name")
        for claim in n["allowed_claims"]:
            exact_keys(claim, {"claim", "evidence_ids"}, label="narrator claim")
            nonempty(claim["claim"], "narrator claim")
            require(isinstance(claim["evidence_ids"], list) and bool(claim["evidence_ids"]), "Narrator claim needs verified evidence IDs")


def validate_research(r: dict, brief: dict) -> None:
    exact_keys(r, {"schema_version", "subject", "sources", "open_questions", "strongest_countercase", "coverage"}, label="research")
    version(r)
    require(r["subject"] == brief["subject"], "Research/brief subject mismatch")
    require(isinstance(r["sources"], list) and bool(r["sources"]), "Research needs sources; do not manufacture them")
    ids: set[str] = set()
    for e in r["sources"]:
        exact_keys(e, {"id", "kind", "source", "locator", "retrieved_at", "excerpt", "claim", "population",
                       "permitted_inference", "prohibited_inferences", "counterevidence", "rights_basis", "verification"}, label="source")
        identifier(e["id"])
        require(e["id"] not in ids, "Duplicate evidence ID")
        ids.add(e["id"])
        require(e["kind"] in ("research", "lived_experience", "authority", "illustration"), "Unknown evidence kind")
        for k in ("source", "locator", "retrieved_at", "excerpt", "claim", "population", "permitted_inference", "rights_basis"):
            nonempty(e[k], k)
        if "://" in e["source"]:
            url = urlparse(e["source"])
            require(url.scheme in ("https", "http") and bool(url.netloc) and not url.username and not url.password, "Unsafe source URL")
        for k in ("prohibited_inferences", "counterevidence"):
            require(isinstance(e[k], list) and all(isinstance(x, str) for x in e[k]), f"{k} must be a text list")
        require(e["verification"] in ("retrieved", "verified", "unverified"), "Unknown source verification state")
    nonempty(r["strongest_countercase"], "strongest_countercase (can alter the thesis)")
    require(isinstance(r["open_questions"], list) and all(isinstance(q, str) for q in r["open_questions"]), "Invalid research questions")
    require(isinstance(r["coverage"], dict) and bool(r["coverage"]), "Coverage must document audience situations, gaps and diversity")
    for c in brief["narrator"]["allowed_claims"]:
        require(set(c["evidence_ids"]) <= ids, "Narrator evidence missing")
        for eid in c["evidence_ids"]:
            e = next(e for e in r["sources"] if e["id"] == eid)
            require(e["kind"] == "authority" and e["verification"] == "verified", "Narrator authority needs verified author-specific evidence")


def validate_plan(p: dict, brief: dict, research: dict) -> None:
    exact_keys(p, {"schema_version", "subject", "title", "thesis", "limits", "chapters"}, label="plan")
    version(p)
    require(p["subject"] == brief["subject"], "Plan subject mismatch")
    for key in ("title", "thesis", "limits"):
        nonempty(p[key], key)
    require(isinstance(p["chapters"], list) and bool(p["chapters"]), "Plan must have chapters")
    ids = {e["id"] for e in research["sources"]}
    previous: set[str] = set()
    for i, c in enumerate(p["chapters"], 1):
        exact_keys(c, {"id", "title", "objective", "entering_belief", "strongest_objection", "evidence_ids",
                       "supported_conclusion", "remaining_objection", "dependencies", "scenes", "word_budget"}, label="chapter card")
        require(c["id"] == f"chapter-{i:02d}", "Chapter IDs must be unique, ordered and contiguous")
        for k in ("title", "objective", "entering_belief", "strongest_objection", "supported_conclusion", "remaining_objection"):
            nonempty(c[k], k)
        require(isinstance(c["evidence_ids"], list) and set(c["evidence_ids"]) <= ids, "Unresolved chapter evidence")
        require(isinstance(c["dependencies"], list) and set(c["dependencies"]) <= previous, "Forward/cyclic/missing dependency")
        previous.add(c["id"])
        require(c["word_budget"] is None or (type(c["word_budget"]) is int and c["word_budget"] > 0), "Budget is null or positive integer; it is not a padding quota")
        require(isinstance(c["scenes"], list), "Invalid scenes")
        for s in c["scenes"]:
            exact_keys(s, {"description", "type", "evidence_ids"}, label="scene")
            nonempty(s["description"], "scene description")
            require(s["type"] in ("sourced", "illustration"), "Scenes cannot pose invented experience as a testimonial")
            require(isinstance(s["evidence_ids"], list) and set(s["evidence_ids"]) <= ids, "Scene evidence missing")
            if s["type"] == "sourced":
                require(bool(s["evidence_ids"]), "Sourced scene needs evidence")


def validate_review(r: dict, source_text: str, final: bool = False) -> None:
    required = {"schema_version", "verdict", "checks", "findings"}
    if final:
        required |= {"claim_checks", "screening_resolutions"}
    exact_keys(r, required, label="review")
    version(r)
    require(r["verdict"] in ("ACCEPT", "REVISE", "BLOCKED"), "Unknown review verdict")
    exact_keys(r["checks"], set(CHECKS), label="review checks")
    require(all(type(v) is bool for v in r["checks"].values()), "Every check must be an explicit boolean")
    require(isinstance(r["findings"], list), "Findings must be a list")
    for f in r["findings"]:
        exact_keys(f, {"kind", "severity", "quote", "explanation", "repair"}, label="finding")
        require(f["kind"] in FINDINGS, f"Unknown finding: {f['kind']}")
        require(f["severity"] in ("critical", "material", "minor"), "Invalid severity")
        nonempty(f["explanation"], "Finding explanation")
        nonempty(f["repair"], "Repair")
        require(isinstance(f["quote"], str) and (not f["quote"] or f["quote"] in source_text), "Finding quote not found in the reviewed input")
    if r["verdict"] == "ACCEPT":
        require(all(r["checks"].values()) and not r["findings"], "ACCEPT cannot hide failed checks or findings")
    else:
        require(bool(r["findings"]) or not all(r["checks"].values()), "Non-ACCEPT needs a finding or a failed check")
    if final:
        require(isinstance(r["claim_checks"], list) and bool(r["claim_checks"]), "Final audit must inspect final claims, not just evidence IDs")
        for c in r["claim_checks"]:
            exact_keys(c, {"quote", "evidence_ids", "support", "explanation"}, label="claim check")
            nonempty(c["quote"], "Checked claim")
            require(c["quote"] in source_text, "Audited claim not present in final book")
            require(c["support"] in ("supported", "bounded", "nonempirical", "unsupported"), "Invalid support status")
            nonempty(c["explanation"], "Support explanation")
            require(isinstance(c["evidence_ids"], list), "Claim IDs must be a list")
            if r["verdict"] == "ACCEPT":
                require(c["support"] != "unsupported", "Unsupported final claim blocks acceptance")
                if c["support"] in ("supported", "bounded"):
                    require(bool(c["evidence_ids"]), "Empirical claim needs evidence")
        require(isinstance(r["screening_resolutions"], dict), "Invalid screening resolutions")
        for reason in r["screening_resolutions"].values():
            nonempty(reason, "Screening resolution")


def validate_writer(w: dict, chapter_id: str, research: dict) -> None:
    exact_keys(w, {"schema_version", "chapter_id", "text", "claim_map"}, label="writer")
    version(w)
    require(w["chapter_id"] == chapter_id, "Wrong chapter output")
    nonempty(w["text"], "Chapter text")
    require(isinstance(w["claim_map"], list), "Writer must provide an explicit claim map, empty only for no empirical claims")
    ids = {e["id"] for e in research["sources"]}
    for c in w["claim_map"]:
        exact_keys(c, {"quote", "evidence_ids"}, label="writer claim")
        nonempty(c["quote"], "Claim quote")
        require(c["quote"] in w["text"], "Claim map quote absent from chapter")
        require(isinstance(c["evidence_ids"], list) and bool(c["evidence_ids"]) and set(c["evidence_ids"]) <= ids, "Claim map has missing/unresolved evidence")
        source_map = {e["id"]: e for e in research["sources"]}
        require(all(source_map[e]["kind"] != "illustration" and source_map[e]["verification"] != "unverified" for e in c["evidence_ids"]), "An illustration or unverified source cannot establish an empirical claim")


def validate_state(s: dict, chapter_id: str, text: str) -> None:
    exact_keys(s, {"schema_version", "chapter_id", "established", "unresolved", "used_examples"}, label="reader state")
    version(s)
    require(s["chapter_id"] == chapter_id, "State belongs to another chapter")
    require(isinstance(s["established"], list) and bool(s["established"]), "Reader state needs text-supported conclusions")
    for e in s["established"]:
        exact_keys(e, {"belief", "quote"}, label="established belief")
        nonempty(e["belief"], "Belief")
        require(bool(e["quote"]) and e["quote"] in text, "Reader-state quote absent from delivered text")
    for k in ("unresolved", "used_examples"):
        require(isinstance(s[k], list) and all(isinstance(x, str) for x in s[k]), f"{k} must be a text list")


def validate_metadata(m: dict) -> None:
    import math
    exact_keys(m, {"model", "family", "route", "harness", "usage", "latency_s"}, label="execution metadata")
    for k in ("model", "family", "route", "harness"):
        nonempty(m[k], k)
    require(m["usage"] is None or isinstance(m["usage"], dict), "Usage is a reported object or null")
    t = m["latency_s"]
    require(t is None or type(t) in (int, float) and math.isfinite(t) and t >= 0, "Latency must be nonnegative, finite, or unknown/null")


def validate_config(config: dict) -> None:
    exact_keys(config, {"schema_version", "max_rounds", "profiles"}, label="config")
    version(config)
    require(type(config["max_rounds"]) is int and 1 <= config["max_rounds"] <= 10, "Invalid explicit revision bound")
    exact_keys(config["profiles"], {"factory", "external"}, label="profiles")
    for name, p in config["profiles"].items():
        if p is None:
            require(name == "external", "Factory profile cannot be absent")
            continue
        require(isinstance(p, dict), "Invalid profile")
        adapter = p.get("adapter")
        if adapter == "http":
            exact_keys(p, {"adapter", "family", "routes"}, {"reasoning", "timeout_s"}, label="HTTP profile")
            require(isinstance(p["routes"], list) and bool(p["routes"]), "HTTP routes missing")
            for r in p["routes"]:
                exact_keys(r, {"name", "endpoint", "model", "auth_env", "api"}, label="route (credential values are forbidden)")
                for k in ("name", "model", "auth_env"):
                    nonempty(r[k], k)
                require(re.fullmatch(r"[A-Z][A-Z0-9_]*", r["auth_env"]) is not None, "auth_env must name an environment variable, never contain a credential")
                u = urlparse(r["endpoint"])
                require(u.scheme == "https" and u.netloc and not u.username and not u.password and not u.query and not u.fragment, "Endpoint must be HTTPS without embedded credentials/query")
                require(r["api"] in ("chat", "responses"), "Unknown API shape")
        elif adapter == "command":
            exact_keys(p, {"adapter", "family", "argv"}, {"pass_env", "timeout_s"}, label="command profile")
            require(isinstance(p["argv"], list) and bool(p["argv"]) and all(isinstance(x, str) and x for x in p["argv"]), "Command requires argv strings")
            require(isinstance(p.get("pass_env", []), list) and all(isinstance(x, str) and re.fullmatch(r"[A-Z][A-Z0-9_]*", x) for x in p.get("pass_env", [])), "Invalid environment allowlist")
        else:
            require(False, "Unknown adapter")
        nonempty(p["family"], "Model family")
        require(type(p.get("timeout_s", 600)) in (int, float) and 0 < p.get("timeout_s", 600) <= 7200, "Invalid provider timeout")
    ext = config["profiles"]["external"]
    if ext is not None:
        require(ext["family"] != config["profiles"]["factory"]["family"], "External profile must use an independent family")
