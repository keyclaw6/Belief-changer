#!/usr/bin/env python3
"""RF-32 fail-closed, resumable research coordinator inside one RF-02 candidate."""
import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve()
SCRIPTS = HERE.parents[1]
EVAL = SCRIPTS / "eval"
for directory in (SCRIPTS, EVAL):
    sys.path.insert(0, str(directory))

import candidate_pair as CP  # noqa: E402
import commission_set as CS  # noqa: E402
import legacy_guard as LG  # noqa: E402
import loopcfg  # noqa: E402
import pair_store as PS  # noqa: E402
import validate_research_contract as RC  # noqa: E402
import validate_subject_contract as SC  # noqa: E402

SCHEMA = 1
MODEL = "deepseek/deepseek-v4-pro"
ENDPOINT = "https://openrouter.ai/api/v1/responses"
PRICING_ENDPOINT = "https://openrouter.ai/api/v1/models/deepseek/deepseek-v4-pro/endpoints"
LANES = (
    "lived-experience",
    "scientific-mechanistic",
    "industry-cultural",
    "pro-behavior-counter-corpus",
    "dialect-sensory",
)
LANE_IDS = {
    "lived-experience": "LIVED_EXPERIENCE",
    "scientific-mechanistic": "SCIENCE_MECHANISM",
    "industry-cultural": "INDUSTRY_CULTURE",
    "pro-behavior-counter-corpus": "COUNTER_CORPUS",
    "dialect-sensory": "DIALECT_SENSORY",
}
HARD_REVIEW_CHECKS = (
    "fetch_fidelity", "rights_privacy", "originality", "scientific_rigor",
    "inference_bounds", "deduplication", "carr_intervention_utility",
    "counter_corpus", "belief_persona_safety_slots", "source_traceability",
)
EDITOR_GAP_KINDS = {
    "belief_persona", "floor", "slot", "safety", "diversity", "science_lineage",
    "counter_corpus", "intervention_utility", "deduplication", "inference_bounds",
}
REJECTION_FAMILIES = {
    "community", "study", "report", "transcript", "investigative", "forum", "unknown",
}
STATE = "state.json"
CHAPTER_GAP = "chapter-gap-request.json"
HEX = re.compile(r"^[0-9a-f]{64}$")
SAFE_SLUG = re.compile(r"[^a-z0-9]+")
SINGLE_LINE_CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f]")
EXCERPT_CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f-\x9f]")


class ResearchFactoryError(RuntimeError):
    pass


class ResearchBlocked(ResearchFactoryError):
    pass


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha(value):
    data = value if isinstance(value, bytes) else _canonical(value).encode("utf-8")
    return PS.sha(data)


def _utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _single_line(value, name, *, placeholder=True):
    """Validate untrusted text before rendering it into one Markdown field."""
    if not isinstance(value, str):
        raise ResearchBlocked(f"{name} is not text")
    clean = value.strip()
    if not clean or SINGLE_LINE_CONTROL.search(clean) or "```" in clean \
            or placeholder and RC.PLACEHOLDER.search(clean):
        raise ResearchBlocked(f"{name} is not safe resolved single-line text")
    return clean


def _excerpt(value):
    """Keep the exact fetched excerpt while preventing fence/control injection."""
    if not isinstance(value, str) or not value or value != value.strip() \
            or "```" in value or EXCERPT_CONTROL.search(value):
        raise ResearchBlocked("retained excerpt is not safe exact fetched text")
    return value


