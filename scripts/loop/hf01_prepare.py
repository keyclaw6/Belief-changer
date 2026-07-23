#!/usr/bin/env python3
"""Prepare only the matched RF-02 H-F01 snapshots, then stop before any call."""
import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import candidate_pair as CP  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import legacy_guard as LG  # noqa: E402
import pair_store as PS  # noqa: E402


class PrepareError(RuntimeError):
    pass


def _source_hashes(root):
    contract = CP.PC.derive(root, HF.BOOK, "loop/config.yaml")
    return {item["path"]: PS.sha(PS._safe_file(root / item["path"], root).read_bytes())
            for item in contract["pair"]}


def prepare(root, iteration):
    root = HF.require_authorized_root(root)
    if isinstance(iteration, bool) or not isinstance(iteration, int) or iteration < 1:
        raise PrepareError("H-F01 iteration must be a positive integer")
    HF.require_stage({"authority": {"ledger_path": str(HF.LEDGER)}}, "RF-21")
    try:
        _, generation, registry = PS.current(root)
        paths = HF.arm_paths(root)
        experiments = root / "loop/experiments"
        if os.path.lexists(experiments):
            PS.safe_dir(experiments, root)
        missing = {}
        for arm, item in paths.items():
            missing[arm] = not os.path.lexists(item["experiment"])
            if not missing[arm]:
                PS.safe_dir(item["experiment"], experiments)
        experiments = PS.ensure_dir(experiments, root)
        for item in paths.values():
            PS.ensure_dir(item["experiment"], experiments)
        before = _source_hashes(root)
        for arm, item in paths.items():
            experiment = item["experiment"]
            if missing[arm]:
                CP.snapshot(experiment, root, HF.BOOK, "1-3", "loop/config.yaml", iteration)
            manifest = CP.inspect(experiment)
            run = manifest["run"]
            if manifest["state"] != "CANDIDATE" or manifest.get("operation") is not None \
                    or manifest.get("outputs") or manifest["accepted_generation"] != generation \
                    or run != {"experiment_id": experiment.name, "iteration_id": iteration,
                               "book": HF.BOOK, "chapters": [1, 2, 3],
                               "config": "loop/config.yaml"}:
                raise PrepareError(f"existing {arm} snapshot is not the reusable pre-RF21 identity")
        manifests = {arm: CP.inspect(item["experiment"]) for arm, item in paths.items()}
        identities = {(value["accepted_generation"], value["accepted_pair_hash"],
                       value["accepted_evaluation_hash"]) for value in manifests.values()}
        if len(identities) != 1:
            raise PrepareError("H-F01 control and treatment snapshots are not exactly matched")
        if before != _source_hashes(root):
            raise PrepareError("accepted production/configuration bytes changed during preparation")
        return {"schema": 1, "state": "PREPARED_NO_CALLS", "root": str(root),
                "accepted_generation": generation, "accepted_pair_hash": registry["pair_hash"],
                "iteration": iteration, "arms": sorted(paths)}
    except (CP.PairError, PS.StoreError, OSError) as exc:
        raise PrepareError(str(exc)) from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-root", required=True)
    parser.add_argument("--iteration", required=True, type=int)
    LG.add_arguments(parser)
    args = parser.parse_args()
    candidate = LG.require_authorized(args, entrypoint="hf01_prepare.py",
        pre_rf23_stage="RF-21", exact_candidate=HF.AUTHORIZED_ROOT,
        allow_accepted_overlap=True, require_in_progress=True)
    if candidate != HF.require_authorized_root(args.snapshot_root):
        raise SystemExit("RF-00 legacy guard: --snapshot-root must equal --candidate-root")
    LG.require_store_target(candidate, candidate)
    if LG.dry_run(args, "hf01_prepare.py"):
        return
    try:
        result = prepare(candidate, args.iteration)
    except (PrepareError, HF.PreflightError) as exc:
        raise SystemExit(f"H-F01 prepare failed closed: {exc}") from exc
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
