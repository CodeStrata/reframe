# Pipeline 1 acceptance

Live runs from the CLI against the criteria in [specification.md](specification.md), section 9. No account, resource or job identifiers are recorded here; each run's own folder holds them.

All runs used one AWS account in `us-east-1`, a new Neptune Serverless graph per run, and the sign-in as the only setup. The runs took place on 22 November 2026.

## Results

| Run | Mode | Source | Business functions | Requirements | Business rules | Open questions | Answers typed by a person |
|---|---|---|---|---|---|---|---|
| 1 | autonomous | GitHub URL (CardDemo) | 15 | 1,392 | 1,633 | 97 | 0 |
| 2 | autonomous | local folder (CardDemo) | 13 | 1,451 | 1,633 | 91 | 0 |
| 3 | autonomous | local ZIP (CardDemo's card authorization application, 40 files) | 2 | 225 | 155 | 11 | 0 |
| 4 | autonomous | GitHub URL (CardDemo) | 15 | 1,408 | 1,632 | 93 | 0 |
| 5 | interactive | local ZIP (card authorization) | 3 | 214 | 153 | 14 | 6, all through `reframe answer` |

In every run each requirement and rule in AWS's `traceability.yaml` files appears in the report, and every report tab renders.

Run 4 is the one that went from `reframe run` to the report with nothing but the sign-in. AWS's questions and forms were all answered by Reframe. Runs 1 to 3 and 5 each found a case the CLI did not handle yet (see below). The CLI was fixed and the run's worker restarted with `reframe resume`; the same AWS job carried on each time, and nothing was created twice.

The criterion for an existing Neptune cluster does not apply: the account has no cluster Reframe can use as it is. Run 5 listed the one cluster it found, another run's, and said why it could not be used ("no bulk-loader role on it can read the run's source bucket").

## Teardown

`reframe teardown` was run from the CLI after every run. Each time it listed 36 resources, all from the run's own records (three AWS Transform creation receipts, and the run's two Terraform states), and recorded consent before deleting.

- The job, workspace, buckets, IAM roles, network and Neptune graph were deleted every time.
- AWS Transform left a network interface in the run's VPC every time. Reframe deleted it, then the second Terraform destroy finished.
- The AWS Transform connector: DeleteConnector is refused for the signing-in role ("Your account is not authorized to make this call"), so teardown reports the connector by name, with its IAM role deleted. AWS removes the connector itself once its workspace is gone: after the last teardown, none of the five runs' connectors was listed any more, checked by each run's recorded connector ID.
- AWS's tag index still listed some deleted resources afterwards; each was checked in its own service and found gone.
- After the last teardown the account had the same number of VPCs as before the runs, no Neptune cluster and no Reframe bucket.

## What the runs found, and the fixes

AWS words its questions differently in every run. These were all found live and fixed in the CLI, each with an offline test built from AWS's actual message:

- Confirmations after the business function catalog came in many forms: `Reply "yes" to confirm`, `Reply "yes" to proceed with the reimagine workflow`, `(yes/no)`, `Do you want to proceed?`, a "please confirm to proceed" statement, and `please reply: **Yes, proceed**`. Reframe now recognises them by shape, and sends a reply AWS spells out exactly as given.
- AWS sometimes answered the confirmation with "already processed" and left its blocking "Review business functions discovery results" form open. After five quiet minutes Reframe now submits AWS's own response template for that form; in interactive mode it asks first. AWS then asks for the selection again, and Reframe sends the same selection (in interactive mode, as an option).
- Notices such as "What would you like to do next?", "Feel free to ask…" and "You'll be notified…" are no longer treated as questions, and a saved question is cleared once AWS says something newer.
- Resuming a run had dropped the job ID from the run's records, so teardown would have missed the job. It is now kept, and teardown also reads it from the job's own record.
- Runs started together corrupted Terraform's shared provider cache. Each run now has its own copy of the provider, made under a lock.
- The consent list now uses plain names for every resource type, and says up front that a network interface AWS Transform leaves behind is deleted too.

## Still to do

- The owner tests from the CLI and merges.
- A repeat of all five runs on the final code, with no changes in between, has not been done.
