"""One resumable H-F01 coordinator from frozen authority to gate continuation."""
import datetime as dt, os, shlex, sys
from pathlib import Path
HERE = Path(__file__).resolve(); sys.path[:0] = [str(HERE.parent), str(HERE.parents[1] / "eval")]
import candidate_pair as CP  # noqa: E402
import developmental_review as DR  # noqa: E402
import experiment_record as ER  # noqa: E402
import grounded_review as GR  # noqa: E402
import hf01_blind as BLIND  # noqa: E402
import hf01_carr as CARR_NATIVE  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import judges  # noqa: E402
import pair_store as PS  # noqa: E402
import product_decision as PD  # noqa: E402
import score_core  # noqa: E402
import score_receipt  # noqa: E402
FOLDER, TASKS, RECEIPT = BLIND.FOLDER, BLIND.TASKS, BLIND.RECEIPT
CARR, HUMAN = "carr-diagnostic.json", "human-approval.json"
UNSUPPORTED = {"invention", "inference broadening"}
class StageError(RuntimeError): pass
class StagePending(StageError):
    def __init__(self, boundary, commands, resume):
        self.boundary, self.commands, self.resume = boundary, commands, resume
        super().__init__(f"H-F01 pending at {boundary}")
def folder(root): return BLIND.folder(root)
def _read(path):
    try: return BLIND.read(path)
    except BLIND.BlindError as exc: raise StageError(str(exc)) from exc
def _write(path, value):
    try: return BLIND.write(path, value)
    except BLIND.BlindError as exc: raise StageError(str(exc)) from exc
def _time(value, label):
    try: parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc: raise StageError(f"{label} must be UTC ISO-8601") from exc
    if parsed.utcoffset() != dt.timedelta(0): raise StageError(f"{label} must be UTC ISO-8601")
    return parsed
def carr_iteration(manifest):
    value = manifest["run"]["iteration_id"]
    if not isinstance(value, int): raise StageError("H-F01 Carr/gate iteration must be one integer")
    return f"{value:03d}"
def _review(root, authority, native=False):
    commands = []
    for arm, paths in HF.arm_paths(root).items():
        runner = None
        if native:
            import native_grounded_review as NGR
            runner = lambda dispatch: NGR.complete(dispatch["workdir"], dispatch["marker_path"],
                                                     dispatch["transport_path"], dispatch["raw_path"])
        try: GR.require_complete(paths["experiment"])
        except GR.GroundedReviewError:
            try: GR.advance(paths["experiment"], runner=runner)
            except GR.GroundedReviewPending as exc:
                commands.extend(shlex.join(GR.GC.wrapper_command(paths["experiment"], n)) for n in exc.missing)
            except GR.GroundedReviewError as exc: raise StageError(f"{arm} grounded: {exc}") from exc
    if commands: raise StagePending("all-six-grounded-review", commands, HF.resume_command(authority, stage="RF-23"))
    for arm, paths in HF.arm_paths(root).items():
        runner = None
        if native:
            import native_developmental_review as NDR
            runner = lambda dispatch: NDR.complete(dispatch["task_sha256"])
        try: DR.require_developmental_pass(paths["experiment"])
        except DR.DevelopmentalReviewError:
            try: DR.advance(paths["experiment"], runner=runner)
            except DR.DevelopmentalReviewPending:
                task, _ = DR._authority(paths["experiment"]); commands.append(shlex.join(DR.DC.wrapper_command(task)))
            except DR.DevelopmentalReviewError as exc: raise StageError(f"{arm} developmental: {exc}") from exc
    if commands: raise StagePending("both-whole-opening-reviews", commands, HF.resume_command(authority, stage="RF-23"))
def _unsupported(receipt):
    return sum(finding.get("classification") in UNSUPPORTED for chapter in receipt["chapters"]
               for finding in chapter["verdict"]["findings"])
def _sealed(root):
    hashes, integrity = {}, {"status": "PASS", "arms": {}}
    for arm, paths in HF.arm_paths(root).items():
        grounded = GR.require_complete(paths["experiment"]); manifest = CP.load(paths["experiment"])
        tested = manifest.get("tested_hash") if manifest["state"] == "SEALED" else CP.seal(paths["experiment"])
        view = CP.open_sealed(paths["experiment"], tested)
        core = score_core.evaluate(view["config"], view["pair"] / HF.BOOK, "1-3", False)
        row = {"tested_pair_hash": tested, "hard_ok": core["hard_ok"],
               "hard_fails": core["hard_fails"], "checks": core["checks"],
               "grounded_receipt_hash": grounded["receipt_hash"],
               "unsupported_claims": _unsupported(grounded)}
        hashes[arm], integrity["arms"][arm] = tested, row
        if not core["hard_ok"]: integrity["status"] = "FAIL"
    control, treatment = (integrity["arms"][arm]["unsupported_claims"] for arm in ("control", "treatment"))
    integrity["unsupported_claim_comparison"] = {"control": control, "treatment": treatment,
        "increased": treatment > control, "grounded_receipt_hashes": {
            arm: integrity["arms"][arm]["grounded_receipt_hash"] for arm in ("control", "treatment")}}
    if treatment > control: integrity["status"] = "FAIL"
    if integrity["status"] != "PASS": raise StageError("H-F01 integrity or unsupported-claim gate failed")
    return hashes, integrity
