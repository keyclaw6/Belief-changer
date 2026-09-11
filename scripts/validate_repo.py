#!/usr/bin/env python3
"""Active-contract and test-presence gate. Does not claim factual/book quality."""
import json
from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()

def main():
    required = ['AGENTS.md','README.md','docs/FACTORY-V2.md','docs/UPGRADE-MAP.md',
                'scripts/factory.py','scripts/bc_factory/schema.py','scripts/bc_factory/runs.py',
                'scripts/bc_factory/experiments.py','factory/config.json','factory/champion.json',
                'factory/calibration.json','loop/judges/pairwise.md','prompts/evidence-reviewer.md',
                'prompts/book-editor.md','prompts/final-auditor.md']
    errors = [f'Missing required v2 file: {p}' for p in required if not (ROOT/p).is_file()]
    tests = list((ROOT/'scripts/eval/tests').glob('test_*.py'))
    if not tests: errors.append('Mandatory regression suite is absent')
    for rel in ['README.md','AGENTS.md','prompts/style-guide.md','prompts/chapter-reviewer.md','loop/PROGRAM.md']:
        if not (ROOT/rel).exists(): continue
        text=(ROOT/rel).read_text()
        for bad in ["Score 100 only when OUR BOOK", "OVERCLAIM governs facts, not the assigned method promise", "the CAPS name then carries the definition in every sentence"]:
            if bad.lower() in text.lower(): errors.append(f'Forbidden retired runtime contract in {rel}: {bad}')
    if (ROOT/'prompts/style-guide.md').exists() and len((ROOT/'prompts/style-guide.md').read_text().split()) > 2500:
        errors.append('House contract exceeds 2500-word maintenance budget; move optional analysis out of runtime')
    if (ROOT/'factory/config.json').exists():
        cfg=json.loads((ROOT/'factory/config.json').read_text())
        if cfg.get('schema_version') != 2: errors.append('Wrong runtime config version')
        external=cfg.get('profiles',{}).get('external')
        if external and external.get('family') == cfg['profiles']['factory'].get('family'):
            errors.append('External profile duplicates generating family')
    if errors:
        print('\n'.join(errors),file=sys.stderr);return 1
    print(f'Runtime contracts present; {len(tests)} mandatory test module(s).')
    return 0
if __name__=='__main__': raise SystemExit(main())
