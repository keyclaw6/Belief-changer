"""Shared isolated RF-10 candidate fixture."""
import tempfile
from pathlib import Path
from unittest import mock

import candidate_pair as PAIR
import commission_set as SET
from test_commission_contract import commission
from test_commission_set import assigned
from commission_packet_fixture import packet
from developmental_commission_fixture import STATES
from research_contract_fixture import (chapter_binding, evidence_row,
                                       write_sealed_research)


class WriterFixture:
    selection = (1, 2)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.accepted = Path(self.tmp.name) / "repo"
        files = {
            "loop/config.yaml": (
                "writer_model: writer/model\nwriter_reasoning: none\n"
                "grounded_reviewer_model: reviewer/model\n"
                "grounded_reviewer_family: reviewer\n"
                "grounded_reviewer_route: codex-native\n"
                "grounded_reviewer_reasoning: xhigh\n"
                "developmental_reviewer_model: developmental/model\n"
                "developmental_reviewer_family: developmental\n"
                "developmental_reviewer_route: codex-native\n"
                "developmental_reviewer_reasoning: max\n"
                "judge_rubric: calibration/judges/rubric.md\n"
                "reference_dir: calibration/reference/book\nresults_tsv: loop/results.tsv\n"),
            "loop/results.tsv": "iter\treward\tverdict\n",
            "prompts/chapter-writer.md": "COMPACT-CONTRACT chapter=[N] slug=[SLUG]\n",
            "prompts/style-guide.md": "FORBIDDEN-FULL-STYLE\n",
            "prompts/chapter-commissioner.md": "commissioner\n",
            "prompts/commission-set-auditor.md": "auditor\n",
            "prompts/chapter-reviewer.md": "reviewer\n",
            "prompts/grounded-reviewer.md": "grounded reviewer contract\n",
            "prompts/developmental-reviewer.md": "developmental reviewer contract\n",
            "production-books/test/00-brief.md": "brief\n",
            "production-books/test/research/lived-experience.md": "lived\n",
            "production-books/test/research/scientific-evidence.md": "science\n",
            "production-books/test/research/sources/s-101-fixture.md":
                packet("S-101", "E-001", "FORBIDDEN-RAW-ASSIGNED") +
                "\n### E-002\n- **Kind:** INTERPRETATION\n"
                "- **Text:** FORBIDDEN-RAW-UNASSIGNED-SAME-PACKET\n"
                "- **Excerpt ID:** C-001\n- **Locator:** fixture paragraph\n"
                "- **Persona tags:** ALL\n- **Bank slots:** Bank 2\n"
                "- **Evidence grade:** SUPPORTED\n"
                "- **Use / limits:** unassigned mixed-file fixture\n",
            "production-books/test/research/sources/s-102-fixture.md":
                packet("S-102", "E-001", "FORBIDDEN-RAW-SECOND"),
            "production-books/test/research/sources/s-103-fixture.md":
                packet("S-103", "E-001", "THIRD-ASSIGNED-TEXTURE"),
            "production-books/test/research/sources/s-999-unassigned.md":
                packet("S-999", "E-001", "FORBIDDEN-UNASSIGNED"),
            "production-books/test/framing.md": (
                "## Journey\n### CH-01 — First\n- state one\n"
                "### CH-02 — Second\n- state two\n"
                "### CH-03 — Third\n- state three\n"),
            "production-books/test/master-plan.md": (
                "# FORBIDDEN-FULL-PLAN\n### C-01 — First\n"
                f"- **Entering belief:** {STATES[1][0]}\n"
                f"- **Leaving belief:** {STATES[1][1]}\n"
                "### C-02 — Second\n"
                f"- **Entering belief:** {STATES[2][0]}\n"
                f"- **Leaving belief:** {STATES[2][1]}\n"
                "### C-03 — Third\n"
                f"- **Entering belief:** {STATES[3][0]}\n"
                f"- **Leaving belief:** {STATES[3][1]}\n"),
            "production-books/test/master-plan-review.md": "fit to write from\n",
            "production-books/test/reviews/chapter-01.md": "FORBIDDEN-JUDGE-FEEDBACK\n",
            "production-books/test/chapters/chapter-01.md": "ORIGINAL-PREVIOUS-ONE\n",
            "production-books/test/chapters/chapter-02.md": "ORIGINAL-SECOND\n",
            "production-books/test/chapters/chapter-03.md": "FORBIDDEN-EXTRA-CHAPTER\n",
            "calibration/judges/rubric.md": "rubric\n",
            "calibration/reference/book/reference-metrics.json": '{"chapters": []}\n',
            "calibration/reference/book/reference.txt": "FORBIDDEN-REFERENCE-TEXT\n",
        }
        for relative, text in files.items():
            path = self.accepted / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode("utf-8"))
        report = write_sealed_research(self.accepted / "production-books/test")
        self.research_report = report
        units = report["inventory"]["units"]
        rows = "\n".join(evidence_row(report, f"E-{number:02d}", f"LEU-{number:03d}")
                         for number in (1, 2, 3))
        cards = "".join(
            f"### C-{number:02d} â€” Chapter {number}\n"
            f"- **Entering belief:** {STATES[number][0]}\n"
            f"- **Leaving belief:** {STATES[number][1]}\n"
            f"- **Evidence IDs and required limits:** E-{number:02d}\n"
            f"- **Guardrails:** {units[f'LEU-{number:03d}']['safety']}\n"
            for number in (1, 2, 3))
        (self.accepted / "production-books/test/master-plan.md").write_text(
            "# FORBIDDEN-FULL-PLAN\n\n## Evidence ledger\n\n"
            "| ID | Finding / lived material | Research unit IDs | Source ID | Grade or outcome tier | Scope and limit | Permitted inference | Prohibited inference |\n"
            "|---|---|---|---|---|---|---|---|\n" + rows + "\n\n" + cards,
            encoding="utf-8")
        PAIR.initialize(self.accepted, "production-books/test")
        self.assignments = {f"C-{number:02d}": assigned(
            f"C-{number:02d}", f"S-{number:03d}",
            chapter_binding(report, f"E-{number:02d}", f"LEU-{number:03d}"))
            for number in self.selection}

    def tearDown(self):
        self.tmp.cleanup()

    def candidate(self, name):
        root = self.accepted / f"loop/experiments/{name}"
        root.mkdir(parents=True)
        chapters = f"1-{self.selection[-1]}"
        PAIR.snapshot(root, self.accepted, "production-books/test", chapters, iteration=1)
        return root

    def generate(self, root, audit=SET.AUDIT_PASS, assignments=None, runner=None):
        assignments = assignments or self.assignments
        runner = runner or (lambda request: commission(assignments[request["target"]]["authority"]))
        with mock.patch.object(SET.SC, "require_subject_contract"):
            return SET.generate(root, assignments, runner, lambda request: audit)

    def book(self, candidate):
        return PAIR.candidate_tree(candidate) / "production-books/test"
