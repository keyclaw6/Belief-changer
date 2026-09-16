"""Frozen runs and content-addressed, dependency-bound role tasks.

The human/agent orchestrator calls one explicit unit at a time. Nothing in this
module starts background jobs, changes a champion, or reads a legacy live plan.
"""
from __future__ import annotations
import json
import shutil
import subprocess
from pathlib import Path
from .common import (FactoryError, atomic_bytes, canonical, confined, digest, exact_keys, file_hash,
                     identifier, lock, nonempty, now, read_json, require, seal, text_hash, unseal)
from .schema import (EXTERNAL_ROLES, ROLES, REVIEW_ROLES, validate_brief, validate_plan, validate_research,
                     validate_review, validate_state, validate_writer, validate_config, validate_metadata)
from .quality import assemble_book, apply_front_repairs, base_front_matter, edit_book, screen, split_operations

PROMPTS = {"planner": "master-plan-skill-v2.md", "plan-reviewer": "master-plan-reviewer-v2.md",
           "writer": "chapter-writer.md", "chapter-reviewer": "chapter-reviewer.md",
           "evidence-reviewer": "evidence-reviewer.md", "state-editor": "reader-state.md",
           "book-editor": "book-editor.md", "final-auditor": "final-auditor.md"}
REQUIRED_CODE = ["scripts/factory.py", "factory/config.json", "factory/research-access.json"]


def active_files(repo: Path) -> list[str]:
    paths = [*REQUIRED_CODE]
    for glob in ("scripts/bc_factory/*.py", "prompts/*.md", "loop/judges/*.md"):
        paths.extend(p.relative_to(repo).as_posix() for p in repo.glob(glob) if p.is_file())
    return sorted(set(paths))


