"""H-F01 position-swapped GSBS tasks and frozen blind evidence."""
import datetime as dt, json, os, shlex, sys
from pathlib import Path
HERE = Path(__file__).resolve(); sys.path[:0] = [str(HERE.parent), str(HERE.parents[1] / "eval")]
import candidate_pair as CP  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import judges  # noqa: E402
import native_judge as NATIVE  # noqa: E402
import pair_store as PS  # noqa: E402
import path_guard as PG  # noqa: E402
import product_effect as PE  # noqa: E402
import product_effect_absolute as ABS  # noqa: E402
import product_effect_panel as PANEL  # noqa: E402
import immutable_file as IF  # noqa: E402
FOLDER = "loop/experiments/h-f01-treatment/evidence/hf01"
TASKS, RECEIPT = "blind-tasks.json", "blind-receipt.json"
READERS = ("sol-xhigh-r1", "sol-xhigh-r2")
ABS_FIELDS = {"schema", "actor", "model", "route", "reasoning", "command",
              "authority_sha256", "task_sha256", "input_sha256", "native_call_sha256",
              "raw_verdict_id", "raw_verdict"}
CALL_FIELDS = {"schema", "id", "authority_sha256", "task_sha256", "input_sha256",
    "output_sha256", "actor", "model", "route", "reasoning", "command", "thread_id", "raw"}
class BlindError(RuntimeError): pass
class BlindPending(BlindError):
    def __init__(self, commands): self.commands = commands; super().__init__("blind native evidence pending")
def folder(root): return HF.require_authorized_root(root) / FOLDER
def now(): return dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")
def _read(path):
    try: return PG.safe_file(path, Path(path).parent).read_bytes()
    except (PG.PathError, OSError) as exc: raise BlindError(f"invalid {path}: {exc}") from exc
def read(path):
    try: return json.loads(_read(path))
    except json.JSONDecodeError as exc: raise BlindError(f"invalid {path}: {exc}") from exc
def write(path, value):
    path, data = Path(path), PS.json_bytes(value)
    try:
        PG.ensure_dir(path.parent)
        IF.write_once(path, data, _read, "H-F01 evidence")
    except (PG.PathError, IF.ImmutableFileError) as exc: raise BlindError(f"H-F01 evidence write failed: {exc}") from exc
    return value
def _write_bytes(path, data):
    path = Path(path)
    try:
        PG.ensure_dir(path.parent)
        IF.write_once(path, data, _read, "H-F01 task")
    except (PG.PathError, IF.ImmutableFileError) as exc: raise BlindError(f"H-F01 task write failed: {exc}") from exc
def _native_call(base, identity, authority_sha, task_sha, prompt, route, schema,
                 materialized, native, complete, actor=None):
    expected = {"id": identity, "authority_sha256": authority_sha, "task_sha256": task_sha,
        "input_sha256": PS.sha(prompt), "actor": actor or identity, "model": route["model"],
        "route": route["route"], "reasoning": route["reasoning"], "command": NATIVE.command(
            "<isolated-tmp>", "<isolated-tmp>/judge-output-schema.json", route["model"], route["reasoning"])}
    marker, result = base / "native/tasks" / f"{identity}.json", base / "native/calls" / f"{identity}.json"
    marker_value = {"schema": 1, **expected}
    if result.is_file():
        if not marker.is_file() or read(marker) != marker_value:
            raise BlindError(f"{identity}: blind task marker is stale")
        value = read(result)
        if set(value) != CALL_FIELDS or value.get("schema") != 1 \
                or any(value.get(key) != item for key, item in expected.items()) \
                or value.get("output_sha256") != PS.sha(str(value.get("raw", "")).encode()) \
                or not value.get("thread_id"):
            raise BlindError(f"{identity}: blind native result binding is stale")
        return value
    if marker.exists(): raise BlindError(f"{identity}: blind call outcome is ambiguous; do not replay")
    if materialized.exists(): raise BlindError(f"{identity}: blind verdict lacks its durable native result; do not replay")
    if not native: return None
    write(marker, marker_value)
    raw, transport, error = complete(prompt.decode(), expected["actor"], schema,
        model=route["model"], reasoning=route["reasoning"])
    if error: raise BlindError(f"{identity}: {error}")
    if (transport.get("model"), transport.get("reasoning_effort"), transport.get("command")) != \
            (route["model"], route["reasoning"], expected["command"]) or not transport.get("thread_id"):
        raise BlindError(f"{identity}: blind native transport identity is stale")
    value = {"schema": 1, **expected, "output_sha256": PS.sha(raw.encode()),
             "thread_id": transport["thread_id"], "raw": raw}
    write(result, value); return value
