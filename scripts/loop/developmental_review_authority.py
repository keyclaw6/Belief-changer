"""Resolve RF-06/RF-09/RF-11/RF-12 authority into one RF-13 task."""
from pathlib import Path

import candidate_pair as CP
import commission_set as CS
import developmental_review_contract as C
import draft_batch_state as DS
import first_draft_batch as FB
import grounded_review as GR
import loopcfg
import pair_store as PS
import writer_operation as WO


class AuthorityError(RuntimeError):
    pass


def _audit(root, manifest):
    path = CP.evidence_tree(root) / CS.RECEIPT
    data = PS._safe_file(path, root).read_bytes()
    audit = C.loads(data.decode("utf-8"), "commission audit receipt")
    body = {key: value for key, value in audit.items() if key != "receipt_hash"}
    if audit.get("receipt_hash") != PS.state_hash(body) or audit.get("state") != "PASSED":
        raise AuthorityError("RF-09 commission authority is stale or invalid")
    writer = C.loads(WO.read(root, manifest["operation"]), "writer operation receipt")
    wanted = {"path": f"evidence/{CS.RECEIPT}",
              "receipt_hash": audit["receipt_hash"], "sha256": PS.sha(data)}
    if writer.get("audit") != wanted:
        raise AuthorityError("writer operation does not bind the RF-09 commission receipt")
    return audit, writer


def _config(root, manifest, tree, supplied):
    path = CP.require_member(root, tree / manifest["run"]["config"], "config", manifest)
    cfg = loopcfg.load(path)
    reviewer = C.model(cfg)
    if supplied is not None and C.model(supplied) != reviewer:
        raise AuthorityError("developmental reviewer runtime metadata differs from pinned config")
    return cfg, reviewer, {"path": manifest["run"]["config"],
                           "sha256": PS.sha(path.read_bytes()),
                           "values_sha256": PS.state_hash(cfg)}


def _card(root, manifest, tree, audit, plan, number):
    chapter_id = f"C-{number:02d}"
    try:
        card = CS._section(plan, "C", number)
        transition = C.card_transition(chapter_id, card)
    except (CS.CommissionSetError, C.ContractError) as exc:
        raise AuthorityError(f"chapter {number}: reader-state card is invalid: {exc}") from exc
    if audit.get("bindings", {}).get("plan_sha256") != PS.sha(plan.encode("utf-8")):
        raise AuthorityError("RF-09 plan binding is stale")
    plan_path = f"{manifest['run']['book']}/master-plan.md"
    CP.require_member(root, tree / plan_path, "product", manifest)
    return card, transition, {**transition, "path": plan_path,
                              "sha256": PS.sha(card.encode("utf-8"))}


def _commission(root, manifest, tree, audit, writer, number):
    chapter_id = f"C-{number:02d}"
    matches = [item for item in writer.get("commissions", [])
               if isinstance(item, dict) and item.get("chapter") == number]
    if len(matches) != 1:
        raise AuthorityError(f"chapter {number}: commission binding is missing or ambiguous")
    item = matches[0]
    data = CP.require_member(root, tree / item["path"], "product", manifest).read_bytes()
    text = data.decode("utf-8")
    normalized = PS.sha(text.strip().encode("utf-8"))
    if item.get("sha256") != PS.sha(data) \
            or audit.get("bindings", {}).get("commissions", {}).get(chapter_id) != normalized:
        raise AuthorityError(f"chapter {number}: commission hash is stale")
    return text, {"chapter_id": chapter_id, "path": item["path"],
                  "sha256": PS.sha(data)}


def _draft(root, frozen, number):
    matches = [item for item in frozen["batch"]["drafts"] if item["chapter"] == number]
    if len(matches) != 1:
        raise AuthorityError(f"chapter {number}: frozen draft binding is missing")
    path = DS.folder(root) / f"chapter-{number:02d}.md"
    data = PS._safe_file(path, DS.folder(root)).read_bytes()
    if PS.sha(data) != matches[0]["sha256"]:
        raise AuthorityError(f"chapter {number}: frozen draft hash is stale")
    return data.decode("utf-8"), dict(matches[0])


def load(root, supplied_cfg=None):
    root = Path(root).absolute()
    try:
        frozen = FB.require_frozen_batch(root)
        grounded = GR.require_complete(root)
        manifest, tree = CP.load(root), CP.candidate_tree(root)
        audit, writer = _audit(root, manifest)
        _, reviewer, config = _config(root, manifest, tree, supplied_cfg)
        prompt_path = CP.require_member(root, tree / C.PROMPT, "config", manifest)
        prompt = prompt_path.read_text(encoding="utf-8")
        plan_path = tree / manifest["run"]["book"] / "master-plan.md"
        plan = CP.require_member(root, plan_path, "product", manifest).read_text(encoding="utf-8")
        selection, chapters, cards, commissions, drafts = (
            manifest["run"]["chapters"], [], [], [], [])
        if selection != frozen["batch"]["selection"]:
            raise AuthorityError("RF-11 selection differs from the operation selection")
        for number in selection:
            card, transition, card_binding = _card(
                root, manifest, tree, audit, plan, number)
            commission, commission_binding = _commission(
                root, manifest, tree, audit, writer, number)
            draft, draft_binding = _draft(root, frozen, number)
            chapters.append({"number": number, **transition,
                             "reader_state_card": card, "commission": commission,
                             "frozen_draft": draft})
            cards.append(card_binding)
            commissions.append(commission_binding)
            drafts.append(draft_binding)
        grounded_path = GR.receipt_path(root)
        grounded_data = PS._safe_file(grounded_path, GR.folder(root)).read_bytes()
        identity = {
            "operation": {"id": PS.state_hash({"root": str(root),
                "batch": frozen["batch"]["operation"], "grounded": grounded["receipt_hash"]}),
                "batch_sha256": PS.state_hash(frozen["batch"]["operation"])},
            "generation": manifest["accepted_generation"], "config": config,
            "selection": selection}
        task = C.task(C.make_task(identity, reviewer, prompt, chapters))
        common = {**identity, "run_sha256": PS.state_hash(manifest["run"]),
                  "reviewer": reviewer,
                  "rf11_receipt_hash": frozen["receipt_hash"],
                  "rf09_receipt_hash": audit["receipt_hash"],
                  "rf12_receipt": {"path": f"evidence/{GR.C.FOLDER}/{GR.C.RECEIPT}",
                      "sha256": PS.sha(grounded_data),
                      "receipt_hash": grounded["receipt_hash"]},
                  "cards": cards, "commissions": commissions, "drafts": drafts,
                  "prompt_sha256": PS.sha(prompt.encode("utf-8")),
                  "schema_sha256": PS.sha(PS.json_bytes(C.output_schema())),
                  "rules_sha256": PS.state_hash(C.RULES)}
        return task, common
    except AuthorityError:
        raise
    except (CP.PairError, FB.BatchError, GR.GroundedReviewError, PS.StoreError,
            WO.OperationError, OSError, UnicodeError, KeyError, TypeError,
            C.ContractError, SystemExit) as exc:
        raise AuthorityError(f"cannot resolve developmental authority: {exc}") from exc
