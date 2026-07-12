"""Minimal stdlib loader for loop/config.yaml — no PyYAML dependency.

The loop container runs a bare Python (no pyyaml), and the repo law forbids
adding heavy deps for one file. config.yaml is deliberately a flat YAML subset:
`# comments`, blank lines, `key: scalar`, and `- item` list entries that belong
to the most recent `key:` whose value was empty. Anything fancier is rejected
loudly so a malformed config fails fast instead of silently mis-parsing.

Public API:
  load(path="loop/config.yaml") -> dict   # scalars coerced to int/float/bool/str
  find_config(start=None) -> Path          # walk up for loop/config.yaml
"""
import sys
from pathlib import Path


def _coerce(value: str):
    v = value.strip()
    if v == "" or v in ("~", "null", "None"):
        return None
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    if (v[0] in "\"'") and v[-1] == v[0] and len(v) >= 2:
        return v[1:-1]
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


def load(path="loop/config.yaml") -> dict:
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"loopcfg: config not found: {p}")
    cfg = {}
    current_list_key = None
    for lineno, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split(" #", 1)[0].rstrip() if " #" in raw else raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            if current_list_key is None:
                raise SystemExit(f"loopcfg: list item with no parent key (line {lineno})")
            cfg[current_list_key].append(_coerce(stripped[2:]))
            continue
        if ":" not in line:
            raise SystemExit(f"loopcfg: not a key:value line (line {lineno}): {raw!r}")
        key, _, value = line.partition(":")
        key = key.strip()
        if value.strip() == "":
            cfg[key] = []
            current_list_key = key
        else:
            cfg[key] = _coerce(value)
            current_list_key = None
    # A key declared as an empty list but never given items stays [].
    return cfg


def find_config(start=None) -> Path:
    """Walk up from start (or cwd) for loop/config.yaml; raise if absent."""
    here = Path(start or Path.cwd()).resolve()
    for base in (here, *here.parents):
        candidate = base / "loop" / "config.yaml"
        if candidate.is_file():
            return candidate
    raise SystemExit("loopcfg: could not locate loop/config.yaml above cwd")


if __name__ == "__main__":
    import json
    target = sys.argv[1] if len(sys.argv) > 1 else str(find_config())
    print(json.dumps(load(target), indent=1))