def _chapters(root, arm):
    book = HF.arm_paths(root)[arm]["book"]
    return [(book / f"chapters/chapter-{n:02d}.md").read_text(encoding="utf-8")
            for n in HF.CHAPTERS]
def _gsbs(root, authority):
    base = HF.arm_paths(root)["treatment"]["experiment"] / "evaluation"
    rows = []
    for match in authority["identity"]["gsbs_matches"]:
        path = base / match["path"]
        try: data = path.read_bytes()
        except OSError as exc: raise BlindError(f"GSBS match missing: {path}") from exc
        if PS.sha(data) != match["sha256"]: raise BlindError("GSBS matched file hash changed")
        rows.append({**match, "text": data.decode("utf-8")})
    if PS.state_hash([{key: row[key] for key in ("treatment_chapter", "reference_position", "path", "sha256")}
                      for row in rows]) != authority["identity"]["gsbs_sha256"]:
        raise BlindError("GSBS offset mapping changed")
    return rows
def bundle(root, hashes, integrity, authority, upstream_sha):
    target = folder(root) / TASKS
    control, treatment, gsbs = _chapters(root, "control"), _chapters(root, "treatment"), _gsbs(root, authority)
    experiment = PS.state_hash({"control_pair_hash": hashes["control"],
        "treatment_pair_hash": hashes["treatment"], "gsbs_sha256": authority["identity"]["gsbs_sha256"]})
    absolute = []
    for arm, contents in (("control", control), ("treatment", treatment)):
        for number, content in zip(HF.CHAPTERS, contents):
            key = f"{arm}-chapter-{number:02d}"; task = ABS.chapter(HF.SUBJECT, content)
            absolute.append({"key": key, "identity": f"hf01-absolute-{key}",
                "route": {"model": authority["route"]["judge_model"],
                    "route": authority["route"]["judge_route"],
                    "reasoning": authority["route"]["judge_reasoning"]},
                "envelope": ABS.envelope(task, key, experiment)})
    panels, panel_hashes = [], []
    for index, match in enumerate(gsbs):
        files = {match["path"]: match["sha256"]}; rows = []
        for reader, treatment_label in zip(READERS, ("B", "A")):
            task = PE.chapter_pair(HF.SUBJECT, match["text"], treatment[index]) if treatment_label == "B" \
                else PE.chapter_pair(HF.SUBJECT, treatment[index], match["text"])
            rows.append({"identity": reader, "envelope": PE.h_f01_envelope(
                task, hashes["treatment"], files, treatment_label, reader)})
        panels.append({"key": f"chapter-{index + 1:02d}", "readers": rows}); panel_hashes.append(PS.state_hash(files))
    files = {row["path"]: row["sha256"] for row in gsbs}; rows = []
    gsbs_text = [row["text"] for row in gsbs]
    for reader, treatment_label in zip(READERS, ("B", "A")):
        task = PE.whole_opening(HF.SUBJECT, gsbs_text, treatment) if treatment_label == "B" \
            else PE.whole_opening(HF.SUBJECT, treatment, gsbs_text)
        rows.append({"identity": reader, "envelope": PE.h_f01_envelope(
            task, hashes["treatment"], files, treatment_label, reader)})
    panels.append({"key": "whole-opening", "readers": rows}); panel_hashes.append(PS.state_hash(files))
    body = {"schema": 2, "subject": HF.SUBJECT, "authority_sha256": PS.sha(PS.json_bytes(authority)),
        "upstream_receipt_sha256": upstream_sha, "control_pair_hash": hashes["control"],
        "treatment_pair_hash": hashes["treatment"], "experiment_sha256": experiment,
        "gsbs_matches": [{key: row[key] for key in ("treatment_chapter", "reference_position", "path", "sha256")} for row in gsbs],
        "gsbs_sha256": authority["identity"]["gsbs_sha256"], "gsbs_panel_sha256": panel_hashes,
        "integrity": integrity, "absolute_causal_diagnostic": absolute, "gsbs_panels": panels}
    return write(target, {**body, "task_bundle_sha256": PS.state_hash(body)})
