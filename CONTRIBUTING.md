# Contributing to Reframe

Thank you for helping. Bug reports, ideas and pull requests are all welcome.

## Set up

You need macOS or Linux, Python 3.10 or later, and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/sknampally/reframe.git
```

```bash
cd reframe && uv sync
```

```bash
uv tool install --reinstall --editable .
```

The editable install puts `reframe` on your PATH, running the code in your clone.

## Run the tests

The tests are offline. They need no AWS account, no Claude sign-in and no network, and they run on every pull request on Linux and macOS with Python 3.10 to 3.13.

```bash
uv run python -m unittest discover -s tests -t .
```

Every change comes with tests. Anything that calls AWS, Claude Code, `git` or `gh` is tested against a fake that records the calls. The existing `tests/` folders show how.

## Run the checks

CI also lints, type-checks and holds a coverage floor. The checkers are pinned in the `dev` extra:

```bash
uv pip install -e ".[dev]"
```

```bash
ruff check src tests
```

```bash
mypy
```

```bash
coverage run -m unittest discover -s tests -t . && coverage report
```

- **ruff** checks for real faults, not style: pyflakes, syntax errors and bugbear (`[tool.ruff.lint]` in `pyproject.toml`).
- **mypy** checks every module except those listed under `[[tool.mypy.overrides]]`, which still have type errors to fix. The list only shrinks: when you fix a module, take it off.
- **coverage** fails below the floor in `[tool.coverage.report]`. Raise the floor when your tests raise coverage; never lower it.

## How a change is made

Reframe changes in this order. Each step is written down before the next starts:

1. **Specification.** What the change does, and why, in the pipeline's document under `docs/`: for example `pipeline-3.md`, `pipeline-4.md`, `sharing.md` or `release-1.md`.
2. **Plan.** One row per story in [docs/plan.md](docs/plan.md), each with what *done* means.
3. **Stories.** An issue per story.
4. **Build.** A branch from `develop`, one commit per story, and a pull request into `develop`. `main` is the released branch.

For a small fix, an issue and a pull request are enough.

## Conventions

- **Plain words.** Commands, messages and pages say what happens in words a business reader understands. Say it once, and don't invent jargon.
- **Nothing outward without a record.** Every change Reframe makes outside the run folder has an intent, a receipt and a way to settle it after a crash. Anything that deletes, or makes something public, asks for a typed `yes` first.
- **Model output is labelled.** Pages say what a model wrote and what Reframe checked.
- **No secrets, no client data.** Read [SECURITY.md](SECURITY.md) before you attach logs, screenshots or examples. Use a public sample such as CardDemo, or clearly labelled synthetic data, and attach only what Reframe wrote, not the sample's own source.

## Pull requests

- Say what changed and why, and what you checked, using the template.
- Keep each pull request to one purpose.
- Say when AI helped write it.

## Licensing your contribution

Reframe is under the [MIT License](LICENSE). By opening a pull request you agree that your contribution is your own work, or that you have the right to submit it, and that it is licensed under the MIT License like the rest of Reframe.

## Reporting a problem

Open an issue with the bug template: what you ran, what you expected, and what happened. Include `reframe --version` and the run's `reframe status`, with account IDs and paths removed. Report a security problem privately, as [SECURITY.md](SECURITY.md) says, not in an issue.
