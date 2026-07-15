"""Fail-closed product and isolated H-F04 scope for judge_panel."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOOP = ROOT / "scripts" / "loop"
import sys
sys.path.insert(0, str(LOOP))
import candidate_pair as CP  # noqa: E402
import pair_store as PS  # noqa: E402
import h_f04_controls as HF  # noqa: E402


class ScopeError(RuntimeError):
    pass


def _exact(actual, wanted, label):
    if Path(actual).absolute() != Path(wanted).absolute():
        raise ScopeError(f"{label} is outside the pinned evaluation operation")


def _unused(path):
    if os.path.lexists(path):
        raise ScopeError("judge output operation is already present")


def _selection(raw):
    values = []
    for token in raw.split(","):
        token = token.strip()
        if "-" in token:
            left, right = token.split("-", 1)
            if not left.isdigit() or not right.isdigit() or int(left) > int(right):
                raise ScopeError("chapter selection is malformed")
            values.extend(range(int(left), int(right) + 1))
        elif token.isdigit():
            values.append(int(token))
        else:
            raise ScopeError("chapter selection is malformed")
    if not values or values != sorted(set(values)):
        raise ScopeError("chapter selection is malformed")
    return values


def _product(args):
    if not args.candidate_root or not args.tested_pair_hash:
        raise ScopeError("product judgment requires a pinned sealed candidate identity")
    try:
        view = CP.open_sealed(args.candidate_root, args.tested_pair_hash)
        manifest, cfg = view["manifest"], view["config"]
        ours = view["pair"] / manifest["run"]["book"] / "chapters"
        ref = Path(cfg["reference_dir"])
        out = view["evidence"] / "product-judge"
        if _selection(args.chapters) != manifest["run"]["chapters"] or args.pairs:
            raise ScopeError("judge chapter selection differs from the sealed candidate")
        _exact(args.ours, ours, "candidate chapters")
        _exact(args.ref, ref, "reference input")
        _exact(args.out, out, "judge output")
        _unused(out)
        PS.safe_dir(ours, view["pair"])
        PS.safe_dir(ref, view["evaluation"])
        PS.safe_dir(out.parent, Path(args.candidate_root).absolute())
        return {"mode": "product", "candidate_root": str(Path(args.candidate_root).absolute()),
                "tested_pair_hash": args.tested_pair_hash,
                "selection": manifest["run"]["chapters"]}
    except ScopeError:
        raise
    except (CP.PairError, PS.StoreError, OSError, KeyError, TypeError) as exc:
        raise ScopeError(f"product judgment scope is invalid: {exc}") from exc


def _control(args, legacy, configuration=None):
    if legacy or not args.h_f04_root or args.candidate_root or args.tested_pair_hash:
        raise ScopeError("only an isolated canonical H-F04 control may bypass product identity")
    root = Path(args.h_f04_root).absolute()
    if root != ROOT / "calibration" / "h-f04" or not args.control \
            or args.chapters != "1-3" or args.pairs:
        raise ScopeError("H-F04 control scope is not the constrained three-chapter layout")
    ours, ref, out = root / "anonymous-a", root / "anonymous-b", root / "outputs" / args.control
    _exact(args.ours, ours, "H-F04 anonymous candidate A")
    _exact(args.ref, ref, "H-F04 anonymous candidate B")
    _exact(args.out, out, "H-F04 control output")
    try:
        HF.control_layout(args.control, configuration)
        PS.safe_dir(root)
        PS.safe_dir(ours, root)
        PS.safe_dir(ref, root)
        PS.safe_dir(out.parent, root)
    except (PS.StoreError, OSError, ValueError) as exc:
        raise ScopeError(f"H-F04 control scope is invalid: {exc}") from exc
    return {"mode": "h-f04-control", "root": str(root), "control": args.control}


def guard(args, legacy=False, configuration=None):
    if args.control or args.h_f04_root:
        return _control(args, legacy, configuration)
    return _product(args)


def canonical(args, identities, role_specs, judge_dir):
    """Build and authorize canonical inputs before any book/control read."""
    import native_judge as N
    product = not args.control and not args.h_f04_root
    try:
        if product:
            HF.validate_request(args.validated_controls)
        if args.pairs:
            raise ScopeError("canonical Stage-A does not accept custom pairings")
        selection = _selection(args.chapters)
        if len(selection) != 3:
            raise ScopeError("canonical Stage-A requires exactly three unique chapter pairings")
        pairing = [(chapter, chapter) for chapter in selection]
        prompts = {role: (judge_dir / spec["prompt"]).read_text(encoding="utf-8")
                   for role, spec in role_specs.items()}
        schemas = {role: N.role_output_schema(spec) for role, spec in role_specs.items()}
        configuration = N.instrument_configuration(prompts, schemas, pairing, identities)
        controls = N.validate_controls(args.validated_controls, configuration) if product else None
        return {"cfg": {"prompts": prompts, "schemas": schemas}, "pairing": pairing,
                "configuration": configuration, "controls": controls}
    except ScopeError:
        raise
    except (OSError, ValueError) as exc:
        raise ScopeError(f"canonical Stage-A preflight failed: {exc}") from exc