def _carr(root, task_bundle, blind, view, authority, native):
    core = score_core.evaluate(view["config"], view["pair"] / HF.BOOK, "1-3", False)
    labels, name = [row[0] for row in core["pairs"]], carr_iteration(view["manifest"])
    treatment = HF.arm_paths(root)["treatment"]["experiment"]
    if judges.missing_verdicts(view["config"], labels, name, task_bundle["treatment_pair_hash"], treatment):
        rubric = Path(view["config"]["judge_rubric"]).read_text(encoding="utf-8")
        judges.emit_tasks(view["config"], core["pairs"], name, rubric, treatment,
                          task_bundle["treatment_pair_hash"])
    try:
        native_receipt = (CARR_NATIVE.dispatch if native else CARR_NATIVE.verify)(root, view["config"],
            labels, name, task_bundle["treatment_pair_hash"], blind)
    except CARR_NATIVE.CarrPending as exc:
        raise StagePending("post-blind-carr-diagnostic",
            [HF.resume_command(authority, stage="RF-23", native=True)],
            HF.resume_command(authority, stage="RF-23")) from exc
    except CARR_NATIVE.CarrError as exc: raise StageError(str(exc)) from exc
    aggregate = judges.aggregate(view["config"], labels, name, task_bundle["treatment_pair_hash"], treatment)
    artifacts = score_receipt.judge_artifacts(view["config"], labels, name,
                                               task_bundle["treatment_pair_hash"], treatment)
    core.update(pair_root=view["pair"], evaluation_root=view["evaluation"],
                rubric_sha256=PS.sha(Path(view["config"]["judge_rubric"]).read_bytes()))
    score_receipt_value = score_receipt.build(view["manifest"], core, aggregate, artifacts)
    score = {"tested_pair_hash": task_bundle["treatment_pair_hash"], "book": str(view["pair"] / HF.BOOK),
         "hard_ok": core["hard_ok"], "hard_fails": core["hard_fails"], "reward": aggregate["reward"],
         "campaign": view["config"].get("campaign"), "instrument_version": view["config"].get("instrument_version"),
         "judges": {"rubric": aggregate}, "receipt": score_receipt_value}
    _write(Path(view["config"]["scores_dir"]) / f"iter-{name}.json", score)
    path = folder(root) / CARR
    if path.is_file():
        stored = _read(path)
        if set(stored) != {"schema", "iteration", "completed_at_utc", "blind_receipt_sha256",
                "native_receipt_sha256", "aggregate", "score_receipt"} or stored.get("schema") != 3 \
                or stored.get("iteration") != name \
                or stored.get("blind_receipt_sha256") != PS.sha(PS.json_bytes(blind)) \
                or stored.get("native_receipt_sha256") != native_receipt["receipt_hash"] \
                or stored.get("aggregate") != aggregate \
                or stored.get("score_receipt") != score_receipt_value \
                or _time(stored.get("completed_at_utc"), "Carr completion") < _time(
                    native_receipt["calls"][-1]["completed_at_utc"], "Carr native completion"):
            raise StageError("Carr diagnostic identity is stale")
        return stored
    completed = BLIND.now()
    if _time(completed, "Carr completion") < _time(
            native_receipt["calls"][-1]["completed_at_utc"], "Carr native completion"):
        raise StageError("Carr diagnostic must follow the final native call")
    return _write(path, {"schema": 3, "iteration": name,
        "completed_at_utc": completed, "blind_receipt_sha256": PS.sha(PS.json_bytes(blind)),
        "native_receipt_sha256": native_receipt["receipt_hash"],
        "aggregate": aggregate, "score_receipt": score["receipt"]})
