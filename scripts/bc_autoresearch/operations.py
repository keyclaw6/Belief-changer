"""Outer handoff and one-book Pi launch, not a scheduler or autoresearch engine.

progress.json is the existing compact handoff. Approval references are operator
assertions to check against the human source, not cryptographic consent.
"""
from __future__ import annotations

import contextlib
import errno
import json
import os
import shlex
import shutil
import uuid
from pathlib import Path

from bc_factory.common import (FactoryError, confined, digest, file_hash, identifier,
                               nonempty, parse_json, read_json, require, atomic_bytes,
                               atomic_json, seal, unseal)
from bc_factory.runs import Run, active_files, load_caller_repair
from bc_factory.schema import validate_brief
from bc_factory.cli import document


def scope_digest(progress: dict) -> str:
    """Bind approval to science, not generated run IDs or process receipts."""
    return digest({"hypothesis": progress["preregistration_sha256"],
                   "allocation": progress["allocation"]})


def progress_record(repo: Path, iteration: str, *, for_launch: bool = False) -> dict:
    root = confined(repo, f"loop/iterations/{identifier(iteration)}")
    p = read_json(root / "progress.json")
    require(p.get("schema_version") == 1 and p.get("iteration") == iteration,
            "Iteration handoff identity mismatch")
    allocation = p.get("allocation")
    require(isinstance(allocation, dict) and bool(allocation) and
            all(isinstance(k, str) and k and type(v) is int and v > 0
                for k, v in allocation.items()), "Explicit per-subject book allocation required")
    require(p.get("preregistration_sha256") == file_hash(root / "hypothesis.md"),
            "Hypothesis changed: reconcile the frozen scope before execution")
    require(p.get("execution_status") in ("STOPPED", "ACTIVE", "COMPLETE"),
            "Execution status must be STOPPED, ACTIVE or COMPLETE; incidents are not owner stops")
    auth = p.get("authorization", {})
    require(auth.get("status") in ("UNCONFIRMED", "APPROVED"), "Scope authorization is missing")
    if auth["status"] == "APPROVED":
        nonempty(auth.get("reference"), "Human authorization source reference")
        nonempty(auth.get("quote"), "Human authorization quotation")
        require(auth.get("scope_sha256") == scope_digest(p),
                "Allocation/hypothesis differs from the approved scope")
    if for_launch:
        require(p["execution_status"] == "ACTIVE", "Owner stop/completion: do not launch or arm a watchdog")
        require(auth["status"] == "APPROVED", "Confirm the material experiment scope with the owner first")
        if (repo / "loop/commissioning.json").exists():
            from .controller import campaign, validate_checkpoints
            _, boundary = campaign(repo)
            if iteration in boundary["iterations"]:
                require(boundary["execution_status"] == "ACTIVE",
                        "Commissioning stop/completion: do not launch or resume a book")
                completed = boundary.get("completed", [])
                require(len(completed) < len(boundary["iterations"]) and
                        boundary["iterations"][len(completed)] == iteration,
                        "Launch only the next authorized commissioning cycle")
                validate_checkpoints(repo, boundary)
    return p


def iteration_status(repo: Path, iteration: str) -> dict:
    p = progress_record(repo, iteration)
    return {"iteration": iteration, "execution_status": p["execution_status"],
            "authorization": p["authorization"]["status"],
            "scope_sha256": scope_digest(p),
            "next_action": ("AWAIT_OWNER_RESUME" if p["execution_status"] == "STOPPED" else
                            "CAMPAIGN_CHECKPOINT" if p["execution_status"] == "COMPLETE" else
                            "CONFIRM_SCOPE" if p["authorization"]["status"] != "APPROVED" else
                            "RECONCILE_RUNS_THEN_RESUME_OR_ADVANCE"),
            "handoff": f"loop/iterations/{iteration}/progress.json"}


