# Reframe 1.0: anyone can try it

The owner's direction (26 November 2026): release Reframe officially, as version 1.0.0, so anyone can try it and find it useful. This document is the specification and plan for that release. The owner's decisions are in section 7, all agreed on 26 November 2026.

## 1. Goal

Someone who finds the repository can, in this order:

1. **see what it makes, with nothing installed:** the CardDemo reports, open in the browser;
2. **run it on their own code with only Claude:** no AWS account, no AWS Transform;
3. **add AWS Transform when they have it:** the two assessments side by side, reconciled against the code, as today;
4. **share the results their way:** a folder, their AWS account or GitHub Pages, each optional.

## 2. Claude-only mode (C1-01 to C1-05)

Today `reframe run` starts with AWS: the snapshot goes to an S3 bucket, AWS Transform runs, and the Claude assessment needs the run's resources (its Neptune graph). A Claude-only run needs none of that.

```bash
reframe run --tools claude --source <folder | file.zip | github-url>
```

The guided run asks "AWS Transform and Claude, or Claude only?", and Claude only skips the AWS profile and sign-in questions.

| Stage | With AWS Transform | Claude only |
|---|---|---|
| Prerequisites | Git, AWS CLI, Terraform, the MCP server, Claude Code | Git and Claude Code |
| Snapshot | in the run folder, and uploaded to the run's bucket | in the run folder only |
| AWS resources | the run's bucket, sandbox role, Neptune graph | none, so no teardown |
| Claude assessment | the plugin, Reframe's requirements (C6), the graph loaded into Neptune (C7) | the same, without C7: the graph stays a file, `outputs/claude/graph.nq` |
| Business review | AWS Transform's and Claude's | Claude's |
| Comparison | the two tools | none |
| The frame | AWS Transform's domains and business functions | Claude's domains and the functions Reframe wrote in C6 |
| Reconciliation | groups decided against the code; one-sided rules checked | every rule is one-sided, so every rule is checked against the code (`kept`, `rejected` or `needs_sme`), with the same evidence checks, confidence and SME list |
| Design and package | from the reconciled results | the same |
| Publish | all of it | all of it |

The home screen, `reframe status` and the next-step hints say which tools a run uses, and offer only the steps that apply. `reframe claude` on a Claude-only run is the assessment itself; `reframe compare` says there is nothing to compare.

**Cost.** The reconciliation checks every Claude rule, not just the disputed ones. On CardDemo that is about 300 rules: roughly 35 batches, 15 to 40 minutes and about $15 to $40 at API prices.

| Story | Done when |
|---|---|
| C1-01 A run without AWS | `reframe run --tools claude` takes the snapshot, writes no AWS records, and the home screen, status and teardown treat it as Claude-only |
| C1-02 The Claude assessment alone | The plugin, C6 and the report run on a Claude-only run; C7 is skipped with its reason |
| C1-03 Reconciliation from one tool | Pipeline 3 runs with Claude's frame, checks every rule against the code, and writes the same page, SME list and requirements |
| C1-04 Design and publish | `reframe design` and `reframe publish` work unchanged on a Claude-only run |
| C1-05 Live on a second codebase | A Claude-only run of a second, smaller test codebase, from `reframe run` to the package, with no AWS profile set |

## 3. Publishing to GitHub Pages, optional (S-16, S-17)

**S-16 `reframe publish --to pages`.** It is for people who want a link to send, with nothing to install.

```bash
reframe publish --to pages --repo <owner>/<name>
```

- It writes the cleaned copy, exactly as `--to <folder>` does, to the repository's `gh-pages` branch, under `<project>/<run>/`, with an index of every published run. It does this with Git and `gh`, using the person's own GitHub sign-in.
- It turns GitHub Pages on for that branch if it is off, then prints the address.
- **A Pages site is public**, on a public repository and on most private ones. Before anything is pushed, Reframe says so, names the repository and the address, and asks the person to type `yes`. With no terminal it refuses.
- Nothing else changes: publishing stays optional, and `--to <folder>` and `--to aws` are as they are.

