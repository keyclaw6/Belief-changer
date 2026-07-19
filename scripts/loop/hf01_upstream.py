"""Dispatch and verify the six authority-bound H-F01 RF21/RF22 calls."""
import datetime as dt, json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "eval"))
import commission_set as CS  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import hf01_upstream_contract as CONTRACT  # noqa: E402
import native_judge as NATIVE  # noqa: E402
import pair_store as PS  # noqa: E402
import path_guard as PG  # noqa: E402

PATH = "rf21-rf22-receipt.json"
FOLDER = "loop/experiments/h-f01-treatment/evidence/hf01"
IDS, LADDER = CONTRACT.IDS, CONTRACT.LADDER
PLAN_SCHEMA, REVIEW_SCHEMA = CONTRACT.PLAN_SCHEMA, CONTRACT.REVIEW_SCHEMA
COMMISSION_SCHEMA, AUDIT_SCHEMA = CONTRACT.COMMISSION_SCHEMA, CONTRACT.AUDIT_SCHEMA
RECEIPT_FIELDS = {"schema", "authority_sha256", "completed_at_utc", "calls",
                  "artifacts", "commission_receipt_sha256", "receipt_hash"}
RECORD_FIELDS = {"schema", "id", "authority_sha256", "task_sha256", "input_sha256",
    "output_sha256", "actor", "model", "route", "reasoning", "command", "thread_id",
    "started_at_utc", "completed_at_utc", "raw"}

class UpstreamError(RuntimeError): pass
class UpstreamPending(UpstreamError):
    def __init__(self, path): self.path = path; super().__init__(f"native H-F01 evidence is missing: {path}")

def _time(): return dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")
def _parsed(value):
    try: parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc: raise UpstreamError("native call timestamp is invalid") from exc
    if parsed.utcoffset() != dt.timedelta(0): raise UpstreamError("native call timestamp is not UTC")
    return parsed
def _read(path):
    try: return PG.safe_file(path, path.parent).read_bytes()
    except (PG.PathError, OSError) as exc: raise UpstreamError(str(exc)) from exc
