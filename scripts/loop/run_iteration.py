"""Run, score, and gate one candidate iteration."""
import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "eval"))
sys.path.insert(0, str(HERE.parent))
import model_endpoint as ME   # noqa: E402
import loopcfg               # noqa: E402
import judges                # noqa: E402
import score_core            # noqa: E402
import legacy_guard as LG     # noqa: E402
import candidate_pair as CP   # noqa: E402
import pair_store as PS        # noqa: E402
import manual_dispatch as MD    # noqa: E402
import commission_set as CS     # noqa: E402
import writer_context as WC     # noqa: E402
import draft_batch_runtime as BR  # noqa: E402
import first_draft_batch as FB     # noqa: E402
import grounded_review as GR       # noqa: E402
import developmental_review as DR  # noqa: E402
import experiment_record as ER  # noqa: E402
import product_decision as PD  # noqa: E402
write_chapters = BR.write_chapters
def run_step(cmd, cwd=None):
    print(f"[run] $ {' '.join(cmd)}")
    return subprocess.run(cmd, check=False, cwd=cwd).returncode


def _prepare_research_arms(declaration, accepted_root, book, chapters, iteration, RF):
    """Create or resume two RF-02 arms and apply only the declared research text."""
    accepted = Path(accepted_root).absolute()
    inputs = declaration["inputs"]
    roots = {name: Path(inputs[f"{name}_candidate_root"]).absolute()
             for name in ("control", "treatment")}
    experiments = accepted / "loop" / "experiments"
    for name, root in roots.items():
        if root.parent != experiments or root == accepted:
            raise SystemExit(f"[run] {name} research arm is outside the authorized RF-02 root")
        try:
            if not os.path.lexists(root):
                PS.ensure_dir(root, accepted)
            if not os.path.lexists(root / CP.MANIFEST):
                CP.snapshot(root, accepted, book, chapters, iteration=iteration)
            manifest = CP.load(root)
            CP.assert_run(root, manifest, book, chapters, iteration,
                          manifest["run"]["config"])
        except (CP.PairError, PS.StoreError, OSError) as exc:
            raise SystemExit(f"[run] {name} RF-02 research arm blocked: {exc}") from exc
    try:
        control_preflight = RF.require_control_baseline(str(roots["control"]))
    except RF.ResearchFactoryError as exc:
        raise SystemExit(f"[run] control research baseline is invalid: {exc}") from exc
    components = control_preflight.get("research_bundle", {}).get("components", {})
    for relative, text_value in declaration["research_bundle"].items():
        if relative not in components:
            raise SystemExit(f"[run] changed research component is absent: {relative}")
        manifest = CP.load(roots["treatment"])
        target = CP.candidate_path(roots["treatment"], relative)
        control_path = CP.require_member(roots["control"],
            CP.candidate_path(roots["control"], relative), "config")
        treatment_path = CP.require_member(roots["treatment"], target, "config", manifest)
        desired = text_value.encode("utf-8")
        current = treatment_path.read_bytes()
        if current not in {control_path.read_bytes(), desired}:
            raise SystemExit(f"[run] treatment research component has undeclared drift: {relative}")
        if current != desired:
            PS.write(treatment_path, desired)
    return roots


def _research_preflight_identity(declaration, roots, RF):
    """Prove frozen actual bytes and the exact research-only delta before dispatch."""
    try:
        control = RF.require_control_baseline(str(roots["control"]))
        identities = {"control": control,
                      "treatment": RF.preflight(str(roots["treatment"]))}
    except RF.ResearchFactoryError as exc:
        raise SystemExit(f"[run] control research baseline is invalid: {exc}") from exc
    expected = declaration["frozen_variables"]
    for name, identity in identities.items():
        actual = identity.get("frozen_variables")
        if actual != expected:
            mismatch = sorted(set(expected) | set(actual or {}))
            mismatch = next((key for key in mismatch
                             if (actual or {}).get(key) != expected.get(key)), "unknown")
            raise SystemExit(f"[run] {name} actual frozen {mismatch} hash differs")
    control_run = dict(identities["control"].get("run", {}))
    treatment_run = dict(identities["treatment"].get("run", {}))
    control_run.pop("experiment_id", None); treatment_run.pop("experiment_id", None)
    if identities["control"].get("accepted_generation") != \
            identities["treatment"].get("accepted_generation") \
            or control_run != treatment_run:
        raise SystemExit("[run] research arms do not share one accepted RF-02 input identity")
    control = identities["control"].get("research_bundle", {}).get("components", {})
    treatment = identities["treatment"].get("research_bundle", {}).get("components", {})
    if set(control) != set(treatment):
        raise SystemExit("[run] research bundle component inventory differs across arms")
    editor = "prompts/research-evidence-editor.md"
    if control.get(editor) != treatment.get(editor):
        raise SystemExit("[run] independent evidence editor must remain frozen across research arms")
    actual_delta = {name for name in control if control[name] != treatment[name]}
    declared_delta = {item.split(":", 1)[1] for item in declaration["changed_bundle"]}
    if actual_delta != declared_delta:
        raise SystemExit("[run] actual research bundle delta differs from its declaration")
    return identities