**S-17 The demo.** This repository's own Pages site serves `reports/` (CardDemo only: other test codebases are run locally and nothing from them is committed, the owner's decision of 26 November 2026): a GitHub Actions workflow deploys it on every push to `main`. The README's first screen links to it. The demo is optional for anyone forking the repository: the workflow runs only where Pages is turned on.

## 4. A repository that explains itself (R1-01 to R1-04)

| Story | Done when |
|---|---|
| R1-01 README | The first screen says what Reframe is, who it is for and what it makes. It shows badges (CI, release, Python, license), the live demo, and a five-minute quick start for Claude only and for both tools. The detail moves to `docs/` (guides per pipeline), so the README is about 150 lines and every link resolves |
| R1-02 Package metadata | `pyproject.toml` has version 1.0.0, a current description, project URLs, classifiers and the license. `uv tool install git+https://github.com/sknampally/reframe` installs it |
| R1-03 Contributing | `CONTRIBUTING.md` (set-up, tests, the change-control flow), `CHANGELOG.md` (0.3.0 to 1.0.0), bug and feature issue templates, and `SECURITY.md` kept |
| R1-04 A clean machine | On a fresh macOS user account and in a Linux container: install from GitHub, then `reframe --help`, `reframe setup` (its checks), a Claude-only run of the second test codebase, and `reframe publish --to <folder>` |

### Results (R1-04, 26 November 2026)

- **Linux:** a clean `python:3.12-slim` container, with the built wheel.
  - It installs, and `--version` and `--help` work.
  - `reframe publish` of the second codebase's run writes all 453 pages, to a local folder.
  - 351 of 360 offline tests pass. The 9 that error call `git`, which the slim image lacks; Git is one of Reframe's prerequisites.
- **macOS:**
  - `uv tool install "git+https://github.com/sknampally/reframe@<branch>"` into an empty tool folder installs 1.0.0, with `--tools` and `--to pages`.
  - The wheel installs in a clean virtual environment and finds its templates.
  - A fresh user account was not made: that needs the Mac's administrator. CI's macOS jobs, with Python 3.10 to 3.13, run the tests on a clean runner instead.
- **Found and fixed:** `reframe run --source …` with the default `--tools both` started AWS Transform only, because only the guided run added Claude. It now starts both, and `--tools aws` keeps the old behaviour.

## 5. Acceptance before the release (A1-01)

From the CLI only, each from `reframe run` to `reframe publish` and teardown, without any stop that needs a fix in the code:

- CardDemo with both tools, from its GitHub URL;
- the second test codebase with both tools, from its ZIP file;
- the second test codebase with Claude only (C1-05).

Only CardDemo's results are published. The second codebase's runs are kept locally.

Each run's time, agent count and cost are recorded in the plan. A stop because of a usage limit or an expired sign-in is fine: `reframe resume` must carry on without repeating work. Any other stop is fixed, and that run is repeated.

## 6. The release (REL-1)

After the owner's go-ahead: merge `develop` into `main`, tag `v1.0.0` on `main`, and publish a GitHub release with notes from `CHANGELOG.md`.

## 7. The owner's decisions

| Decision | Choice |
|---|---|
| Version | **v1.0.0** (agreed 26 November 2026) |
| Scope | Claude-only mode, optional Pages publishing with the demo, the repository clean-up, and end-to-end runs first (agreed 26 November 2026) |
| Claude-only frame | **Claude's domains** and the functions Reframe already writes in C6, with no new model step (agreed with the reconciliation choice) |
| Claude-only reconciliation | **Every Claude rule is checked against the code**, as one-sided rules are today (agreed 26 November 2026). Taking Claude's rules unchecked would be cheaper, but the P3-11 audit found the errors were in unchecked rules |
| Pages publishing | **Push to `gh-pages`** (agreed 26 November 2026): `reframe publish --to pages --repo <owner>/<name>` pushes to `gh-pages` with the person's GitHub sign-in, after they type `yes` to a warning that the site is public. It is optional, like every publish |
