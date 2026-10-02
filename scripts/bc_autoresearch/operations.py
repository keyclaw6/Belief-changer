"""Outer handoff and one-book Pi launch, not a scheduler or autoresearch engine.

progress.json is the existing compact handoff. Approval references are operator
assertions to check against the human source, not cryptographic consent.
"""
from __future__ import annotations

import contextlib
import errno
import json
import os
import shutil
import uuid
from pathlib import Path

from bc_factory.common import (FactoryError, confined, digest, file_hash, identifier,
                               nonempty, parse_json, read_json, require, atomic_bytes, text_hash)
from bc_factory.runs import Run, load_caller_repair


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


def isolated_subagent_source(extension: Path, snapshot: Path) -> str:
    """Reuse Pi's installed tool; isolate children and retain failure status.

    The upstream example does not forward the parent's isolation flags. Keep
    its dispatch/discovery implementation instead of maintaining another tool.
    An unsupported upstream shape needs a reviewed compatibility repair.
    """
    text = extension.read_text(encoding="utf-8")
    anchor = 'const args: string[] = ["--mode", "json", "-p", "--no-session"];'
    discovery = 'from "./agents.ts";'
    close_result = 'resolve(code ?? 0);'
    child_stdio = 'stdio: ["ignore", "pipe", "pipe"],'
    require(text.count(anchor) == 1 and text.count(discovery) == 1 and
            text.count(close_result) == 1 and text.count(child_stdio) == 1 and
            (extension.parent / "agents.ts").is_file(),
            "Repair Pi subagent startup compatibility; its installed entry point changed")
    child_args = ["--mode", "json", "-p", "--no-session", "--approve",
                  "--no-context-files", "--no-extensions", "--no-skills", "--no-prompt-templates",
                  "--append-system-prompt", str(snapshot / "AGENTS.md")]
    # A signal-killed child has no numeric exit code. It is a failed call,
    # never an empty successful role result.
    return text.replace(anchor, "const args: string[] = " + json.dumps(child_args) + ";").replace(
        discovery, "from " + json.dumps(str(extension.parent / "agents.ts")) + ";").replace(
        close_result, 'resolve(code ?? 1);').replace(
        child_stdio,
        # Node closes unlisted descriptors. Preserve the same kernel ownership in
        # the role child as fd 3, with its environment pointing to the new number.
        'stdio: process.env.BC_PI_WORKER_LOCK_FD ? ["ignore", "pipe", "pipe", '
        'Number(process.env.BC_PI_WORKER_LOCK_FD)] : ["ignore", "pipe", "pipe"],\n'
        'env: {...process.env, ...(process.env.BC_PI_WORKER_LOCK_FD ? {BC_PI_WORKER_LOCK_FD: "3"} : {})},')


