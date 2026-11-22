# Reframe specification: pipeline 1, the AWS Transform assessment

Status: draft for the owner's agreement. No code is written until this is agreed.

## 1. Goal

From a mainframe source repository and an AWS sign-in, one command:

1. creates every AWS resource the assessment needs, with Terraform;
2. copies the source to S3;
3. creates the AWS Transform workspace, connectors and job, and starts it;
4. answers every question AWS asks, so the job runs to the end with no visit to the AWS console or web app;
5. downloads the assessment and the generated requirements;
6. removes everything it created.

The only thing a person provides is the AWS sign-in (`aws sso login`), renewed when Reframe asks for it.

This flow was proven by hand on CardDemo on 21 November 2026 (spike 1). Section 9 lists what that run taught us.

## 2. Scope

In scope:

- one repository per run, pinned to a commit;
- the AWS Transform mainframe plan "assess and reimagine", run over the full repository: every business domain AWS finds, and the programs it leaves unassigned;
- two modes, autonomous and interactive (section 5);
- local runs on the owner's Mac, in `us-east-1`.

Out of scope for pipeline 1: anything that uses the downloaded requirements (checking them, building a design or a package). Those are later pipelines.

## 3. Commands

| Command | What it does |
|---|---|
| `reframe run --repo <path-or-url> --profile <aws-profile> [--commit <sha>] [--mode autonomous\|interactive] [--keep]` | Runs stages 0 to 8. Starts a background worker and returns. |
| `reframe status` | The current stage, the job's plan steps, any question waiting, and the next step. |
| `reframe events [--follow]` | The run's event log. |
| `reframe answer [<choice>...]` | Interactive mode only: shows AWS's waiting question with its options and sends the answer. |
| `reframe resume` | Continues a run that stopped (for example after the AWS sign-in expired). Never repeats a change that has a receipt. |
| `reframe teardown` | Runs stage 8 on its own, for a run started with `--keep` or one that stopped before the end. |

Region defaults to `us-east-1` (`--region` to change it).

## 4. Stages

Each stage writes what it did to the run folder. Every AWS change records an intent before the call and a receipt after it, so a stopped run resumes without creating anything twice. An intent without a receipt is UNCERTAIN: Reframe settles it by reading AWS's state before going on.

### Stage 0: preflight

Checks, before any change:

- the AWS sign-in works for the profile (`sts get-caller-identity`); if it has expired, Reframe stops and prints `aws sso login --profile <profile>`;
- AWS Transform is set up for the account in the region;
- Terraform, Git and the AWS Transform MCP server (pinned version) are installed;
- the repository and commit exist.

### Stage 1: source snapshot

Reframe archives the repository at the pinned commit and records the commit and the archive's SHA-256.

### Stage 2: AWS resources (Terraform)

Two Terraform roots, both named and tagged from the project name, with `reframe:project` and `reframe:run` tags:

| Root | Creates |
|---|---|
| bootstrap | the encrypted, versioned S3 bucket that holds Terraform state |
| project | the encrypted source bucket; the sandbox IAM role that can read only that bucket; the Neptune graph, its VPC, subnets, security groups and S3 endpoint; the loader role; the reimagine connector's IAM role |

Reframe saves each plan, checks that it only adds resources, then applies it.

### Stage 3: upload

Reframe uploads the snapshot to the source bucket and checks the object's checksum.

### Stage 4: AWS Transform setup

