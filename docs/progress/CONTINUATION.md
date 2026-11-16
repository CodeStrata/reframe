# Continuation notes

Read this first if work on `feature/agreed-workflow` resumes in a new session.

## State

- Branch `feature/agreed-workflow`, created from `origin/develop` at `b534f85`.
- Completed: #160 baseline documents.
- In progress: milestone M1 (#161 version manifest, #162 typed stops, #163 operation lifecycle, #34 approval supersession, #164 migration).

## How to run

1. Create a disposable environment outside the checkout: `uv venv --python 3.12 <dir>/.venv` then `uv pip install --python <dir>/.venv/bin/python -e .`.
2. Isolate configuration: set `HOME`, `REFRAME_CONFIG_HOME`, and `TMPDIR` to scratch directories; set `AWS_CONFIG_FILE` and `AWS_SHARED_CREDENTIALS_FILE` to `/dev/null`; unset provider keys. Put stubs for `aws`, `claude`, `codex`, `tofu`, `terraform`, `uvx`, `kiro`, `kiro-cli` first on `PATH`.
3. Call the environment's interpreter by absolute path (a shell alias for `python` can override `PATH`).
4. `PYTHONPATH=tests <venv>/bin/python -m unittest discover -s tests`.

## Rules carried forward

- No live AWS or provider calls; no merge to develop or main; Done issues stay unchanged.
- Commits use the owner's identity without agent trailers (CONTRIBUTING.md); the PR discloses AI assistance.
- Keep #169, #173, #26, #41, #42 open until live (L3) evidence exists.