def _allocated_runs(repo: Path, iteration: str, p: dict) -> dict[str, tuple[Run, list[str]]]:
    """Count books, not their validated research/remediation snapshots.

    Return each active leaf with its existing manifest lineage. No extra registry;
    unrelated or branching attempts cannot hide inside one authorized book slot.
    """
    excluded = p.get("excluded_runs", [])
    require(isinstance(excluded, list), "Excluded runs must be explicit records")
    excluded_ids = set()
    for record in excluded:
        excluded_ids.add(identifier(record["run_id"]))
        nonempty(record.get("reason"), "Exclusion reason")
    prefix = f"iter{iteration}-"
    runs = {root.name: Run(repo, root.name) for root in sorted((repo / "runs").glob(prefix + "*"))
            if root.is_dir() and root.name not in excluded_ids}
    known, lineages = dict(runs), {}
    for run_id in runs:
        chain, current = [], run_id
        while True:
            require(current not in chain, "Cyclic book successor lineage")
            chain.append(current)
            run = known[current]
            links = [(kind, run.manifest.get(kind)) for kind in ("research_revision_of", "remediation_of")
                     if run.manifest.get(kind) is not None]
            require(len(links) <= 1, "A book successor has conflicting lineage types")
            # Prior-iteration research is input history, not a shared book/session.
            if not links or not identifier(links[0][1]).startswith(prefix):
                break
            kind, source_id = links[0]
            if source_id not in known:
                known[source_id] = Run(repo, source_id)
            source = known[source_id]
            for field in ("subject", "brief_sha256", "parent", "fixture", "caller_context_sha256"):
                require(run.manifest.get(field) == source.manifest.get(field),
                        f"Linked successor changed frozen scope: {field}")
            for profile in ("factory", "external"):
                child_profile, source_profile = run.config["profiles"].get(profile), source.config["profiles"].get(profile)
                require(isinstance(child_profile, dict) and isinstance(source_profile, dict) and
                        child_profile.get("family") == source_profile.get("family") and
                        [r.get("model") for r in child_profile.get("routes", [])] ==
                        [r.get("model") for r in source_profile.get("routes", [])],
                        "Linked successor changed frozen model identity")
            if kind == "research_revision_of":
                receipt = source.result("evidence-reviewer")
                feedback = run.evidence_feedback
                require(receipt["output"]["verdict"] in ("REVISE", "BLOCKED") and feedback is not None and
                        feedback["source_result_sha256"] == file_hash(source.root / "results/evidence-reviewer-r01.json") and
                        digest(feedback["review"]) == digest(receipt["output"]) and
                        digest(feedback["reviewer_metadata"]) == digest(receipt["metadata"]),
                        "Research successor source evidence no longer matches its frozen lineage")
            else:
                round_no, audit = source.latest("final-auditor")
                meta = run.manifest.get("remediation_source") or {}
                require(audit["output"]["verdict"] == "REVISE" and
                        meta.get("source_manifest_sha256") == digest(source.manifest) and
                        meta.get("source_audit_sha256") == file_hash(source.root / "results" / f"final-auditor-r{round_no:02d}.json") and
                        meta.get("source_assembly_sha256") == file_hash(source.assembly_path(round_no)),
                        "Remediation successor source evidence no longer matches its frozen lineage")
            current = source_id
        lineages[run_id] = list(reversed(chain))
    predecessors = {rid for chain in lineages.values() for rid in chain[:-1]}
    books = {rid: (runs[rid], chain) for rid, chain in lineages.items() if rid not in predecessors}
    roots = [chain[0] for _, chain in books.values()]
    require(len(roots) == len(set(roots)), "Reconcile branching book successors; do not hide extra samples in one slot")
    counts = {subject: 0 for subject in p["allocation"]}
    for run, _ in books.values():
        subject = run.manifest["subject"]
        require(subject in counts, "Prepared run has a subject outside the approved allocation")
        counts[subject] += 1
    require(all(n <= p["allocation"][subject] for subject, n in counts.items()),
            "Prepared runs exceed the approved allocation; reconcile exclusions, do not enlarge scope")
    return books


