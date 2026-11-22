# Reframe plan: pipeline 1

Status: draft for the owner's agreement, with [the specification](specification.md).

## How the work is done

- One epic for pipeline 1, with the stories below. They go on the board once this plan is agreed.
- One pull request for the pipeline, with one commit per story. The owner merges.
- Code is new. It reuses what the earlier build proved live (the Terraform modules, the MCP client sessions, intent and receipt records, the task classifier), moved across one piece at a time with its tests.
- Unit tests run offline against recorded AWS replies from spike 1, with identifiers removed. Live runs are the acceptance test.

## Stories

| # | Story | Specification | Done when |
|---|---|---|---|
| 1 | Package skeleton, CLI and CI | §3 | `reframe --help` lists the commands; CI runs the tests |
| 2 | Run folder, event log, intent and receipt records, resume | §4, §6, §7 | A stopped run resumes without repeating a change; UNCERTAIN is settled from AWS's state |
| 3 | Preflight | §4 stage 0 | Each missing piece stops the run with the exact fix |
| 4 | Source snapshot and upload | §4 stages 1, 3 | The archive's SHA-256 matches the object in S3 |
| 5 | Terraform roots and apply | §4 stage 2 | Plans that only add, applied; outputs recorded |
| 6 | AWS Transform setup: workspace and connectors | §4 stage 4 | Connectors ACTIVE, IDs recorded from AWS's replies |
| 7 | Job creation and the driver loop | §4 stages 5, 6 | The job is polled and its tasks classified; done means every plan step SUCCEEDED |
| 8 | Answers: plan choice, function selection by structured chat reply, confirmation, defaults | §4 stage 6, §5 | Autonomous answers recorded in `decisions.json` |
| 9 | Interactive mode: `reframe answer` | §5 | Every waiting question can be answered from the CLI |
| 10 | Retrieval: download, check, unpack, manifest, summary | §4 stage 7 | Requirements and assessment downloaded and summarized |
| 11 | Teardown by recorded ID | §4 stage 8 | Nothing the run created remains; nothing it did not create is touched |
| 12 | `status` and `events` | §3 | Shows stage, plan steps, waiting question and next step |
| 13 | Live acceptance: three autonomous runs and one interactive run on CardDemo | §8 | All four pass; results recorded without identifiers |
| 14 | README | | Written last, from the tested commands |

## Decisions

These follow the owner's direction; change any of them before the stories go on the board.

- Test repository: CardDemo at a pinned commit.
- AWS Transform plan: assess and reimagine.
- The full repository includes the unassigned programs.
- Unknown questions in autonomous mode: AWS's default, recorded.
- Teardown: automatic after each run.
- Where it runs: locally on the owner's Mac.
