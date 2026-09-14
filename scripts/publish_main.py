#!/usr/bin/env python3
"""Publish this verified delivery into main; never overwrite an existing working tree.

Default is a local plan only. --apply requires authenticated Git network access.
A single atomic push advances main and removes exactly the two reviewed branches.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

REPOSITORY='https://github.com/keyclaw6/Belief-changer.git'
UPGRADE='upgrade/truth-first-factory-v2'
CAMPAIGN='campaign-001'
EXPECTED={
    'main':'32516fa168f2dc619d5cb2fe767f7728ede15b49',
    CAMPAIGN:'cd730abc9d902f6394a529144ce54c400ae50751',
    UPGRADE:'6a90ffcdddad3c908144014cc41e51d693df7f9e',
}
class PublishError(RuntimeError):pass

def require(ok,message):
    if not ok:raise PublishError(message)

def git(args,cwd=None,check=True):
    p=subprocess.run(['git',*args],cwd=cwd,capture_output=True,text=True)
    if check and p.returncode:
        # Git URLs/credential-helper messages may contain private material.
        raise PublishError('Git step failed: '+args[0]+'. Inspect locally; no remote branch deletion fallback is attempted.')
    return p

def source_files(source:Path)->dict[str,str]:
    manifest=source/'ARCHIVE-MANIFEST.json'
    require(manifest.is_file() and not manifest.is_symlink(),'Run this script from the extracted verified delivery ZIP, containing ARCHIVE-MANIFEST.json')
    files=json.loads(manifest.read_text()).get('files',{})
    require(files and 'scripts/factory.py' in files and 'scripts/publish_main.py' in files,'Not a complete v2.1 delivery')
    for rel,expected in files.items():
        p=Path(rel)
        require(not p.is_absolute() and '..' not in p.parts and '\\' not in rel and '.git' not in p.parts,'Unsafe source path in manifest')
        require(not any(part in ('profile','browser-profiles','node_modules','extensions') for part in p.parts),'Private/runtime assets cannot be published')
        require(not (p.name.startswith('.env') and p.name!='.env.example'),'Credential file in delivery')
        full=source/p
        require(full.is_file() and not any(x.is_symlink() for x in (full,*full.parents) if x!=source.parent),'Missing or symlink source file')
        require(hashlib.sha256(full.read_bytes()).hexdigest()==expected,'Delivery hash mismatch: '+rel)
    return files

def remote_heads(remote:str,cwd:Path|None=None)->dict[str,str]:
    out=git(['ls-remote','--heads',remote],cwd).stdout
    return {ref.removeprefix('refs/heads/'):sha for sha,ref in (line.split() for line in out.splitlines() if line)}

def check_heads(actual:dict,expected:dict)->None:
    require(actual==expected,'Upstream branches changed or an additional branch exists. Stop and re-review; no branches were deleted.')

def default_branch(remote:str)->str:
    if remote != REPOSITORY: # local bare repositories in offline tests only
        return git(['symbolic-ref','--short','HEAD'],Path(remote)).stdout.strip()
    require(shutil.which('gh'), 'GitHub CLI (gh) is required to verify/change the default branch')
    result=subprocess.run(['gh','api','repos/keyclaw6/Belief-changer','--jq','.default_branch'],capture_output=True,text=True)
    require(result.returncode==0, 'Cannot read GitHub default branch; authenticate gh locally')
    return result.stdout.strip()

def set_default_branch(remote:str,branch:str)->None:
    require(branch in EXPECTED, 'Refuse an unexpected default branch')
    if remote != REPOSITORY:
        git(['symbolic-ref','HEAD','refs/heads/'+branch],Path(remote)); return
    result=subprocess.run(['gh','repo','edit','keyclaw6/Belief-changer','--default-branch',branch],capture_output=True,text=True)
    require(result.returncode==0, 'Default-branch update failed; no branch deletions attempted')
    require(default_branch(remote)==branch, 'Default-branch update could not be verified')

def overlay(source:Path,dest:Path,files:dict)->None:
    tracked=git(['ls-files','-z'],dest).stdout.split('\0')
    for rel in tracked:
        if not rel or rel in files:continue
        p=dest/rel
        if p.is_file() or p.is_symlink():p.unlink()
    for rel in sorted(files):
        src=source/rel;dst=dest/rel
        if dst.is_symlink():dst.unlink()
        for parent in dst.parents:
            if parent==dest:break
            require(not parent.is_symlink(),'Unsafe target parent; overlay stopped')
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dst)
        # Preserve useful executable bits across ZIP extraction tools.
        if rel.endswith('.sh') or rel in ('scripts/factory.py','scripts/publish_main.py'):dst.chmod(0o755)
    # Staging names is safe here: this is a brand-new clone populated from a verified inventory.
    git(['add','--all'],dest)
    actual=set(filter(None,git(['ls-files','-z'],dest).stdout.split('\0')))
    require(actual==set(files),'Staged tree differs from delivery inventory')
    for rel,expected in files.items():
        require(hashlib.sha256((dest/rel).read_bytes()).hexdigest()==expected,'Overlay hash mismatch: '+rel)

def identity(dest:Path,name:str|None,email:str|None)->None:
    require(bool(name)==bool(email),'Provide both --git-name and --git-email, or neither')
    if name:
        require('\n' not in name and '\n' not in email,'Invalid Git identity')
        git(['config','user.name',name],dest);git(['config','user.email',email],dest)
    elif git(['var','GIT_AUTHOR_IDENT'],dest,False).returncode:
        require(shutil.which('gh'),'Set your Git identity or provide --git-name and --git-email')
        p=subprocess.run(['gh','api','user','--jq','[.login,.id]|@tsv'],capture_output=True,text=True)
        require(p.returncode==0 and len(p.stdout.strip().split('\t'))==2,'Cannot resolve your authenticated GitHub identity')
        login,uid=p.stdout.strip().split('\t')
        require(uid.isdigit() and login and all(c.isalnum() or c=='-' for c in login),'Unexpected GitHub identity response')
        git(['config','user.name',login],dest)
        git(['config','user.email',f'{uid}+{login}@users.noreply.github.com'],dest)
    git(['var','GIT_AUTHOR_IDENT'],dest)

def verify_worktree(dest:Path)->None:
    p=subprocess.run(['bash','scripts/check.sh'],cwd=dest)
    require(p.returncode==0,'Regression gate failed; no push performed')
    # Synthetic pipeline also runs as an executable interface, not just in unit tests.
    with tempfile.TemporaryDirectory(prefix='bc-publish-demo-') as tmp:
        p=subprocess.run([sys.executable,'scripts/factory.py','demo','--output',str(Path(tmp)/'demo')],cwd=dest)
        require(p.returncode==0,'Offline demo failed; no push performed')
    git(['diff','--cached','--check'],dest)

def publish(source:Path,destination:Path,*,apply:bool=False,remote:str=REPOSITORY,
            expected:dict|None=None,name:str|None=None,email:str|None=None,verify=verify_worktree)->dict:
    # remote/expected are injectable only for isolated local-bare-repository tests.
    expected=EXPECTED if expected is None else expected
    source=source.resolve();destination=destination.absolute()
    files=source_files(source)
    require(not destination.exists(),'Destination must not exist; existing worktrees are never cleaned or reset')
    require(not destination.resolve().is_relative_to(source),'Destination must be outside the delivery')
    if not apply:
        return {'status':'PLAN_ONLY','remote':remote,'destination':str(destination),'files':len(files),
                'steps':['check all remote heads against reviewed SHAs','fresh clone; verify main and campaign are ancestors of upgrade',
                         'fast-forward main through upgrade (already includes campaign)','overlay checksum-verified clean delivery',
                         'run offline tests and synthetic pipeline; commit using authenticated/configured identity',
                         'recheck remote heads; switch GitHub default to main; atomically push main and delete campaign and upgrade','verify remote main-only and ancestry'],
                'remote_changed':False,'apply_flag_required':True}
    check_heads(remote_heads(remote),expected)
    initial_default=default_branch(remote)
    require(initial_default in expected, 'Unexpected default branch; review before publishing')
    git(['clone','--no-tags','--branch','main',remote,str(destination)])
    for branch,sha in expected.items():
        require(git(['rev-parse','origin/'+branch],destination).stdout.strip()==sha,'Fetched branch changed during clone')
    for branch in ('main',CAMPAIGN):
        require(git(['merge-base','--is-ancestor','origin/'+branch,'origin/'+UPGRADE],destination,False).returncode==0,
                'Branches diverged; a human merge review is required')
    git(['merge','--ff-only','origin/'+UPGRADE],destination)
    overlay(source,destination,files)
    verify(destination)
    identity(destination,name,email)
    # Revalidate after arbitrary test execution before creating/publishing the commit.
    for rel,sha in files.items():
        require(hashlib.sha256((destination/rel).read_bytes()).hexdigest()==sha,'Tests modified delivered source: '+rel)
    git(['commit','-m','feat(research): add authenticated social access, CloakBrowser preflight and compact history'],destination)
    head=git(['rev-parse','HEAD'],destination).stdout.strip()
    for sha in expected.values():
        require(git(['merge-base','--is-ancestor',sha,head],destination,False).returncode==0,'History would be lost; stop')
    check_heads(remote_heads(remote),expected)
    args=['push','--atomic',f'--force-with-lease=refs/heads/{CAMPAIGN}:{expected[CAMPAIGN]}',
          f'--force-with-lease=refs/heads/{UPGRADE}:{expected[UPGRADE]}','origin','HEAD:refs/heads/main',
          ':refs/heads/'+CAMPAIGN,':refs/heads/'+UPGRADE]
    require(default_branch(remote)==initial_default, 'Default branch changed during verification; stop without changing it')
    changed_default=initial_default!='main'
    if changed_default: set_default_branch(remote,'main')
    try:
        git(args,destination)
    except PublishError:
        # Network errors can occur after server acceptance. Inspect refs before rollback.
        try: observed=remote_heads(remote)
        except PublishError:
            raise PublishError('Push outcome cannot be verified. Default branch may now be main; inspect GitHub. No automatic deletion/retry was attempted.') from None
        if observed != {'main':head}:
            restored=False
            if changed_default and observed==expected and default_branch(remote)=='main':
                try: set_default_branch(remote,initial_default); restored=True
                except PublishError: pass
            raise PublishError('Atomic push failed; inspect the remote. Previous default restored: '+str(restored)+'. Branch refs were not force-rewritten.') from None
    require(remote_heads(remote)=={'main':head},'Push completed but final remote-head verification differs; inspect remote before doing anything else')
    require(default_branch(remote)=='main', 'Remote refs published but default-branch verification differs; inspect GitHub')
    git(['fetch','--prune','origin'],destination)
    local=git(['for-each-ref','--format=%(refname:short)','refs/heads/'],destination).stdout.splitlines()
    require(local==['main'],'Unexpected local branches in publication clone')
    return {'status':'PUBLISHED_MAIN_ONLY','commit':head,'remote':remote,'checkout':str(destination),
            'files':len(files),'deleted_remote_branches':[CAMPAIGN,UPGRADE],
            'history_rewritten':False,'default_branch':'main','live_research_access':'NOT_TESTED_BY_PUBLICATION'}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--apply',action='store_true')
    p.add_argument('--destination',type=Path,required=True)
    p.add_argument('--git-name');p.add_argument('--git-email')
    a=p.parse_args()
    try:
        print(json.dumps(publish(Path(__file__).resolve().parents[1],a.destination,apply=a.apply,name=a.git_name,email=a.git_email),indent=2));return 0
    except (PublishError,OSError,ValueError) as exc:
        print(json.dumps({'status':'STOPPED','error':str(exc),'note':'No destructive fallback or force-history rewrite was attempted.'}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
