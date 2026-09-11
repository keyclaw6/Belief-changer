"""Guarded legacy command entrypoints. No old mutable-plan fallback exists."""
import os
from pathlib import Path
import sys
from .common import FactoryError
from .cli import main

def legacy_role(role):
    run=os.environ.get('BC_RUN')
    if not run:
        print('Retired campaign-001 entrypoint. Use scripts/factory.py with a frozen v2 run; BC_RUN is required. No paid calls made.',file=sys.stderr)
        return 2
    repo=os.environ.get('BC_REPO',str(Path(__file__).resolve().parents[2]))
    args=['--repo',repo,'task','--run',run,'--role',role]
    if role in ('writer','chapter-reviewer','state-editor'):
        chapter=os.environ.get('CHAPTER')
        if not chapter:
            print('CHAPTER is required; no implicit whole-book loop.',file=sys.stderr);return 2
        args+=['--chapter',chapter]
    if os.environ.get('ROUND'):args+=['--round',os.environ['ROUND']]
    return main(args)
