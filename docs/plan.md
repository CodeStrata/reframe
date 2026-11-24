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
- **When it runs:** as its own command, and offered with the default answer yes in the guided run. It starts as soon as the run's Neptune graph exists, alongside AWS Transform (P2-15).

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
| P2-15 | Pipeline 2 alongside pipeline 1 | §3 Alongside pipeline 1 | Pipeline 2 starts when pipeline 1's AWS resources exist, in its own worker with its own lock; the two workers never overwrite each other's records; the comparison waits for AWS Transform's results; a stop in pipeline 1 stops pipeline 2 with the reason; a fresh guided CardDemo run with the default answers goes through both |

## Sharing the results

Specification: [sharing.md](sharing.md). An epic of its own, outside pipelines 1 and 2: the results of a run, shared with people who don't run Reframe.

| Story | Title | Specification | Done when |
|---|---|---|---|
| S-01 | `reframe publish`: a cleaned copy of a run's reports | §2 | AWS Transform's review, Claude's review, the comparison and the plugin's own pages are copied with an index page. Account IDs, ARNs, bucket names, S3 locations, job, workspace and connector IDs, profile names, e-mail addresses and local paths are removed. A check of the copy finds none left, or nothing is written |
| S-02 | The CardDemo reports in the repository | §3 | The reports of a full CardDemo run are in `reports/carddemo/`, linked from the README, and open in a browser from a clone with no Reframe run |
| S-03 | The reports in a private S3 bucket | §4 | One Terraform root creates a private, encrypted, versioned S3 bucket that refuses requests not over TLS. `reframe publish --to aws` uploads a cleaned copy under `<project>/<run>/`. The bucket outlives runs and is removed only by `reframe reports teardown`, by its own records |
| S-04 | Opening the reports with an AWS sign-in | §4 | `reframe reports` lists what is published and `reframe reports open` downloads a report with the reader's own AWS sign-in and opens it. Nothing can be read without access to the account (owner's decision, 23 November 2026). The CardDemo reports are uploaded and opened this way |
| S-05 | Spike: the AWS sign-in for a link | – | Done. IAM Identity Center belongs to the organization's management account, so a sign-in link needs its administrator to add a SAML application by hand |

S-06 to S-08, a link that opens a report in the browser after the AWS sign-in (CloudFront, Cognito federated with IAM Identity Center, and a sign-in check at the edge), were built and then dropped by the owner on 23 November 2026, before they were merged. Published reports stay in the private bucket and are opened or downloaded with each reader's own AWS sign-in. The AWS resources the link had created were removed by Reframe's records, and the three stories are closed as not planned.

In their place (owner's decision, 24 November 2026), the reports stay in the private bucket and anyone who can sign in to the account opens or downloads them by project name:

| Story | Title | Specification | Done when |
|---|---|---|---|
| S-09 | Find the reports bucket from any computer | §6 | `reframe reports` and `reframe reports open` work on a computer that did not publish: the bucket is found by its tags `ManagedBy=reframe` and `ReframeStore=reports` with the reader's own AWS sign-in. More than one such bucket is refused with the list. Teardown still goes only by the publisher's own records |
| S-10 | Open or download a report by project | §6 | `reframe reports open <project>` opens the project's latest published run and `--run <run>` an older one; `reframe reports download <project> --to <folder>` saves a copy to keep or send, with a warning for a macOS-protected folder |
| S-11 | One file to download from the S3 console | §6 | `reframe publish --to aws` also uploads `<project>/<run>/report.zip`, the same cleaned copy, so a reader without Reframe signs in to the AWS console and downloads one file. Republishing replaces it |

## Pipeline 3: reconcile

Specification: [pipeline-3.md](pipeline-3.md). It starts from the comparison of AWS Transform's and Claude's assessments, works on every rule except those both tools describe the same way, and decides each against the source code. It writes the recommended business rules, then the recommended requirements, and one SME question list. The person adds context: documents, review marks and answered questions (owner's decisions, 24 November 2026).

| Story | Title | Specification | Done when |
|---|---|---|---|
| P3-01 | Spike: one batch decided against the source | §4 R4 | On CardDemo, the decision prompt and schema run on three batches (a conflict, overlapping pairs, one-sided rules). The evidence check passes or catches each answer, and the time and usage per batch are measured and written into the specification |
| P3-02 | Preflight and inputs | §4 R0, R1 | `reframe reconcile` checks both pipelines, the complete pairing, the snapshot's SHA-256 and the sign-in, and runs on a torn-down run. The items, open questions and context are gathered: Markdown, text, PDF and Word documents; review exports, ignoring another snapshot's; answered questions |
| P3-03 | Identical pairs agreed | §4 R2 | `same` pairs become recommended rules without an agent, citing both tools; a *Needs change* or *Question* mark sends a pair to R4 |
| P3-04 | The estimate and limit | §3, §4 R3 | Items are batched by program; the estimate is shown, and Reframe stops and asks above `--max-batches` |
| P3-05 | Decisions with evidence | §4 R4 | Every batch's answer has a decision per item; evidence is checked to exist, asked once more, then becomes `needs_sme`; decisions are stored with their input hash and round |
| P3-06 | Running again with more context | §4 R4 *Running again* | A second run with one more answered question decides only the affected rules again and keeps the rest |
| P3-07 | One SME list | §4 R5 | Both tools' open questions and R4's are merged, each original kept exactly once; answered ones are marked with their source; CSV and JSON out, answered files back in |
| P3-08 | Recommended requirements | §4 R6 | Requirements in AWS Transform's frame, each citing a recommended rule; uncited ones dropped and counted; open questions carried; marked as recommended by Reframe |
| P3-09 | The reconciliation page and publish | §4 R7 | The page as specified, linked from the comparison, with marks and downloads; `reframe publish` includes it as `reconciled/` with a fourth card |
| P3-10 | Live acceptance and README | §7 | Every point of section 7 passes from the CLI; the README and `docs/cli.md` describe pipeline 3 from the tested commands |

## Later pipelines

Specified after pipelines 1 and 2 have been tested, first each on its own and then together.

- **Pipeline 4: final requirements, business rules and wireframes.** It produces them, takes more human context (text, Markdown, documents, PDFs and similar), and gives the updated version of each. This is where Reframe ends.
