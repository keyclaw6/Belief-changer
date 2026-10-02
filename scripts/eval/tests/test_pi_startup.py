"""Opt-in installed Pi checks: real PTY/tools/session, isolated network, no inference.

Set BC_PI_EXECUTABLE to test an installed build. No subagent example is loaded.
"""
from __future__ import annotations
import contextlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from bc_autoresearch.operations import launch_plan, scope_digest, worker_lock
from bc_factory.common import file_hash
from bc_factory.demo import inputs, scaffold
from bc_factory.runs import prepare


@unittest.skipUnless(os.environ.get("BC_PI_EXECUTABLE"),
                     "Set BC_PI_EXECUTABLE for the zero-network native startup check")
class InstalledPiStartupTests(unittest.TestCase):
    def test_native_tools_use_only_the_selected_frozen_workspace(self):
        self.check_startup()

    def test_native_resume_rebinds_preparation_session_without_losing_history(self):
        self.check_startup(resume=True)

    def test_native_stage_execution_fences_a_duplicate_after_parent_lock_closes(self):
        self.check_startup(stage=True)

    def test_native_bash_reports_a_killed_stage_as_failure(self):
        self.check_startup(stage=True, crash=True)

    def check_startup(self, resume=False, stage=False, crash=False):
        self.assertTrue(shutil.which("unshare"), "Network namespace required; do not run the probe online")
        check = subprocess.run(["unshare", "--user", "--map-root-user", "--net", "true"],
                               capture_output=True, timeout=5)
        self.assertEqual(check.returncode, 0, "Network isolation unavailable; no Pi process was started")
        executable = Path(os.environ["BC_PI_EXECUTABLE"]).absolute()
        with tempfile.TemporaryDirectory(prefix="bc-pi-startup-") as directory:
            base, repo = Path(directory), Path(directory) / "repo"
            scaffold(ROOT, repo)
            brief, research, _ = inputs("practice-belief")
            prepare(repo, "iter901-a", brief, research, fixture=True)
            iteration = repo / "loop/iterations/901"
            iteration.mkdir(parents=True)
            (iteration / "hypothesis.md").write_text("Synthetic infrastructure probe; not an experiment.")
            progress = {"schema_version": 1, "iteration": "901", "execution_status": "ACTIVE",
                        "preregistration_sha256": file_hash(iteration / "hypothesis.md"),
                        "allocation": {"practice-belief": 1},
                        "authorization": {"status": "APPROVED", "reference": "synthetic-test-only",
                                          "quote": "Offline infrastructure only; no model calls."}}
            progress["authorization"]["scope_sha256"] = scope_digest(progress)
            (iteration / "progress.json").write_text(json.dumps(progress))
            (repo / "AGENTS.md").write_text("OUTER_CONTEXT_SENTINEL_DO_NOT_INHERIT")
            agent = base / "agent"
            agent.mkdir()
            model = json.loads((ROOT / "factory/config.json").read_text())["profiles"]["factory"]["routes"][0]["model"]
            (agent / "models.json").write_text(json.dumps({"providers": {"opencode-go": {
                "baseUrl": "https://opencode.ai/zen/go/v1", "api": "openai-responses",
                "apiKey": "offline-placeholder", "models": [{"id": model, "reasoning": True}]}}}))
            plan = launch_plan(repo, "901", "iter901-a", agent, pi=str(executable))
            if resume:
                saved = Path(plan["session_dir"]) / "saved.jsonl"
                saved.parent.mkdir(parents=True)
                header = {"type": "session", "version": 3, "id": plan["session_id"],
                          "timestamp": "2026-10-01T00:00:00.000Z", "cwd": str(base / "old-preparation")}
                entry = {"type": "message", "id": "fixture-user", "parentId": None,
                         "timestamp": "2026-10-01T00:00:01.000Z",
                         "message": {"role": "user", "content": [{"type": "text", "text": "SAVED_SESSION_PROBE"}],
                                     "timestamp": 1790812801000}}
                saved.write_text(json.dumps(header) + "\n" + json.dumps(entry) + "\n")
                plan = launch_plan(repo, "901", "iter901-a", agent, pi=str(executable))
            helper = base / "stage.py"
            helper.write_text('''import os,signal,time
from pathlib import Path
from bc_factory.common import lock
with lock(Path(os.environ["BC_PROBE_ROLE_LOCK"])):
    Path(os.environ["BC_PROBE_READY"]).write_text(str(Path.cwd()))
    while not Path(os.environ["BC_PROBE_RELEASE"]).exists(): time.sleep(.01)
    if os.environ["BC_PROBE_CRASH"] == "1": os.kill(os.getpid(),signal.SIGKILL)
''')
            fence = base / "fence.py"
            fence.write_text('''import os
from pathlib import Path
from bc_autoresearch.operations import launch_plan,worker_lock
from bc_factory.common import FactoryError
with worker_lock(Path(os.environ["BC_PROBE_REPO"]),"901"):
    try:
        launch_plan(Path(os.environ["BC_PROBE_REPO"]),"901","iter901-a",Path(os.environ["PI_CODING_AGENT_DIR"]),pi=os.environ["BC_PROBE_PI"])
    except FactoryError as exc:
        assert "role execution lock" in str(exc)
    else: raise AssertionError("Active role admitted a duplicate controller")
''')
            probe = base / "probe.ts"
            probe.write_text('''import fs from "node:fs";
import {spawnSync} from "node:child_process";
import {createBashTool,createReadTool} from "@earendil-works/pi-coding-agent";
const wait=(file)=>new Promise(resolve=>{
 const watcher=fs.watch(process.env.BC_PROBE_DIR,()=>{if(fs.existsSync(file)){watcher.close();resolve();}});
 if(fs.existsSync(file)){watcher.close();resolve();}
});
export default function(pi){
 pi.on("before_agent_start",()=>process.exit(91));
 pi.on("session_start",async(_event,ctx)=>{
   const read=await createReadTool(ctx.cwd).execute("read-probe",{path:".pi/agents/factory-orchestrator.md"},undefined);
   const pwd=await createBashTool(ctx.cwd).execute("bash-probe",{command:"pwd"},undefined);
   const row={kind:"startup",cwd:ctx.cwd,model:ctx.model?.id,sessionId:ctx.sessionManager.getSessionId(),
     restored:JSON.stringify(ctx.sessionManager.getBranch()).includes("SAVED_SESSION_PROBE"),
     provider:ctx.model?.provider,api:ctx.model?.api,baseUrl:ctx.model?.baseUrl,
     frozenContext:ctx.getSystemPrompt().includes("Immutable evidence and honest status"),
     outerContext:ctx.getSystemPrompt().includes("OUTER_CONTEXT_SENTINEL_DO_NOT_INHERIT"),
     tools:pi.getAllTools().map(tool=>tool.name),
     readWrapper:JSON.stringify(read).includes("factory-orchestrator"),bashCwd:pwd.content[0]?.text?.trim()};
   fs.appendFileSync(process.env.BC_PROBE_OUT,JSON.stringify(row)+"\\n");
   if(process.env.BC_PROBE_STAGE === "1"){
     const fd=Number(process.env.BC_PI_WORKER_LOCK_FD);
     row.lockInode=fs.fstatSync(fd).ino;
     const pending=createBashTool(ctx.cwd).execute("owned-stage",{command:'"$BC_PROBE_PYTHON" "$BC_PROBE_STAGE_SCRIPT"'},undefined);
     // Immediately install both promise handlers: a killed child is expected.
     const finished=pending.then(result=>({failed:result.isError===true||result.structuredContent?.exit_code!==0,exit:result.structuredContent?.exit_code}),()=>({failed:true,exit:null}));
     await wait(process.env.BC_PROBE_READY);
     await wait(process.env.BC_PROBE_DRIVER_RELEASE);
     await wait(process.env.BC_PROBE_TEST_RELEASE);
     fs.closeSync(fd);
     const result=spawnSync(process.env.BC_PROBE_PYTHON,[process.env.BC_PROBE_FENCE_SCRIPT]);
     fs.appendFileSync(process.env.BC_PROBE_OUT,JSON.stringify({kind:"ownership",inode:row.lockInode,
       fenced:result.status===0,stageCwd:fs.readFileSync(process.env.BC_PROBE_READY,"utf8")})+"\\n");
     fs.writeFileSync(process.env.BC_PROBE_RELEASE,"release");
     fs.appendFileSync(process.env.BC_PROBE_OUT,JSON.stringify({kind:"stage",...await finished})+"\\n");
   }
   process.exit(0);
 });
}
''')
            # Startup instrumentation is explicit, isolated, and exits before inference.
            plan["argv"][1:1] = ["--extension", str(probe)]
            plan["argv"] = ["unshare", "--user", "--map-root-user", "--net", *plan["argv"]]
            out = base / "probe.jsonl"
            (base / "home").mkdir()
            env = {"HOME": str(base / "home"), "PATH": str(executable.parent) + ":/usr/bin:/bin", "LANG": "C.UTF-8",
                   "PI_OFFLINE": "1", "BC_PROBE_OUT": str(out), "PYTHONPATH": str(ROOT / "scripts"),
                   "BC_PROBE_DIR": str(base), "BC_PROBE_STAGE": "1" if stage else "0", "BC_PROBE_CRASH": "1" if crash else "0",
                   "BC_PROBE_READY": str(base / "stage-ready"), "BC_PROBE_RELEASE": str(base / "release-stage"),
                   "BC_PROBE_TEST_RELEASE": str(base / "test-released"), "BC_PROBE_DRIVER_RELEASE": str(base / "driver-released"),
                   "BC_PROBE_PYTHON": sys.executable, "BC_PROBE_PI": str(executable), "BC_PROBE_REPO": str(repo),
                   "BC_PROBE_STAGE_SCRIPT": str(helper), "BC_PROBE_FENCE_SCRIPT": str(fence),
                   "BC_PROBE_ROLE_LOCK": str(repo / "runs/iter901-a/inflight/offline-probe")}
            driver = '''import json,os,pty,sys
from pathlib import Path
from bc_autoresearch.operations import _pty_run
plan=json.loads(sys.argv[1])
if os.environ["BC_PROBE_STAGE"] == "1":
    native_fork=pty.fork
    def fork():
        pid,master=native_fork()
        if pid:
            os.close(plan["lock_fd"])
            Path(os.environ["BC_PROBE_DRIVER_RELEASE"]).write_text("closed")
        return pid,master
    pty.fork=fork
sys.exit(_pty_run(plan))
'''
            with contextlib.ExitStack() as owner:
                pass_fds = ()
                if stage:
                    fd = owner.enter_context(worker_lock(repo, "901"))
                    plan["lock_fd"] = fd
                    inode = os.fstat(fd).st_ino
                    pass_fds = (fd,)
                proc = subprocess.Popen([sys.executable, "-c", driver, json.dumps(plan)], env=env,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        start_new_session=True, pass_fds=pass_fds)
            (base / "test-released").write_text("closed")
            try:
                _, stderr = proc.communicate(timeout=25)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.communicate()
                self.fail("Native startup probe timed out; no real credentials or network were available")
            log = Path(plan["log"]).read_text(errors="replace") if Path(plan["log"]).exists() else ""
            self.assertEqual(proc.returncode, 0, (stderr.decode(errors="replace") + log)[-2500:])
            self.assertTrue(out.exists(), "Pi did not load startup instrumentation")
            rows = [json.loads(line) for line in out.read_text().splitlines()]
            row = rows[0]
            self.assertFalse(row["outerContext"])
            self.assertTrue(row["frozenContext"])
            self.assertTrue(row["readWrapper"])
            self.assertEqual(row["bashCwd"], plan["cwd"])
            self.assertEqual(row["cwd"], plan["cwd"])
            self.assertEqual((row["model"], row["provider"], row["api"], row["baseUrl"]),
                             (model, "opencode-go", "openai-responses", "https://opencode.ai/zen/go/v1"))
            self.assertEqual(row["sessionId"], plan["session_id"])
            self.assertEqual(row["restored"], resume)
            self.assertTrue({"read", "bash"}.issubset(row["tools"]))
            self.assertNotIn("subagent", row["tools"])
            if stage:
                self.assertEqual(rows[1], {"kind": "ownership", "inode": inode, "fenced": True, "stageCwd": plan["cwd"]})
                self.assertEqual(rows[2]["kind"], "stage")
                self.assertEqual(rows[2]["failed"], crash)
                self.assertEqual(rows[2]["exit"] == 0, not crash)
                with worker_lock(repo, "901"):
                    pass


if __name__ == "__main__":
    unittest.main()
