# Reframe

**From mainframe source to reviewed requirements, business rules and a design to build from.**

[![CI](https://github.com/sknampally/reframe/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sknampally/reframe/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/sknampally/reframe?sort=semver)](https://github.com/sknampally/reframe/releases)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-3776ab)](pyproject.toml)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-blue)](LICENSE)
[![Live demo](https://img.shields.io/badge/demo-CardDemo-8250df)](https://sknampally.github.io/reframe/)

Reframe reads a COBOL and CICS codebase and tells you, in plain words a business can review, what it does. It assesses the code with Claude's [code-modernization plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization), and with AWS Transform as well if you have it, then checks every business rule against the source code itself. From that it designs the modern application, down to a package an AI coding tool can build from.

It is for modernization teams, architects and the business people who have to say "yes, that is what the system does" before anything is rebuilt.

**See what it makes, with nothing to install:** [CardDemo](https://sknampally.github.io/reframe/carddemo/) (AWS's sample, 44 COBOL programs), run end to end.

## What it makes

- **Business reviews:** domains, business functions, capabilities, requirements, business rules and open questions, from overview down to each rule. Reviewers mark *Agree*, *Needs change* or *Question* and send their marks back.
- **Rules checked against the code:** each recommended rule cites the source lines that back it. Each has a confidence Reframe sets from what it checked, a kind and worked examples. Possible defects are noted.
- **One SME list:** every question the code cannot settle, with the rules it holds up, to answer and feed back into the next round.
- **The design:** legacy screens and how they connect, user journeys, modern screens with every legacy field mapped, and a clickable prototype beside the legacy screens. A final specification for every capability, with acceptance criteria and data contracts.
- **An AI-DLC package:** the specifications in Kiro, Claude Code and Spec Kit form, with every ID traced back to the legacy source, a golden dataset per capability for equivalence tests, and a `START-HERE.md` for the team that builds it.

## How it works

![How a Reframe run works: the snapshot, the two assessments side by side, the reports, the reconciliation against the source code, the design, sharing and teardown](docs/images/reframe.svg)

| Step | Command | What happens |
|---|---|---|
| Assess | `reframe run` | One snapshot of the source is assessed by Claude's plugin, and by AWS Transform alongside it if you choose. Each gets a business review. |
| Reconcile | `reframe reconcile` | Claude checks every rule the tools don't describe the same way against the source code. Reframe checks that each cited line exists. Out come recommended rules, requirements and one SME list. |
| Design | `reframe design` | Journeys, modern screens, the prototype, final specifications and the AI-DLC package. A later round redoes only what new context touches. |
| Share (optional) | `reframe publish` | A copy cleaned of your account's identifiers, to a folder, your AWS account or GitHub Pages. |

Every step is recorded before it starts and confirmed after it ends, so a run that stops (an expired sign-in, Claude's usage limit) continues with `reframe resume` without repeating work.

## Quick start

You need macOS or Linux (on Windows, WSL2), Python 3.10 or later and [uv](https://docs.astral.sh/uv/).

```bash
uv tool install "git+https://github.com/sknampally/reframe@v1.0.0"
```

### With Claude only

You need [Claude Code](https://docs.anthropic.com/en/docs/claude-code), signed in with your Claude subscription. You don't need an AWS account.

```bash
reframe setup --tools claude
```

```bash
reframe run --tools claude --source https://github.com/aws-samples/aws-mainframe-modernization-carddemo
```

```bash
reframe reconcile
```

```bash
reframe design --open
```

### With AWS Transform as well

You also need an AWS account where AWS Transform is available, with an AWS CLI profile that signs in through IAM Identity Center. `reframe setup` checks the rest and offers to install it: the AWS CLI, Terraform and the AWS Transform MCP server.

```bash
reframe setup
```

```bash
reframe run
```

The guided run asks for the profile, the source (a folder, a ZIP file or a GitHub URL) and a project name, then runs both assessments in the background. `reframe status` says where a run is and what to do next. When both are done:

```bash
reframe compare --open
```

```bash
reframe reconcile
```

```bash
reframe design --open
```

```bash
reframe teardown
```

`reframe` on its own shows your runs, the suggested next step and a menu. Run every command from one folder, your workspace: each run lives in `.reframe/<project>/<run>/` there, with `inputs/` for the context you add and `outputs/` for what Reframe makes.

## What it takes

| Step | Time | At API prices, on CardDemo |
|---|---|---|
| Claude assessment | about 2 hours | the plugin's agents, on your Claude subscription, within an agent limit you set |
| AWS Transform assessment | about 1 hour, alongside Claude | AWS charges for the job and the run's resources, until `reframe teardown` |
| Reconciliation | 30 to 90 minutes | about $30 to $70 for a full round; a later round only what changed. With Claude only, every rule is checked: estimated $15 to $40 |
| Design | about 30 to 60 minutes | about $35 for a first round; a round that redoes every screen about $60 |
| Publish, package, export | seconds | none |

The figures are from live runs and are recorded in [docs/acceptance.md](docs/acceptance.md), [docs/pipeline-3.md](docs/pipeline-3.md) and [docs/pipeline-4.md](docs/pipeline-4.md). Everything Reframe writes is model output for people to review, and the pages say so.

## Documentation

| Read | For |
|---|---|
| [How to run Reframe](docs/how-to-run.md) | One page from install to handover |
| [The guide](docs/guide.md) | Every step in detail: the guided run, Claude only, results, reviews, the reconciliation, the design, sharing and teardown |
| [Commands](docs/cli.md) | Every command, option and example |
| Specifications | [The AWS Transform assessment](docs/specification.md), [the Claude assessment](docs/pipeline-2.md), [the reconciliation](docs/pipeline-3.md), [the design](docs/pipeline-4.md), [sharing](docs/sharing.md), [release 1.0](docs/release-1.md) |
| [The plan](docs/plan.md) | Every story, with what done means and the results |

## Contributing

Issues and pull requests are welcome. [CONTRIBUTING.md](CONTRIBUTING.md) says how to set up, run the offline tests and propose a change, and [SECURITY.md](SECURITY.md) how to report a problem privately. What has changed in each release is in [CHANGELOG.md](CHANGELOG.md).

**Later:** a replacement order from the specifications, real legacy outputs under GnuCOBOL, and proving it on a larger codebase and on Amazon Bedrock ([docs/plan.md](docs/plan.md)).

## License

The GNU Affero General Public License, version 3 only (AGPL-3.0-only); see [LICENSE](LICENSE) and [NOTICE](NOTICE). You may use, change and share Reframe under it. If you share a changed version, or offer it to others over a network, you share your changes under the same licence. The copyright holder also licenses Reframe on other terms, such as a commercial licence without those obligations.

Versions published before the change, v0.4.0 and earlier, stay under the MIT License.