def prepare(repo: Path, run_id: str, brief: dict, research: dict, parent: str | None = None,
            fixture: bool = False, research_preflight: dict | None = None,
            research_revision_of: str | None = None, remediation_of: str | None = None) -> Path:
    repo = repo.resolve()
    identifier(run_id)
    if parent is not None:
        identifier(parent)
    evidence_feedback = None
    remediation = None
    if remediation_of is not None:
        identifier(remediation_of)
        require(run_id != remediation_of, "Remediation needs a new run ID; source runs are immutable")
        require(research_revision_of is None, "Remediation inherits frozen research; it is not a research revision")
        require(research_preflight is None, "Remediation retrieves nothing new; no fresh preflight is consumed")
        source = Run(repo, remediation_of)
        require(source.manifest["run_id"] == remediation_of, "Source run identity mismatch")
        src_audit_no, src_audit = source.latest("final-auditor")
        require(src_audit["output"]["verdict"] == "REVISE",
                "Remediation needs a prior fixable REVISE audit; BLOCKED stops the run and ACCEPT needs nothing")
        src_asm_no = source.latest_assembly_version()
        require(src_asm_no == src_audit_no,
                "Source audit does not match its latest assembly; remediate only clean audit states")
        require(digest(brief) == digest(source.brief), "Remediation brief must equal the source frozen brief")
        require(digest(research) == digest(source.research), "Remediation research must equal the source frozen research")
        remediation = {"source_run": remediation_of,
                       "source_manifest_sha256": digest(source.manifest),
                       "source_audit_key": f"final-auditor-r{src_audit_no:02d}",
                       "source_audit_sha256": file_hash(source.root / "results" / f"final-auditor-r{src_audit_no:02d}.json"),
                       "source_assembly_rel": f"assembly/assembly-r{src_asm_no:02d}.json",
                       "source_assembly_sha256": file_hash(source.root / "assembly" / f"assembly-r{src_asm_no:02d}.json")}
    if research_revision_of is not None:
        identifier(research_revision_of)
        prior = Run(repo, research_revision_of)
        require(prior.brief["subject"] == brief.get("subject"), "Research revision subject mismatch")
        prior_result = prior.result("evidence-reviewer")
        require(prior_result["output"]["verdict"] != "ACCEPT",
                "Accepted evidence needs no research-revision successor")
        result_path = prior.root / "results/evidence-reviewer-r01.json"
        evidence_feedback = {
            "source_run": research_revision_of,
            "source_result_sha256": file_hash(result_path),
            "review": prior_result["output"],
            "reviewer_metadata": prior_result["metadata"],
        }
    validate_brief(brief)
    validate_research(research, brief)
    if remediation is not None:
        # Nothing is retrieved: frozen research is inherited byte-identical, so
        # the live preflight gate (freshness for NEW retrieval) does not apply.
        # Coverage is revalidated deterministically below.
        if not fixture:
            from .research_access import validate_coverage
            validate_coverage(research)
    elif not fixture:
        from .research_access import config as access_config, validate_preflight, validate_coverage
        validate_preflight(research_preflight or {}, access_config(repo), brief['subject'])
        validate_coverage(research)
    root = confined(repo, f"runs/{run_id}")
    require(not root.exists(), f"Run already exists: {run_id}. Reuse with status/task; never overwrite a frozen run.")
    config = read_json(repo / "factory/config.json")
    validate_config(config)
    files = active_files(repo)
    require(all((repo / rel).is_file() for rel in files), "Required factory code/config missing")
    root.mkdir(parents=True)
    try:
        with lock(root):
            entries = {}
            for rel in files:
                src = confined(repo, rel)
                dest = confined(root / "snapshot", rel)
                atomic_bytes(dest, src.read_bytes())
                entries[rel] = file_hash(dest)
            for name, data in (("brief.json", brief), ("research.json", research)):
                atomic_bytes(root / "inputs" / name, canonical(data) + b"\n")
            if research_preflight is not None:
                atomic_bytes(root / "inputs/research-preflight.json", canonical(research_preflight) + b"\n")
            if evidence_feedback is not None:
                atomic_bytes(root / "inputs/evidence-feedback.json", canonical(evidence_feedback) + b"\n")
            if remediation is not None:
                # Inherit sealed history byte-identical: tasks, results,
                # versioned assemblies and the live book pointer. Upstream
                # stages are never replayed; only new whole-book rounds append.
                src_root = repo / "runs" / remediation["source_run"]
                for sub in ("tasks", "results", "assembly"):
                    src, dest = src_root / sub, root / sub
                    require(src.is_dir(), f"Source run is missing sealed directory: {sub}")
                    shutil.copytree(src, dest)
                for name in ("book.md",):
                    require((src_root / name).is_file(), "Source run is missing its assembled book")
                    shutil.copyfile(src_root / name, root / name)
                # The inherited pointer must equal the inherited latest assembly.
                latest = sorted((root / "assembly").glob("assembly-r*.json"))[-1]
                require(text_hash((root / "book.md").read_text(encoding="utf-8"))
                        == unseal(latest)["text_sha256"], "Inherited book does not match inherited assembly")
            rev = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True)
            manifest = {"schema_version": 2, "run_id": run_id, "subject": brief["subject"],
                        "created_at": now(), "parent": parent, "fixture": fixture,
                        "origin_commit": rev.stdout.strip() if rev.returncode == 0 else None,
                        "factory_files": entries, "factory_digest": digest(entries),
                        "brief_sha256": file_hash(root / "inputs/brief.json"),
                        "research_sha256": file_hash(root / "inputs/research.json"),
                        "research_preflight_sha256": file_hash(root / "inputs/research-preflight.json") if research_preflight is not None else None,
                        "research_revision_of": research_revision_of,
                        "evidence_feedback_sha256": file_hash(root / "inputs/evidence-feedback.json") if evidence_feedback is not None else None,
                        "remediation_of": remediation["source_run"] if remediation is not None else None,
                        "remediation_source": remediation}
            seal(root / "manifest.json", manifest)
            if remediation is not None:
                src_root = repo / "runs" / remediation["source_run"]
                for name in ("brief.json", "research.json"):
                    require(file_hash(root / "inputs" / name) == file_hash(src_root / "inputs" / name),
                            f"Remediation {name} diverged from source")
    except BaseException:
        # Preserve unfinished input files for diagnosis; a missing manifest prevents use.
        raise
    return root