def _go_routes(config: dict) -> str:
    profiles = config["profiles"]
    ext = profiles.get("external")
    require(isinstance(ext, dict) and ext.get("family") != profiles["factory"].get("family"),
            "An independent OpenCode Go evaluator is required")
    for profile in profiles.values():
        require(profile.get("adapter") == "http" and len(profile.get("routes", [])) == 1,
                "This launcher requires the configured single OpenCode Go HTTP route per role family")
        route = profile["routes"][0]
        expected = {"responses": "responses", "chat": "chat/completions"}.get(route.get("api"))
        require(expected is not None and route.get("endpoint") ==
                f"https://opencode.ai/zen/go/v1/{expected}" and
                route.get("auth_env") == "OPENCODE_GO_API_KEY",
                "Repair OpenCode Go routing; no alternate provider is permitted")
    route = profiles["factory"]["routes"][0]
    require(route["name"] == "opencode-go", "Unexpected generator route")
    return nonempty(route.get("model"), "Frozen generator model")


def pending_caller_repair(run: Run) -> bool:
    round_no, _ = run.accepted_audit()
    if not (run.root / "caller-feedback" / f"repair-r{round_no:02d}.json").exists():
        return False
    load_caller_repair(run, round_no)
    return True


def _preparation(repo: Path, iteration: str, run_id: str, p: dict,
                 books: dict, brief: Path | None, caller_context: Path | None) -> dict:
    """Freeze only the supplied science and factory source, before research."""
    require(run_id.startswith(f"iter{iteration}-"), "Book ID must belong to this iteration")
    root = confined(repo, f".loop-work/pi/{identifier(run_id)}/preparation")
    manifest = root / "preparation.json"
    require(run_id not in {entry["run_id"] for entry in p.get("excluded_runs", [])},
            "An excluded diagnostic run cannot become a new book")
    if manifest.exists():
        record = unseal(manifest)
        require(record.get("schema_version") == 1 and record.get("run_id") == run_id,
                "Preparation identity mismatch")
        for rel, expected in record["factory_files"].items():
            require(file_hash(confined(root, rel)) == expected, "Frozen preparation source changed")
        data = read_json(root / "inputs/brief.json")
        require(file_hash(root / "inputs/brief.json") == record["brief_sha256"],
                "Frozen preparation brief changed")
        context_path = root / "inputs/caller-context.json"
        context = None
        if record.get("caller_context_sha256"):
            require(file_hash(context_path) == record["caller_context_sha256"],
                    "Frozen preparation caller context changed")
            context = read_json(context_path)
        if brief is not None:
            require(digest(document(brief)) == digest(data), "Requested brief differs from this book's preparation")
        if caller_context is not None:
            require(context is not None and digest(document(caller_context)) == digest(context),
                    "Requested caller guidance differs from this book's preparation")
    else:
        require(brief is not None, "Supply --brief to research and prepare the next authorized book")
        data = document(brief)
        context = document(caller_context) if caller_context is not None else None
        files = {rel: file_hash(confined(repo, rel)) for rel in active_files(repo)}
        # This plan is read-only; launch writes these exact inputs before inference.
        record = {"schema_version": 1, "run_id": run_id, "factory_files": files}
    validate_brief(data)
    require(context is None or isinstance(context, dict) and bool(context),
            "Caller context must be a nonempty JSON object")
    require(data["subject"] in p["allocation"], "Preparation subject is outside the approved allocation")
    counts = {subject: 0 for subject in p["allocation"]}
    counted = set()
    for run, lineage in books.values():
        counts[run.manifest["subject"]] += 1
        counted.update(lineage)
    excluded = {entry["run_id"] for entry in p.get("excluded_runs", [])}
    for other in (repo / ".loop-work/pi").glob(f"iter{iteration}-*/preparation/preparation.json"):
        if other.parents[1].name in counted | excluded | {run_id}:
            continue
        other_record = unseal(other)
        other_brief = read_json(other.parent / "inputs/brief.json")
        require(other_record["run_id"] == other.parents[1].name and other_brief["subject"] in counts,
                "Reconcile a preparation outside this iteration's allocation")
        require(file_hash(other.parent / "inputs/brief.json") == other_record["brief_sha256"],
                "Another allocated preparation has a changed brief")
        counts[other_brief["subject"]] += 1
    if run_id not in counted:
        counts[data["subject"]] += 1
    require(all(value <= p["allocation"][subject] for subject, value in counts.items()),
            "Prepared books exceed the approved allocation")
    return {"root": str(root), "record": record, "brief": data,
            "caller_context": context, "frozen": manifest.exists()}


