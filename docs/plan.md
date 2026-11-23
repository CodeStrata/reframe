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
| P1-25 | Autonomous answers: the readiness menu after the selection | §4 stage 6 | The readiness menu is answered with its one choice that proceeds; "no further action is needed" is a notice; the catalog's review form is never submitted while a question offering choices waits; offline tests for each wording recorded on 23 November 2026 |
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
| P1-22 | Read AWS's documents in full | §4 stage 8 | Domain and function names and descriptions come from AWS's catalog; capabilities, user stories, schedules, recovery notes, requirements, open questions and owners are read from every requirements document; each open question in AWS's files is counted once |
| P1-23 | Business review report, from overview down to each requirement | §4 stage 8 | Overview, domain, function and capability levels, each requirement with the business rules behind it, a breadcrumb and search; technical detail in its own section; checked on the outputs of every live run |
| P1-24 | Review marks and their export | §4 stage 8 | Agree, Needs change or Question with a comment on each requirement, rule and open question; progress per domain and function; CSV and JSON downloads naming the run, the source's SHA-256 and the reviewer |

## Decisions

These follow the owner's direction; change any of them before the build finishes.

- Sources: a local folder, a local ZIP file or a GitHub repository; any mainframe codebase.
- AWS Transform plan: assess and reimagine, over the full source including the unassigned programs.
- Neptune: a new graph by default in autonomous mode; an existing cluster when the person chooses one.
- Unknown questions in autonomous mode: AWS's default when it marks one, recorded; otherwise wait for `reframe answer`.
- Teardown: only on `reframe teardown`, after the full list is shown and consent is recorded.
- Where it runs: locally on the owner's Mac.

## Pipeline 2: the Claude assessment and the comparison

Specification: [pipeline-2.md](pipeline-2.md). One epic for pipeline 2, with the stories below. The two spikes come first and may change the stories after them; any change goes back into the specification before it is built. One PR for pipeline 2, with a commit per story; the owner tests from the CLI and merges.

Decisions agreed with the owner:

- **Steps:** the plugin's `preflight`, `assess`, `map` and `extract-rules`, the counterpart of AWS Transform's assessment; not its planning or build steps.
- **Requirements:** generated by Reframe from Claude's results, in AWS Transform's shape, marked as such; the plugin's own outputs kept as written.
- **Sign-in:** the owner's Claude subscription by default, with Amazon Bedrock (the run's AWS profile, or a Bedrock API key from the environment) as the alternative.
- **Agent limit:** set before rule extraction.
- **Rule pairing:** by program, and an AI pass that is labelled as AI output.
- **Plugin usage counts:** off.
- **When it runs:** as its own command, and offered with the default answer yes in the guided run, so it follows AWS Transform automatically.

| Story | Title | Specification | Done when |
|---|---|---|---|
| P2-01 | Spike: the plugin headless on CardDemo | §2, §4 C0–C5 | The four steps run with `claude -p` on the subscription and through Bedrock. A note without identifiers records the files and formats written, where the plugin waits for a person headless, where the estimate is read, and the time, agents and tokens per step |
| P2-02 | Spike: the graph in Neptune | §4 C7 | A note records what AWS Transform writes into the graph, the load format, and a load and a query that reach the private cluster from Reframe, tried on a live run |
| P2-03 | Claude prerequisites and sign-in | §4 C0 | Claude Code, its sign-in (subscription or Bedrock), the pinned plugin and `python3` are checked and offered in the guided setup, installed only on a yes. The plugin's usage counts are off. A Bedrock API key is never written by Reframe |
| P2-04 | Workspace from the run's snapshot | §4 C1 | The snapshot's SHA-256 matches pipeline 1's (a mismatch stops the run). The copy is read-only, edits are denied in the settings, Reframe writes the intent, and no AWS Transform result is in the workspace |
| P2-05 | `reframe claude`: the plugin's steps in the worker | §3, §4 C2–C5 | Preflight answers are recorded as decisions or sent with `reframe answer`. Assess, map and rule extraction run with a receipt each. The agent limit is checked before extraction, and resume uses the plugin's run ID. The snapshot is unchanged at the end |
| P2-06 | Guided run continues into pipeline 2 | §3 | The guided run asks with the default answer yes, then asks the sign-in and the agent limit. The worker starts pipeline 2 when pipeline 1 is done. `status`, the home screen and its menu show both pipelines |
| P2-07 | Claude's graph in the same Neptune cluster | §4 C7, teardown | Claude's elements are loaded with source, run and SHA-256, and checked with a query. An existing cluster is loaded only on a yes. Teardown removes what Reframe added, by its records |
| P2-08 | Read Claude's outputs in full | §4 C5 | Preflight, assessment, map, rules and data objects are read into the report model, and the counts match the files on every live run |
| P2-09 | Requirements generated by Reframe from Claude's results | §4 C6 | Domain, function, capability and requirements in AWS Transform's shape. Each cites a rule card or a source line, or is dropped and counted. Each is labelled "generated by Reframe from Claude's results" and kept in its own file |
| P2-10 | Claude's business review report | §4 C8 | Same levels, look and review marks as pipeline 1, the rule cards as written, SME questions, technical detail, and links to the plugin's own pages. The export names the tool |
| P2-11 | Common model and pairing by program | §4 C8 | Domains are aligned by shared programs, with program coverage per tool and rules listed side by side per program, from both runs' files |
| P2-12 | AI pairing of rules, labelled | §4 C8 | A Claude step proposes rule pairs, each with a reason and a confidence, marked as AI output, which a person can mark right or wrong |
| P2-13 | The comparison page | §4 C8 | Overview first, then domains, programs, rules and what only one tool found. Every number links to the items in both reports, and the model-output caveat is stated |
| P2-14 | Live acceptance and README | §7 | Every point of the specification's section 7 passes from the CLI. The README describes pipeline 2 from the tested commands |

## Later pipelines

Specified after pipelines 1 and 2 have been tested, first each on its own and then together.

- **Pipeline 3: reconcile.** It starts from the comparison of AWS Transform's and Claude's assessments. An agent looks only where the two do not match or disagree, and writes the final recommended business rules and requirements. The person can add context as Markdown, documents, PDFs and similar files.
- **Pipeline 4: final requirements, business rules and wireframes.** It produces them, takes more human context (text, Markdown, documents, PDFs and similar), and gives the updated version of each. This is where Reframe ends.
