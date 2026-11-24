# Reframe command reference

Every command, its options and examples, as `reframe --help` and `reframe <command> --help` show them. The [README](../README.md) explains what each pipeline does; this page is the list to keep open while you work.

## The home screen

`reframe` on its own shows your runs, the suggested next step and a numbered menu. Each menu entry runs one of the commands below; an action on a run asks which run, with the latest as the default. After each action the home screen comes back; `0` or Ctrl+D leaves it, and Ctrl+C cancels an action.

![The reframe home screen: the runs table, the suggested next step and the numbered menu](images/cli-home.svg)

*The home screen with one example run that has finished both pipelines.*

| # | Menu entry | Runs |
|---|---|---|
| 1 | Start a guided run | `reframe run` |
| 2 | Run status | `reframe status` |
| 3 | Answer a waiting question | `reframe answer` |
| 4 | Resume a run | `reframe resume` |
| 5 | Open the business review | `reframe report --open` |
| 6 | Assess with Claude (pipeline 2) | `reframe claude` |
| 7 | Open the comparison | `reframe compare --open` |
| 8 | Publish a run's reports to AWS | `reframe publish --to aws` |
| 9 | Published reports | `reframe reports` |
| 10 | Event log | `reframe events` |
| 11 | Tear down a run | `reframe teardown` |
| 12 | Set up prerequisites and sign-in | `reframe setup` |
| 13 | Help | `reframe --help` |
| 0 | Exit | |

## `reframe --help`

![reframe --help: the commands, common examples and options](images/cli-help.svg)

## A full run, start to finish

```bash
aws sso login --profile my-profile        # sign in to AWS; Reframe never sees your credentials
reframe run                               # guided: prerequisites, sign-in, source, choices, then one yes
reframe status                            # where the run is and what to do next
reframe events --follow                   # every step as it happens, until Ctrl+C
reframe answer                            # only if a question waits for you (interactive mode)
reframe report --open                     # AWS Transform's business review
reframe claude                            # pipeline 2, if you did not choose it in the guided run
reframe compare --open                    # AWS Transform and Claude compared
reframe publish --to aws                  # a cleaned copy in your account's private reports bucket
reframe reports open <project>/<run>      # open a published copy with your AWS sign-in
reframe teardown                          # remove the run's AWS resources, after you type yes
```

Every command acts on your latest run; add `--run <run id>` for another one. The home screen and `reframe status` show the run IDs.

**The guided run's questions**, in order:

1. Which AWS profile, and the region (default `us-east-1`).
2. Where the source is: a GitHub or Git URL (with a branch, tag or commit), a local folder or a ZIP file.
3. How AWS Transform's questions are answered: autonomous or interactive.
4. The project name, used in the run's folder and AWS resource names.
5. A new Neptune graph, or an existing cluster.
6. Whether to assess the same snapshot with Claude as well (pipeline 2), how Claude signs in (your Claude subscription or Amazon Bedrock), and the agent limit for rule extraction.
7. A summary of what will be created, and one yes to start.

**The agent limit** is a ceiling, not a target: before rule extraction Reframe compares the plugin's upper estimate with it, and stops to ask if the estimate is higher. On CardDemo the estimate is 38 to 41 shards, up to about 615 agents, and a run uses about 430 to 480; a limit of 650 to 900 lets it go ahead without asking.

**Starting pipeline 2 later.** If your Claude usage limit is close, answer no to Claude in the guided run and run `reframe claude` once the limit resets. On a run whose AWS resources are still being created, it is recorded and starts as soon as they exist; on a run that is further along, it starts at once, alongside AWS Transform.

## Commands

### `reframe run`

Assess mainframe source with AWS Transform: with no options, a guided run that checks and sets up everything first; the AWS resources stay until reframe teardown.