def _research_hard_gates(roots, seals, RF):
    """Derive compact hard-gate evidence only from current production validation."""
    reports, anchors = {}, {}
    for name, root in roots.items():
        identity = RF.preflight(str(root))
        book = CP.candidate_tree(root) / identity["run"]["book"]
        report = RF.RC.inspect_research(book, require_seal=True)
        if not report.get("ok") or report.get("seal_identity") != seals[name]:
            raise SystemExit(f"[run] {name} research hard gates did not validate")
        reports[name] = report
        anchors[name] = {"seal_sha256": seals[name],
            "coverage_sha256": PS.sha((book / "research/research-coverage.json").read_bytes()),
            "review_sha256": PS.sha((book / "research/research-review.json").read_bytes())}
    gate_hashes = {gate: PS.state_hash({"gate": gate, "arms": anchors})
                   for gate in sorted(ER.RESEARCH_HARD_GATES)}
    return {"schema": 1, "control_seal_sha256": seals["control"],
            "treatment_seal_sha256": seals["treatment"], "gates": gate_hashes}, reports


def _research_comparison(declaration, roots, identities, seals, complete=None):
    """Persist one anonymous, task-hash-bound fresh native research comparison."""
    import native_judge as N
    candidates = {"A": ER.research_candidate(
        CP.candidate_tree(roots["control"]) / identities["control"]["run"]["book"]),
        "B": ER.research_candidate(
        CP.candidate_tree(roots["treatment"]) / identities["treatment"]["run"]["book"])}
    task = ER.research_comparison_task(
        declaration, {"A": seals["control"], "B": seals["treatment"]}, candidates)
    treatment_candidate = "B"
    base = roots["treatment"] / "evidence" / "research-causal"
    marker_path, result_path = base / "comparison.marker.json", base / "comparison.result.json"
    marker = {"schema": 1, "task_sha256": task["task_sha256"],
              "treatment_candidate": treatment_candidate, "task": task}
    schema = ER.research_comparison_schema()
    prompt = ER.research_comparison_prompt(task)
    native_binding = {
        "kind": "native-codex-subscription",
        "judge_identity": "research-quality-independent",
        "fresh_ephemeral_context": True,
        "input_sha256": PS.sha(prompt.encode()),
        "output_schema_sha256": PS.sha(ER.research_comparison_schema_bytes()),
    }
    if os.path.lexists(marker_path):
        if json.loads(PS._safe_file(marker_path, roots["treatment"]).read_text(
                encoding="utf-8")) != marker:
            raise SystemExit("[run] research comparison marker is stale")
        if not os.path.lexists(result_path):
            raise SystemExit("[run] research comparison outcome is ambiguous; do not replay")
        result = json.loads(PS._safe_file(result_path, roots["treatment"]).read_text(
            encoding="utf-8"))
    else:
        PS.ensure_dir(base, roots["treatment"])
        PS.write_json(marker_path, marker)
        raw, transport, error = (complete or N.complete)(
            prompt, "research-quality-independent", schema,
            model=ER.RESEARCH_JUDGE_MODEL, reasoning=ER.RESEARCH_JUDGE_REASONING)
        if error:
            raise SystemExit(f"[run] research comparison blocked: {error}")
        try:
            verdict = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit("[run] research comparison verdict is not JSON") from exc
        try:
            ER.validate_research_comparison_verdict(task, verdict)
        except ER.RecordError as exc:
            raise SystemExit("[run] research comparison verdict is stale") from exc
        if transport.get("model") != ER.RESEARCH_JUDGE_MODEL \
                or transport.get("reasoning_effort") != ER.RESEARCH_JUDGE_REASONING \
                or any(transport.get(key) != value
                       for key, value in native_binding.items()) \
                or not transport.get("thread_id"):
            raise SystemExit("[run] research comparison verdict or native binding is stale")
        native = {"task_sha256": task["task_sha256"], "verdict": verdict,
            "model": transport["model"], "reasoning": transport["reasoning_effort"],
            "thread_id": transport["thread_id"], "command": transport.get("command"),
            **native_binding}
        result = {"schema": 1, "task_sha256": task["task_sha256"],
                  "native": native, "native_record_sha256": PS.state_hash(native)}
        PS.write_json(result_path, result)
    verdict = result.get("native", {}).get("verdict", {})
    stored_binding = {key: result.get("native", {}).get(key)
                      for key in native_binding}
    try:
        ER.validate_research_comparison_verdict(task, verdict)
    except ER.RecordError as exc:
        raise SystemExit("[run] durable research comparison result is stale") from exc
    if result.get("schema") != 1 or result.get("task_sha256") != task["task_sha256"] \
            or result.get("native_record_sha256") != PS.state_hash(result.get("native", {})) \
            or stored_binding != native_binding \
            or verdict.get("task_sha256") != task["task_sha256"]:
        raise SystemExit("[run] durable research comparison result is stale")
    receipt = {"schema": 1, "task_sha256": task["task_sha256"],
        "preferred": verdict["preferred"], "treatment_candidate": treatment_candidate,
        "hypothesis_outcome": ER.research_hypothesis_outcome(
            verdict["preferred"], treatment_candidate),
        "verdict_sha256": PS.state_hash(verdict),
        "native_record_sha256": result["native_record_sha256"],
        "native_binding": native_binding}
    return receipt


