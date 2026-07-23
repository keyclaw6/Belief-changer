"""Focused pre-RF21 authority and durable H-F01 execution regressions."""
import json, os, shlex, shutil, sys, tempfile, unittest, urllib.error
from copy import deepcopy
from pathlib import Path
from unittest import mock
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "scripts/loop"), str(ROOT / "scripts/eval/tests")]
import candidate_pair as PAIR  # noqa: E402
import commission_set as SET  # noqa: E402
import first_draft_batch as BATCH  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import hf01_prepare as PREP  # noqa: E402
import hf01_run as RUN  # noqa: E402
import hf01_upstream as UP  # noqa: E402
from commission_packet_fixture import packet  # noqa: E402
from test_commission_contract import authority, commission  # noqa: E402
AUTH = "2026-07-19T10:00:00+00:00"
def assignment(chapter, source):
    auth = deepcopy(authority()); old = next(iter(auth["assigned_evidence"]))
    locator = f"{source}#E-001"; auth["target"] = chapter
    auth["resolved_ids"] = {chapter: auth["required"]["entering belief"]}
    binding = auth["assigned_evidence"].pop(old)
    binding["provenance"] = binding["provenance"].replace(old, locator)
    auth["assigned_evidence"][locator] = binding
    return {"packets": [f"production-books/quit-sugar/research/sources/{source.lower()}-fixture.md"], "authority": auth}
