"""Emit, preserve, and bind fresh native blind product-effect observations."""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1] / "loop"))
import native_judge as N  # noqa: E402
import judges  # noqa: E402
import loopcfg  # noqa: E402
import pair_store as PS  # noqa: E402
import product_decision as DECISION  # noqa: E402
import product_effect as EFFECT  # noqa: E402


FIELDS = {
    "schema", "scope", "promotion_eligible", "task_id", "base_task_sha256",
    "tested_pair_hash", "prompt_sha256", "input_sha256", "raw_verdict_id",
    "actor", "kind", "family", "raw_verdict",
}
EXTERNAL_FIELDS = {"raw_verdict_id", "actor", "kind", "family", "raw_verdict"}


class PanelError(RuntimeError):
    pass


def load_input(path, h_f04=False):
    value = EFFECT._loads(Path(path).read_text(encoding="utf-8"))
    return EFFECT.validate_h_f04(value) if h_f04 else EFFECT.validate_task(value)


def _task(source, h_f04):
    return (EFFECT.h_f04_judge_task(EFFECT.validate_h_f04(source)) if h_f04
            else EFFECT.validate_task(source))


def _prompt(cfg, task):
    rubric_bytes = Path(cfg["product_effect_rubric"]).read_bytes()
    rubric = rubric_bytes.decode("utf-8")
    if rubric.count("{{TASK}}") != 1 or "{{REFERENCE}}" in rubric:
        raise PanelError("product-effect rubric must have one anonymous task slot only")
    payload = json.dumps(task, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False)
    rendered = rubric.replace("{{TASK}}", payload).encode()
    return rendered, {"prompt_sha256": PS.sha(rubric_bytes),
                      "input_sha256": PS.sha(rendered)}


def _binding(cfg, task, tested_pair_hash, h_f04):
    prompt, hashes = _prompt(cfg, task)
    if h_f04:
        scope, eligible, tested_pair_hash = "h_f04_calibration", False, None
    elif not isinstance(tested_pair_hash, str) \
            or not DECISION.HEX.fullmatch(tested_pair_hash):
        raise PanelError("ordinary product observation requires a sealed tested-pair hash")
    else:
        scope, eligible = "ordinary_product", True
    return prompt, {"scope": scope, "promotion_eligible": eligible,
                    "base_task_sha256": task["task_sha256"],
                    "tested_pair_hash": tested_pair_hash, **hashes}


def _call_id(binding, actor):
    return DECISION.bound_task_id({**binding, "actor": actor})


def _paths(cfg, iteration, task, identities, tested_pair_hash, h_f04):
    base = judges.judging_dir(cfg, iteration)
    if h_f04:
        base /= "h-f04"
    _prompt_bytes, binding = _binding(cfg, task, tested_pair_hash, h_f04)
    rows = []
    for identity in identities:
        task_id = _call_id(binding, identity)
        stem = f"product-{task['mode']}-{task_id[:16]}"
        rows.append((identity, task_id, base / "tasks" / f"{stem}.md",
                     base / "verdicts" / f"{stem}.json"))
    return rows


def emit(cfg, iteration, source, identities=N.DEFAULT_IDENTITIES,
         h_f04=False, tested_pair_hash=None):
    task = _task(source, h_f04)
    identities = N.parse_identities(",".join(identities))
    prompt, _binding_value = _binding(cfg, task, tested_pair_hash, h_f04)
    paths = _paths(cfg, iteration, task, identities, tested_pair_hash, h_f04)
    for _identity, _task_id, task_path, _verdict_path in paths:
        PS.write(task_path, prompt)
    return paths


def dispatch(cfg, iteration, source, identities=N.DEFAULT_IDENTITIES,
             h_f04=False, tested_pair_hash=None, complete=N.complete):
    """Run exactly two ephemeral native contexts and preserve their raw replies."""
    task = _task(source, h_f04)
    prompt, binding = _binding(cfg, task, tested_pair_hash, h_f04)
    rows = emit(cfg, iteration, source, identities, h_f04, tested_pair_hash)
    for identity, task_id, task_path, verdict_path in rows:
        raw, transport, error = complete(
            task_path.read_text(encoding="utf-8"), identity, EFFECT.output_schema())
        if error:
            raise PanelError(f"{identity}: {error}")
        EFFECT.verdict(raw, task)
        raw_id = transport.get("thread_id")
        if not isinstance(raw_id, str) or not raw_id:
            raise PanelError(f"{identity}: native verdict has no thread identity")
        if transport.get("input_sha256") not in (None, binding["input_sha256"]):
            raise PanelError(f"{identity}: native transport input hash is stale")
        record = {"schema": 2, **binding, "task_id": task_id,
                  "raw_verdict_id": raw_id, "actor": identity,
                  "kind": "model", "family": "openai", "raw_verdict": raw}
        PS.write(verdict_path, json.dumps(
            record, sort_keys=True, separators=(",", ":")).encode())
    return rows