def _downstream_arms(declaration, roots, seals, RF):
    """Hard-gate two sealed downstream outcomes under identical process variables."""
    pair_hashes, hard_gates, candidates = {}, {}, {}
    chapters = None
    for name, label in (("control", "A"), ("treatment", "B")):
        root = roots[name]
        try:
            manifest = CP.load(root)
            tested = manifest.get("tested_hash")
            if manifest.get("state") != "SEALED" or ER.SHA256.fullmatch(
                    str(tested or "")) is None:
                raise CP.PairError(f"downstream {name} is not sealed")
            view = CP.open_sealed(root, tested)
            identity = (RF.require_control_baseline(str(root)) if name == "control"
                        else RF.preflight(str(root)))
            if identity["frozen_variables"] != declaration["frozen_variables"]:
                raise ER.RecordError(f"downstream {name} process variables drifted")
            book = view["pair"] / manifest["run"]["book"]
            if RF.RC.research_seal_identity(book) != seals[name]:
                raise ER.RecordError(f"downstream {name} research seal drifted")
            FB.require_frozen_batch(root)
            grounded = GR.require_complete(root)
            developmental = DR.require_developmental_pass(root)
            current_chapters = manifest["run"]["chapters"]
            if chapters is None:
                chapters = current_chapters
            elif current_chapters != chapters:
                raise ER.RecordError("downstream arms use different chapter scopes")
            core = score_core.evaluate(
                view["config"], str(book), ",".join(map(str, current_chapters)), False)
            if not core.get("hard_ok"):
                raise ER.RecordError(f"downstream {name} integrity hard gate failed")
            gate = {"tested_pair_hash": tested, "research_seal_sha256": seals[name],
                "core_sha256": PS.state_hash(core),
                "grounded_review_sha256": PS.state_hash(grounded),
                "developmental_review_sha256": PS.state_hash(developmental)}
            pair_hashes[label] = tested
            hard_gates[label] = PS.state_hash(gate)
            candidates[label] = ER.research_downstream_candidate(
                book, current_chapters)
        except (CP.PairError, PS.StoreError, RF.ResearchFactoryError,
                RF.RC.ContractError, FB.BatchError, GR.GroundedReviewError,
                DR.DevelopmentalReviewError, ER.RecordError, OSError,
                UnicodeError, KeyError, TypeError) as exc:
            raise SystemExit(f"[run] downstream {name} hard gates failed: {exc}") from exc
    contract = ER.research_downstream_contract(chapters)
    task = ER.research_downstream_task(declaration, contract, pair_hashes,
        {"A": seals["control"], "B": seals["treatment"]}, hard_gates, candidates)
    return contract, task, pair_hashes, hard_gates


