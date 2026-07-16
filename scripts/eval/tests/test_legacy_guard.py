"""RF-00 regressions for the factory-experimentation Legacy loop pause."""
import ast, contextlib, hashlib, importlib.util, io, sys, tempfile, unittest
from pathlib import Path
from unittest import mock
ROOT = Path(__file__).resolve().parents[3]
LOOP = ROOT / "scripts/loop"
sys.path.insert(0, str(ROOT / "scripts/eval"))
sys.path.insert(0, str(LOOP))
import legacy_guard as LG  # noqa: E402
def load_entrypoint(name):
    spec = importlib.util.spec_from_file_location(f"rf00_{name}", LOOP / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
RUN = load_entrypoint("run_iteration")
SCORE = load_entrypoint("score")
GATE = load_entrypoint("gate")
HF_RUN = load_entrypoint("hf01_run")
WRITE_METHODS = {
    "Popen", "call", "check_call", "chmod", "copy", "copy2", "copyfile", "dump",
    "hardlink_to", "makedirs", "mkdir", "move", "open", "remove", "removedirs",
    "rename", "replace", "rmdir", "rmtree", "run", "symlink_to", "touch", "unlink",
    "write", "write_bytes", "write_text", "writelines", "writerow", "writerows",
}
def entrypoint_state(source):
    tree = ast.parse(source)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    main = functions.get("main")
    main_nodes = list(ast.walk(main)) if main is not None else []
    executable = any(
        isinstance(node, ast.If) and "__main__" in ast.unparse(node.test)
        for node in ast.walk(tree)
    )
    def writes(node):
        return isinstance(node, ast.Call) and (
            isinstance(node.func, ast.Attribute) and node.func.attr in WRITE_METHODS
            or isinstance(node.func, ast.Name) and node.func.id == "open"
        )
    local_calls = {
        name: {node.func.id for node in ast.walk(body) if isinstance(node, ast.Call)
               and isinstance(node.func, ast.Name) and node.func.id in functions}
        for name, body in functions.items()
    }
    capable = {name for name, body in functions.items() if any(writes(n) for n in ast.walk(body))}
    while True:
        expanded = capable | {name for name, calls in local_calls.items() if calls & capable}
        if expanded == capable:
            break
        capable = expanded
    guards = [
        node for node in main_nodes if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "LG"
        and node.func.attr == "require_authorized"
    ]
    risky = [node for node in main_nodes if writes(node) or isinstance(node, ast.Call)
             and isinstance(node.func, ast.Name) and node.func.id in capable]
    guarded = bool(guards) and (
        not risky or min(node.lineno for node in guards) < min(node.lineno for node in risky)
    )
    return executable, bool(capable), guarded


def digest(paths):
    return {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
class LegacyGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.outside = self.root / "accepted-fixtures"
        self.product = self.outside / "product/current.md"
        self.config = self.outside / "config.yaml"
        self.score = self.outside / "scores/iter-001.json"
        self.results = self.outside / "results.tsv"
        for path, body in (
            (self.product, "accepted product\n"),
            (self.config, "accepted config\n"),
            (self.score, '{"accepted": true}\n'),
            (self.results, "accepted ledger\n"),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        self.protected = (self.product, self.config, self.score, self.results)

    def tearDown(self): self.tmp.cleanup()

    def candidate_fixture(self):
        candidate = self.root / "candidate"
        book = candidate / "product"
        book.mkdir(parents=True)
        paths = {
            "scores_dir": candidate / "scores",
            "results_tsv": candidate / "results.tsv",
            "tasks_dir": candidate / "iterations",
        }
        config = candidate / "config.yaml"
        config.write_text(
            "epsilon: 0.03\n" + "".join(f"{key}: {value}\n" for key, value in paths.items()),
            encoding="utf-8",
        )
        return candidate, book, config

    def ledger(self, rf20="READY", rf23="READY"):
        path = self.root / "tasks.md"
        path.write_text(
            "# fixture\n\n"
            f"### RF-20 — calibration\n\n- Status: `{rf20}`\n\n"
            f"### RF-23 — prose\n\n- Status: `{rf23}`\n",
            encoding="utf-8",
        )
        return path

    def test_inventory_is_complete_and_guards_future_entrypoints(self):
        """Infrastructure: static inventory fails for an unguarded future writer."""
        inventory = {}
        for path in LOOP.glob("*.py"):
            executable, _, guarded = entrypoint_state(path.read_text(encoding="utf-8"))
            if executable and path.name not in ("loopcfg.py", "hf01_preflight.py"):
                inventory[path.name] = guarded
        self.assertEqual(
            {"developmental_review.py": True, "gate.py": True,
             "grounded_review.py": True, "hf01_run.py": True,
             "run_iteration.py": True, "score.py": True},
            inventory,
        )
        future = (
            "from pathlib import Path\n"
            "def write_helper(): Path('product').write_text('x')\n"
            "def main():\n"
            " write_helper()\n"
            " LG.require_authorized(None, entrypoint='future')\n"
            "if __name__ == '__main__': main()\n"
        )
        self.assertEqual((True, True, False), entrypoint_state(future))
        snapshot = self.root / "snapshot"
        (snapshot / "loop/experiments").mkdir(parents=True)
        resume = HF_RUN._resume(snapshot)
        for token in ("--redesign-authorized", "--rf-stage", "RF-23", str(snapshot / "loop/experiments")): self.assertIn(token, resume)
        wrong = self.root / "wrong"; wrong.mkdir()
        argv = ["hf01_run.py", "--snapshot-root", str(snapshot), "--redesign-authorized",
                "--rf-stage", "RF-23", "--candidate-root", str(wrong)]
        with mock.patch.object(LG, "LEDGER", self.ledger()), \
                mock.patch.object(sys, "argv", argv), mock.patch.object(HF_RUN, "run") as dispatch:
            with self.assertRaisesRegex(SystemExit, "candidate-root must equal"): HF_RUN.main()
        dispatch.assert_not_called()
    def test_program_redirects_legacy_recovery_to_the_ledger(self):
        """OpenSpec scenario: The legacy loop is invoked before redesign readiness."""
        program = (ROOT / "PROGRAM.md").read_text(encoding="utf-8")
        for required in (
            "PAUSED BY RF-00",
            "recover only from",
            "openspec/changes/redesign-book-factory/tasks.md",
            "scripts/loop/legacy_guard.py",
        ):
            self.assertIn(required, program)

    def test_pre_ready_entrypoints_stop_before_resolution_and_writes(self):
        """OpenSpec scenario: The legacy loop is invoked before redesign readiness."""
        before = digest(self.protected)
        cases = (
            (RUN, ["run_iteration.py", "--book", str(self.product.parent),
                   "--iter", "1", "--config", str(self.config)], RUN.judges, "endpoint"),
            (SCORE, ["score.py", "--book", str(self.product.parent),
                     "--iter", "1", "--config", str(self.config)],
             SCORE.score_core, "evaluate"),
            (GATE, ["gate.py", "--iter", "1", "--config", str(self.config)],
             GATE, "append_row"),
        )
        for module, argv, boundary_owner, boundary_name in cases:
            with self.subTest(entrypoint=argv[0]), mock.patch.object(sys, "argv", argv), \
                    mock.patch.object(module.loopcfg, "load", side_effect=AssertionError), \
                    mock.patch.object(boundary_owner, boundary_name, side_effect=AssertionError):
                with self.assertRaises(SystemExit) as stopped:
                    module.main()
                self.assertIn("explicit redesign authorization", str(stopped.exception))
        self.assertEqual(before, digest(self.protected))

    def test_authorized_rf23_isolated_dry_run_reaches_boundary(self):
        """OpenSpec scenario: An authorized isolated redesign path is exercised."""
        candidate, book, config = self.candidate_fixture()
        score = candidate / "scores/iter-001.json"
        score.parent.mkdir()
        score.write_text(f'{{"book": "{book}"}}', encoding="utf-8")
        common = ["--config", str(config), "--redesign-authorized", "--rf-stage", "RF-23",
                  "--candidate-root", str(candidate), "--rf-dry-run"]
        cases = (
            (RUN, ["run_iteration.py", "--book", str(book), "--iter", "1"], RUN.judges, "endpoint"),
            (SCORE, ["score.py", "--book", str(book), "--iter", "1"],
             SCORE.score_core, "evaluate"),
            (GATE, ["gate.py", "--iter", "1"], GATE, "append_row"),
        )
        before = digest(self.protected)
        candidate_before = {p.relative_to(candidate): p.read_bytes()
                            for p in candidate.rglob("*") if p.is_file()}
        with mock.patch.object(LG, "LEDGER", self.ledger()):
            for module, prefix, owner, boundary in cases:
                stdout = io.StringIO()
                with self.subTest(entrypoint=prefix[0]), mock.patch.object(sys, "argv", prefix + common), \
                        mock.patch.object(owner, boundary, side_effect=AssertionError), \
                        contextlib.redirect_stdout(stdout):
                    module.main()
                self.assertIn("authorized isolated dispatch boundary", stdout.getvalue())
        self.assertEqual(before, digest(self.protected))
        self.assertEqual(candidate_before, {p.relative_to(candidate): p.read_bytes()
                                           for p in candidate.rglob("*") if p.is_file()})
        LG.require_targets(candidate, candidate / "allowed-output")
        with self.assertRaises(SystemExit):
            LG.require_targets(candidate, self.product)

    def test_ready_stage_still_rejects_accepted_product_and_config(self):
        """OpenSpec scenario: An authorized isolated redesign path is exercised."""
        candidate, _, config = self.candidate_fixture()
        linked_book = candidate / "linked-product"
        linked_book.mkdir()
        (linked_book / "chapters").symlink_to(
            ROOT / "production-books/quit-sugar/chapters", target_is_directory=True,
        )
        base = [
            "--iter", "1", "--redesign-authorized", "--rf-stage", "RF-23",
            "--candidate-root", str(candidate), "--rf-dry-run",
        ]
        with mock.patch.object(LG, "LEDGER", self.ledger()):
            for target_config, target_book in (
                (ROOT / "loop/config.yaml", candidate / "product"),
                (config, ROOT / "production-books/quit-sugar"),
                (config, linked_book),
            ):
                argv = ["run_iteration.py", "--book", str(target_book),
                        "--config", str(target_config), *base]
                with self.subTest(target=target_book), mock.patch.object(sys, "argv", argv):
                    with self.assertRaises(SystemExit) as stopped:
                        RUN.main()
                    self.assertIn("target ", str(stopped.exception))

    def test_stage_and_rf23_readiness_are_both_required(self):
        """OpenSpec scenario: An authorized isolated redesign path is exercised."""
        candidate, book, config = self.candidate_fixture()
        common = ["--config", str(config), "--redesign-authorized", "--rf-stage", "RF-20",
                  "--candidate-root", str(candidate), "--rf-dry-run"]
        with mock.patch.object(LG, "LEDGER", self.ledger(rf20="TODO")), \
                mock.patch.object(sys, "argv", ["score.py", "--book", str(book),
                                                *common]):
            with self.assertRaises(SystemExit) as stopped:
                SCORE.main()
            self.assertIn("RF-20 is TODO", str(stopped.exception))
        cases = ((RUN, ["run_iteration.py", "--book", str(book), "--iter", "1", "--no-write"]),
                 (SCORE, ["score.py", "--book", str(book), "--iter", "1"]),
                 (GATE, ["gate.py", "--iter", "1"]))
        with mock.patch.object(LG, "LEDGER", self.ledger(rf23="TODO")):
            for module, prefix in cases:
                with self.subTest(entrypoint=prefix[0]), mock.patch.object(sys, "argv", prefix + common), \
                        mock.patch.object(module.loopcfg, "load", side_effect=AssertionError):
                    with self.assertRaises(SystemExit) as stopped:
                        module.main()
                    self.assertIn("legacy execution requires RF-23 READY", str(stopped.exception))


if __name__ == "__main__":
    unittest.main()
