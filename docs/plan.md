# Reframe plan: pipeline 1

Status: draft for the owner's agreement, with [the specification](specification.md).

## How the work is done

- One epic for pipeline 1, with the stories below on the board.
- Every story is built, then the builder runs one full round of acceptance from the CLI (specification section 9), then opens one PR with a commit per story. The owner tests from the CLI and merges.
- Code is new and laid out by area (specification section 6). It reuses what the earlier build proved live (the Terraform modules, the MCP client sessions, intent and receipt records, the task classifier), moved across one piece at a time with its tests.
- Unit tests run offline against recorded AWS reply shapes from spike 1, with identifiers removed. Live runs are the acceptance test.

## Stories

| Story | Title | Specification | Done when |
|---|---|---|---|
| P1-01 | Package skeleton, CLI and CI | §3 | `reframe --help` lists the commands; CI runs the tests |
| P1-02 | Run folder, event log, intent and receipt records, resume | §4, §7, §8 | A stopped run resumes without repeating a change; UNCERTAIN is settled from AWS's state |
| P1-03 | Preflight | §4 stage 0 | Each missing piece stops the run with the exact fix |
| P1-04 | Source input (folder, ZIP, GitHub), snapshot and upload | §4 stages 1, 3 | Each source form gives a checked archive whose SHA-256 matches the object in S3 |
| P1-05 | Terraform roots and apply | §4 stage 2 | Plans that only create, applied; outputs recorded |
| P1-15 | Neptune graph: a new one or an existing cluster | §4 stage 2 | The clusters are listed with what each lacks; a usable one can be chosen and is used as it is, never changed |
| P1-17 | Code layout by area | §6 | Core, source, infrastructure, Transform and report code each in its own folder, with tests alongside |
| P1-06 | AWS Transform setup: workspace and reimagine connector | §4 stage 4 | Connector ACTIVE, IDs recorded from AWS's replies |
| P1-07 | Job creation and the driver loop | §4 stages 5, 6 | The job is polled and its tasks classified; done means every plan step SUCCEEDED with "Generate requirements" in the plan |
| P1-08 | Autonomous answers: plan, source location, function selection, confirmation, defaults | §4 stage 6, §5 | Autonomous answers recorded in `decisions.json` |
| P1-09 | Interactive mode: `reframe answer` | §5 | Every waiting question can be answered from the CLI |
| P1-10 | Retrieval: download, check, unpack, manifest, summary | §4 stage 7 | Requirements and assessment downloaded and summarized |
| P1-16 | HTML report | §4 stage 8 | One self-contained report covers the overview, functions, requirements, business rules, open questions, data model, assessment and decisions |
| P1-11 | Teardown: inventory, recorded consent, deletion by recorded ID | §4 stage 9 | Every resource is listed at once, consent is recorded before anything is deleted, and nothing the run created remains |
| P1-12 | `status` and `events` | §3 | Shows stage, plan steps, waiting question and next step |
| P1-13 | Live acceptance from the CLI | §9 | Every run in section 9 passes; results recorded without identifiers |
| P1-14 | README | | Written last, from the tested commands |
| P1-18 | Guided prerequisites: check, install on request, remember | §3 | Each missing tool is named with its install command for macOS or Linux and installed only on a yes; Terraform is installed by Reframe and checked against HashiCorp's SHA-256 sums; the MCP server is fetched once; paths are saved and used |
| P1-19 | Guided run: sign-in, source and choices | §3 | `reframe run` with no arguments chooses a profile, checks or starts the sign-in, takes and checks the source, asks the mode, project and Neptune choice, shows a summary, and starts on one yes; `reframe run --source` asks nothing |
| P1-20 | The look of the first console | §3 | Header panel, coloured status, tables and numbered choices in the guided run and `reframe status`; plain output without a terminal |
| P1-21 | Home screen and help in the look of the first console | §3 | `reframe` alone shows the header, the runs with their status, the suggested next step and a numbered menu that runs each command; `reframe --help` and each command's help show tables of commands and options with examples; plain help and exit code 2 without a terminal |

## Decisions

These follow the owner's direction; change any of them before the build finishes.

- Sources: a local folder, a local ZIP file or a GitHub repository; any mainframe codebase.
- AWS Transform plan: assess and reimagine, over the full source including the unassigned programs.
- Neptune: a new graph by default in autonomous mode; an existing cluster when the person chooses one.
- Unknown questions in autonomous mode: AWS's default when it marks one, recorded; otherwise wait for `reframe answer`.
- Teardown: only on `reframe teardown`, after the full list is shown and consent is recorded.
- Where it runs: locally on the owner's Mac.

## Pipeline 2, part 1: business review of the AWS Transform results

The AWS Transform results are kept and shown so that business users and functional subject-matter experts can review them, before the second assessment (with Claude's code-modernization plugin, on the same source snapshot) is specified. Specification section 4, stage 8.

| Story | Title | Specification | Done when |
|---|---|---|---|
| P2-01 | Read AWS's documents in full | §4 stage 8 | Domain and function names and descriptions come from AWS's catalog; capabilities, user stories, schedules, recovery notes, requirements, open questions and owners are read from every requirements document; each open question in AWS's files is counted once |
| P2-02 | Business review report, from overview down to each requirement | §4 stage 8 | Overview, domain, function and capability levels, each requirement with the business rules behind it, a breadcrumb and search; technical detail in its own section; checked on the outputs of every live run |
| P2-03 | Review marks and their export | §4 stage 8 | Agree, Needs change or Question with a comment on each requirement, rule and open question; progress per domain and function; CSV and JSON downloads naming the run, the source's SHA-256 and the reviewer |

