"""Exercise publication against temporary local bare Git repositories; never GitHub."""
from __future__ import annotations
import hashlib,json,os
from pathlib import Path
import shutil,sys,tempfile,unittest
from unittest.mock import patch
SOURCE=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(SOURCE/'scripts'))
import publish_main as P

class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.remote=self.root/'remote.git';self.seed=self.root/'seed';self.source=self.root/'delivery';self.dest=self.root/'published'
        P.git(['init','--bare',str(self.remote)]);P.git(['init','-b','main',str(self.seed)])
        P.git(['config','user.name','Offline Test'],self.seed);P.git(['config','user.email','offline@example.invalid'],self.seed)
        (self.seed/'VISION.md').write_text('Original vision must stay.\n');P.git(['add','.'],self.seed);P.git(['commit','-m','main'],self.seed)
        self.heads={'main':P.git(['rev-parse','HEAD'],self.seed).stdout.strip()}
        P.git(['checkout','-b',P.CAMPAIGN],self.seed)
        (self.seed/'old-iteration.txt').write_text('Disposable historical output\n');P.git(['add','.'],self.seed);P.git(['commit','-m','campaign'],self.seed)
        self.heads[P.CAMPAIGN]=P.git(['rev-parse','HEAD'],self.seed).stdout.strip()
        P.git(['checkout','-b',P.UPGRADE],self.seed)
        (self.seed/'v2.py').write_text('version = 2\n');P.git(['add','.'],self.seed);P.git(['commit','-m','upgrade'],self.seed)
        self.heads[P.UPGRADE]=P.git(['rev-parse','HEAD'],self.seed).stdout.strip()
        P.git(['remote','add','origin',str(self.remote)],self.seed);P.git(['push','origin','--all'],self.seed)
        P.git(['symbolic-ref','HEAD','refs/heads/main'],self.remote)
        self.source.mkdir();(self.source/'scripts').mkdir()
        (self.source/'VISION.md').write_text('Original vision must stay.\n')
        (self.source/'v2.py').write_text('version = 2.1\n')
        (self.source/'scripts/factory.py').write_text('# synthetic fixture\n')
        (self.source/'scripts/publish_main.py').write_text('# synthetic fixture\n')
        self.manifest()
    def tearDown(self):self.tmp.cleanup()
    def manifest(self):
        files={p.relative_to(self.source).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in self.source.rglob('*') if p.is_file() and p.name!='ARCHIVE-MANIFEST.json'}
        (self.source/'ARCHIVE-MANIFEST.json').write_text(json.dumps({'files':files}))
    def run_publish(self,**kwargs):
        return P.publish(self.source,self.dest,remote=str(self.remote),expected=self.heads,name='Offline Test',email='offline@example.invalid',verify=lambda path:None,**kwargs)
    def test_default_plan_makes_no_changes(self):
        with patch.object(P,'remote_heads',side_effect=AssertionError('No network for default plan')):
            result=self.run_publish()
        self.assertEqual(result['status'],'PLAN_ONLY');self.assertFalse(self.dest.exists())
    def test_complete_atomic_merge_and_delete(self):
        result=self.run_publish(apply=True)
        self.assertEqual(result['status'],'PUBLISHED_MAIN_ONLY')
        self.assertEqual(P.remote_heads(str(self.remote)),{'main':result['commit']})
        self.assertFalse((self.dest/'old-iteration.txt').exists())
        self.assertEqual((self.dest/'VISION.md').read_text(),'Original vision must stay.\n')
        for sha in self.heads.values():self.assertEqual(P.git(['merge-base','--is-ancestor',sha,result['commit']],self.dest).returncode,0)
        self.assertEqual(P.git(['show',self.heads[P.CAMPAIGN]+':old-iteration.txt'],self.dest).stdout,'Disposable historical output\n')
    def test_existing_destination_never_cleaned(self):
        self.dest.mkdir();(self.dest/'precious').write_text('User work')
        with self.assertRaises(P.PublishError):self.run_publish(apply=True)
        self.assertEqual((self.dest/'precious').read_text(),'User work')
        self.assertEqual(P.remote_heads(str(self.remote)),self.heads)
    def test_modified_delivery_blocks_before_clone(self):
        (self.source/'v2.py').write_text('tamper')
        with self.assertRaises(P.PublishError):self.run_publish(apply=True)
        self.assertFalse(self.dest.exists());self.assertEqual(P.remote_heads(str(self.remote)),self.heads)
    def test_unknown_remote_branch_blocks(self):
        P.git(['push','origin','HEAD:refs/heads/new-work'],self.seed)
        before=P.remote_heads(str(self.remote))
        with self.assertRaises(P.PublishError):self.run_publish(apply=True)
        self.assertFalse(self.dest.exists());self.assertEqual(P.remote_heads(str(self.remote)),before)
    def test_changed_remote_head_blocks(self):
        (self.seed/'more.py').write_text('new work');P.git(['add','.'],self.seed);P.git(['commit','-m','later'],self.seed);P.git(['push','origin',P.UPGRADE],self.seed)
        before=P.remote_heads(str(self.remote))
        with self.assertRaises(P.PublishError):self.run_publish(apply=True)
        self.assertEqual(P.remote_heads(str(self.remote)),before)
    def test_failed_tests_do_not_push(self):
        def fail(path):raise P.PublishError('Synthetic test failure')
        with self.assertRaises(P.PublishError):
            P.publish(self.source,self.dest,apply=True,remote=str(self.remote),expected=self.heads,name='Offline Test',email='offline@example.invalid',verify=fail)
        self.assertEqual(P.remote_heads(str(self.remote)),self.heads)
    def test_concurrent_change_after_tests_is_not_deleted(self):
        def update_remote(path):
            (self.seed/'concurrent').write_text('new work');P.git(['add','.'],self.seed);P.git(['commit','-m','concurrent'],self.seed);P.git(['push','origin',P.UPGRADE],self.seed)
        with self.assertRaises(P.PublishError):
            P.publish(self.source,self.dest,apply=True,remote=str(self.remote),expected=self.heads,name='Offline Test',email='offline@example.invalid',verify=update_remote)
        actual=P.remote_heads(str(self.remote));self.assertEqual(actual['main'],self.heads['main']);self.assertIn(P.CAMPAIGN,actual);self.assertIn(P.UPGRADE,actual)
    def test_atomic_server_rejection_preserves_all_branches(self):
        # Branch deletions are denied, so the atomic main update must fail too.
        P.git(['config','receive.denyDeletes','true'],self.remote)
        with self.assertRaises(P.PublishError):self.run_publish(apply=True)
        self.assertEqual(P.remote_heads(str(self.remote)),self.heads)
    def test_source_escape_in_manifest_rejected(self):
        m=json.loads((self.source/'ARCHIVE-MANIFEST.json').read_text());m['files']['../outside']='0'*64
        (self.source/'ARCHIVE-MANIFEST.json').write_text(json.dumps(m))
        with self.assertRaises(P.PublishError):P.source_files(self.source)
    def test_secret_file_in_manifest_rejected(self):
        (self.source/'.env').write_text('KEY=synthetic');self.manifest()
        with self.assertRaises(P.PublishError):P.source_files(self.source)
    def test_campaign_default_changed_to_main(self):
        P.git(['symbolic-ref','HEAD','refs/heads/'+P.CAMPAIGN],self.remote)
        self.run_publish(apply=True)
        self.assertEqual(P.default_branch(str(self.remote)),'main')
    def test_rejected_push_restores_old_default(self):
        P.git(['symbolic-ref','HEAD','refs/heads/'+P.CAMPAIGN],self.remote)
        P.git(['config','receive.denyDeletes','true'],self.remote)
        with self.assertRaises(P.PublishError):self.run_publish(apply=True)
        self.assertEqual(P.default_branch(str(self.remote)),P.CAMPAIGN)
        self.assertEqual(P.remote_heads(str(self.remote)),self.heads)
    def test_local_snapshot_only_main(self):
        self.run_publish(apply=True)
        names=P.git(['for-each-ref','--format=%(refname:short)','refs/heads/'],self.dest).stdout.splitlines()
        self.assertEqual(names,['main'])

if __name__=='__main__':unittest.main()