def _decision_context(task_bundle, blind, carr, prompt_sha256):
    reference = PS.sha(PS.json_bytes(carr)); frozen = PS.sha(PS.json_bytes(blind))
    value = {"control_pair_hash": task_bundle["control_pair_hash"],
        "treatment_pair_hash": task_bundle["treatment_pair_hash"], "gsbs_sha256": task_bundle["gsbs_sha256"],
        "gsbs_panel_sha256": task_bundle["gsbs_panel_sha256"], "prompt_sha256": prompt_sha256,
        "blind_receipt_sha256": frozen, "reference_sighted_diagnostic_sha256": reference}
    return PS.state_hash(value), reference
def _human(root, task_bundle, blind, carr, prompt_sha256):
    value = _read(folder(root) / HUMAN)
    fields = {"schema", "reviewer", "verdict", "reviewed_at_utc", "control_pair_hash",
              "treatment_pair_hash", "gsbs_sha256", "blind_receipt_sha256",
              "reference_sighted_diagnostic_sha256", "decision_context_sha256"}
    context, reference = _decision_context(task_bundle, blind, carr, prompt_sha256)
    if set(value) != fields or value.get("schema") != 2 or len(str(value.get("reviewer", "")).split()) < 2 \
            or value.get("verdict") not in {"APPROVE", "REJECT"} \
            or value.get("control_pair_hash") != task_bundle["control_pair_hash"] \
            or value.get("treatment_pair_hash") != task_bundle["treatment_pair_hash"] \
            or value.get("gsbs_sha256") != task_bundle["gsbs_sha256"] \
            or value.get("blind_receipt_sha256") != PS.sha(PS.json_bytes(blind)) \
            or value.get("reference_sighted_diagnostic_sha256") != reference \
            or value.get("decision_context_sha256") != context \
            or _time(carr["completed_at_utc"], "Carr completion") <= _time(blind["frozen_at_utc"], "blind freeze") \
            or _time(value.get("reviewed_at_utc"), "human review") <= _time(carr["completed_at_utc"], "Carr completion"):
        raise StageError("named-human receipt hashes or chronology are invalid")
    return {**value, "receipt_sha256": PS.sha(PS.json_bytes(value))}
def recompute(root, carr_aggregate=None):
    base, task_bundle, blind = folder(root), _read(folder(root) / TASKS), _read(folder(root) / RECEIPT)
    task_body = {key: value for key, value in task_bundle.items() if key != "task_bundle_sha256"}
    if task_bundle.get("task_bundle_sha256") != PS.state_hash(task_body) \
            or blind.get("task_bundle_sha256") != task_bundle.get("task_bundle_sha256") \
            or blind.get("authority_sha256") != task_bundle.get("authority_sha256"):
        raise StageError("blind task bundle identity is stale")
    body = {key: value for key, value in blind.items() if key != "receipt_hash"}
    if blind.get("receipt_hash") != PS.state_hash(body): raise StageError("blind evidence receipt is stale")
    carr = _read(base / CARR); view = CP.open_sealed(HF.arm_paths(root)["treatment"]["experiment"],
        task_bundle["treatment_pair_hash"]); manifest = view["manifest"]
    core = score_core.evaluate(view["config"], view["pair"] / HF.BOOK, "1-3", False)
    try: native = CARR_NATIVE.verify(root, view["config"], [row[0] for row in core["pairs"]],
        carr_iteration(manifest), task_bundle["treatment_pair_hash"], blind)
    except CARR_NATIVE.CarrError as exc: raise StageError(str(exc)) from exc
    if carr.get("schema") != 3 or carr.get("iteration") != carr_iteration(manifest) \
            or carr.get("blind_receipt_sha256") != PS.sha(PS.json_bytes(blind)) \
            or carr.get("native_receipt_sha256") != native["receipt_hash"] \
            or _time(carr.get("completed_at_utc"), "Carr completion") < _time(
                native["calls"][-1]["completed_at_utc"], "Carr native completion") \
            or carr_aggregate is not None and carr.get("aggregate") != carr_aggregate:
        raise StageError("Carr diagnostic identity or blind binding is stale")
    prompt = CP.open_sealed(HF.arm_paths(root)["treatment"]["experiment"],
        task_bundle["treatment_pair_hash"])["config"]["product_effect_rubric"]
    prompt_sha = PS.sha(Path(prompt).read_bytes()); human = _human(root, task_bundle, blind, carr, prompt_sha)
    context, reference = _decision_context(task_bundle, blind, carr, prompt_sha)
    return PD.decide_hf01(integrity=blind["integrity"],
        causal_diagnostic=blind["control_treatment_causal_diagnostic"],
        chapter_panels=blind["gsbs_chapter_panels"], whole_opening_panel=blind["gsbs_whole_opening_panel"],
        carr_craft=carr["aggregate"], human_approval=human,
        control_pair_hash=task_bundle["control_pair_hash"], treatment_pair_hash=task_bundle["treatment_pair_hash"],
        gsbs_sha256=task_bundle["gsbs_sha256"], gsbs_panel_sha256=task_bundle["gsbs_panel_sha256"],
        prompt_sha256=prompt_sha, blind_receipt_sha256=PS.sha(PS.json_bytes(blind)),
        reference_sighted_diagnostic_sha256=reference, decision_context_sha256=context)
