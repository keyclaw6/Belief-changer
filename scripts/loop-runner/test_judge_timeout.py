#!/usr/bin/env python3
import subprocess, sys, tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parent))
import judge_replicate as j
d = Path(tempfile.mkdtemp()); out = d / "response.md"
with patch.object(j.subprocess, "run", side_effect=subprocess.TimeoutExpired("a", 1)):
    assert j.run_agent("p", out, "lane-ch01") is False
assert not out.exists() and "TIMEOUT" in (d / "response.md.partial").read_text()
print("ok")
