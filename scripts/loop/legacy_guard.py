"""RF-00 fail-closed authorization for legacy product-loop entrypoints."""
import os
import re
from pathlib import Path
import path_guard as PG


REPO_ROOT = Path(__file__).resolve().parents[2]
LEDGER = REPO_ROOT / "openspec/changes/redesign-book-factory/tasks.md"
READY = {"READY", "DONE"}
STATUSES = {"TODO", "READY", "IN_PROGRESS", "REVIEW", "REVISE", "BLOCKED",
            "CONDITIONAL", "DONE", "SKIPPED"}
_HEADING = re.compile(r"^### (RF-\d{2}) — \S.*$", re.MULTILINE)
_RF_LIKE = re.compile(r"^#{3,}\s*RF-[^\n]*$", re.MULTILINE | re.IGNORECASE)
_STATUS_LINE = re.compile(r"^- Status:.*$", re.MULTILINE)
_STATUS = re.compile(r"- Status: `([A-Z_]+)`")
_ACCEPTED = (
    REPO_ROOT / "production-books",
    REPO_ROOT / "prompts",
    REPO_ROOT / "loop/config.yaml",
    REPO_ROOT / "loop/results.tsv",
    REPO_ROOT / "loop/learnings.md",
    REPO_ROOT / "loop/scores",
    REPO_ROOT / "loop/iterations",
)


def add_arguments(parser):
    parser.add_argument(
        "--redesign-authorized", action="store_true",
        help="explicitly authorize an isolated redesign stage (never the legacy product)",
    )
    parser.add_argument("--rf-stage", help="ready redesign ledger item, for example RF-23")
    parser.add_argument("--candidate-root", help="isolated candidate snapshot root")
    parser.add_argument(
        "--rf-dry-run", action="store_true",
        help="stop after authorization and target validation, before dispatch or writes",
    )


def _stop(detail):
    raise SystemExit(
        "RF-00 legacy guard: " + detail + ". Recovery state is controlled by "
        "openspec/changes/redesign-book-factory/tasks.md"
    )


def _statuses():
    if not LEDGER.is_file():
        _stop(f"authoritative ledger is missing: {LEDGER}")
    text = LEDGER.read_text(encoding="utf-8")
    headings = list(_HEADING.finditer(text))
    if len(headings) != len(list(_RF_LIKE.finditer(text))):
        _stop("authoritative ledger contains a malformed RF task heading")
    statuses = {}
    for index, heading in enumerate(headings):
        task = heading.group(1)
        if task in statuses:
            _stop(f"authoritative ledger contains duplicate task {task}")
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        lines = _STATUS_LINE.findall(text[heading.end():end])
        if len(lines) != 1:
            _stop(f"{task} must contain exactly one status (found {len(lines)})")
        status = _STATUS.fullmatch(lines[0])
        if status is None or status.group(1) not in STATUSES:
            _stop(f"{task} has an invalid status: {lines[0]}")
        statuses[task] = status.group(1)
    if "RF-23" not in statuses:
        _stop("authoritative ledger must contain exactly one RF-23 task")
    return statuses


def _inside(path, root):
    return path == root or root in path.parents


def _overlaps(left, right):
    return _inside(left, right) or _inside(right, left)


def require_authorized(args, *, entrypoint, pre_rf23_stage=None,
                       exact_candidate=None, allow_accepted_overlap=False,
                       require_in_progress=False):
    """Reject before config, endpoint, network, or write resolution."""
    if not args.redesign_authorized:
        _stop(f"{entrypoint} is paused; explicit redesign authorization is required")
    stage = (args.rf_stage or "").upper()
    if not re.fullmatch(r"RF-\d{2}", stage):
        _stop("--rf-stage must name one RF-NN ledger item")
    if not args.candidate_root:
        _stop("--candidate-root is required")
    candidate = PG.absolute(args.candidate_root)
    if exact_candidate is not None and candidate != PG.absolute(exact_candidate):
        _stop(f"candidate root must be exactly {PG.absolute(exact_candidate)}")
    statuses = _statuses()
    status = statuses.get(stage, "MISSING")
    allowed = {"IN_PROGRESS"} if require_in_progress else READY
    expected = "IN_PROGRESS" if require_in_progress else "READY"
    if status not in allowed:
        _stop(f"{stage} is {status}, not {expected}")
    if pre_rf23_stage is not None and stage != pre_rf23_stage:
        _stop(f"this non-prose operation requires {pre_rf23_stage} authorization")
    if pre_rf23_stage is None and statuses.get("RF-23") not in READY:
        _stop(f"legacy execution requires RF-23 READY (found {statuses.get('RF-23', 'MISSING')})")
    try:
        PG.safe_dir(candidate)
    except PG.PathError as exc:
        _stop(f"candidate root is unsafe: {exc}")
    for accepted in _ACCEPTED:
        if _overlaps(candidate, accepted.absolute()):
            if allow_accepted_overlap and exact_candidate is not None \
                    and candidate == PG.absolute(exact_candidate):
                continue
            _stop(f"candidate root overlaps accepted production/configuration: {accepted}")
    return candidate


def require_store_target(candidate, target):
    """Pre-RF23 store maintenance may write only to its isolated authorized root."""
    target = PG.absolute(target)
    try:
        PG.safe_dir(target)
    except PG.PathError as exc:
        _stop(f"accepted-store target is unsafe: {exc}")
    if target != candidate:
        _stop("--accepted-root must equal the isolated --candidate-root for RF-02 setup")
    return target


def require_output(candidate, target):
    """Reject aliases and escapes at a concrete output path."""
    if target is None or str(target).strip() == "":
        _stop("an isolated target path is missing")
    path = Path(os.path.abspath(target))
    if not _inside(path, candidate):
        _stop(f"target escapes candidate root: {path}")
    current = candidate
    for part in path.relative_to(candidate).parts:
        current /= part
        if os.path.lexists(current) and PG.aliased(os.lstat(current)):
            _stop(f"target contains a symlink or reparse alias: {current}")
    if not _inside(path.resolve(), candidate.resolve()):
        _stop(f"target escapes candidate root: {path.resolve()}")
    if path.is_file() and path.stat().st_nlink > 1:
        _stop(f"target is a multiply linked file: {path}")
    return path


def require_targets(candidate, *targets):
    """Require every potential write/product target to remain in the snapshot."""
    for target in targets:
        require_output(candidate, target)


def require_config_targets(candidate, cfg, *keys):
    require_targets(candidate, *(cfg.get(key) for key in keys))


def forward_arguments(args):
    return [
        "--redesign-authorized", "--rf-stage", args.rf_stage,
        "--candidate-root", str(Path(args.candidate_root).resolve()),
    ]


def dry_run(args, entrypoint):
    if not args.rf_dry_run:
        return False
    print(f"[RF-00] {entrypoint}: authorized isolated dispatch boundary; no dispatch or write")
    return True