class Hf01Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name).resolve()
        self.root_patch = mock.patch.object(HF, "AUTHORIZED_ROOT", self.root); self.root_patch.start(); self.addCleanup(self.root_patch.stop)
        self.clean = mock.patch.object(HF, "_clean", return_value=True); self.clean.start(); self.addCleanup(self.clean.stop)
        self.commit_patch = mock.patch.object(HF, "_commit", return_value="a" * 40)
        self.commit_patch.start(); self.addCleanup(self.commit_patch.stop)
        self.sync_patch = mock.patch.object(PAIR.PS, "_sync", return_value=None)
        self.sync_patch.start(); self.addCleanup(self.sync_patch.stop)
        self.replace_patch = mock.patch.object(PAIR.PS, "_replace_file", side_effect=self._replace)
        self.replace_patch.start(); self.addCleanup(self.replace_patch.stop)
        self.ledger = self.root / "tasks.md"; self._ledger("BLOCKED", "BLOCKED")
        self.ledger_patch = mock.patch.object(HF, "LEDGER", self.ledger)
        self.ledger_patch.start(); self.addCleanup(self.ledger_patch.stop)
        for relative in ("prompts/style-guide.md", "prompts/chapter-writer.md", "prompts/grounded-reviewer.md",
                         "prompts/developmental-reviewer.md", "prompts/master-plan-skill-v2.md", "prompts/master-plan-reviewer-v2.md"):
            target = self.root / relative; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
        files = {
            "prompts/chapter-commissioner.md": "commissioner contract\n",
            "prompts/commission-set-auditor.md": "grounding continuity leakage\n",
            "production-books/quit-sugar/00-brief.md": "Safety perimeter is fixed.\n",
            "production-books/quit-sugar/research/lived-experience.md": "shared lived\n",
            "production-books/quit-sugar/research/scientific-evidence.md": "shared science\n",
            **{f"production-books/quit-sugar/research/sources/s-{100+n}-fixture.md": packet(
                f"S-{100+n}", "E-001", f"ONLY-{n}") for n in (1, 2, 3)},
            "production-books/quit-sugar/framing.md": "# Framing\n" + "".join(
                f"### CH-{n:02d} — State {n}\n- **Entering belief:** RS-{n-1:02d} | state\n"
                for n in (1, 2, 3)),
            "production-books/quit-sugar/master-plan.md": "# Plan\n\n" + "\n".join(
                f"| EV-L{n:02d} | bounded finding {n} | S-{100+n}#E-001. | "
                f"bounded use {n} | forbidden broadening {n} |" for n in (1, 2, 3)) +
                "\n\n" + "\n\n".join(
                f"### C-{n:02d} — Chapter {n}\n- **Belief job:** correct belief {n}.\n"
                f"- **Entering belief:** RS-{n-1:02d} | received state {n}.\n"
                f"- **Leaving belief:** RS-{n:02d} | handed state {n}.\n"
                f"- **Evidence:** EV-L{n:02d}.\n- **Guardrails:** safety limit {n}; no diagnosis.\n"
                f"- **Continuity:** receives received state {n}; hands C-{n+1:02d} handed state {n}."
                for n in (1, 2, 3)),
            "production-books/quit-sugar/master-plan-review.md": "fit to write from\n",
            **{f"production-books/quit-sugar/chapters/chapter-{n:02d}.md": f"baseline {n}\n" for n in (1, 2, 3)},
            "calibration/reference/gsbs/reference-metrics.json": '{"chapters": []}\n',
            **{f"calibration/reference/gsbs/chapter-{n}.txt": f"GSBS offset {n}\n" for n in range(1, 6)},
            "loop/results.tsv": "iter\treward\tverdict\n", "loop/causal-bundle-results.jsonl": ""}
        for relative, text in files.items():
            path = self.root / relative; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        shutil.copy2(ROOT / "loop/config.yaml", self.root / "loop/config.yaml")
        self.config_patch = mock.patch.object(HF, "CONFIG", self.root / "loop/config.yaml")
        self.config_patch.start(); self.addCleanup(self.config_patch.stop)
        for relative in ("calibration/judges/carr-likeness-rubric.md", *HF.RUBRICS):
            target = self.root / relative; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
        PAIR.initialize(self.root, HF.BOOK); self.arms = HF.arm_paths(self.root)
        for paths in self.arms.values(): paths["experiment"].mkdir(parents=True); PAIR.snapshot(paths["experiment"], self.root, HF.BOOK, "1-3", iteration=1)
        self.assignments = {f"C-{n:02d}": assignment(f"C-{n:02d}", f"S-{100+n}") for n in (1, 2, 3)}
        self.location_proof = {"source": HF.LOCATION_URL, "country_code": "US"}
        self.preflight_proof = {"model": HF.MODEL, "canonical_model": HF.CANONICAL_MODEL,
            "provider": "Meta", "calls": 6,
            "cache_read_price_per_token": HF.PRICING["input_cache_read"],
            "reasoning_mandatory": True,
            "reasoning_supported_efforts": list(HF.SUPPORTED_EFFORTS),
            "current_request_location": self.location_proof,
            "current_request_account_visible_model": {"source": HF.USER_MODELS_URL,
                "authenticated": True, "exact_matches": 1, "id": HF.MODEL,
                "canonical_slug": HF.CANONICAL_MODEL}}
    def tearDown(self): self.tmp.cleanup()
    @staticmethod
    def _replace(source, target):
        target = Path(target)
        if target.exists() and not target.is_symlink(): target.chmod(0o644)
        os.replace(source, target)
    def _ledger(self, rf22, rf23, rf21="IN_PROGRESS"):
        self.ledger.write_text("### RF-20 — calibration\n- Status: `BLOCKED`\n"
            f"### RF-21 — generation\n- Status: `{rf21}`\n"
            f"### RF-22 — commissions\n- Status: `{rf22}`\n"
            f"### RF-23 — readiness\n- Status: `{rf23}`\n", encoding="utf-8")
    def manifest(self, **changes):
        return HF.build_manifest(self.root, key_present=True, ledger=self.ledger, authority_timestamp=AUTH, **changes)
    def snapshot(self):
        return {path.relative_to(self.root).as_posix(): PAIR.PS.sha(path.read_bytes()) for path in self.root.rglob("*") if path.is_file()}
    def freeze(self):
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), mock.patch.object(HF, "LEDGER", self.ledger):
            return RUN._authority(self.root, AUTH)
    def prepare_treatment(self):
        book = self.arms["treatment"]["book"]
        for relative, suffix in (("00-brief.md", "Treatment reader journey.\n"),
                ("framing.md", "\nTreatment linked reader state.\n"),
                ("master-plan.md", "\nTreatment source-grounded handoff.\n"),
                ("master-plan-review.md", "Treatment plan review.\n")):
            path = book / relative; path.write_text(path.read_text() + suffix)
        UP._declare_review(self.arms["treatment"]["experiment"])
        (book / "framing-review.md").write_text("Treatment framing review.\n")
        with mock.patch.object(SET.SC, "require_subject_contract"):
            SET.generate(self.arms["treatment"]["experiment"], self.assignments, lambda request: commission(self.assignments[request["target"]]["authority"]), lambda _request: SET.AUDIT_PASS)
    def assignment_rows(self):
        rows = []
        for chapter, record in self.assignments.items():
            authority = record["authority"]
            rows.append({"chapter": chapter, "required": authority["required"],
                "resolved_ids": [{"id": key, "value": value}
                                 for key, value in authority["resolved_ids"].items()],
                "assigned_evidence": [{"locator": key, **value}
                    for key, value in authority["assigned_evidence"].items()],
                "frozen_tokens": list(authority["frozen_tokens"]),
                "forbidden": list(authority["forbidden"])})
        return rows
    def native(self, content, actor, _schema, model, reasoning):
        task = json.loads(content); call_id = task["id"]
        book = self.arms["control"]["book"]
        if call_id == "rf21-plan":
            value = {"brief": (book / "00-brief.md").read_text() + "Treatment reader journey.\n",
                "framing": (book / "framing.md").read_text() + "\nTreatment linked reader state.\n",
                "master_plan": (book / "master-plan.md").read_text() + "\nTreatment source-grounded handoff.\n",
                "assignments": self.assignment_rows()}
        elif call_id == "rf21-plan-review":
            value = {"framing_review": "Treatment framing review.",
                     "master_plan_review": "Treatment plan review."}
        elif call_id.startswith("rf22-commission"):
            target = f"C-{int(call_id[-2:]):02d}"
            value = {"commission": commission(self.assignments[target]["authority"])}
        else: value = {"verdict": SET.AUDIT_PASS}
        transport = {"thread_id": f"thread-{call_id}", "model": model,
            "reasoning_effort": reasoning, "command": UP.NATIVE.command(
                "<isolated-tmp>", "<isolated-tmp>/judge-output-schema.json", model, reasoning)}
        return json.dumps(value), transport, None
    def writer_response(self, text, include_attempts=True):
        metadata = {"requested": HF.MODEL, "strategy": "direct", "attempt": 1,
            "endpoints": {"total": 1, "available": [{"provider": "Meta",
                "model": HF.CANONICAL_MODEL, "selected": True, "future_field": "ignored"}]},
            "future_metadata": ["ignored"]}
        if include_attempts:
            metadata["attempts"] = [{"provider": "Meta", "model": HF.CANONICAL_MODEL,
                "status": 200, "future_field": {"ignored": True}}]
        return {"model": HF.CANONICAL_MODEL,
                "openrouter_metadata": metadata,
                "choices": [{"message": {"content": text}}]}
    def http_values(self):
        return {
            HF.LOCATION_URL: "fl=fixture\nip=192.0.2.10\nloc=US\ntls=TLSv1.3\n",
            HF.MODEL_URL: {"data": {"id": HF.MODEL, "canonical_slug": HF.CANONICAL_MODEL,
                "top_provider": {"context_length": 1048576, "max_completion_tokens": None},
                "pricing": {"prompt": "0.00000125", "completion": "0.00000425",
                    "web_search": "0.0025", "input_cache_read": "0.00000015"},
                "supported_parameters": ["reasoning", "temperature", "max_tokens"],
                "reasoning": {"mandatory": True,
                    "supported_efforts": list(HF.SUPPORTED_EFFORTS),
                    "default_effort": "medium"}}},
            HF.USER_MODELS_URL: {"data": [{"id": HF.MODEL,
                "canonical_slug": HF.CANONICAL_MODEL}]},
            HF.ENDPOINTS_URL: {"data": {"endpoints": [{"provider_name": "Meta",
                "model_id": HF.MODEL, "status": 0, "tag": "meta",
                "name": f"Meta | {HF.CANONICAL_MODEL}"}]}},
            HF.KEY_URL: {"data": {"limit_remaining": 100,
                "expires_at": "2027-12-31T23:59:59Z"}},
            HF.CREDITS_URL: {"data": {"total_credits": 100, "total_usage": 1}}}
    @staticmethod
    def open_values(values):
        def open_url(request, timeout):
            response = mock.MagicMock(); response.status = 200
            response.__enter__.return_value = response
            value = values[request.full_url]
            response.read.return_value = (value if isinstance(value, str)
                                          else json.dumps(value)).encode()
            return response
        return open_url
    def write_upstream(self, authority, authority_sha):
        with mock.patch.object(SET.SC, "require_subject_contract"):
            UP.dispatch_stage(self.root, authority, authority_sha, "RF-21", complete=self.native)
            self._ledger("IN_PROGRESS", "BLOCKED", rf21="DONE")
            UP.dispatch_stage(self.root, authority, authority_sha, "RF-22", complete=self.native)
        return self.root / UP.FOLDER / UP.PATH
    def authorize_run(self):
        _folder, authority, authority_sha = self.freeze()
        path = self.write_upstream(authority, authority_sha)
        self._ledger("DONE", "READY", rf21="DONE")
        return authority, authority_sha, path
    def test_rf21_pauses_before_rf22_and_rf22_requires_ledger_transition(self):
        """Scenario: RF-21 and RF-22 dispatch is durable and authority-bound."""
        _folder, authority, authority_sha = self.freeze(); calls = []
        original = UP.dispatch_stage
        def dispatch(root, auth, digest, stage):
            before = set((self.root / UP.FOLDER / "upstream/calls").glob("*.json")) \
                if (self.root / UP.FOLDER / "upstream/calls").exists() else set()
            result = original(root, auth, digest, stage, complete=self.native)
            after = set((self.root / UP.FOLDER / "upstream/calls").glob("*.json"))
            calls.extend(path.stem for path in sorted(after - before))
            return result
        with mock.patch.object(UP, "dispatch_stage", side_effect=dispatch), \
                mock.patch.object(SET.SC, "require_subject_contract"):
            result = RUN.run(self.root, native=True, upstream_stage="RF-21", authority_timestamp=AUTH)
            self.assertEqual(("RF21_COMPLETE_PAUSED", 2, False),
                (result["state"], len(calls), (self.root / UP.FOLDER / UP.PATH).exists()))
            with self.assertRaisesRegex(HF.PreflightError, "RF-22 is BLOCKED"):
                RUN.run(self.root, native=True, upstream_stage="RF-22", authority_timestamp=AUTH)
            self.assertEqual(2, len(calls))
            self._ledger("IN_PROGRESS", "BLOCKED", rf21="DONE")
            result = RUN.run(self.root, native=True, upstream_stage="RF-22", authority_timestamp=AUTH)
        self.assertEqual(("RF22_COMPLETE_PAUSED", 6), (result["state"], len(calls)))

    def test_prepare_requires_explicit_store_then_reuses_matched_snapshots(self):
        """Scenario: Candidate preparation performs no accepted-store setup."""
        for directory in (self.root / "loop/accepted", self.root / "loop/experiments"):
            if directory.exists():
                for path in directory.rglob("*"):
                    if path.is_file(): path.chmod(0o644)
                shutil.rmtree(directory)
        before = PREP._source_hashes(self.root)
        with mock.patch.object(PAIR, "initialize", side_effect=AssertionError("prepare initialized store")) as initialize, \
                mock.patch.object(RUN, "_post") as model, \
                mock.patch.object(UP.NATIVE, "complete") as native:
            with self.assertRaisesRegex(PREP.PrepareError, "pointer missing or malformed"):
                PREP.prepare(self.root, 7)
        initialize.assert_not_called(); model.assert_not_called(); native.assert_not_called()
        self.assertFalse((self.root / "loop/accepted").exists())
        self.assertFalse((self.root / "loop/experiments").exists())
        self.assertEqual(before, PREP._source_hashes(self.root))
        PAIR.initialize(self.root, HF.BOOK, "loop/config.yaml")
        with mock.patch.object(RUN, "_post") as model, mock.patch.object(UP.NATIVE, "complete") as native:
            first = PREP.prepare(self.root, 7); second = PREP.prepare(self.root, 7)
        model.assert_not_called(); native.assert_not_called()
        self.assertEqual((first, before), (second, PREP._source_hashes(self.root)))
        manifests = [PAIR.inspect(HF.arm_paths(self.root)[arm]["experiment"])
                     for arm in ("control", "treatment")]
        self.assertEqual(1, len({(row["accepted_generation"], row["accepted_pair_hash"],
                                  row["accepted_evaluation_hash"]) for row in manifests}))

    def test_prepare_rejects_unsafe_arm_before_creating_sibling(self):
        """Scenario: An operation root contains an unsafe path."""
        experiments = self.root / "loop/experiments"
        for path in experiments.rglob("*"):
            if path.is_file(): path.chmod(0o644)
        shutil.rmtree(experiments)
        experiments.mkdir()
        treatment = HF.arm_paths(self.root)["treatment"]["experiment"]
        treatment.write_text("not a directory\n", encoding="utf-8")
        control = HF.arm_paths(self.root)["control"]["experiment"]
        with self.assertRaisesRegex(PREP.PrepareError, "not a directory"):
            PREP.prepare(self.root, 7)
        self.assertFalse(os.path.lexists(control))
        self.assertEqual("not a directory\n", treatment.read_text(encoding="utf-8"))

    def test_prepare_rejects_aliased_parent_and_arm_before_snapshot(self):
        """Scenario: An operation root contains an unsafe path."""
        experiments = self.root / "loop/experiments"
        for case in ("parent", "arm"):
            with self.subTest(case=case):
                if os.path.lexists(experiments):
                    if experiments.is_symlink():
                        experiments.unlink()
                    else:
                        for path in experiments.rglob("*"):
                            if path.is_file(): path.chmod(0o644)
                        shutil.rmtree(experiments)
                outside = self.root / f"outside-{case}"
                outside.mkdir()
                try:
                    if case == "parent":
                        experiments.symlink_to(outside, target_is_directory=True)
                    else:
                        experiments.mkdir()
                        HF.arm_paths(self.root)["treatment"]["experiment"].symlink_to(
                            outside, target_is_directory=True)
                except OSError as exc:
                    if os.name == "nt" and getattr(exc, "winerror", None) in (50, 1314):
                        self.skipTest(f"directory symlinks unavailable: {exc}")
                    raise
                with self.assertRaisesRegex(PREP.PrepareError, "aliased"):
                    PREP.prepare(self.root, 7)
                self.assertEqual([], list(outside.iterdir()))
                control = HF.arm_paths(self.root)["control"]["experiment"]
                self.assertFalse(os.path.lexists(control))

    def test_authenticated_preflight_fails_closed_without_inference(self):
        """Scenario: Muse account and capability preflight fails closed."""
        values = self.http_values()
        keys = {"OPENROUTER_API_KEY": "test-key", "OPENROUTER_MANAGEMENT_KEY": "management-key"}
        with mock.patch.dict(os.environ, keys):
            proof = HF.authenticated_preflight(open_url=self.open_values(values),
                now=HF.dt.datetime(2026, 7, 22, tzinfo=HF.dt.timezone.utc))
        self.assertEqual((HF.CANONICAL_MODEL, "Meta", "0.00000015"),
            (proof["canonical_model"], proof["provider"],
             proof["cache_read_price_per_token"]))
        self.assertNotIn("region", proof)
        self.assertEqual(self.location_proof, proof["current_request_location"])
        self.assertEqual({"source", "country_code"},
                         set(proof["current_request_location"]))
        self.assertNotIn("192.0.2.10", json.dumps(proof))
        self.assertNotIn("ip=", json.dumps(proof))
        self.assertEqual({"source": HF.USER_MODELS_URL, "authenticated": True,
            "exact_matches": 1, "id": HF.MODEL,
            "canonical_slug": HF.CANONICAL_MODEL},
            proof["current_request_account_visible_model"])
        cases = {}
        for name in ("metadata", "reasoning", "pricing", "visibility-missing",
                     "visibility-duplicate", "endpoint", "allowance", "credit"):
            cases[name] = deepcopy(values)
        cases["metadata"][HF.MODEL_URL] = deepcopy(values[HF.MODEL_URL]); cases["metadata"][HF.MODEL_URL]["data"]["id"] = "wrong"
        cases["reasoning"][HF.MODEL_URL]["data"]["reasoning"]["mandatory"] = False
        cases["pricing"][HF.MODEL_URL]["data"]["pricing"]["input_cache_read"] = "0"
        cases["visibility-missing"][HF.USER_MODELS_URL]["data"] = []
        cases["visibility-duplicate"][HF.USER_MODELS_URL]["data"].append(
            deepcopy(values[HF.USER_MODELS_URL]["data"][0]))
        cases["endpoint"][HF.ENDPOINTS_URL]["data"]["endpoints"][0]["provider_name"] = "Other"
        cases["allowance"][HF.KEY_URL] = deepcopy(values[HF.KEY_URL]); cases["allowance"][HF.KEY_URL]["data"]["limit_remaining"] = 0
        cases["credit"][HF.CREDITS_URL] = deepcopy(values[HF.CREDITS_URL]); cases["credit"][HF.CREDITS_URL]["data"]["total_credits"] = 1
        with mock.patch.dict(os.environ, keys):
            for name, invalid in cases.items():
                with self.subTest(name=name), self.assertRaises(HF.PreflightError):
                    HF.authenticated_preflight(open_url=self.open_values(invalid))
            location_cases = {
                "account-visible-dk": ("ip=192.0.2.20\nloc=DK\n", "not eligible: DK"),
                "missing": ("ip=192.0.2.20\ntls=TLSv1.3\n", "missing loc"),
                "duplicate": ("loc=US\nloc=US\n", "duplicate loc"),
                "malformed": ("loc=USA\n", "malformed loc"),
            }
            for name, (trace, message) in location_cases.items():
                invalid, opened = deepcopy(values), []
                invalid[HF.LOCATION_URL] = trace
                delegate = self.open_values(invalid)
                def tracked(request, timeout):
                    opened.append(request.full_url)
                    return delegate(request, timeout)
                with self.subTest(location=name), self.assertRaisesRegex(
                        HF.PreflightError, message):
                    HF.authenticated_preflight(open_url=tracked)
                self.assertEqual([HF.LOCATION_URL], opened)
            def unauthorized(request, timeout):
                if request.full_url == HF.LOCATION_URL:
                    return self.open_values(values)(request, timeout)
                raise urllib.error.HTTPError(HF.KEY_URL, 401, "unauthorized", {}, None)
            with self.assertRaisesRegex(HF.PreflightError, "HTTP 401"):
                HF.authenticated_preflight(open_url=unauthorized)
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=True), \
                self.assertRaisesRegex(HF.PreflightError, "OPENROUTER_MANAGEMENT_KEY"):
            HF.authenticated_preflight(open_url=self.open_values(values))
    def test_ready_unstarted_rejects_snapshot_authority_and_dispatch(self):
        """Scenario: Offline readiness does not start H-F01."""
        self._ledger("BLOCKED", "BLOCKED", rf21="READY")
        before = self.snapshot()
        manifest = self.manifest()
        self.assertFalse(manifest["ready_to_freeze_authority"])
        self.assertIn("RF21_NOT_STARTED",
                      {row["code"] for row in manifest["blockers"]})
        with self.assertRaisesRegex(HF.PreflightError,
                                    "RF-21 is READY, not IN_PROGRESS"):
            HF.require_stage({"authority": {"ledger_path": str(self.ledger)}},
                             "RF-21")
        cases = (
            (PREP, ["hf01_prepare.py", "--snapshot-root", str(self.root),
                    "--iteration", "2", "--redesign-authorized", "--rf-stage",
                    "RF-21", "--candidate-root", str(self.root)], PREP, "prepare"),
            (RUN, ["hf01_run.py", "--snapshot-root", str(self.root),
                   "--redesign-authorized", "--rf-stage", "RF-21",
                   "--candidate-root", str(self.root / "loop/experiments"),
                   "--authority-timestamp", AUTH, "--native"], RUN, "run"),
        )
        with mock.patch.object(PREP.LG, "LEDGER", self.ledger):
            for module, argv, owner, boundary in cases:
                with self.subTest(entrypoint=argv[0]), \
                        mock.patch.object(sys, "argv", argv), \
                        mock.patch.object(owner, boundary,
                                          side_effect=AssertionError):
                    with self.assertRaisesRegex(
                            SystemExit, "RF-21 is READY, not IN_PROGRESS"):
                        module.main()
        self.assertEqual(before, self.snapshot())

        self._ledger("BLOCKED", "BLOCKED", rf21="IN_PROGRESS")
        started_before = self.snapshot()
        with mock.patch.object(PREP.LG, "LEDGER", self.ledger):
            for module, argv, _owner, _boundary in cases:
                with self.subTest(started_entrypoint=argv[0]), \
                        mock.patch.object(sys, "argv", [*argv, "--rf-dry-run"]):
                    module.main()
        self.assertEqual(started_before, self.snapshot())

    def test_direct_ready_boundaries_reject_before_snapshot_or_native_call(self):
        """Scenario: Offline readiness does not start H-F01."""
        experiments = self.root / "loop/experiments"
        for path in experiments.rglob("*"):
            if path.is_file():
                path.chmod(0o644)
        shutil.rmtree(experiments)
        self._ledger("BLOCKED", "BLOCKED", rf21="READY")
        before = self.snapshot()
        with mock.patch.object(PREP.CP, "snapshot") as snapshot, \
                self.assertRaisesRegex(HF.PreflightError,
                                       "RF-21 is READY, not IN_PROGRESS"):
            PREP.prepare(self.root, 2)
        snapshot.assert_not_called()
        self.assertEqual(before, self.snapshot())
        self.assertFalse(experiments.exists())

        self._ledger("BLOCKED", "BLOCKED", rf21="IN_PROGRESS")
        PREP.prepare(self.root, 2)
        _folder, authority_value, authority_sha = RUN._authority(self.root, AUTH)
        self._ledger("BLOCKED", "BLOCKED", rf21="READY")
        native = mock.Mock()
        before = self.snapshot()
        with self.assertRaisesRegex(HF.PreflightError,
                                    "RF-21 is READY, not IN_PROGRESS"):
            UP.dispatch_stage(self.root, authority_value, authority_sha,
                              "RF-21", complete=native)
        native.assert_not_called()
        self.assertEqual(before, self.snapshot())

    def test_preflight_is_pure_and_freezes_offset_gsbs_before_rf21(self):
        before, secret = self.snapshot(), "do-not-serialize"
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": secret}): manifest = self.manifest()
        self.assertEqual(before, self.snapshot()); self.assertTrue(manifest["ready_to_freeze_authority"])
        self.assertFalse(manifest["ready_to_send"])
        self.assertNotIn(secret, json.dumps(manifest)); self.assertEqual(HF.ROUTE_LAW, manifest["route"])
        self.assertEqual([3, 4, 5], [row["reference_position"] for row in manifest["identity"]["gsbs_matches"]])
        self.assertEqual(40, manifest["call_budget"]["planned_total"])
        self.assertEqual(0, manifest["call_budget"]["counted_before_authority"])
        self.assertEqual(["RF-25", "RF-30", "RF-31"], manifest["validation_ladder"]["order"])
        self.assertEqual(("evaluation-only", False), (manifest["subject_reference_isolation"]["reference_mode"], manifest["subject_reference_isolation"]["reference_in_rf21_rf22_inputs"]))
        self.assertEqual(list(UP.IDS), [row["id"] for row in manifest["rf21_rf22_native_calls"]])
        self.assertEqual(("gpt-5.6-luna", "gpt-5.6-sol"), tuple(row["model"] for row in manifest["rf21_rf22_native_calls"][:2]))
        self.assertNotIn("null", json.dumps(manifest["rf21_rf22_native_calls"]))
        self.assertTrue(all(row["reference_blind"] and "read-only" in row["command"]
                            for row in manifest["rf21_rf22_native_calls"]))
        self.assertNotIn("calibration/reference", json.dumps(
            manifest["rf21_rf22_native_calls"][0]["input_contract"]))
        self.assertEqual({"RF22_NOT_READY", "RF23_NOT_READY"},
                         {row["code"] for row in manifest["downstream_blockers"]})
        command = shlex.split(manifest["next_command"])
        self.assertEqual(("{python}", "scripts/loop/hf01_run.py"), tuple(command[:2]))
        self.assertEqual(sys.executable, shlex.split(HF.resume_command(manifest))[0])
        self.assertEqual((AUTH, "RF-21"), (command[command.index("--authority-timestamp") + 1], command[command.index("--rf-stage") + 1]))
        with self.assertRaisesRegex(HF.PreflightError, "persistent root must be exactly"):
            HF.build_manifest(self.root / "alternative", ledger=self.ledger,
                              authority_timestamp=AUTH)
    def test_authority_precedes_treatment_and_rejects_drift_outside_allowlist(self):
        brief = self.arms["treatment"]["book"] / "00-brief.md"; original = brief.read_text()
        brief.write_text(original + "premature treatment\n")
        self.assertIn("RF21_ALREADY_STARTED_BEFORE_AUTHORITY",
                      {row["code"] for row in self.manifest()["blockers"]})
        brief.write_text(original); _folder, authority, _sha = self.freeze(); self.prepare_treatment()
        self.assertEqual(set(HF.TREATMENT_PATHS), set(HF.treatment_artifacts(self.root)))
        HF.validate_execution_authority(self.root, authority, key_present=True)
        source = self.arms["treatment"]["book"] / "research/lived-experience.md"
        source.write_text(source.read_text() + "escaped change\n")
        with self.assertRaisesRegex(HF.PreflightError, "allowlist"):
            HF.validate_execution_authority(self.root, authority, key_present=True)
    def test_missing_writer_key_does_not_block_pre_rf21_authority(self):
        manifest = HF.build_manifest(self.root, key_present=False, ledger=self.ledger, authority_timestamp=AUTH)
        self.assertTrue(manifest["ready_to_freeze_authority"])
        self.assertFalse(manifest["ready_to_send"])
        self.assertNotIn("OPENROUTER_API_KEY_MISSING",
                         {row["code"] for row in manifest["blockers"]})
        self.assertIn("OPENROUTER_API_KEY_MISSING",
                      {row["code"] for row in manifest["downstream_blockers"]})
        with mock.patch.object(HF, "_clean", return_value=False): self.assertIn("GIT_WORKTREE_DIRTY", {row["code"] for row in self.manifest()["blockers"]})
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(HF, "LEDGER", self.ledger):
            _folder, authority, _digest = RUN._authority(self.root, AUTH)
        HF.validate_execution_authority(self.root, authority, key_present=False)
    def test_missing_and_tampered_upstream_receipts_fail_at_exact_boundary(self):
        _folder, authority, authority_sha = self.freeze()
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                self.assertRaises(RUN.STAGE.StagePending) as stopped:
            RUN.run(self.root, credit_check=lambda: self.preflight_proof, authority_timestamp=AUTH)
        self.assertEqual("rf-21-authority-bound-native-tasks", stopped.exception.boundary)
        self.assertEqual("RF-21", shlex.split(stopped.exception.commands[0])[shlex.split(stopped.exception.commands[0]).index("--rf-stage") + 1])
        path = self.write_upstream(authority, authority_sha)
        with mock.patch.object(SET.SC, "require_subject_contract"):
            self.assertEqual(64, len(UP.verify(self.root, authority, authority_sha)))
        task_path = self.root / UP.FOLDER / "upstream/tasks/rf21-plan.json"
        call_path = self.root / UP.FOLDER / "upstream/calls/rf21-plan.json"
        task = json.loads(task_path.read_text()); task["instruction"] = "validly rehashed substitution"
        task["task_sha256"] = PAIR.PS.state_hash({key: item for key, item in task.items()
                                                  if key != "task_sha256"})
        task_path.chmod(0o644); task_path.write_bytes(PAIR.PS.json_bytes(task))
        call = json.loads(call_path.read_text()); call["task_sha256"] = task["task_sha256"]
        call["input_sha256"] = PAIR.PS.sha(PAIR.PS.json_bytes(task))
        call_path.chmod(0o644); call_path.write_bytes(PAIR.PS.json_bytes(call))
        value = json.loads(path.read_text()); value["calls"][0].update(
            task_sha256=call["task_sha256"], input_sha256=call["input_sha256"])
        value["receipt_hash"] = PAIR.PS.state_hash({key: item for key, item in value.items()
                                                    if key != "receipt_hash"})
        path.chmod(0o644); path.write_bytes(PAIR.PS.json_bytes(value))
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                self.assertRaisesRegex(UP.UpstreamError, "native record binding is stale"):
            UP.verify(self.root, authority, authority_sha)
    def test_run_resumes_one_authority_and_freezes_exactly_six_drafts(self):
        authority, authority_sha, _path = self.authorize_run(); calls = []; credit = mock.Mock(side_effect=AssertionError("credit check on frozen resume"))
        def post(payload):
            calls.append(payload); text = f"# Chapter {len(calls)}\n" + "earned discovery relief " * 280
            return json.dumps(self.writer_response(text, include_attempts=len(calls) != 1)).encode()
        with mock.patch.dict(os.environ, {}, clear=True), \
                mock.patch.object(HF, "LEDGER", self.ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.STAGE, "advance",
                    side_effect=lambda root, auth, upstream, **_kw: RUN.verify_frozen(root, auth)), \
                mock.patch.object(RUN, "_post", side_effect=post):
            frozen = RUN.run(self.root, credit_check=lambda: self.preflight_proof,
                authority_timestamp=AUTH, location_check=lambda: self.location_proof)
        with mock.patch.dict(os.environ, {}, clear=True), \
                mock.patch.object(HF, "LEDGER", self.ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.STAGE, "advance",
                    side_effect=lambda root, auth, upstream, **_kw: RUN.verify_frozen(root, auth)), \
                mock.patch.object(RUN, "_post", side_effect=AssertionError("duplicate dispatch")):
            again = RUN.run(self.root, credit_check=credit, authority_timestamp=AUTH,
                            location_check=lambda: self.location_proof)
        credit.assert_not_called(); self.assertEqual((6, "BATCH_FROZEN", frozen), (len(calls), again["state"], again))
        self.assertEqual(authority["frozen_at_utc"], AUTH)
        self.assertEqual({"authority.json", "openrouter-preflight.json", UP.RF21_PATH, UP.PATH, "upstream", "writer-route"}, {
            path.name for path in (self.root / RUN.FOLDER).iterdir()})
        control, treatment = (calls[index]["messages"][0]["content"] for index in (0, 3))
        self.assertIn("frozen_full_style_guide", control); self.assertNotIn("audited_chapter_commission", control)
        self.assertIn("compact_writer_contract", treatment)
        for payload in calls:
            self.assertEqual(RUN.WRITER_SETTINGS,
                {key: payload[key] for key in RUN.WRITER_SETTINGS})
            self.assertNotIn("models", payload); self.assertNotIn("fallbacks", payload)
        proofs = sorted((self.root / RUN.FOLDER / "writer-route").glob("*.json"))
        self.assertEqual(6, len(proofs))
        self.assertNotIn("attempts", json.loads(proofs[0].read_text())
                         ["openrouter_metadata"])
        self.assertEqual(1, len(json.loads(proofs[1].read_text())
                                ["openrouter_metadata"]["attempts"]))
        with self.assertRaisesRegex(RUN.RunError, "seventh writer call"):
            RUN._route_proof(self.root, authority, authority_sha, "control", 1,
                calls[0], self.writer_response("# Chapter 1\n" + "word " * 900),
                "# Chapter 1\n" + "word " * 900)
        proofs[-1].chmod(0o644); proofs[-1].unlink()
        mismatch = self.writer_response("# Chapter 3\n" + "word " * 900)
        mismatch["openrouter_metadata"]["attempts"][0]["status"] = 500
        with self.assertRaisesRegex(RUN.RunError, "fallback, retry, or noncanonical"):
            RUN._route_proof(self.root, authority, authority_sha, "treatment", 3,
                calls[5], mismatch, "# Chapter 3\n" + "word " * 900)
        mismatch["openrouter_metadata"]["attempts"] = None
        with self.assertRaisesRegex(RUN.RunError, "fallback, retry, or noncanonical"):
            RUN._route_proof(self.root, authority, authority_sha, "treatment", 3,
                calls[5], mismatch, "# Chapter 3\n" + "word " * 900)
        for arm, paths in self.arms.items():
            self.assertEqual("BATCH_FROZEN", PAIR.load(paths["experiment"])["state"])
            batch = BATCH.require_frozen_batch(paths["experiment"])["batch"]; self.assertEqual((3, authority_sha), (len(batch["responses"]), batch["authority_sha256"]))
    def test_writer_request_enables_router_metadata_header(self):
        """Scenario: H-F01 writer settings are identical and route-verifiable."""
        response = mock.MagicMock(); response.__enter__.return_value = response
        response.read.return_value = b"{}"
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key",
                                          "OPENROUTER_MANAGEMENT_KEY": "management-key"}), \
                mock.patch.object(RUN.urllib.request, "urlopen", return_value=response) as opened:
            RUN._post(RUN._payload("no prose fixture"))
        request = opened.call_args.args[0]
        self.assertEqual("enabled", request.headers["X-openrouter-metadata"])
    def test_ambiguous_call_and_credit_boundary_fail_closed(self):
        self.authorize_run()
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                mock.patch.object(HF, "LEDGER", self.ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN, "_post", side_effect=RuntimeError("network lost")):
            with self.assertRaisesRegex(RuntimeError, "network lost"):
                RUN.run(self.root, credit_check=lambda: self.preflight_proof,
                    authority_timestamp=AUTH, location_check=lambda: self.location_proof)
            with self.assertRaisesRegex(RUN.RunError, "replay is ambiguous"):
                RUN.run(self.root, credit_check=lambda: self.preflight_proof,
                    authority_timestamp=AUTH, location_check=lambda: self.location_proof)

    def test_frozen_preflight_rechecks_current_location_before_writer(self):
        """Scenario: Muse account and capability preflight fails closed."""
        authority, authority_sha, _path = self.authorize_run()
        RUN._authenticated_preflight(
            self.root, authority, authority_sha, lambda: self.preflight_proof)
        frozen = (self.root / RUN.FOLDER / "openrouter-preflight.json").read_text()
        self.assertNotIn("192.0.2.10", frozen)
        self.assertNotIn("ip=", frozen)
        dk = self.http_values(); dk[HF.LOCATION_URL] = "ip=192.0.2.30\nloc=DK\n"
        with mock.patch.dict(os.environ, {}, clear=True), \
                mock.patch.object(HF, "LEDGER", self.ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN, "_post") as post, \
                self.assertRaisesRegex(RUN.RunError, "not eligible: DK"):
            RUN.run(self.root, credit_check=mock.Mock(side_effect=AssertionError),
                authority_timestamp=AUTH,
                location_check=lambda: HF.current_location(
                    open_url=self.open_values(dk)))
        post.assert_not_called()
    def test_zero_credit_stops_before_chapter_generation(self):
        self.authorize_run(); before = self.snapshot(); values = self.http_values()
        values[HF.CREDITS_URL]["data"] = {"total_credits": 1, "total_usage": 1}
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key",
                                          "OPENROUTER_MANAGEMENT_KEY": "management-key"}), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN, "_post") as post, self.assertRaisesRegex(RUN.RunError, "account credit"):
                RUN.run(self.root, credit_check=lambda: RUN._credit_check(
                    open_url=self.open_values(values)), authority_timestamp=AUTH)
        post.assert_not_called(); self.assertEqual(before, self.snapshot())
if __name__ == "__main__": unittest.main()
