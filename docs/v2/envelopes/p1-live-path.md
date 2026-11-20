# P1 live path: execution envelope (draft)

**Status: revision 4, for the owner's decision. Stage A ran under revision 3 on 20 November 2026 and changed nothing ([#232](https://github.com/sknampally/reframe/issues/232)); nothing else has run.** Story: [#230](https://github.com/sknampally/reframe/issues/230) (P1-01). Specification: section 15 (P1), section 11, section 8, section 4 (uncertain dispatch, AWS review tasks), FR-14.

**Revision 2 (19 November 2026):** the first run assumes no Neptune graph is in place. Stage B lists the region's Neptune clusters and the owner chooses one by name, or a new graph. Only a new graph needs stage C, which creates it in the account's default VPC (owner, 19 November 2026; [#250](https://github.com/sknampally/reframe/issues/250)).

**Revision 3 (20 November 2026):** the test leaves nothing behind. Stage E removes everything stages C and D created: the job and the Transform workspace with its connectors, then every Terraform resource, including both buckets with their contents and the graph without a final snapshot. What the run produced is saved locally first, and a read-only listing at the end shows nothing is left (owner, 19 November 2026; [#253](https://github.com/sknampally/reframe/issues/253)). It needs P2-07's `disposable` setting, merged.

**Revision 4 (20 November 2026):** a new graph gets its own private network. Stage B found no default VPC in the test region, so revision 2's network had nowhere to go. As AWS's own Neptune template does, Terraform now creates a VPC, two subnets in different Availability Zones, a route table and an S3 gateway endpoint, with no internet gateway or NAT; stage E removes them with the graph. No existing network is used or changed (owner, 20 November 2026: "Always its own VPC"; [#259](https://github.com/sknampally/reframe/issues/259)). It needs P2-08, merged. Stage A's record stands: it ran under revision 3, made no change, and its operations and tool schemas are what this revision relies on.

This envelope says exactly what the P1 live path may do:
- the read-only discovery in P1-03 ([#232](https://github.com/sknampally/reframe/issues/232));
- the resource checks and the graph choice in P1-04 ([#233](https://github.com/sknampally/reframe/issues/233));
- the resources a new graph needs;
- one function, from selection to retrieved requirements, in P1-05 ([#234](https://github.com/sknampally/reframe/issues/234)).

Anything not listed here is outside the envelope, and Reframe stops and asks.

**How it is approved.** The owner comments on #230 with "Approved" or with changes, naming the commit of this file. A change after approval is a new revision of this file and needs approval again. The approval covers stages A and B below. Every later stage waits for its own separate go-ahead, given after the owner has seen the report from the stage before.

Items marked **Proposed** are defaults for the owner to accept or change. No account id, ARN, resource id, bucket name, profile name, job id or secret appears here or anywhere in GitHub.

## Stages

| Stage | What happens | Changes in AWS | Needs |
| --- | --- | --- | --- |
| A Discovery (P1-03) | The owner signs in. Reframe starts the pinned AWS Transform MCP server, lists its tools and schema hashes, and makes read-only reads of the workspaces and their connectors | None | This approval |
| B Checks and the graph choice (P1-04) | `reframe graph` lists the region's Neptune clusters and says which can serve the reimagine connector and why the others cannot. The owner chooses one by name, or a new graph. For a new graph, Reframe shows the Terraform plan, including the graph's own network. One report covers what was found, what stage C would create and what it would cost | None | This approval |
| C Provision (only for a new graph) | Terraform creates the resources in the "New graph" table below, from the saved plan the owner reviewed. Reframe then creates the Transform workspace and both connectors | Creates what the table lists. Neptune bills from here | A second go-ahead, after stage B's report |
| D One job (P1-05) | Snapshot, source copy, one requirements job, the owner's function selection, answers to AWS review tasks, and retrieval of the requirements and traceability | One source object, one Transform job and its records | A further go-ahead |
| E Full teardown | Reframe saves the requirements, traceability, receipts and plans in the local project folder. It deletes the job and the workspace it created, through the server's own delete operations, and checks the connectors are gone. Terraform destroys `project/`, then `bootstrap/`. A read-only listing then shows nothing tagged for the project is left | Deletes everything stages C and D created. No snapshot is kept | The owner's explicit confirmation |

## The envelope

| Item | Proposed | Owner's choice |
| --- | --- | --- |
| Source | CardDemo at the commit v1 pinned (`59cc6c2`), snapshotted from a clean checkout. A checkout with local changes is refused for live work. Specification section 15 makes CardDemo the default; another public repository the owner names works the same way | |
| Function | One function. Reframe does not preselect it: AWS's job lists its business-function catalog, the owner picks one there in person, and Reframe passes AWS's name exactly. **Proposed:** the smallest function in the catalog that has an online (CICS) path, which keeps the job short. v1 found that AWS treats "Account and Customer Profile Administration" as one function (398 requirements); that is P2's domain | |
| AWS account and region | The owner's SSO profile and the region v1 used (us-east-1), recorded in the local project policy, never here. The owner signs in with `aws sso login`; Reframe never signs in or handles credentials | |
| AWS Transform MCP server | Pinned to `awslabs.aws-transform-mcp-server==0.2.4`, the version v1 resolved and cached. Stage A records its tool schema hashes; a later run with different hashes stops and asks | |
| Neptune graph (P1-04 decision) | **Chosen by the owner at stage B, by name.** If a listed cluster can serve the connector and the owner names it, it is used as client-owned: never tagged, changed or deleted, and out of stage E. Otherwise a new graph is created in stage C. Sharing a graph between repositories is unproven (section 8), so the report says whether another reimagine connector already uses the named cluster | |
| Other resources with an existing graph | If v1's Transform workspace already has a reimagine connector on the chosen cluster, P1 uses that workspace, connector, connector role and bucket as client-owned, through a resources file. Nothing is created and stage C is skipped. A chosen cluster with no connector of its own takes the new-graph path's workspace and connectors (below), but not its graph | |
| Resources with a new graph | Everything in the "New graph" table, under one project name. A new Transform workspace is needed, because AWS allows one reimagine connector per workspace and v1's workspace already has one | |
| Who runs Terraform | **Proposed:** Reframe writes the Terraform and the variables, then runs `init` and `plan` (read-only) and saves the plan. The owner reads the plan and runs `terraform apply <saved plan>` themselves, so exactly the reviewed changes are made. The same goes for `destroy` in stage E | |
| Project state | **Proposed:** Terraform state goes in the Reframe state bucket, with S3 locking. Reframe's own ledger, event log and manifest stay in the local project folder for P1, so the run is tied to one machine. Runs across machines come with P2's run command | |
| Test resources | **Proposed:** the project is disposable (`disposable = true` in both Terraform compositions, P2-07). Destroying it deletes both buckets with every object version and the graph without a final snapshot | |
| Data policy | Public source only. The Claude Code CLI backend is allowed by the policy, though this path makes no model call | |

### New graph (stage C)

Every resource is named from the project name, starts with `reframe-` and carries the tags `ManagedBy=reframe`, `ReframeProject` and `ReframeRun`.

| Resource | Created by | Notes |
| --- | --- | --- |
| Reframe state bucket | Terraform, `bootstrap/` composition | Encrypted, versioned, private. Its own state stays on the owner's machine. Created for this test and removed at stage E, last |
| Source bucket and sandbox role | Terraform, `project/` composition | Encrypted, versioned, private; the role cannot read outside the bucket. Removed at stage E with its contents |
| Neptune Serverless cluster, 1 instance, 1 to 8 NCUs | Terraform, `project/` with `reimagine = true` | Engine 1.4.5.1, IAM authentication, encryption |
| The graph's own VPC, two subnets in different Availability Zones, one route table | Terraform, `project/` | Private: no internet gateway, NAT or peering. No charge. Removed at stage E with the graph |
| S3 gateway endpoint | Terraform, on the graph's own route table | The bulk loader needs it. No charge |
| Two security groups, the Neptune subnet group, the bulk-loader role | Terraform | In the graph's own subnets. Only the connector reaches Neptune |
| Reimagine connector role | Terraform | The trust and permissions v1 recorded from the console (#206) |
| Transform workspace, assessment connector, reimagine connector | Reframe, through the MCP server | With the arguments v1 used live. If AWS returns a verification link, the owner opens it and approves the connection in person |

No internet gateway, NAT or peering is created, and no existing network, including another project's VPC, is used or changed. If the region has no room for another VPC, the plan fails and Reframe stops and asks.

### AWS operations

Only these. Every other tool, including any stop operation and any delete operation not listed here, and any IAM, EC2, CloudFormation or Neptune change outside the saved Terraform plan, is refused before anything is sent. Operation names come from the server's own listing, never a console label.

| Operation | Kind | Stage | Limit | Rules |
| --- | --- | --- | --- | --- |
| List the server's tools | Read | A to E | Once per stage | Calls no tool |
| `list_resources`, `get_resource`, `load_instructions` | Read | A to E | At most one read every 60 seconds while polling | At E, they confirm the job, workspace and connectors are gone |
| `get_job_status` | Read | D | Same | Always with `detailed: true`. Without it, the server writes into the job chat (v1, 17 November 2026) |
| AWS CLI describe, get and simulate calls | Read | B, E | As needed | At B, the calls `reframe graph` and the resource checks make. At E, the final listing: resources tagged with the project's `ReframeProject` tag (Resource Groups Tagging API `get-resources`), and describe calls for the cluster, VPC, buckets and roles. Nothing else |
| `terraform init` and `plan` | Read | B, E | As needed | The plan is saved for the owner. At E, `plan -destroy` saves each destroy plan for the owner to read |
| `terraform apply <saved plan>` | Change | C | 2: `bootstrap/`, then `project/` | Run by the owner (proposed), exactly the reviewed plan. A plan that differs from the reviewed one is refused |
| `create_workspace` | Change | C | 1 | Arguments as v1 used live |
| `create_connector` | Change | C | 2 | One `mainframe_modernization\|s3\|2` and one `mainframe_modernization\|reimagine\|1`, with the configuration Terraform outputs. Intent recorded before, receipt after |
| `accept_connector` | Change | C | 2 | With the role Terraform created for each |
| S3: write the source archive | Data-plane write | D | 1 | To the declared prefix in the connector's bucket, with its checksum recorded. Skipped if an object with the same checksum is already there |
| `create_job` | Change | D | **1** | After the go-ahead. `orchestratorAgent` is the value AWS accepted in v1's job, read from v1's receipt, never guessed. Intent recorded before, receipt after |
| `send_message` | Change | D | 15 | Only to answer a question the job asks, with text from the review-task rules below |
| `complete_task` | Change | D | 15 | Only for a task the classifier (P0-11) recognizes, under the review-task rules below |
| `delete_job` | Delete | E | 1 | Only the job `create_job` made, by its receipt. Only if stage A's listing shows the operation; its arguments come from the server's schema, never guessed. Intent recorded before, receipt after |
| `delete_workspace` | Delete | E | 1 | Only the workspace `create_workspace` made, by its receipt, after its job is deleted. Same rules. A workspace that was used as client-owned is never deleted |
| `terraform apply <saved destroy plan>` | Delete | E | 2: `project/`, then `bootstrap/` | Run by the owner (proposed), after the Transform deletions, exactly the reviewed destroy plan. `project/` removes the graph, roles, security groups, subnet group, S3 endpoint, route table, subnets, VPC and the source bucket with its contents. `bootstrap/` then removes the state bucket. A destroy plan that would delete anything stage C did not create is refused |

### Claude backend and models

None. P1-05 stores AWS's requirements and traceability unchanged, with status `NOT_CHECKED`; checking them is later work. A step that needs a model call is outside this envelope.

### Spend

Estimates. Reframe labels them as estimates and says that AWS billing lags (NFR-03). Neptune prices are from v1's reading ($0.1608 per NCU-hour in us-east-1); check current pricing.

| Item | Estimate | Limit |
| --- | --- | --- |
| Model calls | 0 | 0 |
| AWS Transform | The owner stated on 16 November 2026 that this use has no charge. **To confirm again** | One job |
| Neptune, existing graph | No new resource. It keeps billing what it already does: v1's test stack runs about $0.32 an hour at idle, and v1 saw it scale towards about $10.29 an hour during a job | One job and the 8-hour limit. Worst case: about $80 more than idle |
| Neptune, new graph | About $0.16 an hour at idle (1 instance at 1 NCU), up to about $1.29 an hour at its 8-NCU ceiling. An 8-hour job at the ceiling costs about $10.30. Removed right after the job, the whole run costs about $11. Left for the full 7 days, it costs about $36 | The 8-NCU ceiling, one instance, and stage E. Capped at 8 NCUs, the job may run slower than v1's did; that is not yet measured |
| Neptune final snapshot | None: a disposable project deletes the graph without one | |
| Network, buckets, roles, workspace, connectors | No charge, apart from S3 storage for a few MB | |

### Duration

| Limit | Proposed |
| --- | --- |
| The envelope | 7 days from approval, or until stage E's final listing is reported, whichever comes first |
| The job | 8 hours from `create_job`. At the limit, Reframe stops polling and parks the project as `WAITING_HUMAN`. It does not stop the job: no stop operation is allowed here, so stopping it is the owner's step in the AWS Transform console |
| Stage E | **Proposed:** offered as soon as the requirements are retrieved and saved locally, or when the job limit is reached. Until the owner confirms it, the new graph keeps billing at idle. If the job is still running at the limit, the owner stops it in the console before stage E |
| Sign-in | When the SSO sign-in expires, work parks as `WAITING_EXTERNAL` until the owner signs in again; nothing retries in the meantime |

### Uncertain dispatch

- An operation is never re-dispatched automatically.
- An operation is settled only from:
  - AWS's own state (a read-only listing, `get_resource`, or Terraform state read with `terraform show`);
  - a durable receipt;
  - a read-only CloudTrail lookup.
- A timeout, killed process, missing file or empty reply never proves a call did not happen.
- Otherwise the operation stays `UNCERTAIN` until the owner records the outcome or authorizes one more counted attempt.
- While `create_job`, `create_workspace` or `create_connector` is uncertain, no second one is created (FR-14).
- An interrupted `terraform apply` is resumed only from the state it left, after a new plan the owner reviews.

### Cleanup

Outside stage E, nothing is deleted: no resource, job, object, receipt or record.

Stage E removes everything stages C and D created, in this order, after the owner confirms it once:
1. **Save locally:** the requirements, traceability, receipts, ledger and Terraform plans go to the local project folder, with their content hashes recorded.
2. **The job,** with `delete_job`.
3. **The workspace,** with `delete_workspace`. Then a read checks that the workspace and both connectors are gone. v1's tool listing had no connector delete, so whether deleting a workspace removes its connectors is checked here, not assumed.
4. **`project/`:** the graph without a final snapshot, the connector role, the security groups, the subnet group, the S3 endpoint, the route table, both subnets and the VPC, the sandbox role, and the source bucket with every object version.
5. **`bootstrap/`:** the state bucket. It is last, because `project/`'s state lives in it.
6. **Final listing:** a read-only listing of the project's tag, and describe calls for the cluster, VPC, buckets and roles, reported to the owner.

If a Transform delete operation is missing at stage A, or a step fails, Reframe stops, keeps everything it has, and reports what is left. The owner then removes it in the console. Nothing is retried on its own.

**Never touched:**
- an existing cluster the owner chose at stage B;
- a workspace, connector, role or bucket used as client-owned;
- v1's test stack and the old IAM role `reframe-reimagine-mainframe-modernization-test`, which v1 left in place;
- v1's Transform workspace and its job, which stage A found still listed as running;
- every other VPC in the region, including those of other projects.

Removing v1's leftovers is the owner's separate decision. If the owner did not choose v1's stack at stage B, it keeps billing until the owner removes it.

### Gates and AWS review tasks

Every decision on the live path is genuine. No simulated actor answers anything here; simulated actors stay in the offline tests, labelled.

| Decision | Who |
| --- | --- |
| Approve this envelope; the go-aheads for stages C and D; the confirmation for stage E | The owner, in person |
| The graph choice at stage B, by name, or a new graph | The owner, in person |
| Reviewing each saved Terraform plan before it is applied | The owner, in person |
| The connector verification link, if AWS returns one | The owner, in person, in the AWS console |
| The job's plan ("Assess and reimagine" in v1), the objective confirmation, "Proceed with this plan", the function catalog and the function selection, the reimagine confirmations | The owner, in person, each time (class `APPROVE_ONLY`) |
| Source location, collaborators, output language | Answered from this envelope (class `ANSWER_FROM_INTAKE`): the declared source copy, no collaborators, English only. These are **Proposed** values; the owner may change them |
| Display-only forms | Shown and recorded; nothing to answer (`DISPLAY_ONLY`) |
| Anything the classifier does not recognize, or that needs a value this envelope does not give | Parked for the owner (`PARK`); never guessed |

v1's standing delegation does not carry over (FR-20: v1 approvals are re-decided, never transferred). The specification's context gates 1 to 3 are not reached on this path.

### Stop and ask

Reframe stops, keeps everything it has, and asks the owner when:

- discovery shows a needed operation missing, or a tool schema hash differs from stage A's record;
- a resource check fails, or a resource differs from what this envelope names;
- the region has fewer than two Availability Zones, or no room for another VPC;
- a Terraform plan would create, change or delete anything outside the "New graph" table, or would change any existing resource;
- a step needs an operation, resource, value or model call this envelope does not list;
- a limit (calls, duration, spend) is reached;
- an operation is `UNCERTAIN`;
- AWS rejects a change;
- a destroy plan would delete anything stage C did not create;
- stage E's final listing shows a resource tagged for the project, or a workspace or connector Reframe created, still present.

### Evidence

Live evidence stays in the local project folder, and so do the Terraform variables and plans, which name the account. GitHub gets public-safe records only: counts, statuses, content hashes, and the capability record without identifiers. No job id, account id, ARN, resource id, bucket name or profile name goes there.

## What v1 already proved live

From [#197](https://github.com/sknampally/reframe/issues/197), [#206](https://github.com/sknampally/reframe/issues/206) and [#173](https://github.com/sknampally/reframe/issues/173), 16 and 17 November 2026:

- All seven adapter operations were verified against the live server.
- A workspace and connectors can be created from the CLI. A workspace holds only one reimagine connector.
- One "Assess and reimagine" job ran to completion. AWS found 15 business functions in 4 domains. The owner selected one in the job chat, because AWS's form gives no selection schema. Requirements and traceability were retrieved.
- Two rules the server's schemas do not state are now checked in v2 before dispatch: a status read needs `detailed: true`, and `create_job` needs `orchestratorAgent` ([port-or-drop.md](../port-or-drop.md)).

**Not yet proven live:**
- the graph listing and checks;
- a graph in a private network Terraform builds, rather than one AWS's template builds;
- whether the bootstrap policy covers every call Terraform makes. The owner's SSO role is used here, not the bootstrap policy;
- the server's `delete_job` and `delete_workspace`, and whether deleting a workspace removes its connectors.

## Owner decisions needed

1. Source: CardDemo at `59cc6c2`, or another repository and commit.
2. Function: chosen at the catalog in person, and whether to prefer the smallest online function.
3. The graph: chosen at stage B by name, or a new graph. Nothing is needed now.
4. Who runs `terraform apply` and `destroy`: the owner (proposed), or Reframe after the owner has reviewed the plan.
5. Stage E: a full teardown (proposed, as you asked), as soon as the requirements are retrieved and saved locally (proposed), or later.
6. Terraform state in a new Reframe state bucket, created for this test and removed last at stage E; Reframe's own state kept locally for P1.
7. The limits: operations, the 8-hour job, the 7-day envelope, the 8-NCU ceiling and the spend estimates.
8. The three intake answers.
9. Confirm again that AWS Transform has no charge for this use.
10. Whether anyone other than the owner may make the in-person decisions; if so, name them.
