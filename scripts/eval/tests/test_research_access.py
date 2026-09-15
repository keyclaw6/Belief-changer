"""Offline research integration tests: all external tools/sites are mocked, never live readiness."""
from __future__ import annotations
import copy
from datetime import datetime, timezone, timedelta
import hashlib, io, json, os
from pathlib import Path
import shutil, stat, subprocess, sys, tempfile, unittest, zipfile
from unittest.mock import patch
SOURCE=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(SOURCE/'scripts'))
from bc_factory import research_access as A
from bc_factory.research_setup import unpack_extension, bootstrap
from bc_factory.common import FactoryError, digest, file_hash
from bc_factory.demo import scaffold, inputs
from bc_factory.runs import prepare, Run
from bc_factory.archive import build, excluded

class Base(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.repo=Path(self.temp.name)/'repo'
        scaffold(SOURCE,self.repo); self.c=A.config(self.repo)
    def tearDown(self):self.temp.cleanup()
    def report(self,subject='practice-belief'):
        return {'schema_version':1,'subject':subject,'created_at':datetime.now(timezone.utc).isoformat(),
                'config_sha256':digest(self.c),'status':'READY','live':True,
                'checks':{c:True for c in A.CHECKS},'failures':[],'tools':{'fixture':'mocked; not live'}}
    def bridge_report(self,subject='practice-belief'):
        return {'schema_version':1,'subject':subject,'created_at':datetime.now(timezone.utc).isoformat(),
                'config_sha256':digest(self.c),'status':'READY','live':True,'via':'bridge',
                'checks':{c:True for c in A.BRIDGE_CHECKS},'failures':[],'tools':{'fixture':'mocked; not live'}}
    def dossier(self):
        b,r,_=inputs(); src=r['sources'][0]
        r['sources']=[]; lanes={}
        for lane,url in [('web','https://example.org/paper'),('reddit','https://www.reddit.com/comments/abc123'),('x','https://x.com/i/status/123'),('recovery_forums','https://example.org/forum')]:
            s=copy.deepcopy(src);s.update(id=lane,kind='lived_experience',source=url,verification='retrieved')
            r['sources'].append(s)
            lanes[lane]={'queries':['test-only executed query'],'source_ids':[lane],'unfilled_slots':[],'access_failures':[],'scarcity_reason':''}
        r['coverage']={'general_web_preserved':True,'effort_weights':{'web':1,'reddit':1,'x':1},'allocation_reason':'test fixture',
                       'saturation_rationale':'Test-only dossier, never empirical evidence.','lanes':lanes}
        return b,r

class AccessContractTests(Base):
    def test_non_cloak_browser_rejected(self):
        self.c['browser']='chromium';(self.repo/'factory/research-access.json').write_text(json.dumps(self.c))
        with self.assertRaises(FactoryError):A.config(self.repo)
    def test_extension_unpinned_source_rejected(self):
        self.c['nopecha_asset_url']='https://example.org/extension.zip';(self.repo/'factory/research-access.json').write_text(json.dumps(self.c))
        with self.assertRaises(FactoryError):A.config(self.repo)
    def test_only_additive_default_accepted(self):
        self.c['default_effort_weights']['web']=0.3;(self.repo/'factory/research-access.json').write_text(json.dumps(self.c))
        with self.assertRaises(FactoryError):A.config(self.repo)
    def test_profile_in_repo_rejected(self):
        with patch.dict(os.environ,{'BC_RESEARCH_HOME':str(self.repo/'profile')}):
            with self.assertRaises(FactoryError):A.state_root(self.repo)
    def test_profile_symlink_rejected(self):
        link=Path(self.temp.name)/'profile';link.symlink_to(self.repo,target_is_directory=True)
        with patch.dict(os.environ,{'BC_RESEARCH_HOME':str(link)}):
            with self.assertRaises(FactoryError):A.state_root(self.repo)
    def test_no_bootstrap_side_effect_without_apply(self):
        state=Path(self.temp.name)/'external'
        with patch.dict(os.environ,{'BC_RESEARCH_HOME':str(state)}),patch('bc_factory.research_setup.command') as cmd:
            out=bootstrap(self.repo);self.assertEqual(out['status'],'INSTALL_PLAN');cmd.assert_not_called();self.assertFalse(state.exists())
    def test_social_write_rejected(self):
        for action in ('post','vote','comment','reply','follow','login','delete'):
            with self.assertRaises(FactoryError):A.social_args('x',action,'something')
    def test_option_injection_rejected(self):
        with self.assertRaises(FactoryError):A.social_args('reddit','search','--post')
    def test_read_command_expands_comments_and_reports_limit(self):
        args=A.social_args('reddit','read','https://www.reddit.com/r/test/comments/abc123/title',50)
        self.assertEqual(args[:3],['reddit','read','abc123']);self.assertIn('--expand-more',args);self.assertIn('20000',args);self.assertIn('50',args)
    def test_social_search_no_shell_interpolation(self):
        query='recovery; $(touch nope)'
        self.assertEqual(A.social_args('x','search',query)[2],query)
    def test_cross_domain_reads_rejected(self):
        for url in ('https://example.org/status/123','https://x.com.evil.org/status/123'):
            with self.assertRaises(FactoryError):A.social_args('x','read',url)
    def test_private_and_credential_urls_rejected(self):
        for url in ('http://example.org','https://127.0.0.1/','https://10.0.0.2/','https://user:pass@example.org/','https://example.org/?auth_token=a','https://example.org:9222/'):
            with self.assertRaises(FactoryError):A.safe_url(url)
    def test_login_wall_and_challenge_not_evidence(self):
        for title,url in [('Sign in to continue','https://example.org/topic'),('Just a moment','https://example.org/topic'),('Forum','https://example.org/login')]:
            with self.assertRaises(FactoryError):A.validate_page(title,url,'Please authenticate to continue. '*10)
        A.validate_page('A recovery discussion','https://example.org/topic','A substantive discussion of a lived experience. '*4)
    def test_valid_url_strips_fragment(self):self.assertEqual(A.safe_url('https://example.org/path#part'),'https://example.org/path')
    def test_empty_or_error_output_is_not_success(self):
        for data in ([],[{}],{'error':'auth'},{'success':False},[{'status':'ok'}],{'username':'anon','authenticated':False}):
            with self.assertRaises(FactoryError):A.rows(data)
    def test_nested_results_parsed(self):self.assertEqual(A.rows({'data':{'rows':[{'text':'Actual text'}]}}),[{'text':'Actual text'}])
    def test_field_value_auth_accepted(self):
        self.assertEqual(A.auth_rows([{'field':'Username','value':'u/test'},{'field':'ID','value':'t2_x'}]),[{'username':'u/test'}])
        with self.assertRaises(FactoryError):A.auth_rows([{'field':'Username','value':' '}])
        with self.assertRaises(FactoryError):A.auth_rows([{'field':'Karma','value':'1'}])
    def test_first_canonical_post_url(self):self.assertEqual(A.first_url([{'id':'t3_abc123'}],'reddit'),'https://www.reddit.com/comments/abc123')
    def test_redacts_keys_and_setup_url(self):
        with patch.dict(os.environ,{'NOPECHA_API_KEY':'local-secret-value'}):
            text=A.redact('local-secret-value https://nopecha.com/setup#another-secret auth_token=secret')
            self.assertNotIn('local-secret-value',text);self.assertNotIn('another-secret',text);self.assertNotIn('auth_token=secret',text)
    def test_external_exceptions_do_not_leak_urls(self):
        self.assertNotIn('secret',A.safe_error(RuntimeError('https://x.com/?token=secret')))
    def test_bad_limit_rejected(self):
        for n in (0,-1,1001,True):
            with self.assertRaises(FactoryError):A.social_args('reddit','search','test',n)

class PreflightTests(Base):
    def test_offline_never_ready(self):
        with patch.object(A,'CloakSession') as b:
            report=A.preflight(self.repo,'practice-belief');b.assert_not_called()
        self.assertEqual(report['status'],'BLOCKED');self.assertFalse(any(report['checks'].values()))
    def test_ready_report_validates(self):A.validate_preflight(self.report(),self.c,'practice-belief')
    def test_missing_check_rejected(self):
        report=self.report();report['checks'].pop('reddit_read')
        with self.assertRaises(FactoryError):A.validate_preflight(report,self.c,'practice-belief')
    def test_false_check_rejected(self):
        report=self.report();report['checks']['x_auth']=False
        with self.assertRaises(FactoryError):A.validate_preflight(report,self.c,'practice-belief')
    def test_unresolved_failure_rejected(self):
        report=self.report();report['failures']=['quota']
        with self.assertRaises(FactoryError):A.validate_preflight(report,self.c,'practice-belief')
    def test_stale_future_subject_and_config_rejected(self):
        for key,value in [('created_at',(datetime.now(timezone.utc)-timedelta(days=2)).isoformat()),('created_at',(datetime.now(timezone.utc)+timedelta(days=1)).isoformat()),('subject','other'),('config_sha256','wrong'),('live',False)]:
            r=self.report();r[key]=value
            with self.assertRaises(FactoryError):A.validate_preflight(r,self.c,'practice-belief')
    def test_doctor_alone_cannot_pass(self):
        from unittest.mock import Mock
        version = Mock(returncode=0, stdout='opencli 1.8.7')
        with patch.object(A, 'command', return_value=version), \
             patch.object(A, 'bridge_social', side_effect=FactoryError('Expired login')), \
             patch.object(A, 'bridge_search_web', return_value=[{'title': 't', 'url': 'https://example.org'}]), \
             patch.object(A, 'bridge_read_web', return_value={'url': 'https://example.com/', 'title': 't', 'text': 'x' * 50, 'retrieved_at': '', 'truncated': False}):
            report = A.preflight(self.repo, 'practice-belief', True, True)
        self.assertEqual(report['status'], 'BLOCKED')
        self.assertTrue(report['checks']['web_search'])
        self.assertFalse(report['checks']['x_auth'])
    def test_mocked_full_live_probe_calls_all_lanes(self):
        from unittest.mock import Mock
        calls = []
        def social(c, state, lane, action, *args):
            calls.append(lane + '_' + action)
            return [{'id': 'abc123' if lane == 'reddit' else '123', 'text': 'Test-only mocked content'}]
        def web_search(c, query, limit=10):
            calls.append('web_search')
            return [{'title': 't', 'url': 'https://example.org'}]
        def web_read(c, url):
            calls.append('web_read')
            return {'url': url, 'title': 't', 'text': 'x' * 50, 'retrieved_at': '', 'truncated': False}
        version = Mock(returncode=0, stdout='opencli 1.8.7')
        with patch.object(A, 'command', return_value=version), \
             patch.object(A, 'bridge_social', side_effect=social), \
             patch.object(A, 'bridge_search_web', side_effect=web_search), \
             patch.object(A, 'bridge_read_web', side_effect=web_read):
            r = A.preflight(self.repo, 'practice-belief', True, True)
        self.assertEqual(r['status'], 'READY')
        self.assertEqual(r['via'], 'bridge')
        self.assertEqual(len(calls), 8)
    def test_failed_auth_blocks_read_and_campaign(self):
        from unittest.mock import Mock
        version = Mock(returncode=0, stdout='opencli 1.8.7')
        with patch.object(A, 'command', return_value=version), \
             patch.object(A, 'bridge_search_web', return_value=[{'title': 't', 'url': 'https://example.org'}]), \
             patch.object(A, 'bridge_read_web', return_value={'url': 'x', 'title': 't', 'text': 'y' * 50, 'retrieved_at': '', 'truncated': False}), \
             patch.object(A, 'bridge_social', side_effect=FactoryError('Expired login')):
            r = A.preflight(self.repo, 'practice-belief', True, True)
        self.assertEqual(r['status'], 'BLOCKED')
        self.assertFalse(r['checks']['x_read'])
        self.assertFalse(r['checks']['reddit_read'])
    def test_opencli_minimum_floor(self):
        from unittest.mock import Mock
        self.assertTrue(A.version_tuple('opencli 1.8.9') >= A.version_tuple('1.8.7'))
        self.assertFalse(A.version_tuple('opencli 1.8.6') >= A.version_tuple('1.8.7'))
        self.c['opencli_version'] = '9.9.9'
        (self.repo / 'factory/research-access.json').write_text(json.dumps(self.c))
        version = Mock(returncode=0, stdout='opencli 1.8.7')
        with patch.object(A, 'command', return_value=version):
            r = A.preflight(self.repo, 'practice-belief', True, True)
        self.assertEqual(r['status'], 'BLOCKED')
        self.assertIn('minimum', r['failures'][0])
    def test_bridge_ready_report_validates(self):
        A.validate_preflight(self.bridge_report(), self.c, 'practice-belief')
    def test_cloak_report_without_via_still_validates(self):
        A.validate_preflight(self.report(), self.c, 'practice-belief')
    def test_query_route_mismatch_rejected(self):
        with self.assertRaises(FactoryError):
            A.query(self.repo, 'practice-belief', 'web', 'search', 'test', 5, self.bridge_report(), True, via='cloak')
    def test_real_prepare_cannot_skip_preflight(self):
        b,r=self.dossier()
        with self.assertRaises(FactoryError):prepare(self.repo,'blocked',b,r,fixture=False)
        self.assertFalse((self.repo/'runs/blocked').exists())
    def test_real_prepare_freezes_report_and_detects_tamper(self):
        b,r=self.dossier();prepare(self.repo,'gated',b,r,fixture=False,research_preflight=self.report())
        run=Run(self.repo,'gated');self.assertTrue(run.manifest['research_preflight_sha256'])
        path=run.root/'inputs/research-preflight.json';path.write_text('{}')
        with self.assertRaises(FactoryError):Run(self.repo,'gated')

class CoverageTests(Base):
    def test_four_lanes_validate(self):A.validate_coverage(self.dossier()[1])
    def test_missing_reddit_rejected(self):
        r=self.dossier()[1];r['coverage']['lanes'].pop('reddit')
        with self.assertRaises(FactoryError):A.validate_coverage(r)
    def test_web_reduction_rejected(self):
        r=self.dossier()[1];r['coverage']['effort_weights']['web']=0.5
        with self.assertRaises(FactoryError):A.validate_coverage(r)
    def test_adaptive_effort_requires_reason(self):
        r=self.dossier()[1];r['coverage']['effort_weights']['x']=0.5
        with self.assertRaises(FactoryError):A.validate_coverage(r)
        r['coverage']['allocation_reason']='The actual topic searches yielded few firsthand X accounts but many relevant independent forum discussions.'
        A.validate_coverage(r)
    def test_blocked_site_not_scarcity(self):
        r=self.dossier()[1];lane=r['coverage']['lanes']['x'];lane.update(source_ids=[],scarcity_reason='No stories',access_failures=['403'])
        with self.assertRaises(FactoryError):A.validate_coverage(r)
    def test_true_scarcity_needs_query_trail(self):
        r=self.dossier()[1];lane=r['coverage']['lanes']['x'];lane.update(source_ids=[],scarcity_reason='Multiple reachable searches returned no relevant firsthand narratives.')
        A.validate_coverage(r);lane['queries']=[]
        with self.assertRaises(FactoryError):A.validate_coverage(r)
    def test_unknown_source_rejected(self):
        r=self.dossier()[1];r['coverage']['lanes']['x']['source_ids']=['invented']
        with self.assertRaises(FactoryError):A.validate_coverage(r)
    def test_wrong_platform_source_rejected(self):
        r=self.dossier()[1];r['coverage']['lanes']['x']['source_ids']=['web']
        with self.assertRaises(FactoryError):A.validate_coverage(r)
    def test_illustration_not_live_coverage(self):
        r=self.dossier()[1];r['sources'][1]['kind']='illustration'
        with self.assertRaises(FactoryError):A.validate_coverage(r)
    def test_duplicate_count_rejected(self):
        r=self.dossier()[1];r['coverage']['lanes']['x']['source_ids']=['x','x']
        with self.assertRaises(FactoryError):A.validate_coverage(r)

class PackageTests(Base):
    def zipbytes(self,name='manifest.json',mode=0o100644):
        b=io.BytesIO()
        with zipfile.ZipFile(b,'w') as z:
            i=zipfile.ZipInfo(name);i.external_attr=mode<<16;z.writestr(i,'{}')
        return b.getvalue()
    def test_digest_checked_before_install(self):
        with self.assertRaises(FactoryError):unpack_extension(self.zipbytes(),Path(self.temp.name)/'extension','0'*64)
    def test_extension_zip_traversal_rejected(self):
        for name in ('../manifest.json','/manifest.json','x\\manifest.json'):
            b=self.zipbytes(name)
            with self.assertRaises(FactoryError):unpack_extension(b,Path(self.temp.name)/'extension',hashlib.sha256(b).hexdigest())
    def test_extension_symlink_rejected(self):
        b=self.zipbytes(mode=stat.S_IFLNK|0o777)
        with self.assertRaises(FactoryError):unpack_extension(b,Path(self.temp.name)/'extension',hashlib.sha256(b).hexdigest())
    def test_safe_extension_hashes_recorded(self):
        b=self.zipbytes();r=unpack_extension(b,Path(self.temp.name)/'extension',hashlib.sha256(b).hexdigest())
        self.assertEqual(r['manifest.json'],hashlib.sha256(b'{}').hexdigest())
    def test_private_profile_and_cookie_files_excluded(self):
        for p in ('profile/Cookies','browser-profiles/x/Login Data','cookies.json','credential.json','.env','storage-state.json'):
            self.assertTrue(excluded(p),p)
    def test_old_archive_manifest_not_duplicated(self):
        (self.repo/'ARCHIVE-MANIFEST.json').write_text('old manifest')
        out=Path(self.temp.name)/'archive.zip';build(self.repo,out)
        with zipfile.ZipFile(out) as z:self.assertEqual(z.namelist().count('Belief-changer/ARCHIVE-MANIFEST.json'),1)

if __name__=='__main__':unittest.main()
