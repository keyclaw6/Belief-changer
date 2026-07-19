"""RF-11 ordered first-draft progress and immutable batch evidence."""
import json
import os
import stat
import candidate_pair as CP
import draft_call as DC
import draft_batch_state as S
import pair_store as PS
import writer_refusal as WR

BatchError = S.BatchError
validate_draft = S.validate_draft
def begin(root, authority, mode, interrupt=None):
    manifest = CP.load(root)
    if authority is None:
        authority_sha256 = manifest["operation"]["receipt_hash"]
    elif isinstance(authority, str) and len(authority) == 64 \
            and not set(authority) - set("0123456789abcdef"):
        authority_sha256 = authority
    else:
        try: authority_sha256 = PS.state_hash(authority)
        except TypeError:
            authority_sha256 = manifest["operation"]["receipt_hash"]
    return S.begin(root, mode, authority_sha256, interrupt)
def _recover_pending(root, manifest, batch, interrupt=None):
    pending = batch["pending"]
    if pending is None:
        return manifest, batch
    number, wanted = pending["chapter"], pending["sha256"]
    snapshot = S.folder(root) / f"chapter-{number:02d}.md"
    work = CP.candidate_tree(root) / pending["path"]
    response = None
    accepted = None
    if batch["mode"] == "api":
        raw, response = DC.read(root, batch["call"])
        accepted = S.clean_response(raw)
        if PS.sha(accepted) != wanted:
            raise BatchError("durable model response differs from accepted draft identity")
    staged = S.safe_pending(snapshot, S.folder(root), wanted) \
        if os.path.lexists(S.folder(root)) else None
    if os.path.lexists(snapshot):
        data = PS._safe_file(snapshot, S.folder(root)).read_bytes()
    elif staged is not None:
        data = staged
        S.write_snapshot(root, snapshot, data)
    elif accepted is not None:
        data = accepted
        S.write_snapshot(root, snapshot, data)
    else:
        baseline = next(item["sha256"] for item in batch["baseline"]
                        if item["chapter"] == number)
        if PS.sha(PS._safe_file(work, CP.candidate_tree(root)).read_bytes()) != baseline:
            raise BatchError("pending draft bytes disappeared after the product changed")
        manifest = S.save(root, manifest, {**batch, "pending": None})
        return manifest, manifest["draft_batch"]
    if PS.sha(data) != wanted:
        raise BatchError("pending draft hash differs from its operation state")
    validate_draft(data, number)
    current = PS._safe_file(work, CP.candidate_tree(root)).read_bytes()
    baseline = next(item["sha256"] for item in batch["baseline"]
                    if item["chapter"] == number)
    work_staged = S.safe_pending(work, CP.candidate_tree(root), wanted)
    if PS.sha(current) == baseline or work_staged is not None:
        PS.write(work, data)
    elif PS.sha(current) != wanted:
        raise BatchError("pending draft product bytes were overwritten")
    committed = {**batch, "drafts": [*batch["drafts"], pending], "pending": None}
    if response is not None:
        committed.update(responses=[*batch["responses"], response], call=None)
    boundary = interrupt or (lambda _step: None)
    boundary("progress-committing")
    manifest = S.save(root, manifest, committed, boundary)
    return manifest, manifest["draft_batch"]
def _verify_drafting(root, allow_unrecorded=False, allow_receipt=False):
    manifest = CP.load(root)
    batch = manifest.get("draft_batch")
    if not batch or batch.get("state") != "DRAFTING":
        raise BatchError("operation has no in-progress first-draft batch")
    WR.require_clear(root, batch)
    S.identity(root, manifest, batch)
    manifest, batch = _recover_pending(root, manifest, batch)
    expected = [{"group": "evidence", "path": S.START}]
    for item in batch["drafts"]:
        number = item["chapter"]
        snapshot = S.folder(root) / f"chapter-{number:02d}.md"
        data = PS._safe_file(snapshot, S.folder(root)).read_bytes()
        work = PS._safe_file(CP.candidate_tree(root) / item["path"],
                             CP.candidate_tree(root)).read_bytes()
        if PS.sha(data) != item["sha256"] or PS.sha(work) != item["sha256"]:
            raise BatchError(f"completed draft {number} was overwritten")
        validate_draft(data, number)
        expected.append({"group": "evidence", "path": snapshot.name})
    for response in batch["responses"]:
        _, actual = DC.read(root, response)
        if actual != response:
            raise BatchError("completed model response identity changed")
        expected.append({"group": "evidence", "path": response["path"]})
    if batch["call"] is not None:
        DC.read(root, batch["call"])
        expected.append({"group": "evidence", "path": batch["call"]["path"]})
    if allow_receipt and os.path.lexists(S.folder(root) / S.RECEIPT):
        expected.append({"group": "evidence", "path": S.RECEIPT})
    if os.path.lexists(S.folder(root)):
        PS.exact_tree(S.folder(root), expected)
    baseline = {item["chapter"]: item for item in batch["baseline"]}
    if not allow_unrecorded:
        for number in batch["selection"][len(batch["drafts"]):]:
            path = CP.candidate_tree(root) / baseline[number]["path"]
            if PS.sha(PS._safe_file(path, CP.candidate_tree(root)).read_bytes()) \
                    != baseline[number]["sha256"]:
                raise BatchError("unrecorded or mixed draft bytes are present")
    return manifest, batch
