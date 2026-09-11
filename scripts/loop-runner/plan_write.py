#!/usr/bin/env python3
"""Legacy name; constructs a guarded v2 planner task only. Never uses old file markers."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bc_factory.compat import legacy_role
from bc_factory.schema import finding_types, FINDINGS
MAX_REWRITES = 3
if __name__=='__main__': raise SystemExit(legacy_role('planner'))
