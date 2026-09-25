"""Offline regression tests. No API credentials, providers or network are used."""
from __future__ import annotations
import copy
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

SOURCE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE / "scripts"))
from bc_factory.common import FactoryError, atomic_json, confined, digest, file_hash, lock, parse_json, read_json, reply_json, seal, unseal
from bc_factory.schema import CHECKS, DIMENSIONS, FINDINGS, finding_types, validate_brief, validate_plan, validate_research, validate_review, validate_state, validate_writer, validate_config, validate_metadata
from bc_factory.runs import Run, prepare
from bc_factory.quality import assemble_book, edit_book, overlap_screen, screen
from bc_factory.demo import accepted, finish, inputs, metadata, scaffold, run_demo
from bc_factory.adapters import execute, extract
from bc_factory.experiments import CALIBRATION_CATEGORIES, decide, pair_task, promote, register, submit_pair, transfer_decide, validate_calibration, wilson_lower
from bc_factory.archive import build, excluded

class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        scaffold(SOURCE, self.repo)
        self.brief, self.research, self.plan = inputs()
    def tearDown(self):
        self.tmp.cleanup()
    def newrun(self, name="r1", fixture=True):
        if fixture:
            prepare(self.repo, name, self.brief, self.research, fixture=True)
        else:
            with patch('bc_factory.research_access.validate_preflight'), patch('bc_factory.research_access.validate_coverage'):
                prepare(self.repo, name, self.brief, self.research, fixture=False)
        return Run(self.repo, name)
    def to_plan(self, run):
        for role, output in (("evidence-reviewer", accepted()), ("planner", self.plan), ("plan-reviewer", accepted())):
            run.submit(run.task(role), output, metadata(role=="evidence-reviewer"))
    def to_writer(self, run):
        self.to_plan(run)
        out={"schema_version":2,"chapter_id":"chapter-01","text":"One attempt does not logically prove a universal inability.","claim_map":[]}
        run.submit(run.task("writer",1), out, metadata())
        return out

class SerializationTests(Base):
    def test_duplicate_json_key(self):
        with self.assertRaises(FactoryError): parse_json('{"a":1,"a":2}')
    def test_nan_rejected(self):
        with self.assertRaises(FactoryError): parse_json('{"n":NaN}')
    def test_marker_string_is_not_report(self):
        for text in ('PASS\nCLUSTER CENSUS', 'log\n{"schema_version":2}', '[]'):
            with self.assertRaises(FactoryError): reply_json(text)
    def test_single_fenced_json(self):
        self.assertEqual(reply_json('```json\n{"a":1}\n```'), {"a":1})
    def test_path_traversal(self):
        for p in ('../secret','/etc/passwd','a/../../x','x\\y'):
            with self.assertRaises(FactoryError): confined(self.repo,p)
    def test_symlink_rejected(self):
        (self.repo/'link').symlink_to(Path(self.tmp.name),target_is_directory=True)
        with self.assertRaises(FactoryError): confined(self.repo,'link/file')
    def test_sealed_tamper_detected(self):
        p=self.repo/'record.json'; seal(p,{"a":1})
        d=read_json(p);d['payload']['a']=2;atomic_json(p,d)
        with self.assertRaises(FactoryError): unseal(p)
    def test_seal_is_immutable(self):
        p=self.repo/'record.json';seal(p,{'a':1});seal(p,{'a':1})
        with self.assertRaises(FactoryError): seal(p,{'a':2})
    def test_lock_not_stolen(self):
        with lock(self.repo):
            with self.assertRaises(FactoryError):
                with lock(self.repo): pass
        self.assertFalse((self.repo/'.factory.lock').exists())

class SchemaTests(Base):
    def test_fragment_shared_parser(self):
        self.assertIn('FRAGMENT',FINDINGS)
        self.assertEqual(finding_types('REVISE\nFRAGMENT three fragments'),['FRAGMENT'])
    def test_unknown_finding_rejected(self):
        with self.assertRaises(FactoryError): finding_types('REVISE\nNEW-BAN something')
    def test_accept_with_hidden_failure_rejected(self):
        r=accepted();r['checks']['truth']=False
        with self.assertRaises(FactoryError): validate_review(r,'text')
    def test_accept_with_fragment_rejected(self):
        r=accepted();r['findings']=[{'kind':'FRAGMENT','severity':'minor','quote':'text','explanation':'Incomplete thought','repair':'Make complete'}]
        with self.assertRaises(FactoryError): validate_review(r,'text')
    def test_invented_review_quote_rejected(self):
        r=accepted();r['verdict']='REVISE';r['findings']=[{'kind':'OVERCLAIM','severity':'critical','quote':'not here','explanation':'Overclaim','repair':'Narrow'}]
        with self.assertRaises(FactoryError): validate_review(r,'actual text')
    def test_finding_may_quote_any_reviewed_input(self):
        r=accepted();r['verdict']='REVISE';r['findings']=[{'kind':'SCOPE','severity':'material','quote':'brief goal','explanation':'Scope','repair':'Narrow'}]
        validate_review(r,'{"brief": "brief goal", "research": "actual text"}')
        with self.assertRaises(FactoryError): validate_review(r,'{"research": "actual text"}')
    def test_final_claims_stay_bound_to_book_text(self):
        r=accepted();r['verdict']='REVISE';r['findings']=[{'kind':'EVIDENCE','severity':'material','quote':'brief goal','explanation':'Gap','repair':'Add'}]
        r['claim_checks']=[{'quote':'book sentence','evidence_ids':[],'support':'nonempirical','explanation':'Logic'}]
        r['screening_resolutions']={}
        validate_review(r,'{"brief": "brief goal"}',final=True,claim_text='book sentence')
        with self.assertRaises(FactoryError):
            validate_review(r,'{"brief": "brief goal"}',final=True,claim_text='other text')
    def test_unknown_json_finding_rejected(self):
        r=accepted();r['verdict']='REVISE';r['findings']=[{'kind':'SUPERSTYLE','severity':'minor','quote':'text','explanation':'x','repair':'x'}]
        with self.assertRaises(FactoryError): validate_review(r,'text')
    def test_narrator_cannot_invent_credentials(self):
        b=copy.deepcopy(self.brief);b['narrator']['allowed_claims']=[{'claim':'I treated 100 patients','evidence_ids':['demo-illustration']}]
        with self.assertRaises(FactoryError): validate_brief(b)
    def test_verified_author_needs_author_specific_source(self):
        b=copy.deepcopy(self.brief);b['narrator']={'mode':'verified_person','name':'Test Person','allowed_claims':[{'claim':'I ran this practice','evidence_ids':['demo-illustration']}]}
        with self.assertRaises(FactoryError): validate_research(self.research,b)
    def test_health_requires_advisory(self):
        b=copy.deepcopy(self.brief);b['risk_level']='health'
        with self.assertRaises(FactoryError): validate_brief(b)
    def test_duplicate_source_rejected(self):
        r=copy.deepcopy(self.research);r['sources']*=2
        with self.assertRaises(FactoryError): validate_research(r,self.brief)
    def test_plan_forward_dependency_rejected(self):
        p=copy.deepcopy(self.plan);p['chapters'][0]['dependencies']=['chapter-02']
        with self.assertRaises(FactoryError): validate_plan(p,self.brief,self.research)
    def test_missing_plan_evidence_rejected(self):
        p=copy.deepcopy(self.plan);p['chapters'][0]['evidence_ids']=['absent']
        with self.assertRaises(FactoryError): validate_plan(p,self.brief,self.research)
    def test_budget_is_not_required(self):
        validate_plan(self.plan,self.brief,self.research)
    def test_source_scene_requires_evidence(self):
        p=copy.deepcopy(self.plan);p['chapters'][0]['scenes']=[{'description':'An actual person','type':'sourced','evidence_ids':[]}]
        with self.assertRaises(FactoryError): validate_plan(p,self.brief,self.research)
    def test_writer_map_quote_must_exist(self):
        with self.assertRaises(FactoryError): validate_writer({'schema_version':2,'chapter_id':'chapter-01','text':'Actual text','claim_map':[{'quote':'Invented claim','evidence_ids':['demo-illustration']}]},'chapter-01',self.research)
    def test_state_must_quote_delivered_text(self):
        with self.assertRaises(FactoryError): validate_state({'schema_version':2,'chapter_id':'chapter-01','established':[{'belief':'Desired result','quote':'never said'}],'unresolved':[],'used_examples':[]},'chapter-01','Actual text')

