#!/usr/bin/env python3
"""Repo gate for the Belief-changer agents-native repo.

Enforces the AGENTS.md constitution: AGENTS.md presence, docs cap, root-file
allowlist, and production-books required-artifact presence. Exits non-zero on
the first violation (fail-fast). Print only on failure; quiet on success.

Run: python3 scripts/validate_repo.py [repo_root]
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

DOCS_MAX_FILES = 10

# Files permitted at the repo root (directories are governed separately).
ROOT_ALLOWED_FILES = {
    "AGENTS.md",
    "LICENSE",
    "README.md",
    "PROGRAM.md",  # self-improvement loop operator runbook (see PROGRAM.md)
    ".gitignore",
    ".mcp.json",
}

# A real (in-production) book folder under production-books/. _template is the
# scaffold, not a book. Every real book must carry these foundational artifacts.
BOOK_REQUIRED = ("00-brief.md", "README.md")


def fail(msg):
    print(f"validate_repo: FAIL — {msg}", file=sys.stderr)
    return 1


def tracked_files(root: Path) -> list[Path]:
    """Files git tracks, relative to root. Empty list if git unavailable."""
    import subprocess
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files"],
            capture_output=True, text=True, check=True,
        ).stdout
    except Exception:
        return []
    return [root / p for p in out.splitlines() if p]


def main():
    files = tracked_files(ROOT)
    if not files:
        return fail("no tracked files (not a git repo or git unavailable)")

    # 1. AGENTS.md presence
    agents = ROOT / "AGENTS.md"
    if not agents.is_file():
        return fail("AGENTS.md missing at repo root")

    # 2. docs/ file count
    docs_dir = ROOT / "docs"
    if docs_dir.is_dir():
        doc_files = [f for f in files if f.is_file() and "docs" in f.relative_to(ROOT).parts[:1]]
        if len(doc_files) > DOCS_MAX_FILES:
            return fail(f"docs/ has {len(doc_files)} files (max {DOCS_MAX_FILES})")

    # 3. Root file allowlist (files only; directories are unbounded)
    for f in files:
        parts = f.relative_to(ROOT).parts
        if len(parts) == 1 and parts[0] not in ROOT_ALLOWED_FILES:
            return fail(f"unsanctioned root file: {parts[0]}")

    # 4. production-books/<slug>/ required artifacts (excludes _template)
    pb = ROOT / "production-books"
    if pb.is_dir():
        for sub in sorted(pb.iterdir()):
            if not sub.is_dir() or sub.name == "_template":
                continue
            for art in BOOK_REQUIRED:
                if not (sub / art).is_file():
                    return fail(f"production-books/{sub.name}/ missing required artifact: {art}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