def _downstream_comparison(declaration, roots, seals, complete=None):
    """Run or revalidate one fresh anonymous downstream A/B judgment."""
    import research_factory as RF
    import native_judge as N
    contract, task, pair_hashes, hard_gates = _downstream_arms(
        declaration, roots, seals, RF)
    base = roots["treatment"] / "evidence" / "research-causal"
    marker_path = base / "downstream.marker.json"
    result_path = base / "downstream.result.json"
    marker = {"schema": 1, "task_sha256": task["task_sha256"],
              "treatment_candidate": "B", "task": task}
    prompt = ER.research_comparison_prompt(task)
    binding = {"kind": "native-codex-subscription",
        "judge_identity": "research-downstream-effect-independent",
        "fresh_ephemeral_context": True, "input_sha256": PS.sha(prompt.encode()),
        "output_schema_sha256": PS.sha(ER.research_comparison_schema_bytes())}
    if os.path.lexists(marker_path):
        if json.loads(PS._safe_file(marker_path, roots["treatment"]).read_text(
                encoding="utf-8")) != marker:
            raise SystemExit("[run] downstream comparison marker is stale")
        if not os.path.lexists(result_path):
            raise SystemExit("[run] downstream comparison outcome is ambiguous; do not replay")
        result = json.loads(PS._safe_file(result_path, roots["treatment"]).read_text(
            encoding="utf-8"))
    else:
        if complete is False:
            raise SystemExit("[run] preregistered downstream-effect receipt is pending")
        PS.ensure_dir(base, roots["treatment"])
        PS.write_json(marker_path, marker)
        raw, transport, error = (complete or N.complete)(prompt,
            "research-downstream-effect-independent",
            ER.research_comparison_schema(), model=ER.RESEARCH_JUDGE_MODEL,
            reasoning=ER.RESEARCH_JUDGE_REASONING)
        if error:
            raise SystemExit(f"[run] downstream comparison blocked: {error}")
        try:
            verdict = json.loads(raw)
            ER.validate_research_comparison_verdict(task, verdict)
        except (json.JSONDecodeError, ER.RecordError) as exc:
            raise SystemExit("[run] downstream comparison verdict is stale") from exc
        if transport.get("model") != ER.RESEARCH_JUDGE_MODEL \
                or transport.get("reasoning_effort") != ER.RESEARCH_JUDGE_REASONING \
                or any(transport.get(key) != value for key, value in binding.items()) \
                or not transport.get("thread_id"):
            raise SystemExit("[run] downstream native binding is stale")
        native = {"task_sha256": task["task_sha256"], "verdict": verdict,
            "model": transport["model"], "reasoning": transport["reasoning_effort"],
            "thread_id": transport["thread_id"], "command": transport.get("command"),
            **binding}
        result = {"schema": 1, "task_sha256": task["task_sha256"],
                  "native": native, "native_record_sha256": PS.state_hash(native)}
        PS.write_json(result_path, result)
    native = result.get("native", {})
    verdict = native.get("verdict", {}) if isinstance(native, dict) else {}
    try:
        ER.validate_research_comparison_verdict(task, verdict)
    except ER.RecordError as exc:
        raise SystemExit("[run] durable downstream comparison is stale") from exc
    stored_binding = {key: native.get(key) for key in binding}
    if result != {"schema": 1, "task_sha256": task["task_sha256"],
                  "native": native, "native_record_sha256": PS.state_hash(native)} \
            or stored_binding != binding \
            or native.get("model") != ER.RESEARCH_JUDGE_MODEL \
            or native.get("reasoning") != ER.RESEARCH_JUDGE_REASONING \
            or not native.get("thread_id") or not native.get("command"):
        raise SystemExit("[run] durable downstream comparison is stale")
    outcome = ER.research_hypothesis_outcome(verdict["preferred"], "B")
    return {"schema": 1, "task_sha256": contract["contract_sha256"],
        "comparison_task_sha256": task["task_sha256"],
        "status": "PASS" if outcome == "SUPPORTED" else "BLOCKED",
        "preferred": verdict["preferred"], "treatment_candidate": "B",
        "hypothesis_outcome": outcome,
        "frozen_writing_sha256": declaration["frozen_variables"]["writing"],
        "control_seal_sha256": seals["control"],
        "treatment_seal_sha256": seals["treatment"],
        "control_pair_hash": pair_hashes["A"],
        "treatment_pair_hash": pair_hashes["B"],
        "hard_gate_sha256": hard_gates,
        "verdict_sha256": PS.state_hash(verdict),
        "native_record_sha256": result["native_record_sha256"],
        "native_binding": binding}


