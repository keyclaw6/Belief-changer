"""Synthetic, offline integration fixture. Never empirical research or release evidence."""
from __future__ import annotations
import shutil
from pathlib import Path
from .common import atomic_json, require
from .runs import Run, active_files, prepare
from .schema import CHECKS


def inputs(subject: str = "practice-belief") -> tuple[dict, dict, dict]:
    brief = {"schema_version": 2, "subject": subject, "title": "One Attempt Is Not a Verdict (SOFTWARE FIXTURE)",
             "audience": "A consenting adult examining a belief about practice", "reader_goal": "Examine what one unsuccessful attempt can logically establish",
             "target_belief": "One error proves I cannot learn", "target_kind": "belief", "outcome_mode": "reframe", "risk_level": "low",
             "safety_advisory": "", "narrator": {"mode": "informed_author", "name": "", "allowed_claims": []}, "scope_exclusions": ["Clinical or educational outcome guarantees"]}
    research = {"schema_version": 2, "subject": subject,
                "sources": [{"id": "demo-illustration", "kind": "illustration", "source": "synthetic-software-fixture-not-a-retrieved-source",
                             "locator": "demo.py", "retrieved_at": "NOT RETRIEVED: SOFTWARE FIXTURE", "excerpt": "A deliberately invented attempt at a puzzle.",
                             "claim": "Illustration only; no empirical claim", "population": "No observed participants", "permitted_inference": "Illustrate a logical distinction only",
                             "prohibited_inferences": ["Any claim of observed learning or book efficacy"], "counterevidence": ["No empirical data were collected"],
                             "rights_basis": "Original synthetic illustration for testing", "verification": "unverified"}],
                "open_questions": ["Actual reader effects are unmeasured"], "strongest_countercase": "Practice does not guarantee every desired outcome.",
                "coverage": {"fixture_only": True, "empirical_coverage": "none"}}
    chapters = []
    for n in (1, 2):
        chapters.append({"id": f"chapter-{n:02d}", "title": "What follows" if n == 1 else "A bounded choice",
                         "objective": "Separate one observation from a universal conclusion" if n == 1 else "Preserve agency without promising success",
                         "entering_belief": "An error proves inability" if n == 1 else "A new attempt must guarantee success",
                         "strongest_objection": "The unsuccessful attempt did happen", "evidence_ids": [],
                         "supported_conclusion": "One attempt alone is not a universal proof" if n == 1 else "Choosing another attempt need not promise its result",
                         "remaining_objection": "What to choose next" if n == 1 else "No further claim is established",
                         "dependencies": [] if n == 1 else ["chapter-01"], "scenes": [], "word_budget": None})
    return brief, research, {"schema_version": 2, "subject": subject, "title": brief["title"],
                             "thesis": "A limited observation does not alone establish a universal conclusion", "limits": "Logical illustration only; no measured effects", "chapters": chapters}


def metadata(external: bool = False) -> dict:
    return {"model": "synthetic-external" if external else "synthetic-generator", "family": "fixture-external" if external else "meta",
            "route": "offline-fixture", "harness": "fixture", "usage": None, "latency_s": 0.0}


def accepted() -> dict:
    return {"schema_version": 2, "verdict": "ACCEPT", "checks": {c: True for c in CHECKS}, "findings": []}


def finish(run: Run, plan: dict) -> dict:
    def put(role: str, output: dict, chapter: int | None = None, round_no: int = 1) -> None:
        task = run.task(role, chapter, round_no)
        run.submit(task, output, metadata(role in ("evidence-reviewer", "final-auditor")))
    put("evidence-reviewer", accepted())
    put("planner", plan)
    put("plan-reviewer", accepted())
    texts = ["One unsuccessful attempt is one observation. It does not, by logic alone, establish that every future attempt must fail. That leaves a question rather than a verdict.",
             "You may choose another attempt without promising its result. You may also choose a different goal. The earlier observation does not decide that choice for you."]
    for n, card in enumerate(plan["chapters"], 1):
        text = texts[(n-1) % len(texts)]
        put("writer", {"schema_version": 2, "chapter_id": card["id"], "text": text, "claim_map": []}, n)
        put("chapter-reviewer", accepted(), n)
        put("state-editor", {"schema_version": 2, "chapter_id": card["id"], "established": [{"belief": card["supported_conclusion"], "quote": text.split(". ")[0]+"."}],
                             "unresolved": [card["remaining_objection"]], "used_examples": []}, n)
    put("book-editor", {"schema_version": 2, "operations": [], "explanation": "Synthetic two-chapter integration fixture; no actual editorial effectiveness judgment."})
    a = run.assemble()
    final = accepted()
    final.update({"claim_checks": [{"quote": texts[0].split(". ")[0]+".", "evidence_ids": [], "support": "nonempirical", "explanation": "Logical illustration, not an observed outcome."}],
                  "screening_resolutions": {f["id"]: "Synthetic fixture inspected; not empirical evidence." for f in a["screening"]}})
    put("final-auditor", final)
    return run.complete()


def scaffold(source: Path, dest: Path) -> None:
    require(not dest.exists() or not any(dest.iterdir()), "Demo/test destination must be new or empty")
    dest.mkdir(parents=True, exist_ok=True)
    for rel in active_files(source):
        p = dest / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / rel, p)
    for rel in ("factory/champion.json", "factory/calibration.json"):
        p = dest / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / rel, p)


def run_demo(source: Path, dest: Path) -> dict:
    scaffold(source, dest)
    brief, research, plan = inputs()
    prepare(dest, "offline-demo", brief, research, fixture=True)
    status = finish(Run(dest, "offline-demo"), plan)
    result = {"status": "OFFLINE_DEMO_PASSED", "calls_to_live_models": 0,
              "book": str((dest / "runs/offline-demo/book.md").resolve()), "verification": status,
              "warning": "Synthetic software fixture. Not research, human calibration, publishable content or proof of reader outcomes."}
    atomic_json(dest / "DEMO-RESULT.json", result)
    return result
