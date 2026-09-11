"""Frozen runs and content-addressed, dependency-bound role tasks.

The human/agent orchestrator calls one explicit unit at a time. Nothing in this
module starts background jobs, changes a champion, or reads a legacy live plan.
"""
from __future__ import annotations
import json
import subprocess
from pathlib import Path
from .common import (FactoryError, atomic_bytes, canonical, confined, digest, exact_keys, file_hash,
                     identifier, lock, nonempty, now, read_json, require, seal, text_hash, unseal)
from .schema import (EXTERNAL_ROLES, ROLES, REVIEW_ROLES, validate_brief, validate_plan, validate_research,
                     validate_review, validate_state, validate_writer, validate_config, validate_metadata)
from .quality import assemble_book, edit_book, screen

PROMPTS = {"planner": "master-plan-skill-v2.md", "plan-reviewer": "master-plan-reviewer-v2.md",
           "writer": "chapter-writer.md", "chapter-reviewer": "chapter-reviewer.md",
           "evidence-reviewer": "evidence-reviewer.md", "state-editor": "reader-state.md",
           "book-editor": "book-editor.md", "final-auditor": "final-auditor.md"}
REQUIRED_CODE = ["scripts/factory.py", "factory/config.json"]


def active_files(repo: Path) -> list[str]:
    paths = [*REQUIRED_CODE]
    for glob in ("scripts/bc_factory/*.py", "prompts/*.md", "loop/judges/*.md"):
        paths.extend(p.relative_to(repo).as_posix() for p in repo.glob(glob) if p.is_file())
    return sorted(set(paths))


def prepare(repo: Path, run_id: str, brief: dict, research: dict, parent: str | None = None,
            fixture: bool = False) -> Path:
    repo = repo.resolve()
    identifier(run_id)
    if parent is not None:
        identifier(parent)
    validate_brief(brief)
    validate_research(research, brief)
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
            rev = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True)
            manifest = {"schema_version": 2, "run_id": run_id, "subject": brief["subject"],
                        "created_at": now(), "parent": parent, "fixture": fixture,
                        "origin_commit": rev.stdout.strip() if rev.returncode == 0 else None,
                        "factory_files": entries, "factory_digest": digest(entries),
                        "brief_sha256": file_hash(root / "inputs/brief.json"),
                        "research_sha256": file_hash(root / "inputs/research.json")}
            seal(root / "manifest.json", manifest)
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
        require(task["run_manifest_sha256"] == digest(self.manifest), "Result from a different frozen run")
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
        deps: dict[str, str] = {}
        inputs = {"brief": self.brief, "research": self.research}
        if role == "evidence-reviewer":
            require(round_no == 1, "Research revision requires a new snapshot/run")
        else:
            evidence = self.deps_add(deps, "evidence-reviewer")
            require(evidence["verdict"] == "ACCEPT", "Research needs independent evidence acceptance")
        if role == "planner":
            if round_no > 1:
                inputs["previous_plan"] = self.deps_add(deps, "planner", round_no=round_no-1)
                inputs["feedback"] = self.deps_add(deps, "plan-reviewer", round_no=round_no-1)
                require(inputs["feedback"]["verdict"] != "ACCEPT", "Cannot revise an accepted plan in place; create a new run")
        elif role == "plan-reviewer":
            inputs["plan"] = self.deps_add(deps, "planner", round_no=round_no)
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
                inputs["draft"] = self.deps_add(deps, "writer", chapter, round_no-1)
                inputs["feedback"] = self.deps_add(deps, "chapter-reviewer", chapter, round_no-1)
                require(inputs["feedback"]["verdict"] != "ACCEPT", "Accepted chapters cannot be rewritten in place")
            if role in ("chapter-reviewer", "state-editor"):
                inputs["draft"] = self.deps_add(deps, "writer", chapter, round_no)
            if role == "state-editor":
                review = self.deps_add(deps, "chapter-reviewer", chapter, round_no)
                require(review["verdict"] == "ACCEPT", "Reader state can only describe accepted delivered text")
            if role == "book-editor":
                require(round_no == 1, "Editorial revision requires new run; never overwrite accepted source chapters")
                inputs["screening"] = screen("\n\n".join(c["text"] for c in previous))
            if role == "final-auditor":
                require(round_no == 1, "Final-audit revision requires a new run")
                assembled = self.assemble()
                deps["assembly.json"] = file_hash(self.root / "assembly.json")
                inputs["assembled_book"] = assembled["text"]
                inputs["screening"] = assembled["screening"]
                inputs["editorial_changes"] = self.deps_add(deps, "book-editor")
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
            source_text = (inputs["assembled_book"] if role == "final-auditor" else
                           inputs["draft"]["text"] if role == "chapter-reviewer" else
                           json.dumps(inputs.get("plan", self.research), ensure_ascii=False))
            validate_review(output, source_text, final=role == "final-auditor")
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
            edit_book(inputs["delivered_previous_chapters"], output)

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

    def assemble(self) -> dict:
        _, plan = self.accepted_plan()
        deps = {}
        self.deps_add(deps, "evidence-reviewer")
        pr, _ = self.latest("planner")
        self.deps_add(deps, "planner", round_no=pr)
        self.deps_add(deps, "plan-reviewer", round_no=pr)
        chapters = []
        for n, card in enumerate(plan["chapters"], 1):
            cr, c = self.accepted_chapter(n)
            self.deps_add(deps, "writer", n, cr)
            self.deps_add(deps, "chapter-reviewer", n, cr)
            self.deps_add(deps, "state-editor", n, cr)
            chapters.append({"id": card["id"], "title": card["title"], "text": c["text"],
                             "claim_map": c["claim_map"], "source_chapters": [card["id"]]})
        editor = self.deps_add(deps, "book-editor")
        edited = edit_book(chapters, editor)
        text = assemble_book(self.brief, self.research, plan, edited)
        screening = screen("\n\n".join(c["text"] for c in edited))
        assembly = {"schema_version": 2, "run_manifest_sha256": digest(self.manifest), "dependency_hashes": deps,
                    "text": text, "text_sha256": text_hash(text), "chapters": edited, "screening": screening}
        with lock(self.root):
            seal(self.root / "assembly.json", assembly)
            dest = self.root / "book.md"
            if dest.exists():
                require(dest.read_text(encoding="utf-8") == text, "Assembled book was modified")
            else:
                atomic_bytes(dest, text.encode("utf-8"))
        return assembly

    def complete(self) -> dict:
        assembly = self.assemble()
        audit = self.result("final-auditor")
        require(audit["output"]["verdict"] == "ACCEPT", "Final audit did not accept the assembled publication")
        require(audit["metadata"]["family"] not in self.generating_families(), "Final audit is not independent")
        require((self.root / "book.md").read_text(encoding="utf-8") == assembly["text"], "Assembled publication changed after audit")
        return {"status": "COMPLETE_UNRELEASED", "fixture": self.manifest["fixture"],
                "run_id": self.manifest["run_id"], "book_sha256": assembly["text_sha256"],
                "factory_digest": self.manifest["factory_digest"], "efficacy": "NOT_MEASURED"}

    def status(self) -> dict:
        try:
            return self.complete()
        except (FactoryError, FileNotFoundError) as exc:
            return {"status": "INCOMPLETE", "reason": str(exc), "run_id": self.manifest["run_id"]}
