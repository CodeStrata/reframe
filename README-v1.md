# Reframe

**From legacy mainframe code to evidence-backed modernization plans.**

Reframe is an open-source CLI for understanding mainframe applications before rebuilding them. It connects pinned source code to AWS Transform assessments, optional independent AI review, human decisions, HTML wireframe drafts, and AI-assisted development lifecycle (**AI-DLC**) handoff packages.

**Reframe prepares a modernization project; it does not translate the application into production code, deploy a target system, or prove runtime equivalence.** The target language and architecture are decisions for the implementing team.

[![CI](https://github.com/sknampally/reframe/actions/workflows/ci.yml/badge.svg)](https://github.com/sknampally/reframe/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-POC%20%7C%20offline--tested-orange)](docs/limitations.md)

> **v1 is frozen.** This is the v1 CLI (`reframe`), kept as a pinned release and readable archive on `main`. Reframe v2 is being built on the [`v2` branch](https://github.com/sknampally/reframe/tree/v2) from its [specification](docs/v2/specification.md), as a separate package (`reframe_v2`, command `reframe-v2`) in [`v2/`](v2/). v1 receives no new features; it is retired once v2 passes phase P3 of the [plan](docs/v2/plan.md).

> **Project maturity:** The CLI and offline workflows have been exercised with fixtures. A CardDemo AWS assessment has reached a human-review gate, but uninterrupted live AWS/provider acceptance, production application buildout, and behavioral equivalence are **not** established. Generated implementation packages remain drafts until required reviews and evidence gates are satisfied.

## Why Reframe?

Modernizing COBOL, CICS, VSAM and JCL is not simply converting syntax. Teams must recover business rules, data semantics, screen behavior, batch dependencies, operational assumptions and the decisions that exist outside the code. AI-generated documents can accelerate discovery, but need traceable evidence and human approval.

Reframe organizes that work into a controlled, repeatable preparation flow:

- **Source-first:** Pin a Git repository revision or supplied source package and preserve provenance.
- **Assessment-backed:** Use AWS Transform to inventory and analyze the mainframe workload.
- **Reviewable:** Optionally run an executor and independent reviewer; keep unresolved findings visible.
- **Human-informed, not human-dependent:** Add business clarifications and future-state ideas when available. Source-only draft preparation remains possible.
- **Mode-aware:** Prepare *Functional Parity* or *Reimagine* design drafts without confusing intended changes with verified legacy behavior.
- **Portable handoff:** Export HTML previews and AI-DLC packages for a subsequent implementation team.

## How it works

Reframe is an orchestrator. It runs on your workstation, drives an AWS Transform assessment, hands bounded evidence to separate AI agents, and stops for a person at every approval.

![Reframe orchestrator hub: source in, AI-DLC package out, AWS Transform and people above, and the executor, reviewer and wireframe agents below](docs/images/orchestration-layer.svg)

| Part | Runs as | What it does |
| --- | --- | --- |
| **Orchestrator** | The `reframe` CLI on your machine | Pins the source revision, uploads it to AWS Transform, seals the findings, gives each agent only the evidence it needs, enforces the model-call budget, records approvals and writes the packages. It is the only part that touches files or AWS. |
| **AWS Transform** | Your AWS account, in a private sandbox | Inventories programs, data and jobs, generates technical documentation and extracts business rules. |
| **Executor agent** | Claude Sonnet by default (Codex or Kiro optional) | Reads the source and the AWS findings and writes a candidate specification, with every rule cited to a file and line. |
| **Reviewer agent** | Claude Opus, always a different model from the executor | Checks the candidate against the same evidence and returns `PASS`, `REWORK` (back to the executor) or `BLOCKED` (needs a person). |
| **Wireframe agent** | Codex or Claude, your choice | Turns the approved specification into linked HTML wireframes, an API reference and OpenAPI contracts. |
| **People** | You and your reviewers | Approve the assessment, answer SME questions, approve the specification and the wireframes. A model's `PASS` never counts as approval. |

The agents run with no tools, so they cannot read files, call AWS or change anything. They return JSON, and the orchestrator decides what happens next.

A run moves through four phases: assess, validate, wireframes and package, with a human approval after each of the first three. After the assessment is approved you choose a route. **Skip** goes straight to draft wireframes and a draft AI-DLC ZIP, built from the AWS findings alone and labelled unverified. **Review** runs phases 2 to 4 and is the only route that produces the approved package. Every step is saved, so you can stop at any point and continue later. See the [four-phase workflow](docs/four-phase-workflow.md) and [multi-agent workflow](architecture/multi-agent-workflow.md) for more detail.

## How to run

**Supported workstations:** macOS or Linux. On Windows, use Ubuntu under WSL2.

### 1. Install the tools

| Tool | Needed for | Check it with |
| --- | --- | --- |
| Git | Always | `git --version` |
| uv with Python 3.10+ | Always | `uv --version` |
| AWS CLI v2 | Running an assessment | `aws --version` |
| OpenTofu 1.5+ | Creating the AWS sandbox | `tofu version` |
| Claude Code CLI | Executor and reviewer agents | `claude --version` |
| Codex CLI | Only if Codex writes the wireframes | `codex --version` |
| Kiro CLI | Only if Kiro is the executor | `kiro-cli --version` |

The [platform installation guide](docs/platform-install.md) and [engineer setup guide](docs/engineer-setup.md) have install commands for each tool and fixes for PATH problems.

### 2. Sign in

Sign in to each service you will use. Reframe checks these, but it never collects credentials itself.

```bash
aws sso login --profile your-profile
```

```bash
claude auth login
```

```bash
codex login
```

`aws sts get-caller-identity --profile your-profile` confirms the AWS session. Your AWS identity needs permission to create an S3 bucket and IAM role for the sandbox and to use AWS Transform workspaces, jobs and connectors. Guided setup also connects to the AWS Transform application, which is a separate browser sign-in.

### 3. Install Reframe

```bash
git clone https://github.com/sknampally/reframe.git
cd reframe
uv tool install --force --managed-python --python 3.12 --editable .
reframe --help
```

Keep this checkout in place and unchanged while a run is active: Reframe loads its prompts and contracts from it.

### 4. Try the demo (optional)

```bash
reframe demo
```

The demo walks through every stage with simulated data. It calls no AWS or AI service.

### 5. Run the guided flow

```bash
reframe
```

Choose **1 · Guided start / continue**. You can also type `/flow` at any time to continue a saved run. The guide asks for:

- **Source:** a GitHub URL or a clean local Git checkout. Reframe pins the current commit.
- **Workspace directory:** where outputs go. Reframe creates a `<repo>_assessment` folder inside it. Keep it private and outside this repository.
- **Scope:** which business journey to assess, or the whole repository.
- **AWS profile and region:** if your SSO session has expired, the guide offers to sign you in.
- **Executor:** `claude` (default), `codex` or `kiro`.
- **Wireframe provider:** `claude` or `codex`.

Reframe then creates the sandbox with OpenTofu: one S3 bucket and one role per source. It checks that the role cannot read any other bucket in the account, then creates the AWS Transform workspace and connector. Nothing is uploaded until you confirm.

### 6. Assess and approve

Confirm the source upload when asked. Reframe starts the AWS Transform job and waits for it to finish, which can take a while. If you leave, run `reframe` again and choose **1** to pick up the same job.

When the findings are downloaded, Reframe lists the files to review, including `assessment-review.html`. Approve them with your name, a short note, and confirmation that the findings match the pinned source.

### 7. Follow the review gates

After assessment approval, menu **1** takes you through these gates in order. Each one waits for a person. Typing `pause` at a gate stops without recording anything; choose **1** again to continue.

1. **Business requirements.** Choose `generate`, `import`, or `none`. `generate` appears only when Reframe has verified that this account can run an AWS Transform requirements job. Otherwise the guide explains why and offers `import` (files exported from AWS, labeled *imported*) or `none`. Reframe never presents imported or missing requirements as generated.
2. **Baseline context.** Give a Markdown file with clarifications, corrections, or constraints, or answer `none`. `none` is recorded as a valid answer. Admitted context is input from a named person, not source truth or approval.
3. **Skip or review.**

   | Choice | What runs | What you get |
   | --- | --- | --- |
   | **skip** (default) | Wireframe agent only, using the AWS findings as they are. You record your name and why you trust them. | Draft HTML wireframes and a package labeled unverified |
   | **review** | Executor and reviewer agents check the evidence program by program, then you answer SME questions and approve the specification | A reviewed specification, then wireframes and a package |

4. **Specification review** (review route only). Open `preparation/review.html`. Add Markdown context or `none`, answer or defer the SME questions, then approve validation. A deferral is not an answer, and the affected work stays blocked.
5. **Design plan.** Choose Functional Parity or Reimagine, a design version, the target stack, and any architecture constraints. Reframe records this before it generates detailed screens and APIs. Changing the plan later creates a new design version; the earlier one is kept.
6. **Design review.** Open the wireframes (`index.html`, `api.html`, `openapi.json`). Add Markdown context or `none`. Then `approve`, `design-change` (regenerate the design and keep the specification), or `behavior-change` (return to the specification).
7. **Package review.** Reframe builds the package and shows its file list, its exact SHA-256, the approvals it rests on, and the implementation blockers. Building it did not accept it. Add Markdown context or `none`, then `accept` that exact hash or ask for changes. On the skip route a second person must also accept the skipped validation.

Accepting the package records your name, rationale, and the archive hash in `acceptance/ledger.jsonl`, outside the archive. Implementation readiness is reported separately and stays blocked while decisions are deferred or conflicts are open.

**Validation calls.** The review route makes two calls for each program, two synthesis calls, and extra calls when a program needs correction. A new project has no call cap. A saved run keeps its recorded cap and the calls already used. If that cap is short, the guide states the count and asks before raising or removing it. A billed API key also stops at the saved dollar cap. Preparation, wireframe, and skip-draft calls are counted separately.

After the package exists you can optionally export a **Functional Parity** or **Reimagine** design as a separate draft package with `reframe design-export` and `reframe package-export`.

### 8. Check progress and find outputs

```bash
reframe status
```

`status` shows the current stage, the approvals recorded and the next command to run. `reframe resume` continues interrupted work. After a controller fix is reviewed and merged, use a clean committed checkout of that revision, reinstall, then record the new revision on the saved run:

```bash
git checkout main
git pull origin main
uv tool install --force --reinstall --managed-python --python 3.12 --editable .
reframe --workspace /path/to/private-poc upgrade-framework --note WHY
reframe --workspace /path/to/private-poc status
reframe --workspace /path/to/private-poc resume
```

`upgrade-framework` records this checkout. A prompt migration recorded for an earlier revision does not authorize this one. Run the upgrade command without `--adopt-prompts`. If its response is `Preparation prompts changed. The upgrade was not recorded.`, repeat that same command with `--adopt-prompts` and the same note. Do not add `--adopt-prompts` for any other response. This release does not change the preparation prompts.

```bash
reframe --workspace /path/to/private-poc upgrade-framework --note WHY --adopt-prompts
reframe --workspace /path/to/private-poc status
reframe --workspace /path/to/private-poc resume
```

That records the old and new prompt hashes for the calls and passed units already saved, then lets the saved review continue. It does not restart the assessment or the passed units.

A run waiting at `AWAITING_VALIDATION_APPROVAL` with a reviewed specification and no validation approval can record this controller revision. `approve validation` checks the framework revision, so record the update before approval:

```bash
reframe --workspace /path/to/private-poc upgrade-framework --note WHY
reframe --workspace /path/to/private-poc status
reframe --workspace /path/to/private-poc decide --open --by NAME --answer WHY --disposition deferred --confirm
reframe --workspace /path/to/private-poc approve validation --by NAME --note WHY
reframe --workspace /path/to/private-poc review-site
```

The upgrade keeps the specification, its review hash, the checkpoints, the assessment approval, the saved decisions, and the call count. It records the revision only when the preparation prompts are unchanged. A checkout that changes those prompts is refused, including with `--adopt-prompts`, because the reviewed specification stays bound to the saved prompt hash. Use the matching checkout or start a new workspace. `decide --open` records only questions that have no decision. Do not `resume`, and do not amend saved rationales unless you pass `--amend --confirm`. `review-site` is the wireframe provider call and runs only after validation approval.

`YOUR_REASON`, `YOUR_APPROVAL_RATIONALE`, `YOUR_NAME`, and `YOUR_NOTE` are rejected. A saved run that already used those tokens replaces them explicitly:

```bash
reframe --workspace /path/to/private-poc decide --placeholders --amend --confirm --by NAME --answer RATIONALE --disposition deferred
reframe --workspace /path/to/private-poc upgrade-framework --note WHY
reframe --workspace /path/to/private-poc approve validation --by NAME --note RATIONALE
reframe --workspace /path/to/private-poc review-site
```

The saved wireframe counter is not lowered just because `screens.json` is absent. An empty `previews/business-1` does not prove the provider was skipped. `recover-ui-call --confirm --note WHY` releases only a reservation the controller recorded before dispatch, with no provider receipt and no spending change. A failed reply, invalid reply, or dispatched call without a receipt stays counted and needs reconciliation. Receipts, the spending ledger, and earlier audit events stay in place. `review-site` keeps that unexplained count and numbers the next provider call after it.

The amendment keeps every previous answer, the batch history, and the superseded validation approval, then returns the run to `AWAITING_VALIDATION_APPROVAL`. `upgrade-framework` can record this controller revision in that state when the preparation prompts are unchanged. It still refuses a prompt change. `review-site` checks the context budget before it reserves a call or creates an output directory. A request that does not fit is split into explicit stages. References across those stages are kept, conflicting ids are rejected, and the merged screen and API model is checked against the complete specification. A restart uses a saved provider receipt instead of calling again. Do not `resume` into preparation, and do not start an assessment.

A saved correction that does not match the edit contract is rejected before any edit is applied. The same `reframe resume`, and menu 1, continue through that rejection and through one synthesis rework when a retry and the call budget remain. Progress is shown during that invocation. The run stops for a human approval, an exhausted allowance, an evidence failure, or a provider failure. It stops after three invalid candidates and prints the latest error. Another attempt is only:

```bash
reframe --workspace /path/to/private-poc feedback --authorize-correction --by NAME --note WHY
reframe --workspace /path/to/private-poc resume
```

Plain `resume` does not reset that count. Passed units stay sealed, and no assessment job is created. This controller change does not change the preparation prompts. Add `--adopt-prompts` only when `upgrade-framework` responds `Preparation prompts changed. The upgrade was not recorded.`

`reframe status` separates the project phase, the saved assessment service state, whether assessment approval is recorded, the last local action, and the required human action. A historical `AWAITING_ASSESSMENT_APPROVAL` service record is not the current blocker after assessment approval, while validation is still pending. Question counts are total, answered, deferred, and remaining. Deferral is not an answer, and the affected implementation stays blocked. Menu 1 records every still-open question in one confirmed batch and leaves saved decisions unchanged. A reviewed change to a saved decision uses `reframe decide --amend --confirm` and keeps the previous answer.

Tracked API spend is the local ledger for billed API calls. An API dollar cap of 0 is a real budget and blocks the next billed API call. Subscription and other provider usage are unmeasured, and that absence is not a zero-dollar charge.

Inside the workspace folder:

| Folder | Contents |
| --- | --- |
| `runs/<run>/` | Sealed AWS findings and `assessment-review.html` |
| `preparation/` | Executor and reviewer output and `review.html` |
| `previews/` | Wireframe sites, for both the skip and review routes |
| `packages/` | Draft ZIPs and the built packages (`package-<version>.zip`, `skip-<version>.zip`) |
| `acceptance/ledger.jsonl` | Hash-chained package acceptances, outside every archive |
| `requirements/` | Requirements capability, jobs, and imported sets with their original files |
| `human-review-context/` | Markdown context, gate records, dispositions, and conflicts |
| `versions/` | Immutable version manifests that approvals are bound to |
| `last-stop.json` | The most recent stop: cause, recovery class, and next safe command |
| `reports/index.html` | Links to every report for this run |

### Running without the menu

Every step is also a command, for scripts or for picking up one step by hand. `NAME`, `WHY`, and `RATIONALE` stand for your own values; the CLI refuses them if they are copied unchanged. Approvals need `--by` and `--note`, and nothing is approved by default.

```bash
W=/path/to/private-poc
reframe --workspace "$W" assess --allow-new-assessment --wait
reframe --workspace "$W" approve assessment --by NAME --note WHY --confirm-source-match

# Requirements and baseline context (both may be none)
reframe --workspace "$W" requirements status
reframe --workspace "$W" requirements import --requirements requirements.md --traceability traceability.yaml --function FUNCTION_ID --by NAME --note WHY
reframe --workspace "$W" requirements none --by NAME
reframe --workspace "$W" context import --file notes.md --by NAME --role architect --category clarification --gate baseline
reframe --workspace "$W" context none --gate baseline --by NAME

# Skip route
reframe --workspace "$W" design-plan --mode functional-parity --language java --by NAME
reframe --workspace "$W" preview --skip-validation --by NAME --note WHY --provider claude --name draft-1
reframe --workspace "$W" approve design --by NAME --note WHY

# Review route
reframe --workspace "$W" validate
reframe --workspace "$W" questions --state open --groups
reframe --workspace "$W" decide --question QUESTION_ID --by NAME --answer RATIONALE --disposition resolved
reframe --workspace "$W" approve validation --by NAME --note WHY
reframe --workspace "$W" design-plan --mode reimagine --language java --constraint "Keep the nightly batch window" --by NAME
reframe --workspace "$W" review-site --provider claude
reframe --workspace "$W" feedback --scope design --by NAME --note WHY
reframe --workspace "$W" approve specifications --by NAME --note WHY

# Both routes: build, review, and accept the exact package
reframe --workspace "$W" package
reframe --workspace "$W" package-review
reframe --workspace "$W" approve verification-skip --by NAME --note WHY   # skip route, a second person
reframe --workspace "$W" accept-package --sha256 PACKAGE_SHA256 --by NAME --note WHY
```

When a run stops, `reframe --workspace "$W" status` names the cause, the recovery class, and the next safe command. `reframe --workspace "$W" recovery-plan` is a read-only check of saved hashes, receipts, and the approvals that need renewal. An uncertain provider call is settled with `reconcile-operation`, and conflicting shared screen or API definitions with `reconcile-design`; neither erases a counted call.

The [CLI guide](docs/cli-guide.md) covers every command and flag, including design exports, comparing two assessments and recovering from a blocked run.

## What the package contains

The package is one ZIP. The skip route also keeps its earlier draft ZIP unchanged. Each file below is written by the function named, on the routes marked. A mode export is the optional `package-export` draft.

| File | Contents | Written by | Review | Skip | Mode export |
| --- | --- | --- | --- | --- | --- |
| `ai-dlc.json` | Phase, verification, boundaries, workflow status, readiness and blockers | `package()`, `reframe_preview.run()`, `package_skip()`, `reframe_optional.package_export()` | ✓ | ✓ | ✓ |
| `package-manifest.json` | FR-10 items carried, and any item stated absent | `reframe_acceptance.fr10_manifest()` | ✓ | ✓ | |
| `checksums.json` | SHA-256 of every file | `package()`, `package_skip()`, `reframe_preview.run()`, `reframe_optional.package_export()` | ✓ | ✓ | ✓ |
| `provenance.json` | Source pin, framework revision, providers, assessment hash | `package()`, `reframe_preview.run()` | ✓ | ✓ | |
| `specification.json` | Business specification (reviewed on the review route only) | `package()`, `reframe_preview.run()`, `reframe_optional.package_export()` | ✓ | ✓ | ✓ |
| `decisions.json`, `approvals.json` | SME decisions and current approvals | `package()` | ✓ | | |
| `decisions-needed.json`, `assumptions.json`, `rules.json`, `rules.html` | Open questions, the recorded skip decision, imported rule catalog | `reframe_preview.run()` | | ✓ | |
| `traceability.json`, `assessment-evidence.json` | Rules, tests, coverage, assessment-only evidence | `package()` | ✓ | | |
| `acceptance-catalog.json` | Acceptance criteria per imported rule, all `NOT RUN` | `reframe_preview.run()` | | ✓ | |
| `requirements-evidence.json`, `requirements-<function>-*` | Active requirements set and its provenance statement; imported originals unchanged | `package_extras()` | ✓ | ✓ | |
| `human-context.json` | Context submissions, dispositions, gate records, conflicts | `package_extras()` | ✓ | ✓ | |
| `approval-history.json` | Current and superseded approvals | `package_extras()` | ✓ | ✓ | |
| `design-plan.json`, `design-inventory.json` | Mode, target constraints, and the screen/API inventory saved before detail | `package_extras()` | ✓ | plan only | |
| `api-completeness.json`, `superseded-definitions.json` | API contract gaps; definitions replaced by a recorded reconciliation | `review_site()` via `package_extras()` | ✓ | | |
| `review.html`, `index.html`, `api.html`, `usage.html` | Wireframes, API reference, usage | `review_site()`, `reframe_preview.run()`, `reframe_optional.package_export()` | ✓ | `index.html` | `api.html`, `usage.html` |
| `screens.json`, `api-contracts.json`, `openapi.json` | Screen model, API contracts, OpenAPI 3 | `review_site()`, `reframe_preview.run()` | contracts, OpenAPI | screens, contracts | screens, OpenAPI |
| `current-state.html`, `design.json`, `inventories.json`, `manifest.json`, `context-conflicts.json` | Mode export design and its inputs | `reframe_optional.package_export()` | | | ✓ |
| `deltas.json`, `future-state.html`, `future-screens.json` | Reimagine proposals, unapproved until a person approves each | `reframe_optional.design_export()` | Reimagine | | Reimagine |
| `sme-architect-review.html` | The preparation report the approval was bound to | `package()` | ✓ | | |
| `implementation-backlog.json`, `monorepo-layout.txt`, `*-prompt.md` | Dependency-ordered backlog and section tasks | `package()`, `reframe_preview.run()` | ✓ | ✓ | backlog |
| `modernization-sequence.json`, `capability-map.json`, `parallel-validation.json`, `field-inventory.json`, `batch-inventory.json`, `api-boundary.json`, `governance.json`, `extraction-reading.json`, `rule-coverage.json`, `legacy-requirements.json` | Handoff records: every step `NOT_STARTED`, every capability unassigned, every comparison `NOT RUN` | `reframe_handoff.write_into()` | ✓ | ✓ | ✓ |
| `AGENTS.md`, `SKILL.md`, `skill-*.md` | Agent instructions, written into the export | `package()`, `reframe_preview.run()`, `reframe_handoff.write_into()` | ✓ | ✓ | ✓ |
| `README.md`, `reframe-notice.md` | How to read the package; notice for copied Reframe material | all package writers | ✓ | ✓ | ✓ |

The skill files exist only inside each exported package. The repository does not install a skills directory. The acceptance ledger is never inside an archive, so no hash refers to itself.

## Deliverables and quality gates

Reframe separates preparation outputs from completed modernization:

| Output | Purpose | Evidence boundary |
| --- | --- | --- |
| Source and assessment records | Inventory, dependencies, data and extracted rules | Source-pinned; verify Transform coverage |
| Business review and wireframes | Screens, navigation, rules and proposed journeys | Generated material, not automatically approved |
| Human decision records | Clarifications, conflicts, approvals and deferrals | Preserve provenance and unresolved decisions |
| AI-DLC handoff packages | Requirements, designs, guidance and test planning inputs | Opt-in mode packages are **DRAFT**, not complete build contracts |
| Target application | Implemented and operated by a downstream team | **Not generated or validated by this POC** |

Financial rules, authorization, EBCDIC data conversion, batch restart, concurrency and data equivalence require explicit validation. The [quality gates](quality-gates/README.md), [contracts](contracts/README.md), and [limitations](docs/limitations.md) describe the controls.

## Documentation

| Start with | Read |
| --- | --- |
| Install on your workstation | [Platform installation](docs/platform-install.md) · [Engineer setup](docs/engineer-setup.md) |
| Operate Reframe | [CLI guide](docs/cli-guide.md) · [Terminal console](docs/terminal-console.md) |
| Understand the process | [Four-phase workflow](docs/four-phase-workflow.md) · [Multi-agent workflow](architecture/multi-agent-workflow.md) |
| Examine security boundaries | [Sandbox infrastructure](infrastructure/README.md) · [Security policy](SECURITY.md) |
| Review methodology | [Modernization methodology](methodology/modernization.md) · [Quality gates](quality-gates/README.md) |
| Reproduce a safe example | [CardDemo example](examples/carddemo/README.md) · [Assessment comparison](docs/assessment-comparison.md) |
| Contribute | [Contributing](CONTRIBUTING.md) · [Third-party guidance](THIRD_PARTY.md) |

## Development and CI

Run the offline test suite from the repository with its dependencies installed:

```bash
PYTHONPATH=tests python -m unittest discover -s tests
reframe --help
```

The [CI workflow](.github/workflows/ci.yml) is configured for pull requests and pushes to `develop` (integration) and `main` (release). Feature branches open pull requests into `develop`. It runs three jobs in parallel: offline tests, a package build check, and a pinned gitleaks secret scan. **The badge reflects GitHub's actual workflow result; it is not a claim of live AWS acceptance.** No AWS credentials or paid model calls are required by CI.

## Author and attribution

Satish Kumar Nampally created Reframe. The project repository is [https://github.com/sknampally/reframe](https://github.com/sknampally/reframe).

The [MIT license](LICENSE) permits commercial use, modification, and redistribution, subject to its terms. A copy or a substantial portion of Reframe must keep the copyright notice and the permission notice.

Public acknowledgment and a link to the repository are appreciated. The MIT license does not require them.

## Security, licensing and scope

Keep source assessments, account identifiers, credentials and client documents in private workspaces—**never in this public repository or public issues**. Do not upload third-party source without authorization. Reframe itself is [MIT licensed](LICENSE); [AWS CardDemo](https://github.com/aws-samples/aws-mainframe-modernization-carddemo) remains an independent sample under its own license. See [SECURITY.md](SECURITY.md) and [THIRD_PARTY.md](THIRD_PARTY.md).

This framework has been developed with AI assistance. Humans are responsible for interpreting evidence, approving decisions and validating any resulting application.