def _validate(cfg, value, task, tested_pair_hash, h_f04, actor=None):
    _prompt_bytes, binding = _binding(cfg, task, tested_pair_hash, h_f04)
    if not isinstance(value, dict) or set(value) != FIELDS or value.get("schema") != 2 \
            or any(value.get(key) != item for key, item in binding.items()) \
            or actor is not None and value.get("actor") != actor \
            or value.get("task_id") != _call_id(binding, value.get("actor")):
        raise PanelError("stale, unbound, or malformed raw product verdict")
    if value.get("kind") not in {"model", "human"} \
            or not isinstance(value.get("actor"), str) or not value["actor"].strip() \
            or not isinstance(value.get("raw_verdict_id"), str) \
            or not value["raw_verdict_id"].strip():
        raise PanelError("raw product verdict identity is malformed")
    if value["kind"] == "model" and (not isinstance(value.get("family"), str)
                                      or not value["family"].strip()) \
            or value["kind"] == "human" and (
                value.get("family") is not None or len(value["actor"].split()) < 2):
        raise PanelError("external verdict must identify a model family or named human")
    EFFECT.verdict(value["raw_verdict"], task)
    return value


def records(cfg, iteration, source, identities=N.DEFAULT_IDENTITIES,
            h_f04=False, tested_pair_hash=None):
    task = _task(source, h_f04)
    identities = N.parse_identities(",".join(identities))
    found = []
    for identity, _task_id, _task_path, verdict_path in _paths(
            cfg, iteration, task, identities, tested_pair_hash, h_f04):
        if not verdict_path.is_file():
            raise PanelError(f"missing raw verdict: {verdict_path}")
        value = EFFECT._loads(verdict_path.read_text(encoding="utf-8"))
        found.append(_validate(cfg, value, task, tested_pair_hash, h_f04, identity))
    if len({row["raw_verdict_id"] for row in found}) != 2:
        raise PanelError("native contexts did not preserve two raw verdict identities")
    return found


def ingest(cfg, source, tested_pair_hash, external):
    """Validate and bind one second-family or named-human raw observation."""
    task = _task(source, False)
    if not isinstance(external, dict) or set(external) != EXTERNAL_FIELDS:
        raise PanelError("external verdict fields must be exact")
    _prompt_bytes, binding = _binding(cfg, task, tested_pair_hash, False)
    record = {"schema": 2, **binding,
              "task_id": _call_id(binding, external.get("actor")), **external}
    return _validate(cfg, record, task, tested_pair_hash, False)


def aggregate(cfg, iteration, source, identities=N.DEFAULT_IDENTITIES,
              h_f04=False, tested_pair_hash=None):
    task = _task(source, h_f04)
    rows = records(cfg, iteration, source, identities, h_f04, tested_pair_hash)
    parsed = [EFFECT.verdict(row["raw_verdict"], task) for row in rows]
    choices = {row["preferred"] for row in parsed}
    return {"status": parsed[0]["preferred"] if len(choices) == 1 else "INCONCLUSIVE",
            "panel": "two_fresh_native_same_family_repeats",
            "promotion_eligible": False,
            "task_ids": [row["task_id"] for row in rows],
            "raw_verdict_ids": [row["raw_verdict_id"] for row in rows],
            "raw_verdicts": parsed}


def decision_row(cfg, record, task, support_candidate, tested_pair_hash):
    """Map one verified ordinary observation for an independent decisive panel."""
    if record.get("scope") != "ordinary_product" \
            or record.get("promotion_eligible") is not True:
        raise PanelError("H-F04/calibration records cannot enter product decisions")
    task = _task(task, False)
    record = _validate(cfg, record, task, tested_pair_hash, False)
    if support_candidate not in EFFECT.LABELS:
        raise PanelError("support candidate must be anonymous A or B")
    parsed = EFFECT.verdict(record["raw_verdict"], task)
    vote = ("INCONCLUSIVE" if parsed["preferred"] == "TIE" else
            "PASS" if parsed["preferred"] == support_candidate else "FAIL")
    return {key: record[key] for key in DECISION.VERDICT_FIELDS - {"verdict"}} | {
        "verdict": vote}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("emit", "dispatch", "aggregate", "ingest"))
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--task")
    source.add_argument("--h-f04-envelope")
    parser.add_argument("--iter", required=True)
    parser.add_argument("--config")
    parser.add_argument("--tested-pair-hash")
    parser.add_argument("--judge-identities", default=",".join(N.DEFAULT_IDENTITIES))
    parser.add_argument("--external-record")
    parser.add_argument("--support-candidate", choices=sorted(EFFECT.LABELS))
    args = parser.parse_args()
    cfg = loopcfg.load(args.config or loopcfg.find_config())
    h_f04 = bool(args.h_f04_envelope)
    task = load_input(args.h_f04_envelope or args.task, h_f04)
    identities = N.parse_identities(args.judge_identities)
    call = {"emit": emit, "dispatch": dispatch, "aggregate": aggregate}
    if args.action == "ingest":
        if h_f04 or not args.external_record or not args.support_candidate:
            parser.error("ingest requires ordinary --task, --external-record, and support candidate")
        external = EFFECT._loads(Path(args.external_record).read_text(encoding="utf-8"))
        record = ingest(cfg, task, args.tested_pair_hash, external)
        value = {"record": record, "decision_row": decision_row(
            cfg, record, task, args.support_candidate, args.tested_pair_hash)}
    else:
        value = call[args.action](cfg, args.iter, task, identities, h_f04,
                                  args.tested_pair_hash)
        if args.action in {"emit", "dispatch"}:
            value = [str(row[2 if args.action == "emit" else 3]) for row in value]
    print(json.dumps(value, indent=1))


if __name__ == "__main__":
    main()
