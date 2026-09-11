#!/usr/bin/env python3
"""Portable entrypoint. Python 3.11+; no third-party Python dependencies."""
from bc_factory.cli import main
if __name__ == "__main__":
    raise SystemExit(main())
