"""Explicit local installation, never a global/system install or a campaign side effect."""
from __future__ import annotations
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.request
import venv
import zipfile
from .common import FactoryError, atomic_json, require, read_json
from .research_access import config, state_root, command


def unpack_extension(data: bytes, dest: Path, sha256: str) -> dict:
    require(hashlib.sha256(data).hexdigest()==sha256,'NopeCHA download hash mismatch; nothing installed')
    require(not dest.exists(), 'Extension target must be new')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        files=z.infolist()
        require(sum(i.file_size for i in files)<=64*1024*1024 and len(files)<=3000,'Unexpected extension archive size')
        names=set()
        for i in files:
            p=PurePosixPath(i.filename)
            require(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename,'Unsafe extension ZIP path')
            require(i.filename not in names,'Duplicate extension ZIP entry'); names.add(i.filename)
            require(not stat.S_ISLNK(i.external_attr>>16),'Extension ZIP contains a symlink')
        require('manifest.json' in names,'Extension archive has no root manifest')
        dest.mkdir(parents=True,mode=0o700)
        z.extractall(dest)
    return {p.relative_to(dest).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.rglob('*') if p.is_file()}


def bootstrap(repo: Path,apply: bool=False) -> dict:
    c=config(repo); state=state_root(repo,apply)
    py=state/'venv/bin/python'
    steps=[
        [str(py),'-m','pip','install','git+https://github.com/Panniantong/Agent-Reach.git@'+c['agent_reach_commit'], 'cloakbrowser=='+c['cloakbrowser_version']],
        ['npm','install','--prefix',str(state/'node'),'--save-exact','@jackwener/opencli@'+c['opencli_version']],
        [str(py),'-m','cloakbrowser','install']]
    result={'status':'INSTALL_PLAN','state_outside_repo':str(state),'commands':steps,
            'nopecha_asset':c['nopecha_asset_url'],'sha256':c['nopecha_sha256'],
            'notes':['No global/system packages, account creation, cookie extraction or paid subscriptions.',
                     'Node >=20.18.1 and Git must already be available. Linux needs browser system libraries and a display/Xvfb.',
                     'No browser/extension binaries are bundled or relicensed. Review upstream licenses before deployment.',
                     'Set NOPECHA_API_KEY locally; any CloakBrowser license is also local. Then login and run live preflight.']}
    if not apply: return result
    require(shutil.which('git') and shutil.which('npm'),'Git and npm must already be installed')
    n=command(['node','--version'],timeout=10)
    try: version=tuple(int(x) for x in n.stdout.strip().lstrip('v').split('.'))
    except ValueError: raise FactoryError('Cannot determine Node version') from None
    require(n.returncode==0 and version>=(20,18,1),'Node >=20.18.1 is required')
    venv.EnvBuilder(with_pip=True).create(state/'venv')
    for args in steps:
        r=command(args,timeout=900)
        require(r.returncode==0,f'Installation failed at {Path(args[0]).name}; inspect the installation locally. No credentials printed.')
    req=urllib.request.Request(c['nopecha_asset_url'],headers={'User-Agent':'Belief-Changer-research-setup/2.1'})
    with urllib.request.urlopen(req,timeout=90) as response:
        data=response.read(8*1024*1024+1)
    require(len(data)<=8*1024*1024,'Extension download exceeds size guard')
    parent=state/'extensions'; parent.mkdir(exist_ok=True,mode=0o700)
    with tempfile.TemporaryDirectory(dir=parent) as td:
        stage=Path(td)/'nopecha'
        hashes=unpack_extension(data,stage,c['nopecha_sha256'])
        m=read_json(stage/'manifest.json')
        require(m.get('version')==c['nopecha_version'],'NopeCHA version mismatch')
        dest=parent/'nopecha'
        require(not dest.is_symlink(),'Unsafe installed extension path')
        if dest.exists(): shutil.rmtree(dest)
        shutil.move(stage,dest)
        atomic_json(parent/'nopecha-install.json',{'asset_sha256':c['nopecha_sha256'],'files':hashes})
    result['status']='INSTALLED_NOT_AUTHENTICATED'
    result['next']=[str(py),str(repo/'scripts/factory.py'),'research-login','--allow-captcha']
    return result