class AdditionalSafetyTests(Base):
    def test_config_cannot_store_api_key_values(self):
        cfg=read_json(self.repo/'factory/config.json')
        cfg['profiles']['factory']['routes'][0]['api_key']='not-allowed'
        with self.assertRaises(FactoryError): validate_config(cfg)
    def test_config_endpoint_cannot_embed_credential(self):
        cfg=read_json(self.repo/'factory/config.json')
        cfg['profiles']['factory']['routes'][0]['endpoint']='https://user:password@example.org'
        with self.assertRaises(FactoryError): validate_config(cfg)
    def test_nan_latency_rejected(self):
        m=metadata();m['latency_s']=float('nan')
        with self.assertRaises(FactoryError): validate_metadata(m)
    def test_illustration_cannot_prove_empirical_claim(self):
        with self.assertRaises(FactoryError): validate_writer({'schema_version':2,'chapter_id':'chapter-01','text':'This improves learning.','claim_map':[{'quote':'This improves learning.','evidence_ids':['demo-illustration']}]},'chapter-01',self.research)
    def test_unverified_live_dossier_cannot_be_accepted(self):
        run=self.newrun(fixture=False)
        m=metadata(True);m['harness']='test-supplied-independent-review'
        with self.assertRaises(FactoryError): run.submit(run.task('evidence-reviewer'),accepted(),m)
    def test_generator_cannot_switch_to_review_family(self):
        run=self.newrun()
        run.submit(run.task('evidence-reviewer'),accepted(),metadata(True))
        with self.assertRaises(FactoryError): run.submit(run.task('planner'),self.plan,metadata(True))
    def test_editor_move_merge_replace(self):
        c=[{'id':f'chapter-{n:02d}','title':str(n),'text':f'Text {n}.','source_chapters':[f'chapter-{n:02d}'],'claim_map':[]} for n in (1,2,3)]
        out=edit_book(c,{'schema_version':2,'operations':[
            {'op':'move','chapter':'chapter-03','before':'chapter-02','reason':'Dependency'},
            {'op':'merge','first':'chapter-01','second':'chapter-03','title':'Joined','reason':'Economy'},
            {'op':'replace','chapter':'chapter-01','old':'Text 3.','new':'Edited 3.','reason':'Clarity'}], 'explanation':'Global revision'})
        self.assertEqual([x['id'] for x in out],['chapter-01','chapter-02'])
        self.assertIn('Edited 3.',out[0]['text'])
        self.assertEqual(c[0]['text'],'Text 1.')