def _absolute_record(base, row, prompt, authority_sha, native, complete=NATIVE.complete):
    task, path = ABS.judge_task(row["envelope"]), base / "absolute/verdicts" / f"{row['key']}.json"
    call = _native_call(base, row["identity"], authority_sha, task["task_sha256"], prompt,
                        row["route"], ABS.output_schema(), path, native, complete)
    if call is not None and not path.is_file():
        ABS.verdict(call["raw"], task)
        write(path, {"schema": 1, "actor": row["identity"], "authority_sha256": authority_sha,
            "model": call["model"], "route": call["route"], "reasoning": call["reasoning"],
            "command": call["command"], "task_sha256": task["task_sha256"],
            "input_sha256": PS.sha(prompt), "native_call_sha256": PS.sha(PS.json_bytes(call)),
            "raw_verdict_id": call["thread_id"], "raw_verdict": call["raw"]})
    if not path.is_file(): return None
    value = read(path); route = row["route"]
    command = NATIVE.command("<isolated-tmp>", "<isolated-tmp>/judge-output-schema.json",
                             route["model"], route["reasoning"])
    if set(value) != ABS_FIELDS or value.get("schema") != 1 or value.get("actor") != row["identity"] \
            or value.get("model") != route["model"] or value.get("route") != route["route"] \
            or value.get("reasoning") != route["reasoning"] or value.get("authority_sha256") != authority_sha \
            or value.get("task_sha256") != task["task_sha256"] \
            or value.get("input_sha256") != PS.sha(prompt) or value.get("command") != command \
            or value.get("native_call_sha256") != PS.sha(PS.json_bytes(call)) \
            or not isinstance(value.get("raw_verdict_id"), str) or not value["raw_verdict_id"]:
        raise BlindError("absolute native route, identity, command, or task binding is stale")
    ABS.verdict(value["raw_verdict"], task); return value
def emit(root, task_bundle, authority, native=False, complete=NATIVE.complete):
    base, treatment = folder(root), HF.arm_paths(root)["treatment"]["experiment"]
    view, commands = CP.open_sealed(treatment, task_bundle["treatment_pair_hash"]), []
    rubric_bytes = Path(view["config"]["product_effect_absolute_rubric"]).read_bytes()
    rubric = rubric_bytes.decode("utf-8")
    if rubric.count("{{TASK}}") != 1 or "{{REFERENCE}}" in rubric: raise BlindError("absolute rubric is not blind")
    write(base / "absolute-schema.json", ABS.output_schema())
    missing_absolute = False
    for row in task_bundle["absolute_causal_diagnostic"]:
        task = ABS.judge_task(row["envelope"]); prompt = rubric.replace("{{TASK}}", json.dumps(
            task, sort_keys=True, separators=(",", ":"), ensure_ascii=False)).encode()
        _write_bytes(base / "absolute/tasks" / f"{row['key']}.md", prompt)
        if _absolute_record(base, row, prompt, task_bundle["authority_sha256"], native, complete) is None:
            missing_absolute = True
    if missing_absolute: commands.append(HF.resume_command(authority, stage="RF-23", native=True))
    for panel in task_bundle["gsbs_panels"]:
        for item in panel["readers"]:
            envelope, identity = item["envelope"], item["identity"]
            task, name = PE.h_f01_judge_task(envelope), f"{panel['key']}-{identity}"
            task_path = base / "gsbs" / f"{name}.json"; write(task_path, task)
            rows = PANEL.emit(view["config"], name, task, identities=(identity,),
                tested_pair_hash=task_bundle["experiment_sha256"], single=True)
            verdict_path, prompt = rows[0][3], PANEL._prompt(view["config"], task)[0]
            call = _native_call(base, f"gsbs-{name}", task_bundle["authority_sha256"],
                task["task_sha256"], prompt, {"model": view["config"]["judge_model"],
                "route": view["config"]["judge_route"], "reasoning": view["config"]["judge_reasoning"]},
                PE.output_schema(), verdict_path, native, complete, identity)
            if call is None: commands.append(HF.resume_command(authority, stage="RF-23", native=True)); continue
            if not verdict_path.is_file():
                PANEL.dispatch(view["config"], name, task, identities=(identity,),
                    tested_pair_hash=task_bundle["experiment_sha256"], single=True,
                    complete=lambda *_args, **_kwargs: (call["raw"], {"thread_id": call["thread_id"],
                        "model": call["model"], "reasoning_effort": call["reasoning"],
                        "command": call["command"], "input_sha256": call["input_sha256"]}, None))
            record = PANEL.records(view["config"], name, task, identities=(identity,),
                tested_pair_hash=task_bundle["experiment_sha256"], single=True)[0]
            if (record["raw_verdict_id"], record["raw_verdict"]) != (call["thread_id"], call["raw"]):
                raise BlindError(f"{name}: GSBS verdict differs from durable native result")
    if commands: raise BlindPending(sorted(set(commands)))
    return view
