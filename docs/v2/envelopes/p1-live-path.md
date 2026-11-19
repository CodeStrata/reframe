# P1 live path: execution envelope (draft)

**Status: draft for the owner's decision. Nothing has run under it.** Story: [#230](https://github.com/sknampally/reframe/issues/230) (P1-01). Specification: section 15 (P1), section 11, section 8, section 4 (uncertain dispatch, AWS review tasks), FR-14.

This envelope says exactly what the P1 live path may do: the read-only discovery in P1-03 ([#232](https://github.com/sknampally/reframe/issues/232)), the resource checks in P1-04 ([#233](https://github.com/sknampally/reframe/issues/233)), and one function from selection to retrieved requirements in P1-05 ([#234](https://github.com/sknampally/reframe/issues/234)). Anything not listed here is outside it, and Reframe stops and asks.

**How it is approved.** The owner comments on #230 with "Approved" or with changes, naming the commit of this file. A change after approval is a new revision of this file and needs approval again. The approval covers stages A and B below. Stage C, the one AWS job, waits for a second, separate go-ahead after the owner has seen stage B's report.

Items marked **Proposed** are defaults for the owner to accept or change. No account id, ARN, bucket name, profile name, job id or secret appears here or anywhere in GitHub.

## Stages

| Stage | What happens | Changes in AWS |
| --- | --- | --- |
| A Discovery (P1-03) | The owner signs in. Reframe starts the pinned AWS Transform MCP server, lists its tools and schema hashes, and makes read-only reads of the workspace and its connectors | None |
| B Resource checks (P1-04) | Read-only checks of the resources below; one report to the owner of what was found, what matches, and what Stage C would cost | None |
| C One job (P1-05), after a second go-ahead | Snapshot, source copy, one requirements job, the owner's function selection, answers to AWS review tasks, retrieval of requirements and traceability | One source object, one Transform job and its records |

## The envelope

| Item | Proposed | Owner's choice |
| --- | --- | --- |
| Source | CardDemo at the commit v1 pinned (`59cc6c2`), snapshotted from a clean checkout. A checkout with local changes is refused for live work. Specification section 15 makes CardDemo the default; another public repository the owner names works the same way | |
| Function | One function. Reframe does not preselect it: AWS's job lists its business-function catalog, the owner picks one there in person, and Reframe passes AWS's name exactly. **Proposed:** the smallest function in the catalog that has an online (CICS) path, which keeps the job short. v1 found that AWS treats "Account and Customer Profile Administration" as one function (398 requirements); that is P2's domain | |
| AWS account and region | The owner's SSO profile and the region v1 used (us-east-1), recorded in the local project policy, never here. The owner signs in with `aws sso login`; Reframe never signs in or handles credentials | |
| AWS Transform MCP server | Pinned to `awslabs.aws-transform-mcp-server==0.2.4`, the version v1 resolved and cached. Stage A records its tool schema hashes; a later run with different hashes stops and asks | |
| Resources (P1-04 decision) | **Proposed: used as client-owned, through a resources file.** These already exist from v1: the Transform workspace, its project-named reimagine connector (active), that connector's IAM role, the Neptune test stack and its bucket, and the per-repo project bucket. Reframe checks them read-only and adds no tags; their configuration and permissions are unchanged afterwards (FR-02 acceptance). The other two options, `reframe resources adopt` (adds tags, needs its own confirmation) and a clean start (deletes), are not part of this envelope | |
| Project state | **Proposed:** for P1 only, the ledger, event log and manifest are kept in the local project folder and the run is attached to one machine. No Reframe state bucket is created. The state bucket, the lease and runs across machines come with P2, which builds `reframe bootstrap`. This is a P1 limit, not the specification's contract | |
| Data policy | Public source only. The Claude Code CLI backend is allowed by the policy, though this path makes no model call | |

### AWS operations

Only these. Every other tool, including `create_connector`, `accept_connector`, any delete, any IAM, CloudFormation or Neptune change, is refused before anything is sent. Operation names come from the server's own listing, never a console label.

| Operation | Kind | Limit | Rules |
| --- | --- | --- | --- |
| List the server's tools | Read | Once per stage | Calls no tool |
| `list_resources`, `get_resource`, `load_instructions` | Read | Within the duration; at most one read every 60 seconds while polling | |
| `get_job_status` | Read | Same | Always with `detailed: true`; without it the server writes into the job chat (v1, 17 November 2026) |
| S3: write the source archive | Data-plane write | 1 | To a declared prefix in the stack's bucket, checksum recorded. Skipped if an object with the same checksum is already there |
| `create_job` | Change | **1** | Stage C only, after the go-ahead. `orchestratorAgent` is the value AWS accepted in v1's job, read from v1's receipt, never guessed. Intent recorded before, receipt after |
| `send_message` | Change | 15 | Only to answer a question the job asks, with text from the review-task rules below |
| `complete_task` | Change | 15 | Only for a task the classifier (P0-11) recognizes, under the review-task rules below |

### Claude backend and models

None. P1-05 stores AWS's requirements and traceability unchanged with status `NOT_CHECKED`; checking them is later work. A step that needs a model call is outside this envelope.

### Spend

| Item | Estimate | Limit |
| --- | --- | --- |
| Model calls | 0 | 0 |
| AWS Transform | The owner stated on 16 November 2026 that this use has no charge. **To confirm again** | One job |
| Neptune Serverless | Bills about $0.32 an hour at its minimum while the stack runs, job or not. A job can scale it towards about $10.29 an hour. Estimate, from v1's reading of the stack | One job; the duration limit below. Worst case, the top rate for all 8 hours: about $80 more than idle (estimate) |
| S3 | One object of about 4 MB | One object |

Reframe reports these as estimates, labelled, and says AWS billing lags (NFR-03).

### Duration

| Limit | Proposed |
| --- | --- |
| The envelope | 7 days from approval, or until the chosen function's requirements are retrieved, whichever comes first |
| The job | 8 hours from `create_job`. At the limit Reframe stops polling and parks the project as `WAITING_HUMAN`. It does not stop the job: no stop operation is allowed here, so stopping is the owner's step in the AWS Transform console |
| Sign-in | When the SSO sign-in expires, work parks as `WAITING_EXTERNAL` until the owner signs in again; nothing retries in the meantime |

### Uncertain dispatch

- Never re-dispatched automatically.
- An operation is settled only from AWS's own state (a read-only listing or `get_resource`), a durable receipt, or a read-only CloudTrail lookup. A timeout, killed process, missing file or empty reply never proves a call did not happen.
- Otherwise it stays `UNCERTAIN` until the owner records the outcome or authorizes one more counted attempt.
- While `create_job` is uncertain, no second job is created (FR-14).

### Cleanup

Delete nothing: no resource, job, object, receipt or record. The job and the source copy stay. The Neptune stack keeps billing until the owner stops or deletes it; that is the owner's decision, made separately after P1. So is the old IAM role `reframe-reimagine-mainframe-modernization-test` that v1 left in place.

### Gates and AWS review tasks

Every decision on the live path is genuine. No simulated actor answers anything here; simulated actors stay in the offline tests, labelled.

| Decision | Who |
| --- | --- |
| Approve this envelope; the go-ahead for stage C | The owner, in person |
| The job's plan ("Assess and reimagine" in v1), the objective confirmation, "Proceed with this plan", the function catalog and the function selection, the reimagine confirmations | The owner, in person, each time (class `APPROVE_ONLY`) |
| Source location, collaborators, output language | Answered from this envelope (class `ANSWER_FROM_INTAKE`): the declared source copy, no collaborators, English only. **Proposed** values; the owner may change them |
| Display-only forms | Shown and recorded; nothing to answer (`DISPLAY_ONLY`) |
| Anything the classifier does not recognize, or that needs a value this envelope does not give | Parked for the owner (`PARK`); never guessed |

v1's standing delegation does not carry over (FR-20: v1 approvals are re-decided, never transferred). The specification's context gates 1 to 3 are not reached on this path.

### Stop and ask

Reframe stops, keeps everything it has, and asks the owner when:

- discovery shows a needed operation missing, or a tool schema hash differs from stage A's record;
- a resource check fails or a resource differs from what this envelope names;
- a step needs an operation, resource, value or model call this envelope does not list;
- a limit (calls, duration, spend) is reached;
- an operation is `UNCERTAIN`;
- AWS rejects a change.

### Evidence

Live evidence stays in the local project folder. GitHub gets public-safe records only: counts, statuses, content hashes and the capability record without identifiers. No job id, account id, ARN, bucket name or profile name.

## What v1 already proved live

From [#197](https://github.com/sknampally/reframe/issues/197), [#206](https://github.com/sknampally/reframe/issues/206) and [#173](https://github.com/sknampally/reframe/issues/173), 16 and 17 November 2026:

- All seven adapter operations were verified against the live server.
- A reimagine connector can be created from the CLI. A workspace holds only one reimagine connector. The project-named connector is active.
- One "Assess and reimagine" job ran to completion. AWS found 15 business functions in 4 domains, and the owner selected one in the job chat, because AWS's form gives no selection schema. Requirements and traceability were retrieved.
- Two rules the server's schemas do not state are now checked in v2 before dispatch: a status read needs `detailed: true`, and `create_job` needs `orchestratorAgent` ([port-or-drop.md](../port-or-drop.md)).

## Owner decisions needed

1. Source: CardDemo at `59cc6c2`, or another repository and commit.
2. Function: chosen at the catalog in person, and whether to prefer the smallest online function.
3. Resources (#233): client-owned through a resources file, or another option.
4. Project state kept locally for P1, with the state bucket left to P2.
5. The limits: operations, 8-hour job, 7-day envelope, and the Neptune estimate.
6. The three intake answers.
7. Confirm again that AWS Transform has no charge for this use.
8. Whether anyone other than the owner may answer the in-person decisions; if so, name them.