Reframe creates the workspace and the reimagine connector (type `mainframe_modernization|reimagine|1`, configured from Terraform's outputs), accepts the connector with the reimagine role and waits until it is ACTIVE. It records each ID from AWS's reply. No separate S3 connector is needed: the job reads the source from the location Reframe gives in AWS's source-location form, and writes its outputs through the reimagine connector to the source bucket.

### Stage 5: job

Reframe creates the mainframe job in the workspace and starts it.

### Stage 6: driving the job

Reframe polls the job and its open tasks and chat. It answers each question as follows.

| AWS asks | Autonomous mode | Interactive mode |
|---|---|---|
| Which plan to run | "Assess and reimagine", with the setup answers (English only, no collaborators) in the same reply | The same question through `reframe answer` |
| Where the source is (the source-location form) | The S3 location of the uploaded snapshot | The same answer; the form is answered from the run's own record |
| Which business functions to reimagine (the catalog's chat message) | One structured chat reply naming every business domain in the catalog and the unassigned programs | The catalog's options through `reframe answer` |
| "Do you want to proceed?" after the selection | "Yes, proceed." | `reframe answer` |
| Any other blocking question with options | AWS's default option, recorded as Reframe's decision | `reframe answer` |
| A blocking question with no default or options | Stops and asks the owner | `reframe answer` |
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

It skips the graph-database files and AWS's internal state. It checks every archive for unsafe paths, unpacks the requirements, and writes a manifest (file, size, SHA-256) and a summary: functions, requirement counts by type, and the coverage figure.

### Stage 8: teardown

By default teardown runs automatically after retrieval; `--keep` skips it. Reframe deletes only resources whose creation it recorded, by the ID in its own receipt, never by name. In order:

1. stop the job, wait until it has stopped, delete it;
2. delete the workspace;
3. check account-wide that the run's connectors are gone; if one is still listed, call `DeleteConnector` once and record the result; if AWS refuses, report the connector by name as left over (its IAM role is removed in step 4, so it can no longer reach anything) and check again on the next run;
4. destroy the project Terraform root, then the bootstrap root, each from a saved plan that is checked to destroy only what the run created;
5. a final read-only check that nothing tagged with the run remains.

## 5. Modes

- **Autonomous** (default): Reframe makes every decision in section 4's table and records each one with its reason in the run's decisions file. The owner reads them afterwards.
- **Interactive**: Reframe stops at each question and waits for `reframe answer`. All answers go from the Reframe CLI to AWS; the owner never needs the AWS console or web app.

## 6. Run folder

`~/.reframe/projects/<project>/runs/<run>/`, owner-only permissions:

- `run.json`: inputs, mode, stage, status;
- `events.jsonl`: every event;
- `changes/`: intent and receipt for every AWS change;
- `decisions.json`: every answer Reframe gave and why;
- `outputs/`: the downloads, the manifest and the summary;
- `terraform/`: the roots, saved plans and state locations.

Nothing from the run folder is committed to Git. GitHub issues, PRs and committed files never carry account IDs, ARNs, resource IDs, job IDs, profile names or bucket names.

## 7. Failures and resumption

- An expired sign-in stops the run with the login command; `reframe resume` continues it.
- An AWS refusal stops the run and keeps AWS's reason.
- A stage that fails can be rerun; changes with receipts are skipped.
- If the run stops after stage 2, `reframe teardown` removes what it created.

## 8. Acceptance

Pipeline 1 is done when three runs in a row on CardDemo at a pinned commit, in autonomous mode:

- finish with no input except the AWS sign-in;
- each download requirements covering every business domain and the unassigned programs, and the assessment files in section 4, stage 7;
- each finish with a clean account: no resource tagged with the run, no workspace the run created, and no connector the run created, or, while the open question in section 9 stands, a connector reported by name whose IAM role is gone.

One interactive run must also finish with every answer sent through `reframe answer`.

## 9. What spike 1 showed

- Function selection works from code, with a structured chat reply. No console is needed.
- The job's status stays EXECUTING while the optional "Add collaborators" form is open, even after every step has succeeded.
- AWS lists no job artifacts. The outputs are in the source bucket under `transform-output/<job>/`.
- Connectors outlive their workspace. After the earlier run, the connector was gone some time after its workspace was deleted. After spike 1 it was still listed, and `DeleteConnector` was refused as not authorized for the signing-in role (an earlier attempt returned HTTP 500). Open question: which permission `DeleteConnector` needs, and whether the owner's role can be given it.
- AWS Transform workspaces are visible only to their members. The MCP server's identity owns everything Reframe creates, so the owner's own web-app user does not see it unless added as a collaborator.
- The AWS Transform CLI (`atx`) covers only "AWS Transform custom", not mainframe, so Reframe uses the MCP server's API client.
- From creating the workspace to the requirements being written took about 45 minutes.
