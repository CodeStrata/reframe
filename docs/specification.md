# Reframe specification: pipeline 1, the AWS Transform assessment

Status: draft for the owner's agreement. Stories are built from it; the owner tests the finished pipeline from the CLI and merges it in one PR.

## 1. Goal

From mainframe source code and an AWS sign-in, the Reframe CLI:

1. takes the source as a local folder, a local ZIP file or a GitHub repository, and copies it to S3;
2. creates every AWS resource the assessment needs with Terraform, using a new Neptune graph or one already in the account, as the person chooses;
3. creates the AWS Transform workspace, connector and job, and starts the job;
4. answers every question AWS asks, so the job runs to the end with no visit to the AWS console or web app;
5. downloads the assessment and the generated requirements, and builds an HTML report to review them;
6. when the person asks, lists every AWS resource the run created, records their consent, and removes them.

The only things a person provides are the AWS sign-in (`aws sso login`), renewed when Reframe asks for it, and the teardown consent.

This flow was proven by hand on CardDemo on 21 November 2026 (spike 1). Section 10 lists what that run taught us. Nothing in Reframe depends on CardDemo: any mainframe codebase AWS Transform accepts is an input.

## 2. Scope

In scope:

- one source per run: a local folder, a local ZIP file, or a GitHub repository at a branch, tag or commit;
- the AWS Transform mainframe plan "assess and reimagine", run over the full source: every business domain AWS finds, and the programs it leaves unassigned;
- a new Neptune graph per run, or an existing cluster in the account;
- two modes, autonomous and interactive (section 5);
- local runs on the owner's Mac, in `us-east-1` by default.

Out of scope for pipeline 1: anything that uses the downloaded requirements (checking them, building a design or a package). Those are later pipelines.

## 3. Commands

| Command | What it does |
|---|---|
| `reframe run --source <folder \| file.zip \| github-url> --profile <aws-profile> [--ref <branch-tag-or-commit>] [--mode autonomous\|interactive] [--graph new\|existing\|<cluster-name>]` | Runs stages 0 to 8 in a background worker and returns. |
| `reframe status` | The current stage, the job's plan steps, any question waiting, and the next step. |
| `reframe events [--follow]` | The run's event log. |
| `reframe answer [<choice>...] [--text <answer>]` | Shows AWS's waiting question with its options, or sends the answer. |
| `reframe resume` | Continues a run that stopped (for example after the AWS sign-in expired). Never repeats a change that has a receipt. |
| `reframe report [--open]` | Builds the HTML report again from the run's downloads, and opens it in the browser. |
| `reframe teardown` | Lists every AWS resource the run created, asks for consent, records it, then removes them (section 4, stage 9). |

Region defaults to `us-east-1` (`--region` to change it). `--run <id>` picks a run other than the latest.

## 4. Stages

Each stage writes what it did to the run folder. Every AWS change records an intent before the call and a receipt after it, so a stopped run resumes without creating anything twice. An intent without a receipt is UNCERTAIN: Reframe settles it by reading AWS's state before going on.

### Stage 0: preflight

Checks, before any change, and reports every problem together with its fix:

- the AWS sign-in works for the profile (`sts get-caller-identity`); if it has expired, Reframe stops and prints `aws sso login --profile <profile>`;
- AWS Transform is set up for the account in the region;
- Git, the AWS CLI, uv, Terraform 1.10 or later, and the pinned AWS Transform MCP server are installed;
- the source exists: the folder or ZIP file can be read, or the GitHub repository and ref can be reached.

### Stage 1: source snapshot

| Source | Snapshot |
|---|---|
| A local folder that is a Git checkout | `git archive` of the commit (`--ref`, default `HEAD`): only committed files |
| A local folder that is not a Git checkout | A ZIP of every file under it, in name order with fixed timestamps, so the same files give the same bytes; `.git`, `.DS_Store` and similar are left out |
| A local ZIP file | The file itself, after checking it opens, has no unsafe paths (absolute, `..`, links) and is not larger than 2 GB unpacked |
| A GitHub URL | Cloned into the run folder at `--ref` (default branch when not given), then `git archive` of that commit |

Reframe records the source, the commit when there is one, the number of files, and the archive's SHA-256.

### Stage 2: AWS resources (Terraform)

**The Neptune graph.** Reframe lists the Neptune clusters in the account and region (name, engine version, status) and the person chooses one or a new graph:

- interactive mode asks, with the list;
- autonomous mode creates a new graph unless `--graph <cluster-name>` names one; `--graph existing` asks even in autonomous mode.

An existing cluster must be available and run engine 1.4.5.1 or later, which AWS requires for the reimagine connector. Before using it, Reframe shows exactly what it will add and asks for consent: a loader role associated with the cluster, and a security group in the cluster's VPC with one ingress rule to the cluster's security group on port 8182. Reframe never deletes or otherwise changes an existing cluster; teardown removes only those additions.

**Terraform roots.** Both are named `reframe-<project>-<run>-…` and tagged `ManagedBy=reframe`, `ReframeProject` and `ReframeRun`:

| Root | Creates |
|---|---|
| bootstrap | the encrypted, versioned S3 bucket that holds the project root's state |
| project | the encrypted source bucket and the sandbox IAM role that can read only that bucket; with a new graph, the Neptune Serverless cluster, its VPC, subnets, security groups, S3 endpoint and loader role; with an existing cluster, the additions above; the reimagine connector's IAM role |

Reframe saves each plan, checks that it only creates resources, then applies it.

### Stage 3: upload

Reframe uploads the snapshot to the source bucket once, with S3's SHA-256 checksum, and checks the stored object against the snapshot.

### Stage 4: AWS Transform setup

Reframe creates the workspace and the reimagine connector (type `mainframe_modernization|reimagine|1`, configured from Terraform's outputs), accepts the connector with the reimagine role and waits until it is ACTIVE. It records each ID from AWS's reply. No separate S3 connector is needed: the job reads the source from the location Reframe gives in AWS's source-location form, and writes its outputs through the reimagine connector to the source bucket.

### Stage 5: job

Reframe creates the mainframe job in the workspace and starts it.

### Stage 6: driving the job

Reframe polls the job every minute, with its open tasks and chat. It answers each question as follows.

| AWS asks | Autonomous mode | Interactive mode |
|---|---|---|
| Which plan to run | "Assess and reimagine", with the setup answers (English only, no collaborators) in the same reply | `reframe answer` |
| Where the source is (the source-location form) | The S3 location of the uploaded snapshot | The same, from the run's own record |
| Which business functions to reimagine (the catalog's chat message) | One structured chat reply naming every business domain in the catalog and the unassigned programs | The catalog's options through `reframe answer` |
| "Do you want to proceed?" after the selection | "Yes, proceed." | `reframe answer` |
| Any other blocking question with options | AWS's default option when AWS marks one, recorded as Reframe's decision | `reframe answer` |
| A blocking question with no default | Waits for `reframe answer` | `reframe answer` |
| Non-blocking forms (for example "Add collaborators") | Left open | Left open |

Selection is answered the way the web app does it: `SendMessage` with the reply text and `interactionResults` naming the catalog message. The review form "Review business functions discovery results" is not submitted; its own hint sends the selection to chat.

The job is done when every step in its plan has SUCCEEDED and the plan includes "Generate requirements". (Before the selection, the plan holds only the assessment steps, so "every step succeeded" alone is not enough.) AWS keeps the job's own status at EXECUTING while a non-blocking form is open, so Reframe does not wait for COMPLETED. A step that fails stops the run with AWS's reason.

### Stage 7: retrieval

AWS writes its outputs to the source bucket under `transform-output/<job>/`, not as job artifacts. Reframe downloads:

| Output | Path in S3 | Contents |
|---|---|---|
| Requirements | `spec_gen/*.zip` | One requirements document per business function and one for the unassigned programs, each with traceability and discovery files; a data model; a coverage report |
| Assessment | `results/` | Classification, codebase issues, generic analyses, scheduler data, `analyze_code_results.zip`, `slicing_outputs.zip` |
| Business function catalog | `business-functions/delivery.zip` | AWS's browsable catalog |

It skips the graph-database files and AWS's internal state. It checks every archive for unsafe paths, unpacks the requirements, and writes a manifest (file, size, SHA-256) and a summary: functions, requirement counts by type, and coverage.

### Stage 8: report

Reframe builds one self-contained HTML report in the run folder (`outputs/report/index.html`, no network needed to view it):

- **Overview:** the source and commit, the run's dates, counts of domains, functions, programs and requirements by type, and AWS's coverage figures;
- **Business domains and functions:** each function's requirements, with its programs, batch jobs, screens and data stores, and the source programs each requirement traces to;
- **Requirements and business rules:** every requirement in one searchable, filterable table (by domain, function and type); the business rules AWS extracted, from each function's traceability file (rule, program, disposition such as captured or not applicable, and the requirements it backs), with AWS's rule counts; and AWS's open questions from each requirements document;
- **Data model:** AWS's data model;
- **Assessment:** classification of the source files, codebase issues, missing and unsupported files, and the scheduler data;
- **AWS's own pages:** links to AWS's coverage report and business function catalog, unpacked beside it;
- **Decisions:** every answer Reframe gave AWS on the person's behalf, and why.

`reframe report --open` rebuilds it and opens it.

### Stage 9: teardown (on request)

The run keeps its AWS resources until the person runs `reframe teardown`. Then Reframe:

1. builds the inventory from the run's own records only (receipts and Terraform state, never names or guesses), adding any detached network interface AWS Transform left in the run's own VPC, and lists every resource at once: the job, workspace and connector, each Terraform resource (S3 buckets, IAM roles, the Neptune cluster and instance, VPC, subnets, security groups, endpoint), and, with an existing cluster, Reframe's additions to it;
2. asks the person to type `yes` to delete exactly that list;
3. records the consent (who, when, the list and its hash) in the run folder before deleting anything; a list that changes before deletion needs consent again;
4. deletes, in order:
   1. stops the job, waits until it has stopped, and deletes it;
   2. deletes the workspace;
   3. checks account-wide that the run's connector is gone; if it is still listed, calls `DeleteConnector` once and records the result; if AWS refuses, reports the connector by name as left over (its IAM role is removed in step 5, so it can no longer reach anything);
   4. deletes the detached AWS Transform network interfaces in the run's VPC, which block the security group and subnet from being deleted;
   5. destroys the project Terraform root, then the bootstrap root, each from a saved plan checked to destroy only what the run created; a destroy that stops part way is planned again for what is left and continued;
5. checks, read-only, that nothing tagged with the run remains. AWS's tag index keeps entries for a while after deletion, so each entry it still lists is checked against its own service, and only one that still exists counts.

## 5. Modes

- **Autonomous** (default): Reframe makes every decision in section 4's table and records each one with its reason in the run's decisions file and the report. The person reads them afterwards.
- **Interactive**: Reframe waits at each question for `reframe answer`. All answers go from the Reframe CLI to AWS; the person never needs the AWS console or web app.

Teardown consent is always the person's, in both modes.

## 6. Code layout

Each area has its own folder, so it is clear where a change belongs:

| Folder | Holds |
|---|---|
| `src/reframe/core/` | The CLI and its commands, the run folder and records, errors, the shell helper, preflight, the background worker, status |
| `src/reframe/source/` | Reading a folder, a ZIP file or a GitHub repository, the snapshot, the S3 upload |
| `src/reframe/infrastructure/` | The Terraform runner, Neptune cluster discovery, network clean-up, and the Terraform roots and modules (`terraform/`) |
| `src/reframe/transform/` | The AWS Transform MCP client and API helper, the workspace and connector, the job driver and its answers, retrieval, and the Transform part of teardown |
| `src/reframe/report/` | The HTML report |
| `tests/` | Offline tests, in the same folders |

Later pipelines get their own folders (for example `src/reframe/claude/` for the Claude-based pipelines).

## 7. Run folder

`~/.reframe/projects/<project>/runs/<run>/`, owner-only permissions:

- `run.json`: inputs, mode, stage, status;
- `events.jsonl`: every event;
- `changes/`: intent and receipt for every AWS change;
- `decisions.json`: every answer Reframe gave and why;
- `outputs/`: the downloads, the manifest, the summary and the report;
- `terraform/`: the roots, saved plans and the bootstrap state;
- `teardown/`: the inventory, the consent and the deletion records.

Nothing from the run folder is committed to Git. GitHub issues, PRs and committed files never carry account IDs, ARNs, resource IDs, job IDs, profile names or bucket names.

## 8. Failures and resumption

- An expired sign-in stops the run with the login command; `reframe resume` continues it.
- An AWS refusal stops the run and keeps AWS's reason.
- A stage that fails can be rerun; changes with receipts are skipped.
- A run that stops at any point keeps what it created until `reframe teardown`.

## 9. Acceptance

Pipeline 1 is done when, run from the CLI only:

- three autonomous runs finish with no input except the AWS sign-in, one for each source form (a GitHub URL, a local folder, a local ZIP file), on any mainframe codebase;
- each downloads requirements covering every business domain and the unassigned programs, and the assessment files in section 4, stage 7, and builds the report;
- `reframe teardown` after each lists every resource, records consent and leaves a clean account: no resource tagged with the run, no workspace the run created, and no connector the run created, or, while the open question in section 10 stands, a connector reported by name whose IAM role is gone;
- one interactive run finishes with every answer sent through `reframe answer`;
- when the account has a suitable Neptune cluster, one run uses it, and teardown leaves the cluster as it was.

Reframe's builder runs one full round of these from the CLI before the PR; the owner then tests from the CLI and merges.

## 10. What spike 1 showed

- Function selection works from code, with a structured chat reply. No console is needed.
- The job's status stays EXECUTING while the optional "Add collaborators" form is open, even after every step has succeeded.
- AWS lists no job artifacts. The outputs are in the source bucket under `transform-output/<job>/`.
- Connectors outlive their workspace. After the earlier run, the connector was gone some time after its workspace was deleted. After spike 1 it was still listed, and `DeleteConnector` was refused as not authorized for the signing-in role (an earlier attempt returned HTTP 500). Open question: which permission `DeleteConnector` needs, and whether the owner's role can be given it.
- AWS Transform leaves a detached network interface in the graph's VPC after the job. Until it is deleted, the security group and subnet cannot be, and the Terraform AWS provider stopped responding twice while waiting on them.
- AWS's tag index still listed five deleted resources (a VPC endpoint and four security group rules) after teardown; each was NotFound in EC2.
- The S3 console's bucket list showed the deleted state bucket for a while after S3 itself returned 404 for it.
- AWS Transform workspaces are visible only to their members. The MCP server's identity owns everything Reframe creates, so the owner's own web-app user does not see it unless added as a collaborator.
- The AWS Transform CLI (`atx`) covers only "AWS Transform custom", not mainframe, so Reframe uses the MCP server's API client.
- From creating the workspace to the requirements being written took about 45 minutes.