def freeze(root, task_bundle, view, carr_name):
    base, task_ids, raw_ids, transitions, diagnostic = folder(root), [], [], [], {"control": [], "treatment": []}
    rubric = Path(view["config"]["product_effect_absolute_rubric"]).read_text(encoding="utf-8")
    for row in task_bundle["absolute_causal_diagnostic"]:
        task = ABS.judge_task(row["envelope"]); prompt = rubric.replace("{{TASK}}", json.dumps(
            task, sort_keys=True, separators=(",", ":"), ensure_ascii=False)).encode()
        value = _absolute_record(base, row, prompt, task_bundle["authority_sha256"], False); verdict = ABS.verdict(value["raw_verdict"], task)
        arm = row["key"].split("-", 1)[0]; task_ids.append(task["task_sha256"]); raw_ids.append(value["raw_verdict_id"])
        diagnostic[arm].append({"key": row["key"], "task_sha256": task["task_sha256"],
            "record_sha256": PS.sha(PS.json_bytes(value)), "observation": verdict["observation"]})
        if arm == "treatment":
            obs = verdict["observation"]
            if obs["construct_sufficiency"] != "MEETS": raise BlindError("treatment absolute observation does not meet")
            transitions.append(tuple(obs[key] for key in ("entering_belief", "leaving_belief", "enacted_discovery")))
    if len(set(task_ids)) != 6 or len(set(raw_ids)) != 6 or len(set(transitions)) != 3:
        raise BlindError("absolute diagnostic identities or treatment transitions are stale")
    panels, panel_ids = [], []
    for panel in task_bundle["gsbs_panels"]:
        rows = []
        for item in panel["readers"]:
            task, name = PE.h_f01_judge_task(item["envelope"]), f"{panel['key']}-{item['identity']}"
            record = PANEL.records(view["config"], name, task, identities=(item["identity"],),
                tested_pair_hash=task_bundle["experiment_sha256"], single=True)[0]
            call = read(base / "native/calls" / f"gsbs-{name}.json")
            if call.get("authority_sha256") != task_bundle["authority_sha256"] \
                    or (record["raw_verdict_id"], record["raw_verdict"]) != (call.get("thread_id"), call.get("raw")):
                raise BlindError(f"{name}: GSBS native authority or result binding is stale")
            panel_ids.append(record["raw_verdict_id"])
            rows.append({**PANEL.h_f01_decision_row(view["config"], record, item["envelope"],
                task_bundle["experiment_sha256"]), "authority_sha256": task_bundle["authority_sha256"],
                "native_call_sha256": PS.sha(PS.json_bytes(call))})
        panels.append(rows)
    if len(set(raw_ids + panel_ids)) != 14: raise BlindError("blind observations require fourteen fresh native contexts")
    if judges.judging_dir(view["config"], carr_name).exists() or Path(view["config"]["scores_dir"]).exists():
        raise BlindError("Carr diagnostic predates frozen blind evidence")
    body = {"schema": 2, "frozen_at_utc": now(), "authority_sha256": task_bundle["authority_sha256"],
        "upstream_receipt_sha256": task_bundle["upstream_receipt_sha256"],
        "task_bundle_sha256": task_bundle["task_bundle_sha256"], "control_pair_hash": task_bundle["control_pair_hash"],
        "treatment_pair_hash": task_bundle["treatment_pair_hash"], "experiment_sha256": task_bundle["experiment_sha256"],
        "gsbs_matches": task_bundle["gsbs_matches"], "gsbs_sha256": task_bundle["gsbs_sha256"],
        "gsbs_panel_sha256": task_bundle["gsbs_panel_sha256"], "integrity": task_bundle["integrity"],
        "control_treatment_causal_diagnostic": {"role": "DIAGNOSTIC_ONLY", "status": "PASS",
            "task_ids": task_ids, "raw_verdict_ids": raw_ids, "arms": diagnostic},
        "gsbs_chapter_panels": panels[:3], "gsbs_whole_opening_panel": panels[3]}
    return write(base / RECEIPT, {**body, "receipt_hash": PS.state_hash(body)})
