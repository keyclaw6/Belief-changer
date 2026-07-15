"""Explicit accepted-store setup and terminal RF-02 pair decisions."""
import json
import os
from pathlib import Path

import gate_decision as GD
import loopcfg
import pair_contract as PC
import pair_store as PS


def assert_run(root, manifest, book, chapters, iteration, config):
    import candidate_pair as CP
    pair = CP.candidate_tree(root)

    def relative(value):
        path = Path(value)
        if not path.is_absolute():
            return path.as_posix()
        try:
            return path.absolute().relative_to(pair).as_posix()
        except ValueError as exc:
            raise CP.PairError(f"resume path is outside sealed pair: {path}") from exc

    actual = {"experiment_id": Path(root).name, "iteration_id": iteration,
              "book": relative(book), "chapters": CP._chapters(chapters),
              "config": relative(config)}
    if actual != manifest.get("run"):
        raise CP.PairError("resume CLI differs from canonical sealed run identity")


def initialize(accepted_root, book, config="loop/config.yaml", interrupt=None):
    import candidate_pair as CP
    accepted = Path(accepted_root).absolute()
    try:
        if PS.current(accepted, required=False)[0] is not None:
            raise CP.PairError("accepted store is already initialized")
        contract = PC.derive(accepted, book, config)
        pair = contract["pair"]
        evaluation = [{"group": "evaluation", "path": path}
                      for path in contract["evaluation"]]
        before_pair, before_eval = PS.states(accepted, pair), PS.states(accepted, evaluation)
        pair_hash, eval_hash = PS.state_hash(before_pair), PS.state_hash(before_eval)
        generation = PS.generation_hash(pair_hash, eval_hash)
        PS.materialize(accepted, generation, pair, evaluation, accepted, accepted)
        if (before_pair, before_eval) != (PS.states(accepted, pair), PS.states(accepted, evaluation)):
            raise CP.PairError("bootstrap inputs changed during accepted-store setup")
        boundary = interrupt or (lambda _step: None)
        boundary("generation-ready")
        PS.switch(accepted, generation, boundary)
        return generation
    except (PS.StoreError, PC.ContractError, OSError) as exc:
        CP._fail(exc)


def add_book(accepted_root, book, config="loop/config.yaml", interrupt=None):
    """Atomically add one validated complete workshop without rebuilding history."""
    import candidate_pair as CP
    accepted = Path(accepted_root).absolute()
    stage = PS.state_dir(accepted) / ".extend-pair-tmp"
    try:
        tree, _, registry = PS.current(accepted)
        book_rel, additions = PC.workshop_entries(accepted, book)
        prefix = f"{book_rel}/"
        if any(item["path"].startswith(prefix) for item in registry["entries"]):
            raise CP.PairError(f"workshop is already in the accepted view: {book_rel}")
        PS.discard_stage(stage, PS.state_dir(accepted))
        PS._copy_tree(stage, tree / "pair", registry["entries"])
        PS._copy_tree(stage, accepted, additions)
        contract = PC.derive(stage, book_rel, config, evaluation_root=tree / "evaluation")
        pair, evaluation = contract["pair"], registry["evaluation"]
        if evaluation != [{"group": "evaluation", "path": path}
                          for path in contract["evaluation"]]:
            raise CP.PairError("new workshop changed the accepted evaluation contract")
        pair_hash = PS.state_hash(PS.exact_tree(stage, pair))
        generation = PS.generation_hash(pair_hash, registry["evaluation_hash"])
        PS.materialize(accepted, generation, pair, evaluation, stage, tree / "evaluation")
        boundary = interrupt or (lambda _step: None)
        boundary("generation-ready")
        PS.switch(accepted, generation, boundary)
        return generation
    except (PS.StoreError, PC.ContractError, OSError) as exc:
        CP._fail(exc)
    finally:
        PS.discard_stage(stage, PS.state_dir(accepted))


