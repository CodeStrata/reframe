# Reframe

Reframe runs an AWS Transform assessment of a mainframe codebase from one command and brings the results back as a report you can read: business domains and functions, requirements, business rules, open questions and the data model.

You give it the source as a local folder, a local ZIP file or a GitHub URL. Reframe creates the AWS resources with Terraform, uploads a snapshot of the source, drives the AWS Transform job to the end, downloads what AWS produced and builds an HTML report. The AWS resources stay until you remove them with `reframe teardown`, which lists every resource first and asks for your consent.

This is pipeline 1. The full design is in [docs/specification.md](docs/specification.md), the stories are in [docs/plan.md](docs/plan.md), and the live test results are in [docs/acceptance.md](docs/acceptance.md).

## The pipeline

![How a pipeline 1 run works: ten stages from preflight to the report, with teardown only on request; you sign in, answer AWS's questions in interactive mode, read the report and consent to teardown; next, pipeline 2 adds Claude's graph to the same Neptune cluster](docs/images/pipeline-1.svg)

| Stage | What happens |
|---|---|
| 0. Preflight | Checks Git, the AWS CLI, uv, Terraform 1.10 or later, your AWS sign-in, the source and that AWS Transform is ready in the region. Nothing is created if a check fails. |
| 1. Snapshot | The source becomes one deterministic ZIP: a folder as it is, a Git checkout or URL at the commit you choose with `--ref`, or your ZIP after a safety check. |
| 2. AWS resources | Terraform creates a state bucket, then the source bucket, the IAM roles and a new Neptune Serverless graph in its own private network. You can use an existing Neptune cluster instead (see below). |
| 3. Upload | The snapshot goes to the source bucket with a SHA-256 checksum. |
| 4. AWS Transform setup | Reframe creates the workspace and the reimagine connector to the Neptune graph, and waits for the connector to be active. |
| 5-6. Job | Reframe creates the job ("Assess and reimagine") and polls it every minute. AWS asks questions and shows forms along the way: the plan, the source location, the business function catalog and its confirmations. In autonomous mode Reframe answers each one and records why in `decisions.json`; in interactive mode it asks you. |
| 7. Retrieval | When every step has succeeded, including "Generate requirements", Reframe downloads the requirements, the assessment and the business function catalog from S3. |
| 8. Report | One self-contained HTML page for business users and subject-matter experts to review: from the overview down by business domain, business function and capability to each requirement and the business rules behind it, with review marks a reviewer can download. Technical detail has its own section. |
| 9. Teardown | Only when you run `reframe teardown`. See [Removing the AWS resources](#removing-the-aws-resources). |

Every change Reframe makes in AWS is written down before it is sent and confirmed after, so a run that stops can be resumed with `reframe resume` without creating anything twice. A run takes about an hour, most of it AWS Transform's own work.

## What you need

- macOS or Linux, with Python 3.10 or later.
- [uv](https://docs.astral.sh/uv/) to install Reframe. The guided run checks the rest and offers to install what is missing: Git, the [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), [Terraform](https://developer.hashicorp.com/terraform/install) 1.10 or later and the AWS Transform MCP server.
- An AWS account where AWS Transform is available (Reframe uses `us-east-1` by default), and an AWS CLI profile that signs in with IAM Identity Center (`aws sso login`).
- That profile needs permission to create and delete S3 buckets, IAM roles, a VPC with subnets and security groups, a Neptune Serverless cluster, and an AWS Transform workspace, connector and job.

## Install

You need macOS or Linux (on Windows, use WSL2), Python 3.10 or later, and [uv](https://docs.astral.sh/uv/). Install Reframe from a clone of this repository on the `v2` branch:

```bash
uv tool install --reinstall --editable ~/path/to/reframe
```

Or, without a clone, straight from GitHub:

```bash
uv tool install --reinstall "git+https://github.com/sknampally/reframe@v2"
```

Check it with `reframe --version`. With the editable install, `git pull` in the clone updates Reframe; reinstall only when `pyproject.toml` changes.

Everything else a run needs is checked, and installed on request, by the guided run below.

## The home screen

```bash
reframe
```

`reframe` on its own shows your runs (status, stage, when each started, and whether its AWS resources are still in place), the suggested next step, and a numbered menu: start a guided run, run status, answer a waiting question, resume, open the business review, event log, tear down, setup and help. An action on a run asks which run, with the latest as the default. After each action the home screen comes back; 0 or Ctrl+D leaves it, and Ctrl+C cancels an action. `reframe --help`, and `--help` after any command, shows the commands or options as a table with examples.

## Run an assessment: the guided way

```bash
reframe run
```

Reframe guides you through five steps and checks each answer before going on:

1. **Prerequisites.** A table of what a run needs and what this computer has: Git, the AWS CLI v2, uv, Terraform 1.10 or later and the AWS Transform MCP server (Claude Code is listed as optional, for pipeline 2). For anything missing it shows the install command for your operating system and offers to run it; nothing is installed without your yes. Reframe installs Terraform itself: the pinned HashiCorp release, checked against HashiCorp's SHA-256 sums, kept in `~/.reframe/tools` and used from there, so your PATH, your shell files and any older Terraform stay as they are.
2. **AWS sign-in.** Choose one of your AWS CLI profiles and the region. If the profile is not signed in, Reframe offers to run `aws sso login` for you; you sign in in your browser, and Reframe never sees your credentials. With no profiles, it offers `aws configure sso`.
3. **Source.** A GitHub or Git URL (checked with Git, and optionally a branch, tag or commit), a local folder, or a local ZIP file.
4. **Choices.** Autonomous or interactive (see below), the project name (a short label such as `carddemo`: it names the run's folder, `~/.reframe/projects/<project>/runs/<run>/`, and starts the name of every AWS resource the run creates, `reframe-<project>-<run>`), and a new Neptune graph or an existing cluster.
5. **Summary.** What will be created, then one yes to start. The run continues in the background.

Your profile, region and tool paths are saved in `~/.reframe/config.json` as the next run's defaults. To check the prerequisites and sign in without starting a run:

```bash
reframe setup
```

### Follow the run

```bash
reframe status
```

```bash
reframe events --follow
```

`reframe status` shows the stage, the AWS Transform job's plan steps, any question waiting for you and what to do next. Every command acts on your latest run; add `--run <run id>` for another one. The run ID is printed when the run starts.

Open the report when the run is done:

```bash
reframe report --open
```

### Run without questions

When the prerequisites are set up (for example after `reframe setup`, or on a build machine), give the source and Reframe asks nothing. The profile and region default to the ones you saved:

```bash
reframe run --source https://github.com/aws-samples/aws-mainframe-modernization-carddemo
```

```bash
reframe run --source ~/code/my-mainframe-app --profile my-profile --mode interactive
```

```bash
reframe run --source ~/Downloads/my-mainframe-app.zip --project my-app
```

Add `--ref <branch, tag or commit>` for a Git source, `--region` for another region, `--graph new|existing|<cluster name>` for the Neptune choice, and `--terraform /path/to/terraform` (or `REFRAME_TERRAFORM`) for a Terraform of your own.

### Autonomous or interactive

Autonomous is the default: Reframe answers AWS on your behalf and writes each answer and its reason to the run's `decisions.json`. It chooses "Assess and reimagine", gives the uploaded source's location, and selects every business domain plus the unassigned programs, so the whole source is assessed.

To make the choices yourself, add `--mode interactive`:

```bash
reframe run --source ~/code/my-mainframe-app --profile my-profile --mode interactive
```

When AWS asks something, `reframe status` says so. See the question and its numbered options:

```bash
reframe answer
```

Answer with the option numbers (several for the catalog, such as `reframe answer 2 3`), or in your own words:

```bash
reframe answer 1
```

```bash
reframe answer --text "Reimagine business domain \"Payments\""
```

The worker sends your answer within a minute. In autonomous mode, a question Reframe does not recognise also waits for `reframe answer`.

### Neptune: a new graph or an existing cluster

By default each run creates its own Neptune Serverless graph in a private network with no internet access. It bills until you run `reframe teardown`.

To use a Neptune cluster you already have, pass `--graph existing` to choose from a list, or `--graph <cluster name>`. With no `--graph`, interactive mode lists the clusters in the region and asks. Reframe uses an existing cluster as it is and never changes or deletes it. It offers one only if it meets every need: available with an instance, Serverless, engine 1.4.5.1 or later, IAM authentication, encryption, subnets in two availability zones with an S3 gateway endpoint, a security group pair, and a bulk-loader role that can read the run's source bucket. For each cluster it rejects, it says why.

## If a run stops

`reframe status` names what happened and the next step. The usual cases:

| Status | What to do |
|---|---|
| `WAITING_SIGNIN` | Your AWS sign-in expired. Run `aws sso login --profile my-profile`, then `reframe resume`. |
| `WAITING_HUMAN` | AWS is waiting for an answer: run `reframe answer`, then answer it. |
| `UNCERTAIN` | A change was sent but its result is unknown. `reframe resume` checks AWS's state before doing anything again. |
| `FAILED` or `REFUSED` | Read the message and `worker.log` in the run folder, fix what it says, then `reframe resume`. |

`reframe resume` continues from where the run stopped. Nothing with a receipt is done again.

## Results

Everything for a run is in `~/.reframe/projects/<project>/runs/<run id>/`:

| Path | What it holds |
|---|---|
| `outputs/report/index.html` | The business review report. Rebuild it with `reframe report`. |
| `outputs/requirements/` | AWS's requirements per business function, with `traceability.yaml` linking rules to requirements. |
| `outputs/aws/` | AWS's assessment results. |
| `outputs/catalog/` | The business function catalog (`delivery.zip`, unpacked). |
| `decisions.json` | Every answer Reframe gave on your behalf, and why. |
| `events.jsonl` | The run's event log. |
| `changes/` | The record of every change Reframe made in AWS: what it meant to do, and AWS's receipt. |
| `worker.log` | The background worker's output. |

## Reviewing the results with the business

`reframe report --open` opens the business review report. It is one HTML file with everything inside it, so you can send it to business users and functional subject-matter experts as it is; they need only a browser.

- **It starts at the top:** what was assessed and the business domains. From a domain they go to its business functions, from a function to its capabilities (AWS's user stories), and from a capability to each requirement in plain words, with the business rules behind it and AWS's open questions for the business. A breadcrumb leads back up, and the search box finds any requirement, rule or question.
- **They mark what they read:** Agree, Needs change or Question on each requirement, business rule and open question, with a comment. Progress shows on every domain, function and capability. Marks stay in their browser.
- **They send their review back:** under **Your review** they enter their name and download their marks as a CSV file (for a spreadsheet) or a JSON file. Each row names the domain, function, capability, item, mark and comment, and the file names the run and the source's SHA-256, so a review always matches the code that was assessed.
- **Technical detail** (all requirements and rules in tables, the data model, the assessment, AWS's own pages and Reframe's answers) is in its own section, for engineers.

## Removing the AWS resources

```bash
reframe teardown
```

Teardown runs in your terminal and asks before it deletes anything:

1. It lists every AWS resource the run created, taken only from the run's own records: the AWS Transform job, workspace and connector from their creation receipts, and everything in the run's Terraform state. Nothing is found by name.
2. You type `yes` to delete them all. Anything else keeps them. Your consent, with the list and its hash, is saved in `teardown/consents.json`.
3. It deletes in order: the job, the workspace, the connector, any network interface AWS Transform left in the run's own network, the project resources, then the state bucket. With a new Neptune graph this takes about 15 minutes.
4. It checks every resource tagged with the run and reports anything still in AWS.

Two things you may see at the end:

- The AWS Transform connector may be left over. Some roles are not allowed to call DeleteConnector, and AWS often removes the connector itself a little later. Its IAM role is deleted, so it can reach nothing.
- AWS's tag index can list deleted resources for a while. Reframe checks each one in its own service and reports only what still exists.

If the list changes between your `yes` and the deletion, Reframe stops and asks again. An existing Neptune cluster you chose is never in the list.

## Code layout

| Folder | What it does |
|---|---|
| `src/reframe/core/` | The CLI, the run folder and its change records, preflight, the stage pipeline and teardown |
| `src/reframe/source/` | Taking the source snapshot and uploading it to S3 |
| `src/reframe/infrastructure/` | The Terraform roots and modules, the Neptune cluster checks and the network clean-up |
| `src/reframe/transform/` | AWS Transform: the MCP client, the workspace and connector, the job driver, answering questions, retrieval |
| `src/reframe/report/` | The HTML report |
| `tests/` | Offline tests for each folder above; they run on every pull request |

Run the tests from a checkout:

```bash
python -m unittest discover -s tests -t .
```

## Next

Pipeline 2 will run the same assessment with Claude, using Anthropic's [code-modernization plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization), and add its graph to the same Neptune cluster, so the two assessments can be compared. It will be specified and planned once pipeline 1 has been tested.

Earlier work stays in the repository's history: the build before this rebuild ends at commit `000b816`, and the first release is tagged `v0.3.0`.

## License

MIT. See [LICENSE](LICENSE).
