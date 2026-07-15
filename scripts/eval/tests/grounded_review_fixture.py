"""Shared RF-12 frozen-batch and proven-native-result fixture helpers."""
import json
from pathlib import Path
from unittest import mock

import commission_set as SET
import first_draft_batch as BATCH
import grounded_review as GR
import grounded_review_call as CALL
import run_iteration as RUN
from writer_context_fixture import WriterFixture


def draft(number, marker=""):
    return f"# Chapter {number}\n{marker}\n" + "word " * 801 + "\n"


def verdict(task, status="PASS", findings=None):
    return json.dumps({"schema": 2, "task_sha256": task["task_sha256"],
                       "verdict": status, "findings": findings or []}, sort_keys=True)


def finding(task, classification, owner=None):
    routes = {
        "invention": ("unsupported_by_assigned_authority", "writing",
                       "remove_unsupported_span"),
        "inference broadening": ("exceeds_permitted_inference", "writing",
                                  "narrow_claim_to_assigned_authority"),
        "packet conflict": ("assigned_authority_conflict", "research",
                            "resolve_assigned_conflict"),
        "safety breach": ("violates_required_safety_limit", "writing",
                          "restore_required_safeguard"),
        "originality/near-copy": ("near_copy_of_assigned_excerpt", "writing",
                                  "replace_near_copy_span"),
        "ownership leakage": ("uses_unassigned_authority", "writing",
                              "remove_reserved_or_unassigned_work"),
    }
    condition, default_owner, action = routes[classification]
    if owner is not None:
        default_owner = owner
    locator = task["context"]["assigned_evidence"][0]["locator"]
    return {"classification": classification, "draft_span": "FROZEN-ONE",
            "source_locators": [locator], "condition_code": condition,
            "owner": default_owner, "action_code": action}


def proven_runner(response=None, calls=None, interrupt=None):
    def run(dispatch):
        task, marker = dispatch["task"], dispatch["marker"]
        if calls is not None:
            calls.append(task["chapter"])
        raw = response(task) if response else verdict(task)
        runtime = {"exit_code": 0, "thread_id": f"thread-{task['chapter']:02d}",
                   "usage": {"input_tokens": 1}, "command": marker["command"]}
        root = Path(dispatch["workdir"]).parents[3]
        CALL.persist(root, task, marker, raw, runtime, interrupt)
    return run


def pass_review(candidate):
    return GR.advance(candidate, runner=proven_runner())


class GroundedFixture(WriterFixture):
    def frozen(self, name, before_generate=None):
        candidate = self.candidate(name)
        if before_generate:
            before_generate(candidate)
        self.generate(candidate)
        outputs = [draft(1, "FROZEN-ONE"), draft(2, "FROZEN-TWO")]
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "key")), \
                mock.patch.object(RUN.ME, "chat", side_effect=outputs):
            RUN.write_chapters({"writer_model": "writer/model", "writer_reasoning": "none"},
                               self.book(candidate), [1, 2], candidate)
        BATCH.freeze(candidate)
        return candidate