class RunTests(Base):
    def test_zero_chapters_not_complete(self):
        run=self.newrun()
        self.assertEqual(run.status()['status'],'INCOMPLETE')
        with self.assertRaises(FactoryError): run.complete()
    def test_freeze_cannot_overwrite(self):
        self.newrun()
        with self.assertRaises(FactoryError): self.newrun()
    def test_frozen_input_tamper_fails(self):
        run=self.newrun();(run.root/'inputs/brief.json').write_text('{}')
        with self.assertRaises(FactoryError): Run(self.repo,'r1')
    def test_frozen_prompt_tamper_fails(self):
        run=self.newrun();(run.root/'snapshot/prompts/style-guide.md').write_text('changed')
        with self.assertRaises(FactoryError): Run(self.repo,'r1')
    def test_current_prompt_does_not_change_frozen_task(self):
        run=self.newrun();task=run.task('evidence-reviewer')
        (self.repo/'prompts/evidence-reviewer.md').write_text('different live prompt')
        self.assertEqual(run.task('evidence-reviewer'),task)
    def test_no_plan_before_research_review(self):
        run=self.newrun()
        task=run.task('evidence-reviewer')
        self.assertEqual(set(task['inputs']), {'brief','research'})
        with self.assertRaises(FactoryError): run.task('planner')
    def test_evidence_reviewer_contract_is_bounded_and_convergent(self):
        contract=(self.repo/'prompts/evidence-reviewer.md').read_text()
        for phrase in ('bounded-plan readiness gate', 'do not create findings that require',
                       'previous_evidence_review', 'finite blocking set',
                       'not exhaustive coverage of every adjacent subtopic'):
            self.assertIn(phrase, contract)
    def test_research_revision_carries_finite_prior_feedback(self):
        run=self.newrun('r1')
        review=accepted();review['verdict']='REVISE';review['checks']['completeness']=False
        review['findings']=[{'kind':'EVIDENCE','severity':'material','quote':'',
                            'explanation':'One load-bearing evidence gap remains.',
                            'repair':'Add or explicitly scope out that one gap.'}]
        run.submit(run.task('evidence-reviewer'),review,metadata(True))
        prepare(self.repo,'r2',self.brief,self.research,fixture=True,research_revision_of='r1')
        successor=Run(self.repo,'r2');task=successor.task('evidence-reviewer')
        self.assertEqual(task['inputs']['previous_evidence_review'],review)
        self.assertEqual(task['inputs']['previous_evidence_review_source']['source_run'],'r1')
        self.assertEqual(successor.manifest['research_revision_of'],'r1')
        self.assertTrue(successor.manifest['evidence_feedback_sha256'])
    def test_research_revision_of_accepted_review_is_rejected(self):
        run=self.newrun('r1')
        run.submit(run.task('evidence-reviewer'),accepted(),metadata(True))
        with self.assertRaises(FactoryError):
            prepare(self.repo,'r2',self.brief,self.research,fixture=True,research_revision_of='r1')
    def test_research_revision_feedback_is_immutable(self):
        run=self.newrun('r1')
        review=accepted();review['verdict']='BLOCKED';review['checks']['truth']=False
        review['findings']=[{'kind':'EVIDENCE','severity':'critical','quote':'',
                            'explanation':'Required evidence cannot currently support the brief.',
                            'repair':'Repair the finite blocking evidence set.'}]
        run.submit(run.task('evidence-reviewer'),review,metadata(True))
        prepare(self.repo,'r2',self.brief,self.research,fixture=True,research_revision_of='r1')
        p=self.repo/'runs/r2/inputs/evidence-feedback.json';p.write_text('{}')
        with self.assertRaises(FactoryError): Run(self.repo,'r2')
    def test_revision_rounds_carry_cumulative_history(self):
        run=self.newrun()
        run.submit(run.task('evidence-reviewer'),accepted(),metadata(True))
        revise=accepted();revise['verdict']='REVISE';revise['checks']['argument']=False
        revise['findings']=[{'kind':'JOB','severity':'material','quote':'',
                            'explanation':'A bounded repair is still needed.',
                            'repair':'Repair this specific issue without regressions.'}]
        run.submit(run.task('planner',round_no=1),self.plan,metadata())
        run.submit(run.task('plan-reviewer',round_no=1),revise,metadata(True))
        p2=run.task('planner',round_no=2)
        self.assertEqual([h['round'] for h in p2['inputs']['revision_history']],[1])
        self.assertEqual(p2['inputs']['feedback'],revise)
        run.submit(p2,self.plan,metadata())
        pr2=run.task('plan-reviewer',round_no=2)
        self.assertEqual([h['round'] for h in pr2['inputs']['revision_history']],[1])
        run.submit(pr2,revise,metadata(True))
        p3=run.task('planner',round_no=3)
        self.assertEqual([h['round'] for h in p3['inputs']['revision_history']],[1,2])

    def test_chapter_revision_rounds_carry_cumulative_history(self):
        run=self.newrun();self.to_plan(run)
        revise=accepted();revise['verdict']='REVISE';revise['checks']['argument']=False
        revise['findings']=[{'kind':'JOB','severity':'material','quote':'',
                            'explanation':'A bounded chapter repair is still needed.',
                            'repair':'Repair this issue and preserve prior fixes.'}]
        draft={'schema_version':2,'chapter_id':'chapter-01','text':'A bounded draft.','claim_map':[]}
        run.submit(run.task('writer',1,1),draft,metadata())
        run.submit(run.task('chapter-reviewer',1,1),revise,metadata(True))
        w2=run.task('writer',1,2)
        self.assertEqual([h['round'] for h in w2['inputs']['revision_history']],[1])
        run.submit(w2,draft,metadata())
        cr2=run.task('chapter-reviewer',1,2)
        self.assertEqual([h['round'] for h in cr2['inputs']['revision_history']],[1])
        run.submit(cr2,revise,metadata(True))
        w3=run.task('writer',1,3)
        self.assertEqual([h['round'] for h in w3['inputs']['revision_history']],[1,2])

    def test_revision_prompts_define_convergence_contract(self):
        checks={
            'prompts/master-plan-skill-v2.md':('revision_history','preserve earlier repairs'),
            'prompts/master-plan-reviewer-v2.md':('revision_history','do not reopen a repaired issue'),
            'prompts/chapter-writer.md':('revision_history','reintroducing an older one'),
            'prompts/chapter-reviewer.md':('revision_history','do not reopen a repaired issue'),
        }
        for rel,phrases in checks.items():
            text=(self.repo/rel).read_text()
            for phrase in phrases:self.assertIn(phrase,text)
    def test_same_family_evidence_reviewer_blocked(self):
        run=self.newrun()
        with self.assertRaises(FactoryError): run.submit(run.task('evidence-reviewer'),accepted(),metadata())
    def test_fabricated_fixture_metadata_cannot_be_live(self):
        run=self.newrun(fixture=False)
        with self.assertRaises(FactoryError): run.submit(run.task('evidence-reviewer'),accepted(),metadata(True))
    def test_missing_metadata_rejected(self):
        run=self.newrun()
        with self.assertRaises(FactoryError): run.submit(run.task('evidence-reviewer'),accepted(),{'model':'x'})
    def test_no_chapter_two_before_state_one(self):
        run=self.newrun();out=self.to_writer(run)
        run.submit(run.task('chapter-reviewer',1),accepted(),metadata())
        with self.assertRaises(FactoryError): run.task('writer',2)
    def test_failed_review_blocks_state(self):
        run=self.newrun();self.to_writer(run)
        r=accepted();r['verdict']='REVISE';r['checks']['argument']=False
        run.submit(run.task('chapter-reviewer',1),r,metadata())
        with self.assertRaises(FactoryError): run.task('state-editor',1)
    def test_cap_cannot_be_acceptance(self):
        run=self.newrun();self.to_plan(run)
        cap=run.config['max_rounds']
        for n in range(1,cap+1):
            task=run.task('writer',1,n)
            run.submit(task,{'schema_version':2,'chapter_id':'chapter-01','text':'A partial argument.','claim_map':[]},metadata())
            r=accepted();r['verdict']='REVISE';r['checks']['argument']=False
            run.submit(run.task('chapter-reviewer',1,n),r,metadata())
        with self.assertRaises(FactoryError): run.task('writer',1,cap+1)
        with self.assertRaises(FactoryError): run.accepted_chapter(1)
    def test_result_is_not_filename_cache(self):
        run=self.newrun();self.to_plan(run)
        p=run.root/'results/planner-r01.json';p.write_text('PASS')
        with self.assertRaises(FactoryError): run.task('writer',1)
    def test_stale_task_dependency_rejected(self):
        run=self.newrun();self.to_plan(run);task=run.task('writer',1)
        p=run.root/'results/plan-reviewer-r01.json';data=unseal(p);data['output']['verdict']='REVISE';data['output']['checks']['argument']=False;p.unlink();seal(p,data)
        with self.assertRaises(FactoryError): run.submit(task,{'schema_version':2,'chapter_id':'chapter-01','text':'Actual text','claim_map':[]},metadata())
    def test_full_pipeline_offline(self):
        run=self.newrun();result=finish(run,self.plan)
        self.assertEqual(result['status'],'COMPLETE_UNRELEASED')
        self.assertTrue(result['fixture'])
        self.assertEqual(result['efficacy'],'NOT_MEASURED')
    def test_post_audit_book_mutation_rejected(self):
        run=self.newrun();finish(run,self.plan);(run.root/'book.md').write_text('Different book')
        with self.assertRaises(FactoryError): run.complete()
    def test_missing_final_audit_not_complete(self):
        run=self.newrun();finish(run,self.plan);(run.root/'results/final-auditor-r01.json').unlink()
        self.assertEqual(run.status()['status'],'INCOMPLETE')
    def test_segregated_records_citable_only_for_bounded_exclusions(self):
        import copy
        research = copy.deepcopy(self.research)
        research["coverage"]["rejected_records"] = [{"id": "demo-rejected", "reason": "Fixture segregation."}]
        prepare(self.repo, "segrun", self.brief, research, fixture=True)
        run = Run(self.repo, "segrun")
        finish(run, self.plan)
        run.root.joinpath("results/final-auditor-r01.json").unlink()
        asm = run.assemble()["assembly"]
        base = {"quote": "One unsuccessful attempt is one observation.", "evidence_ids": ["demo-rejected"],
                "support": "bounded", "explanation": "Exclusion documented against the segregated record."}
        good = accepted()
        good["claim_checks"] = [base]
        good["screening_resolutions"] = {f["id"]: "Fixture triage." for f in asm["screening"]}
        run.submit(run.task("final-auditor"), good, metadata(True))
        self.assertEqual(run.complete()["status"], "COMPLETE_UNRELEASED")
        run.root.joinpath("results/final-auditor-r01.json").unlink()
        bad = accepted()
        bad["claim_checks"] = [dict(base, support="supported")]
        bad["screening_resolutions"] = dict(good["screening_resolutions"])
        with self.assertRaises(FactoryError):
            run.submit(run.task("final-auditor"), bad, metadata(True))
        run.root.joinpath("results/final-auditor-r01.json").unlink() if (run.root / "results/final-auditor-r01.json").exists() else None
        worse = accepted()
        worse["claim_checks"] = [dict(base, evidence_ids=["no-such-record"])]
        worse["screening_resolutions"] = dict(good["screening_resolutions"])
        with self.assertRaises(FactoryError):
            run.submit(run.task("final-auditor"), worse, metadata(True))
    def to_book_revise(self, run, quote="Body sentence 1.", edit_a=False):
        self.to_plan(run)
        for n, card in enumerate(self.plan["chapters"], 1):
            text = f"Body sentence {n}. Second sentence {n}."
            run.submit(run.task("writer", n),
                       {"schema_version": 2, "chapter_id": card["id"], "text": text, "claim_map": []}, metadata())
            run.submit(run.task("chapter-reviewer", n), accepted(), metadata())
            run.submit(run.task("state-editor", n),
                       {"schema_version": 2, "chapter_id": card["id"],
                        "established": [{"belief": card["supported_conclusion"], "quote": f"Body sentence {n}."}],
                        "unresolved": [card["remaining_objection"]], "used_examples": []}, metadata())
        if edit_a:
            ops = [{"op": "replace", "chapter": f"chapter-0{n}",
                    "old": f"Second sentence {n}.", "new": f"Edited second sentence {n}.",
                    "reason": "First assembly edit."} for n in (1, 2)]
            quote = "Edited second sentence 1."
        else:
            ops = []
        run.submit(run.task("book-editor"),
                   {"schema_version": 2, "operations": ops,
                    "explanation": "First assembly with real edit A." if edit_a else "First assembly; no edits."},
                   metadata())
        first = run.assemble()
        audit = accepted(); audit["verdict"] = "REVISE"; audit["checks"]["continuity"] = False
        audit["findings"] = [{"kind": "EVIDENCE", "severity": "material", "quote": quote,
                              "explanation": "Needs a bounded revision.", "repair": "Revise in place."}]
        audit["claim_checks"] = [{"quote": quote, "evidence_ids": [], "support": "nonempirical",
                                  "explanation": "Fixture sentence."}]
        audit["screening_resolutions"] = {f["id"]: "Fixture triage." for f in first["assembly"]["screening"]}
        run.submit(run.task("final-auditor"), audit, metadata(True))
        return first
    def test_final_audit_revise_converges_in_run(self):
        run = self.newrun()
        first = self.to_book_revise(run, edit_a=True)
        self.assertEqual(run.status()["status"], "INCOMPLETE")
        editor_task = run.task("book-editor", round_no=2)
        self.assertEqual(editor_task["inputs"]["audit_history"][0]["audit"]["verdict"], "REVISE")
        self.assertEqual(editor_task["inputs"]["previous_assembly"]["text"], first["assembly"]["text"])
        v1bytes = (run.root / "assembly/assembly-r01.json").read_bytes()
        # Anchors for r02 bind to the previous assembly (which contains edit A),
        # not the accepted originals: an anchor spanning text edit A removed fails.
        with self.assertRaises(FactoryError):
            run.submit(editor_task, {"schema_version": 2, "operations": [
                {"op": "replace", "chapter": "chapter-01", "old": "Body sentence 1. Second sentence 1.",
                 "new": "Broken anchor.", "reason": "Stale anchor test."}],
                "explanation": "Must fail validation."}, metadata())
        run.submit(editor_task, {"schema_version": 2, "operations": [
            {"op": "replace", "chapter": "chapter-01", "old": "Edited second sentence 1.",
             "new": "Twice revised sentence 1.", "reason": "Audit repair."}],
            "explanation": "One justified whole-book fix on top of edit A."}, metadata())
        second = run.assemble()
        self.assertEqual((run.root / "assembly/assembly-r01.json").read_bytes(), v1bytes)
        self.assertIn("Edited second sentence 2.", second["assembly"]["text"])
        self.assertIn("Twice revised sentence 1.", second["assembly"]["text"])
        self.assertNotIn("Edited second sentence 1.", second["assembly"]["text"])
        self.assertEqual((run.root / "book.md").read_text(), second["assembly"]["text"])
        auditor_task = run.task("final-auditor", round_no=2)
        self.assertEqual(len(auditor_task["inputs"]["audit_history"]), 1)
        self.assertIn("Twice revised sentence 1.", auditor_task["inputs"]["assembled_book"])
        final = accepted()
        final["claim_checks"] = [{"quote": "Twice revised sentence 1.", "evidence_ids": [],
                                  "support": "nonempirical", "explanation": "Fixture sentence."}]
        final["screening_resolutions"] = {f["id"]: "Fixture triage." for f in second["assembly"]["screening"]}
        run.submit(auditor_task, final, metadata(True))
        result = run.complete()
        self.assertEqual(result["status"], "COMPLETE_UNRELEASED")
        self.assertEqual(result["book_sha256"], second["assembly"]["text_sha256"])
    def test_audit_blocked_stops_whole_book_revision(self):
        run = self.newrun()
        self.to_book_revise(run)
        (run.root / "results/final-auditor-r01.json").unlink()
        audit = accepted(); audit["verdict"] = "BLOCKED"; audit["checks"]["truth"] = False
        audit["findings"] = [{"kind": "SAFETY", "severity": "critical", "quote": "",
                              "explanation": "Unfixable by editing.", "repair": "New run upstream."}]
        audit["claim_checks"] = [{"quote": "Body sentence 1.", "evidence_ids": [],
                                  "support": "nonempirical", "explanation": "Fixture."}]
        first = run.assemble()
        audit["screening_resolutions"] = {f["id"]: "Fixture triage." for f in first["assembly"]["screening"]}
        run.submit(run.task("final-auditor"), audit, metadata(True))
        with self.assertRaises(FactoryError):
            run.task("book-editor", round_no=2)
        self.assertEqual(run.status()["status"], "INCOMPLETE")
    def test_unaudited_edits_cannot_complete(self):
        run = self.newrun()
        self.to_book_revise(run)
        run.submit(run.task("book-editor", round_no=2),
                   {"schema_version": 2, "operations": [], "explanation": "No-op second edit."}, metadata())
        run.assemble()
        with self.assertRaises(FactoryError):
            run.complete()
    def test_revision_preserves_frozen_artifacts(self):
        run = self.newrun()
        first = self.to_book_revise(run)
        before = {str(p.relative_to(run.root)): file_hash(p)
                  for p in list((run.root / "inputs").glob("*.json")) + list((run.root / "results").glob("*.json"))}
        chapter_texts = {n: run.result("writer", n)["output"]["text"] for n in (1, 2)}
        run.submit(run.task("book-editor", round_no=2),
                   {"schema_version": 2, "operations": [
                       {"op": "replace", "chapter": "chapter-01", "old": "Body sentence 1.",
                        "new": "Revised body sentence 1.", "reason": "Audit repair."}],
                    "explanation": "One fix."}, metadata())
        run.assemble()
        after = {k: file_hash(run.root / k) for k in before}
        self.assertEqual(before, after)
        for n in (1, 2):
            self.assertEqual(run.result("writer", n)["output"]["text"], chapter_texts[n])
        self.assertEqual(first["assembly"]["text_sha256"],
                         run.assembly_version(1)["assembly"]["text_sha256"])
    def test_whole_book_round_cap(self):
        run = self.newrun()
        with self.assertRaises(FactoryError):
            run.key("book-editor", None, run.config["max_rounds"] + 1)
        with self.assertRaises(FactoryError):
            run.key("final-auditor", None, run.config["max_rounds"] + 1)
    def test_wrapper_screen_flags_universals(self):
        from bc_factory.quality import screen_wrappers
        flags = screen_wrappers({"title": "Quit Smoking", "safety": "Relapse is common and expected."},
                                ["A Calm Start", "Never Again"])
        kinds = {(f["id"], f["kind"]) for f in flags}
        self.assertTrue(any(k == "wrapper_universal" for _, k in kinds))
        self.assertEqual(len(flags), 2)
        clean = screen_wrappers({"title": "Quit Smoking", "safety": "Talk to your clinician."},
                                ["A Calm Start"])
        self.assertEqual(clean, [])
    def test_wrapper_flags_enter_assembly_screening(self):
        run = self.newrun()
        self.to_book_revise(run)
        asm = run.assembly_version(1)["assembly"]
        self.assertTrue(all("id" in f for f in asm["screening"]))
    def test_assembly_recomputation_drift_fails_closed(self):
        run = self.newrun()
        self.to_book_revise(run)
        before = (run.root / "assembly/assembly-r01.json").read_bytes()
        book_before = (run.root / "book.md").read_bytes()
        with patch("bc_factory.runs.assemble_book", return_value="drifted text\n"):
            with self.assertRaises(FactoryError):
                run.assemble()
        self.assertEqual((run.root / "assembly/assembly-r01.json").read_bytes(), before)
        self.assertEqual((run.root / "book.md").read_bytes(), book_before)
    def front_revise(self, run, quote="Examine what one unsuccessful attempt can logically establish"):
        return self.to_book_revise(run, quote=quote)
    def test_retitle_repairs_rendered_header(self):
        run = self.newrun()
        self.to_book_revise(run)
        run.submit(run.task("book-editor", round_no=2), {"schema_version": 2, "operations": [
            {"op": "retitle", "chapter": "chapter-01", "title": "Repaired Header",
             "reason": "Audit repair."}],
            "explanation": "Header fix."}, metadata())
        second = run.assemble()
        self.assertIn("## 1. Repaired Header", second["assembly"]["text"])
        self.assertNotIn("## 1. What follows", second["assembly"]["text"])
        v1 = unseal(run.root / "assembly/assembly-r01.json")
        self.assertIn("## 1. What follows", v1["text"])
        with self.assertRaises(FactoryError):
            run.submit(run.task("book-editor", round_no=3), {"schema_version": 2, "operations": [
                {"op": "retitle", "chapter": "chapter-99", "title": "Nope",
                 "reason": "Bad chapter."}], "explanation": "Must fail."}, metadata())
        with self.assertRaises(FactoryError):
            run.submit(run.task("book-editor", round_no=3), {"schema_version": 2, "operations": [
                {"op": "retitle", "chapter": "chapter-01", "title": "   ",
                 "reason": "Empty title."}], "explanation": "Must fail."}, metadata())
    def test_notes_repairs_converge_in_lineage(self):
        import copy
        research = copy.deepcopy(self.research)
        extra = copy.deepcopy(research['sources'][0])
        extra['id'] = 'demo-second'
        research['sources'].append(extra)
        prepare(self.repo, 'notesrun', self.brief, research, fixture=True)
        run = Run(self.repo, 'notesrun')
        self.to_book_revise(run)
        first = run.assembly_version(1)["assembly"]
        self.assertEqual(len(first["source_notes"]), 2)
        # Relabel one note and remove another; removal needs the full note text.
        second_body = first["source_notes"][1]["body"]
        run.submit(run.task("book-editor", round_no=2), {"schema_version": 2, "operations": [
            {"op": "notes", "id": first["source_notes"][0]["id"], "old": "synthetic",
             "new": "test-only", "reason": "Audit repair."},
            {"op": "notes", "id": "demo-second", "old": second_body, "new": "",
             "reason": "Unused note."}],
            "explanation": "Note fixes."}, metadata())
        second = run.assemble()
        self.assertIn("test-only", second["assembly"]["text"])
        self.assertNotIn("synthetic", second["assembly"]["text"].split("## Source notes")[1])
        self.assertEqual(len(second["assembly"]["source_notes"]), 1)
        self.assertEqual(len(second["assembly"]["source_note_repairs"]), 2)
        v1bytes = (run.root / "assembly/assembly-r01.json").read_bytes()
        # A later chapter-only round preserves the note repairs cumulatively.
        revise = accepted(); revise["verdict"] = "REVISE"; revise["checks"]["continuity"] = False
        revise["findings"] = [{"kind": "EVIDENCE", "severity": "material", "quote": "Body sentence 2.",
                               "explanation": "Needs a bounded fix.", "repair": "Fix in place."}]
        revise["claim_checks"] = [{"quote": "Body sentence 2.", "evidence_ids": [],
                                   "support": "nonempirical", "explanation": "Fixture."}]
        revise["screening_resolutions"] = {f["id"]: "Fixture triage." for f in second["assembly"]["screening"]}
        run.submit(run.task("final-auditor", round_no=2), revise, metadata(True))
        run.submit(run.task("book-editor", round_no=3), {"schema_version": 2, "operations": [
            {"op": "replace", "chapter": "chapter-01", "old": "Body sentence 1.",
             "new": "Edited body sentence 1.", "reason": "Later fix."}],
            "explanation": "Chapter fix."}, metadata())
        third = run.assemble()
        self.assertIn("test-only", third["assembly"]["text"])
        self.assertEqual(len(third["assembly"]["source_notes"]), 1)
        self.assertEqual((run.root / "assembly/assembly-r01.json").read_bytes(), v1bytes)
        # Unknown ids, partial-removal anchors and last-note removal fail closed.
        revise3 = accepted(); revise3["verdict"] = "REVISE"; revise3["checks"]["continuity"] = False
        revise3["findings"] = [{"kind": "EVIDENCE", "severity": "material", "quote": "Edited body sentence 1.",
                                "explanation": "Needs more.", "repair": "Fix again."}]
        revise3["claim_checks"] = [{"quote": "Edited body sentence 1.", "evidence_ids": [],
                                    "support": "nonempirical", "explanation": "Fixture."}]
        revise3["screening_resolutions"] = {f["id"]: "Fixture triage." for f in third["assembly"]["screening"]}
        run.submit(run.task("final-auditor", round_no=3), revise3, metadata(True))
        with self.assertRaises(FactoryError):
            run.submit(run.task("book-editor", round_no=4), {"schema_version": 2, "operations": [
                {"op": "notes", "id": "no-such-note", "old": "x", "new": "y",
                 "reason": "Bad id."}], "explanation": "Must fail."}, metadata())
        with self.assertRaises(FactoryError):
            run.submit(run.task("book-editor", round_no=4), {"schema_version": 2, "operations": [
                {"op": "notes", "id": "demo-illustration", "old": "test",
                 "new": "", "reason": "Partial removal."}], "explanation": "Must fail."}, metadata())
    def test_front_matter_repair_converges_in_lineage(self):
        run = self.newrun()
        first = self.front_revise(run)
        goal = self.brief["reader_goal"]
        editor_task = run.task("book-editor", round_no=2)
        self.assertIn(goal, editor_task["inputs"]["previous_assembly"]["text"])
        run.submit(editor_task, {"schema_version": 2, "operations": [
            {"op": "front", "field": "reader_goal", "old": goal,
             "new": "Examine what one unsuccessful attempt can logically establish, and nothing more.",
             "reason": "Audit repair."}],
            "explanation": "Narrow the overclaiming promise."}, metadata())
        second = run.assemble()
        self.assertIn("and nothing more.", second["assembly"]["text"])
        v1text = unseal(run.root / "assembly/assembly-r01.json")["text"]
        self.assertEqual(v1text, first["assembly"]["text"])
        self.assertEqual(second["assembly"]["front_matter_repairs"][0]["field"], "reader_goal")
        auditor_task = run.task("final-auditor", round_no=2)
        final = accepted()
        final["claim_checks"] = [{"quote": "Body sentence 1.", "evidence_ids": [],
                                  "support": "nonempirical", "explanation": "Fixture."}]
        final["screening_resolutions"] = {f["id"]: "Fixture triage." for f in second["assembly"]["screening"]}
        run.submit(auditor_task, final, metadata(True))
        result = run.complete()
        self.assertEqual(result["status"], "COMPLETE_UNRELEASED")
        self.assertIn("and nothing more.", (run.root / "book.md").read_text())
    def test_front_repair_survives_later_round(self):
        run = self.newrun()
        self.front_revise(run)
        run.submit(run.task("book-editor", round_no=2), {"schema_version": 2, "operations": [
            {"op": "front", "field": "reader_goal", "old": self.brief["reader_goal"],
             "new": "Narrowed promise.", "reason": "Audit repair."}],
            "explanation": "Front repair."}, metadata())
        mid = run.assemble()
        second_audit = accepted(); second_audit["verdict"] = "REVISE"; second_audit["checks"]["continuity"] = False
        second_audit["findings"] = [{"kind": "EVIDENCE", "severity": "material",
                                     "quote": "Body sentence 2.",
                                     "explanation": "Chapter needs a bounded fix.", "repair": "Fix in place."}]
        second_audit["claim_checks"] = [{"quote": "Body sentence 2.", "evidence_ids": [],
                                         "support": "nonempirical", "explanation": "Fixture."}]
        second_audit["screening_resolutions"] = {f["id"]: "Fixture triage." for f in mid["assembly"]["screening"]}
        run.submit(run.task("final-auditor", round_no=2), second_audit, metadata(True))
        run.submit(run.task("book-editor", round_no=3), {"schema_version": 2, "operations": [
            {"op": "replace", "chapter": "chapter-02", "old": "Body sentence 2.",
             "new": "Edited body sentence 2.", "reason": "Later fix."}],
            "explanation": "Chapter fix."}, metadata())
        third = run.assemble()
        self.assertIn("Narrowed promise.", third["assembly"]["text"])
        self.assertIn("Edited body sentence 2.", third["assembly"]["text"])
        self.assertEqual(len(third["assembly"]["front_matter_repairs"]), 1)
    def test_safety_front_matter_cannot_be_deleted(self):
        run = self.newrun()
        self.front_revise(run)
        task = run.task("book-editor", round_no=2)
        for bad in ("", "   "):
            with self.assertRaises(FactoryError):
                run.submit(task, {"schema_version": 2, "operations": [
                    {"op": "front", "field": "safety", "old": "", "new": bad,
                     "reason": "Deletion attempt."}], "explanation": "Must fail."}, metadata())
        with self.assertRaises(FactoryError):
            run.submit(task, {"schema_version": 2, "operations": [
                {"op": "front", "field": "subtitle", "old": "x", "new": "y",
                 "reason": "Unknown field."}], "explanation": "Must fail."}, metadata())
        with self.assertRaises(FactoryError):
            run.submit(task, {"schema_version": 2, "operations": [
                {"op": "front", "field": "reader_goal", "old": "wrong anchor",
                 "new": "Narrowed promise.", "reason": "Stale anchor."}], "explanation": "Must fail."}, metadata())
    def test_remediation_continues_frozen_run(self):
        src = self.newrun("src1")
        first = self.front_revise(src)
        src_files = {}
        for dp, _, fns in os.walk(src.root):
            for f in fns:
                p = Path(dp) / f
                src_files[str(p.relative_to(src.root))] = file_hash(p)
        with patch("bc_factory.research_access.validate_coverage"):
            prepare(self.repo, "rem1", self.brief, self.research,
                    fixture=True, remediation_of="src1")
        rem = Run(self.repo, "rem1")
        self.assertEqual(rem.manifest["remediation_of"], "src1")
        self.assertEqual(rem.manifest["remediation_source"]["source_assembly_sha256"],
                         file_hash(src.root / "assembly/assembly-r01.json"))
        # Upstream stages are inherited, never replayed.
        for role in ("evidence-reviewer", "planner", "writer"):
            with self.assertRaises(FactoryError):
                rem.task(role, 1 if role == "writer" else None)
        goal = self.brief["reader_goal"]
        rem.submit(rem.task("book-editor", round_no=2), {"schema_version": 2, "operations": [
            {"op": "front", "field": "reader_goal", "old": goal,
             "new": "Remediated promise.", "reason": "Audit repair."}],
            "explanation": "Front repair in remediation."}, metadata())
        second = rem.assemble()
        self.assertIn("Remediated promise.", second["assembly"]["text"])
        good = accepted()
        good["claim_checks"] = [{"quote": "Body sentence 1.", "evidence_ids": [],
                                 "support": "nonempirical", "explanation": "Fixture."}]
        good["screening_resolutions"] = {f["id"]: "Fixture triage." for f in second["assembly"]["screening"]}
        rem.submit(rem.task("final-auditor", round_no=2), good, metadata(True))
        result = rem.complete()
        self.assertEqual(result["status"], "COMPLETE_UNRELEASED")
        self.assertNotEqual(result["book_sha256"], first["assembly"]["text_sha256"])
        self.assertEqual(rem.accepted_assembly()["assembly"]["assembly_round"], 2)
        self.assertTrue(str(rem.accepted_audit_file()).endswith("final-auditor-r02.json"))
        # Source historical bytes are unchanged.
        for rel, h in src_files.items():
            self.assertEqual(file_hash(src.root / rel), h, rel)
        self.assertEqual(rem.manifest["brief_sha256"], src.manifest["brief_sha256"])
        self.assertEqual(rem.manifest["research_sha256"], src.manifest["research_sha256"])
    def test_live_production_plan_not_used(self):
        run=self.newrun();self.to_plan(run)
        p=self.repo/'production-books/practice-belief/master-plan.md';p.parent.mkdir(parents=True);p.write_text('Wrong mutable legacy plan')
        self.assertEqual(run.task('writer',1)['inputs']['plan'],self.plan)

