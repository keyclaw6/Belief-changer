"""Fixed H-F04 control authority for canonical product judging."""
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOOP = ROOT / "scripts" / "loop"
sys.path.insert(0, str(LOOP))
import pair_store as PS  # noqa: E402
import path_guard as PG  # noqa: E402

MODES = ("identical", "degraded-reference")
RECEIPT = "control-validation-receipt.json"


def root():
    return ROOT / "calibration" / "h-f04"


def summaries():
    return tuple(root() / "outputs" / mode / "judge-summary.json" for mode in MODES)


def canonical_argument():
    return ",".join(str(path) for path in summaries())


def validate_request(raw):
    if raw and raw != canonical_argument():
        raise ValueError("--validated-controls must be the exact canonical ordered H-F04 pair")


def _names(path):
    return {entry.name for entry in os.scandir(path)}


def control_layout(mode, configuration=None):
    """Validate the only layout allowed to generate one H-F04 control."""
    base, outputs = root(), root() / "outputs"
    try:
        PS.safe_dir(base)
        for name in ("anonymous-a", "anonymous-b", "outputs"):
            PS.safe_dir(base / name, base)
    except (PS.StoreError, OSError) as exc:
        raise ValueError(f"H-F04 layout is unsafe: {exc}") from exc
    if (_names(base) != {"anonymous-a", "anonymous-b", "outputs"} or
            not _names(outputs) <= set(MODES)):
        raise ValueError("H-F04 layout contains an undeclared entry")
    if os.path.lexists(outputs / mode):
        raise ValueError("H-F04 control output operation is already present")
    if configuration is not None:
        for prior in _names(outputs):
            path = outputs / prior / "judge-summary.json"
            try:
                PS.safe_dir(outputs / prior, base)
            except PS.StoreError as exc:
                raise ValueError(f"existing H-F04 control is unsafe: {exc}") from exc
            identity = _inspect(path, base)
            _validate_summary(_read_stable(path, identity), prior, configuration)


def _identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)


def _inspect(path, boundary):
    try:
        path = PG.safe_file(path, boundary)
        info = os.lstat(path)
    except (PG.PathError, OSError) as exc:
        raise ValueError(f"canonical control authority is unsafe: {exc}") from exc
    if stat.S_IMODE(info.st_mode) != 0o444:
        raise ValueError(f"canonical control authority has wrong mode: {path}")
    return _identity(info)


def _read_stable(path, expected):
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        with os.fdopen(descriptor, "rb") as handle:
            before = _identity(os.fstat(handle.fileno()))
            payload = handle.read()
            after = _identity(os.fstat(handle.fileno()))
        current = _inspect(path, root())
    except OSError as exc:
        raise ValueError(f"canonical control authority changed during read: {path}") from exc
    if expected != before or before != after or after != current:
        raise ValueError(f"canonical control authority changed during read: {path}")
    return payload


def _decode(payload, label):
    def unique(items):
        value = {}
        for key, item in items:
            if key in value:
                raise ValueError(f"duplicate key in {label}: {key}")
            value[key] = item
        return value
    try:
        value = json.loads(payload, object_pairs_hook=unique)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"malformed {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} is not an object")
    return value


def _validate_summary(payload, mode, configuration):
    data = _decode(payload, f"{mode} control summary")
    control = data.get("prompt_control")
    valid = (isinstance(control, dict) and data.get("protocol") == "stage-a-v2.3"
             and data.get("canonical") is True and data.get("panel_complete") is True
             and data.get("raw_judgments") == 20 and data.get("invalid_judgments") == 0
             and data.get("collapsed_observations") == 5
             and isinstance(data.get("matrix"), dict) and data["matrix"].get("passed") is True
             and control.get("mode") == mode and control.get("passed") is True
             and control.get("matrix_transport_valid") is True
             and control.get("semantic_expectation_met") is True)
    if not valid:
        raise ValueError(f"{mode} control did not pass canonically")
    if (data.get("instrument_configuration") != configuration or
            control.get("instrument_configuration") != configuration):
        raise ValueError(f"{mode} control configuration is stale")
    if payload != PS.json_bytes(data):
        raise ValueError(f"{mode} control summary bytes are not canonical")
    return data


def _receipt(configuration, payloads, identities):
    controls = []
    for mode, path, payload, identity in zip(MODES, summaries(), payloads, identities):
        controls.append({
            "control_identity": f"h-f04:{mode}:anonymous-a-vs-anonymous-b",
            "mode": mode, "path": path.relative_to(root()).as_posix(),
            "sha256": hashlib.sha256(payload).hexdigest(), "file_mode": "0444",
            "st_dev": identity[0], "st_ino": identity[1], "st_nlink": identity[3],
        })
    return {
        "schema": 2, "authority": "canonical-h-f04-stage-a-controls",
        "instrument_configuration": configuration,
        "instrument_configuration_sha256": PS.state_hash(configuration),
        "replica_identities": configuration.get("replica_identities"),
        "controls": controls,
    }


