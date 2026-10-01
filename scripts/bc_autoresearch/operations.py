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


def _allocated_runs(repo: Path, iteration: str, p: dict) -> dict[str, Run]:
    excluded = p.get("excluded_runs", [])
    require(isinstance(excluded, list), "Excluded runs must be explicit records")
    excluded_ids = set()
    for record in excluded:
        excluded_ids.add(identifier(record["run_id"]))
        nonempty(record.get("reason"), "Exclusion reason")
    runs = {}
    counts = {subject: 0 for subject in p["allocation"]}
    for root in sorted((repo / "runs").glob(f"iter{iteration}-*")):
        if not root.is_dir() or root.name in excluded_ids:
            continue
        run = Run(repo, root.name)
        subject = run.manifest["subject"]
        require(subject in counts, "Prepared run has a subject outside the approved allocation")
        counts[subject] += 1
        runs[root.name] = run
    require(all(n <= p["allocation"][subject] for subject, n in counts.items()),
            "Prepared runs exceed the approved allocation; reconcile exclusions, do not enlarge scope")
    return runs


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
    require(text.count(anchor) == 1 and text.count(discovery) == 1 and
            text.count(close_result) == 1 and
            (extension.parent / "agents.ts").is_file(),
            "Repair Pi subagent startup compatibility; its installed entry point changed")
    child_args = ["--mode", "json", "-p", "--no-session", "--approve",
                  "--no-context-files", "--no-extensions", "--no-skills", "--no-prompt-templates",
                  "--append-system-prompt", str(snapshot / "AGENTS.md")]
    # A signal-killed child has no numeric exit code. It is a failed call,
    # never an empty successful role result.
    return text.replace(anchor, "const args: string[] = " + json.dumps(child_args) + ";").replace(
        discovery, "from " + json.dumps(str(extension.parent / "agents.ts")) + ";").replace(
        close_result, 'resolve(code ?? 1);')


def launch_plan(repo: Path, iteration: str, run_id: str, agent_dir: Path,
                extension: Path, pi: str = "pi") -> dict:
    repo = repo.resolve()
    p = progress_record(repo, iteration, for_launch=True)
    runs = _allocated_runs(repo, iteration, p)
    require(run_id in runs, "Prepare this authorized run first, using a fresh research preflight")
    run = runs[run_id]
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
    root = confined(repo, f".loop-work/pi/{identifier(run_id)}")
    session_id = str(uuid.uuid5(uuid.NAMESPACE_URL, str(repo / "runs" / run_id)))
    sessions = sorted(root.glob("*.jsonl"))
    require(len(sessions) <= 1, "Reconcile multiple native sessions for this book; never guess the latest")
    session_options = ["--session-id", session_id, "--session-dir", str(root)]
    if sessions:
        require(not sessions[0].is_symlink(), "Native session must not be a symlink")
        with sessions[0].open() as stream:
            header = parse_json(stream.readline())
        require(isinstance(header, dict) and header.get("type") == "session", "Recover the damaged native session header")
        session_id = nonempty(header.get("id"), "Native Pi session identity")
        session_options = ["--session", str(sessions[0]), "--session-dir", str(root)]
    snapshot = run.root / "snapshot"
    wrapper = snapshot / ".pi/agents/factory-orchestrator.md"
    require(wrapper.is_file(), "Frozen factory wrapper is missing; repair the snapshot lineage")
    subagent = isolated_subagent_source(extension, snapshot)
    subagent_path = root / "subagent.ts"
    prompt = (
        f"Operate only the already-prepared book {run_id}. Its repository is {repo}. "
        f"Use this snapshot as the project root, and invoke scripts/factory.py --repo {repo} "
        f"with --run {run_id}. Inspect status before doing work. Do not prepare another run. "
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
    return {"status": "READY_TO_LAUNCH", "run_id": run_id, "cwd": str(snapshot),
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
        yield
    finally:
        # No unlink/explicit unlock: an orphaned child can still own the same
        # open-file description until it genuinely exits.
        os.close(fd)


def _pty_run(plan: dict) -> int:
    import pty
    log = Path(plan["log"])
    log.parent.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PI_CODING_AGENT_DIR": plan["agent_dir"]}
    fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    with os.fdopen(fd, "ab") as output:
        pid, master = pty.fork()
        if pid == 0:
            try:
                os.chdir(plan["cwd"])
                os.execvpe(plan["argv"][0], plan["argv"], env)
            except Exception:
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
    with worker_lock(repo, iteration):
        plan = launch_plan(repo, iteration, run_id, agent_dir, extension, pi)
        if plan["status"] == "ALREADY_COMPLETE":
            return plan
        require(bool(os.environ.get("OPENCODE_GO_API_KEY", "").strip()),
                "Repair the existing authorized OPENCODE_GO_API_KEY wiring before launch")
        subagent = isolated_subagent_source(Path(plan["subagent"]["source"]), Path(plan["cwd"]))
        require(text_hash(subagent) == plan["subagent"]["sha256"], "Pi extension changed since launch inspection")
        atomic_bytes(Path(plan["subagent"]["path"]), subagent.encode("utf-8"))
        code = _pty_run(plan)
        run = Run(repo, run_id)
        status = run.status()
        complete = status["status"] == "COMPLETE_UNRELEASED" and not pending_caller_repair(run)
        return {"status": "COMPLETE_UNRELEASED" if complete
                else "NEEDS_INSPECTION", "worker_exit_code": code, "factory": status,
                "log": plan["log"], "session_id": plan["session_id"], "session_dir": plan["session_dir"]}
