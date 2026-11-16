# Continuation notes

Read this first if work on `feature/agreed-workflow` resumes in a new session.

## State

- Branch `feature/agreed-workflow`, created from `origin/develop` at `b534f85`. Acceptance candidate `d65d86f` (frozen checkout `../candidate-d65d86f`).
- Implemented and tested offline: every M1–M5 story in the completion matrix (docs/validation/completion-matrix.md). Live work is not done: #169, #173, #197, #26, #41, #42 stay open.
- Review package: docs/validation/review-package.md. Independent acceptance report: docs/validation/acceptance-report.md.
- Explicit checks: `REFRAME_WHEEL_CHECK=1 REFRAME_UV=<uv>` runs tests/test_installed_wheel.py; the clean snapshot runs the fresh-start journey (`test_clean_snapshot_passes_and_a_dirty_tree_is_refused`).
- Acceptance harness: `acceptance/harness.py` (run it from a clean candidate checkout).
- Never commit from a shell that sourced the isolated env.sh: it sets a test Git identity.
- The isolated `TMPDIR` sits inside another repository's working tree. A test must never run a Git write command in a fixture folder; stub `pilot.git` instead. (One test did once; the two staged paths were unstaged and nothing else changed.)
- Round two (`351d34c`) failed; its defects N1–N9 and the D12–D14 leftovers are fixed on the branch except N9 (see docs/validation/acceptance-defects.md). Round three (`fd0e4c8`) failed narrowly with R3-1 to R3-10, all fixed on the branch. Next: freeze a new candidate and run acceptance round four.

## How to run

1. Create a disposable environment outside the checkout: `uv venv --python 3.12 <dir>/.venv` then `uv pip install --python <dir>/.venv/bin/python -e .`.
2. Isolate configuration: set `HOME`, `REFRAME_CONFIG_HOME`, and `TMPDIR` to scratch directories; set `AWS_CONFIG_FILE` and `AWS_SHARED_CREDENTIALS_FILE` to `/dev/null`; unset provider keys. Put stubs for `aws`, `claude`, `codex`, `tofu`, `terraform`, `uvx`, `kiro`, `kiro-cli` first on `PATH`.
3. Call the environment's interpreter by absolute path (a shell alias for `python` can override `PATH`).
4. `PYTHONPATH=tests <venv>/bin/python -m unittest discover -s tests`.

## Rules carried forward

- No live AWS or provider calls; no merge to develop or main; Done issues stay unchanged.
- Commits use the owner's identity without agent trailers (CONTRIBUTING.md); the PR discloses AI assistance.
- Keep #169, #173, #26, #41, #42 open until live (L3) evidence exists.
