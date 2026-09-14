# Research access and repository compaction — v2.1 verification

Verified 2026-09-11. Base: `6a90ffcdddad3c908144014cc41e51d693df7f9e`.

## Implemented and tested

- Mandatory source gate: **141 tests passed**, exit 0: 80 existing v2 tests, 47 research/access/retention tests, 14 publication tests.
- The end-to-end synthetic factory demo passed with zero live model calls. Output remains `COMPLETE_UNRELEASED`, `fixture: true`; effectiveness is not measured.
- Offline research preflight returned `BLOCKED`, all twelve checks false, and exit 2. It cannot masquerade as a live authenticated check.
- Bootstrap's default invocation returned an installation plan without downloads or installation.
- Tests cover stale and wrong-subject reports, login failures, challenge failures, missing dependencies, malformed results, secret redaction, dangerous archive entries and misleading research coverage.
- Publication tests use real local Git repositories: ancestry preservation, tested source overlay, only-main result, concurrent-update refusal, atomic branch deletion, default-branch migration and rejection rollback. GitHub calls are mocked in these local tests.
- All **146** retained decision/hypothesis/change files are byte-identical to the base archive. The compact index covers **51 entries: baseline 000 plus iterations 001–050**.
- All **six** current/original vision and strategy documents are byte-identical to the base archive; their hashes are in `loop/history/compaction.json`.
- **30,341 original files removed; 496 original files retained.** New integration, tests and delivery documentation are additional files.

## Limits and execution status

No live X or Reddit login, browser session, CAPTCHA solve, paid model call, research campaign, or human-reader test was performed in this session. Browser/service interactions in regression tests are simulated. Installation and the twelve live checks must run on the campaign computer before it can prepare a real book run. This is integration verification, not evidence that upstream websites are currently accessible from that computer.

The connected tools in this session were read-only. **No GitHub branch, default branch, pull request or commit was changed.** The verified publication command in `docs/PUBLISH-MAIN.md` must be run on an authenticated computer. Its checked remote state has three branches and `campaign-001` as default. It refuses changed heads rather than overwriting intervening work. Git history is retained, not rewritten.

## Reproduce

```bash
bash scripts/check.sh
python3 scripts/factory.py demo --output /path/to/new/demo-directory
python3 scripts/factory.py research-bootstrap
python3 scripts/factory.py research-preflight --subject quit-smoking
# The last command intentionally exits 2 without --live and local authorized setup.
```

This sandbox's regular scratch filesystem does not support `fsync`; the tests and synthetic runtime were executed with `TMPDIR=/dev/shm`, where durability operations work. The production atomic-write/durability code was not weakened and is unchanged from the base. Use a normal filesystem supporting atomic rename and fsync on the campaign host.

The delivery archive regenerates its per-file SHA-256 manifest and checks ZIP integrity. An external delivery verification report records the final ZIP hash and the subsequent extracted-copy checks; no circular self-checksum is claimed here.