def _write(path, data):
    path = Path(path)
    if os.path.lexists(path):
        if _read(path) != data: raise UpstreamError(f"immutable H-F01 evidence differs: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data); handle.flush(); os.fchmod(handle.fileno(), 0o444); os.fsync(handle.fileno())
    PS._sync(path.parent)
def _json(raw, call_id):
    try: value = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc: raise UpstreamError(f"{call_id}: invalid JSON output") from exc
    if not isinstance(value, dict): raise UpstreamError(f"{call_id}: output must be an object")
    return value
def _spec(index):
    command = lambda model, reasoning: NATIVE.command(
        "<isolated-tmp>", "<isolated-tmp>/judge-output-schema.json", model, reasoning)
    return CONTRACT.spec(index, HF.ROUTE_LAW, command, HF.BOOK)
def call_specs(_paths=None, _maps=None): return [_spec(index) for index in range(6)]
def authority_contract(paths, maps):
    return {"subject_reference_isolation": {"subject": HF.SUBJECT, "generation_book": HF.BOOK,
        "generation_root": str(paths["treatment"]["candidate"]),
        "reference_root": str(paths["control"]["experiment"] / "evaluation/calibration/reference/gsbs"),
        "reference_mode": "evaluation-only", "reference_in_rf21_rf22_inputs": False},
        "validation_ladder": LADDER, "rf21_rf22_native_calls": call_specs(paths, maps)}
def _task(spec, authority_sha, inputs):
    body = {"schema": 1, "id": spec["id"], "actor": spec["actor"], "role": spec["role"],
        "fresh_context": True, "reference_blind": True, "authority_sha256": authority_sha,
        "instruction": "Return only the strict JSON output. Do not read files, tools, history, references, or prior verdicts.",
        "inputs": inputs, "output_identities": spec["output_identities"]}
    return {**body, "task_sha256": PS.state_hash(body)}
def _record(base, spec, authority_sha, task, schema, complete):
    task_path, path = base / "upstream/tasks" / f"{spec['id']}.json", base / "upstream/calls" / f"{spec['id']}.json"
    task_bytes = PS.json_bytes(task)
    if path.is_file():
        value = json.loads(_read(path)); expected = {"id": spec["id"], "authority_sha256": authority_sha,
            "task_sha256": task["task_sha256"], "input_sha256": PS.sha(task_bytes),
            "actor": spec["actor"], "model": spec["model"], "route": spec["route"],
            "reasoning": spec["reasoning"], "command": spec["command"]}
        if set(value) != RECORD_FIELDS or value.get("schema") != 1 \
                or any(value.get(key) != item for key, item in expected.items()) \
                or value.get("output_sha256") != PS.sha(str(value.get("raw", "")).encode()) \
                or not value.get("thread_id") or _read(task_path) != task_bytes:
            raise UpstreamError(f"{spec['id']}: native record binding is stale")
        return value
    if task_path.exists(): raise UpstreamError(f"{spec['id']}: native call outcome is ambiguous; do not replay")
    if complete is None: raise UpstreamPending(path)
    _write(task_path, task_bytes); started = _time()
    raw, transport, error = complete(json.dumps(task, sort_keys=True, ensure_ascii=False),
        spec["actor"], schema, model=spec["model"], reasoning=spec["reasoning"])
    if error: raise UpstreamError(f"{spec['id']}: {error}")
    expected_transport = (spec["model"], spec["reasoning"], spec["command"])
    if (transport.get("model"), transport.get("reasoning_effort"), transport.get("command")) != expected_transport \
            or not transport.get("thread_id"):
        raise UpstreamError(f"{spec['id']}: native transport identity is stale")
    _json(raw, spec["id"])
    value = {"schema": 1, "id": spec["id"], "authority_sha256": authority_sha,
        "task_sha256": task["task_sha256"], "input_sha256": PS.sha(task_bytes),
        "output_sha256": PS.sha(raw.encode()), "actor": spec["actor"], "model": spec["model"],
        "route": spec["route"], "reasoning": spec["reasoning"], "command": spec["command"],
        "thread_id": transport["thread_id"], "started_at_utc": started,
        "completed_at_utc": _time(), "raw": raw}
    _write(path, PS.json_bytes(value)); return value

def _baseline_inputs(root):
    base = HF.arm_paths(root)["control"]["candidate"]
    names = ("prompts/style-guide.md", f"{HF.BOOK}/00-brief.md", f"{HF.BOOK}/framing.md",
             f"{HF.BOOK}/research/lived-experience.md", f"{HF.BOOK}/research/scientific-evidence.md")
    contract = "\n\n".join((HF.REPO / path).read_text(encoding="utf-8") for path in
        ("production-books/_template/00-brief.md", "production-books/_template/framing.md",
         "prompts/master-plan-skill-v2.md"))
    return {"contract": contract,
        "rf21_scope": "Revise only the brief, framing, and master plan for the first three cumulative sugar transitions; also return exact RF22 assignment authority derived only from the two syntheses.",
        "files": {name: (base / name).read_text(encoding="utf-8") for name in names}}
def _assignments(root, rows):
    try: return CONTRACT.assignments(root, rows, HF.arm_paths)
    except (KeyError, TypeError, ValueError) as exc: raise UpstreamError(f"rf21-plan: {exc}") from exc
def _declare_review(experiment):
    manifest = CS.CP.load(experiment); relative = f"{HF.BOOK}/framing-review.md"
    if relative in {item["path"] for item in manifest["outputs"]}: return
    updated = dict(manifest); updated["outputs"] = [*manifest["outputs"], {"group": "product", "path": relative}]
    PS.exact_layout(experiment, manifest, {".pair.json.rf02-tmp": PS.json_bytes(updated)})
    PS.write_json(CS.CP._manifest_path(experiment), updated)
def _apply(path, text, baseline=None):
    data = (text.rstrip() + "\n").encode(); path = Path(path)
    if path.is_file() and path.read_bytes() == data: return
    if baseline is None and path.exists():
        raise UpstreamError(f"RF21 output already exists with different bytes: {path}")
    if baseline is not None and (not path.is_file() or path.read_bytes() != baseline):
        raise UpstreamError(f"RF21 output escaped its frozen baseline: {path}")
    PS.write(path, data)
def _plan_outputs(root, value, apply):
    paths = HF.arm_paths(root); treatment, control = paths["treatment"]["candidate"], paths["control"]["candidate"]
    mapping = {f"{HF.BOOK}/00-brief.md": "brief", f"{HF.BOOK}/framing.md": "framing",
               f"{HF.BOOK}/master-plan.md": "master_plan"}
    if set(value) != {"brief", "framing", "master_plan", "assignments"}: raise UpstreamError("rf21-plan: output fields are not exact")
    for relative, key in mapping.items():
        target, expected = treatment / relative, (value[key].rstrip() + "\n").encode()
        if apply: _apply(target, value[key], (control / relative).read_bytes())
        elif target.read_bytes() != expected: raise UpstreamError(f"rf21-plan: stale {relative}")
    return _assignments(root, value["assignments"])
def _review_inputs(root):
    book = HF.arm_paths(root)["treatment"]["book"]
    contract = "\n\n".join((HF.REPO / path).read_text(encoding="utf-8") for path in
        ("production-books/_template/framing-review.md", "prompts/master-plan-reviewer-v2.md"))
    files = ("prompts/style-guide.md", f"{HF.BOOK}/00-brief.md", f"{HF.BOOK}/framing.md",
             f"{HF.BOOK}/master-plan.md", f"{HF.BOOK}/research/lived-experience.md",
             f"{HF.BOOK}/research/scientific-evidence.md")
    candidate = HF.arm_paths(root)["treatment"]["candidate"]
    return {"contract": contract, "files": {name: (candidate / name).read_text(encoding="utf-8") for name in files}}
def _review_outputs(root, value, apply):
    if set(value) != {"framing_review", "master_plan_review"}: raise UpstreamError("rf21-plan-review: output fields are not exact")
    paths = HF.arm_paths(root); experiment, book = paths["treatment"]["experiment"], paths["treatment"]["book"]
    if apply: _declare_review(experiment)
    targets = ((book / "framing-review.md", value["framing_review"], None),
               (book / "master-plan-review.md", value["master_plan_review"], paths["control"]["book"] / "master-plan-review.md"))
    for path, text, baseline in targets:
        expected = (text.rstrip() + "\n").encode()
        if apply: _apply(path, text, baseline.read_bytes() if baseline else None)
        elif path.read_bytes() != expected: raise UpstreamError(f"rf21-plan-review: stale {path.name}")

def _commission_calls(root, authority_sha, assignments, complete, records):
    experiment, base = HF.arm_paths(root)["treatment"]["experiment"], Path(root) / FOLDER
    def commissioner(request):
        index = int(request["target"][2:]) + 1; spec = _spec(index)
        task = _task(spec, authority_sha, request); record = _record(base, spec, authority_sha, task, COMMISSION_SCHEMA, complete)
        records.append(record); value = _json(record["raw"], spec["id"])
        if set(value) != {"commission"}: raise UpstreamError(f"{spec['id']}: output fields are not exact")
        return value["commission"]
    def auditor(request):
        spec = _spec(5); task = _task(spec, authority_sha, request)
        record = _record(base, spec, authority_sha, task, AUDIT_SCHEMA, complete); records.append(record)
        value = _json(record["raw"], spec["id"])
        if set(value) != {"verdict"}: raise UpstreamError("rf22-audit: output fields are not exact")
        return value["verdict"]
    if not (experiment / "evidence" / CS.RECEIPT).is_file():
        CS.generate(experiment, assignments, commissioner, auditor)
    receipt = json.loads(_read(experiment / "evidence" / CS.RECEIPT))
    if receipt.get("assignments") != assignments: raise UpstreamError("RF22 assignment authority differs from RF21 output")
    inputs = CS._inputs(experiment, CS.CP.inspect(experiment), assignments)
    requests = {chapter: {"role": "fresh high-reasoning commissioning editor", "fresh_context": True,
        "reasoning": "high", "reference_blind": True, "prompt": inputs["commissioner"], "target": chapter,
        "accepted_plan": inputs["plan"], "target_card": inputs["cards"][chapter]["plan"],
        "state_card": inputs["cards"][chapter]["state"], "assigned_packets": inputs["packets"][chapter]}
        for chapter in CS._selection(CS.CP.inspect(experiment))}
    for chapter, request in requests.items():
        spec = _spec(int(chapter[2:]) + 1); records.append(_record(base, spec, authority_sha,
            _task(spec, authority_sha, request), COMMISSION_SCHEMA, None))
    commissions = {chapter: CS._member_text(experiment, CS.CP.inspect(experiment),
        f"{HF.BOOK}/commissions/chapter-{int(chapter[2:]):02d}.md").strip() for chapter in requests}
    audit = {"role": "fresh high-reasoning commission-set auditor", "fresh_context": True,
        "reasoning": "high", "reference_blind": True, "prompt": inputs["auditor"],
        "selection": list(requests), "commissions": commissions, "accepted_cards": inputs["cards"],
        "assignments": inputs["assignments"], "assigned_evidence": inputs["evidence"]}
    spec = _spec(5); records.append(_record(base, spec, authority_sha, _task(spec, authority_sha, audit), AUDIT_SCHEMA, None))
    return receipt["receipt_hash"]

def _pipeline(root, authority, authority_sha, complete, apply):
    root, base, records = Path(root).absolute(), Path(root).absolute() / FOLDER, []
    plan_spec = _spec(0); plan = _record(base, plan_spec, authority_sha,
        _task(plan_spec, authority_sha, _baseline_inputs(root)), PLAN_SCHEMA, complete)
    records.append(plan); assignments = _plan_outputs(root, _json(plan["raw"], plan_spec["id"]), apply)
    review_spec = _spec(1); review = _record(base, review_spec, authority_sha,
        _task(review_spec, authority_sha, _review_inputs(root)), REVIEW_SCHEMA, complete)
    records.append(review); _review_outputs(root, _json(review["raw"], review_spec["id"]), apply)
    CS.SC.require_subject_contract(HF.arm_paths(root)["treatment"]["book"], "commissioning")
    commission = _commission_calls(root, authority_sha, assignments, complete, records)
    unique = {row["id"]: row for row in records}
    if set(unique) != set(IDS) or len({row["thread_id"] for row in unique.values()}) != 6:
        raise UpstreamError("RF21/RF22 requires six fresh native call identities")
    previous = _parsed(authority["frozen_at_utc"])
    for row in (unique[item] for item in IDS):
        started, completed = _parsed(row["started_at_utc"]), _parsed(row["completed_at_utc"])
        if not previous <= started <= completed: raise UpstreamError("RF21/RF22 native call chronology is stale")
        previous = completed
    artifacts = HF.treatment_artifacts(root)
    calls = [{key: row[key] for key in RECORD_FIELDS - {"schema", "raw"}} for row in (unique[item] for item in IDS)]
    body = {"schema": 2, "authority_sha256": authority_sha, "completed_at_utc": _time(),
        "calls": calls, "artifacts": artifacts, "commission_receipt_sha256": commission}
    return {**body, "receipt_hash": PS.state_hash(body)}
def dispatch(root, authority, authority_sha, complete=NATIVE.complete):
    value = _pipeline(root, authority, authority_sha, complete, True)
    path = Path(root).absolute() / FOLDER / PATH; _write(path, PS.json_bytes(value)); return PS.sha(_read(path))
def verify(root, authority, authority_sha):
    path = Path(root).absolute() / FOLDER / PATH
    if not path.is_file(): raise UpstreamPending(path)
    value = json.loads(_read(path)); body = {key: item for key, item in value.items() if key != "receipt_hash"}
    if set(value) != RECEIPT_FIELDS or value.get("schema") != 2 or value.get("authority_sha256") != authority_sha \
            or value.get("receipt_hash") != PS.state_hash(body): raise UpstreamError("RF21/RF22 receipt binding is invalid")
    expected = _pipeline(root, authority, authority_sha, None, False)
    for key in ("schema", "authority_sha256", "calls", "artifacts", "commission_receipt_sha256"):
        if value[key] != expected[key]: raise UpstreamError(f"RF21/RF22 receipt {key} is stale")
    return PS.sha(_read(path))