def _read_json(path, root, label):
    try:
        return json.loads(PS._safe_file(path, root).read_text(encoding="utf-8"))
    except (PS.StoreError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ResearchFactoryError(f"invalid {label}: {exc}") from exc


def _ensure_dir(path, boundary):
    try:
        if os.path.lexists(path):
            return PS.safe_dir(path, boundary)
        return PS.ensure_dir(path, boundary)
    except PS.StoreError as exc:
        raise ResearchFactoryError(str(exc)) from exc


def _factory_root(root):
    return Path(root).absolute() / "evidence" / "research-factory"


def _state_path(root):
    return _factory_root(root) / STATE


def _chapter_gap_path(root):
    return _factory_root(root) / CHAPTER_GAP


def _calls_root(root):
    return _factory_root(root) / "calls"


def _stage_book(ctx):
    return _factory_root(ctx["root"]) / "workshop" / ctx["book_relative"]


def _call_paths(root, call_id):
    if not re.fullmatch(r"[a-z0-9-]+", call_id):
        raise ResearchFactoryError(f"unsafe call id: {call_id}")
    base = _calls_root(root)
    return base / f"{call_id}.marker.json", base / f"{call_id}.result.json"


def _write_json(path, value, root):
    _ensure_dir(path.parent, Path(root).absolute())
    try:
        PS.write_json(path, value)
    except (PS.StoreError, OSError) as exc:
        raise ResearchFactoryError(str(exc)) from exc


def _publish_marker(path, value, root):
    """Marker publication seam used only to prove pre-dispatch crash recovery."""
    _write_json(path, value, root)


def _publish_file(path, data):
    """Final candidate publication seam for deterministic interruption proof."""
    PS.write(path, data)


def _context(candidate_root, *, mutable=True):
    root = Path(candidate_root).absolute()
    try:
        manifest = CP.inspect(root)
        allowed = {"CANDIDATE"} if mutable else {"CANDIDATE", "SEALED"}
        if manifest["state"] not in allowed or manifest.get("operation") is not None:
            purpose = ("one mutable pre-writer RF-02 candidate" if mutable else
                       "one candidate or sealed pre-decision RF-02 arm")
            raise ResearchFactoryError(f"research requires {purpose}")
        tree = CP.candidate_tree(root)
        book = tree / manifest["run"]["book"]
        config_path = CP.require_member(root, tree / manifest["run"]["config"], "config", manifest)
        prompt_path = CP.require_member(root, tree / "prompts/research-agent.md", "config", manifest)
        editor_prompt_path = CP.require_member(
            root, tree / "prompts/research-evidence-editor.md", "config", manifest)
        brief = CP.require_member(root, book / "00-brief.md", "product", manifest)
        SC.require_subject_contract(book, "research-synthesis")
        cfg = loopcfg.load(config_path)
    except (CP.PairError, SC.ContractError, PS.StoreError, OSError, SystemExit) as exc:
        raise ResearchFactoryError(f"research preflight failed: {exc}") from exc
    return {
        "root": root, "manifest": manifest, "tree": tree, "book": book,
        "book_relative": manifest["run"]["book"], "config_path": config_path,
        "prompt_path": prompt_path, "editor_prompt_path": editor_prompt_path,
        "brief_path": brief, "config": cfg,
    }


def _hash_group(files, values=None):
    """Bind a named causal group without returning its potentially sensitive bytes."""
    value_hash = _sha(values or {})
    body = {"files": dict(sorted(files.items())), "values_sha256": value_hash}
    return {**body, "sha256": _sha(body)}


def _causal_identities(ctx):
    """Derive the eight frozen research-treatment identities from declared bytes."""
    tree, manifest = ctx["tree"], ctx["manifest"]
    entry_paths = {item["path"] for item in manifest["entries"]}
    file_hashes = {relative: PS.sha(PS._safe_file(tree / relative, tree).read_bytes())
                   for relative in sorted(entry_paths)}
    book_prefix = ctx["book_relative"] + "/"
    brief_relative = book_prefix + "00-brief.md"
    config_relative = manifest["run"]["config"]

    def matches(names=(), prefixes=()):
        return {path: digest for path, digest in file_hashes.items()
                if path in names or any(path.startswith(prefix) for prefix in prefixes)}

    research_prompts = {
        "prompts/research-agent.md", "prompts/research-evidence-editor.md",
    }
    planning_files = matches(names={
        "prompts/master-plan-skill-v2.md", "prompts/master-plan-reviewer-v2.md"})
    commission_files = matches(names={
        "prompts/chapter-commissioner.md", "prompts/commission-set-auditor.md"})
    writing_files = matches(names={
        "prompts/chapter-writer.md", "prompts/style-guide.md"})
    downstream_artifacts = matches(prefixes=tuple(book_prefix + name for name in (
        "framing.md", "framing-review.md", "master-plan.md", "master-plan-review.md",
        "commissions/", "chapters/")))
    safety_files = matches(names={"prompts/grounded-reviewer.md"})
    evaluation_prompt_names = {
        "prompts/book-analysis-agent.md", "prompts/book-factory-reviewer.md",
        "prompts/chapter-reviewer.md", "prompts/developmental-reviewer.md",
    }
    evaluation_files = matches(names=evaluation_prompt_names)
    evaluation_root = CP.evaluation_tree(ctx["root"])
    for item in sorted(manifest["evaluation"], key=lambda row: row["path"]):
        relative = item["path"]
        evaluation_files["evaluation/" + relative] = PS.sha(
            PS._safe_file(evaluation_root / relative, evaluation_root).read_bytes())

    cfg = ctx["config"]
    research_config = {key: cfg[key] for key in sorted(cfg)
                       if key.startswith("researcher_") or key.startswith("research_")}
    model_fragments = (
        "model", "provider", "route", "reasoning", "endpoint", "temperature",
        "attempts", "allow_fallbacks", "family",
    )
    model_config = {key: cfg[key] for key in sorted(cfg)
                    if any(fragment in key for fragment in model_fragments)}
    planning_config = {key: cfg[key] for key in sorted(cfg) if key.startswith("planner_")}
    writing_config = {key: cfg[key] for key in sorted(cfg) if key.startswith("writer_")}
    safety_config = {key: cfg[key] for key in sorted(cfg)
                     if key.startswith("grounded_reviewer_")}
    evaluation_prefixes = (
        "developmental_reviewer_", "judge_", "product_effect_", "reference_",
    )
    evaluation_names = {
        "instrument_version", "weights", "epsilon", "originality_tripwire",
        "near_copy_tripwire", "length_band",
    }
    evaluation_config = {key: cfg[key] for key in sorted(cfg)
                         if key in evaluation_names
                         or any(key.startswith(prefix) for prefix in evaluation_prefixes)}
    input_config = {key: cfg[key] for key in sorted(cfg)
                    if key not in research_config}

    brief_text = ctx["brief_path"].read_text(encoding="utf-8")
    sections = SC._sections(brief_text)
    subject_contract = {
        "beliefs": list(SC.belief_set(brief_text)),
        "scalars": {name: SC.scalar_value(sections, name)
                    for name in SC.SCALAR_FIELDS},
        "forks": sections["Fork decisions"],
    }
    research_artifacts = {path for path in file_hashes
                          if path.startswith(book_prefix + "research/")}
    classified = ({brief_relative, config_relative} | research_prompts | research_artifacts
                  | set(planning_files) | set(commission_files) | set(writing_files)
                  | set(downstream_artifacts)
                  | set(safety_files) | set(evaluation_files))
    input_files = {path: digest for path, digest in file_hashes.items()
                   if path not in classified}

    frozen = {
        "subject": _hash_group({brief_relative: file_hashes[brief_relative]}, subject_contract),
        "input": _hash_group(input_files, input_config),
        "model": _hash_group({}, model_config),
        "planning": _hash_group(planning_files, planning_config),
        "commission": _hash_group(commission_files),
        "writing": _hash_group(writing_files, writing_config),
        "safety": _hash_group(safety_files, {
            "safety_perimeter": SC.scalar_value(sections, "Safety perimeter"),
            **safety_config}),
        "evaluation": _hash_group(evaluation_files, evaluation_config),
    }
    research_components = {
        relative: file_hashes[relative] for relative in sorted(research_prompts)
    }
    research_components[config_relative + "#research"] = _sha(research_config)
    research_body = {
        "components": research_components,
        "configuration_sha256": _sha(research_config),
    }
    research_bundle = {**research_body, "sha256": _sha(research_body)}
    return frozen, research_bundle


def preflight(candidate_root):
    """Read-only production preflight. It deliberately performs no credential check."""
    ctx = _context(candidate_root, mutable=False)
    frozen, research_bundle = _causal_identities(ctx)
    return {
        "candidate_root": str(ctx["root"]),
        "accepted_generation": ctx["manifest"]["accepted_generation"],
        "run": ctx["manifest"]["run"],
        "brief_sha256": PS.sha(ctx["brief_path"].read_bytes()),
        "configuration_sha256": PS.sha(ctx["config_path"].read_bytes()),
        "prompt_sha256": PS.sha(ctx["prompt_path"].read_bytes()),
        "frozen_variables": {key: value["sha256"] for key, value in frozen.items()},
        "frozen_components": frozen,
        "research_bundle": research_bundle,
    }


def require_control_baseline(candidate_root):
    """Prove the control's research components still equal its accepted snapshot."""
    identity = preflight(candidate_root)
    root = Path(candidate_root).absolute()
    manifest = CP.load(root)
    entries = {item["path"]: item for item in manifest["entries"]}
    for component in identity["research_bundle"]["components"]:
        relative = component.partition("#")[0]
        item = entries.get(relative)
        if item is None or item.get("group") != "config":
            raise ResearchBlocked(
                f"control research component lacks accepted authority: {relative}")
        path = CP.require_member(root, CP.candidate_tree(root) / relative,
                                 "config", manifest)
        if PS.sha(path.read_bytes()) != item.get("accepted_sha256"):
            raise ResearchBlocked(
                f"control research component differs from accepted baseline: {relative}")
    return identity


def completed_experiment(candidate_root):
    """Return a prior isolated arm seal only when its durable run finished here."""
    ctx = _context(candidate_root, mutable=False)
    state_path = _state_path(ctx["root"])
    if not state_path.is_file():
        return None
    state = _read_json(state_path, ctx["root"], "research state")
    seal = _current_seal(ctx)
    required = {"lead-plan", *(f"lane-{index}-{lane}"
                 for index, lane in enumerate(LANES, 1))}
    if state.get("stage") != "SEALED" or state.get("seal_identity") != seal \
            or not required <= set(state.get("results", {})):
        return None
    return seal


def _current_seal(ctx):
    try:
        return RC.research_seal_identity(ctx["book"])
    except (RC.ContractError, SC.ContractError, OSError):
        return None


def _validated_chapter_gap(ctx, value):
    """Bind one explicit targeted continuation to the current seal and card."""
    if not isinstance(value, dict) or set(value) != {
            "schema", "research_seal_sha256", "chapter_id", "plan", "card", "gaps"} \
            or value.get("schema") != 1:
        raise ResearchBlocked("chapter research gap request shape is invalid")
    seal = _current_seal(ctx)
    if seal is None or value.get("research_seal_sha256") != seal:
        raise ResearchBlocked("chapter research gap request binds a stale research seal")
    chapter = _single_line(value.get("chapter_id"), "chapter gap chapter")
    if re.fullmatch(r"C-\d{2}", chapter) is None:
        raise ResearchBlocked("chapter research gap request has an invalid chapter")
    plan_relative = ctx["book_relative"] + "/master-plan.md"
    plan_record, card_record = value.get("plan"), value.get("card")
    if not isinstance(plan_record, dict) or set(plan_record) != {"path", "sha256"} \
            or not isinstance(card_record, dict) or set(card_record) != {"path", "sha256"} \
            or plan_record.get("path") != plan_relative \
            or card_record.get("path") != f"{plan_relative}#{chapter}":
        raise ResearchBlocked("chapter research gap request has invalid plan/card bindings")
    plan_path = CP.require_member(
        ctx["root"], ctx["tree"] / plan_relative, "product", ctx["manifest"])
    plan_bytes = plan_path.read_bytes()
    try:
        plan_text = plan_bytes.decode("utf-8").replace("\r\n", "\n")
        card = CS._section(plan_text, "C", int(chapter.removeprefix("C-")))
    except (UnicodeError, CS.CommissionSetError) as exc:
        raise ResearchBlocked("chapter research gap request cannot resolve its card") from exc
    if plan_record.get("sha256") != PS.sha(plan_text.encode("utf-8")) \
            or card_record.get("sha256") != PS.sha(card.encode("utf-8")):
        raise ResearchBlocked("chapter research gap request plan/card binding is stale")
    gaps = value.get("gaps")
    if not isinstance(gaps, list) or len(gaps) != 1:
        raise ResearchBlocked("chapter research gap request has no demonstrated gap")
    normalized = []
    for gap in gaps:
        if not isinstance(gap, dict) or set(gap) != {"code", "detail"}:
            raise ResearchBlocked("chapter research gap item shape is invalid")
        code = _single_line(gap["code"], "chapter gap code")
        detail = _single_line(gap["detail"], "chapter gap detail")
        if re.fullmatch(r"[a-z][a-z0-9_]{1,63}", code) is None:
            raise ResearchBlocked("chapter research gap code is invalid")
        if code != "unit_missing":
            raise ResearchBlocked("only a proven missing research unit may target continuation")
        normalized.append({"code": code, "detail": detail})
    canonical = {"schema": 1, "research_seal_sha256": seal, "chapter_id": chapter,
                 "plan": dict(plan_record), "card": dict(card_record), "gaps": normalized}
    try:
        demonstrated = CS.chapter_gap_request(
            ctx["root"], int(chapter.removeprefix("C-")))
    except CS.CommissionSetError as exc:
        raise ResearchBlocked(
            "chapter research gap is not currently demonstrated by the dispatch gate") from exc
    if demonstrated != canonical:
        raise ResearchBlocked(
            "chapter research gap request differs from the current dispatch-gate proof")
    return canonical


def _persist_chapter_gap(ctx, value):
    value = _validated_chapter_gap(ctx, value)
    path = _chapter_gap_path(ctx["root"])
    if os.path.lexists(path):
        existing = _read_json(path, ctx["root"], "chapter gap request")
        if existing != value:
            if not os.path.lexists(_state_path(ctx["root"])):
                raise ResearchBlocked("another chapter research gap request is already durable")
            state = _read_json(_state_path(ctx["root"]), ctx["root"], "research state")
            if state.get("stage") != "SEALED" or state.get("seal_identity") != _current_seal(ctx) \
                    or state.get("chapter_gap_sha256") != _sha(existing):
                raise ResearchBlocked("another chapter research gap request is already durable")
            state["chapter_gap_rotation"] = {
                "previous_request_sha256": _sha(existing),
                "previous_chapter_id": existing.get("chapter_id"),
                "resulting_seal_identity": state["seal_identity"],
                "next_request": value,
                "next_request_sha256": _sha(value),
            }
            _write_json(_state_path(ctx["root"]), state, ctx["root"])
            return _finish_chapter_gap_rotation(ctx, state)
    else:
        _write_json(path, value, ctx["root"])
    return value


def _finish_chapter_gap_rotation(ctx, state):
    """Complete either side of the durable request-rotation write boundary."""
    rotation = state.get("chapter_gap_rotation")
    if not isinstance(rotation, dict) or set(rotation) != {
            "previous_request_sha256", "previous_chapter_id",
            "resulting_seal_identity", "next_request", "next_request_sha256"}:
        raise ResearchBlocked("chapter research gap rotation state is invalid")
    next_request = _validated_chapter_gap(ctx, rotation["next_request"])
    if rotation["next_request_sha256"] != _sha(next_request) \
            or state.get("stage") != "SEALED" \
            or state.get("seal_identity") != rotation["resulting_seal_identity"] \
            or state.get("chapter_gap_sha256") != rotation["previous_request_sha256"]:
        raise ResearchBlocked("chapter research gap rotation identity is stale")
    path = _chapter_gap_path(ctx["root"])
    current = _read_json(path, ctx["root"], "chapter gap request")
    current_sha = _sha(current)
    if current_sha == rotation["previous_request_sha256"]:
        _write_json(path, next_request, ctx["root"])
    elif current_sha != rotation["next_request_sha256"] or current != next_request:
        raise ResearchBlocked("chapter research gap rotation file is stale")
    completed = {"request_sha256": rotation["previous_request_sha256"],
                 "chapter_id": rotation["previous_chapter_id"],
                 "resulting_seal_identity": rotation["resulting_seal_identity"]}
    history = state.setdefault("completed_chapter_gaps", [])
    if completed not in history:
        history.append(completed)
    for key in ("chapter_gap_sha256", "chapter_gap_start_round",
                "chapter_gap_round", "chapter_round_gaps", "chapter_gap_rotation"):
        state.pop(key, None)
    _write_json(_state_path(ctx["root"]), state, ctx["root"])
    return next_request


def _positive(cfg, name, cast=int):
    try:
        value = cast(cfg[name])
    except (KeyError, TypeError, ValueError) as exc:
        raise ResearchFactoryError(f"missing or invalid research policy: {name}") from exc
    if value <= 0:
        raise ResearchFactoryError(f"research policy must be positive: {name}")
    return value


def policy_from_config(cfg):
    if (cfg.get("researcher_model"), cfg.get("researcher_provider"),
            cfg.get("researcher_reasoning"), cfg.get("researcher_endpoint")) != (
            MODEL, "openrouter", "xhigh", ENDPOINT):
        raise ResearchFactoryError("research route differs from RF-32 production law")
    blocked = cfg.get("research_blocked_domains")
    if not isinstance(blocked, list) or "reddit.com" not in blocked:
        raise ResearchFactoryError("research blocked-domain policy must exclude Reddit")
    return {
        "call_ceiling": _positive(cfg, "research_call_ceiling"),
        "gap_round_ceiling": _positive(cfg, "research_gap_round_ceiling"),
        "input_tokens_per_call": _positive(cfg, "research_input_tokens_per_call"),
        "serialized_input_bytes": _positive(cfg, "research_serialized_input_bytes"),
        "output_tokens_per_call": _positive(cfg, "research_output_tokens_per_call"),
        "total_output_tokens": _positive(cfg, "research_total_output_tokens"),
        "retained_results_per_call": _positive(
            cfg, "research_retained_results_per_call"),
        "retained_result_ceiling": _positive(cfg, "research_retained_result_ceiling"),
        "retained_excerpt_characters": _positive(
            cfg, "research_retained_excerpt_characters"),
        "editor_input_bytes": _positive(cfg, "research_editor_input_bytes"),
        "cost_ceiling_usd": _positive(cfg, "research_cost_ceiling_usd", float),
        "search_results_per_call": _positive(cfg, "research_search_results_per_call"),
        "search_characters_per_call": _positive(
            cfg, "research_search_characters_per_call"),
        "search_requests_per_call": _positive(cfg, "research_search_requests_per_call"),
        "search_requests_total": _positive(cfg, "research_search_requests_total"),
        "fetch_uses_per_call": _positive(cfg, "research_fetch_uses_per_call"),
        "fetch_uses_total": _positive(cfg, "research_fetch_uses_total"),
        "fetch_content_tokens_per_call": _positive(
            cfg, "research_fetch_content_tokens_per_call"),
        "blocked_domains": sorted(set(str(item).casefold() for item in blocked)),
    }


class OpenRouterTransport:
    """Fixed production transport; the credential is kept only in request headers."""
    def __init__(self, key, open_url=urllib.request.urlopen):
        if not isinstance(key, str) or not key.strip():
            raise ResearchFactoryError("OPENROUTER_API_KEY is missing")
        self._key = key.strip()
        self._open = open_url

    def _request(self, url, method="GET", body=None, timeout=600):
        headers = {"Authorization": f"Bearer {self._key}",
                   "X-OpenRouter-Metadata": "enabled"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=body, method=method, headers=headers)
        try:
            with self._open(request, timeout=timeout) as response:
                return json.loads(response.read())
        except (urllib.error.URLError, OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ResearchBlocked(f"OpenRouter transport failed: {type(exc).__name__}") from exc

    def pricing(self, policy):
        value = self._request(PRICING_ENDPOINT, timeout=60)
        endpoints = value.get("data", {}).get("endpoints") if isinstance(value, dict) else None
        if not isinstance(endpoints, list) or not endpoints:
            raise ResearchBlocked("pricing preflight returned no eligible endpoint metadata")
        costs = []
        for endpoint in endpoints:
            pricing = endpoint.get("pricing") if isinstance(endpoint, dict) else None
            try:
                prompt = float(pricing["prompt"])
                completion = float(pricing["completion"])
                search = float(pricing["web_search"])
                request = float(pricing.get("request", 0))
            except (KeyError, TypeError, ValueError):
                continue
            if min(prompt, completion, search, request) < 0:
                continue
            tool_context = ((policy["fetch_uses_per_call"]
                             + policy["search_results_per_call"])
                            * policy["fetch_content_tokens_per_call"])
            costs.append(request + prompt * (policy["input_tokens_per_call"] + tool_context)
                         + completion * policy["output_tokens_per_call"]
                         + search * (policy["search_requests_per_call"]
                                     + policy["fetch_uses_per_call"]))
        if not costs:
            raise ResearchBlocked("pricing/tool-cost metadata is missing or contradictory")
        maximum = max(costs)
        if maximum <= 0:
            raise ResearchBlocked("pricing preflight produced a nonpositive reservation")
        return {"schema": 1, "model": MODEL, "max_cost_per_call": maximum,
                "endpoint_count": len(costs)}

    def call(self, payload):
        data = self._request(ENDPOINT, "POST", _canonical(payload).encode("utf-8"))
        if not isinstance(data, dict) or data.get("status") != "completed" \
                or data.get("error") not in (None, {}) or not isinstance(data.get("output"), list):
            raise ResearchBlocked("OpenRouter Responses result is incomplete or not completed")
        texts, fetches, search_count, fetch_count = [], [], 0, 0
        for item in data["output"]:
            if not isinstance(item, dict):
                raise ResearchBlocked("OpenRouter Responses output item is malformed")
            item_type = item.get("type")
            if item_type == "message":
                if item.get("status") not in (None, "completed"):
                    raise ResearchBlocked("OpenRouter assistant output did not complete")
                for part in item.get("content", ()):
                    if isinstance(part, dict) and part.get("type") == "output_text" \
                            and isinstance(part.get("text"), str):
                        texts.append(part["text"])
            elif item_type == "openrouter:web_search":
                search_count += 1
                if item.get("status") != "completed" or item.get("error"):
                    raise ResearchBlocked("OpenRouter web search item did not complete")
            elif item_type == "openrouter:web_fetch":
                fetch_count += 1
                status = item.get("httpStatus")
                try:
                    url = _canonical_url(item.get("url"))
                except ResearchBlocked as exc:
                    raise ResearchBlocked(
                        "OpenRouter web fetch item lacks successful content proof") from exc
                if item.get("status") != "completed" or item.get("error") \
                        or not isinstance(item.get("content"), str) or not item["content"] \
                        or status is not None and (
                            type(status) is not int or not 200 <= status < 300):
                    raise ResearchBlocked("OpenRouter web fetch item lacks successful content proof")
                fetches.append({"url": url, "title": item.get("title"),
                                "content": item["content"]})
        content = "".join(texts)
        usage = data.get("usage")
        input_tokens = usage.get("input_tokens") if isinstance(usage, dict) else None
        output_tokens = usage.get("output_tokens") if isinstance(usage, dict) else None
        total_tokens = usage.get("total_tokens") if isinstance(usage, dict) else None
        cost = usage.get("cost") if isinstance(usage, dict) else None
        details = usage.get("server_tool_use_details") if isinstance(usage, dict) else None
        legacy = usage.get("server_tool_use") if isinstance(usage, dict) else None
        counted = {"web_search_requests": search_count, "web_fetch_requests": fetch_count}
        observed_total = search_count + fetch_count
        details_ok = details is None
        if isinstance(details, dict):
            executed = details.get("tool_calls_executed")
            requested = details.get("tool_calls_requested")
            reported_search = details.get("web_search_requests")
            details_ok = all(value is None or type(value) is int and value >= 0
                             for value in (executed, requested, reported_search)) \
                and (executed is None or executed == observed_total) \
                and (requested is None or requested >= observed_total) \
                and (reported_search is None or reported_search == search_count)
        legacy_ok = legacy is None
        if isinstance(legacy, dict):
            reported_search = legacy.get("web_search_requests")
            legacy_ok = reported_search is None or (
                type(reported_search) is int and reported_search == search_count)
        if not content or any(type(value) is not int or value < 0
                              for value in (input_tokens, output_tokens, total_tokens)) \
                or total_tokens < input_tokens + output_tokens \
                or not isinstance(cost, (int, float)) or cost < 0 \
                or not details_ok or not legacy_ok:
            raise ResearchBlocked("OpenRouter Responses usage/content/tool counts are incomplete")
        return {"content": content, "model": data.get("model"),
                "usage": {"input_tokens": input_tokens,
                          "completion_tokens": output_tokens,
                          "total_tokens": total_tokens, "cost": cost,
                          "server_tool_use": counted},
                "fetches": fetches}


def _editor_schema():
    checks = {name: {"type": "string", "enum": ["PASS", "BLOCKED"]}
              for name in HARD_REVIEW_CHECKS}
    return {"type": "object", "additionalProperties": False,
            "properties": {
                "status": {"type": "string", "enum": ["PASS", "BLOCKED"]},
                "gaps": {"type": "array", "items": _object_schema({
                    "kind": {"enum": sorted(EDITOR_GAP_KINDS)},
                    "target": {"type": "string", "minLength": 1},
                    "message": {"type": "string", "minLength": 1}})},
                "checks": {"type": "object", "additionalProperties": False,
                           "properties": checks, "required": list(checks)},
                "scarcity_waivers": {"type": "array", "items": {
                    "type": "object", "additionalProperties": False,
                    "properties": {
                        "floor": {"type": "string"},
                        "attempts_sha256": {"type": "string"},
                        "demonstrated_ceiling": {"type": "integer"},
                        "finding": {"type": "string"},
                    }, "required": ["floor", "attempts_sha256",
                                    "demonstrated_ceiling", "finding"]}},
            }, "required": ["status", "gaps", "checks", "scarcity_waivers"]}


def _editor_input(task):
    return (task["prompt"] + "\n\nExact candidate task:\n" + _canonical(task)).encode("utf-8")


def _editor_schema_bytes():
    return json.dumps(_editor_schema(), sort_keys=True, separators=(",", ":")).encode("utf-8")


class NativeEvidenceEditor:
    def review(self, task):
        import native_judge as native
        content = _editor_input(task).decode("utf-8")
        raw, transport, error = native.complete(
            content, "research-evidence-editor", _editor_schema(),
            model="gpt-5.6-sol", reasoning="xhigh")
        if error:
            raise ResearchBlocked(error)
        try:
            verdict = json.loads(raw)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ResearchBlocked("native evidence editor returned invalid JSON") from exc
        return {"verdict": verdict,
                "transport": {key: transport.get(key) for key in (
                    "kind", "judge_identity", "model", "reasoning_effort",
                    "fresh_ephemeral_context", "isolated_workdir", "thread_id", "usage",
                    "input_sha256", "output_schema_sha256")}}


def _object_schema(properties, required=None):
    return {"type": "object", "properties": properties,
            "required": required or list(properties), "additionalProperties": False}


def _response_schema(kind):
    string = {"type": "string", "minLength": 1}
    strings = {"type": "array", "items": string, "minItems": 1}
    if kind == "plan":
        persona = _object_schema({"id": string, "context": string,
            "applicable_beliefs": strings,
            "applicable_banks": {"type": "array", "items": {"type": "integer",
                                                                "minimum": 1, "maximum": 10},
                                 "minItems": 1}})
        return _object_schema({"kind": {"const": "plan"},
            "preset": {"enum": ["FULL-LENGTH", "POCKET"]},
            "coverage_plan": _object_schema({"beliefs": strings, "questions": strings,
                "personas": {"type": "array", "items": persona, "minItems": 3}}),
            "commissions": _object_schema({lane: string for lane in LANES})})
    if kind in ("discovery", "gap-fill"):
        scientific = _object_schema({name: string for name in
            ("design", "class", "lineage", "grade_rationale", "scope", "counterevidence")})
        evidence = _object_schema({
            "kind": {"enum": ["EXACT_QUOTE", "INTERPRETATION"]}, "text": string,
            "persona_tags": strings,
            "bank_slots": {"type": "array", "items": {"type": "integer", "minimum": 1,
                                                         "maximum": 10}, "minItems": 1},
            "beliefs": strings, "style_slots": strings, "safety_boundary": string,
            "evidence_grade": {"enum": ["SUPPORTED", "MIXED", "CONTESTED", "n/a"]},
            **{name: string for name in ("grade_rationale", "scope", "counterevidence",
                "permitted_inference", "prohibited_inference", "situation", "emotion",
                "semantic_key", "claim_key", "story_key", "testimonial_qualification")},
            "scientific": {"anyOf": [scientific, {"type": "null"}]},
        })
        rights = _object_schema({
            **{name: {"const": "PASS"} for name in
               ("access", "excerpt", "redistribution", "attribution", "retention", "privacy")},
            "deletion_sensitive": {"const": False},
            "personal_data_retention": {"enum": ["NONE", "MINIMAL_REQUIRED_ATTRIBUTION"]},
        })
        accepted = _object_schema({
            **{name: string for name in ("url", "title", "source_type", "source_family",
                "author_organization", "discovery_lane", "story_identity", "study_lineage",
                "study_design_class")},
            "rights": rights,
            "rights_basis": _object_schema({name: string for name in
                ("access", "excerpt", "redistribution", "attribution", "retention", "privacy")}),
            "fetch": _object_schema({"url": string, "locator": string, "excerpt": string}),
            "evidence": {"type": "array", "items": evidence, "minItems": 1},
        })
        rejection = _object_schema({"source_family": {"enum": sorted(REJECTION_FAMILIES)},
                                    "reason": string,
                                    "count": {"type": "integer", "minimum": 1}})
        return _object_schema({"kind": {"const": "discovery"},
            "accepted": {"type": "array", "items": accepted},
            "rejections": {"type": "array", "items": rejection}})
    if kind == "synthesis":
        return _object_schema({"kind": {"const": "synthesis"},
            "selected_evidence_keys": {"type": "array", "items": string},
            "notes": {"type": "array", "items": string}})
    raise ResearchFactoryError(f"unknown response schema kind: {kind}")


def _payload(prompt, request, policy, tools):
    value = {
        "model": MODEL,
        "reasoning": {"effort": "xhigh"},
        "instructions": prompt,
        "input": _canonical(request),
        "max_output_tokens": policy["output_tokens_per_call"],
        "text": {"format": {"type": "json_schema", "name": "research_" + request["kind"].replace("-", "_"),
                            "schema": _response_schema(request["kind"]), "strict": True}},
        "store": False,
    }
    if tools:
        value["max_tool_calls"] = (policy["search_requests_per_call"]
                                   + policy["fetch_uses_per_call"])
        value["tools"] = [
            {"type": "openrouter:web_search",
             "parameters": {"engine": "exa",
                            "max_results": policy["search_results_per_call"],
                            "max_total_results": policy["search_results_per_call"],
                            "max_characters": policy["search_characters_per_call"],
                            "excluded_domains": policy["blocked_domains"]}},
            {"type": "openrouter:web_fetch",
             "parameters": {"engine": "openrouter",
                            "max_uses": policy["fetch_uses_per_call"],
                            "max_content_tokens": policy["fetch_content_tokens_per_call"],
                            "blocked_domains": policy["blocked_domains"]}},
        ]
    return value


def _validate_payload_reservation(payload, policy):
    # UTF-8 bytes are a conservative upper bound on model input tokens. Server-
    # tool result context is not in this request and is reserved by pricing().
    if len(_canonical(payload).encode("utf-8")) > policy["serialized_input_bytes"] \
            or policy["serialized_input_bytes"] > policy["input_tokens_per_call"]:
        raise ResearchBlocked("serialized research input exceeds its pre-dispatch reservation")


def _response_contract(kind):
    """Exact machine contract given to the model; Markdown is rendered by code."""
    if kind == "plan":
        return {"kind": "plan", "preset": "FULL-LENGTH|POCKET",
                "coverage_plan": {"questions": ["model-owned subject question"],
                    "personas": [{"id": "P-01", "context": "materially distinct subject-specific context",
                                  "applicable_beliefs": ["exact brief belief"],
                                  "applicable_banks": [1]}]},
                "commissions": {lane: "nonempty subject-specific commission" for lane in LANES}}
    if kind in ("discovery", "gap-fill"):
        return {"kind": "discovery", "accepted": [{
            "url": "canonical fetched http(s) URL", "title": "source title",
            "source_type": "community|study|report|transcript|investigative",
            "source_family": "generic policy-level family", "author_organization": "author or organization",
            "discovery_lane": "one exact enum: " + "|".join(sorted(RC.LANES)),
            "story_identity": "stable story key or n/a", "study_lineage": "lineage or n/a",
            "study_design_class": "design/class or n/a",
            "rights": {"access": "PASS", "excerpt": "PASS", "redistribution": "PASS",
                       "attribution": "PASS", "retention": "PASS", "privacy": "PASS",
                       "deletion_sensitive": False,
                       "personal_data_retention": "NONE|MINIMAL_REQUIRED_ATTRIBUTION"},
            "rights_basis": {key: "substantive verified basis" for key in
                             ("access", "excerpt", "redistribution", "attribution", "retention", "privacy")},
            "fetch": {"url": "same canonical URL", "locator": "precise locator",
                      "excerpt": "unchanged minimum excerpt from caller-visible fetch annotation"},
            "evidence": [{"kind": "EXACT_QUOTE|INTERPRETATION", "text": "exact or unquoted text",
                "persona_tags": ["P-01"], "bank_slots": [1], "beliefs": ["exact brief belief"],
                "style_slots": sorted(RC.SLOTS), "safety_boundary": "exact brief Safety perimeter",
                "evidence_grade": "SUPPORTED|MIXED|CONTESTED|n/a",
                "grade_rationale": "why this grade is bounded", "scope": "claim scope",
                "counterevidence": "material disagreement or none found after named search",
                "permitted_inference": "exact bounded inference", "prohibited_inference": "exact excluded claim",
                "situation": "source-grounded situation", "emotion": "source-grounded emotion",
                "semantic_key": "normalized evidence-meaning key", "claim_key": "cross-lineage claim key",
                "story_key": "story key or n/a", "testimonial_qualification":
                    "NOT_CANDIDATE or QUALIFIED; numbers=...; sensory=...; authority_conflict=...",
                "scientific": "null unless Bank 7/8, else {design,class,lineage,grade_rationale,scope,counterevidence}"}]}],
            "rejections": [{"source_family": "generic family", "reason":
                "access ineligible|excerpt ineligible|redistribution ineligible|attribution ineligible|retention ineligible|deletion sensitive|privacy basis failed|personal data|no eligible evidence|rights/privacy ineligible|source excluded|duplicate",
                "count": 1}]}
    if kind == "synthesis":
        return {"kind": "synthesis", "selected_evidence_keys":
                "array containing only supplied evidence keys", "notes": ["bounded synthesis judgment"]}
    raise ResearchFactoryError(f"unknown response contract kind: {kind}")


def _canonical_url(value):
    value = _single_line(value, "source URL", placeholder=False)
    try:
        parsed = urllib.parse.urlsplit(value)
        host = parsed.hostname
        port = parsed.port
        username = parsed.username
    except (UnicodeError, ValueError) as exc:
        raise ResearchBlocked("accepted source has an invalid URL") from exc
    if parsed.scheme not in ("http", "https") or not parsed.netloc or username or not host:
        raise ResearchBlocked("accepted source has an invalid URL")
    host = host.casefold()
    if host in {"reddit.com", "www.reddit.com"} or host.endswith(".reddit.com"):
        raise ResearchBlocked("excluded Reddit material reached eligibility filtering")
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query = [(key, val) for key, val in query if not key.casefold().startswith("utm_")]
    canonical_host = f"[{host}]" if ":" in host else host
    netloc = canonical_host + (f":{port}" if port else "")
    path = parsed.path.rstrip("/") or "/"
    return urllib.parse.urlunsplit((parsed.scheme.casefold(), netloc, path,
                                    urllib.parse.urlencode(sorted(query)), ""))


def _json_content(value, expected):
    raw = value.get("content") if isinstance(value, dict) else None
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ResearchBlocked(f"{expected} response is not JSON") from exc
    if not isinstance(raw, dict) or raw.get("kind") != expected:
        raise ResearchBlocked(f"{expected} response has an invalid contract")
    return raw


def _usage(value, reservation, needs_tools):
    if value.get("model") != MODEL:
        raise ResearchBlocked("provider returned a different research model")
    usage = value.get("usage")
    if not isinstance(usage, dict) or any(type(usage.get(name)) is not int
                                          for name in ("input_tokens", "completion_tokens",
                                                       "total_tokens")):
        raise ResearchBlocked("provider usage is missing")
    if min(usage["input_tokens"], usage["completion_tokens"], usage["total_tokens"]) < 0 \
            or usage["total_tokens"] < usage["input_tokens"] + usage["completion_tokens"]:
        raise ResearchBlocked("provider usage is contradictory")
    try:
        cost = float(usage["cost"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ResearchBlocked("provider cost is missing") from exc
    tools = usage.get("server_tool_use")
    if tools is None and not needs_tools:
        tools = {}
    if not isinstance(tools, dict):
        raise ResearchBlocked("provider server-tool usage is missing")
    search = tools.get("web_search_requests", 0)
    fetch = tools.get("web_fetch_requests", 0)
    if any(type(item) is not int or item < 0 for item in (search, fetch)):
        raise ResearchBlocked("provider server-tool counts are invalid")
    if usage["input_tokens"] > reservation["input_tokens"] \
            or usage["completion_tokens"] > reservation["output_tokens"] \
            or cost > reservation["cost_usd"] \
            or search > reservation["search_requests"] or fetch > reservation["fetch_uses"]:
        raise ResearchBlocked("provider exceeded its reserved ceiling")
    return {"input_tokens": usage["input_tokens"],
            "completion_tokens": usage["completion_tokens"],
            "total_tokens": usage["total_tokens"], "cost": cost,
            "server_tool_use": {"web_search_requests": search,
                                "web_fetch_requests": fetch}}


def _aggregate_rejections(rows):
    counts = {}
    allowed_reasons = {
        "access ineligible", "excerpt ineligible", "redistribution ineligible",
        "attribution ineligible", "retention ineligible", "deletion sensitive",
        "privacy basis failed", "personal data", "no eligible evidence",
        "rights/privacy ineligible", "source excluded", "duplicate",
    }
    for row in rows:
        if not isinstance(row, dict):
            raise ResearchBlocked("rejection aggregate is malformed")
        family = str(row.get("source_family", "unknown")).strip().casefold()
        reason = str(row.get("reason", "eligibility failed")).strip().casefold()
        try:
            count = int(row.get("count", 1))
        except (TypeError, ValueError) as exc:
            raise ResearchBlocked("rejection count is malformed") from exc
        if family not in REJECTION_FAMILIES or reason not in allowed_reasons \
                or count <= 0:
            raise ResearchBlocked("rejection record contains source-specific material")
        counts[(family, reason)] = counts.get((family, reason), 0) + count
    return [{"source_family": key[0], "reason": key[1], "count": count}
            for key, count in sorted(counts.items())]


def _safe_list(value, name):
    if not isinstance(value, list) or not value:
        raise ResearchBlocked(f"accepted evidence has no {name}")
    return [_single_line(item, f"accepted evidence {name}") for item in value]


def _rejection_family(row):
    value = str(row.get("source_type", "unknown")).strip().casefold()
    return value if value in REJECTION_FAMILIES else "unknown"


def _sanitize_candidate(row, annotations, lane, safety_boundary, persona_plan, received_utc,
                        excerpt_limit):
    if not isinstance(row, dict):
        raise ResearchBlocked("accepted source candidate is malformed")
    required_identity = ("url", "title", "source_type", "source_family",
                         "author_organization", "rights_basis",
                         "fetch", "evidence")
    if any(name not in row for name in required_identity):
        raise ResearchBlocked("accepted source identity/provenance is incomplete")
    rights = row.get("rights")
    required = ("access", "excerpt", "redistribution", "attribution", "retention", "privacy")
    if not isinstance(rights, dict) or any(rights.get(key) != "PASS" for key in required) \
            or rights.get("deletion_sensitive") is not False \
            or rights.get("personal_data_retention") not in {
                "NONE", "MINIMAL_REQUIRED_ATTRIBUTION"}:
        return None, (_rejection_family(row), "rights/privacy ineligible")
    url = _canonical_url(row.get("url"))
    citation = annotations.get(url)
    fetch = row.get("fetch")
    if not isinstance(fetch, dict) or _canonical_url(fetch.get("url")) != url or citation is None:
        raise ResearchBlocked("eligible source lacks a matching caller-visible fetch annotation")
    excerpt = _excerpt(fetch.get("excerpt"))
    locator = _single_line(fetch.get("locator"), "fetch locator")
    if not excerpt or not locator or excerpt not in citation["content"] \
            or len(excerpt) > excerpt_limit:
        raise ResearchBlocked("retained excerpt is not exact caller-visible fetched content")
    evidence = []
    for item in row.get("evidence", ()):
        if not isinstance(item, dict):
            raise ResearchBlocked("evidence item is malformed")
        kind = item.get("kind")
        text = _single_line(item.get("text"), "evidence text")
        if kind not in ("EXACT_QUOTE", "INTERPRETATION") or not text:
            raise ResearchBlocked("evidence kind/text is invalid")
        if kind == "EXACT_QUOTE" and text not in excerpt:
            raise ResearchBlocked("exact quote is absent from retained excerpt")
        grade = item.get("evidence_grade")
        if grade not in ("SUPPORTED", "MIXED", "CONTESTED", "n/a"):
            raise ResearchBlocked("evidence grade is invalid")
        banks = item.get("bank_slots")
        if not isinstance(banks, list) or any(type(bank) is not int or not 1 <= bank <= 10 for bank in banks):
            raise ResearchBlocked("evidence bank slots are invalid")
        permitted = _single_line(item.get("permitted_inference"), "permitted inference")
        prohibited = _single_line(item.get("prohibited_inference"), "prohibited inference")
        style_slots = _safe_list(item.get("style_slots"), "style slots")
        safety = _single_line(item.get("safety_boundary"), "safety boundary")
        if any(slot not in RC.SLOTS for slot in style_slots) or safety != safety_boundary \
                or not permitted or not prohibited or permitted == prohibited:
            raise ResearchBlocked("evidence inference bounds are incomplete")
        grade_rationale = _single_line(item.get("grade_rationale"), "grade rationale")
        scope = _single_line(item.get("scope"), "evidence scope")
        counterevidence = _single_line(item.get("counterevidence"), "counterevidence")
        testimonial = _single_line(
            item.get("testimonial_qualification", "NOT_CANDIDATE"),
            "testimonial qualification")
        if not grade_rationale or not scope or not counterevidence \
                or testimonial != "NOT_CANDIDATE" and re.fullmatch(
                    r"QUALIFIED;\s*numbers=.+;\s*sensory=.+;\s*authority_conflict=.+",
                    testimonial) is None:
            raise ResearchBlocked("evidence grade/scope/testimonial metadata is incomplete")
        scientific = item.get("scientific")
        if any(bank in (7, 8) for bank in banks):
            names = ("design", "class", "lineage", "grade_rationale", "scope", "counterevidence")
            if not isinstance(scientific, dict):
                raise ResearchBlocked("scientific lineage or rigor fields are incomplete")
            scientific = {name: _single_line(scientific.get(name), f"scientific {name}")
                          for name in names}
        else:
            scientific = None
        persona_tags = _safe_list(item.get("persona_tags"), "personas")
        beliefs = [_single_line(value, "evidence belief").strip('"“”')
                   for value in item.get("beliefs", ())]
        if any(persona not in persona_plan for persona in persona_tags) \
                or any(not set(beliefs).issubset(persona_plan[persona]["applicable_beliefs"])
                       or not set(banks).issubset(persona_plan[persona]["applicable_banks"])
                       for persona in persona_tags):
            raise ResearchBlocked("evidence persona/belief/bank tags exceed the lead coverage plan")
        evidence.append({
            "kind": kind, "text": text, "persona_tags": persona_tags,
            "bank_slots": sorted(set(banks)), "evidence_grade": grade,
            "style_slots": style_slots, "safety_boundary": safety,
            "permitted_inference": permitted, "prohibited_inference": prohibited,
            "situation": _single_line(item.get("situation"), "evidence situation"),
            "emotion": _single_line(item.get("emotion"), "evidence emotion"),
            "beliefs": beliefs,
            "semantic_key": _single_line(item.get("semantic_key"), "semantic key").casefold(),
            "claim_key": _single_line(item.get("claim_key"), "claim key").casefold(),
            "story_key": _single_line(item.get("story_key"), "story key").casefold(),
            "grade_rationale": grade_rationale, "scope": scope,
            "counterevidence": counterevidence,
            "testimonial_qualification": testimonial,
            "scientific": scientific,
        })
    if not evidence:
        return None, (_rejection_family(row), "no eligible evidence")
    if any(not item["semantic_key"] or not item["claim_key"] for item in evidence):
        raise ResearchBlocked("accepted evidence lacks semantic or cross-lineage claim keys")
    lane_id = LANE_IDS.get(lane, row.get("discovery_lane"))
    if lane_id not in RC.LANES:
        raise ResearchBlocked("accepted source has no canonical discovery lane")
    author = _single_line(row.get("author_organization"), "source author/organization")
    family = _single_line(row.get("source_family"), "source family").casefold()
    story = _single_line(row.get("story_identity", "n/a"), "story identity")
    scientific_items = [item["scientific"] for item in evidence if item.get("scientific")]
    if scientific_items:
        lineages = {item["lineage"] for item in scientific_items}
        designs = {f"{item['design']} / {item['class']}" for item in scientific_items}
        if len({value.casefold() for value in lineages}) != 1 \
                or len({value.casefold() for value in designs}) != 1:
            raise ResearchBlocked(
                "one source packet claims multiple scientific lineages or designs")
        lineage, design = next(iter(lineages)), next(iter(designs))
        declared_lineage = _single_line(row.get("study_lineage"), "study lineage")
        declared_design = _single_line(row.get("study_design_class"), "study design/class")
        if declared_lineage.casefold() != lineage.casefold() \
                or declared_design.casefold() != design.casefold():
            raise ResearchBlocked(
                "packet scientific lineage/design contradicts its evidence items")
    else:
        lineage = _single_line(row.get("study_lineage", "n/a"), "study lineage")
        design = _single_line(row.get("study_design_class", "n/a"), "study design/class")
        if lineage.casefold() not in {"n/a", "not applicable"} \
                or design.casefold() not in {"n/a", "not applicable"}:
            raise ResearchBlocked(
                "non-scientific packet declares a scientific lineage or design")
    annotated_title = citation.get("title")
    model_title = _single_line(row["title"], "source title")
    title = (_single_line(annotated_title, "fetched source title")
             if isinstance(annotated_title, str) and annotated_title.strip() else model_title)
    source_type = _single_line(row["source_type"], "source type").casefold()
    bases = row["rights_basis"]
    if isinstance(bases, dict):
        bases = {key: _single_line(bases.get(key), f"{key} rights basis")
                 for key in required}
    if not title or RC.PLACEHOLDER.search(title) or source_type not in {
            "community", "study", "report", "transcript", "investigative"} \
            or re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", received_utc) is None \
            or not isinstance(bases, dict) or any(key not in bases for key in required) \
            or any(bases[key].casefold() in RC.RIGHTS_UNKNOWN
                   for key in required if not (key == "attribution" and
                                               bases[key].casefold() == "n/a")) \
            or rights["personal_data_retention"] == "MINIMAL_REQUIRED_ATTRIBUTION" \
            and bases["attribution"].casefold() == "n/a":
        raise ResearchBlocked("accepted source contains unresolved identity or rights provenance")
    return {
        "url": url, "title": title,
        "source_type": source_type,
        "source_family": family, "discovery_lane": lane_id, "author_organization": author,
        "story_identity": story, "study_lineage": lineage, "study_design_class": design,
        "retrieved_utc": received_utc,
        "personal_data_retention": rights["personal_data_retention"],
        "rights_basis": bases,
        "fetch": {"locator": locator,
                  "capture_method": "OpenRouter Responses web_fetch output item",
                  "excerpt": excerpt, "content_sha256": PS.sha(citation["content"].encode("utf-8"))},
        "evidence": evidence, "corroboration_count": 1,
    }, None


def _sanitize_discovery(body, response, lane, safety_boundary, coverage_plan,
                        received_utc, retained_limit, excerpt_limit):
    annotations = {}
    for item in response.get("fetches", ()):
        try:
            url = _canonical_url(item.get("url"))
        except ResearchBlocked:
            continue
        content = item.get("content")
        if isinstance(content, str) and content:
            annotations[url] = {"content": content, "title": item.get("title")}
    accepted, rejected = [], list(body.get("rejections", ()))
    personas = coverage_plan.get("personas") if isinstance(coverage_plan, dict) else None
    if not isinstance(personas, list):
        raise ResearchBlocked("discovery lost the lead persona coverage plan")
    persona_plan = {row["id"]: row for row in personas}
    returned = sum(len(row.get("evidence", ())) for row in body.get("accepted", ())
                   if isinstance(row, dict))
    if returned > retained_limit:
        raise ResearchBlocked("provider returned more evidence than its retained-result reservation")
    for row in body.get("accepted", ()):
        clean, disposition = _sanitize_candidate(
            row, annotations, lane, safety_boundary, persona_plan, received_utc,
            excerpt_limit)
        if clean is not None:
            accepted.append(clean)
        else:
            rejected.append({"source_family": disposition[0], "reason": disposition[1], "count": 1})
    return {"kind": "discovery", "accepted": accepted,
            "rejections": _aggregate_rejections(rejected)}


def _reservation(state, policy, price, tools=True, cost=True):
    tool_context = ((policy["fetch_uses_per_call"] + policy["search_results_per_call"])
                    * policy["fetch_content_tokens_per_call"] if tools else 0)
    return {"calls": 1, "input_tokens": policy["input_tokens_per_call"] + tool_context,
            "output_tokens": policy["output_tokens_per_call"],
            "cost_usd": price["max_cost_per_call"] if cost else 0,
            "search_requests": policy["search_requests_per_call"] if tools else 0,
            "fetch_uses": policy["fetch_uses_per_call"] if tools else 0,
            "retained_results": policy["retained_results_per_call"] if tools else 0}


def _reserve_group(root, state, requests, policy, price):
    group_body = [{"call_id": call_id, "request_sha256": _sha(request), "tools": tools}
                  for call_id, request, tools in requests]
    group_id = _sha(group_body)
    groups = state.setdefault("reservation_groups", {})
    prior_group = groups.get(group_id)
    if prior_group is not None and prior_group.get("members") != group_body:
        raise ResearchBlocked("durable reservation group identity is stale")
    prepared = []
    for call_id, request, tools in requests:
        marker_path, result_path = _call_paths(root, call_id)
        if os.path.lexists(result_path) and not os.path.lexists(marker_path):
            raise ResearchBlocked(f"{call_id}: result has no durable marker")
        if os.path.lexists(marker_path):
            marker = _read_json(marker_path, root, f"{call_id} marker")
            if marker.get("request_sha256") != _sha(request):
                raise ResearchBlocked(f"{call_id}: resume request differs from its marker")
            if not os.path.lexists(result_path):
                raise ResearchBlocked(f"{call_id}: ambiguous orphan call marker; replay forbidden")
            prepared.append((call_id, request, tools, marker, result_path, True))
            continue
        reserve = _reservation(state, policy, price, tools)
        stored = state.get("reservations", {}).get(call_id)
        if stored is not None and stored != reserve:
            raise ResearchBlocked(f"{call_id}: durable reservation differs from policy")
        reserve = stored or reserve
        prepared.append((call_id, request, tools, {"schema": 1, "call_id": call_id,
            "request_sha256": _sha(request), "reservation": reserve}, result_path, False))
    additions = [item[3]["reservation"] for item in prepared
                 if not item[5] and item[0] not in state.get("reservations", {})]
    budget = dict(state["budget"])
    for field in ("calls", "output_tokens", "cost_usd", "search_requests", "fetch_uses",
                  "retained_results"):
        budget[field] += sum(row[field] for row in additions)
    limits = {"calls": policy["call_ceiling"], "output_tokens": policy["total_output_tokens"],
              "cost_usd": policy["cost_ceiling_usd"],
              "search_requests": policy["search_requests_total"],
              "fetch_uses": policy["fetch_uses_total"],
              "retained_results": policy["retained_result_ceiling"]}
    over = [name for name, limit in limits.items() if budget[name] > limit]
    if over:
        raise ResearchBlocked("research ceiling exhausted before reservation: " + ", ".join(over))
    if additions:
        if prior_group is not None:
            raise ResearchBlocked("durable reservation group lost its reserved budget")
        state["budget"] = budget
        state["reservations"].update({item[0]: item[3]["reservation"]
                                      for item in prepared if not item[5]})
        groups[group_id] = {"members": group_body, "markers_complete": False}
        _write_json(_state_path(root), state, root)
    elif prior_group is None:
        groups[group_id] = {"members": group_body, "markers_complete": False}
        _write_json(_state_path(root), state, root)
    if prior_group is not None and not prior_group.get("markers_complete"):
        if any(os.path.lexists(_call_paths(root, call_id)[0]) for call_id, _request, _tools in requests):
            raise ResearchBlocked("reservation marker publication was interrupted ambiguously")
        for call_id, _request, _tools, marker, _result, _exists in prepared:
            expected = state["reservations"].get(call_id)
            if expected != marker["reservation"]:
                raise ResearchBlocked("durable reservation budget is stale")
    if not groups[group_id].get("markers_complete"):
        for call_id, _request, _tools, marker, _result, exists in prepared:
            if not exists:
                _publish_marker(_call_paths(root, call_id)[0], marker, root)
        groups[group_id]["markers_complete"] = True
        _write_json(_state_path(root), state, root)
    return prepared


def _validate_provider_result(call_id, marker, result, request=None,
                              expected_kind=None):
    """Revalidate one sanitized durable provider result on every read."""
    fields = {"schema", "call_id", "request_sha256", "model", "usage",
              "result", "result_sha256"}
    if not isinstance(result, dict) or set(result) != fields \
            or result.get("schema") != 1 or result.get("call_id") != call_id \
            or result.get("request_sha256") != marker.get("request_sha256") \
            or result.get("result_sha256") != _sha(result.get("result")):
        raise ResearchBlocked(f"{call_id}: durable result envelope is stale")
    reservation = marker.get("reservation")
    if not isinstance(reservation, dict):
        raise ResearchBlocked(f"{call_id}: durable result lacks its reservation")
    normalized_usage = _usage(
        {"model": result.get("model"), "usage": result.get("usage")}, reservation,
        bool(reservation.get("search_requests") or reservation.get("fetch_uses")))
    if result["usage"] != normalized_usage:
        raise ResearchBlocked(f"{call_id}: durable result usage is not canonical")
    clean = result["result"]
    kind = request.get("kind") if isinstance(request, dict) else expected_kind
    if kind == "gap-fill":
        kind = "discovery"
    if not isinstance(clean, dict) or clean.get("kind") != kind:
        raise ResearchBlocked(f"{call_id}: durable result kind is stale")
    if kind == "plan":
        if set(clean) != {"kind", "preset", "coverage_plan", "commissions"} \
                or clean.get("preset") not in {"FULL-LENGTH", "POCKET"} \
                or not isinstance(clean.get("commissions"), dict) \
                or set(clean["commissions"]) != set(LANES) \
                or any(_single_line(value, "durable commission") != value
                       for value in clean["commissions"].values()):
            raise ResearchBlocked(f"{call_id}: durable lead plan is malformed")
        coverage = clean.get("coverage_plan")
        if not isinstance(coverage, dict) or set(coverage) != {
                "beliefs", "questions", "personas"}:
            raise ResearchBlocked(f"{call_id}: durable coverage plan is malformed")
        beliefs = _safe_list(coverage["beliefs"], "durable planned beliefs")
        questions = _safe_list(coverage["questions"], "durable research questions")
        if beliefs != coverage["beliefs"] or questions != coverage["questions"]:
            raise ResearchBlocked(f"{call_id}: durable coverage plan is not canonical")
        personas, ids, contexts = coverage.get("personas"), set(), set()
        if not isinstance(personas, list) or len(personas) < 3:
            raise ResearchBlocked(f"{call_id}: durable persona plan is incomplete")
        for row in personas:
            if not isinstance(row, dict) or set(row) != {
                    "id", "context", "applicable_beliefs", "applicable_banks"}:
                raise ResearchBlocked(f"{call_id}: durable persona plan is malformed")
            persona, context = row["id"], row["context"]
            if re.fullmatch(r"P-\d{2,3}", str(persona)) is None or persona in ids \
                    or _single_line(context, "durable persona context") != context \
                    or context.casefold() in contexts \
                    or not isinstance(row["applicable_beliefs"], list) \
                    or not set(row["applicable_beliefs"]).issubset(beliefs) \
                    or not isinstance(row["applicable_banks"], list) \
                    or not row["applicable_banks"] \
                    or any(type(bank) is not int or not 1 <= bank <= 10
                           for bank in row["applicable_banks"]):
                raise ResearchBlocked(f"{call_id}: durable persona plan is invalid")
            ids.add(persona); contexts.add(context.casefold())
        if isinstance(request, dict):
            try:
                brief_beliefs = set(SC.belief_set(request["brief"]))
            except (KeyError, SC.ContractError) as exc:
                raise ResearchBlocked(f"{call_id}: durable plan lost its brief") from exc
            if set(beliefs) != brief_beliefs:
                raise ResearchBlocked(f"{call_id}: durable plan differs from brief beliefs")
    elif kind == "synthesis":
        if set(clean) != {"kind", "selected_evidence_keys", "notes"} \
                or clean.get("notes") != [] \
                or not isinstance(clean.get("selected_evidence_keys"), list) \
                or len(clean["selected_evidence_keys"]) != len(set(
                    clean["selected_evidence_keys"])) \
                or any(_single_line(value, "durable synthesis locator") != value
                       for value in clean["selected_evidence_keys"]):
            raise ResearchBlocked(f"{call_id}: durable synthesis is malformed")
        if isinstance(request, dict) and set(clean["selected_evidence_keys"]) \
                - set(request.get("evidence_keys", ())):
            raise ResearchBlocked(f"{call_id}: durable synthesis invented evidence")
    elif kind == "discovery":
        if set(clean) != {"kind", "accepted", "rejections"} \
                or not isinstance(clean.get("accepted"), list) \
                or len(clean["accepted"]) > reservation.get("retained_results", -1) \
                or clean.get("rejections") != _aggregate_rejections(
                    clean.get("rejections", [])):
            raise ResearchBlocked(f"{call_id}: durable discovery is malformed")
        source_fields = {"url", "title", "source_type", "source_family",
            "discovery_lane", "author_organization", "story_identity",
            "study_lineage", "study_design_class", "retrieved_utc",
            "personal_data_retention", "rights_basis", "fetch", "evidence",
            "corroboration_count"}
        evidence_fields = {"kind", "text", "persona_tags", "bank_slots",
            "evidence_grade", "style_slots", "safety_boundary",
            "permitted_inference", "prohibited_inference", "situation", "emotion",
            "beliefs", "semantic_key", "claim_key", "story_key", "grade_rationale",
            "scope", "counterevidence", "testimonial_qualification", "scientific"}
        coverage = request.get("coverage_plan", {}) if isinstance(request, dict) else {}
        persona_plan = {row["id"]: row for row in coverage.get("personas", ())
                        if isinstance(row, dict) and "id" in row}
        for source in clean["accepted"]:
            if not isinstance(source, dict) or set(source) != source_fields \
                    or _canonical_url(source.get("url")) != source.get("url") \
                    or source.get("discovery_lane") not in RC.LANES \
                    or source.get("personal_data_retention") not in {
                        "NONE", "MINIMAL_REQUIRED_ATTRIBUTION"} \
                    or source.get("corroboration_count") != 1 \
                    or re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",
                                    str(source.get("retrieved_utc"))) is None \
                    or not isinstance(source.get("rights_basis"), dict) \
                    or set(source["rights_basis"]) != {
                        "access", "excerpt", "redistribution", "attribution",
                        "retention", "privacy"}:
                raise ResearchBlocked(f"{call_id}: durable accepted source is malformed")
            fetch = source.get("fetch")
            if not isinstance(fetch, dict) or set(fetch) != {
                    "locator", "capture_method", "excerpt", "content_sha256"} \
                    or fetch.get("capture_method") != \
                        "OpenRouter Responses web_fetch output item" \
                    or HEX.fullmatch(str(fetch.get("content_sha256", ""))) is None \
                    or not str(fetch.get("excerpt", "")):
                raise ResearchBlocked(f"{call_id}: durable fetch proof is malformed")
            items = source.get("evidence")
            if not isinstance(items, list) or not items:
                raise ResearchBlocked(f"{call_id}: durable source has no evidence")
            for evidence in items:
                if not isinstance(evidence, dict) or set(evidence) != evidence_fields \
                        or evidence.get("kind") not in {"EXACT_QUOTE", "INTERPRETATION"} \
                        or evidence.get("evidence_grade") not in {
                            "SUPPORTED", "MIXED", "CONTESTED", "n/a"} \
                        or not isinstance(evidence.get("bank_slots"), list) \
                        or any(type(bank) is not int or not 1 <= bank <= 10
                               for bank in evidence["bank_slots"]) \
                        or not isinstance(evidence.get("style_slots"), list) \
                        or any(slot not in RC.SLOTS for slot in evidence["style_slots"]) \
                        or not all(str(evidence.get(key, "")).strip() for key in (
                            "text", "safety_boundary", "permitted_inference",
                            "prohibited_inference", "semantic_key", "claim_key",
                            "story_key", "grade_rationale", "scope", "counterevidence")) \
                        or evidence["kind"] == "EXACT_QUOTE" \
                        and evidence["text"] not in fetch["excerpt"]:
                    raise ResearchBlocked(f"{call_id}: durable evidence is malformed")
                if persona_plan and (not set(evidence.get("persona_tags", ()))
                                     <= set(persona_plan)):
                    raise ResearchBlocked(f"{call_id}: durable personas exceed the plan")
                scientific = evidence.get("scientific")
                if scientific is not None and (not isinstance(scientific, dict)
                        or set(scientific) != {"design", "class", "lineage",
                            "grade_rationale", "scope", "counterevidence"}
                        or any(not str(value).strip() for value in scientific.values())):
                    raise ResearchBlocked(
                        f"{call_id}: durable scientific lineage is malformed")
    else:
        raise ResearchBlocked(f"{call_id}: durable provider kind is unsupported")
    return result


def _provider_call(root, item, prompt, transport, policy):
    call_id, request, tools, marker, result_path, exists = item
    if exists:
        result = _read_json(result_path, root, f"{call_id} result")
        return _validate_provider_result(call_id, marker, result, request)
    payload = _payload(prompt, request, policy, tools)
    response = transport.call(payload)
    received_utc = _utc_now()
    usage = _usage(response, marker["reservation"], tools)
    if request["kind"] == "plan":
        body = _json_content(response, "plan")
        commissions = body.get("commissions")
        if not isinstance(commissions, dict) or set(commissions) != set(LANES) \
                or any(not isinstance(value, str) for value in commissions.values()):
            raise ResearchBlocked("lead plan does not commission every exact discovery lane")
        commissions = {lane: _single_line(commissions[lane], f"{lane} commission")
                       for lane in LANES}
        coverage_plan = body.get("coverage_plan")
        if not isinstance(coverage_plan, dict) or set(coverage_plan) != {
                "beliefs", "questions", "personas"}:
            raise ResearchBlocked("lead coverage plan is malformed")
        personas = coverage_plan.get("personas")
        try:
            brief_beliefs = set(SC.belief_set(request["brief"]))
        except SC.ContractError as exc:
            raise ResearchBlocked("lead plan lost its completed belief contract") from exc
        planned_beliefs = _safe_list(coverage_plan.get("beliefs"), "planned beliefs")
        questions = _safe_list(coverage_plan.get("questions"), "research questions")
        if set(planned_beliefs) != brief_beliefs:
            raise ResearchBlocked("lead coverage plan does not cover the exact brief beliefs")
        normalized, seen_ids, contexts = [], set(), set()
        for row in personas or ():
            if not isinstance(row, dict) or set(row) != {
                    "id", "context", "applicable_beliefs", "applicable_banks"}:
                raise ResearchBlocked("lead persona coverage plan is malformed")
            persona = _single_line(row["id"], "persona id")
            context = _single_line(row["context"], "persona context")
            beliefs = [_single_line(value, "persona belief").strip('"“”')
                       for value in row["applicable_beliefs"]]
            banks = row["applicable_banks"]
            if re.fullmatch(r"P-\d{2,3}", persona) is None or persona in seen_ids \
                    or not context or context.casefold() in contexts \
                    or not beliefs or not set(beliefs).issubset(brief_beliefs) \
                    or not isinstance(banks, list) or not banks \
                    or any(type(bank) is not int or not 1 <= bank <= 10 for bank in banks):
                raise ResearchBlocked("lead personas are not distinct, relevant, and brief-bound")
            seen_ids.add(persona); contexts.add(context.casefold())
            normalized.append({"id": persona, "context": context,
                               "applicable_beliefs": sorted(set(beliefs)),
                               "applicable_banks": sorted(set(banks))})
        if len(normalized) < 3:
            raise ResearchBlocked("lead plan has fewer than three materially distinct personas")
        if {belief for persona in normalized for belief in persona["applicable_beliefs"]} \
                != brief_beliefs:
            raise ResearchBlocked("lead plan leaves a brief belief without a relevant persona")
        coverage_plan = {"beliefs": sorted(brief_beliefs), "questions": questions,
                         "personas": normalized}
        clean = {"kind": "plan", "preset": body.get("preset"),
                 "coverage_plan": coverage_plan, "commissions": commissions}
        if clean["preset"] not in ("FULL-LENGTH", "POCKET"):
            raise ResearchBlocked("lead coverage plan is incomplete")
    elif request["kind"] in ("discovery", "gap-fill"):
        try:
            boundary = _single_line(SC.scalar_value(
                SC._sections(request["brief"]), "Safety perimeter"),
                "brief safety perimeter")
        except (KeyError, SC.ContractError) as exc:
            raise ResearchBlocked("discovery request lost its completed safety boundary") from exc
        clean = _sanitize_discovery(_json_content(response, "discovery"), response,
                                    request.get("lane"), boundary,
                                    request.get("coverage_plan"), received_utc,
                                    marker["reservation"]["retained_results"],
                                    request["retained_excerpt_character_ceiling"])
    elif request["kind"] == "synthesis":
        body = _json_content(response, "synthesis")
        selected = body.get("selected_evidence_keys")
        if not isinstance(selected, list):
            raise ResearchBlocked("synthesis selection is invalid")
        selected = [_single_line(value, "synthesis evidence locator") for value in selected]
        if len(selected) != len(set(selected)):
            raise ResearchBlocked("synthesis selection is invalid")
        clean = {"kind": "synthesis", "selected_evidence_keys": selected,
                 "notes": []}
    else:
        raise ResearchFactoryError(f"unknown provider call kind: {request['kind']}")
    result = {"schema": 1, "call_id": call_id, "request_sha256": marker["request_sha256"],
              "model": MODEL, "usage": usage, "result": clean}
    result["result_sha256"] = _sha(clean)
    _validate_provider_result(call_id, marker, result, request)
    _write_json(result_path, result, root)
    return result


def _call_group(root, state, requests, prompt, transport, policy, price, parallel=False):
    for _call_id, request, tools in requests:
        _validate_payload_reservation(_payload(prompt, request, policy, tools), policy)
    prepared = _reserve_group(root, state, requests, policy, price)
    if not parallel:
        return [_provider_call(root, item, prompt, transport, policy) for item in prepared]
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(prepared)) as pool:
        futures = [pool.submit(_provider_call, root, item, prompt, transport, policy)
                   for item in prepared]
        return [future.result() for future in futures]


def _attempt_receipts(root):
    """Return privacy-safe, content-free evidence of completed discovery effort."""
    receipts = []
    for path in sorted(_calls_root(root).glob("*.result.json")):
        call_id = path.name.removesuffix(".result.json")
        lane = re.fullmatch(r"lane-\d+-(.+)", call_id)
        gap = re.fullmatch(r"gap-r(\d+)", call_id)
        if lane is None and gap is None:
            continue
        result = _read_json(path, root, f"{call_id} result")
        marker = _read_json(_call_paths(root, call_id)[0], root,
                            f"{call_id} marker")
        _validate_provider_result(
            call_id, marker, result, expected_kind="discovery")
        clean = result.get("result", {})
        accepted = clean.get("accepted") if isinstance(clean, dict) else None
        rejections = clean.get("rejections") if isinstance(clean, dict) else None
        usage = result.get("usage", {}).get("server_tool_use")
        if not isinstance(accepted, list) or not isinstance(rejections, list) \
                or not isinstance(usage, dict):
            raise ResearchBlocked(f"{call_id}: sanitized attempt receipt is incomplete")
        body = {
            "call_id": call_id,
            "lane": lane.group(1) if lane else None,
            "round": int(gap.group(1)) if gap else 0,
            "request_sha256": result.get("request_sha256"),
            "search_requests": usage.get("web_search_requests"),
            "fetch_uses": usage.get("web_fetch_requests"),
            "accepted_sources": len(accepted),
            "accepted_evidence": sum(len(row.get("evidence", ())) for row in accepted
                                     if isinstance(row, dict)),
            "accepted_sha256": _sha(accepted),
            "rejections": rejections,
        }
        if HEX.fullmatch(str(body["request_sha256"])) is None \
                or any(type(body[key]) is not int or body[key] < 0
                       for key in ("search_requests", "fetch_uses")):
            raise ResearchBlocked(f"{call_id}: sanitized attempt receipt is malformed")
        receipts.append({**body, "sha256": _sha(body)})
    return receipts


def _existing_source_keys(ctx):
    urls, excerpts, texts, stories, lineages, maximum = (
        {}, set(), set(), set(), set(), 0)
    prefix = ctx["book_relative"] + "/research/sources/"
    paths = [ctx["tree"] / item["path"] for item in CP._members(ctx["manifest"])
             if item["group"] == "product" and item["path"].startswith(prefix)]
    for path in sorted(paths):
        match = re.fullmatch(r"[sS]-(\d{3})-.+\.md", path.name)
        if not match:
            continue
        maximum = max(maximum, int(match.group(1)))
        text = path.read_text(encoding="utf-8")
        canonical = None
        url = re.search(r"^- \*\*URL:\*\*\s*(.+?)\s*$", text, re.M)
        if url:
            try:
                canonical = _canonical_url(url.group(1))
                fetched = re.search(
                    r"^- \*\*Fetched content SHA-256:\*\*\s*([0-9a-f]{64})\s*$",
                    text, re.M)
                urls[canonical] = {"content_sha256": (
                    fetched.group(1) if fetched else ""), "excerpt": ""}
            except ResearchBlocked:
                pass
        block = re.search(r"```text\s*\n(.*?)\n```", text, re.S)
        if block:
            normalized_excerpt = " ".join(block.group(1).casefold().split())
            excerpts.add(normalized_excerpt)
            if canonical in urls:
                urls[canonical]["excerpt"] = normalized_excerpt
        texts.update(" ".join(value.casefold().split()) for value in
                     re.findall(r"^- \*\*Text:\*\*\s*(.+?)\s*$", text, re.M))
        story = re.search(r"^- \*\*Story identity:\*\*\s*(.+?)\s*$", text, re.M)
        if story and story.group(1).casefold() not in {"n/a", "not applicable"}:
            stories.add(story.group(1).casefold())
        lineage = re.search(r"^- \*\*Study lineage:\*\*\s*(.+?)\s*$", text, re.M)
        if lineage and lineage.group(1).casefold() not in {"n/a", "not applicable"}:
            lineages.add(lineage.group(1).casefold())
    return urls, excerpts, maximum, texts, stories, lineages


def _dedupe(rows, ceiling, existing=(set(), set(), 0, set(), set(), set()),
            corroboration=None):
    corroboration = corroboration if corroboration is not None else {}
    def observed(kind):
        corroboration[kind] = corroboration.get(kind, 0) + 1
    if len(existing) == 3:  # Compatibility for import-only fixtures.
        existing_urls, existing_excerpts, maximum = existing
        existing_texts, existing_stories, existing_lineages = set(), set(), set()
    else:
        (existing_urls, existing_excerpts, maximum, existing_texts,
         existing_stories, existing_lineages) = existing
    retained, url_seen, content_seen, excerpt_seen = [], {}, {}, {}
    evidence_seen, text_seen, story_seen, lineage_seen = {}, {}, {}, {}
    for source in sorted(rows, key=lambda item: item["url"]):
        normalized_excerpt = " ".join(source["fetch"]["excerpt"].casefold().split())
        if source["url"] in existing_urls:
            authority = existing_urls[source["url"]] if isinstance(existing_urls, dict) else None
            if authority is not None and authority != {
                    "content_sha256": source["fetch"]["content_sha256"],
                    "excerpt": normalized_excerpt}:
                raise ResearchBlocked(
                    "existing canonical source has conflicting capture provenance")
            observed("existing_canonical_source")
            continue
        if normalized_excerpt in existing_excerpts:
            observed("existing_exact_excerpt")
            continue
        duplicate = next((mapping[key] for mapping, key in (
            (url_seen, source["url"]), (content_seen, source["fetch"]["content_sha256"]),
            (excerpt_seen, normalized_excerpt))
            if key in mapping), None)
        if duplicate is not None:
            owner = retained[duplicate]
            if source["url"] != owner["url"] or source["fetch"] != owner["fetch"]:
                raise ResearchBlocked(
                    "duplicate source records have conflicting capture provenance")
        source_lineage = source["study_lineage"].casefold()
        scientific_source = source_lineage not in {"", "n/a", "not applicable"}
        source_story = source.get("story_identity", "").casefold()
        if source_story in {"n/a", "not applicable"}:
            source_story = ""
        if scientific_source and source_lineage in existing_lineages:
            observed("existing_scientific_lineage")
            continue
        if source_story and source_story in existing_stories:
            observed("existing_lived_story")
            continue
        if scientific_source and source_lineage in lineage_seen \
                and duplicate != lineage_seen[source_lineage]:
            retained[lineage_seen[source_lineage]]["corroboration_count"] += 1
            continue
        if source_story and source_story in story_seen \
                and duplicate != story_seen[source_story]:
            retained[story_seen[source_story]]["corroboration_count"] += 1
            continue
        clean_evidence = []
        corroborated = {duplicate} if duplicate is not None else set()
        for item in source["evidence"]:
            meaning = item["semantic_key"] or " ".join(item["text"].casefold().split())
            normalized_text = " ".join(item["text"].casefold().split())
            item_story = " ".join(item.get("story_key", "").casefold().split())
            if item_story in {"n/a", "not applicable"}:
                item_story = ""
            scientific = any(bank in (7, 8) for bank in item["bank_slots"])
            lineage = source["study_lineage"].casefold() if scientific else ""
            evidence_key = (meaning, lineage) if scientific else (meaning, "")
            text_key = (normalized_text, lineage) if scientific else (normalized_text, "")
            if normalized_text in existing_texts:
                observed("existing_exact_evidence")
                continue
            if item_story and item_story in existing_stories:
                observed("existing_lived_story")
                continue
            duplicate_owners = {mapping[key] for mapping, key in (
                (evidence_seen, evidence_key), (text_seen, text_key),
                (story_seen, item_story))
                if key and key in mapping}
            if duplicate_owners:
                corroborated.update(duplicate_owners)
                continue
            owner = duplicate if duplicate is not None else len(retained)
            evidence_seen[evidence_key] = owner
            text_seen[text_key] = owner
            if item_story:
                story_seen[item_story] = owner
            clean_evidence.append(item)
        if duplicate is not None:
            retained[duplicate]["evidence"].extend(clean_evidence)
            for owner in corroborated:
                retained[owner]["corroboration_count"] += 1
            continue
        if not clean_evidence:
            for owner in corroborated:
                retained[owner]["corroboration_count"] += 1
            continue
        source["evidence"] = clean_evidence
        index = len(retained)
        for mapping, key in ((url_seen, source["url"]),
                             (content_seen, source["fetch"]["content_sha256"]),
                             (excerpt_seen, normalized_excerpt)):
            mapping[key] = index
        retained.append(source)
        if scientific_source:
            lineage_seen[source_lineage] = index
        if source_story:
            story_seen[source_story] = index
        for owner in corroborated:
            retained[owner]["corroboration_count"] += 1
    count = sum(len(source["evidence"]) for source in retained)
    if count > ceiling:
        raise ResearchBlocked("retained-result ceiling exhausted; corpus remains unaccepted")
    for source_number, source in enumerate(retained, maximum + 1):
        source["source_id"] = f"S-{source_number:03d}"
        for evidence_number, item in enumerate(source["evidence"], 1):
            item["evidence_id"] = f"E-{evidence_number:03d}"
            item["locator"] = f"{source['source_id']}#{item['evidence_id']}"
    return retained


def _packet(source):
    title = source["title"].replace("\n", " ")
    basis = source["rights_basis"]
    privacy_detail = ("no personal data retained"
                      if source["personal_data_retention"] == "NONE"
                      else "only required attribution retained")
    lines = [f"# {source['source_id']} — {title}", "",
        f"- **Source ID:** {source['source_id']}", f"- **URL:** {source['url']}",
        f"- **Title:** {title}", f"- **Source type:** {source['source_type']}",
        f"- **Retrieved (UTC):** {source['retrieved_utc']}",
        f"- **Discovery lane:** {source['discovery_lane']}",
        f"- **Source family:** {source['source_family']}",
        f"- **Author / organization:** {source['author_organization']}",
        f"- **Fetched URL:** {source['url']}",
        f"- **Fetched content SHA-256:** {source['fetch']['content_sha256']}",
        f"- **Corroboration count:** {source['corroboration_count']}",
        f"- **Story identity:** {source['story_identity']}",
        f"- **Study lineage:** {source['study_lineage']}",
        f"- **Study design / class:** {source['study_design_class']}",
        "- **Deletion sensitivity:** NOT_DELETION_SENSITIVE",
        f"- **Personal-data retention:** {source['personal_data_retention']}",
        f"- **Access / license basis:** {basis['access']}",
        f"- **Excerpt / redistribution basis:** {basis['excerpt']}; {basis['redistribution']}",
        f"- **Required attribution:** {basis['attribution']}",
        f"- **Retention / deletion sensitivity:** {basis['retention']}; not deletion-sensitive",
        f"- **Privacy / personal-data basis:** {basis['privacy']}; {privacy_detail}",
        "- **Disposition:** ACCEPTED", "", "## Minimum retained excerpt", "", "### C-001", "",
        f"- **Locator:** {source['fetch']['locator']}",
        f"- **Capture method:** {source['fetch']['capture_method']}",
        f"- **Content SHA-256:** {PS.sha(source['fetch']['excerpt'].encode('utf-8'))}", "", "```text",
        source["fetch"]["excerpt"], "```", "", "## Evidence items", ""]
    for item in source["evidence"]:
        scientific = item.get("scientific") or {}
        limits = (f"{item['situation']} {item['emotion']} "
                  f"{item['permitted_inference']} {item['prohibited_inference']}").strip()
        lines.extend([f"### {item['evidence_id']}", "", f"- **Kind:** {item['kind']}",
            f"- **Text:** {item['text']}", "- **Excerpt ID:** C-001",
            f"- **Locator:** {source['fetch']['locator']}",
            f"- **Persona tags:** {'; '.join(item['persona_tags'])}",
            f"- **Bank slots:** {'; '.join(f'Bank {bank}' for bank in item['bank_slots'])}",
            f"- **Brief beliefs:** {'; '.join(item['beliefs'])}",
            f"- **Style slots:** {'; '.join(item['style_slots'])}",
            f"- **Safety relevance:** {item['safety_boundary']}",
            f"- **Situation:** {item['situation']}", f"- **Emotion:** {item['emotion']}",
            f"- **Evidence grade:** {item['evidence_grade']}", f"- **Use / limits:** {limits}"])
        lines.extend([f"- **Grade rationale:** {item['grade_rationale']}",
            f"- **Scope:** {item['scope']}", f"- **Counterevidence:** {item['counterevidence']}",
            f"- **Permitted inference:** {item['permitted_inference']}",
            f"- **Prohibited inference:** {item['prohibited_inference']}",
            f"- **Testimonial qualification:** {item['testimonial_qualification']}"])
        if scientific:
            lines.extend([f"- **Scientific design:** {scientific['design']}",
                f"- **Scientific class:** {scientific['class']}",
                f"- **Scientific lineage:** {scientific['lineage']}"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_syntheses(retained, beliefs, coverage_plan, selected=None, unit_offsets=None):
    allowed = set(selected) if selected is not None else None
    lived, science_groups, lived_units, science_units = [], {}, [], {}
    personas = {}
    for source in retained:
        for item in source["evidence"]:
            key = item["locator"]
            if allowed is not None and key not in allowed:
                continue
            for persona in item["persona_tags"]:
                personas.setdefault(persona, set()).add(source["source_id"])
            for bank in item["bank_slots"]:
                if bank in (7, 8):
                    science_groups.setdefault((bank, item["claim_key"]), []).append((source, item))
                else:
                    lived.append((bank, f"- [Bank {bank}] {item['text']} — Persona IDs: {'; '.join(item['persona_tags'])} — Source IDs: {item['locator']}"))
            if item["kind"] == "EXACT_QUOTE" and item["situation"] and item["emotion"]:
                for belief in item["beliefs"]:
                    if belief in beliefs:
                        if any(bank in (7, 8) for bank in item["bank_slots"]):
                            science_units.setdefault((belief, item["claim_key"]), []).append((source, item))
                        else:
                            lived_units.append((belief, [(source, item)]))
    science = []
    for (bank, _claim), records in sorted(science_groups.items()):
        grades = {item["evidence_grade"] for _source, item in records}
        grade = "CONTESTED" if "CONTESTED" in grades else "MIXED" if "MIXED" in grades else "SUPPORTED"
        personas_for_claim = sorted({persona for _source, item in records for persona in item["persona_tags"]})
        locators = sorted({item["locator"] for _source, item in records})
        first = records[0][1]
        science.append((bank, f"- [Bank {bank}] [{grade}] {first['text']} — Persona IDs: {'; '.join(personas_for_claim)} — Source IDs: {', '.join(locators)} — Limits / disagreement: {first['prohibited_inference']}"))
    persona_lines = ["## Persona map", "", "| Persona ID | Function served / defining context | Applicable beliefs | Applicable banks | Source IDs |",
                     "|---|---|---|---|---|"]
    for record in coverage_plan["personas"]:
        persona, sources = record["id"], personas.get(record["id"], set())
        persona_lines.append(f"| {persona} | {record['context']} | {'; '.join(record['applicable_beliefs'])} | {'; '.join(str(bank) for bank in record['applicable_banks'])} | {', '.join(sorted(sources))} |")
    unit_sections = {"LEU": [], "SEU": []}
    counters = {"LEU": 0, "SEU": 0, **(unit_offsets or {})}
    units = [("LEU", belief, records) for belief, records in lived_units]
    units.extend(("SEU", belief, records) for (belief, _claim), records in sorted(science_units.items()))
    for kind, belief, records in units:
        first = records[0][1]
        locators = sorted({item["locator"] for _source, item in records})
        unit_personas = sorted({persona for _source, item in records for persona in item["persona_tags"]})
        common_slots = set(first["style_slots"])
        for _source, item in records[1:]:
            common_slots.intersection_update(item["style_slots"])
        if not common_slots:
            continue
        grades = {item["evidence_grade"] for _source, item in records}
        grade = "CONTESTED" if "CONTESTED" in grades else "MIXED" if "MIXED" in grades else first["evidence_grade"]
        counters[kind] += 1
        unit_id = f"{kind}-{counters[kind]:03d}"
        unit_sections[kind].extend([f"### {unit_id}", "",
            f"- **Situation:** {first['situation']}", f"- **Reader wording:** \"{first['text']}\"",
            f"- **Implicated belief:** \"{belief}\"", f"- **Emotion:** {first['emotion']}",
            f"- **Permitted inference:** {first['permitted_inference']}",
            f"- **Prohibited inference:** {first['prohibited_inference']}",
            f"- **Source locator:** {', '.join(locators)}",
            f"- **Evidence grade:** {grade}", ""])
        unit_sections[kind][-1:-1] = [
            f"- **Persona IDs:** {'; '.join(unit_personas)}",
            f"- **Style slots:** {'; '.join(sorted(common_slots))}",
            f"- **Safety boundary:** {first['safety_boundary']}",
        ]
    def document(title, findings, kind, banks):
        lines = [f"# {title}", "", *persona_lines, "", "## Intervention-ready evidence units", "",
                 *unit_sections[kind]]
        for bank in banks:
            lines.extend([f"## Bank {bank}", ""])
            lines.extend(text for number, text in findings if number == bank)
            lines.append("")
        lines.extend(["## Slot-tag index", ""])
        lines.extend(f"- Bank {bank} -> all accepted Bank {bank} bullets above" for bank in banks)
        return "\n".join(lines).rstrip() + "\n"
    return (document("Lived Experience", lived, "LEU", (1, 2, 3, 4, 5, 6, 9, 10)),
            document("Scientific Evidence", science, "SEU", (7, 8)))


def _source_name(source):
    slug = SAFE_SLUG.sub("-", source["title"].casefold()).strip("-")[:60] or "source"
    return f"{source['source_id']}-{slug}.md"


def _log(plan, state, retained, attempts):
    lines = ["# Research log", "", f"FORMAT PRESET: {plan['preset']}", "",
             "## Parameter and coverage plan", "", "```json",
             json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False), "```", "",
             "## Sanitized call receipts", "", "| Call | Result hash |", "|---|---|"]
    for call_id, digest in sorted(state.get("results", {}).items()):
        lines.append(f"| {call_id} | `{digest}` |")
    lines.extend(["", "## Sanitized discovery attempt receipts", "",
                  "| Call | Lane / round | Search | Fetch | Accepted sources / evidence | Accepted hash | Aggregate rejections |",
                  "|---|---|---:|---:|---:|---|---|"])
    for row in attempts:
        phase = row["lane"] or f"gap round {row['round']}"
        rejected = json.dumps(row["rejections"], sort_keys=True, ensure_ascii=False)
        lines.append(f"| {row['call_id']} | {phase} | {row['search_requests']} | {row['fetch_uses']} | "
                     f"{row['accepted_sources']} / {row['accepted_evidence']} | `{row['accepted_sha256']}` | {rejected} |")
    lines.extend(["", "## Aggregate rejected/unresolved yield", "",
                  "Only policy-level source-family aggregates are retained.", ""])
    for row in state.get("rejections", ()):
        lines.append(f"- {row['source_family']}: {row['reason']} — {row['count']}")
    lines.extend(["", "## Cross-seal eligible corroboration", "",
                  "Content-free duplicate observations; these do not add packets, evidence, or coverage.", ""])
    corroboration = state.get("corroboration", {})
    if corroboration:
        lines.extend(f"- {kind}: {count}"
                     for kind, count in sorted(corroboration.items()))
    else:
        lines.append("- None")
    lines.extend(["", "## Retained corpus", "",
                  f"- Eligible packets: {len(retained)}",
                  f"- Eligible evidence items: {sum(len(row['evidence']) for row in retained)}",
                  "- Acceptance is determined by the derived coverage report and independent review, never this count."])
    return "\n".join(lines).rstrip() + "\n"


def _render_stage(ctx, plan, state, retained, selected=None):
    root, stage = ctx["root"], _stage_book(ctx)
    try:
        if os.path.lexists(stage):
            PS.discard_stage(stage, _factory_root(root))
        operation = stage.parents[1]
        for relative, source in (
                ("prompts/research-agent.md", ctx["prompt_path"]),
                ("prompts/research-evidence-editor.md", ctx["editor_prompt_path"]),
                (ctx["manifest"]["run"]["config"], ctx["config_path"])):
            target = operation / relative
            _ensure_dir(target.parent, _factory_root(root))
            PS.write(target, source.read_bytes())
        _ensure_dir(stage / "research/sources", _factory_root(root))
        PS.write(stage / "00-brief.md", ctx["brief_path"].read_bytes())
        prefix = ctx["book_relative"] + "/research/sources/"
        existing_sources = [ctx["tree"] / item["path"] for item in CP._members(ctx["manifest"])
                            if item["group"] == "product" and item["path"].startswith(prefix)]
        for path in sorted(existing_sources):
            PS.write(stage / "research/sources" / path.name, path.read_bytes())
        for source in retained:
            PS.write(stage / "research/sources" / _source_name(source),
                     _packet(source).encode("utf-8"))
        lived, science = _render_syntheses(
            retained, SC.belief_set(ctx["brief_path"].read_text(encoding="utf-8")),
            plan["coverage_plan"], selected)
        PS.write(stage / "research/lived-experience.md", lived.encode("utf-8"))
        PS.write(stage / "research/scientific-evidence.md", science.encode("utf-8"))
        PS.write(stage / "research/research-log.md",
                 _log(plan, state, retained, _attempt_receipts(root)).encode("utf-8"))
    except (PS.StoreError, OSError, UnicodeError) as exc:
        raise ResearchFactoryError(f"cannot render private research candidate: {exc}") from exc
    return stage


def _sealed_plan(book):
    path = Path(book) / "research/research-log.md"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ResearchBlocked("sealed research has no reusable coverage plan") from exc
    match = re.search(
        r"^## Parameter and coverage plan\s*$[\s\S]*?^```json\s*$\n([\s\S]*?)^```\s*$",
        text, re.MULTILINE)
    try:
        plan = json.loads(match.group(1)) if match else None
    except json.JSONDecodeError as exc:
        raise ResearchBlocked("sealed research coverage plan is malformed") from exc
    if not isinstance(plan, dict) or plan.get("preset") not in ("FULL-LENGTH", "POCKET") \
            or not isinstance(plan.get("coverage_plan", {}).get("personas"), list):
        raise ResearchBlocked("sealed research has no reusable coverage plan")
    return plan


def _render_extension_stage(ctx, plan, state, retained, selected, prior_report):
    """Copy the sealed corpus byte-for-byte, then append only accepted new units."""
    root, stage = ctx["root"], _stage_book(ctx)
    try:
        if os.path.lexists(stage):
            PS.discard_stage(stage, _factory_root(root))
        operation = stage.parents[1]
        for relative, source in (
                ("prompts/research-agent.md", ctx["prompt_path"]),
                ("prompts/research-evidence-editor.md", ctx["editor_prompt_path"]),
                (ctx["manifest"]["run"]["config"], ctx["config_path"])):
            target = operation / relative
            _ensure_dir(target.parent, _factory_root(root))
            PS.write(target, source.read_bytes())
        _ensure_dir(stage / "research/sources", _factory_root(root))
        PS.write(stage / "00-brief.md", ctx["brief_path"].read_bytes())
        research = ctx["book"] / "research"
        excluded = {"research-coverage.json", "research-review.json", "research-seal.json"}
        for path in sorted(PS.tree_files(research)):
            relative = path.relative_to(research)
            if relative.as_posix() in excluded:
                continue
            target = stage / "research" / relative
            _ensure_dir(target.parent, _factory_root(root))
            PS.write(target, PS._safe_file(path, ctx["tree"]).read_bytes())
        for source in retained:
            PS.write(stage / "research/sources" / _source_name(source),
                     _packet(source).encode("utf-8"))
        offsets = {kind: max((int(value.split("-")[1]) for value in
                              prior_report["inventory"]["units"] if value.startswith(kind + "-")),
                             default=0)
                   for kind in ("LEU", "SEU")}
        lived, science = _render_syntheses(
            retained, SC.belief_set(ctx["brief_path"].read_text(encoding="utf-8")),
            plan["coverage_plan"], selected, offsets)
        for name, addition in (("lived-experience.md", lived),
                               ("scientific-evidence.md", science)):
            target = stage / "research" / name
            original = target.read_text(encoding="utf-8").rstrip()
            PS.write(target, (original + "\n\n" + addition).encode("utf-8"))
        log = stage / "research/research-log.md"
        original_log = log.read_text(encoding="utf-8").rstrip()
        extension = _log(plan, state, retained, _attempt_receipts(root))
        PS.write(log, (original_log + "\n\n## Targeted chapter extension\n\n" + extension).encode("utf-8"))
    except (PS.StoreError, OSError, UnicodeError) as exc:
        raise ResearchFactoryError(f"cannot render targeted research extension: {exc}") from exc
    return stage


def _inspect(book):
    try:
        return RC.inspect_research(book, require_seal=False)
    except (RC.ContractError, SC.ContractError, OSError) as exc:
        raise ResearchBlocked(f"shared research inspection failed: {exc}") from exc


def _gap_request(ctx, plan, report, retained, round_number, retained_limit,
                 excerpt_limit):
    inventory = [{"source_id": source["source_id"], "url": source["url"],
        "lane": source["discovery_lane"], "source_family": source["source_family"],
        "evidence": [{key: item[key] for key in (
            "semantic_key", "claim_key", "beliefs", "persona_tags", "bank_slots",
            "style_slots", "evidence_grade", "permitted_inference", "prohibited_inference")}
            for item in source["evidence"]]} for source in retained]
    return {"kind": "gap-fill", "fresh_context": True, "round": round_number,
        "brief": ctx["brief_path"].read_text(encoding="utf-8"), "plan_sha256": _sha(plan),
        "coverage_plan": plan["coverage_plan"],
        "candidate_sha256": report.get("candidate_sha256") or report.get("corpus_sha256"),
        "demonstrated_gaps": report.get("gaps") or report.get("blockers"),
        "retained_packet_sha256": {source["source_id"]: _sha(_packet(source)) for source in retained},
        "retained_inventory": inventory, "retained_result_ceiling": retained_limit,
        "retained_excerpt_character_ceiling": excerpt_limit,
        "response_contract": _response_contract("gap-fill"),
        "instruction": "Research only these demonstrated gaps; return discovery JSON. Do not rerun unaffected lanes."}


def _scarcity_coverage(root, stage, report, coverage, preset):
    """Request only numeric waivers after every bounded discovery round ran."""
    non_floor = [item for item in report.get("blockers", ())
                 if not (item.startswith("coverage: ") and " floor " in item)]
    floor_gaps = [item for item in coverage.get("gaps", ()) if item.get("kind") == "floor"]
    if non_floor or not floor_gaps or len(floor_gaps) != len(coverage.get("gaps", ())):
        return coverage
    receipts = _attempt_receipts(root)
    if not receipts:
        raise ResearchBlocked("numeric scarcity has no durable search-attempt evidence")
    attempts_sha = _sha(receipts)
    requests = [{"floor": gap["target"], "attempts_sha256": attempts_sha,
                 "demonstrated_ceiling": coverage["floors"][gap["target"]]["actual"]}
                for gap in floor_gaps]
    return RC.build_coverage(stage, preset, requests)


def _purge_late_eligibility_rejection(root, state):
    intent = state.get("eligibility_purge")
    if state.get("stage") != "PURGING_ELIGIBILITY":
        intent = {"reason": "rights/privacy ineligible"}
        state["stage"] = "PURGING_ELIGIBILITY"
        state["eligibility_purge"] = intent
        _write_json(_state_path(root), state, root)
    elif intent != {"reason": "rights/privacy ineligible"}:
        raise ResearchBlocked("eligibility purge intent is invalid")
    rejected = 0
    for path in sorted(_calls_root(root).glob("*.result.json")):
        result = _read_json(path, root, "provider result")
        clean = result.get("result")
        if not isinstance(clean, dict):
            continue
        if clean.get("kind") == "discovery":
            accepted = clean.get("accepted")
            if not isinstance(accepted, list):
                continue
            prior = result.get("purged_candidate_count", 0)
            if type(prior) is not int or prior < 0:
                raise ResearchBlocked("eligibility purge accounting is invalid")
            count = prior + len(accepted)
            if accepted:
                clean = {"kind": "discovery", "accepted": [],
                         "rejections": _aggregate_rejections([
                             *clean.get("rejections", ()),
                             {"source_family": "unknown",
                              "reason": "rights/privacy ineligible",
                              "count": len(accepted)},
                         ])}
            rejected += count
            scrubbed = {"schema": 1, "call_id": result.get("call_id"),
                        "model": result.get("model"), "usage": result.get("usage"),
                        "purged_candidate_count": count, "result": clean,
                        "result_sha256": _sha(clean)}
            if scrubbed != result:
                _write_json(path, scrubbed, root)
            state.setdefault("results", {})[path.name.removesuffix(".result.json")] = scrubbed[
                "result_sha256"]
        elif clean.get("kind") == "synthesis":
            clean = {"kind": "synthesis", "selected_evidence_keys": [], "notes": []}
            scrubbed = {"schema": 1, "call_id": result.get("call_id"),
                        "model": result.get("model"), "usage": result.get("usage"),
                        "result": clean, "result_sha256": _sha(clean)}
            if scrubbed != result:
                _write_json(path, scrubbed, root)
            state.setdefault("results", {})[path.name.removesuffix(".result.json")] = scrubbed[
                "result_sha256"]
    for marker in sorted(_calls_root(root).glob("*.marker.json")):
        PS._safe_file(marker, root).unlink()
    stage = _factory_root(root) / "workshop"
    if os.path.lexists(stage):
        PS.discard_stage(stage, _factory_root(root))
    state["late_eligibility_rejection"] = {
        "reason": "rights/privacy ineligible", "rejected_candidate_count": rejected}
    state.pop("eligibility_purge", None)
    state["stage"] = "BLOCKED_ELIGIBILITY"
    _write_json(_state_path(root), state, root)


def _validate_editor_result(marker, result, task, editor):
    """Revalidate exact normalized editor evidence on fresh and resume paths."""
    fields = {"schema", "call_id", "task_sha256", "verdict", "verdict_sha256",
              "editor_provenance", "editor_receipt_sha256"}
    if not isinstance(result, dict) or set(result) != fields \
            or result.get("schema") != 1 or result.get("call_id") != marker.get("call_id") \
            or marker.get("task_sha256") != _sha(task) or marker.get("task") != task \
            or result.get("task_sha256") != marker["task_sha256"]:
        raise ResearchBlocked("independent editor result envelope is stale")
    verdict = result.get("verdict")
    if not isinstance(verdict, dict) or set(verdict) != {
            "status", "gaps", "checks", "scarcity_waivers"} \
            or verdict.get("status") not in {"PASS", "BLOCKED"} \
            or not isinstance(verdict.get("gaps"), list) \
            or set(verdict.get("checks", {})) != set(HARD_REVIEW_CHECKS):
        raise ResearchBlocked("independent editor durable verdict is malformed")
    if verdict["status"] == "PASS" and (verdict["gaps"] or
            any(value != "PASS" for value in verdict["checks"].values())):
        raise ResearchBlocked("independent editor durable PASS contradicts its checks")
    if verdict["checks"].get("rights_privacy") == "BLOCKED":
        raise ResearchBlocked("independent editor durable result rejects rights/privacy")
    for gap in verdict["gaps"]:
        if not isinstance(gap, dict) or set(gap) != {"kind", "target", "message"} \
                or gap.get("kind") not in EDITOR_GAP_KINDS \
                or _single_line(gap.get("target"), "durable editor gap target") \
                    != gap.get("target") \
                or _single_line(gap.get("message"), "durable editor gap message") \
                    != gap.get("message") \
                or "http://" in (gap["target"] + gap["message"]).casefold() \
                or "https://" in (gap["target"] + gap["message"]).casefold():
            raise ResearchBlocked("independent editor durable gap is not content-safe")
    attempts = task.get("attempt_receipts")
    attempts_sha = _sha(attempts)
    requests = {row["floor"]: row for row in task.get("coverage", {}).get(
        "scarcity_requests", ())}
    if any(row.get("attempts_sha256") != attempts_sha for row in requests.values()):
        raise ResearchBlocked("independent editor durable scarcity task is stale")
    waivers = verdict.get("scarcity_waivers")
    if not isinstance(waivers, list):
        raise ResearchBlocked("independent editor durable scarcity findings are malformed")
    floors = set()
    for row in waivers:
        request = requests.get(row.get("floor")) if isinstance(row, dict) else None
        body = {key: row.get(key) for key in (
            "floor", "attempts_sha256", "demonstrated_ceiling", "finding")} \
            if isinstance(row, dict) else {}
        if not isinstance(row, dict) or set(row) != set(body) | {"finding_sha256"} \
                or request is None or body["attempts_sha256"] != request["attempts_sha256"] \
                or body["demonstrated_ceiling"] != request["demonstrated_ceiling"] \
                or not str(body["finding"]).strip() or body["finding"] != str(
                    body["finding"]).strip() or row["finding_sha256"] != _sha(body):
            raise ResearchBlocked("independent editor durable scarcity finding is stale")
        floors.add(row["floor"])
    if verdict["status"] == "PASS" and floors != set(requests):
        raise ResearchBlocked("independent editor durable PASS omits scarcity findings")
    provenance = result.get("editor_provenance")
    required = {"kind", "judge_identity", "model", "reasoning_effort",
                "fresh_ephemeral_context", "thread_id", "input_sha256",
                "output_schema_sha256", "usage"}
    expected_kind = ("native-codex-subscription"
                     if isinstance(editor, NativeEvidenceEditor)
                     else "captured-native-test-double")
    usage = provenance.get("usage") if isinstance(provenance, dict) else None
    output_tokens = usage.get("output_tokens") if isinstance(usage, dict) else None
    reserve = marker.get("reservation", {})
    if not isinstance(provenance, dict) or set(provenance) != required \
            or provenance.get("kind") != expected_kind \
            or provenance.get("judge_identity") != "research-evidence-editor" \
            or provenance.get("fresh_ephemeral_context") is not True \
            or not all(provenance.get(key) for key in (
                "model", "reasoning_effort", "thread_id")) \
            or provenance.get("input_sha256") != _sha(_editor_input(task)) \
            or provenance.get("output_schema_sha256") != _sha(_editor_schema_bytes()) \
            or type(output_tokens) is not int or output_tokens < 0 \
            or output_tokens > reserve.get("output_tokens", -1) \
            or expected_kind == "native-codex-subscription" and (
                provenance.get("model") != "gpt-5.6-sol"
                or provenance.get("reasoning_effort") != "xhigh"):
        raise ResearchBlocked("independent editor durable provenance is stale")
    receipt_body = {"task_sha256": marker["task_sha256"],
                    "verdict_sha256": _sha(verdict), "provenance": provenance}
    if result.get("verdict_sha256") != receipt_body["verdict_sha256"] \
            or result.get("editor_receipt_sha256") != _sha(receipt_body):
        raise ResearchBlocked("independent editor durable receipt is stale")
    return result


def _editor_result(root, state, task, editor, policy, price):
    attempts = task.get("attempt_receipts") if isinstance(task, dict) else None
    if not isinstance(attempts, list) or not attempts \
            or any(not isinstance(row, dict) or row.get("sha256") != _sha(
                {key: value for key, value in row.items() if key != "sha256"}) for row in attempts):
        raise ResearchBlocked("independent editor lacks current sanitized attempt evidence")
    attempts_sha = _sha(attempts)
    if any(request.get("attempts_sha256") != attempts_sha
           for request in task.get("coverage", {}).get("scarcity_requests", ())):
        raise ResearchBlocked("numeric scarcity is not bound to the editor's attempt evidence")
    editor_input = _editor_input(task)
    if len(editor_input) > policy["editor_input_bytes"]:
        raise ResearchBlocked("exact evidence-editor input exceeds its byte ceiling")
    call_id = f"editor-r{state['gap_round']}"
    marker_path, result_path = _call_paths(root, call_id)
    if os.path.lexists(marker_path):
        marker = _read_json(marker_path, root, "editor marker")
        if marker.get("task_sha256") != _sha(task) or marker.get("task") != task:
            raise ResearchBlocked("independent editor resume task differs from its marker")
        if not os.path.lexists(result_path):
            raise ResearchBlocked("independent editor has an ambiguous orphan marker")
        result = _read_json(result_path, root, "editor result")
        return _validate_editor_result(marker, result, task, editor)
    reserve = _reservation(state, policy, price, False, False)
    stored = state["reservations"].get(call_id)
    if stored is not None and stored != reserve:
        raise ResearchBlocked("independent editor durable reservation differs from policy")
    if stored is None:
        if state["budget"]["calls"] + 1 > policy["call_ceiling"] \
                or state["budget"]["output_tokens"] + reserve["output_tokens"] \
                > policy["total_output_tokens"]:
            raise ResearchBlocked("call/output ceiling exhausted before independent review")
        state["budget"]["calls"] += 1
        state["budget"]["output_tokens"] += reserve["output_tokens"]
        state["reservations"][call_id] = reserve
        _write_json(_state_path(root), state, root)
    else:
        reserve = stored
    marker = {"schema": 1, "call_id": call_id, "task_sha256": _sha(task),
              "reservation": reserve, "task": task}
    _write_json(marker_path, marker, root)
    response = editor.review(task)
    transport = response.get("transport") if isinstance(response, dict) else None
    usage = transport.get("usage") if isinstance(transport, dict) else None
    output_tokens = usage.get("output_tokens") if isinstance(usage, dict) else None
    if type(output_tokens) is not int or output_tokens < 0 \
            or output_tokens > reserve["output_tokens"]:
        raise ResearchBlocked("independent editor output usage is missing or exceeds its reservation")
    verdict = response.get("verdict") if isinstance(response, dict) else None
    if not isinstance(verdict, dict) or verdict.get("status") not in ("PASS", "BLOCKED") \
            or not isinstance(verdict.get("gaps"), list) or set(verdict.get("checks", {})) != set(HARD_REVIEW_CHECKS):
        raise ResearchBlocked("independent evidence editor verdict is malformed")
    if verdict["status"] == "PASS" and (verdict["gaps"] or
            any(value != "PASS" for value in verdict["checks"].values())):
        raise ResearchBlocked("independent editor claimed PASS with failed checks or gaps")
    if verdict["checks"].get("rights_privacy") == "BLOCKED":
        _purge_late_eligibility_rejection(root, state)
        raise ResearchBlocked("independent editor rejected rights/privacy eligibility")
    safe_gaps = []
    for gap in verdict["gaps"]:
        if not isinstance(gap, dict) or set(gap) != {"kind", "target", "message"} \
                or gap.get("kind") not in EDITOR_GAP_KINDS:
            raise ResearchBlocked("independent editor gap is not content-safe")
        target = _single_line(gap["target"], "independent editor gap target")
        message = _single_line(gap["message"], "independent editor gap message")
        if "http://" in target.casefold() or "https://" in target.casefold() \
                or "http://" in message.casefold() or "https://" in message.casefold():
            raise ResearchBlocked("independent editor gap contains source-specific material")
        safe_gaps.append({"kind": gap["kind"], "target": target, "message": message})
    verdict = {**verdict, "gaps": safe_gaps}
    requests = {row["floor"]: row for row in task["coverage"].get("scarcity_requests", [])}
    waivers = verdict.get("scarcity_waivers")
    if not isinstance(waivers, list):
        raise ResearchBlocked("independent editor scarcity findings are malformed")
    normalized_waivers = []
    for waiver in waivers:
        floor = waiver.get("floor") if isinstance(waiver, dict) else None
        request = requests.get(floor)
        if request is None or waiver.get("attempts_sha256") != request["attempts_sha256"] \
                or waiver.get("demonstrated_ceiling") != request["demonstrated_ceiling"] \
                or not str(waiver.get("finding", "")).strip():
            raise ResearchBlocked("independent scarcity finding is not bound to its request")
        row = {"floor": floor, "attempts_sha256": request["attempts_sha256"],
               "demonstrated_ceiling": request["demonstrated_ceiling"],
               "finding": str(waiver["finding"]).strip()}
        row["finding_sha256"] = _sha(row)
        normalized_waivers.append(row)
    if verdict["status"] == "PASS" and set(requests) != {row["floor"] for row in normalized_waivers}:
        raise ResearchBlocked("independent editor did not rule every numeric scarcity request")
    verdict = {**verdict, "scarcity_waivers": normalized_waivers}
    required_provenance = {
        "kind", "judge_identity", "model", "reasoning_effort",
        "fresh_ephemeral_context", "thread_id", "input_sha256",
        "output_schema_sha256", "usage",
    }
    provenance = {key: transport.get(key) for key in required_provenance}
    expected_kind = ("native-codex-subscription" if isinstance(editor, NativeEvidenceEditor)
                     else "captured-native-test-double")
    if set(provenance) != required_provenance or provenance["kind"] != expected_kind \
            or provenance["fresh_ephemeral_context"] is not True \
            or not all(provenance.get(key) for key in (
                "model", "reasoning_effort", "thread_id", "input_sha256", "output_schema_sha256")) \
            or provenance["judge_identity"] != "research-evidence-editor" \
            or provenance["input_sha256"] != _sha(editor_input) \
            or provenance["output_schema_sha256"] != _sha(_editor_schema_bytes()) \
            or expected_kind == "native-codex-subscription" and (
                provenance["model"] != "gpt-5.6-sol" or provenance["reasoning_effort"] != "xhigh"):
        raise ResearchBlocked("independent editor provenance is incomplete or uses the wrong route")
    receipt_body = {"task_sha256": marker["task_sha256"],
                    "verdict_sha256": _sha(verdict), "provenance": provenance}
    result = {"schema": 1, "call_id": call_id, "task_sha256": marker["task_sha256"],
              "verdict": verdict, "verdict_sha256": receipt_body["verdict_sha256"],
              "editor_provenance": provenance,
              "editor_receipt_sha256": _sha(receipt_body)}
    _validate_editor_result(marker, result, task, editor)
    _write_json(result_path, result, root)
    return result


def _declare_outputs(ctx, relatives):
    root, manifest = ctx["root"], CP.load(ctx["root"])
    existing = {item["path"] for item in manifest["entries"] + manifest["outputs"]}
    additions = sorted(set(relatives) - existing)
    for relative in additions:
        if os.path.lexists(ctx["tree"] / relative):
            raise ResearchFactoryError(f"undeclared research output already exists: {relative}")
    if not additions:
        return manifest
    updated = dict(manifest)
    updated["outputs"] = [*manifest["outputs"],
                          *({"group": "product", "path": path} for path in additions)]
    try:
        PS.exact_layout(root, manifest, {".pair.json.rf02-tmp": PS.json_bytes(updated)})
        PS.write_json(CP._manifest_path(root), updated)
        return CP.load(root)
    except (PS.StoreError, CP.PairError, OSError) as exc:
        raise ResearchFactoryError(f"cannot declare research outputs: {exc}") from exc


def _seal_candidate(ctx, stage, state, plan, coverage, review, authority):
    research = stage / "research"
    PS.write_json(research / "research-coverage.json", coverage)
    candidate_sha = RC.candidate_identity(stage, authority)
    if review["candidate_sha256"] != candidate_sha:
        raise ResearchFactoryError("review candidate hash changed before sealing")
    PS.write_json(research / "research-review.json", review)
    seal = RC.build_seal(stage, authority)
    PS.write_json(research / "research-seal.json", seal)
    prefix = ctx["book_relative"] + "/"
    outputs = [prefix + path.relative_to(stage).as_posix() for path in PS.tree_files(stage)
               if not os.path.lexists(ctx["tree"] / (prefix + path.relative_to(stage).as_posix()))]
    _declare_outputs(ctx, outputs)
    state.update({"stage": "PUBLISHING", "candidate_sha256": candidate_sha,
                  "publishing_seal_identity": seal["identity"],
                  "publishing_bindings": {
                      path.relative_to(stage).as_posix(): PS.sha(path.read_bytes())
                      for path in sorted(PS.tree_files(stage))}})
    _write_json(_state_path(ctx["root"]), state, ctx["root"])
    return _resume_publication(ctx, state)


def _resume_publication(ctx, state):
    stage = _stage_book(ctx)
    bindings = state.get("publishing_bindings")
    if state.get("stage") != "PUBLISHING" or not isinstance(bindings, dict) or not bindings:
        raise ResearchBlocked("research publication recovery state is invalid")
    actual = {path.relative_to(stage).as_posix(): PS.sha(path.read_bytes())
              for path in sorted(PS.tree_files(stage))}
    if actual != bindings:
        raise ResearchBlocked("reviewed research stage changed during publication recovery")
    for path in sorted(PS.tree_files(stage)):
        relative = path.relative_to(stage).as_posix()
        target = ctx["book"] / relative
        if os.path.lexists(target):
            PS._safe_file(target, ctx["tree"])
        else:
            _ensure_dir(target.parent, ctx["tree"])
        _publish_file(target, path.read_bytes())
    identity = RC.research_seal_identity(ctx["book"])
    if identity != state.get("publishing_seal_identity"):
        raise ResearchFactoryError("shared validator rejected the newly sealed research identity")
    state.update({"stage": "SEALED", "seal_identity": identity,
                  "publishing_seal_identity": None, "publishing_bindings": None})
    _write_json(_state_path(ctx["root"]), state, ctx["root"])
    return identity


def _initial_state(ctx, policy, price):
    return {"schema": 1, "stage": "PREFLIGHT", "candidate": preflight(ctx["root"]),
        "policy_sha256": _sha(policy), "pricing": price,
        "budget": {"calls": 0, "output_tokens": 0, "cost_usd": 0,
                   "search_requests": 0, "fetch_uses": 0, "retained_results": 0},
        "reservations": {}, "reservation_groups": {}, "results": {}, "rejections": [],
        "corroboration": {},
        "gap_round": 0, "seal_identity": None}


def _load_or_initialize(ctx, policy, price):
    path = _state_path(ctx["root"])
    if not os.path.lexists(path):
        _ensure_dir(_factory_root(ctx["root"]), ctx["root"])
        state = _initial_state(ctx, policy, price)
        _write_json(path, state, ctx["root"])
        return state
    state = _read_json(path, ctx["root"], "research state")
    if state.get("schema") != 1 or state.get("candidate") != preflight(ctx["root"]) \
            or state.get("policy_sha256") != _sha(policy) or state.get("pricing") != price:
        raise ResearchBlocked("research resume identity, policy, or pricing changed")
    if state.get("late_eligibility_rejection"):
        raise ResearchBlocked("research remains blocked after independent rights/privacy rejection")
    if state.get("stage") == "SEALED":
        if RC.research_seal_identity(ctx["book"]) != state.get("seal_identity"):
            raise ResearchBlocked("sealed research changed after completion")
    return state


def _next_chapter_round(ctx, state, gaps, policy):
    start = state["chapter_gap_start_round"]
    current = state["chapter_gap_round"]
    if current - start + 1 >= policy["gap_round_ceiling"]:
        raise ResearchBlocked("targeted chapter gaps remain at the gap-round ceiling")
    safe = []
    for gap in gaps:
        if not isinstance(gap, dict):
            raise ResearchBlocked("targeted follow-up gap is malformed")
        code = _single_line(str(gap.get("kind") or gap.get("code") or "research_gap"),
                            "targeted follow-up gap code")
        code = re.sub(r"[^a-z0-9_]+", "_", code.casefold()).strip("_") or "research_gap"
        target = _single_line(str(gap.get("target") or "corpus"),
                              "targeted follow-up target")
        message = _single_line(str(gap.get("message") or gap.get("detail") or
                                   "additional accepted evidence required"),
                               "targeted follow-up detail")
        safe.append({"code": code[:64], "detail": f"{target}: {message}"})
    if not safe:
        raise ResearchBlocked("targeted follow-up has no precise demonstrated gap")
    following = current + 1
    state["chapter_gap_round"] = following
    state["gap_round"] = following
    state.setdefault("chapter_round_gaps", {})[str(following)] = safe
    state["stage"] = "TARGETED_GAP_REQUEST"
    _write_json(_state_path(ctx["root"]), state, ctx["root"])


def _advance_chapter_gap(ctx, gap, transport, editor, policy, price):
    prior = RC.inspect_research(ctx["book"], require_seal=True)
    if not prior.get("ok") or prior.get("seal_identity") != gap["research_seal_sha256"]:
        raise ResearchBlocked("targeted chapter continuation lost its current sealed corpus")
    plan = _sealed_plan(ctx["book"])
    master_plan_path = ctx["tree"] / gap["plan"]["path"]
    master_plan = PS._safe_file(master_plan_path, ctx["tree"]).read_text(encoding="utf-8")
    chapter_number = int(gap["chapter_id"].removeprefix("C-"))
    card = CS._section(master_plan, "C", chapter_number)
    card_fields = dict(CS.PLAN_FIELD.findall(card))
    ledger = CS._evidence_ledger(master_plan)
    evidence_ids = sorted(set(CS.EVIDENCE_ID.findall(
        card_fields.get("Evidence IDs and required limits", ""))))
    target_names = (
        "Objection / justification resolved", "Entering belief",
        "Concrete subject-specific encounter", "Enacted discovery", "Emotional turn",
        "Leaving belief", "Target personas / reader voice",
        "Evidence IDs and required limits", "Guardrails",
    )
    research_target = {
        "chapter_id": gap["chapter_id"],
        "card_fields": {name: card_fields[name] for name in target_names if name in card_fields},
        "evidence_ledger_rows": {name: ledger[name] for name in evidence_ids if name in ledger},
    }
    if not evidence_ids or len(research_target["evidence_ledger_rows"]) != len(evidence_ids):
        raise ResearchBlocked("targeted chapter gap lacks its exact evidence-ledger need")
    state = _load_or_initialize(ctx, policy, price)
    if state.get("stage") == "SEALED" and state.get("seal_identity") != prior["seal_identity"]:
        raise ResearchBlocked("targeted continuation state binds another research seal")
    gap_sha = _sha(gap)
    prior_gap = state.get("chapter_gap_sha256")
    if prior_gap not in (None, gap_sha):
        raise ResearchBlocked("targeted continuation state binds another chapter gap")
    if prior_gap is None:
        round_number = state["gap_round"] + 1
        state["chapter_gap_sha256"] = gap_sha
        state["chapter_gap_start_round"] = round_number
        state["chapter_gap_round"] = round_number
        state["chapter_round_gaps"] = {str(round_number): gap["gaps"]}
        state["gap_round"] = round_number
    else:
        round_number = state.get("chapter_gap_round")
        if type(round_number) is not int or round_number <= 0 \
                or state.get("gap_round") != round_number:
            raise ResearchBlocked("targeted continuation round identity is stale")
    state["stage"] = "TARGETED_GAP_REQUEST"
    _write_json(_state_path(ctx["root"]), state, ctx["root"])
    demonstrated_gaps = state.get("chapter_round_gaps", {}).get(str(round_number))
    if not isinstance(demonstrated_gaps, list) or not demonstrated_gaps:
        raise ResearchBlocked("targeted continuation lost its demonstrated round gap")
    remaining = policy["retained_result_ceiling"] - prior["counts"]["evidence_items"]
    if remaining <= 0:
        raise ResearchBlocked("targeted continuation has no retained-result capacity")
    packet_bindings = {}
    for packet in prior["inventory"]["packets"].values():
        relative = packet["path"]
        packet_bindings[relative] = PS.sha(
            PS._safe_file(ctx["book"] / relative, ctx["tree"]).read_bytes())
    minimal_inventory = {
        "packet_ids": sorted(prior["inventory"]["packets"]),
        "evidence_locators": sorted(prior["inventory"]["evidence"]),
        "unit_ids": sorted(prior["inventory"]["units"]),
    }
    request = {"kind": "gap-fill", "fresh_context": True, "round": round_number,
        "chapter_gap_request": gap, "brief": ctx["brief_path"].read_text(encoding="utf-8"),
        "research_target": research_target, "research_target_sha256": _sha(research_target),
        "plan_sha256": _sha(plan), "coverage_plan": plan["coverage_plan"],
        "candidate_sha256": prior["seal_identity"], "demonstrated_gaps": demonstrated_gaps,
        "retained_packet_sha256": packet_bindings,
        "retained_inventory": minimal_inventory,
        "retained_result_ceiling": min(policy["retained_results_per_call"], remaining),
        "retained_excerpt_character_ceiling": policy["retained_excerpt_characters"],
        "response_contract": _response_contract("gap-fill"),
        "instruction": ("Research only this current-seal/card-bound chapter gap; do not rerun the "
                        "corpus. Retain only a distinct fetched canonical source: unchanged accepted "
                        "packet bytes are immutable in a targeted extension.")}
    call_id = f"gap-r{round_number}"
    result = _call_group(ctx["root"], state, [(call_id, request, True)],
                         ctx["prompt_path"].read_text(encoding="utf-8"),
                         transport, policy, price)[0]
    state["results"][call_id] = result["result_sha256"]
    state["rejections"] = _aggregate_rejections(
        [*state.get("rejections", ()), *result["result"]["rejections"]])
    observed = {}
    retained = _dedupe(result["result"]["accepted"], remaining,
                       _existing_source_keys(ctx), observed)
    for kind, count in observed.items():
        state.setdefault("corroboration", {})[kind] = \
            state.setdefault("corroboration", {}).get(kind, 0) + count
    if not retained:
        raise ResearchBlocked("targeted chapter gap produced no new eligible evidence")
    keys = [item["locator"] for source in retained for item in source["evidence"]]
    synthesis_request = {"kind": "synthesis", "fresh_context": True,
        "brief": request["brief"], "chapter_gap_request": gap,
        "coverage": {"counts": prior["counts"], "gaps": prior["gaps"]},
        "evidence_keys": keys,
        "response_contract": _response_contract("synthesis"),
        "instruction": "Select only new evidence that resolves the demonstrated chapter gap."}
    synthesis_id = f"synthesis-r{round_number}"
    synthesis = _call_group(ctx["root"], state, [(synthesis_id, synthesis_request, False)],
                            ctx["prompt_path"].read_text(encoding="utf-8"),
                            transport, policy, price)[0]
    state["results"][synthesis_id] = synthesis["result_sha256"]
    selected = synthesis["result"]["selected_evidence_keys"]
    if not selected or set(selected) - set(keys):
        raise ResearchBlocked("targeted synthesis did not select eligible gap evidence")
    stage = _render_extension_stage(ctx, plan, state, retained, selected, prior)
    report = _inspect(stage)
    coverage = RC.build_coverage(stage, plan["preset"])
    if not report.get("ok"):
        coverage = _scarcity_coverage(ctx["root"], stage, report, coverage, plan["preset"])
    if coverage["status"] != "PASS":
        _next_chapter_round(ctx, state, report.get("gaps") or [
            {"kind": "coverage", "target": "extended corpus",
             "message": "; ".join(report.get("blockers", ()))[:1000]}], policy)
        return _advance_chapter_gap(ctx, gap, transport, editor, policy, price)
    PS.write_json(stage / "research/research-coverage.json", coverage)
    attempts = _attempt_receipts(ctx["root"])
    old_seal = _read_json(ctx["book"] / "research/research-seal.json", ctx["tree"],
                          "prior research seal")
    receipts = set(old_seal["authority"]["sanitized_receipt_hashes"])
    receipts.update(PS.sha(path.read_bytes()) for path in
                    _calls_root(ctx["root"]).glob("*.result.json")
                    if not path.name.startswith("editor-"))
    receipts.update(row["sha256"] for row in attempts)
    authority = {"prompt": {"path": "prompts/research-agent.md",
                            "sha256": PS.sha(ctx["prompt_path"].read_bytes())},
        "evidence_editor": {"path": "prompts/research-evidence-editor.md",
                            "sha256": PS.sha(ctx["editor_prompt_path"].read_bytes())},
        "configuration": {"path": ctx["manifest"]["run"]["config"],
                          "sha256": PS.sha(ctx["config_path"].read_bytes())},
        "sanitized_receipt_hashes": sorted(receipts)}
    candidate_sha = RC.candidate_identity(stage, authority)
    task = {"prompt": ctx["editor_prompt_path"].read_text(encoding="utf-8"),
        "candidate_sha256": candidate_sha, "coverage": coverage,
        "attempt_receipts": attempts,
        "bindings": {path.relative_to(stage).as_posix(): PS.sha(path.read_bytes())
                     for path in sorted(PS.tree_files(stage))},
        "artifacts": {path.relative_to(stage).as_posix(): path.read_text(encoding="utf-8")
                      for path in sorted(PS.tree_files(stage))},
        "chapter_gap_request": gap,
        "instruction": "Judge the exact bound extended corpus; return the required structured verdict."}
    editor_result = _editor_result(ctx["root"], state, task, editor, policy, price)
    verdict = editor_result["verdict"]
    if verdict["status"] != "PASS":
        _next_chapter_round(ctx, state, verdict["gaps"], policy)
        return _advance_chapter_gap(ctx, gap, transport, editor, policy, price)
    review = {"schema": 1, "status": "PASS", "task_sha256": editor_result["task_sha256"],
        "candidate_sha256": candidate_sha, "verdict_sha256": editor_result["verdict_sha256"],
        "editor_provenance": editor_result["editor_provenance"],
        "editor_receipt_sha256": editor_result["editor_receipt_sha256"],
        "gaps": [], "checks": verdict["checks"],
        "scarcity_waivers": verdict.get("scarcity_waivers", [])}
    return _seal_candidate(ctx, stage, state, plan, coverage, review, authority)


def advance(candidate_root, transport, editor, policy=None, chapter_gap_request=None,
            force_discovery=False):
    """Import-only deterministic seam for offline tests; production calls start()."""
    ctx = _context(candidate_root)
    if os.path.lexists(_state_path(ctx["root"])):
        publication_state = _read_json(
            _state_path(ctx["root"]), ctx["root"], "research state")
        if publication_state.get("stage") == "PURGING_ELIGIBILITY":
            _purge_late_eligibility_rejection(ctx["root"], publication_state)
            raise ResearchBlocked("research remains blocked after independent rights/privacy rejection")
        if publication_state.get("stage") == "BLOCKED_ELIGIBILITY" \
                or publication_state.get("late_eligibility_rejection"):
            raise ResearchBlocked("research remains blocked after independent rights/privacy rejection")
        if publication_state.get("chapter_gap_rotation") is not None:
            _finish_chapter_gap_rotation(ctx, publication_state)
            publication_state = _read_json(
                _state_path(ctx["root"]), ctx["root"], "research state")
        if publication_state.get("stage") == "PUBLISHING":
            return _resume_publication(ctx, publication_state)
    current_identity = _current_seal(ctx)
    proposed_gap = chapter_gap_request
    if proposed_gap is None and os.path.lexists(_chapter_gap_path(ctx["root"])):
        proposed_gap = _read_json(
            _chapter_gap_path(ctx["root"]), ctx["root"], "chapter gap request")
    if proposed_gap is not None and os.path.lexists(_state_path(ctx["root"])):
        completed = _read_json(_state_path(ctx["root"]), ctx["root"], "research state")
        if completed.get("stage") == "SEALED" \
                and completed.get("seal_identity") == current_identity \
                and completed.get("chapter_gap_sha256") == _sha(proposed_gap):
            return current_identity
    if chapter_gap_request is not None:
        gap = _persist_chapter_gap(ctx, chapter_gap_request)
    elif proposed_gap is not None:
        gap = _validated_chapter_gap(
            ctx, proposed_gap)
    else:
        gap = None
    if gap is None:
        if current_identity is not None and not force_discovery:
            return current_identity
    policy = dict(policy or policy_from_config(ctx["config"]))
    price = transport.pricing(policy)
    if price.get("model") != MODEL or not isinstance(price.get("max_cost_per_call"), (int, float)):
        raise ResearchBlocked("pricing preflight is invalid")
    if gap is not None:
        return _advance_chapter_gap(ctx, gap, transport, editor, policy, price)
    state = _load_or_initialize(ctx, policy, price)
    if state["stage"] == "SEALED":
        return state["seal_identity"]
    prompt = ctx["prompt_path"].read_text(encoding="utf-8")
    brief = ctx["brief_path"].read_text(encoding="utf-8")
    plan_request = {"kind": "plan", "fresh_context": True, "brief": brief,
        "lanes": list(LANES), "response_contract": _response_contract("plan"),
        "instruction": "Return the subject-specific coverage plan and one commission for every exact lane as JSON only."}
    plan_result = _call_group(ctx["root"], state, [("lead-plan", plan_request, False)],
                              prompt, transport, policy, price)[0]
    plan = plan_result["result"]
    state["results"]["lead-plan"] = plan_result["result_sha256"]
    state["stage"] = "PLAN"
    _write_json(_state_path(ctx["root"]), state, ctx["root"])
    lane_requests = [(f"lane-{index}-{lane}", {"kind": "discovery", "lane": lane,
        "fresh_context": True, "brief": brief, "coverage_plan": plan["coverage_plan"],
        "commission": plan["commissions"][lane],
        "retained_result_ceiling": policy["retained_results_per_call"],
        "retained_excerpt_character_ceiling": policy["retained_excerpt_characters"],
        "response_contract": _response_contract("discovery")}, True)
        for index, lane in enumerate(LANES, 1)]
    lane_results = _call_group(ctx["root"], state, lane_requests, prompt, transport,
                               policy, price, True)
    rows = []
    state["rejections"] = []
    for result in lane_results:
        state["results"][result["call_id"]] = result["result_sha256"]
        rows.extend(result["result"]["accepted"])
        state["rejections"] = _aggregate_rejections(
            [*state["rejections"], *result["result"]["rejections"]])
    # A completed targeted round is reconstructed from its sanitized durable
    # result. A marker without that result is never replayed or silently skipped.
    for round_number in range(1, state["gap_round"] + 1):
        gap_id = f"gap-r{round_number}"
        marker_path, result_path = _call_paths(ctx["root"], gap_id)
        if os.path.lexists(marker_path) and not os.path.lexists(result_path):
            raise ResearchBlocked(f"{gap_id}: ambiguous orphan call marker; replay forbidden")
        if not os.path.lexists(marker_path) or not os.path.lexists(result_path):
            raise ResearchBlocked(f"{gap_id}: durable gap-round evidence is incomplete")
        marker = _read_json(marker_path, ctx["root"], f"{gap_id} marker")
        result = _read_json(result_path, ctx["root"], f"{gap_id} result")
        _validate_provider_result(
            gap_id, marker, result, expected_kind="discovery")
        rows.extend(result["result"]["accepted"])
        state["results"][gap_id] = result["result_sha256"]
        state["rejections"] = _aggregate_rejections(
            [*state["rejections"], *result["result"]["rejections"]])
    existing = _existing_source_keys(ctx)
    observed = {}
    retained = _dedupe(rows, policy["retained_result_ceiling"], existing, observed)
    state["corroboration"] = observed
    state["stage"] = "FILTER_DEDUPE"
    _write_json(_state_path(ctx["root"]), state, ctx["root"])
    selected = None
    while True:
        stage = _render_stage(ctx, plan, state, retained, selected)
        report = _inspect(stage)
        coverage = RC.build_coverage(stage, plan["preset"])
        if not report.get("ok") and state["gap_round"] >= policy["gap_round_ceiling"]:
            coverage = _scarcity_coverage(
                ctx["root"], stage, report, coverage, plan["preset"])
        state["stage"] = "COVERAGE"
        _write_json(_state_path(ctx["root"]), state, ctx["root"])
        if not report.get("ok") and coverage["status"] != "PASS":
            if state["gap_round"] >= policy["gap_round_ceiling"]:
                raise ResearchBlocked("derived research gaps remain at the gap-round ceiling")
            state["gap_round"] += 1
            gap_request = _gap_request(ctx, plan, report, retained, state["gap_round"],
                                       policy["retained_results_per_call"],
                                       policy["retained_excerpt_characters"])
            gap_id = f"gap-r{state['gap_round']}"
            gap_result = _call_group(ctx["root"], state, [(gap_id, gap_request, True)],
                                     prompt, transport, policy, price)[0]
            state["results"][gap_id] = gap_result["result_sha256"]
            state["rejections"] = _aggregate_rejections(
                [*state["rejections"], *gap_result["result"]["rejections"]])
            observed = {}
            retained = _dedupe([*retained, *gap_result["result"]["accepted"]],
                               policy["retained_result_ceiling"], existing, observed)
            for kind, count in observed.items():
                state.setdefault("corroboration", {})[kind] = \
                    state.setdefault("corroboration", {}).get(kind, 0) + count
            selected = None
            state["stage"] = "TARGETED_GAP_FILL"
            _write_json(_state_path(ctx["root"]), state, ctx["root"])
            continue
        if selected is None:
            keys = [item["locator"]
                    for source in retained for item in source["evidence"]]
            request = {"kind": "synthesis", "fresh_context": True, "brief": brief,
                "coverage": {"counts": report.get("counts", {}),
                             "gaps": report.get("gaps", []),
                             "blockers": report.get("blockers", [])},
                "evidence_keys": keys,
                "response_contract": _response_contract("synthesis"),
                "instruction": "Select only relevant evidence keys; omit no item needed for a covered belief, persona, safety boundary, bank, or slot."}
            call_id = f"synthesis-r{state['gap_round']}"
            result = _call_group(ctx["root"], state, [(call_id, request, False)],
                                 prompt, transport, policy, price)[0]
            state["results"][call_id] = result["result_sha256"]
            selected = result["result"]["selected_evidence_keys"]
            if set(selected) - set(keys):
                raise ResearchBlocked("synthesis invented an unknown evidence key")
            state["stage"] = "SYNTHESIS"
            _write_json(_state_path(ctx["root"]), state, ctx["root"])
            continue
        if coverage["status"] != "PASS":
            raise ResearchBlocked("shared derived coverage did not PASS")
        PS.write_json(stage / "research/research-coverage.json", coverage)
        attempts = _attempt_receipts(ctx["root"])
        receipts = sorted({PS.sha(path.read_bytes()) for path in
                           _calls_root(ctx["root"]).glob("*.result.json")
                           if not path.name.startswith("editor-")} |
                          {row["sha256"] for row in attempts})
        authority = {"prompt": {"path": "prompts/research-agent.md",
                                "sha256": PS.sha(ctx["prompt_path"].read_bytes())},
            "evidence_editor": {"path": "prompts/research-evidence-editor.md",
                                "sha256": PS.sha(ctx["editor_prompt_path"].read_bytes())},
            "configuration": {"path": ctx["manifest"]["run"]["config"],
                              "sha256": PS.sha(ctx["config_path"].read_bytes())},
            "sanitized_receipt_hashes": receipts}
        candidate_sha = RC.candidate_identity(stage, authority)
        artifacts = {path.relative_to(stage).as_posix(): path.read_text(encoding="utf-8")
                     for path in sorted(PS.tree_files(stage))}
        task = {"prompt": ctx["editor_prompt_path"].read_text(encoding="utf-8"),
            "candidate_sha256": candidate_sha, "coverage": coverage,
            "attempt_receipts": attempts,
            "bindings": {path.relative_to(stage).as_posix(): PS.sha(path.read_bytes())
                         for path in sorted(PS.tree_files(stage))},
            "artifacts": artifacts,
            "instruction": "Judge the exact bound candidate; return the required structured verdict."}
        editor_result = _editor_result(ctx["root"], state, task, editor, policy, price)
        verdict = editor_result["verdict"]
        if verdict["status"] != "PASS":
            if state["gap_round"] >= policy["gap_round_ceiling"]:
                raise ResearchBlocked("independent review gaps remain at the gap-round ceiling")
            report = {**report, "ok": False, "gaps": verdict["gaps"],
                      "blockers": ["independent evidence review rejected"]}
            state["gap_round"] += 1
            gap_id = f"gap-r{state['gap_round']}"
            gap_result = _call_group(ctx["root"], state,
                [(gap_id, _gap_request(ctx, plan, report, retained, state["gap_round"],
                                      policy["retained_results_per_call"],
                                      policy["retained_excerpt_characters"]), True)],
                prompt, transport, policy, price)[0]
            state["results"][gap_id] = gap_result["result_sha256"]
            state["rejections"] = _aggregate_rejections(
                [*state["rejections"], *gap_result["result"]["rejections"]])
            observed = {}
            retained = _dedupe([*retained, *gap_result["result"]["accepted"]],
                               policy["retained_result_ceiling"], existing, observed)
            for kind, count in observed.items():
                    state.setdefault("corroboration", {})[kind] = \
                    state.setdefault("corroboration", {}).get(kind, 0) + count
            selected = None
            state["stage"] = "TARGETED_GAP_FILL"
            _write_json(_state_path(ctx["root"]), state, ctx["root"])
            continue
        review = {"schema": 1, "status": "PASS", "task_sha256": editor_result["task_sha256"],
            "candidate_sha256": candidate_sha, "verdict_sha256": editor_result["verdict_sha256"],
            "editor_provenance": editor_result["editor_provenance"],
            "editor_receipt_sha256": editor_result["editor_receipt_sha256"],
            "gaps": [], "checks": verdict["checks"],
            "scarcity_waivers": verdict.get("scarcity_waivers", [])}
        state["stage"] = "INDEPENDENT_REVIEW"
        _write_json(_state_path(ctx["root"]), state, ctx["root"])
        return _seal_candidate(ctx, stage, state, plan, coverage, review, authority)


def start(candidate_root, chapter_gap_request=None):
    """The sole non-injectable production facade."""
    _context(candidate_root)  # completed subject and RF-02 identity, read-only
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise ResearchBlocked("OPENROUTER_API_KEY is missing; no research was started")
    return advance(candidate_root, OpenRouterTransport(key), NativeEvidenceEditor(),
                   chapter_gap_request=chapter_gap_request)


def start_experiment(candidate_root):
    """Run one real isolated causal arm even when its baseline seal is current."""
    _context(candidate_root)
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise ResearchBlocked("OPENROUTER_API_KEY is missing; no research was started")
    return advance(candidate_root, OpenRouterTransport(key), NativeEvidenceEditor(),
                   force_discovery=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    start_parser = subparsers.add_parser("start", help="start or resume real candidate research")
    LG.add_arguments(start_parser)
    start_parser.add_argument("--chapter-gap-request",
                              help="current-seal/plan/card-bound targeted gap JSON")
    args = parser.parse_args(argv)
    candidate = LG.require_authorized(
        args, entrypoint="research_factory.py", pre_rf23_stage="RF-21",
        require_in_progress=True)
    if LG.dry_run(args, "research_factory.py"):
        return 0
    try:
        gap = None
        if args.chapter_gap_request:
            gap = json.loads(Path(args.chapter_gap_request).read_text(encoding="utf-8"))
        identity = start(candidate, gap)
    except (ResearchFactoryError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"research-factory: BLOCKED — {exc}", file=sys.stderr)
        return 1
    print(f"research-factory: SEALED {identity}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
