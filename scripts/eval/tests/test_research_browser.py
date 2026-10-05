"""Private state/owned browser guards. No credentials, browser launch or network."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from bc_factory import research_browser as B, research_access as A
from bc_factory.common import FactoryError


class ResearchBrowserTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.repo=self.base/'repo';self.repo.mkdir()
        self.home=self.base/'private';self.home.mkdir(mode=0o700)

    def test_private_state_rejects_repo_and_traversal(self):
        for p in (self.repo/'state.enc',self.home/'..'/'repo'/'state.enc'):
            with self.assertRaisesRegex(FactoryError,'outside'):
                B.private_file(p,self.repo)

    def test_private_state_rejects_symlink_parent(self):
        link=self.home/'link';link.symlink_to(self.base,target_is_directory=True)
        with self.assertRaisesRegex(FactoryError,'symlink'):
            B.write_private(link/'secret',b'fixture',self.repo)

    @unittest.skipUnless(os.name=='posix','POSIX permissions')
    def test_private_files_are_owner_only_and_insecure_reads_fail(self):
        path=self.home/'auth/state.enc';B.write_private(path,b'fixture',self.repo)
        self.assertEqual(path.stat().st_mode & 0o777,0o600)
        path.chmod(0o644)
        with self.assertRaisesRegex(FactoryError,'owner-only'):
            B.private_file(path,self.repo,existing=True)

    def test_binding_uses_owned_cdp_identity_not_foreign_alias(self):
        c={'bridge_profile':'research','bridge_profiles':{'web':'research','reddit':'research','x':'research'}}
        p=self.home/'opencli-config/browser-profiles.json';p.parent.mkdir();p.write_text(json.dumps({'aliases':{'research':'foreign'}}))
        with patch.object(B,'bridge_profiles',return_value={'foreign','owned'}), \
             patch.object(B,'owned_bridge',return_value='owned'), \
             patch.object(B.subprocess,'run',return_value=Mock(returncode=0)) as cmd:
            selected=B.bind_bridge(c,self.home,{'foreign','owned'})
        self.assertEqual(selected,'owned')
        self.assertEqual(cmd.call_args.args[0][-2:],['owned','research'])

    def test_missing_owned_identity_fails_without_renaming_foreign_context(self):
        c={'bridge_profile':'research'}
        with patch.object(B,'bridge_profiles',return_value={'foreign'}), \
             patch.object(B,'owned_bridge',return_value=None), \
             patch.object(B.time,'monotonic',side_effect=[0,0,30]), \
             patch.object(B.time,'sleep'), patch.object(B.subprocess,'run') as cmd:
            with self.assertRaisesRegex(FactoryError,'uniquely'):
                B.bind_bridge(c,self.home,set())
        cmd.assert_not_called()

    def test_bridge_extension_modification_is_rejected(self):
        p=self.home/'extensions/opencli';p.mkdir(parents=True)
        manifest={'manifest_version':3,'version':'1.0.24'}
        (p/'manifest.json').write_text(json.dumps(manifest));(p/'background.js').write_text('original')
        files={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in p.iterdir()}
        sha='a'*64
        (p.parent/'opencli-install.json').write_text(json.dumps({'asset_sha256':sha,'files':files}))
        c={'opencli_extension_version':'1.0.24','opencli_extension_sha256':sha}
        A.extension_check(p,c,'opencli')
        (p/'background.js').write_text('changed')
        with self.assertRaisesRegex(FactoryError,'modified'):
            A.extension_check(p,c,'opencli')

    def test_domain_filter_excludes_other_accounts_and_fake_suffixes(self):
        # Node is an explicitly installed live-research dependency; no browser used.
        import shutil
        if not shutil.which('node'):self.skipTest('Node unavailable')
        helper=ROOT/'scripts/bc_factory/research_state.cjs'
        script="const {filterState}=require(process.argv[1]); const s=JSON.parse(process.argv[2]); console.log(JSON.stringify(filterState(s,['x.com'])));"
        state={'cookies':[{'domain':'.x.com','name':'allowed'},{'domain':'notx.com','name':'denied'},{'domain':'.economic.dk','name':'business'}],
               'origins':[{'origin':'https://x.com','localStorage':[]},{'origin':'https://x.com.evil.org','localStorage':[]}],
               'credentials':[{'rpId':'x.com'},{'rpId':'economic.dk'}],'unknown_secret_field':'fixture'}
        r=subprocess.run(['node','-e',script,str(helper),json.dumps(state)],capture_output=True,text=True,check=True)
        filtered=json.loads(r.stdout)
        self.assertEqual([c['name'] for c in filtered['cookies']],['allowed'])
        self.assertEqual([o['origin'] for o in filtered['origins']],['https://x.com'])
        self.assertEqual(filtered['credentials'],[{'rpId':'x.com'}])
        self.assertNotIn('unknown_secret_field',filtered)


if __name__=='__main__':unittest.main()
