"""Derive one complete stable RF-02 factory view from a validated root."""
import os
import re
from pathlib import Path

import loopcfg
import pair_store as PS


class ContractError(RuntimeError):
    pass


def _store_error(call, *args):
    try:
        return call(*args)
    except PS.StoreError as exc:
        raise ContractError(str(exc)) from exc


def valid_run(run, experiment_id):
    keys = {"experiment_id", "iteration_id", "book", "chapters", "config"}
    chapters = run.get("chapters") if isinstance(run, dict) else None
    return isinstance(run, dict) and set(run) == keys \
        and run.get("experiment_id") == experiment_id \
        and isinstance(run.get("iteration_id"), (int, str)) \
        and isinstance(run.get("book"), str) \
        and re.fullmatch(r"production-books/[a-z0-9]+(?:-[a-z0-9]+)*", run["book"]) \
        and isinstance(run.get("config"), str) and run["config"] \
        and isinstance(chapters, list) and chapters \
        and all(type(number) is int and number > 0 for number in chapters) \
        and len(chapters) == len(set(chapters)) and chapters == sorted(chapters)


def relative(value, root: Path) -> str:
    path, root = Path(value), Path(root).absolute()
    absolute = path if path.is_absolute() else root / path
    try:
        rel = Path.absolute(absolute).relative_to(root)
    except ValueError as exc:
        raise ContractError(f"contract path is outside operation root: {value}") from exc
    if ".." in rel.parts or not rel.parts:
        raise ContractError(f"invalid contract path: {value}")
    return rel.as_posix()


def _file(path, root, label):
    try:
        return PS._safe_file(path, root)
    except PS.StoreError as exc:
        raise ContractError(f"{label}: {exc}") from exc


def _files(path, root, label):
    try:
        return PS.tree_files(path, root)
    except PS.StoreError as exc:
        raise ContractError(f"{label}: {exc}") from exc


def evaluation_paths(cfg, root: Path) -> list[str]:
    root = Path(root).absolute()
    rubric = relative(cfg.get("judge_rubric", ""), root)
    _file(root / rubric, root, "judge rubric")
    ref_dir = relative(cfg.get("reference_dir", ""), root)
    ref_root = root / ref_dir
    paths = [rubric]
    for key, label in (("product_effect_rubric", "product-effect rubric"),
                       ("product_effect_absolute_rubric", "absolute product-effect rubric")):
        product_rubric = cfg.get(key)
        if product_rubric:
            product_rubric = relative(product_rubric, root)
            _file(root / product_rubric, root, label)
            paths.append(product_rubric)
    for path in _files(ref_root, root, "reference directory"):
        if path.name == "reference-metrics.json" or path.suffix.lower() in (".md", ".txt"):
            paths.append(path.relative_to(root).as_posix())
    metrics = f"{ref_dir}/reference-metrics.json"
    if metrics not in paths:
        raise ContractError(f"reference metrics are missing: {root / metrics}")
    for key in ("results_tsv", "causal_results_jsonl"):
        results = cfg.get(key)
        if not results:
            continue
        result_rel = relative(results, root)
        if os.path.lexists(root / result_rel):
            _file(root / result_rel, root, "decision history")
            paths.append(result_rel)
    return sorted(set(paths))


def workshop_entries(root, book):
    root = Path(root).absolute()
    book_rel = relative(book, root)
    parts = Path(book_rel).parts
    if len(parts) != 2 or parts[0] != "production-books" or parts[1] in ("", ".", ".."):
        raise ContractError(f"book is not a stable production-books/<slug> workshop: {book}")
    workshop = root / book_rel
    files = _files(workshop, root, "book workshop")
    _file(workshop / "master-plan.md", root, "master plan")
    chapters = _files(workshop / "chapters", root, "chapter directory")
    if not any(path.name.startswith("chapter-") and path.suffix == ".md" for path in chapters):
        raise ContractError(f"no product chapters found: {workshop / 'chapters'}")
    return book_rel, [{"group": "product", "path": path.relative_to(root).as_posix()}
                      for path in files]


def derive(pair_root, book, config="loop/config.yaml", carry=(), evaluation_root=None):
    """Return every config asset and complete workshop at stable relative paths."""
    del carry
    root = Path(pair_root).absolute()
    _store_error(PS.safe_dir, root)
    config_rel = relative(config, root)
    config_path = _file(root / config_rel, root, "loop config")
    prompt_files = _files(root / "prompts", root, "prompt assets")
    production_files = _files(root / "production-books", root, "production workshops")
    book_rel, _ = workshop_entries(root, book)
    cfg = loopcfg.load(config_path)
    groups = {config_rel: "config"}
    for path in prompt_files:
        groups[path.relative_to(root).as_posix()] = "config"
    for path in production_files:
        groups[path.relative_to(root).as_posix()] = "product"
    pair = [{"group": groups[path], "path": path} for path in sorted(groups)]
    evaluation = evaluation_paths(cfg, Path(evaluation_root or root))
    return {"pair": pair, "evaluation": evaluation, "config": config_rel,
            "book": book_rel}