def status(root):
    import candidate_pair as CP
    path = Path(root).absolute() / CP.DECISION
    if not os.path.lexists(path):
        return CP.load(root)["state"]
    try:
        value = json.loads(PS._safe_file(path, Path(root).absolute()).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, PS.StoreError) as exc:
        raise CP.PairError("invalid pair decision receipt") from exc
    if value.get("schema") != 1 or value.get("tested_hash") != CP.load(root).get("tested_hash") \
            or value.get("decision") not in ("REJECTED", "PROMOTED"):
        raise CP.PairError("invalid pair decision receipt")
    try:
        receipt = GD.load(root, value["tested_hash"])
    except GD.DecisionError as exc:
        raise CP.PairError(str(exc)) from exc
    if value != GD.terminal(receipt):
        raise CP.PairError("terminal decision differs from canonical gate decision")
    return value["decision"]


def _decide(root, tested_hash, decision, gate_receipt, interrupt=None):
    import candidate_pair as CP
    value = GD.terminal(gate_receipt)
    if decision != value["decision"]:
        raise CP.PairError("terminal decision contradicts the canonical gate decision")
    current = status(root)
    if current == decision:
        return
    if current != "SEALED":
        raise CP.PairError(f"cannot decide pair in state {current}")
    PS.write_json(Path(root).absolute() / CP.DECISION, value, interrupt)


def reject(root, tested_hash, interrupt=None):
    import candidate_pair as CP
    try:
        receipt = GD.load(root, tested_hash)
        CP.verify_sealed(root, tested_hash, {
            ".decision.json.rf02-tmp": GD.terminal_bytes(receipt)})
    except GD.DecisionError as exc:
        raise CP.PairError(str(exc)) from exc
    _decide(root, tested_hash, "REJECTED", receipt, interrupt)


def _promotion_evaluation(root, accepted, manifest, history_bytes):
    import candidate_pair as CP
    source = CP.evaluation_tree(root)
    pair = CP.candidate_tree(root)
    cfg = loopcfg.load(PS._safe_file(pair / manifest["run"]["config"], pair))
    history_rel = PC.relative(
        cfg.get("causal_results_jsonl") or cfg.get("results_tsv", ""), source)
    if history_rel not in {item["path"] for item in manifest["evaluation"]}:
        raise CP.PairError("accepted decision lineage is not a sealed evaluation member")
    stage = PS.state_dir(accepted) / ".promotion-evaluation-tmp"
    PS.discard_stage(stage, PS.state_dir(accepted))
    PS._copy_tree(stage, source, CP._bare(manifest["evaluation"]))
    PS.write(stage / history_rel, history_bytes)
    eval_hash = PS.state_hash(PS.exact_tree(stage, CP._bare(manifest["evaluation"])))
    return stage, eval_hash, stage


def promote(root, accepted_root, tested_hash, history_bytes, interrupt=None):
    import candidate_pair as CP
    accepted = Path(accepted_root).absolute()
    stage = None
    try:
        gate_receipt = GD.for_promotion(root, tested_hash, history_bytes)
        manifest = CP.verify_sealed(root, tested_hash, {
            ".decision.json.rf02-tmp": GD.terminal_bytes(gate_receipt)})
        PS.same_filesystem(Path(root), accepted, PS.state_dir(accepted))
        _, current_id, registry = PS.current(accepted)
        eval_source, eval_hash, stage = _promotion_evaluation(
            root, accepted, manifest, history_bytes)
        boundary = interrupt or (lambda _step: None)
        boundary("history-ready")
        promoted = PS.generation_hash(manifest["sealed"]["pair_hash"], eval_hash)
        if current_id != promoted:
            if status(root) != "SEALED" or current_id != manifest["accepted_generation"] \
                    or registry["pair_hash"] != manifest["accepted_pair_hash"] \
                    or registry["evaluation_hash"] != manifest["accepted_evaluation_hash"]:
                raise CP.PairError("accepted generation changed after the candidate snapshot")
            PS.materialize(accepted, promoted, CP._bare(CP._members(manifest)),
                           CP._bare(manifest["evaluation"]), CP.candidate_tree(root),
                           eval_source)
            boundary("generation-ready")
            PS.switch(accepted, promoted, boundary)
        _decide(root, tested_hash, "PROMOTED", gate_receipt, boundary)
    except (PS.StoreError, GD.DecisionError, OSError) as exc:
        CP._fail(exc)
    finally:
        if stage is not None:
            PS.discard_stage(stage, PS.state_dir(accepted))