def _freeze_preparation(repo: Path, preparation: dict) -> None:
    if preparation["frozen"]:
        return
    root = Path(preparation["root"])
    expected = preparation["record"]["factory_files"]
    require(not (root / "preparation.json").exists(), "Preparation appeared while acquiring ownership")
    for rel, value in expected.items():
        source = confined(repo, rel)
        require(file_hash(source) == value, "Factory source changed before preparation was frozen")
        atomic_bytes(confined(root, rel), source.read_bytes())
        require(file_hash(confined(root, rel)) == value, "Factory source changed while freezing preparation")
    atomic_json(root / "inputs/brief.json", preparation["brief"])
    context = preparation["caller_context"]
    if context is not None:
        atomic_json(root / "inputs/caller-context.json", context)
    elif (root / "inputs/caller-context.json").exists():
        # An interrupted pre-inference freeze may have left an unsealed input.
        (root / "inputs/caller-context.json").unlink()
    record = {**preparation["record"], "brief_sha256": file_hash(root / "inputs/brief.json"),
              "caller_context_sha256": file_hash(root / "inputs/caller-context.json") if context is not None else None}
    seal(root / "preparation.json", record)


def _check_handoff(repo: Path, book_id: str, run: Run) -> None:
    path = confined(repo, f".loop-work/pi/{identifier(book_id)}/preparation/preparation.json")
    if not path.exists():
        return
    record = unseal(path)
    require(run.manifest["factory_files"] == record["factory_files"],
            "Factory source changed during research; preserve this preparation and reconcile before executing stages")
    for key in ("brief_sha256", "caller_context_sha256"):
        require(run.manifest.get(key) == record.get(key), "Preparation handoff changed frozen " + key)


def _session_options(repo: Path, lineage: list[str]) -> tuple[list[str], Path, str]:
    roots = [confined(repo, f".loop-work/pi/{identifier(rid)}") for rid in lineage]
    sessions = sorted(path for directory in roots for path in directory.glob("*.jsonl"))
    require(len(sessions) <= 1, "Reconcile multiple native sessions for this book; never guess the latest")
    root = sessions[0].parent if sessions else roots[0]
    session_id = str(uuid.uuid5(uuid.NAMESPACE_URL, str(repo / "runs" / lineage[0])))
    options = ["--session-id", session_id, "--session-dir", str(root)]
    if sessions:
        require(not sessions[0].is_symlink(), "Native session must not be a symlink")
        line_no = 1
        try:
            with sessions[0].open(encoding="utf-8") as stream:
                header = parse_json(stream.readline())
                require(isinstance(header, dict) and header.get("type") == "session", "Invalid native session header")
                session_id = nonempty(header.get("id"), "Native Pi session identity")
                for line_no, line in enumerate(stream, 2):
                    if not line.strip():
                        continue
                    entry = parse_json(line)
                    require(isinstance(entry, dict) and isinstance(entry.get("type"), str) and
                            bool(entry["type"].strip()) and entry["type"] != "session", "Invalid native session record")
        except (FactoryError, UnicodeError) as exc:
            raise FactoryError(f"Repair damaged native session near line {line_no}: reconcile worker ownership; "
                               "once idle, preserve the original and recover from intact history/frozen artifacts "
                               "before resuming this book") from exc
        options = ["--session", str(sessions[0]), "--session-dir", str(root)]
    return options, root, session_id


