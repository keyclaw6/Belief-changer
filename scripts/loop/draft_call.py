"""Durable RF-11 model-call marker and exact raw response envelope."""
import base64
import json
import os

import draft_batch_state as S
import pair_store as PS

SCHEMA = 1
ENVELOPE_KEYS = {"schema", "chapter", "authority_sha256", "request_sha256",
                 "response_sha256", "response_b64"}


def marker(batch, number, request):
    return {"chapter": number, "path": f"response-{number:02d}.json",
            "authority_sha256": batch["start_sha256"],
            "request_sha256": PS.state_hash(request)}


def _path(root, value):
    return S.folder(root) / value["path"]


def _envelope(value, raw):
    body = {"schema": SCHEMA, "chapter": value["chapter"],
            "authority_sha256": value["authority_sha256"],
            "request_sha256": value["request_sha256"],
            "response_sha256": PS.sha(raw),
            "response_b64": base64.b64encode(raw).decode("ascii")}
    return PS.json_bytes(body)


def _decode(data, value):
    try:
        body = json.loads(data)
        raw = base64.b64decode(body["response_b64"], validate=True)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise S.BatchError(f"durable model response is malformed: {exc}") from exc
    if set(body) != ENVELOPE_KEYS or body["schema"] != SCHEMA \
            or body["chapter"] != value["chapter"] \
            or body["authority_sha256"] != value["authority_sha256"] \
            or body["request_sha256"] != value["request_sha256"] \
            or body["response_sha256"] != PS.sha(raw):
        raise S.BatchError("durable model response identity mismatch")
    return raw


def read(root, value):
    path, temp = _path(root, value), _path(root, value).with_name(
        f".{value['path']}.rf02-tmp")
    if os.path.lexists(path) and os.path.lexists(temp):
        raise S.BatchError("model response has both final and staged artifacts")
    if os.path.lexists(path):
        data = PS._safe_file(path, S.folder(root)).read_bytes()
    elif os.path.lexists(temp):
        data = PS._safe_file(temp, S.folder(root)).read_bytes()
        if os.lstat(temp).st_uid != os.lstat(S.folder(root)).st_uid:
            raise S.BatchError("model response staging artifact has the wrong owner")
        _decode(data, value)
        S.write_snapshot(root, path, data)
    else:
        raise S.BatchError("in-flight model call has no durable response; replay is ambiguous")
    raw = _decode(data, value)
    descriptor = {**value, "sha256": PS.sha(data), "response_sha256": PS.sha(raw)}
    return raw, descriptor


def invoke(root, manifest, batch, number, request, callback, interrupt=None):
    """Persist the exact callback response before exposing it to the runtime."""
    wanted = marker(batch, number, request)
    if batch["call"] is not None:
        if batch["call"] != wanted:
            raise S.BatchError("resumed model request differs from its in-flight identity")
        raw, _ = read(root, wanted)
        try:
            return raw.decode("utf-8")
        except UnicodeError as exc:
            raise S.BatchError("durable model response is not UTF-8") from exc
    if batch["pending"] is not None:
        raise S.BatchError("cannot start a model call while draft progress is pending")
    manifest = S.save(root, manifest, {**batch, "call": wanted}, interrupt)
    boundary = interrupt or (lambda _step: None)
    boundary("call-marked")
    raw = callback()
    boundary("response-received")
    if not isinstance(raw, str):
        raise S.BatchError("model callback returned no text")
    try:
        response = raw.encode("utf-8")
    except UnicodeError as exc:
        raise S.BatchError("model callback returned non-UTF-8 text") from exc
    data = _envelope(wanted, response)
    S.write_snapshot(root, _path(root, wanted), data, boundary)
    boundary("response-staged")
    boundary("response-returning")
    return raw
