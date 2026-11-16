# Continuation notes

Read this first if work on `feature/agreed-workflow` resumes in a new session.

## State

- Branch `feature/agreed-workflow`, created from `origin/develop` at `b534f85`.
- Completed: #160, M1 (#161–#166, #34), requirements boundary offline (#169–#173), context and validation inputs (#174–#177), links (#181), acceptance and readiness (#187, #188, #190), isolation and installed wheel (#195). See agreed-workflow-progress.md.
- Next: design plan and inventory (#182, #183), reconciliation (#184), API completeness (#185), Reimagine deltas (#186), feedback routing (#189), route manifest (#191), skip parity (#178), coverage and questions (#179, #180), guided journey (#192), docs (#116, #115), fixtures and acceptance (#44, #194, #196), verification of the 17 Awaiting-verification items.
- Explicit checks: `REFRAME_WHEEL_CHECK=1 REFRAME_UV=<uv>` runs tests/test_installed_wheel.py (builds, installs, probes outside the repo).
- Never commit from a shell that sourced the isolated env.sh: it sets a test Git identity.

## How to run

1. Create a disposable environment outside the checkout: `uv venv --python 3.12 <dir>/.venv` then `uv pip install --python <dir>/.venv/bin/python -e .`.
2. Isolate configuration: set `HOME`, `REFRAME_CONFIG_HOME`, and `TMPDIR` to scratch directories; set `AWS_CONFIG_FILE` and `AWS_SHARED_CREDENTIALS_FILE` to `/dev/null`; unset provider keys. Put stubs for `aws`, `claude`, `codex`, `tofu`, `terraform`, `uvx`, `kiro`, `kiro-cli` first on `PATH`.
3. Call the environment's interpreter by absolute path (a shell alias for `python` can override `PATH`).
4. `PYTHONPATH=tests <venv>/bin/python -m unittest discover -s tests`.

## Rules carried forward

- No live AWS or provider calls; no merge to develop or main; Done issues stay unchanged.
- Commits use the owner's identity without agent trailers (CONTRIBUTING.md); the PR discloses AI assistance.
- Keep #169, #173, #26, #41, #42 open until live (L3) evidence exists.