def _downstream_effect_receipt(declaration, roots, seals):
    """Revalidate a required effect against the canonical sealed product."""
    spec = declaration["downstream_effect"]
    if not spec["required"]:
        return None
    receipt_path = Path(spec["receipt_path"]).absolute()
    if roots["treatment"] not in receipt_path.parents or not receipt_path.is_file():
        raise SystemExit("[run] preregistered downstream-effect receipt is pending")
    try:
        receipt = json.loads(PS._safe_file(
            receipt_path, roots["treatment"]).read_text(encoding="utf-8"))
    except (PS.StoreError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit("[run] preregistered downstream-effect receipt is malformed") from exc
    expected = _downstream_comparison(declaration, roots, seals, complete=False)
    if receipt != expected or expected["status"] != "PASS":
        raise SystemExit("[run] preregistered downstream-effect receipt is stale or blocking")
    return receipt


def _bind_downstream_effect(path, accepted_root):
    """Blindly compare two completed, hard-gated downstream arm outcomes."""
    try:
        declaration = json.loads(Path(path).read_text(encoding="utf-8"))
        ER.validate_research_treatment(declaration)
    except (OSError, json.JSONDecodeError, ER.RecordError) as exc:
        raise SystemExit(f"[run] downstream-effect declaration blocked: {exc}") from exc
    spec = declaration["downstream_effect"]
    if not spec["required"]:
        raise SystemExit("[run] downstream-effect binding was not preregistered")
    accepted = Path(accepted_root).absolute()
    roots = {name: Path(declaration["inputs"][f"{name}_candidate_root"]).absolute()
             for name in ("control", "treatment")}
    if any(root.parent != accepted / "loop/experiments" for root in roots.values()):
        raise SystemExit("[run] downstream-effect arms escape the accepted RF-02 store")
    import research_factory as RF
    seals = {}
    try:
        for name, root in roots.items():
            identity = (RF.require_control_baseline(str(root)) if name == "control"
                        else RF.preflight(str(root)))
            if identity["frozen_variables"] != declaration["frozen_variables"]:
                raise SystemExit(f"[run] downstream {name} arm differs from frozen variables")
            book = CP.candidate_tree(root) / identity["run"]["book"]
            seals[name] = RF.RC.research_seal_identity(book)
    except (CP.PairError, PS.StoreError, RF.ResearchFactoryError, RF.RC.ContractError, OSError,
            UnicodeError, json.JSONDecodeError, KeyError) as exc:
        raise SystemExit(f"[run] completed downstream product decision is unavailable: {exc}") from exc
    receipt = _downstream_comparison(declaration, roots, seals)
    receipt_path = Path(spec["receipt_path"]).absolute()
    if roots["treatment"] not in receipt_path.parents:
        raise SystemExit("[run] downstream-effect receipt target escapes the treatment arm")
    if os.path.lexists(receipt_path):
        try:
            if json.loads(PS._safe_file(receipt_path, roots["treatment"]).read_text(
                    encoding="utf-8")) != receipt:
                raise SystemExit("[run] downstream-effect receipt resume inputs differ")
        except (PS.StoreError, OSError, json.JSONDecodeError) as exc:
            raise SystemExit(f"[run] downstream-effect receipt is malformed: {exc}") from exc
    else:
        PS.ensure_dir(receipt_path.parent, roots["treatment"])
        PS.write_json(receipt_path, receipt)
    if receipt["status"] != "PASS":
        raise SystemExit(
            "[run] blinded downstream comparison did not support the research treatment")
    _downstream_effect_receipt(declaration, roots, seals)
    return receipt


def _research_causal_record(declaration, authority, hard, comparison, downstream):
    """Build and revalidate the compact schema-2 record without appending it."""
    decision = comparison["hypothesis_outcome"]
    inputs = dict(declaration["inputs"])
    inputs["research_declaration_sha256"] = PS.state_hash(declaration)
    if declaration["downstream_effect"]["required"]:
        inputs["downstream_effect_task_sha256"] = \
            declaration["downstream_effect"]["task_sha256"]
    record = {"schema": 2, "surface": "research",
        "hypothesis": declaration["hypothesis"],
        "causal_chain": declaration["causal_chain"],
        "changed_bundle": declaration["changed_bundle"],
        "frozen_variables": declaration["frozen_variables"],
        "inputs": inputs,
        "evidence": {"integrity": authority["hard_gate_receipt_sha256"],
            "reader_effect": authority["comparison_receipt_sha256"],
            "whole_opening_sequence": (
                authority["downstream_effect_receipt_sha256"] or "NOT_REQUIRED"),
            "carr_craft_diagnostic": "NOT_APPLICABLE: research surface"},
        "research": authority, "decision": decision,
        "falsifier": declaration["falsifier"]}
    evidence = {"hard_gates": hard, "comparison": comparison,
                "downstream_effect": downstream}
    return ER.bind_research_evidence(record, evidence), evidence


def _persist_research_causal(root, declaration, record, evidence):
    """Persist exact candidate evidence; never append or promote from this seam."""
    base = Path(root).absolute() / "evidence" / "research-causal"
    PS.ensure_dir(base, root)
    values = {"declaration.json": declaration,
              "hard-gates.json": evidence["hard_gates"],
              "comparison-receipt.json": evidence["comparison"],
              "causal-record.json": record}
    if evidence["downstream_effect"] is not None:
        values["downstream-effect-bound.json"] = evidence["downstream_effect"]
    for name, value in values.items():
        path, data = base / name, PS.json_bytes(value)
        if os.path.lexists(path):
            if PS._safe_file(path, root).read_bytes() != data:
                raise SystemExit(f"[run] durable research causal evidence differs: {name}")
        else:
            PS.write(path, data)


def _research_treatment(path, accepted_root=None, book=None, chapters="1-3",
                        iteration=None):
    """Execute the production research surface without deciding or promoting it."""
    try:
        declaration = json.loads(Path(path).read_text(encoding="utf-8"))
        ER.validate_research_treatment(declaration)
    except (OSError, json.JSONDecodeError, ER.RecordError) as exc:
        raise SystemExit(f"[run] research treatment declaration blocked: {exc}") from exc
    if not os.environ.get("OPENROUTER_API_KEY", "").strip():
        raise SystemExit("[run] OPENROUTER_API_KEY is missing; research treatment made no writes")
    import research_factory as RF  # fixed production facade; no injectable backend
    roots = _prepare_research_arms(declaration, accepted_root, book, chapters,
                                   iteration, RF)
    identities = _research_preflight_identity(declaration, roots, RF)
    seals = {name: (RF.completed_experiment(str(root)) or
                    RF.start_experiment(str(root)))
             for name, root in roots.items()}
    for label, seal in seals.items():
        if not isinstance(seal, str) or ER.SHA256.fullmatch(seal) is None:
            raise SystemExit(f"[run] {label} research arm returned no valid seal")
    hard, _reports = _research_hard_gates(roots, seals, RF)
    comparison = _research_comparison(declaration, roots, identities, seals)
    downstream = declaration["downstream_effect"]
    downstream_receipt = _downstream_effect_receipt(declaration, roots, seals)
    authority = {"control_seal_sha256": seals["control"],
        "treatment_seal_sha256": seals["treatment"],
        "hard_gate_receipt_sha256": PS.state_hash(hard),
        "comparison_task_sha256": comparison["task_sha256"],
        "comparison_receipt_sha256": PS.state_hash(comparison),
        "downstream_effect_required": downstream["required"],
        "downstream_effect_receipt_sha256": (
            PS.state_hash(downstream_receipt) if downstream_receipt else None)}
    record, evidence = _research_causal_record(
        declaration, authority, hard, comparison, downstream_receipt)
    _persist_research_causal(roots["treatment"], declaration, record, evidence)
    try:
        manifest = CP.load(roots["treatment"])
        if manifest["state"] == "SEALED":
            tested_pair_hash = manifest["tested_hash"]
            CP.verify_sealed(roots["treatment"], tested_pair_hash)
        else:
            tested_pair_hash = CP.seal(roots["treatment"])
    except CP.PairError as exc:
        raise SystemExit(f"[run] research treatment pair could not be sealed: {exc}") from exc
    continuation = shlex.join([
        sys.executable, "scripts/loop/gate.py", "--iter", str(iteration),
        "--config", str(CP.candidate_tree(roots["treatment"]) /
                        identities["treatment"]["run"]["config"]),
        "--tested-pair-hash", tested_pair_hash,
        "--accepted-root", str(Path(accepted_root).absolute()),
        "--decision-timestamp", "<UTC_ISO_8601>", "--research-causal",
        "--redesign-authorized", "--rf-stage", "RF-32",
        "--candidate-root", str(roots["treatment"]),
    ])
    return {**authority, "record": record,
            "tested_pair_hash": tested_pair_hash,
            "gate_continuation": continuation}
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True)
    ap.add_argument("--chapters", default="1-3")
    ap.add_argument("--iter", type=int, required=True)
    ap.add_argument("--hypothesis", default="")
    ap.add_argument("--no-write", action="store_true", help="skip RUN; score+gate existing chapters")
    ap.add_argument("--writer-authority-receipt",
                    help="pinned manual writer handoff identity for --no-write replay")
    ap.add_argument("--score-now", action="store_true",
                    help="skip the stop-for-review pause and score immediately after writing")
    ap.add_argument("--config", default=None)
    ap.add_argument("--accepted-root")
    ap.add_argument("--promote-pair", action="store_true",
                    help="forward explicit human promotion approval to the gate")
    ap.add_argument("--decision-timestamp",
                    help="pinned UTC timestamp forwarded unchanged to the atomic gate")
    ap.add_argument("--initialize-accepted-store", action="store_true",
                    help="explicitly freeze repo-root bootstrap inputs behind the atomic pointer")
    ap.add_argument("--add-book-to-accepted-store", action="store_true",
                    help="atomically add one complete workshop to the accepted operation view")
    ap.add_argument("--research-treatment",
                    help="schema-2 research-only declaration for the existing causal path")
    ap.add_argument("--bind-research-downstream-effect", action="store_true",
                    help="bind a completed canonical product decision to a preregistered research effect")
    LG.add_arguments(ap)
    a = ap.parse_args()
    if a.initialize_accepted_store and a.add_book_to_accepted_store:
        ap.error("choose one accepted-store operation")
    if a.writer_authority_receipt and not a.no_write:
        ap.error("--writer-authority-receipt requires --no-write")
    if a.bind_research_downstream_effect and not a.research_treatment:
        ap.error("--bind-research-downstream-effect requires --research-treatment")

    store_operation = a.initialize_accepted_store or a.add_book_to_accepted_store
    research_operation = bool(a.research_treatment)
    candidate = LG.require_authorized(
        a, entrypoint="run_iteration.py",
        pre_rf23_stage=("RF-02" if store_operation else
                        "RF-32" if research_operation else None))
    target = Path(a.accepted_root or LG.REPO_ROOT).absolute()
    if a.research_treatment:
        if store_operation or a.no_write or a.promote_pair:
            ap.error("--research-treatment cannot be combined with another run operation")
        if a.rf_dry_run:
            LG.dry_run(a, "run_iteration.py")
            return
        if a.bind_research_downstream_effect:
            if not os.environ.get("OPENROUTER_API_KEY", "").strip():
                raise SystemExit(
                    "[run] OPENROUTER_API_KEY is missing; downstream binding made no writes")
            receipt = _bind_downstream_effect(
                a.research_treatment, candidate)
            print(f"[run] bound downstream research effect: {PS.state_hash(receipt)}")
            return
        seals = _research_treatment(a.research_treatment, candidate, a.book,
                                    a.chapters, a.iter)
        print(f"[run] isolated research arms sealed: {seals['control_seal_sha256']} "
              f"{seals['treatment_seal_sha256']}")
        print(f"[run] RF-02 research gate continuation: {seals['gate_continuation']}")
        return
    if store_operation:
        target = LG.require_store_target(candidate, target)
        if LG.dry_run(a, "run_iteration.py"):
            return
        try:
            action = CP.initialize if a.initialize_accepted_store else CP.add_book
            generation = action(target, a.book, a.config or "loop/config.yaml")
        except CP.PairError as exc:
            label = "setup" if a.initialize_accepted_store else "workshop addition"
            raise SystemExit(f"run: accepted-store {label} failed closed: {exc}") from exc
        print(f"[run] accepted generation {generation}")
        return
    if a.rf_dry_run:
        config_path = Path(a.config) if a.config else loopcfg.find_config()
        book = Path(a.book)
        LG.require_targets(candidate, config_path, book, book / "chapters")
        loopcfg.load(config_path)
        LG.dry_run(a, "run_iteration.py")
        return
    if not a.decision_timestamp:
        ap.error("candidate execution requires --decision-timestamp for resumable gating")
    if not os.path.lexists(candidate / CP.MANIFEST):
        try:
            CP.snapshot(candidate, target, a.book, a.chapters,
                        a.config or "loop/config.yaml", a.iter)
        except CP.PairError as exc:
            raise SystemExit(f"run: candidate snapshot failed closed: {exc}") from exc
    manifest = CP.load(candidate)
    try:
        CP.assert_run(candidate, manifest, a.book, a.chapters, a.iter,
                      a.config or "loop/config.yaml")
    except CP.PairError as exc:
        raise SystemExit(f"run: resume rejected: {exc}") from exc
    tree = CP.candidate_tree(candidate)
    config_path = CP.candidate_path(candidate, manifest["run"]["config"])
    book = tree / manifest["run"]["book"]
    CP.require_member(candidate, config_path, "config", manifest)
    LG.require_targets(candidate, config_path, book, book / "chapters")
    cfg = loopcfg.load(config_path)
    cfg = dict(cfg)
    evidence = CP.evidence_tree(candidate)
    cfg.update(scores_dir=str(evidence / "scores"),
               results_tsv=str(evidence / "results.tsv"),
               tasks_dir=str(evidence / "iterations"))
    LG.require_config_targets(candidate, cfg, "scores_dir", "results_tsv", "tasks_dir")
    ch_dir = book / "chapters"
    try:
        PS.safe_dir(ch_dir, tree)
    except PS.StoreError as exc:
        raise SystemExit(f"run: incomplete explicit pair: {exc}") from exc
    sel = list(manifest["run"]["chapters"])
    try:
        for n in sel:
            CP.require_member(candidate, ch_dir / f"chapter-{n:02d}.md", "product", manifest)
            if n > 1:
                CP.require_member(candidate, ch_dir / f"chapter-{n-1:02d}.md",
                                  "product", manifest)
    except CP.PairError as exc:
        raise SystemExit(f"run: incomplete explicit pair: {exc}") from exc

    handoff = manifest["state"] == "WRITER_HANDOFF" or manifest.get("operation") is not None
    receipt_exists = os.path.lexists(WC.manual_receipt_path(candidate))
    batch = manifest.get("draft_batch")
    if not a.no_write and batch and batch["mode"] == "manual":
        raise SystemExit("[run] durable manual writer handoff requires --no-write replay")
    if a.no_write and (batch and batch["mode"] == "manual" or not batch and
                       (handoff or a.writer_authority_receipt or receipt_exists)):
        if not a.writer_authority_receipt:
            raise SystemExit("[run] manual writer resume lacks its pinned receipt identity")
        try:
            WC.require_manual_resume(candidate, book, sel, a.writer_authority_receipt)
            if batch and batch["state"] == "FROZEN":
                FB.require_frozen_batch(candidate)
            else:
                if batch is None:
                    FB.begin(candidate, None, "manual")
                remaining = FB.accept_manual(candidate)
                if remaining:
                    print(f"[run] manual batch remains partial; write chapters "
                          f"{','.join(map(str, remaining))} in order, then replay:")
                    print(f"[run]   {MD.resume(a, HERE, sys.executable or 'python3',
                                               a.writer_authority_receipt)}")
                    sys.exit(2)
                FB.freeze(candidate)
        except (WC.WriterContextError, FB.BatchError, PS.StoreError) as exc:
            raise SystemExit(f"[run] manual writer resume blocked: {exc}") from exc
    elif a.no_write:
        try:
            FB.require_frozen_batch(candidate)
        except FB.BatchError as exc:
            raise SystemExit(f"[run] review/evaluation blocked: {exc}") from exc

    if not a.no_write:
        wrote = write_chapters(cfg, book, sel, candidate)
        if not wrote:
            print("[run] stopping before SCORE (no chapters were written). "
                  "Write them manually per the instructions above, then replay:")
            try:
                receipt_hash = WC.manual_receipt_hash(candidate)
            except WC.WriterContextError as exc:
                raise SystemExit(f"[run] manual writer handoff failed closed: {exc}") from exc
            print(f"[run]   {MD.resume(a, HERE, sys.executable or 'python3', receipt_hash)}")
            sys.exit(2)
        current_batch = CP.load(candidate).get("draft_batch") or {}
        if current_batch.get("state") != "FROZEN":
            try:
                FB.freeze(candidate)
            except FB.BatchError as exc:
                raise SystemExit(f"[run] first-draft freeze failed closed: {exc}") from exc
    try:
        grounded = GR.advance(candidate, cfg)
    except GR.GroundedReviewPending as exc:
        print("[run] Complete first-draft batch frozen. Grounded review is mandatory.")
        print(f"[run] {MD.grounded(candidate, exc.missing)}")
        print(f"[run] Then replay: {MD.resume(a, HERE, sys.executable or 'python3')}")
        sys.exit(4)
    except GR.GroundedReviewError as exc:
        raise SystemExit(f"[run] grounded review blocked: {exc}") from exc
    try:
        try:
            developmental = DR.require_developmental_pass(candidate, cfg)
        except DR.DevelopmentalReviewError:
            developmental = DR.advance(candidate, cfg)
    except DR.DevelopmentalReviewPending:
        print("[run] Grounded review PASS. Whole-opening developmental review is mandatory.")
        print(f"[run] {MD.developmental(candidate)}")
        print(f"[run] Then replay: {MD.resume(a, HERE, sys.executable or 'python3')}")
        sys.exit(4)
    except DR.DevelopmentalReviewError as exc:
        raise SystemExit(f"[run] developmental review blocked: {exc}") from exc
    if not a.no_write and not a.score_now:
        print(f"[run] Grounded review PASS {grounded['receipt_hash']}; developmental "
              f"PASS {developmental['receipt_hash']}. Legacy literary review may now "
              f"start ({MD.reviewer(candidate)}).")
        print("[run] Then resume:")
        print(f"[run]   {MD.resume(a, HERE, sys.executable or 'python3')}")
        sys.exit(0)

    manifest = CP.load(candidate)
    try:
        if manifest["state"] in ("CANDIDATE", "WRITER_HANDOFF", "BATCH_FROZEN"):
            tested_hash = CP.seal(candidate)
        elif manifest["state"] == "SEALED" and CP.status(candidate) == "SEALED":
            tested_hash = manifest["tested_hash"]
            CP.verify_sealed(candidate, tested_hash)
        else:
            raise CP.PairError(f"cannot resume decided pair {CP.status(candidate)}")
    except CP.PairError as exc:
        raise SystemExit(f"run: candidate sealing failed closed: {exc}") from exc
    print(f"[run] sealed exact evaluation pair {tested_hash}")
    py = sys.executable or "python3"
    auth = LG.forward_arguments(a)
    rc_score = run_step([py, str(HERE.parent / "score.py"), "--book", str(book),
                         "--chapters", a.chapters, "--iter", str(a.iter),
                         "--config", str(config_path),
                         "--tested-pair-hash", tested_hash] + auth, cwd=tree)
    if rc_score == 3:
        print("[run] WAITING FOR JUDGE VERDICTS — dispatch the emitted task files as fresh")
        print("      native Sol subagents (see [judges] lines above), save the JSON verdicts,")
        print("      then replay the pinned run command:")
        print(f"[run]   {MD.resume(a, HERE, py)}")
        sys.exit(3)
    if rc_score != 0:
        print(f"[run] score.py exited {rc_score}; not gating.")
        sys.exit(rc_score)
    # Step 3 GATE.
    pair_args = ["--tested-pair-hash", tested_hash,
                 "--accepted-root", str(target),
                 "--decision-timestamp", a.decision_timestamp]
    if a.promote_pair:
        pair_args.append("--promote-pair")
    rc_gate = run_step([py, str(HERE.parent / "gate.py"), "--iter", str(a.iter),
                        "--hypothesis", a.hypothesis, "--config", str(config_path)]
                       + auth + pair_args, cwd=tree)
    print("[run] Gate exit 0 = decision made (verdict is in the row/stdout, incl. REVERT). "
          "The pair is already promoted or retained as rejected evidence.")
    sys.exit(rc_gate)


if __name__ == "__main__":
    main()