def launch_plan(repo: Path, iteration: str, run_id: str, agent_dir: Path,
                extension: Path, pi: str = "pi") -> dict:
    repo = repo.resolve()
    p = progress_record(repo, iteration, for_launch=True)
    books = _allocated_runs(repo, iteration, p)
    successors = [rid for rid, (_, chain) in books.items() if run_id in chain[:-1]]
    require(not successors, f"Run has an existing successor: {', '.join(successors)}; resume that same book")
    require(run_id in books, "Prepare this authorized run first, using a fresh research preflight")
    run, lineage = books[run_id]
    book_id = lineage[0]
    status = run.status()
    if status["status"] == "COMPLETE_UNRELEASED" and not pending_caller_repair(run):
        return {"status": "ALREADY_COMPLETE", "factory": status}
    # Prepared/paused books are not live workers. The kernel lock serializes
    # execution; do not create a circular block between two unfinished runs.
    model = _go_routes(run.config)
    agent_dir, extension = agent_dir.resolve(), extension.resolve()
    require(extension.is_file(), "Repair/install the Pi subagent extension before launch")
    executable = shutil.which(pi)
    require(executable is not None, "Repair/install the Pi executable before launch")
    # Pin before changing cwd; preserve the chosen symlink/venv invocation.
    executable = os.path.join(os.getcwd(), executable)
    provider = read_json(agent_dir / "models.json").get("providers", {}).get("opencode-go", {})
    factory_route = run.config["profiles"]["factory"]["routes"][0]
    require(provider.get("baseUrl", "").rstrip("/") == "https://opencode.ai/zen/go/v1" and
            provider.get("api") == {"responses": "openai-responses", "chat": "openai-completions"}[factory_route["api"]],
            "Repair the Pi OpenCode Go provider mapping to match the frozen factory")
    selected = [m for m in provider.get("models", []) if isinstance(m, dict) and m.get("id") == model]
    require(len(selected) == 1,
            "Repair the Pi model catalog for the frozen generator; select exactly one model")
    overrides = provider.get("modelOverrides", {})
    require(isinstance(overrides, dict), "Repair the Pi model overrides")
    for settings in (selected[0], overrides.get(model, {})):
        base_url = settings.get("baseUrl", provider["baseUrl"]) if isinstance(settings, dict) else None
        require(isinstance(base_url, str) and base_url.rstrip("/") == provider["baseUrl"].rstrip("/") and
                settings.get("api", provider["api"]) == provider["api"],
                "Repair the Pi model-specific route; it must match the frozen OpenCode Go API/endpoint")
    roots = [confined(repo, f".loop-work/pi/{identifier(rid)}") for rid in lineage]
    sessions = sorted(path for directory in roots for path in directory.glob("*.jsonl"))
    require(len(sessions) <= 1, "Reconcile multiple native sessions for this book; never guess the latest")
    # Reuse the one existing native history, including a pre-upgrade successor's
    # location. A new logical book never imports another book's conversation.
    root = sessions[0].parent if sessions else roots[0]
    session_id = str(uuid.uuid5(uuid.NAMESPACE_URL, str(repo / "runs" / book_id)))
    session_options = ["--session-id", session_id, "--session-dir", str(root)]
    if sessions:
        require(not sessions[0].is_symlink(), "Native session must not be a symlink")
        line_no = 1
        try:
            with sessions[0].open(encoding="utf-8") as stream:
                header = parse_json(stream.readline())
                require(isinstance(header, dict) and header.get("type") == "session",
                        "Invalid native session header")
                session_id = nonempty(header.get("id"), "Native Pi session identity")
                # A valid header is not an intact transcript. Inspect structure only;
                # preserve unknown extension records and never silently drop a tail.
                for line_no, line in enumerate(stream, 2):
                    if not line.strip():
                        continue
                    entry = parse_json(line)
                    require(isinstance(entry, dict) and
                            isinstance(entry.get("type"), str) and bool(entry["type"].strip()) and
                            entry["type"] != "session", "Invalid native session record")
        except (FactoryError, UnicodeError) as exc:
            raise FactoryError(f"Repair damaged native session near line {line_no}: reconcile worker ownership; "
                               "once idle, preserve the original and recover from intact history/frozen artifacts "
                               "before resuming this book") from exc
        session_options = ["--session", str(sessions[0]), "--session-dir", str(root)]
    snapshot = run.root / "snapshot"
    wrapper = snapshot / ".pi/agents/factory-orchestrator.md"
    require(wrapper.is_file(), "Frozen factory wrapper is missing; repair the snapshot lineage")
    subagent = isolated_subagent_source(extension, snapshot)
    subagent_path = root / "subagent.ts"
    prompt = (
        f"Operate snapshot {run_id} of the already-prepared logical book {book_id}. Its repository is {repo}. "
        f"Use this snapshot as the project root, and invoke scripts/factory.py --repo {repo} "
        f"with --run {run_id}. Inspect status before doing work. Do not start an unrelated book or sample. "
        "If independent evidence review requires revised research, dispatch the researcher to close its findings. "
        f"You may prepare one linked successor with --research-revision-of {run_id} and an iter{iteration}- run ID, "
        "a fresh subject research preflight, the same brief, parent release, fixture/live status and caller context, "
        "and unchanged model identities. Preserve the prior snapshot and findings. After preparation, return "
        "the successor run ID to the host without executing its stages here: the host relaunches this same "
        "book/session against the successor snapshot so runtime context is not mixed. "
        "If status is complete, reopen only for a valid sealed caller-feedback repair request; "
        "otherwise hand back the verified result. Follow the factory-orchestrator contract "
        "and dispatch project-local roles with agentScope=project. "
        "This book's configured model calls are authorized. Never author or manufacture a "
        "role result yourself. Keep the frozen inputs, generator model and independent "
        "evaluator unchanged. Return at verified COMPLETE_UNRELEASED or with concrete "
        "evidence of an infrastructure/stage blocker. The host owns operational repair "
        "and everything outside this factory call."
    )
    argv = [executable, "--provider", "opencode-go", "--model", model,
            "--models", f"opencode-go/{model}", "--thinking", "high", "--mode", "json",
            *session_options, "--approve",
            "--no-extensions", "--extension", str(subagent_path), "--no-skills",
            "--no-prompt-templates", "--no-context-files",
            "--append-system-prompt", str(snapshot / "AGENTS.md"),
            "--append-system-prompt", str(wrapper), "-p", prompt]
    return {"status": "READY_TO_LAUNCH", "run_id": run_id, "book_id": book_id, "cwd": str(snapshot),
            "argv": argv, "agent_dir": str(agent_dir), "log": str(root / "console.log"),
            "session_id": session_id, "session_dir": str(root),
            "subagent": {"source": str(extension), "source_sha256": file_hash(extension),
                         "path": str(subagent_path), "sha256": text_hash(subagent)}}


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
                extension: Path, pi: str = "pi", allow_paid: bool = False) -> dict:
    if not allow_paid:
        return launch_plan(repo, iteration, run_id, agent_dir, extension, pi)
    with worker_lock(repo, iteration) as lock_fd:
        plan = launch_plan(repo, iteration, run_id, agent_dir, extension, pi)
        if plan["status"] == "ALREADY_COMPLETE":
            return plan
        plan["lock_fd"] = lock_fd
        require(bool(os.environ.get("OPENCODE_GO_API_KEY", "").strip()),
                "Repair the existing authorized OPENCODE_GO_API_KEY wiring before launch")
        subagent = isolated_subagent_source(Path(plan["subagent"]["source"]), Path(plan["cwd"]))
        require(text_hash(subagent) == plan["subagent"]["sha256"], "Pi extension changed since launch inspection")
        atomic_bytes(Path(plan["subagent"]["path"]), subagent.encode("utf-8"))
        code = _pty_run(plan)
        run = Run(repo, run_id)
        status = run.status()
        books = _allocated_runs(repo, iteration, progress_record(repo, iteration))
        next_run = next((rid for rid, (_, chain) in books.items() if run_id in chain), run_id)
        complete = (next_run == run_id and status["status"] == "COMPLETE_UNRELEASED"
                    and not pending_caller_repair(run))
        return {"status": "COMPLETE_UNRELEASED" if complete
                else "NEEDS_INSPECTION", "worker_exit_code": code, "factory": status,
                "book_id": plan["book_id"], "next_run": next_run,
                "log": plan["log"], "session_id": plan["session_id"], "session_dir": plan["session_dir"]}
