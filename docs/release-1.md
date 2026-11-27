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

### Results (C1-05, 26 November 2026)

The second test codebase with Claude only (run 3095b6, from its ZIP file), with the CLI alone and no AWS profile. Every stage worked:

| Stage | Result | Cost at API prices |
|---|---|---|
| `reframe run --tools claude` | Snapshot, preflight without AWS, then the plugin's preflight, assess, map and extract-rules: 103 rule cards. Reframe's requirements ran over Claude's 9 domains and 22 functions, and Claude's business review was built. | $42.95, including $11.98 for the extraction attempt the usage limit cut short |
| `reframe reconcile` | 103 one-tool units in 14 batches, under the batch limit (estimate 4 to 12 minutes, $7 to $16). 102 kept and 1 for an SME: 220 recommended rules, all cited by 254 requirements, with 32 decision tables, 43 SME questions from 49, and 36 possible defects. The page says the run used Claude only and links to no comparison. | $18.63 |
| `reframe design` | 15 journeys (1 screen unused), 13 modern screens, 68 specifications (all draft, since nothing is signed off), 2 data contracts and package v1, with 0 problems in every stage, in 17 minutes. `--package` copied 511 files, and `--check` lists 85 placeholders. | $9.54 |
| `reframe publish --to <folder>` | 528 pages: Claude's review, the reconciliation and the design. No AWS review, no comparison, 0 broken links, no local paths. | none |
| `reframe teardown` | "It created no AWS resources, so there is nothing to tear down." | none |

**Found and fixed: a usage limit read as a failure.** Rule extraction hit Claude's 5-hour usage limit. Claude Code then wrote an empty *success* result for a background task's notice, and Reframe, reading only the last line, recorded FAILED. The step's answer is now the last result that is not such a notice, and a usage-limit result anywhere makes the step a limit stop. `reframe resume` after the reset finished the run, with no work repeated.

**Seen, not a fault:** Claude's plugin puts the codebase's screens in a domain of their own, *3270 presentation*, so all of the run's journeys sit in that one domain. With both tools, the journeys follow AWS Transform's business domains instead.

## 5. Acceptance before the release (A1-01)

From the CLI only, each from `reframe run` to `reframe publish` and teardown, without any stop that needs a fix in the code:

- CardDemo with both tools, from its GitHub URL;
- the second test codebase with both tools, from its ZIP file;
- the second test codebase with Claude only (C1-05).

Only CardDemo's results are published. The second codebase's runs are kept locally.

Each run's time, agent count and cost are recorded in the plan. A stop because of a usage limit or an expired sign-in is fine: `reframe resume` must carry on without repeating work. Any other stop is fixed, and that run is repeated.

### Results: the second test codebase with both tools (A1-01, 26 and 27 November 2026)

Run 8f53b4, from `reframe run --source <its ZIP file> --project <name> --max-agents 650`, which now starts both assessments. It reached the end, but not without interruption. Every stop it made was fixed in Reframe or resumed:

| Stage | Result |
|---|---|
| AWS Transform | All 9 plan steps succeeded, and the results and business review were built. It was stuck for about four hours at *Discover business functions* (fix 2). |
| Claude | Preflight, assess, map and extract-rules: 109 rules and 314 requirements, with the graph loaded into Neptune (5,318 quads, 54 rules joined to AWS's programs) and the comparison built. It stopped once at Claude's usage limit, reported correctly as a limit stop thanks to C1-05's fix, and resumed. |
| Teardown | 40 resources. The first attempt stopped partway when the Mac lost DNS. The second deleted only the 10 left, and the check found nothing still in AWS. |
| Reconciliation | 248 units decided against the code and 9 rules agreed by both tools: 466 recommended rules, all cited by 392 requirements, 36 decision tables, 138 SME questions and 70 possible defects. |
| Design | 11 journeys, 10 modern screens, 67 specifications and 2 contracts, with 0 problems. Package v1 has 504 files, and `--check` lists 85 placeholders. It stopped once at Claude's usage limit and was continued with `reframe design`. |
| Publish | 523 pages: AWS's review, Claude's, the comparison, the reconciliation and the design, with 0 broken links. |

Claude's cost at API prices was about $85: assessment $36.79, comparison $1.53, reconciliation $36.59, design $9.91.

**Found and fixed:**
1. **The "already in progress" loop.** AWS said the reimagine was initiated but added no steps to its plan. After that, every six minutes, its review form reopened; Reframe submitted it, AWS asked for the selection, and then refused the same selection as a second request. Once AWS refuses a selection this way, Reframe now stops resubmitting the form and asks once, in plain words, what is running and to start again. Live, AWS's readiness menu came back, and its Proceed added the steps and started the plan. A second refusal waits for the person.
2. **"Not configured" read as an expired sign-in.** The AWS Transform MCP server's start-up region probe sometimes failed for us-east-1 with an empty error. Reframe then stopped the run as an expired sign-in, although the AWS CLI sign-in was valid. The client now starts a new server after 5, 15 and 30 seconds before giving up.
3. **Two design rounds at once.** A round was started in a terminal while another was running on the same run. Rounds now take the run's design lock.

## 6. The release (REL-1)

After the owner's go-ahead: merge `develop` into `main`, tag `v1.0.0` on `main`, and publish a GitHub release with notes from `CHANGELOG.md`.

## 7. The owner's decisions

| Decision | Choice |
|---|---|
| Version | **v1.0.0** (agreed 26 November 2026) |
| Licence | **MIT** (the owner, 27 November 2026): Reframe stays open source under the MIT License, so anyone, the owner's own later work included, can use and improve it. A move to the AGPL, merged on 26 November, was reverted before 1.0 |
| Published examples | **CardDemo only** (the owner, 26 November 2026), with its Apache-2.0 licence and notice; other test codebases are run locally and nothing from them is committed |
| Scope | Claude-only mode, optional Pages publishing with the demo, the repository clean-up, and end-to-end runs first (agreed 26 November 2026) |
| Claude-only frame | **Claude's domains** and the functions Reframe already writes in C6, with no new model step (agreed with the reconciliation choice) |
| Claude-only reconciliation | **Every Claude rule is checked against the code**, as one-sided rules are today (agreed 26 November 2026). Taking Claude's rules unchecked would be cheaper, but the P3-11 audit found the errors were in unchecked rules |
| Pages publishing | **Push to `gh-pages`** (agreed 26 November 2026): `reframe publish --to pages --repo <owner>/<name>` pushes to `gh-pages` with the person's GitHub sign-in, after they type `yes` to a warning that the site is public. It is optional, like every publish |
