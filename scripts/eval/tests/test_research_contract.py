"""Focused RF-32 regressions for aggregate inspection and sealed research."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "scripts"), str(Path(__file__).resolve().parent)]

import validate_research_contract as RC  # noqa: E402
import research_contract_fixture as FIX  # noqa: E402
from research_contract_fixture import write_sealed_research  # noqa: E402


class ResearchContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="research contract "))
        self.operation = self.tmp / "Windows path with spaces"
        self.book = self.operation / "production-books" / "book"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def seal(self):
        return write_sealed_research(self.book)

    def test_sealed_contract_exposes_one_current_source_bounded_inventory(self):
        """RF-32: Research is independently accepted and sealed."""
        report = self.seal()
        units = RC.require_research_contract(self.book)
        identity = RC.research_seal_identity(self.book)
        self.assertTrue(report["ok"])
        self.assertEqual(identity, report["seal_identity"])
        self.assertRegex(identity, r"^[0-9a-f]{64}$")
        self.assertEqual(set(units), set(report["inventory"]["units"]))
        self.assertGreaterEqual(len(units), 4)
        for unit in report["inventory"]["units"].values():
            self.assertTrue(unit["Source locator"])
            self.assertTrue(unit["Permitted inference"])
            self.assertTrue(unit["Prohibited inference"])
            self.assertTrue(unit["Safety boundary"])
            self.assertEqual(unit["Source locator"].split(", "), unit["locators"])
            self.assertEqual(unit["Safety boundary"], unit["safety"])

    def test_current_quit_sugar_report_is_truthful_and_aggregate(self):
        """RF-32: The current quit-sugar corpus is inspected under the new contract."""
        book = ROOT / "production-books/quit-sugar"
        report = RC.inspect_research(book, require_seal=False)
        self.assertFalse(report["ok"])
        self.assertEqual(
            {"packets": 23, "evidence_items": 47, "lived_bank_entries": 57,
             "scientific_bank_entries": 12, "leu": 0, "seu": 0, "gap": 0},
            {key: report["counts"][key] for key in
             ("packets", "evidence_items", "lived_bank_entries",
              "scientific_bank_entries", "leu", "seu", "gap")},
        )
        blockers = "\n".join(report["blockers"])
        self.assertIn("missing section: Intended reader", blockers)
        self.assertIn("unresolved placeholder", blockers)
        self.assertIn("lack machine fields", blockers)
        self.assertIn("FULL-LENGTH floor lived_experience is 54/500", blockers)
        self.assertIsNone(report["seal_identity"])
        self.assertEqual(47, len(RC._packet_index(book / "research/sources")))

    def test_windows_cp1252_inspection_is_json_and_stops_directly(self):
        """RF-32: Offline readiness is tested without a production research run."""
        environment = dict(os.environ)
        environment["PYTHONIOENCODING"] = "cp1252"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_research_contract.py"),
             "--book", str(ROOT / "production-books/quit-sugar"), "--inspect"],
            cwd=self.tmp, env=environment, capture_output=True, text=True,
            encoding="ascii", errors="strict", check=False,
        )
        self.assertEqual(1, result.returncode)
        report = json.loads(result.stdout)
        self.assertEqual("BLOCKED", report["status"])
        self.assertEqual(23, report["counts"]["packets"])
        self.assertNotIn("Traceback", result.stderr)

    def test_changed_packet_stales_coverage_review_and_seal(self):
        """RF-32: Research is independently accepted and sealed."""
        self.seal()
        packet = next((self.book / "research/sources").glob("s-*.md"))
        packet.write_text(packet.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
        report = RC.inspect_research(self.book, require_seal=True)
        self.assertFalse(report["ok"])
        self.assertIn("stale", "\n".join(report["blockers"]))
        with self.assertRaises(RC.ContractError):
            RC.research_seal_identity(self.book)

    def test_candidate_local_prompt_and_config_drift_stale_the_seal(self):
        """RF-32: A research seal binds the candidate-local execution authority."""
        self.seal()
        for relative in ("prompts/research-agent.md", "prompts/research-evidence-editor.md",
                         "loop/config.yaml"):
            path = self.operation / relative
            original = path.read_bytes()
            path.write_bytes(original + b"\nchanged candidate authority\n")
            report = RC.inspect_research(self.book, require_seal=True)
            self.assertFalse(report["ok"])
            self.assertIn("stale", "\n".join(report["blockers"]))
            path.write_bytes(original)

    def test_review_rejection_and_task_tamper_fail_closed(self):
        """RF-32: Coverage or independent review proves a research gap."""
        self.seal()
        review_path = self.book / "research/research-review.json"
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["status"] = "BLOCKED"
        review_path.write_text(json.dumps(review), encoding="utf-8")
        report = RC.inspect_research(self.book, require_seal=True)
        self.assertFalse(report["ok"])
        self.assertIn("review", "\n".join(report["blockers"]))

    def test_rights_privacy_and_fetch_hash_defects_are_aggregated(self):
        """RF-32: A discovered source fails rights or privacy eligibility."""
        self.seal()
        packet = next((self.book / "research/sources").glob("s-*.md"))
        text = packet.read_text(encoding="utf-8")
        text = text.replace("synthetic fixture; no personal data retained", "unknown", 1)
        text = re.sub(r"(- \*\*Content SHA-256:\*\* )[0-9a-f]{64}", r"\g<1>" + "0" * 64,
                      text, count=1)
        packet.write_text(text, encoding="utf-8")
        blockers = "\n".join(RC.inspect_research(self.book, require_seal=False)["blockers"])
        self.assertIn("rights/privacy", blockers)
        self.assertIn("content hash", blockers)

    def test_duplicate_url_and_excerpt_cannot_inflate_coverage(self):
        """RF-32: Eligible evidence duplicates a retained source or study."""
        self.seal()
        packets = sorted((self.book / "research/sources").glob("s-*.md"))
        first, second = (path.read_text(encoding="utf-8") for path in packets[:2])
        first_url = re.search(r"^- \*\*URL:\*\* (.+)$", first, re.MULTILINE).group(1)
        second_url = re.search(r"^- \*\*URL:\*\* (.+)$", second, re.MULTILINE).group(1)
        second = second.replace(second_url, first_url)
        packets[1].write_text(second, encoding="utf-8")
        blockers = "\n".join(RC.inspect_research(self.book, require_seal=False)["blockers"])
        self.assertIn("duplicate canonical URL", blockers)

    def test_shared_url_policy_collapses_tracking_order_and_rejects_ineligible_hosts(self):
        """RF-32: shared inspection uses the production URL eligibility law."""
        self.seal()
        packets = sorted((self.book / "research/sources").glob("s-*.md"))
        first = packets[0].read_text(encoding="utf-8")
        second = packets[1].read_text(encoding="utf-8")
        first_old = re.search(r"^- \*\*URL:\*\* (.+)$", first, re.MULTILINE).group(1)
        second_old = re.search(r"^- \*\*URL:\*\* (.+)$", second, re.MULTILINE).group(1)
        first_url = "https://source.test/article?a=1&b=2"
        second_url = "https://SOURCE.test/article/?b=2&utm_source=lane&a=1"
        packets[0].write_text(first.replace(first_old, first_url), encoding="utf-8")
        packets[1].write_text(second.replace(second_old, second_url), encoding="utf-8")
        blockers = "\n".join(RC.inspect_research(
            self.book, require_seal=False)["blockers"])
        self.assertIn("duplicate canonical URL", blockers)
        for bad in ("https://user@example.test/story", "https://reddit.com/r/story"):
            self.seal()
            packet = next((self.book / "research/sources").glob("s-*.md"))
            text = packet.read_text(encoding="utf-8")
            old = re.search(r"^- \*\*URL:\*\* (.+)$", text, re.MULTILINE).group(1)
            packet.write_text(text.replace(old, bad), encoding="utf-8")
            blockers = "\n".join(RC.inspect_research(
                self.book, require_seal=False)["blockers"])
            self.assertIn("URL is not fetch-bound", blockers)

    def test_duplicate_source_id_across_filenames_is_explicitly_blocked(self):
        """RF-32: Packet-map overwrite cannot hide two files claiming one Source ID."""
        self.seal()
        source = self.book / "research/sources/S-001-sealed-fixture.md"
        (source.parent / "S-001-zz-mirror.md").write_bytes(source.read_bytes())
        report = RC.inspect_research(self.book, require_seal=False)
        blockers = "\n".join(report["blockers"])
        self.assertIn("duplicate Source ID across packet files (S-001)", blockers)
        self.assertEqual("research/sources/S-001-sealed-fixture.md",
                         report["inventory"]["packets"]["S-001"]["path"])

    def test_duplicate_excerpt_and_evidence_ids_block_the_sealed_packet(self):
        """RF-32: One packet locator cannot have conflicting retained authority."""
        self.seal()
        packet = next((self.book / "research/sources").glob("S-*.md"))
        text = packet.read_text(encoding="utf-8")
        excerpt = re.search(r"(?ms)^### C-001\s*$.*?(?=^## Evidence items\s*$)", text).group(0)
        evidence = re.search(r"(?ms)^### E-001\s*$.*?\Z", text).group(0)
        text = text.replace("## Evidence items", excerpt + "\n\n## Evidence items", 1)
        packet.write_text(text + "\n\n" + evidence + "\n", encoding="utf-8")
        report = RC.inspect_research(self.book, require_seal=True)
        blockers = "\n".join(report["blockers"])
        self.assertFalse(report["ok"])
        self.assertIn("duplicate excerpt ID C-001", blockers)
        self.assertIn("duplicate evidence ID E-001", blockers)

    def test_malformed_fetched_url_is_an_aggregate_blocker_not_an_exception(self):
        """RF-32: Malformed fetch provenance fails inside the aggregate report."""
        self.seal()
        packet = next((self.book / "research/sources").glob("S-*.md"))
        text = packet.read_text(encoding="utf-8")
        text = re.sub(r"^- \*\*Fetched URL:\*\* .+$",
                      "- **Fetched URL:** http://[malformed", text,
                      count=1, flags=re.MULTILINE)
        packet.write_text(text, encoding="utf-8")
        report = RC.inspect_research(self.book, require_seal=False)
        self.assertFalse(report["ok"])
        self.assertIn("URL is not fetch-bound", "\n".join(report["blockers"]))

    def test_rejected_packet_reports_only_aggregate_retention(self):
        """RF-32: A discovered source fails rights or privacy eligibility."""
        self.seal()
        packet = next((self.book / "research/sources").glob("s-*.md"))
        text = packet.read_text(encoding="utf-8").replace(
            "- **Disposition:** ACCEPTED", "- **Disposition:** REJECTED", 1)
        packet.write_text(text, encoding="utf-8")
        report = RC.inspect_research(self.book, require_seal=False)
        self.assertEqual(1, report["counts"]["rejected_packets"])
        rejection = [item for item in report["blockers"] if "rejected source packet" in item]
        self.assertEqual(["eligibility: 1 rejected source packet(s) were retained"], rejection)

    def test_scarcity_can_name_only_an_unmet_numeric_floor(self):
        """RF-32: A numeric floor is genuinely scarce."""
        self.seal()
        with self.assertRaisesRegex(RC.ContractError, "scarcity request"):
            RC.build_coverage(self.book, "POCKET", [{
                "floor": "belief_persona", "attempts_sha256": "0" * 64,
                "demonstrated_ceiling": 0,
            }])

    def test_missing_belief_persona_unit_blocks_downstream_authority(self):
        """RF-32: Every applicable belief/persona pair needs one complete unit."""
        self.seal()
        lived = self.book / "research/lived-experience.md"
        text = re.sub(r"(- \*\*Persona IDs:\*\* P-01; P-02); P-03", r"\1",
                      lived.read_text(encoding="utf-8"))
        lived.write_text(text, encoding="utf-8")
        report = RC.inspect_research(self.book, require_seal=True)
        self.assertIn("brief belief/persona lacks intervention unit",
                      "\n".join(report["blockers"]))
        self.assertIsNone(report["seal_identity"])

    def test_brief_belief_with_no_applicable_persona_is_an_explicit_gap(self):
        """RF-32: A lead cannot omit a completed brief belief from persona coverage."""
        self.seal()
        lived = self.book / "research/lived-experience.md"
        other = "; ".join(FIX.BELIEFS[1:])
        lived.write_text(lived.read_text(encoding="utf-8").replace(
            "| ALL |", f"| {other} |"), encoding="utf-8")
        report = RC.inspect_research(self.book, require_seal=False)
        self.assertIn("brief belief has no applicable persona", "\n".join(report["blockers"]))
        self.assertIn(f"{FIX.BELIEFS[0]} / UNASSIGNED",
                      {gap["target"] for gap in report["gaps"]})

    def test_style_slots_require_three_distinct_source_grounded_personas(self):
        """RF-32: Slot coverage is persona-spread, not mere nonempty activity."""
        self.seal()
        for packet in (self.book / "research/sources").glob("S-*.md"):
            packet.write_text(packet.read_text(encoding="utf-8").replace(
                "- **Persona tags:** P-01; P-02; P-03",
                "- **Persona tags:** P-01; P-02"), encoding="utf-8")
        blockers = "\n".join(RC.inspect_research(self.book, require_seal=False)["blockers"])
        self.assertIn("reaches 2/3 distinct personas", blockers)

    def test_deselected_packet_cannot_supply_style_slot_coverage(self):
        """RF-32: Only accepted synthesis/unit citations count toward style slots."""
        self.seal()
        lived = self.book / "research/lived-experience.md"
        lived.write_text("\n".join(
            line for line in lived.read_text(encoding="utf-8").splitlines()
            if "S-010#E-001" not in line) + "\n", encoding="utf-8")
        for packet in (self.book / "research/sources").glob("S-*.md"):
            if not packet.name.startswith("S-010-"):
                packet.write_text(packet.read_text(encoding="utf-8").replace(
                    "; TESTIMONIAL", ""), encoding="utf-8")
        blockers = "\n".join(RC.inspect_research(
            self.book, require_seal=False)["blockers"])
        self.assertIn("style slot TESTIMONIAL reaches 0/3 distinct personas", blockers)

    def test_malformed_source_identity_and_unsafe_retention_are_aggregated(self):
        """RF-32: Empty provenance and deletion-sensitive retention never pass."""
        self.seal()
        packet = next((self.book / "research/sources").glob("S-*.md"))
        text = packet.read_text(encoding="utf-8")
        text = re.sub(r"(- \*\*Fetched content SHA-256:\*\* )[0-9a-f]{64}", r"\1", text, count=1)
        text = text.replace("- **Retrieved (UTC):** 2026-07-23T00:00:00Z",
                            "- **Retrieved (UTC):** yesterday", 1)
        text = text.replace("- **Source type:** report", "- **Source type:** unknown", 1)
        text = text.replace("- **Deletion sensitivity:** NOT_DELETION_SENSITIVE",
                            "- **Deletion sensitivity:** DELETION_SENSITIVE", 1)
        packet.write_text(text, encoding="utf-8")
        blockers = "\n".join(RC.inspect_research(self.book, require_seal=False)["blockers"])
        self.assertIn("invalid title/type/retrieval identity", blockers)
        self.assertIn("invalid fetched-content hash", blockers)
        self.assertIn("unsafe retention/privacy status", blockers)

    def test_empty_unit_grounding_and_ambiguous_grade_do_not_enter_inventory(self):
        """RF-32: Units and evidence require resolved exact machine authority."""
        self.seal()
        lived = self.book / "research/lived-experience.md"
        lived.write_text(lived.read_text(encoding="utf-8").replace(
            "- **Situation:** Distinct cue 1", "- **Situation:** ", 1), encoding="utf-8")
        packet = next((self.book / "research/sources").glob("S-*.md"))
        packet.write_text(packet.read_text(encoding="utf-8").replace(
            "- **Evidence grade:** n/a", "- **Evidence grade:** n/a MIXED", 1), encoding="utf-8")
        report = RC.inspect_research(self.book, require_seal=False)
        blockers = "\n".join(report["blockers"])
        self.assertIn("lacks complete intervention authority", blockers)
        self.assertIn("exactly one canonical grade", blockers)
        self.assertNotIn("LEU-001", report["inventory"]["units"])

    def test_two_lineage_rule_applies_to_bank7_but_not_bank8(self):
        """RF-32: Mechanism support needs two studies; industry receipts do not."""
        self.seal()
        science = self.book / "research/scientific-evidence.md"
        packet7 = self.book / "research/sources/S-005-sealed-fixture.md"
        packet7.write_text(packet7.read_text(encoding="utf-8").replace(
            "- **Evidence grade:** CONTESTED", "- **Evidence grade:** SUPPORTED", 1),
            encoding="utf-8")
        science.write_text(science.read_text(encoding="utf-8").replace(
            "- **Evidence grade:** CONTESTED", "- **Evidence grade:** SUPPORTED", 1),
            encoding="utf-8")
        self.assertIn("science: SEU-001 lacks two independent study lineages",
                      RC.inspect_research(self.book, require_seal=False)["blockers"])

        self.seal()
        science_text = (self.book / "research/scientific-evidence.md").read_text(encoding="utf-8")
        replacements = {"Distinct cue 5": "Distinct cue 6", "example 5": "example 6",
                        "unease 5": "unease 6", "Example 5": "Example 6",
                        "S-005#E-001": "S-006#E-001", "CONTESTED": "SUPPORTED"}
        for old, new in replacements.items():
            science_text = science_text.replace(old, new, 1)
        (self.book / "research/scientific-evidence.md").write_text(science_text, encoding="utf-8")
        packet8 = self.book / "research/sources/S-006-sealed-fixture.md"
        packet8.write_text(packet8.read_text(encoding="utf-8").replace(
            "- **Evidence grade:** CONTESTED", "- **Evidence grade:** SUPPORTED", 1),
            encoding="utf-8")
        blockers = RC.inspect_research(self.book, require_seal=False)["blockers"]
        self.assertNotIn("science: SEU-001 lacks two independent study lineages", blockers)

    def test_scientific_duplicate_meaning_is_scoped_to_underlying_lineage(self):
        """RF-32: Independent studies may share a claim; same-lineage mirrors may not."""
        self.seal()
        packet = self.book / "research/sources/S-006-sealed-fixture.md"
        text = packet.read_text(encoding="utf-8")
        for old, new in (("example 6", "example 5"),
                         ("Distinct cue 6 and unease 6", "Distinct cue 5 and unease 5"),
                         ("Example 6 does not", "Example 5 does not")):
            text = text.replace(old, new)
        excerpt = re.search(r"```text\n(.*?)\n```", text, re.S).group(1)
        digest = RC._sha_bytes(excerpt.encode("utf-8"))
        text = re.sub(r"(?m)(- \*\*(?:Fetched content SHA-256|Content SHA-256):\*\* )[0-9a-f]{64}",
                      rf"\g<1>{digest}", text)
        packet.write_text(text, encoding="utf-8")
        blockers = RC.inspect_research(self.book, require_seal=False)["blockers"]
        self.assertNotIn("duplicate evidence meaning", "\n".join(blockers))
        packet.write_text(text.replace("fixture-lineage-6", "fixture-lineage-5"),
                          encoding="utf-8")
        blockers = RC.inspect_research(self.book, require_seal=False)["blockers"]
        self.assertIn("duplicate evidence meaning", "\n".join(blockers))

    def test_lineage_case_and_whitespace_cannot_fake_independence(self):
        """RF-32: Study-lineage identity is case/whitespace normalized."""
        self.seal()
        packet5 = self.book / "research/sources/S-005-sealed-fixture.md"
        packet6 = self.book / "research/sources/S-006-sealed-fixture.md"
        packet5.write_text(packet5.read_text(encoding="utf-8").replace(
            "- **Evidence grade:** CONTESTED", "- **Evidence grade:** SUPPORTED"),
            encoding="utf-8")
        packet6.write_text(packet6.read_text(encoding="utf-8")
            .replace("fixture-lineage-6", "  FIXTURE-LINEAGE-5  ")
            .replace("- **Bank slots:** Bank 8", "- **Bank slots:** Bank 7")
            .replace("- **Evidence grade:** CONTESTED", "- **Evidence grade:** SUPPORTED"),
            encoding="utf-8")
        science = self.book / "research/scientific-evidence.md"
        text = science.read_text(encoding="utf-8")
        text = text.replace("- **Source locator:** S-005#E-001",
                            "- **Source locator:** S-005#E-001; S-006#E-001", 1)
        text = text.replace("- **Evidence grade:** CONTESTED",
                            "- **Evidence grade:** SUPPORTED", 1)
        text = text.replace("[Bank 7] [CONTESTED]", "[Bank 7] [SUPPORTED]", 1)
        text = text.replace("Source IDs: S-005#E-001",
                            "Source IDs: S-005#E-001; S-006#E-001", 1)
        science.write_text(text, encoding="utf-8")
        blockers = "\n".join(RC.inspect_research(
            self.book, require_seal=False)["blockers"])
        self.assertIn("lacks two independent study lineages", blockers)


if __name__ == "__main__":
    unittest.main()
