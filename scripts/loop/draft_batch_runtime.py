"""RF-11 writer dispatch over one durable ordered batch."""
from pathlib import Path

import candidate_pair as CP
import commission_set as CS
import first_draft_batch as FB
import manual_dispatch as MD
import model_endpoint as ME
import pair_store as PS
import writer_context as WC
import writer_refusal as WR
import judges
import legacy_guard as LG


def _capture(candidate, book, selected):
    manifest = CP.load(candidate)
    batch = manifest.get("draft_batch")
    if batch is not None:
        WR.require_clear(candidate, batch)
    if batch is None:
        authority = WC.capture(candidate, book, selected)
    else:
        receipt = manifest.get("operation", {}).get("receipt_hash")
        authority = WC.resume_authority(candidate, book, selected, receipt)
    WC.require_fresh(candidate, authority)
    return authority, batch


def write_chapters(cfg, book, selected, candidate, interrupt=None):
    """Generate only the remaining selected chapters in canonical order."""
    try:
        authority, batch = _capture(candidate, book, selected)
    except (CS.CommissionSetError, CP.PairError, PS.StoreError,
            WC.WriterContextError, WR.RefusalError, OSError) as exc:
        raise SystemExit(f"[run] writer blocked before dispatch: {exc}") from exc
    base_url, key = judges.endpoint()
    try:
        WC.require_fresh(candidate, authority)
        if batch is None:
            WC.persist_manual_receipt(candidate, authority)
            batch = FB.begin(candidate, authority, "api" if key else "manual", interrupt)
        else:
            batch = FB.begin(candidate, authority, batch["mode"])
    except (WC.WriterContextError, FB.BatchError) as exc:
        raise SystemExit(f"[run] writer blocked after endpoint resolution: {exc}") from exc
    if batch["state"] == "FROZEN":
        FB.require_frozen_batch(candidate)
        return True
    if len(batch["drafts"]) == len(batch["selection"]):
        FB.prepare(candidate)
        return True
    if not key:
        if batch is not None and batch["mode"] != "manual":
            raise SystemExit("[run] API batch cannot resume without its writer endpoint")
        WR.prepare_manual(candidate)
        MD.writer(cfg, CP.candidate_tree(candidate), book, selected, authority)
        return False
    if batch["mode"] != "api":
        raise SystemExit("[run] manual writer handoff cannot become an API batch")
    model, reasoning = cfg["writer_model"], cfg.get("writer_reasoning", "none")
    try:
        remaining = FB.prepare(candidate)
    except (FB.BatchError, PS.StoreError) as exc:
        raise SystemExit(f"[run] writer resume failed closed: {exc}") from exc
    for number in remaining:
        out = Path(book) / f"chapters/chapter-{number:02d}.md"
        LG.require_output(candidate, out)
        try:
            WC.require_fresh(candidate, authority)
            content = WC.build(WC.inputs(candidate, book, authority, number))
        except (CP.PairError, WC.WriterContextError, OSError, UnicodeError) as exc:
            raise SystemExit(f"[run] writer input failed closed: {exc}") from exc
        print(f"[run] writing ch{number} via {model} ...")
        request = {"chapter": number, "endpoint": base_url.rstrip("/"),
                   "model": model, "reasoning": reasoning,
                   "content_sha256": PS.sha(content.encode("utf-8")),
                   "max_tokens": 16000, "temperature": 0.7}
        try:
            reply = FB.durable_call(candidate, number, request, lambda: ME.chat(
                base_url, key, model, content, reasoning, max_tokens=16000,
                temperature=0.7, retries=1), interrupt)
            WR.capture_api(candidate, number, reply, interrupt)
            WC.require_fresh(candidate, authority)
            words = FB.accept_response(candidate, number, interrupt)
        except WR.RoutedRefusal as exc:
            raise SystemExit(f"[run] {exc}") from exc
        except WR.RefusalError as exc:
            raise SystemExit(f"[run] invalid writer route refusal: {exc}") from exc
        except WC.WriterContextError as exc:
            raise SystemExit(f"[run] writer output failed closed: {exc}") from exc
        except FB.BatchError as exc:
            raise SystemExit(f"[run] writer returned an incomplete response — that is a "
                             f"report or refusal, not a chapter. NOT saved: {exc}") from exc
        print(f"[run] wrote {out} ({words} words)")
    return True