class EditingAndProviderTests(Base):
    def test_capitalization_regression_detected(self):
        flags=screen(('This is BAD SUGAR and BAD SUGAR again. '*100))
        self.assertTrue(any(f['kind']=='capital_density' for f in flags))
    def test_authority_screen(self):
        self.assertTrue(any(f['kind']=='authority' for f in screen('I have treated hundreds of clients.')))
    def test_overlap_is_only_review_queue(self):
        t='one two three four five six seven eight nine ten eleven twelve thirteen'
        self.assertTrue(overlap_screen(t,{'reference':t})[0]['requires_review'])
    def test_editor_unique_anchor(self):
        c=[{'id':'chapter-01','title':'x','text':'same same','source_chapters':['chapter-01'],'claim_map':[]}]
        r={'schema_version':2,'operations':[{'op':'replace','chapter':'chapter-01','old':'same','new':'new','reason':'test'}],'explanation':'test'}
        with self.assertRaises(FactoryError): edit_book(c,r)
    def test_editor_cannot_delete_all(self):
        c=[{'id':'chapter-01','title':'x','text':'x','source_chapters':['chapter-01'],'claim_map':[]}]
        with self.assertRaises(FactoryError): edit_book(c,{'schema_version':2,'operations':[{'op':'remove','chapter':'chapter-01','reason':'test'}],'explanation':'test'})
    def test_safety_and_source_notes_assembled(self):
        b=copy.deepcopy(self.brief);b['risk_level']='health';b['safety_advisory']='IMPORTANT TEST ADVISORY'
        text=assemble_book(b,self.research,self.plan,[{'title':'Chapter','text':'Actual text'}])
        self.assertLess(text.index('IMPORTANT TEST ADVISORY'),text.index('Actual text'))
        self.assertIn('Source notes',text)
    def test_source_notes_are_reader_facing(self):
        b=copy.deepcopy(self.brief)
        r=copy.deepcopy(self.research)
        r['sources'][0]['locator']='Example review (abstract via example; envelope test-capture.json; ledger test-ledger.json)'
        text=assemble_book(b,r,self.plan,[{'title':'Chapter','text':'Actual text'}])
        notes=text[text.index('Source notes'):]
        self.assertNotIn(r['sources'][0]['id'],notes)
        self.assertNotIn('.json',notes)
        self.assertIn('abstract via example',notes)
    def test_no_paid_call_without_flag(self):
        with patch('urllib.request.urlopen') as call:
            with self.assertRaises(FactoryError): execute({'role':'writer'},read_json(self.repo/'factory/config.json'))
            call.assert_not_called()
    def test_external_profile_missing_fails_before_spend(self):
        with patch('urllib.request.urlopen') as call:
            with self.assertRaises(FactoryError): execute({'role':'final-auditor'},read_json(self.repo/'factory/config.json'),True)
            call.assert_not_called()
    def test_truncated_chat_rejected(self):
        with self.assertRaises(FactoryError): extract({'choices':[{'finish_reason':'length','message':{'content':'partial'}}]},'chat')
    def test_incomplete_responses_rejected(self):
        with self.assertRaises(FactoryError): extract({'status':'incomplete','output_text':'partial'},'responses')
    def test_refused_response_rejected(self):
        with self.assertRaises(FactoryError): extract({'status':'completed','output':[{'content':[{'type':'refusal','refusal':'no'}]}]},'responses')
    def test_complete_response_extracted(self):
        self.assertEqual(extract({'status':'completed','output_text':'{"ok":true}'},'responses'),'{"ok":true}')
    def test_archive_excludes_credentials(self):
        (self.repo/'.env').write_text('DO_NOT_EXPORT=synthetic-test-value')
        (self.repo/'.env.example').write_text('KEY=')
        out=Path(self.tmp.name)/'full.zip';s=build(self.repo,out)
        with zipfile.ZipFile(out) as z:
            self.assertNotIn('Belief-changer/.env',z.namelist())
            self.assertIn('Belief-changer/.env.example',z.namelist())
            self.assertIn('Belief-changer/ARCHIVE-MANIFEST.json',z.namelist())
            self.assertIsNone(z.testzip())
            self.assertTrue(all(info.date_time == (2026,9,11,0,0,0) for info in z.infolist()))
        self.assertEqual(s['sha256'],file_hash(out))
    def test_archive_internal_symlink_materialized(self):
        (self.repo/'target.md').write_text('Safe retained reference alias.')
        (self.repo/'alias.md').symlink_to('target.md')
        out=Path(self.tmp.name)/'internal.zip';build(self.repo,out)
        with zipfile.ZipFile(out) as z:
            self.assertEqual(z.read('Belief-changer/alias.md'),b'Safe retained reference alias.')
            manifest=json.loads(z.read('Belief-changer/ARCHIVE-MANIFEST.json'))
            self.assertEqual(manifest['dereferenced_symlinks'],{'alias.md':'target.md'})
    def test_archive_external_symlink_rejected(self):
        outside=Path(self.tmp.name)/'private.txt';outside.write_text('Never export outside tree')
        (self.repo/'alias.txt').symlink_to(outside)
        with self.assertRaises(FactoryError): build(self.repo,Path(self.tmp.name)/'external.zip')
    def test_archive_credential_alias_rejected(self):
        (self.repo/'.env').write_text('Never export credentials')
        (self.repo/'alias.txt').symlink_to('.env')
        with self.assertRaises(FactoryError): build(self.repo,Path(self.tmp.name)/'credential.zip')
    def test_archive_directory_symlink_rejected(self):
        (self.repo/'alias').symlink_to('scripts',target_is_directory=True)
        with self.assertRaises(FactoryError): build(self.repo,Path(self.tmp.name)/'directory.zip')
    def test_archive_broken_symlink_rejected(self):
        (self.repo/'alias.txt').symlink_to('missing-file.txt')
        with self.assertRaises(FactoryError): build(self.repo,Path(self.tmp.name)/'broken.zip')
    def test_archive_reproducible(self):
        a=Path(self.tmp.name)/'a.zip';b=Path(self.tmp.name)/'b.zip'
        self.assertEqual(build(self.repo,a)['sha256'],build(self.repo,b)['sha256'])

