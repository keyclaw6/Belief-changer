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
from bc_factory.experiments import CALIBRATION_CATEGORIES, decide, pair_task, promote, register, submit_pair, validate_calibration, wilson_lower
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
        prepare(self.repo, name, self.brief, self.research, fixture=fixture)
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
        with self.assertRaises(FactoryError): self.newrun().task('planner')
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
        for n in range(1,5):
            task=run.task('writer',1,n)
            run.submit(task,{'schema_version':2,'chapter_id':'chapter-01','text':'A partial argument.','claim_map':[]},metadata())
            r=accepted();r['verdict']='REVISE';r['checks']['argument']=False
            run.submit(run.task('chapter-reviewer',1,n),r,metadata())
        with self.assertRaises(FactoryError): run.task('writer',1,5)
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

    def test_three_wins_not_statistical_sufficiency(self):
        self.assertLess(wilson_lower(3,3),0.5)
        self.assertGreater(wilson_lower(5,5),0.5)
    def test_missing_human_calibration_rejected(self):
        with self.assertRaises(FactoryError): validate_calibration({},'0'*64,'judge','external')

if __name__=='__main__': unittest.main()