def gate_product(root, carr, product_path, record_path):
    product = recompute(root, carr)
    if _read(product_path) != product: raise StageError("stored H-F01 product decision differs")
    prereg = _read(folder(root) / "authority.json")["preregistration"]
    return product, ER.bind(ER.load_one(record_path), product, product["tested_pair_hash"],
                            PS.state_hash(product), prereg)
def gate_command(root, task_bundle, timestamp, promote):
    treatment = HF.arm_paths(root)["treatment"]["experiment"]
    manifest = CP.open_sealed(treatment, task_bundle["treatment_pair_hash"])["manifest"]
    command = [sys.executable, "scripts/loop/gate.py", "--iter", str(manifest["run"]["iteration_id"]),
        "--config", str(HF.arm_paths(root)["treatment"]["candidate"] / "loop/config.yaml"),
        "--tested-pair-hash", task_bundle["treatment_pair_hash"], "--accepted-root", str(Path(root).absolute()),
        "--decision-timestamp", timestamp, "--redesign-authorized", "--rf-stage", "RF-25",
        "--candidate-root", str(treatment)]
    if promote: command.append("--promote-pair")
    return shlex.join(command)
def advance(root, authority, upstream_sha, native=False, decision_timestamp=None, promote_pair=False):
    _review(root, authority, native); hashes, integrity = _sealed(root)
    try:
        task_bundle = BLIND.bundle(root, hashes, integrity, authority, upstream_sha)
        view = BLIND.emit(root, task_bundle, authority, native)
        blind = _read(folder(root) / RECEIPT) if (folder(root) / RECEIPT).is_file() \
            else BLIND.freeze(root, task_bundle, view, carr_iteration(view["manifest"]))
    except BLIND.BlindPending as exc: raise StagePending("blind-native-dispatch", exc.commands, HF.resume_command(authority, stage="RF-23")) from exc
    except BLIND.BlindError as exc: raise StageError(str(exc)) from exc
    carr = _carr(root, task_bundle, blind, view, authority, native)
    if not (folder(root) / HUMAN).is_file():
        raise StagePending("named-human-reading", [str(folder(root) / HUMAN)], HF.resume_command(authority, stage="RF-23"))
    product = recompute(root, carr["aggregate"]); treatment = HF.arm_paths(root)["treatment"]["experiment"]
    _write(treatment / "evidence" / PD.PATH, product); prereg = authority["preregistration"]
    inputs = {**prereg["inputs"], "control_tested_pair_hash": hashes["control"],
        "tested_pair_hash": hashes["treatment"], "blind_receipt_sha256": product["blind_receipt_sha256"],
        "product_decision_sha256": PS.state_hash(product)}
    record = {**{key: prereg[key] for key in prereg if key != "inputs"}, "inputs": inputs,
        "evidence": ER.decision_evidence(product), "decision": {"PROMOTE": "SUPPORTED",
        "REJECT": "REFUTED", "INCONCLUSIVE": "INCONCLUSIVE"}[product["decision"]]}
    ER.bind(record, product, hashes["treatment"], PS.state_hash(product), prereg)
    _write(treatment / "evidence" / ER.PATH, record)
    required = product["decision"] == "PROMOTE"
    if not decision_timestamp or required and not promote_pair:
        template = gate_command(root, task_bundle, decision_timestamp or "<UTC_ISO_8601>", required)
        raise StagePending("explicit-atomic-gate-authority", [template], HF.resume_command(authority, stage="RF-23"))
    human = _read(folder(root) / HUMAN)
    if _time(decision_timestamp, "gate timestamp") <= _time(human["reviewed_at_utc"], "human review"):
        raise StageError("gate timestamp must follow named-human approval")
    if promote_pair and not required: raise StageError("promotion authority is invalid for a non-PROMOTE decision")
    return {"schema": 1, "state": "ATOMIC_GATE_COMMAND_EMITTED", "decision": product["decision"],
            "gate_command": gate_command(root, task_bundle, decision_timestamp, promote_pair),
            "control_pair_hash": hashes["control"], "treatment_pair_hash": hashes["treatment"]}