class ExperimentTests(Base):
    _finished_cache = None
    @classmethod
    def tearDownClass(cls):
        if cls._finished_cache is not None:
            cls._finished_cache.cleanup()

    def setup_experiment(self, finished=False):
        if finished and type(self)._finished_cache is not None:
            shutil.copytree(Path(type(self)._finished_cache.name)/"repo", self.repo, dirs_exist_ok=True)
            return unseal(self.repo/"experiments/exp1/registration.json")["spec"]
        pairs=[]
        for subject in ('s1','s2'):
            self.brief,self.research,self.plan=inputs(subject)
            for n in range(3):
                for arm in ('p','c'):
                    r=self.newrun(f'{subject}-{arm}{n}')
                    if finished: finish(r,self.plan)
                pairs.append({'id':f'{subject}-{n}','subject':subject,'parent_run':f'{subject}-p{n}','candidate_run':f'{subject}-c{n}'})
        spec={'schema_version':2,'id':'exp1','parent_release':None,'hypothesis':'Controlled fixture-only comparison','primary_dimension':'argument',
              'allowed_change_paths':['prompts/chapter-writer.md'],'subjects':['s1','s2'],'samples_per_subject':3,'pairs':pairs,'freeze_plan':True,'confirmatory':not finished}
        register(self.repo,spec)
        if finished:
            type(self)._finished_cache = tempfile.TemporaryDirectory()
            shutil.copytree(self.repo, Path(type(self)._finished_cache.name)/'repo')
        return spec
    def pair_report(self,task,order,regress=False):
        candidate='B' if order=='AB' else 'A'
        prefs={d:{'winner':candidate if d=='argument' else 'tie','a_quote':'One unsuccessful attempt is one observation.',
                  'b_quote':'One unsuccessful attempt is one observation.','reason':'Fixture comparison only'} for d in DIMENSIONS}
        if regress: prefs['voice']['winner']='A' if candidate=='B' else 'B'
        return {'schema_version':2,'preferences':prefs,'critical':{'A':[],'B':[]}}
    def test_zero_judgments_not_panel_done(self):
        self.setup_experiment()
        self.assertEqual(decide(self.repo,'exp1')['decision'],'INCONCLUSIVE')
        self.assertEqual(len(decide(self.repo,'exp1')['missing']),12)
        transfer=transfer_decide(self.repo,'exp1')
        self.assertEqual(transfer['decision'],'INCONCLUSIVE')
        self.assertEqual(len(transfer['missing']),12)
        self.assertEqual(transfer['judge_models'],[])
    def test_research_process_intervention_must_be_preregistered(self):
        pairs=[]
        for subject in ('rs1','rs2'):
            brief,research,plan=inputs(subject)
            for n in range(3):
                prepare(self.repo,f'{subject}-p{n}',brief,research,fixture=True)
                changed=copy.deepcopy(research)
                changed['open_questions']=list(changed['open_questions'])+[f'candidate research question {n}']
                prepare(self.repo,f'{subject}-c{n}',brief,changed,fixture=True)
                pairs.append({'id':f'{subject}-{n}','subject':subject,
                              'parent_run':f'{subject}-p{n}','candidate_run':f'{subject}-c{n}'})
        spec={'schema_version':2,'id':'research-open','parent_release':None,
              'hypothesis':'Research-process intervention fixture','primary_dimension':'argument',
              'allowed_change_paths':['prompts/research-agent.md'],'subjects':['rs1','rs2'],
              'samples_per_subject':3,'pairs':pairs,'freeze_plan':False,
              'freeze_research':False,'confirmatory':True}
        register(self.repo,spec)
        strict=copy.deepcopy(spec);strict['id']='research-frozen';strict['freeze_research']=True
        with self.assertRaises(FactoryError): register(self.repo,strict)

    def test_register_rejects_fixture_live_trust_confound(self):
        spec=self.setup_experiment()
        candidate=self.repo/'runs/s1-c0/manifest.json'
        manifest=unseal(candidate)
        candidate.unlink()
        manifest['fixture']=False
        seal(candidate,manifest)
        spec['id']='trust-confound'
        with self.assertRaises(FactoryError): register(self.repo,spec)

    def test_register_rejects_inherited_learning_confound_even_when_research_may_differ(self):
        pairs=[]
        manifests={}
        for subject in ('la','lb'):
            for n in range(3):
                for arm in ('p','c'):
                    rid=f'{subject}-{arm}{n}'
                    files={'prompts/chapter-writer.md':'a' if arm=='p' else 'b'}
                    manifests[rid]={'run_id':rid,'subject':subject,'parent':None,'fixture':False,
                                    'brief_sha256':'1'*64,'research_sha256':('2' if arm=='p' else '3')*64,
                                    'learning_from':None if arm=='p' else 'other-baseline',
                                    'learning_sha256':None if arm=='p' else '4'*64,
                                    'factory_files':files,'factory_digest':digest(files)}
                pairs.append({'id':f'{subject}-{n}','subject':subject,
                              'parent_run':f'{subject}-p{n}','candidate_run':f'{subject}-c{n}'})
        class FakeRun:
            def __init__(self, _repo, rid): self.manifest=manifests[rid]
        spec={'schema_version':2,'id':'learning-confound','parent_release':None,
              'hypothesis':'Reject inherited-learning confound','primary_dimension':'argument',
              'allowed_change_paths':['prompts/chapter-writer.md'],'subjects':['la','lb'],
              'samples_per_subject':3,'pairs':pairs,'freeze_plan':False,
              'freeze_research':False,'confirmatory':False}
        with patch('bc_factory.experiments.Run',side_effect=FakeRun):
            with self.assertRaises(FactoryError): register(self.repo,spec)

    def test_register_reused_book_as_replicate_rejected(self):
        spec=self.setup_experiment();spec['id']='exp2';spec['pairs'][1]['parent_run']=spec['pairs'][0]['parent_run']
        with self.assertRaises(FactoryError): register(self.repo,spec)
    def test_confirmatory_cannot_be_posthoc(self):
        spec=self.setup_experiment(True);spec['id']='exp2';spec['confirmatory']=True
        with self.assertRaises(FactoryError): register(self.repo,spec)
    def test_pair_task_is_blinded(self):
        spec=self.setup_experiment(True);t=pair_task(self.repo,'exp1','s1-0','AB')
        self.assertNotIn('s1-p0',json.dumps(t));self.assertNotIn('s1-c0',json.dumps(t));self.assertNotIn('parent_run',json.dumps(t))
    def test_same_family_pair_judge_rejected(self):
        self.setup_experiment(True);t=pair_task(self.repo,'exp1','s1-0','AB')
        with self.assertRaises(FactoryError): submit_pair(self.repo,'exp1','s1-0','AB',self.pair_report(t,'AB'),metadata())
    def test_one_subject_regression_blocks(self):
        spec=self.setup_experiment(True)
        for pair in spec['pairs']:
            for order in ('AB','BA'):
                t=pair_task(self.repo,'exp1',pair['id'],order)
                submit_pair(self.repo,'exp1',pair['id'],order,self.pair_report(t,order,regress=pair['id']=='s1-0'),metadata(True))
        d=decide(self.repo,'exp1')
        self.assertEqual(d['decision'],'REJECT')
        self.assertEqual(d['subjects']['s1']['n_generation_pairs'],3) # NOT 6 label orders
    def test_fixture_never_promotes(self):
        self.setup_experiment()
        before=read_json(self.repo/'factory/champion.json')
        with self.assertRaises(FactoryError): promote(self.repo,'exp1','release1',{}, {})
        self.assertEqual(read_json(self.repo/'factory/champion.json'),before)
    def test_instrument_change_after_registration_rejected(self):
        self.setup_experiment()
        p=self.repo/'loop/judges/pairwise.md';p.write_text(p.read_text()+'Changed rubric.')
        with self.assertRaises(FactoryError): decide(self.repo,'exp1')
    def test_champion_remains_when_approval_fails(self):
        self.setup_experiment()
        before=file_hash(self.repo/'factory/champion.json')
        with patch('bc_factory.experiments.decide',return_value={'decision':'KEEP_ELIGIBLE'}):
            with self.assertRaises(FactoryError): promote(self.repo,'exp1','bad-approval',{}, {})
        self.assertEqual(file_hash(self.repo/'factory/champion.json'),before)
    def test_pair_task_binds_latest_accepted_audit(self):
        runs = {}
        for subject in ('s1', 's2'):
            self.brief, self.research, self.plan = inputs(subject)
            for n in range(3):
                for arm in ('p', 'c'):
                    r = self.newrun(f'{subject}-{arm}{n}')
                    runs[f'{subject}-{arm}{n}'] = r
                    if not (subject == 's1' and arm == 'c' and n == 0):
                        finish(r, self.plan)
        cand = runs['s1-c0']
        self.brief, self.research, self.plan = inputs('s1')
        self.to_plan(cand)
        for n, card in enumerate(self.plan["chapters"], 1):
            text = f"Body sentence {n}. Second sentence {n}."
            cand.submit(cand.task("writer", n),
                        {"schema_version": 2, "chapter_id": card["id"], "text": text, "claim_map": []}, metadata())
            cand.submit(cand.task("chapter-reviewer", n), accepted(), metadata())
            cand.submit(cand.task("state-editor", n),
                        {"schema_version": 2, "chapter_id": card["id"],
                         "established": [{"belief": card["supported_conclusion"], "quote": f"Body sentence {n}."}],
                         "unresolved": [card["remaining_objection"]], "used_examples": []}, metadata())
        cand.submit(cand.task("book-editor"),
                    {"schema_version": 2, "operations": [], "explanation": "First assembly."}, metadata())
        v1 = cand.assemble()
        bad = accepted(); bad["verdict"] = "REVISE"; bad["checks"]["continuity"] = False
        bad["findings"] = [{"kind": "EVIDENCE", "severity": "material", "quote": "Body sentence 1.",
                            "explanation": "Needs revision.", "repair": "Revise."}]
        bad["claim_checks"] = [{"quote": "Body sentence 1.", "evidence_ids": [],
                                "support": "nonempirical", "explanation": "Fixture."}]
        bad["screening_resolutions"] = {f["id"]: "Fixture triage." for f in v1["assembly"]["screening"]}
        cand.submit(cand.task("final-auditor"), bad, metadata(True))
        cand.submit(cand.task("book-editor", round_no=2),
                    {"schema_version": 2, "operations": [
                        {"op": "replace", "chapter": "chapter-01", "old": "Body sentence 1.",
                         "new": "Fixed sentence 1.", "reason": "Audit repair."}],
                     "explanation": "Audit repair."}, metadata())
        v2 = cand.assemble()
        good = accepted()
        good["claim_checks"] = [{"quote": "Fixed sentence 1.", "evidence_ids": [],
                                 "support": "nonempirical", "explanation": "Fixture."}]
        good["screening_resolutions"] = {f["id"]: "Fixture triage." for f in v2["assembly"]["screening"]}
        cand.submit(cand.task("final-auditor", round_no=2), good, metadata(True))
        self.assertEqual(cand.complete()["status"], "COMPLETE_UNRELEASED")
        pairs = [{'id': f'{subject}-{n}', 'subject': subject,
                  'parent_run': f'{subject}-p{n}', 'candidate_run': f'{subject}-c{n}'}
                 for subject in ('s1', 's2') for n in range(3)]
        spec = {'schema_version': 2, 'id': 'expB', 'parent_release': None,
                'hypothesis': 'Late-audit binding fixture', 'primary_dimension': 'argument',
                'allowed_change_paths': ['prompts/chapter-writer.md'], 'subjects': ['s1', 's2'],
                'samples_per_subject': 3, 'pairs': pairs,
                'freeze_plan': True, 'confirmatory': False}
        register(self.repo, spec)
        pair_task(self.repo, 'expB', 's1-0', 'AB')
        rec = unseal(self.repo / 'experiments/expB/tasks/s1-0-AB.json')
        r01 = file_hash(self.repo / 'runs/s1-c0/results/final-auditor-r01.json')
        r02 = file_hash(self.repo / 'runs/s1-c0/results/final-auditor-r02.json')
        self.assertNotEqual(r01, r02)
        self.assertEqual(rec['candidate_audit_sha256'], r02)
        self.assertEqual(rec['parent_audit_sha256'],
                         file_hash(self.repo / 'runs/s1-p0/results/final-auditor-r01.json'))
        self.assertEqual(rec['candidate_book_sha256'], cand.complete()['book_sha256'])

    def test_three_wins_not_statistical_sufficiency(self):
        self.assertLess(wilson_lower(3,3),0.5)
        self.assertGreater(wilson_lower(5,5),0.5)
    def test_missing_human_calibration_rejected(self):
        with self.assertRaises(FactoryError): validate_calibration({},'0'*64,'judge','external')

if __name__=='__main__': unittest.main()