def launch_plan(repo: Path, iteration: str, run_id: str, agent_dir: Path,
                extension: Path | None = None, pi: str = "pi", brief: Path | None = None,
                caller_context: Path | None = None) -> dict:
    """Inspect one book; extension is an ignored legacy argument, never loaded."""
    repo = repo.resolve()
    p = progress_record(repo, iteration, for_launch=True)
    books = _allocated_runs(repo, iteration, p)
    successors = [rid for rid, (_, chain) in books.items() if run_id in chain[:-1]]
    if successors:
        # _allocated_runs has already proved an unbranched same-book lineage.
        run_id = successors[0]
    preparation = None
    if run_id in books:
        run, lineage = books[run_id]
        # Preparation binds the initial run. Validated same-book successors may
        # freeze repaired runtime contracts while preserving their source history.
        _check_handoff(repo, lineage[0], Run(repo, lineage[0]))
        if brief is not None:
            require(digest(document(brief)) == digest(run.brief), "Requested brief differs from this frozen book")
        if caller_context is not None:
            require(run.caller_context is not None and
                    digest(document(caller_context)) == digest(run.caller_context),
                    "Requested caller guidance differs from this frozen book")
        status = run.status()
        if status["status"] == "COMPLETE_UNRELEASED" and not pending_caller_repair(run):
            return {"status": "ALREADY_COMPLETE", "run_id": run_id, "book_id": lineage[0],
                    "next_run": run_id, "factory": run.complete()}
        snapshot, config = run.root / "snapshot", run.config
        repo_arg = shlex.quote(str(repo))
        prompt = (
            f"Operate snapshot {run_id} of logical book {lineage[0]}. Its repository is {repo}. "
            f"Use scripts/factory.py --repo {repo_arg} with --run {run_id}; inspect status first. "
            "You own this book end-to-end. Execute model-only stages through frozen task/execute; "
            "never author a stage result yourself. Follow the frozen factory-orchestrator contract. "
            "If evidence review requires research repair, load prompts/research-agent.md and "
            f"prepare one linked successor using --research-revision-of {run_id}, an iter{iteration}- ID, "
            "a fresh subject preflight, the identical brief, caller context, parent, fixture/live status and model identities. "
            "Return immediately after preparing it; the launcher automatically rebinds this same session to its snapshot. "
            "Reopen a complete book only for a valid sealed caller-feedback repair. "
            "Return at verified COMPLETE_UNRELEASED or a concrete unresolved gate/infrastructure failure. "
            "Configured model calls and read-only research are authorized. The outer controller owns hypothesis, evaluation and advancement."
        )
    else:
        preparation = _preparation(repo, iteration, run_id, p, books, brief, caller_context)
        lineage = [run_id]
        snapshot = Path(preparation["root"])
        config = read_json(snapshot / "factory/config.json") if preparation["frozen"] else read_json(repo / "factory/config.json")
        prepare_argv = ["python3", "scripts/factory.py", "--repo", str(repo), "prepare", "--run", run_id,
                        "--brief", str(snapshot / "inputs/brief.json"), "--research", str(snapshot / "inputs/research.json"),
                        "--research-preflight", str(snapshot / "inputs/research-preflight.json")]
        if preparation["caller_context"] is not None:
            prepare_argv += ["--caller-context", str(snapshot / "inputs/caller-context.json")]
        prompt = (
            f"Research and prepare logical book {run_id}, repository {repo}, from this frozen preparation workspace. "
            "Read prompts/research-agent.md and docs/RESEARCH-ACCESS.md; resume retained local research if present. "
            "The supplied inputs/brief.json and optional inputs/caller-context.json are frozen: preserve their exact content. "
            "Carry out fresh subject preflight and substantial general-web, Reddit, authenticated X and recovery-forum research, "
            "including original source/thread reading, counterevidence and honest inference bounds. Retain research provenance. "
            "Save the substantive dossier as inputs/research.json and the actual successful preflight as inputs/research-preflight.json. "
            f"Then use {shlex.join(prepare_argv)}. "
            "Return immediately after successful preparation: the launcher automatically resumes this same book/session "
            "in the resulting snapshot for the remaining complete factory workflow. Never manufacture role results or access readiness. "
            "Configured model calls and read-only research are authorized. Return concrete blockers if preparation cannot honestly complete."
        )
    # Native Bash does not forward extra FDs. Existing execution locks fence a
    # role that outlives Pi, including an interrupted earlier book in this iteration.
    inflight = [path for _, chain in books.values() for rid in chain
                for path in (Run(repo, rid).root / "inflight").glob("*/.factory.lock")]
    require(not inflight, "A factory role execution lock remains; reconcile its result and owner before relaunch")
    model = _go_routes(config)
    agent_dir = agent_dir.resolve()
    executable = shutil.which(pi)
    require(executable is not None, "Repair/install the Pi executable before launch")
    executable = os.path.join(os.getcwd(), executable)
    provider = read_json(agent_dir / "models.json").get("providers", {}).get("opencode-go", {})
    route = config["profiles"]["factory"]["routes"][0]
    require(provider.get("baseUrl", "").rstrip("/") == "https://opencode.ai/zen/go/v1" and
            provider.get("api") == {"responses": "openai-responses", "chat": "openai-completions"}[route["api"]],
            "Repair the Pi OpenCode Go provider mapping to match the frozen factory")
    selected = [m for m in provider.get("models", []) if isinstance(m, dict) and m.get("id") == model]
    require(len(selected) == 1, "Repair the Pi model catalog for the frozen generator; select exactly one model")
    overrides = provider.get("modelOverrides", {})
    require(isinstance(overrides, dict), "Repair the Pi model overrides")
    for settings in (selected[0], overrides.get(model, {})):
        base_url = settings.get("baseUrl", provider["baseUrl"]) if isinstance(settings, dict) else None
        require(isinstance(base_url, str) and base_url.rstrip("/") == provider["baseUrl"].rstrip("/") and
                settings.get("api", provider["api"]) == provider["api"],
                "Repair the Pi model-specific route; it must match the frozen OpenCode Go API/endpoint")
    options, root, session_id = _session_options(repo, lineage)
    wrapper = snapshot / ".pi/agents/factory-orchestrator.md"
    require(wrapper.is_file() or preparation is not None and not preparation["frozen"], "Frozen factory wrapper is missing")
    argv = [executable, "--provider", "opencode-go", "--model", model,
            "--models", f"opencode-go/{model}", "--thinking", "high", "--mode", "json", *options, "--approve",
            "--no-extensions", "--no-skills", "--no-prompt-templates", "--no-context-files",
            "--append-system-prompt", str(snapshot / "AGENTS.md"),
            "--append-system-prompt", str(wrapper), "-p", prompt]
    return {"status": "READY_TO_LAUNCH", "run_id": run_id, "book_id": lineage[0], "cwd": str(snapshot),
            "argv": argv, "agent_dir": str(agent_dir), "log": str(root / "console.log"),
            "session_id": session_id, "session_dir": str(root), "preparation": preparation}