| Option | What it does |
|---|---|
| `--source <source>` | the mainframe source: a local folder, a local .zip file, or a GitHub URL; given, nothing is asked and the prerequisites are assumed to be set up |
| `--profile <profile>` | the AWS CLI profile to sign in with (default: the one saved by the guided setup) |
| `--ref <ref>` | for a Git checkout or URL: the branch, tag or commit to assess (default: HEAD) |
| `--mode autonomous\|interactive` | autonomous: Reframe answers AWS and records why; interactive: answer each question with reframe answer |
| `--region <region>` | AWS region (default: the one saved by the guided setup, then us-east-1) |
| `--project <project>` | project name used in resource names (default: from the source's name) |
| `--graph <graph>` | new, existing (choose from a list) or the name of an existing Neptune cluster (default: interactive mode asks; autonomous mode creates a new graph) |
| `--terraform <terraform>` | the Terraform binary to use (default: REFRAME_TERRAFORM, then the one Reframe installed, then terraform on PATH) |
| `--foreground` | run in this terminal instead of a background worker |

```bash
reframe run                                             # guided: asks for everything it needs
reframe run --source https://github.com/<owner>/<repo>  # a GitHub repository, latest commit
reframe run --source ~/code/app --ref release-1         # a local Git checkout, at a branch, tag or commit
reframe run --source app.zip --mode interactive         # a ZIP file; you answer AWS's questions with reframe answer
```

### `reframe setup`

Check and set up the prerequisites and the AWS sign-in, without starting a run.

### `reframe status`

The run's stage, the job's plan steps, any waiting question and the next step.

| Option | What it does |
|---|---|
| `--run <run>` | the run to act on (default: the latest run) |

```bash
reframe status             # the latest run
reframe status --run <id>  # another run, by the ID the home screen shows
```

### `reframe events`

The run's event log.

| Option | What it does |
|---|---|
| `--run <run>` | the run to act on (default: the latest run) |
| `--follow` | keep printing new events |

```bash
reframe events --follow  # keep printing new events until Ctrl+C
```

### `reframe answer`

Show AWS's waiting question, or answer it.

| Option | What it does |
|---|---|
| `--run <run>` | the run to act on (default: the latest run) |
| `<choices> ...` | option numbers as listed by reframe answer |
| `--text <text>` | a free-text answer, for a question without options |

```bash
reframe answer                        # show the waiting question and its numbered options
reframe answer 1 3                    # choose options 1 and 3
reframe answer --text "Yes, proceed"  # answer a question that has no options
```

### `reframe resume`

Continue a run that stopped; nothing with a receipt is repeated.

| Option | What it does |
|---|---|
| `--run <run>` | the run to act on (default: the latest run) |
| `--foreground` | run in this terminal instead of a background worker |

```bash
reframe resume  # continue the latest run, and pipeline 2 if it stopped too
```

### `reframe report`

Build the HTML report from the run's downloads again.

| Option | What it does |
|---|---|
| `--run <run>` | the run to act on (default: the latest run) |
| `--open` | open the report in the browser |

```bash
reframe report --open  # build the report again and open it
```

### `reframe claude`

Pipeline 2: assess the same snapshot with Claude's code-modernization plugin, show it in the same business review, load its graph into the run's Neptune cluster, and compare it with AWS Transform's results.

| Option | What it does |
|---|---|
| `--run <run>` | the run to act on (default: the latest run) |
| `--auth subscription\|bedrock` | how Claude signs in: your Claude subscription (default) or Amazon Bedrock with the run's AWS profile |
| `--max-agents <max_agents>` | the agent limit for rule extraction (default: 600) |
| `--mode autonomous\|interactive` | default: the run's mode |
| `--graph-load yes\|no` | load Claude's graph into the cluster (default: yes on a graph the run created, no on an existing cluster) |
| `--foreground` | run in this terminal instead of a background worker |

```bash
reframe claude                   # start pipeline 2 on the latest run, now or as soon as its AWS resources exist
reframe claude --max-agents 650  # a higher agent limit, so a larger estimate does not stop to ask
```

### `reframe compare`

Build the page comparing AWS Transform's and Claude's results again.

| Option | What it does |
|---|---|
| `--run <run>` | the run to act on (default: the latest run) |
| `--open` | open the page in the browser |

```bash
reframe compare --open  # build the comparison page again and open it
```

### `reframe publish`

Copy a run's reports, cleaned of the AWS account's identifiers, into a folder others can open.

| Option | What it does |
|---|---|
| `--run <run>` | the run to act on (default: the latest run) |
| `--to <to>` | a folder to write the copy into (for example reports/carddemo), or aws to upload it to the private reports bucket in your AWS account |
| `--profile <profile>` | for --to aws: the AWS profile (default: the one saved by reframe setup) |
| `--region <region>` | for --to aws: the AWS region (default: the saved one, then us-east-1) |

```bash
reframe publish --to aws                # upload to the private reports bucket in your AWS account
reframe publish --to reports/my-system  # write the copy into a folder
```

### `reframe reports`

The reports published to your AWS account: list them, open one with your AWS sign-in, or remove the bucket.

| Option | What it does |
|---|---|
| `<action>` | list (the default): what is published; open: download one and open it; teardown: remove the bucket |
| `<path>` | for open: <project>/<run>, as reframe reports lists it |
| `--profile <profile>` | the AWS profile (default: the one saved by reframe setup) |
| `--region <region>` | the AWS region (default: the saved one, then us-east-1) |

```bash
reframe reports                       # list the published reports
reframe reports open <project>/<run>  # download one with your AWS sign-in and open it
reframe reports teardown              # remove the bucket and every report in it, after your consent
```

### `reframe teardown`

List every AWS resource the run created, ask for consent, record it, then remove them.

| Option | What it does |
|---|---|
| `--run <run>` | the run to act on (default: the latest run) |

```bash
reframe teardown  # list the latest run's AWS resources, then remove them after you type yes
```

## Where things are

| Path | What it holds |
|---|---|
| `~/.reframe/config.json` | The saved profile, region and tool paths: the next run's defaults |
| `~/.reframe/projects/<project>/runs/<run>/` | A run: its state, event log, change records, Terraform roots, downloads and reports |
| `…/outputs/report/index.html` | AWS Transform's business review |
| `…/outputs/claude/report/index.html` | Claude's business review |
| `…/outputs/comparison/index.html` | The comparison page |
| `~/.reframe/reports-store/` | The private reports bucket's Terraform state and records, and `cache/` for reports opened with `reframe reports open` |

`reframe publish` builds one more page, the copy's `index.html`, which links the three reports above with the source, its commit and SHA-256. It exists only in a published copy: open it with `reframe reports open <project>/<run>`, or from the folder you gave to `--to`.

**On a Mac, publish outside Desktop, Documents and Downloads.** macOS keeps those folders private: a browser that has not been given access to one opens `index.html` but not the pages it links to. Reframe warns when you publish there. Use a folder such as `~/reframe-reports/<project>`, or give the browser access in System Settings > Privacy & Security > Files and Folders.