class Run:
    def __init__(self, repo: Path, run_id: str):
        self.repo = repo.resolve()
        self.root = confined(self.repo, f"runs/{identifier(run_id)}")
        self.manifest = unseal(self.root / "manifest.json")
        require(self.manifest["run_id"] == run_id, "Run identity mismatch")
        require(digest(self.manifest["factory_files"]) == self.manifest["factory_digest"], "Factory manifest mismatch")
        for rel, expected in self.manifest["factory_files"].items():
            p = confined(self.root / "snapshot", rel)
            require(p.is_file() and file_hash(p) == expected, f"Frozen input changed: {rel}")
        for name in ("brief", "research"):
            path = self.root / "inputs" / f"{name}.json"
            require(file_hash(path) == self.manifest[f"{name}_sha256"], f"Frozen {name} changed")
        if self.manifest.get("research_preflight_sha256"):
            require(file_hash(self.root / "inputs/research-preflight.json") == self.manifest["research_preflight_sha256"], "Frozen research preflight changed")
        if self.manifest.get("evidence_feedback_sha256"):
            require(file_hash(self.root / "inputs/evidence-feedback.json") == self.manifest["evidence_feedback_sha256"], "Frozen evidence feedback changed")
            self.evidence_feedback = read_json(self.root / "inputs/evidence-feedback.json")
            require(self.evidence_feedback.get("source_run") == self.manifest.get("research_revision_of"), "Evidence-feedback lineage mismatch")
            require(self.evidence_feedback.get("review", {}).get("verdict") in ("REVISE", "BLOCKED"), "Research revision needs prior non-ACCEPT feedback")
            validate_metadata(self.evidence_feedback.get("reviewer_metadata", {}))
        else:
            self.evidence_feedback = None
            require(self.manifest.get("research_revision_of") is None, "Research-revision lineage is missing evidence feedback")
        self.brief = read_json(self.root / "inputs/brief.json")
        self.research = read_json(self.root / "inputs/research.json")
        validate_brief(self.brief)
        validate_research(self.research, self.brief)
        self.config = read_json(self.root / "snapshot/factory/config.json")
        validate_config(self.config)

    def assert_runtime(self) -> None:
        # Prompts are read from snapshot. Execution code must also match it.
        frozen = {p: h for p, h in self.manifest["factory_files"].items() if p.startswith("scripts/")}
        runtime_root = Path(__file__).resolve().parents[2]
        current = {p: file_hash(runtime_root / p) for p in active_files(runtime_root) if p.startswith("scripts/")}
        require(frozen == current, "Execution code differs from frozen run. Use its code snapshot or prepare a new run.")

    def snapshot(self, rel: str) -> str:
        return confined(self.root / "snapshot", rel).read_text(encoding="utf-8")

    def key(self, role: str, chapter: int | None, round_no: int) -> str:
        require(role in ROLES, f"Unknown factory role: {role}")
        require(type(round_no) is int and 1 <= round_no <= self.config["max_rounds"], "Round limit reached; fix upstream in a new run, never accept by cap")
        needs_chapter = role in ("writer", "chapter-reviewer", "state-editor")
        require((chapter is not None) == needs_chapter, "Chapter parameter does not match role")
        if chapter is not None:
            require(type(chapter) is int and chapter > 0, "Chapter must be a positive integer")
        return role + (f"-ch{chapter:02d}" if chapter is not None else "") + f"-r{round_no:02d}"

    def result(self, role: str, chapter: int | None = None, round_no: int = 1) -> dict:
        key = self.key(role, chapter, round_no)
        result = unseal(self.root / "results" / f"{key}.json")
        task = unseal(self.root / "tasks" / f"{result['task_digest']}.json")
        require(result["key"] == key and task["key"] == key, "Result identity mismatch")
        require(digest(task) == result["task_digest"] and result["output_sha256"] == digest(result["output"]), "Result/input hash mismatch")
        if task["run_manifest_sha256"] != digest(self.manifest):
            # Content-addressed inheritance: a remediation run accepts results
            # sealed under its recorded source manifest, byte-identical.
            require(self.manifest.get("remediation_of") is not None, "Result from a different frozen run")
            require(task["run_manifest_sha256"]
                    == self.manifest["remediation_source"]["source_manifest_sha256"],
                    "Result from an unbound run")
        for dep, sha in task["dependency_hashes"].items():
            path = confined(self.root, dep)
            require(path.is_file() and file_hash(path) == sha, f"Dependency changed or missing: {dep}")
        return result

    def latest(self, role: str, chapter: int | None = None) -> tuple[int, dict]:
        prefix = role + (f"-ch{chapter:02d}" if chapter is not None else "") + "-r"
        files = sorted((self.root / "results").glob(prefix + "*.json"))
        require(bool(files), f"Missing result: {prefix}")
        numbers = [int(p.stem.rsplit("-r", 1)[1]) for p in files]
        require(numbers == list(range(1, max(numbers) + 1)), f"Gap in role rounds: {prefix}")
        return numbers[-1], self.result(role, chapter, numbers[-1])

    def accepted_plan(self) -> tuple[int, dict]:
        r, plan = self.latest("planner")
        review = self.result("plan-reviewer", round_no=r)
        require(review["output"]["verdict"] == "ACCEPT", "Plan has not passed review")
        validate_plan(plan["output"], self.brief, self.research)
        return r, plan["output"]

    def accepted_chapter(self, n: int) -> tuple[int, dict]:
        r, writer = self.latest("writer", n)
        review = self.result("chapter-reviewer", n, r)
        require(review["output"]["verdict"] == "ACCEPT", f"Chapter {n} is not accepted; cap is never acceptance")
        return r, writer["output"]

    def deps_add(self, deps: dict, role: str, chapter: int | None = None, round_no: int = 1) -> dict:
        result = self.result(role, chapter, round_no)
        rel = f"results/{self.key(role, chapter, round_no)}.json"
        deps[rel] = file_hash(self.root / rel)
        return result["output"]

    def task(self, role: str, chapter: int | None = None, round_no: int = 1) -> dict:
        self.assert_runtime()
        key = self.key(role, chapter, round_no)
        require(not (self.root / "results" / f"{key}.json").exists(), f"Result already exists: {key}. It is immutable.")
        if self.manifest.get("remediation_of") is not None and role in (
                "evidence-reviewer", "planner", "plan-reviewer", "writer", "chapter-reviewer", "state-editor"):
            require(False, "Remediation inherits upstream stages byte-identical from its source run; only book-editor and final-auditor rounds continue here")
        deps: dict[str, str] = {}
        inputs = {"brief": self.brief, "research": self.research}
        if role == "evidence-reviewer":
            require(round_no == 1, "Research revision requires a new snapshot/run")
            if self.evidence_feedback is not None:
                inputs["previous_evidence_review"] = self.evidence_feedback["review"]
                inputs["previous_evidence_review_source"] = {
                    "source_run": self.evidence_feedback["source_run"],
                    "source_result_sha256": self.evidence_feedback["source_result_sha256"],
                }
        else:
            evidence = self.deps_add(deps, "evidence-reviewer")
            require(evidence["verdict"] == "ACCEPT", "Research needs independent evidence acceptance")
        if role == "planner":
            if round_no > 1:
                history = []
                for prior_round in range(1, round_no):
                    prior_plan = self.deps_add(deps, "planner", round_no=prior_round)
                    prior_review = self.deps_add(deps, "plan-reviewer", round_no=prior_round)
                    history.append({"round": prior_round, "plan": prior_plan, "review": prior_review})
                inputs["revision_history"] = history
                inputs["previous_plan"] = history[-1]["plan"]
                inputs["feedback"] = history[-1]["review"]
                require(inputs["feedback"]["verdict"] != "ACCEPT", "Cannot revise an accepted plan in place; create a new run")
        elif role == "plan-reviewer":
            inputs["plan"] = self.deps_add(deps, "planner", round_no=round_no)
            if round_no > 1:
                history = []
                for prior_round in range(1, round_no):
                    history.append({
                        "round": prior_round,
                        "plan": self.deps_add(deps, "planner", round_no=prior_round),
                        "review": self.deps_add(deps, "plan-reviewer", round_no=prior_round),
                    })
                inputs["revision_history"] = history
        elif role not in ("evidence-reviewer",):
            pr, plan = self.accepted_plan()
            inputs["plan"] = self.deps_add(deps, "planner", round_no=pr)
            self.deps_add(deps, "plan-reviewer", round_no=pr)
            if chapter is not None:
                require(chapter <= len(plan["chapters"]), "Chapter outside accepted plan")
                inputs["card"] = plan["chapters"][chapter-1]
            previous = []
            limit = chapter-1 if chapter is not None else len(plan["chapters"])
            for n in range(1, limit+1):
                cr, c = self.accepted_chapter(n)
                self.deps_add(deps, "writer", n, cr)
                self.deps_add(deps, "chapter-reviewer", n, cr)
                state = self.deps_add(deps, "state-editor", n, cr)
                previous.append({"id": c["chapter_id"], "title": plan["chapters"][n-1]["title"],
                                 "text": c["text"], "claim_map": c["claim_map"], "state": state,
                                 "source_chapters": [c["chapter_id"]]})
            inputs["delivered_previous_chapters"] = previous
            if role == "writer" and round_no > 1:
                history = []
                for prior_round in range(1, round_no):
                    history.append({
                        "round": prior_round,
                        "draft": self.deps_add(deps, "writer", chapter, prior_round),
                        "review": self.deps_add(deps, "chapter-reviewer", chapter, prior_round),
                    })
                inputs["revision_history"] = history
                inputs["draft"] = history[-1]["draft"]
                inputs["feedback"] = history[-1]["review"]
                require(inputs["feedback"]["verdict"] != "ACCEPT", "Accepted chapters cannot be rewritten in place")
            if role in ("chapter-reviewer", "state-editor"):
                inputs["draft"] = self.deps_add(deps, "writer", chapter, round_no)
            if role == "chapter-reviewer" and round_no > 1:
                history = []
                for prior_round in range(1, round_no):
                    history.append({
                        "round": prior_round,
                        "draft": self.deps_add(deps, "writer", chapter, prior_round),
                        "review": self.deps_add(deps, "chapter-reviewer", chapter, prior_round),
                    })
                inputs["revision_history"] = history
            if role == "state-editor":
                review = self.deps_add(deps, "chapter-reviewer", chapter, round_no)
                require(review["verdict"] == "ACCEPT", "Reader state can only describe accepted delivered text")
            if role == "book-editor":
                if round_no > 1:
                    # Bounded whole-book revision: the previous final audit must have
                    # asked for fixes (REVISE). BLOCKED stops the run; accepted
                    # chapters are never rewritten in place — edits apply to copies.
                    prior_audit = self.deps_add(deps, "final-auditor", round_no=round_no-1)
                    require(prior_audit["verdict"] == "REVISE",
                            "Whole-book revision needs a prior REVISE audit; BLOCKED stops the run")
                    editor_history = []
                    for prior_round in range(1, round_no):
                        editor_history.append({
                            "round": prior_round,
                            "edits": self.deps_add(deps, "book-editor", round_no=prior_round),
                            "audit": self.deps_add(deps, "final-auditor", round_no=prior_round),
                        })
                    inputs["revision_history"] = editor_history
                    inputs["audit_history"] = editor_history
                    prev = self.assembly_version(round_no-1)
                    deps[prev["rel"]] = prev["sha256"]
                    inputs["previous_assembly"] = {"assembly_round": round_no-1,
                                                   "text": prev["assembly"]["text"],
                                                   "text_sha256": prev["assembly"]["text_sha256"]}
                    inputs["screening"] = screen("\n\n".join(c["text"] for c in prev["assembly"]["chapters"]))
                else:
                    inputs["screening"] = screen("\n\n".join(c["text"] for c in previous))
            if role == "final-auditor":
                if round_no > 1:
                    # Successor audit: the matching revised edit round must exist;
                    # earlier audits travel as the finite blocking set.
                    self.deps_add(deps, "book-editor", round_no=round_no)
                    audit_history = []
                    for prior_round in range(1, round_no):
                        audit_history.append({
                            "round": prior_round,
                            "audit": self.deps_add(deps, "final-auditor", round_no=prior_round),
                        })
                    inputs["audit_history"] = audit_history
                assembled = self.assemble(round_no if role == "final-auditor" and round_no > 1 else None)
                deps[assembled["rel"]] = assembled["sha256"]
                inputs["assembled_book"] = assembled["assembly"]["text"]
                inputs["screening"] = assembled["assembly"]["screening"]
                inputs["editorial_changes"] = self.deps_add(deps, "book-editor",
                                                            round_no=round_no if round_no > 1 else 1)
        task = {"schema_version": 2, "key": key, "role": role, "chapter": chapter, "round": round_no,
                "run_manifest_sha256": digest(self.manifest), "dependency_hashes": deps,
                "contract": self.snapshot("prompts/" + PROMPTS[role]),
                "style": self.snapshot("prompts/style-guide.md"), "inputs": inputs}
        with lock(self.root):
            seal(self.root / "tasks" / f"{digest(task)}.json", task)
        return task

    def generating_families(self) -> set[str]:
        families = {self.config["profiles"]["factory"]["family"]}
        for path in (self.root / "results").glob("*.json"):
            result = unseal(path)
            if result["role"] in ("planner", "writer", "book-editor"):
                families.add(result["metadata"]["family"])
        return families

    def validate_output(self, task: dict, output: dict) -> None:
        role, inputs = task["role"], task["inputs"]
        if role in REVIEW_ROLES:
            # Finding quotes may come from any reviewed input (brief, plan, draft,
            # research); only final-audit claim checks are bound to the book text.
            inputs_text = json.dumps(inputs, ensure_ascii=False)
            book_text = inputs["assembled_book"] if role == "final-auditor" else None
            validate_review(output, inputs_text, final=role == "final-auditor", claim_text=book_text)
            if role == "evidence-reviewer" and output["verdict"] == "ACCEPT" and not self.manifest["fixture"]:
                require(all(e["verification"] != "unverified" for e in self.research["sources"]), "Unverified sources cannot pass live evidence review; verify retrieval and prepare a new run")
            if role == "final-auditor":
                flags = {f["id"] for f in inputs["screening"]}
                require(set(output["screening_resolutions"]) == flags, "Every screening flag needs explicit semantic triage")
                ids = {e["id"] for e in self.research["sources"]}
                for claim in output["claim_checks"]:
                    require(set(claim["evidence_ids"]) <= ids, "Final claim refers to unknown evidence")
                    if claim["support"] in ("supported", "bounded"):
                        source_map = {e["id"]: e for e in self.research["sources"]}
                        require(all(source_map[e]["kind"] != "illustration" and source_map[e]["verification"] != "unverified" for e in claim["evidence_ids"]), "An illustration or unverified source cannot support a final empirical claim")
        elif role == "planner":
            validate_plan(output, self.brief, self.research)
        elif role == "writer":
            validate_writer(output, f"chapter-{task['chapter']:02d}", self.research)
        elif role == "state-editor":
            validate_state(output, f"chapter-{task['chapter']:02d}", inputs["draft"]["text"])
        elif role == "book-editor":
            base = inputs["delivered_previous_chapters"]
            front_base = base_front_matter(self.brief, self.accepted_plan()[1])
            if task["round"] > 1:
                # Revision anchors bind to the previous immutable edited
                # assembly, not the accepted originals (cumulative edits).
                prev_asm = self.assembly_version(task["round"] - 1)["assembly"]
                base = prev_asm["chapters"]
                front_base = prev_asm.get("front_matter") or front_base
            chapter_ops, front_ops = split_operations(output["operations"])
            edit_book(base, {"schema_version": output.get("schema_version", 2),
                             "operations": chapter_ops, "explanation": output.get("explanation", "n/a")})
            apply_front_repairs(front_base, front_ops, task["round"])

    def submit(self, task: dict, output: dict, metadata: dict) -> dict:
        self.assert_runtime()
        require(task["run_manifest_sha256"] == digest(self.manifest), "Task not bound to this run")
        require(unseal(self.root / "tasks" / f"{digest(task)}.json") == task, "Task is missing/modified")
        # Reconstruct the task: rejects stale feedback, missing stages and changed dependencies.
        fresh = self.task(task["role"], task["chapter"], task["round"])
        require(fresh == task, "Task is stale; inputs/dependencies changed")
        validate_metadata(metadata)
        if not self.manifest["fixture"]:
            require(metadata["harness"] != "fixture" and metadata["family"] != "fixture", "Fixture output cannot enter a live run")
        if task["role"] in EXTERNAL_ROLES:
            require(metadata["family"] not in self.generating_families(), "Independent review cannot silently fall back to the generating model family")
        if task["role"] in ("planner", "writer", "book-editor"):
            evidence_review = self.result("evidence-reviewer")
            require(evidence_review["metadata"]["family"] != metadata["family"], "Generator switched into the evidence reviewer family; prepare a new independently reviewed run")
        self.validate_output(task, output)
        record = {"schema_version": 2, "key": task["key"], "role": task["role"], "task_digest": digest(task),
                  "output": output, "output_sha256": digest(output), "metadata": metadata, "created_at": now()}
        with lock(self.root):
            seal(self.root / "results" / f"{task['key']}.json", record)
        return record

    def assembly_path(self, version: int) -> Path:
        require(type(version) is int and version >= 1, "Assembly version must be a positive integer")
        return self.root / "assembly" / f"assembly-r{version:02d}.json"

    def assembly_version(self, version: int) -> dict:
        """Load one immutable assembly version; verifies seal and returns its hash."""
        path = self.assembly_path(version)
        rel = path.relative_to(self.root).as_posix()
        require(path.is_file(), f"Missing assembly version: {rel}")
        return {"rel": rel, "sha256": file_hash(path), "assembly": unseal(path)}

    def latest_assembly_version(self) -> int:
        files = sorted((self.root / "assembly").glob("assembly-r*.json")) if (self.root / "assembly").is_dir() else []
        require(bool(files), "Missing result: assembly-r")
        numbers = [int(p.stem.rsplit("-r", 1)[1]) for p in files]
        require(numbers == list(range(1, max(numbers) + 1)), "Gap in assembly versions")
        return numbers[-1]

    def assemble(self, editor_round: int | None = None) -> dict:
        _, plan = self.accepted_plan()
        deps = {}
        self.deps_add(deps, "evidence-reviewer")
        pr, _ = self.latest("planner")
        self.deps_add(deps, "planner", round_no=pr)
        self.deps_add(deps, "plan-reviewer", round_no=pr)
        chapters = []
        if editor_round is None:
            editor_round, _ = self.latest("book-editor")
        if editor_round > 1:
            # Cumulative revision: later edits transform the previous immutable
            # edited assembly, never the accepted originals — earlier repairs
            # survive unless the inherited audit explicitly changes them.
            prev = self.assembly_version(editor_round - 1)
            deps[prev["rel"]] = prev["sha256"]
            chapters = prev["assembly"]["chapters"]
            front_base = prev["assembly"].get("front_matter") or base_front_matter(self.brief, plan)
            prior_repairs = list(prev["assembly"].get("front_matter_repairs", []))
        else:
            chapters = []
            for n, card in enumerate(plan["chapters"], 1):
                cr, c = self.accepted_chapter(n)
                self.deps_add(deps, "writer", n, cr)
                self.deps_add(deps, "chapter-reviewer", n, cr)
                self.deps_add(deps, "state-editor", n, cr)
                chapters.append({"id": card["id"], "title": card["title"], "text": c["text"],
                                 "claim_map": c["claim_map"], "source_chapters": [card["id"]]})
        editor = self.deps_add(deps, "book-editor", round_no=editor_round)
        chapter_ops, front_ops = split_operations(editor["operations"])
        edited = edit_book(chapters, {"schema_version": 2, "operations": chapter_ops,
                                      "explanation": editor.get("explanation", "n/a")})
        if editor_round > 1:
            front_matter, new_repairs = apply_front_repairs(front_base, front_ops, editor_round)
            front_repairs = prior_repairs + new_repairs
        else:
            front_matter, new_repairs = apply_front_repairs(base_front_matter(self.brief, plan), front_ops, editor_round)
            front_repairs = new_repairs
        text = assemble_book(self.brief, self.research, plan, edited, front_matter=front_matter)
        screening = screen("\n\n".join(c["text"] for c in edited))
        assembly = {"schema_version": 2, "assembly_round": editor_round,
                    "run_manifest_sha256": digest(self.manifest), "dependency_hashes": deps,
                    "front_matter": front_matter, "front_matter_repairs": front_repairs,
                    "text": text, "text_sha256": text_hash(text), "chapters": edited, "screening": screening}
        with lock(self.root):
            (self.root / "assembly").mkdir(exist_ok=True)
            vpath = self.assembly_path(editor_round)
            preexisting = vpath.is_file()
            dest = self.root / "book.md"
            if not preexisting and dest.exists():
                prior = sorted((self.root / "assembly").glob("assembly-r*.json"))
                if not prior and dest.read_text(encoding="utf-8") != text:
                    # Legacy layout (assembly.json-era book): refuse to seal over it
                    # or move its pointer. Inspect with the frozen snapshot runtime.
                    # No file is written on this path.
                    require(False, "Existing book predates versioned assemblies; inspect it with the run's frozen snapshot runtime")
            if preexisting:
                sealed = unseal(vpath)
                require(sealed["text"] == text,
                        "Assembly recomputation diverged from sealed history; use the run's frozen snapshot runtime")
            else:
                seal(vpath, assembly)
            latest = self.latest_assembly_version()
            latest_text = unseal(self.assembly_path(latest))["text"]
            dest = self.root / "book.md"
            if dest.exists():
                cur = dest.read_text(encoding="utf-8")
                if cur != latest_text:
                    if (editor_round == latest and latest > 1
                            and cur == unseal(self.assembly_path(latest - 1))["text"]):
                        # Normal advancement: move the live pointer to the new version.
                        atomic_bytes(dest, latest_text.encode("utf-8"))
                    else:
                        require(False, "Assembled book was modified")
            else:
                require(latest == 1 and not preexisting, "Assembled book was modified")
                atomic_bytes(dest, latest_text.encode("utf-8"))
        path = self.assembly_path(editor_round)
        return {"rel": path.relative_to(self.root).as_posix(), "sha256": file_hash(path), "assembly": assembly}

    def accepted_audit(self) -> tuple[int, dict]:
        """Latest ACCEPTED final audit. Downstream consumers (judgment, release,
        archive) must bind this — never round 1 by convention."""
        au, audit = self.latest("final-auditor")
        require(audit["output"]["verdict"] == "ACCEPT", "No accepted final audit")
        self.assembly_version(au)
        return au, audit

    def accepted_audit_file(self) -> Path:
        au, _ = self.accepted_audit()
        return self.root / "results" / f"final-auditor-r{au:02d}.json"

    def accepted_assembly(self) -> dict:
        """Latest accepted immutable assembly — exactly what complete() certifies."""
        er, _ = self.latest("book-editor")
        au, _ = self.accepted_audit()
        require(au == er, "Latest edits are unaudited")
        return self.assembly_version(er)

    def complete(self) -> dict:
        er, _ = self.latest("book-editor")
        assembly = self.assembly_version(er)
        au, audit = self.latest("final-auditor")
        require(au == er, "Latest edits are unaudited; audit the current assembly before completion")
        require(audit["output"]["verdict"] == "ACCEPT", "Final audit did not accept the assembled publication")
        require(audit["metadata"]["family"] not in self.generating_families(), "Final audit is not independent")
        require((self.root / "book.md").read_text(encoding="utf-8") == assembly["assembly"]["text"], "Assembled publication changed after audit")
        return {"status": "COMPLETE_UNRELEASED", "fixture": self.manifest["fixture"],
                "run_id": self.manifest["run_id"], "book_sha256": assembly["assembly"]["text_sha256"],
                "factory_digest": self.manifest["factory_digest"], "efficacy": "NOT_MEASURED"}

    def status(self) -> dict:
        try:
            return self.complete()
        except (FactoryError, FileNotFoundError) as exc:
            return {"status": "INCOMPLETE", "reason": str(exc), "run_id": self.manifest["run_id"]}
