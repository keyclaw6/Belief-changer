"""Opt-in installed-Pi boundary check: isolated network, dummy auth, no model inference.

Set BC_PI_EXECUTABLE and BC_PI_SUBAGENT_EXTENSION to test an installed Pi build.
The ordinary offline suite skips this deployment-specific test.
"""
from __future__ import annotations
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
from bc_autoresearch.operations import isolated_subagent_source, launch_plan, scope_digest
from bc_factory.common import file_hash
from bc_factory.demo import inputs, scaffold
from bc_factory.runs import prepare


@unittest.skipUnless(os.environ.get("BC_PI_EXECUTABLE") and os.environ.get("BC_PI_SUBAGENT_EXTENSION"),
                     "Set installed Pi executable/subagent paths for the zero-network startup check")
class InstalledPiStartupTests(unittest.TestCase):
    def test_parent_and_actual_child_use_only_frozen_context(self):
        self.check_startup()

    def test_killed_child_is_not_reported_as_success(self):
        self.check_startup(child_crash=True)

    def test_native_resume_preserves_session_and_does_not_leak_to_child(self):
        self.check_startup(resume=True)

    def test_actual_child_retains_lock_after_parent_descriptors_close(self):
        self.check_startup(child_ownership=True)

    def check_startup(self, child_crash=False, resume=False, child_ownership=False):
        self.assertTrue(shutil.which("unshare"), "A network namespace is required; do not run this probe online")
        check = subprocess.run(["unshare", "--user", "--map-root-user", "--net", "true"],
                               capture_output=True, timeout=5)
        self.assertEqual(check.returncode, 0, "Network isolation unavailable; no Pi process was started")
        executable = Path(os.environ["BC_PI_EXECUTABLE"]).resolve()
        upstream = Path(os.environ["BC_PI_SUBAGENT_EXTENSION"]).resolve()
        with tempfile.TemporaryDirectory(prefix="bc-pi-startup-") as directory:
            base = Path(directory)
            repo = base / "repo"
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
            (agent / "extensions").mkdir(parents=True)
            model = json.loads((ROOT / "factory/config.json").read_text())["profiles"]["factory"]["routes"][0]["model"]
            (agent / "models.json").write_text(json.dumps({"providers": {"opencode-go": {
                "baseUrl": "https://opencode.ai/zen/go/v1", "api": "openai-responses",
                "apiKey": "offline-placeholder", "models": [{"id": model, "reasoning": True}]}}}))
            plan = launch_plan(repo, "901", "iter901-a", agent, upstream, str(executable))
            if resume:
                # A native-format saved user message, confined to this synthetic
                # fixture. No assistant/role response is manufactured.
                session_dir = Path(plan["session_dir"])
                session_dir.mkdir(parents=True)
                saved = session_dir / "saved.jsonl"
                header = {"type": "session", "version": 3, "id": plan["session_id"],
                          "timestamp": "2026-10-01T00:00:00.000Z", "cwd": plan["cwd"]}
                entry = {"type": "message", "id": "fixture-user", "parentId": None,
                         "timestamp": "2026-10-01T00:00:01.000Z",
                         "message": {"role": "user", "content": [{"type": "text", "text": "SAVED_SESSION_PROBE"}],
                                     "timestamp": 1790812801000}}
                saved.write_text(json.dumps(header) + "\n" + json.dumps(entry) + "\n")
                plan = launch_plan(repo, "901", "iter901-a", agent, upstream, str(executable))
                self.assertIn(str(saved), plan["argv"])
            generated = Path(plan["subagent"]["path"])
            generated.parent.mkdir(parents=True, exist_ok=True)
            probe = agent / "extensions/probe.ts"
            source = isolated_subagent_source(upstream, Path(plan["cwd"]))
            # Instrumentation only: explicitly load a startup probe in the otherwise
            # isolated child and exit before inference. Dispatch is the real Pi tool.
            source = source.replace('"--no-session",', '"--no-session", "--extension", ' + json.dumps(str(probe)) + ',', 1)
            generated.write_text(source)
            probe.write_text('import fs from "node:fs";\nimport {spawnSync} from "node:child_process";\nimport subagent from ' + json.dumps(str(generated)) + ';\n' + '''
function waitForFile(file) {
 return new Promise(resolve=>{
   const watcher=fs.watch(process.env.BC_PROBE_DIR,()=>{
     if(fs.existsSync(file)){watcher.close();resolve();}
   });
   if(fs.existsSync(file)){watcher.close();resolve();}
 });
}
export default function(pi) {
 let tool;
 const child=process.argv.includes("--no-session");
 const ownership=process.env.BC_PROBE_LOCK === "1";
 const lockFd=Number(process.env.BC_PI_WORKER_LOCK_FD);
 if(!child) subagent(new Proxy(pi,{get(target,key){
   if(key==="registerTool") return(def)=>{tool=def;return target.registerTool(def)};
   return Reflect.get(target,key);
 }}));
 pi.on("before_agent_start",()=>process.exit(91));
 pi.on("session_start",async(_event,ctx)=>{
   const row={kind:child?"child":"parent",cwd:ctx.cwd,model:ctx.model?.id,
     sessionId:ctx.sessionManager.getSessionId(),
     restored:JSON.stringify(ctx.sessionManager.getBranch()).includes("SAVED_SESSION_PROBE"),
     provider:ctx.model?.provider,api:ctx.model?.api,baseUrl:ctx.model?.baseUrl,
     frozenContext:ctx.getSystemPrompt().includes("Immutable evidence and honest status"),
     outerContext:ctx.getSystemPrompt().includes("OUTER_CONTEXT_SENTINEL_DO_NOT_INHERIT")};
   if(ownership){
     try{row.lockInode=fs.fstatSync(lockFd).ino;}catch{row.lockInode=null;}
   }
   fs.appendFileSync(process.env.BC_PROBE_OUT,JSON.stringify(row)+"\\n");
   if(!child){
     const ready=ownership?waitForFile(process.env.BC_PROBE_READY):null;
     const pending=tool.execute("offline-probe",{agent:"chapter-writer",task:"Offline startup only.",agentScope:"project"},undefined,undefined,ctx);
     if(ownership){
       await ready;
       await waitForFile(process.env.BC_PROBE_TEST_RELEASE);
       await waitForFile(process.env.BC_PROBE_DRIVER_RELEASE);
       fs.closeSync(lockFd);
       const check=spawnSync(process.env.BC_PROBE_PYTHON,["-c",
         "import fcntl,sys; f=open(sys.argv[1],'r+'); fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)",
         process.env.BC_PROBE_LOCK_PATH]);
       fs.appendFileSync(process.env.BC_PROBE_OUT,JSON.stringify({kind:"ownership",
         blocked:check.status===1 && check.stderr.toString().includes("BlockingIOError")})+"\\n");
       fs.writeFileSync(process.env.BC_PROBE_RELEASE,"release");
     }
     const result=await pending;
     fs.appendFileSync(process.env.BC_PROBE_OUT,JSON.stringify({kind:"dispatch",error:result.isError??false,exitCode:result.details?.results?.[0]?.exitCode})+"\\n");
   }else if(ownership){
     fs.writeFileSync(process.env.BC_PROBE_READY,"ready");
     await waitForFile(process.env.BC_PROBE_RELEASE);
   }
   if(child && process.env.BC_PROBE_CHILD_CRASH === "1") process.kill(process.pid, "SIGKILL");
   process.exit(0);
 });
}
''')
            plan["argv"][plan["argv"].index("--extension") + 1] = str(probe)
            # Use the actual PTY driver, bounded externally even if startup regresses.
            plan["argv"] = ["unshare", "--user", "--map-root-user", "--net", *plan["argv"]]
            out = base / "probe.jsonl"
            (base / "home").mkdir()
            env = {"HOME": str(base / "home"), "PATH": str(executable.parent) + ":/usr/bin:/bin",
                   "LANG": "C.UTF-8", "PI_OFFLINE": "1", "BC_PROBE_OUT": str(out),
                   "PYTHONPATH": str(ROOT / "scripts"),
                   "BC_PROBE_CHILD_CRASH": "1" if child_crash else "0",
                   "BC_PROBE_LOCK": "1" if child_ownership else "0",
                   "BC_PROBE_DIR": str(base), "BC_PROBE_READY": str(base / "child-ready"),
                   "BC_PROBE_RELEASE": str(base / "release-child"),
                   "BC_PROBE_TEST_RELEASE": str(base / "test-released"),
                   "BC_PROBE_DRIVER_RELEASE": str(base / "driver-released"),
                   "BC_PROBE_PYTHON": sys.executable,
                   "BC_PROBE_LOCK_PATH": str(repo / ".loop-work/pi/iteration-901.lock")}
            driver = '''
import json,os,pty,sys
from pathlib import Path
from bc_autoresearch.operations import _pty_run
plan=json.loads(sys.argv[1])
if os.environ.get("BC_PROBE_LOCK") == "1":
    native_fork=pty.fork
    def relinquishing_fork():
        pid,master=native_fork()
        if pid:
            os.close(plan["lock_fd"])
            Path(os.environ["BC_PROBE_DRIVER_RELEASE"]).write_text("closed")
        return pid,master
    pty.fork=relinquishing_fork
sys.exit(_pty_run(plan))
'''
            import contextlib
            from bc_autoresearch.operations import worker_lock
            with contextlib.ExitStack() as owner:
                pass_fds = ()
                if child_ownership:
                    fd = owner.enter_context(worker_lock(repo, "901"))
                    plan["lock_fd"] = fd
                    inode = os.fstat(fd).st_ino
                    pass_fds = (fd,)
                proc = subprocess.Popen([sys.executable, "-c", driver, json.dumps(plan)], env=env,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        start_new_session=True, pass_fds=pass_fds)
            (base / "test-released").write_text("closed")
            try:
                stdout, stderr = proc.communicate(timeout=20)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.communicate()
                self.fail("Installed Pi startup did not complete; no network access or real credentials were available")
            self.assertEqual(proc.returncode, 0, stderr.decode(errors="replace")[-2000:])
            self.assertTrue(out.exists(), "Pi did not load the startup probe")
            rows = [json.loads(line) for line in out.read_text().splitlines()]
            self.assertEqual([row["kind"] for row in rows],
                             ["parent", "child", "ownership", "dispatch"] if child_ownership
                             else ["parent", "child", "dispatch"])
            if child_ownership:
                self.assertEqual(rows[-2], {"kind": "ownership", "blocked": True})
                for row in rows[:2]:
                    self.assertEqual(row["lockInode"], inode, row["kind"])
                with worker_lock(repo, "901"):
                    pass  # All actual native owners exited; the old lock file is reusable.
            for row in rows[:2]:
                self.assertFalse(row["outerContext"], row["kind"])
                self.assertTrue(row["frozenContext"], row["kind"])
                self.assertEqual(row["cwd"], plan["cwd"])
                self.assertEqual(row["model"], model)
                self.assertEqual((row["provider"], row["api"], row["baseUrl"]),
                                 ("opencode-go", "openai-responses", "https://opencode.ai/zen/go/v1"))
            self.assertEqual(rows[0]["sessionId"], plan["session_id"])
            self.assertEqual(rows[0]["restored"], resume)
            self.assertFalse(rows[1]["restored"], "Independent child must not inherit the parent's transcript")
            self.assertNotEqual(rows[0]["sessionId"], rows[1]["sessionId"])
            self.assertEqual(rows[-1], {"kind": "dispatch", "error": child_crash, "exitCode": 1 if child_crash else 0})


if __name__ == "__main__":
    unittest.main()