def _validate_bound_identities(receipt, configuration, identities):
    if (receipt.get("schema") != 2 or
            receipt.get("authority") != "canonical-h-f04-stage-a-controls" or
            receipt.get("instrument_configuration") != configuration or
            receipt.get("instrument_configuration_sha256") != PS.state_hash(configuration) or
            receipt.get("replica_identities") != configuration.get("replica_identities") or
            not isinstance(receipt.get("controls"), list) or
            len(receipt["controls"]) != len(MODES)):
        raise ValueError("H-F04 validation receipt is stale or tampered")
    for mode, path, identity, item in zip(MODES, summaries(), identities,
                                          receipt["controls"]):
        expected = {
            "control_identity": f"h-f04:{mode}:anonymous-a-vs-anonymous-b",
            "mode": mode, "path": path.relative_to(root()).as_posix(),
            "file_mode": "0444", "st_dev": identity[0], "st_ino": identity[1],
            "st_nlink": identity[3],
        }
        if not isinstance(item, dict) or any(
                type(item.get(key)) is not type(value) or item.get(key) != value
                for key, value in expected.items()):
            raise ValueError("H-F04 control summary identity does not match its receipt")


def _preflight(include_receipt):
    base, outputs = root(), root() / "outputs"
    try:
        PS.safe_dir(base)
        PS.safe_dir(outputs, base)
        for mode in MODES:
            PS.safe_dir(outputs / mode, base)
    except (PS.StoreError, OSError) as exc:
        raise ValueError(f"canonical H-F04 controls are unavailable: {exc}") from exc
    root_names = {"anonymous-a", "anonymous-b", "outputs", RECEIPT}
    expected_root = root_names if include_receipt else root_names - {RECEIPT}
    if _names(base) != expected_root or _names(outputs) != set(MODES):
        raise ValueError("canonical H-F04 control layout is missing or has extra entries")
    paths = ((root() / RECEIPT,) if include_receipt else ()) + summaries()
    return paths, [_inspect(path, base) for path in paths]


def require(configuration, raw=""):
    """Derive and verify the receipt-bound canonical pair before product reads."""
    validate_request(raw)
    paths, identities = _preflight(True)
    receipt_payload = _read_stable(paths[0], identities[0])
    receipt = _decode(receipt_payload, "H-F04 validation receipt")
    if receipt_payload != PS.json_bytes(receipt):
        raise ValueError("H-F04 validation receipt is stale or tampered")
    _validate_bound_identities(receipt, configuration, identities[1:])
    payloads = [_read_stable(path, identity)
                for path, identity in zip(paths[1:], identities[1:])]
    final_paths, final_identities = _preflight(True)
    if paths != final_paths or identities != final_identities:
        raise ValueError("canonical control authority changed during validation")
    for mode, payload in zip(MODES, payloads):
        _validate_summary(payload, mode, configuration)
    if receipt != _receipt(configuration, payloads, identities[1:]):
        raise ValueError("H-F04 validation receipt is stale or tampered")
    receipt_hash = hashlib.sha256(receipt_payload).hexdigest()
    return {mode: {
        "mode": mode, "passed": True, "instrument_configuration": configuration,
        "summary": str(path), "sha256": hashlib.sha256(payload).hexdigest(),
        "receipt": str(root() / RECEIPT), "receipt_sha256": receipt_hash,
    } for mode, path, payload in zip(MODES, summaries(), payloads)}


def finalize(configuration):
    """Atomically publish a receipt once both fixed controls have passed."""
    receipt_path = root() / RECEIPT
    if not all(os.path.lexists(path) for path in summaries()):
        if os.path.lexists(receipt_path):
            raise ValueError("H-F04 validation receipt exists without both controls")
        return None
    if os.path.lexists(receipt_path):
        return require(configuration)
    paths, identities = _preflight(False)
    payloads = [_read_stable(path, identity) for path, identity in zip(paths, identities)]
    final_paths, final_identities = _preflight(False)
    if paths != final_paths or identities != final_identities:
        raise ValueError("canonical control authority changed during validation")
    for mode, payload in zip(MODES, payloads):
        _validate_summary(payload, mode, configuration)
    PS.write(receipt_path, PS.json_bytes(_receipt(configuration, payloads, identities)))
    receipt_path.chmod(0o444)
    return require(configuration)