@contextlib.contextmanager
def worker_lock(repo: Path, iteration: str):
    """Kernel-owned lock survives into Pi; stale PID/service text never owns it."""
    require(os.name == "posix", "Use a POSIX host for the Pi PTY launcher")
    import fcntl
    root = confined(repo, ".loop-work/pi")
    root.mkdir(parents=True, exist_ok=True)
    fd = os.open(root / f"iteration-{identifier(iteration)}.lock", os.O_CREAT | os.O_RDWR, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise FactoryError("A Pi launch still owns this iteration; inspect it, do not duplicate it") from exc
        os.set_inheritable(fd, True)
        yield fd
    finally:
        # No unlink/explicit unlock: an orphaned child can still own the same
        # open-file description until it genuinely exits.
        os.close(fd)


def _pty_run(plan: dict) -> int:
    import pty
    log = Path(plan["log"])
    log.parent.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PI_CODING_AGENT_DIR": plan["agent_dir"]}
    env.pop("BC_PI_WORKER_LOCK_FD", None)
    if plan.get("lock_fd") is not None:
        env["BC_PI_WORKER_LOCK_FD"] = str(plan["lock_fd"])
    fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    with os.fdopen(fd, "ab") as output:
        # Pi restores header.cwd on resume, overriding the process directory.
        # The caller holds the worker lock; retain metadata history in the existing log.
        if "--session" in plan["argv"]:
            session = Path(plan["argv"][plan["argv"].index("--session") + 1])
            original_header, _, history = session.read_bytes().partition(b"\n")
            header = parse_json(original_header.decode("utf-8"))
            if header.get("cwd") != plan["cwd"]:
                output.write(b"Pi workspace rebind; previous session header: " + original_header + b"\n")
                output.flush()
                os.fsync(output.fileno())
                header["cwd"] = plan["cwd"]
                atomic_bytes(session, json.dumps(header, ensure_ascii=False).encode("utf-8") + b"\n" + history)
        pid, master = pty.fork()
        if pid == 0:
            phase = "chdir"
            try:
                os.chdir(plan["cwd"])
                phase = "exec"
                os.execvpe(plan["argv"][0], plan["argv"], env)
            except Exception as exc:
                # Log mechanics, not exception text/argv/env that may contain secrets.
                diagnostic = (f"Pi launch failed during {phase}: {type(exc).__name__} "
                              f"(errno={getattr(exc, 'errno', None)})\n")
                with contextlib.suppress(OSError):
                    os.write(2, diagnostic.encode("utf-8"))
                os._exit(127)
        try:
            while True:
                try:
                    chunk = os.read(master, 65536)
                except OSError as exc:
                    if exc.errno == errno.EIO:
                        break
                    raise
                if not chunk:
                    break
                output.write(chunk)
                output.flush()
        finally:
            os.close(master)
        _, status = os.waitpid(pid, 0)
    return os.waitstatus_to_exitcode(status)


def launch_book(repo: Path, iteration: str, run_id: str, agent_dir: Path,
                extension: Path | None = None, pi: str = "pi", allow_paid: bool = False,
                brief: Path | None = None, caller_context: Path | None = None) -> dict:
    """Run one logical book, automatically crossing preparation/research handoffs."""
    if not allow_paid:
        return launch_plan(repo, iteration, run_id, agent_dir, extension, pi, brief, caller_context)
    with worker_lock(repo, iteration) as lock_fd:
        current = run_id
        while True:
            plan = launch_plan(repo, iteration, current, agent_dir, extension, pi, brief, caller_context)
            if plan["status"] == "ALREADY_COMPLETE":
                return plan
            current = plan["run_id"]
            require(bool(os.environ.get("OPENCODE_GO_API_KEY", "").strip()),
                    "Repair the existing authorized OPENCODE_GO_API_KEY wiring before launch")
            if plan["preparation"] is not None:
                _freeze_preparation(repo.resolve(), plan["preparation"])
            plan["lock_fd"] = lock_fd
            code = _pty_run(plan)
            p = progress_record(repo, iteration)
            books = _allocated_runs(repo, iteration, p)
            next_run = next((rid for rid, (_, chain) in books.items() if current in chain), current)
            if current in books:
                run = books[current][0]
                status = run.status()
                complete = status["status"] == "COMPLETE_UNRELEASED" and not pending_caller_repair(run)
                if complete:
                    status = run.complete()
            else:
                status, complete = {"status": "UNPREPARED", "run_id": current}, False
            stopped = p["execution_status"] != "ACTIVE" or p["authorization"]["status"] != "APPROVED"
            # Reconcile durable effects even after an abnormal exit. A known
            # prepared successor is progress; an unchanged unfinished run is not.
            transition = next_run != current or plan["preparation"] is not None and current in books
            if transition and not stopped:
                current = next_run
                brief = caller_context = None
                continue
            return {"status": "COMPLETE_UNRELEASED" if complete else "STOPPED" if stopped else "NEEDS_INSPECTION",
                    "worker_exit_code": code, "factory": status, "book_id": plan["book_id"], "next_run": next_run,
                    "log": plan["log"], "session_id": plan["session_id"], "session_dir": plan["session_dir"]}
