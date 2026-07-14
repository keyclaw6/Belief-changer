"""Pure RF-11 batch/start metadata contract validation."""
import os
from pathlib import Path

import pair_store as PS

SCHEMA = 1
FOLDER = "first-draft-batch"
RECEIPT = "receipt.json"
KEYS = {"schema", "state", "mode", "operation", "selection", "config",
        "baseline", "drafts", "pending", "receipt", "pair_sha256",
        "start_sha256", "responses", "call"}
CALL_KEYS = {"chapter", "path", "authority_sha256", "request_sha256"}


class BatchError(RuntimeError):
    pass


def relative(manifest, number):
    return f"{manifest['run']['book']}/chapters/chapter-{number:02d}.md"


def folder(root):
    return Path(root).absolute() / "evidence" / FOLDER


def start_marker(batch):
    body = {key: batch[key] for key in
            ("schema", "mode", "operation", "selection", "config")}
    return {**body, "start_sha256": PS.state_hash(body)}


def validate_pair(manifest, root):
    batch, start, state = (manifest.get("draft_batch"),
                           manifest.get("draft_batch_start"), manifest.get("state"))
    evidence = os.path.lexists(folder(root))
    if batch is None:
        if start is not None or state in ("DRAFTING", "BATCH_FROZEN") or evidence:
            raise BatchError("started draft batch metadata was removed or downgraded")
        return
    validate_shape(batch, manifest)
    expected = start_marker(batch)
    if start != expected or batch["start_sha256"] != expected["start_sha256"]:
        raise BatchError("draft batch start identity is missing or drifted")
    expected_state = "DRAFTING" if batch["state"] == "DRAFTING" else "BATCH_FROZEN"
    if state != expected_state and not (state == "SEALED" and expected_state == "BATCH_FROZEN"):
        raise BatchError("candidate state was downgraded from its draft batch")


def validate_shape(batch, manifest):
    if not isinstance(batch, dict) or set(batch) != KEYS \
            or batch.get("schema") != SCHEMA \
            or batch.get("state") not in ("DRAFTING", "FROZEN") \
            or batch.get("mode") not in ("api", "manual") \
            or batch.get("selection") != manifest["run"]["chapters"] \
            or manifest.get("operation") is None:
        raise BatchError("draft batch metadata is malformed or selection-drifted")
    drafts, selection = batch.get("drafts"), batch["selection"]
    if not isinstance(drafts, list) or [item.get("chapter") for item in drafts
                                       if isinstance(item, dict)] != selection[:len(drafts)]:
        raise BatchError("draft progress is out of order or contains a gap")
    baseline = batch.get("baseline")
    if not isinstance(baseline, list):
        raise BatchError("draft baseline is malformed")
    for item in [*baseline, *drafts]:
        if not _valid_entry(item) or item["path"] != relative(manifest, item["chapter"]):
            raise BatchError("draft chapter metadata is malformed")
    if [item["chapter"] for item in baseline] != selection:
        raise BatchError("draft baseline is incomplete or out of order")
    pending = batch.get("pending")
    if pending is not None and (len(drafts) == len(selection)
                                or pending.get("chapter") != selection[len(drafts)]
                                or not _valid_entry(pending)
                                or pending.get("path") != relative(
                                    manifest, pending.get("chapter"))):
        raise BatchError("pending draft is not the next selected chapter")
    _validate_state(batch, drafts, selection, pending)


def _validate_state(batch, drafts, selection, pending):
    frozen, descriptor = batch["state"] == "FROZEN", batch.get("receipt")
    if frozen != (pending is None and len(drafts) == len(selection)
                  and isinstance(descriptor, dict)
                  and set(descriptor) == {"path", "sha256", "receipt_hash"}
                  and descriptor.get("path") == f"evidence/{FOLDER}/{RECEIPT}"
                  and _valid_hash(descriptor.get("sha256"))
                  and _valid_hash(descriptor.get("receipt_hash"))
                  and _valid_hash(batch.get("pair_sha256"))):
        raise BatchError("draft batch state markers are inconsistent")
    if not frozen and (descriptor is not None or batch.get("pair_sha256") is not None):
        raise BatchError("drafting batch contains frozen state markers")
    responses, call = batch.get("responses"), batch.get("call")
    if not isinstance(responses, list) or any(not _valid_call(item, True)
                                              for item in responses) \
            or batch["mode"] == "api" and (len(responses) != len(drafts) or
                [item["chapter"] for item in responses] !=
                [item["chapter"] for item in drafts]):
        raise BatchError("durable model response history is malformed")
    if batch["mode"] == "manual" and (responses or call is not None):
        raise BatchError("manual draft batch contains API call state")
    if call is not None and (frozen or len(drafts) == len(selection)
                             or not _valid_call(call, False)
                             or call["chapter"] != selection[len(drafts)]
                             or call["authority_sha256"] != batch.get("start_sha256")):
        raise BatchError("in-flight model call identity is malformed")
    if batch["mode"] == "api" and pending is not None and call is None:
        raise BatchError("accepted API response lost its durable call identity")
    if not _valid_hash(batch.get("start_sha256")):
        raise BatchError("draft batch start hash is malformed")


def _valid_entry(item):
    value = item.get("sha256") if isinstance(item, dict) else None
    return isinstance(item, dict) and set(item) == {"chapter", "path", "sha256"} \
        and _valid_hash(value)


def _valid_hash(value):
    return isinstance(value, str) and len(value) == 64 \
        and not set(value) - set("0123456789abcdef")


def _valid_call(item, completed):
    keys = CALL_KEYS | ({"sha256", "response_sha256"} if completed else set())
    if not isinstance(item, dict) or set(item) != keys \
            or not isinstance(item.get("chapter"), int) \
            or item.get("path") != f"response-{item.get('chapter', 0):02d}.json":
        return False
    return all(_valid_hash(item.get(key)) for key in keys - {"chapter", "path"})
