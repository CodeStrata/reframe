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
- **No secrets, no client data.** Read [SECURITY.md](SECURITY.md) before you attach logs, screenshots or examples. Use the public samples (CardDemo, GenApp) or clearly labelled synthetic data.

## Pull requests

- Say what changed and why, and what you checked, using the template.
- Keep each pull request to one purpose.
- Say when AI helped write it.

## Reporting a problem

Open an issue with the bug template: what you ran, what you expected, and what happened. Include `reframe --version` and the run's `reframe status`, with account IDs and paths removed. Report a security problem privately, as [SECURITY.md](SECURITY.md) says, not in an issue.