def accept(root, number, data, allow_unrecorded=False, interrupt=None):
    manifest, batch = _verify_drafting(root, allow_unrecorded)
    remaining = batch["selection"][len(batch["drafts"]):]
    if not remaining or number != remaining[0]:
        raise BatchError("draft acceptance is out of order or outside the selection")
    if batch["mode"] == "api":
        raw, _ = DC.read(root, batch["call"])
        if S.clean_response(raw) != data:
            raise BatchError("accepted draft bytes differ from durable model response")
    validate_draft(data, number)
    pending = S.entry(manifest, number, data)
    manifest = S.save(root, manifest, {**batch, "pending": pending}, interrupt)
    (interrupt or (lambda _step: None))("pending-recorded")
    (interrupt or (lambda _step: None))("snapshot-preparing")
    S.write_snapshot(root, S.folder(root) / f"chapter-{number:02d}.md", data, interrupt)
    (interrupt or (lambda _step: None))("evidence-written")
    PS.write(CP.candidate_tree(root) / pending["path"], data)
    (interrupt or (lambda _step: None))("product-written")
    _, batch = _recover_pending(root, CP.load(root), manifest["draft_batch"], interrupt)
    (interrupt or (lambda _step: None))("progress-recorded")
    return batch["drafts"][-1]
def durable_call(root, number, request, callback, interrupt=None):
    manifest, batch = _verify_drafting(root)
    remaining = batch["selection"][len(batch["drafts"]):]
    if batch["mode"] != "api" or not remaining or number != remaining[0]:
        raise BatchError("model call is outside the next API draft assignment")
    return DC.invoke(root, manifest, batch, number, request, callback, interrupt)
def accept_response(root, number, interrupt=None):
    batch = CP.load(root)["draft_batch"]
    raw, _ = DC.read(root, batch["call"])
    data = S.clean_response(raw)
    words = validate_draft(data, number)
    accept(root, number, data, interrupt=interrupt)
    return words


def accept_manual(root):
    WR.capture_manual(root)
    _, batch = _verify_drafting(root, True)
    if batch["mode"] != "manual":
        raise BatchError("manual completion cannot enter an API batch")
    baseline = {item["chapter"]: item for item in batch["baseline"]}
    remaining = batch["selection"][len(batch["drafts"]):]
    changed = []
    for number in remaining:
        item = baseline[number]
        data = PS._safe_file(CP.candidate_tree(root) / item["path"],
                             CP.candidate_tree(root)).read_bytes()
        changed.append(PS.sha(data) != item["sha256"])
    if False in changed and True in changed[changed.index(False):]:
        raise BatchError("manual drafts contain an out-of-order gap")
    count = changed.index(False) if False in changed else len(changed)
    for number in remaining[:count]:
        item = baseline[number]
        data = PS._safe_file(CP.candidate_tree(root) / item["path"],
                             CP.candidate_tree(root)).read_bytes()
        accept(root, number, data, allow_unrecorded=True)
    return remaining_chapters(root)


def remaining_chapters(root):
    manifest = CP.load(root)
    batch = manifest.get("draft_batch") or {}
    S.validate_shape(batch, manifest)
    return batch["selection"][len(batch["drafts"]):]


def prepare(root):
    """Verify resumable progress before another writer callback can run."""
    try:
        batch = CP.load(root).get("draft_batch") or {}
        complete = len(batch.get("drafts", ())) == len(batch.get("selection", ()))
        _, batch = _verify_drafting(root, allow_receipt=complete)
    except (PS.StoreError, OSError) as exc:
        raise BatchError(f"draft progress layout is invalid: {exc}") from exc
    return batch["selection"][len(batch["drafts"]):]


def _receipt_body(batch):
    return {key: value for key, value in batch.items() if key != "receipt"}


def freeze(root, interrupt=None):
    manifest, batch = _verify_drafting(root, allow_receipt=True)
    if len(batch["drafts"]) != len(batch["selection"]):
        raise BatchError("cannot freeze a partial first-draft batch")
    pair_hash = PS.state_hash(PS.exact_tree(CP.candidate_tree(root), CP._members(manifest)))
    frozen = {**batch, "state": "FROZEN", "pair_sha256": pair_hash}
    body = {"schema": S.SCHEMA, "batch": _receipt_body(frozen)}
    body["receipt_hash"] = PS.state_hash(body)
    data = PS.json_bytes(body)
    S.write_snapshot(root, S.folder(root) / S.RECEIPT, data)
    frozen["receipt"] = {"path": f"evidence/{S.FOLDER}/{S.RECEIPT}",
                         "sha256": PS.sha(data), "receipt_hash": body["receipt_hash"]}
    for path in PS.tree_files(S.folder(root)):
        path.chmod(0o444)
    S.save(root, manifest, frozen, interrupt, state="BATCH_FROZEN")
    return require_frozen_batch(root)


def _require_frozen_batch(root):
    manifest = CP.load(root)
    batch = manifest.get("draft_batch")
    WR.require_clear(root, batch)
    if not batch or batch.get("state") != "FROZEN" or batch.get("pending") is not None:
        raise BatchError("complete first-draft batch is not frozen")
    S.identity(root, manifest, batch)
    if len(batch["drafts"]) != len(batch["selection"]):
        raise BatchError("frozen first-draft batch is partial")
    descriptor = batch.get("receipt")
    if not isinstance(descriptor, dict) or set(descriptor) != {"path", "sha256", "receipt_hash"}:
        raise BatchError("frozen first-draft receipt descriptor is malformed")
    receipt = S.folder(root) / S.RECEIPT
    try:
        data = PS._safe_file(receipt, S.folder(root)).read_bytes()
        body = json.loads(data)
        recorded = body.pop("receipt_hash")
    except (PS.StoreError, OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise BatchError(f"frozen first-draft receipt is invalid: {exc}") from exc
    expected_body = {"schema": S.SCHEMA, "batch": _receipt_body(batch)}
    expected_descriptor = {"path": f"evidence/{S.FOLDER}/{S.RECEIPT}",
                           "sha256": PS.sha(data), "receipt_hash": recorded}
    if descriptor != expected_descriptor or recorded != PS.state_hash(body) \
            or body != expected_body:
        raise BatchError("frozen first-draft receipt identity mismatch")
    entries = ([{"group": "evidence", "path": S.START}] +
               [{"group": "evidence", "path": f"chapter-{n:02d}.md"}
                for n in batch["selection"]] +
               [{"group": "evidence", "path": item["path"]}
                for item in batch["responses"]] +
               [{"group": "evidence", "path": S.RECEIPT}])
    hashes = {item["path"]: item["sha256"]
              for item in PS.exact_tree(S.folder(root), entries)}
    for item in batch["drafts"]:
        name = f"chapter-{item['chapter']:02d}.md"
        draft = PS._safe_file(S.folder(root) / name, S.folder(root))
        if hashes.get(name) != item["sha256"]:
            raise BatchError("frozen first-draft bytes changed")
        validate_draft(draft.read_bytes(), item["chapter"])
    for path in PS.tree_files(S.folder(root)):
        if stat.S_IMODE(os.lstat(path).st_mode) != 0o444:
            raise BatchError("frozen first-draft evidence mode is not canonical 0444")
    return {**body, "receipt_hash": recorded}
def require_frozen_batch(root):
    try:
        return _require_frozen_batch(root)
    except (CP.PairError, PS.StoreError, OSError) as exc:
        raise BatchError(f"frozen first-draft layout is invalid: {exc}") from exc
