# Reframe specification: sharing the results

Status: draft for the owner's agreement. Stories S-01 to S-12 in [the plan](plan.md), in their own epic, outside pipelines 1 and 2.

## 1. Goal

People who review the results (business users, subject-matter experts, a client) open them in a browser, without running Reframe or having access to the AWS account that ran it.

## 2. A cleaned copy of a run's reports (S-01)

`reframe publish [--run <id>] --to <folder>` copies into one folder:

- AWS Transform's business review (`aws/index.html`);
- Claude's business review (`claude/index.html`), when pipeline 2 ran;
- the comparison (`comparison/index.html`), when both did;
- the plugin's own report and interactive map (`claude/plugin/`), never its `SECRETS.local.md`;
- an index page naming the source, its commit and SHA-256, when each assessment ran, and the tool versions.

The links between the pages still work in the copy.

**What is removed.** The pages carry the run's records, so Reframe removes before writing anything:

- 12-digit account IDs and ARNs;
- S3 bucket names and `s3://` locations;
- AWS Transform job, workspace and connector IDs, and any other UUID;
- the AWS profile name, e-mail addresses, and local paths such as the home folder.

Each is replaced by a placeholder such as `<account>`. Reframe then checks the whole copy for each of those patterns. If any is still there, nothing is written and the file is named.

The review marks in a published copy stay in each reader's browser, as in the original. A reviewer downloads them from the page; the reconciliation's next round and `reframe review` read that download like one made on the run's own page, although the copy names items by their cleaned keys ([pipeline-3.md](pipeline-3.md), section 8.11).

## 3. The CardDemo reports in the repository (S-02)

The reports of a full CardDemo run (pipeline 1 and pipeline 2, same snapshot) are published into `reports/carddemo/` in the repository and linked from the README, so anyone can read them from GitHub or a clone. CardDemo is AWS's public sample, so its results can be shared. A newer run replaces the copy in a later commit.

## 4. The reports in your AWS account (S-03, S-04)

The owner's decision (23 November 2026): published reports are open only to people who can already sign in to the AWS account. So there is no public website and no CloudFront. The reports sit in a private S3 bucket, and each reader opens them with their own AWS sign-in.

**The bucket (S-03).** A Terraform root of its own, `reports`, apart from any run, creates one bucket per account and region:

- private: all public access blocked, objects owned by the bucket owner, and a policy that refuses any request not over TLS;
- encrypted and versioned;
- tagged `ManagedBy=reframe` and `ReframeStore=reports`;
- with its state and records in `~/.reframe/reports-store/`.

Reframe creates it the first time a report is uploaded, from a plan checked to only create.

**The commands.** They sign in with the saved profile and region, or `--profile` and `--region`.

| Command | What it does |
|---|---|
| `reframe publish [--run <id>] --to aws` | Uploads the run under `<project>/<run>/` in the bucket, with a receipt: `source/`, `results/` and `reports/` (S-15, below). |
| `reframe reports` | Lists the reports in the bucket: project, run, source and when each was published. |
| `reframe reports open <project>/<run>` | Downloads that report with your AWS sign-in into `~/.reframe/reports-store/cache/`, and opens it in your browser. |
| `reframe reports teardown` | Lists the bucket and how many objects it holds from the store's own records, asks for `yes`, and removes the bucket with its contents. |

**A run's three folders (S-15).** The owner's request (26 November 2026): publishing is optional; when the work is done, an engineer may publish the whole run to one bucket, with a folder each for the source, the results and the reports. The owner chose the standing bucket over each run's source bucket, which `reframe teardown` deletes, so a run can be published after teardown too.

```text
reframe-reports-xxxxxxxx/
  <project>/<run>/
    source/       <sha>.zip, the snapshot both tools read, and source.json (its checksum, files and origin)
    results/
      aws/        what AWS Transform wrote, as Reframe retrieved it
      claude/     what Claude's code-modernization plugin wrote
    reports/      the cleaned copy: every report, the design and the AI-DLC package, and report.zip
```

`source/` and `results/` are the run's own files, not cleaned. Anyone who can read the bucket can read the source code and the raw results, so give read access only to people who may see the code. The bucket is apart from every run, so `reframe teardown` leaves it and what is in it; publish after teardown as well as before.

Each folder is sent only if the run has it: a run with no Claude results has no `results/claude/`. A report published before S-15 sits at `<project>/<run>/` itself; `reframe reports` lists it and `open` and `download` still find it.

**Who can open them (S-04).** Only someone whose AWS sign-in may read the bucket: `s3:ListBucket` and `s3:GetObject` on it. That is anyone the account already trusts with S3 reads, and no one else. Readers can also download a report from the S3 console. Nothing is reachable without signing in to the account.

**Tried and dropped.** A link that opens a report in the browser after the AWS sign-in, so a reader needs no Reframe and no download, was built (S-05 to S-08) and dropped by the owner on 23 November 2026. It needed the organization's IAM Identity Center administrator to add an application by hand, and added CloudFront, a Cognito user pool and an edge function to the account. The reports stay in the bucket, opened as above.

## 5. GitHub Pages, optional (S-16, S-17)

The owner's decision (26 November 2026, [release 1.0](release-1.md), section 3): a person who wants a link to send, with nothing to install, can publish the cleaned copy to GitHub Pages. Like every publish target, it is optional.

```bash
reframe publish --to pages --repo <owner>/<name>
```

- Reframe makes the cleaned copy of section 2 and puts it on the repository's `gh-pages` branch, under `<project>/<run>/`, with a front page of every published run, newest first. Publishing the same run again replaces it.
- It uses the person's own GitHub sign-in through `git` and `gh`. It turns Pages on for the branch if it is off, then prints the address.
- **A Pages site is public**: anyone with the address can read it, on a public repository and on a private one too (only GitHub Enterprise Cloud can limit who reads a Pages site). So before anything is pushed, Reframe names the repository and the address, says the site is public, and asks the person to type `yes`. With no terminal it refuses.

**The demo (S-17).** This repository's own Pages site, <https://sknampally.github.io/reframe/>, serves `reports/`: the CardDemo copy of section 3 and a front page for it. Only CardDemo's reports are published; other codebases Reframe is tested on are run locally, and nothing from them is committed (the owner, 26 November 2026). A workflow deploys it on every push to `main` that changes `reports/`. It runs only in `sknampally/reframe`, so a fork publishes nothing unless its owner chooses to.

## 6. Opening and downloading by project (S-09 to S-11)

The owner's direction (24 November 2026): an engineer runs and publishes; an architect or stakeholder gets the project's name and opens or downloads the report with their own AWS sign-in. Nothing is hosted, and nothing is readable without that sign-in.

**Any computer in the account (S-09).** The store's records, and so the bucket's name, are only on the computer that published. On any other computer Reframe finds it by its tags (`ManagedBy=reframe`, `ReframeStore=reports`) in the reader's region, using the reader's sign-in; if it finds more than one it lists them and stops. A reader without permission for the tag index (`tag:GetResources`) is served by listing the account's `reframe-reports-…` buckets (`s3:ListAllMyBuckets`) and reading their tags; each found bucket is checked to exist, since the tag index can list a deleted one for a while. Finding by tag is used only for reading. Removing the bucket still needs the publisher's records (`reframe reports teardown`).

**By project name (S-10).**

| Command | What it does |
|---|---|
| `reframe reports open <project>` | Downloads the project's latest published run and opens its index page |
| `reframe reports open <project> --run <run>` | The same for an older run (`reframe reports` lists them) |
| `reframe reports download <project> [--run <run>] --to <folder>` | Saves the copy in a folder, to keep or send on; warns, as `publish` does, about a macOS-protected folder |

**Without Reframe (S-11).** `reframe publish --to aws` also uploads `report.zip`, the same cleaned copy in one file, with everything in one folder `<project>-<run>/`, next to the pages in `reports/`. `reframe reports open` and `download` leave it out. A reader signs in to the AWS console, opens the bucket in S3, and downloads `<project>/<run>/reports/report.zip`: the console downloads single files, not folders. They unzip it and open `index.html`.

Pre-signed download links are left out on purpose: they work for anyone who has the link, with no sign-in.

## 7. Requirements to a spreadsheet (S-12)

People who plan the new system work in spreadsheets: they sort, filter, assign and add their own columns. `reframe export --to xlsx` writes the reconciled results as one Excel workbook, so nobody has to copy them out of the page.

| Command | What it does |
|---|---|
| `reframe export --to xlsx` | Writes `outputs/reconcile/<project>-<run>-requirements.xlsx` from the latest run's reconciliation |
| `reframe export --to xlsx --out <file or folder>` | Writes it there instead; a folder gets the same file name |
| `reframe export --to xlsx --context <folder>` | Adds the reviewers' marks from the review downloads in that folder (default: the reconciliation's context folder) |
| `reframe export --to xlsx --open` | Opens it in the computer's spreadsheet app when written |

It needs the reconciliation done. It runs nothing, uses no AWS and no Claude, and reads only the run folder and the context folder.

**Sheets.** Each sheet is one table with a header row, frozen, with filters on, every column named in plain words. The workbook opens on Requirements.

| Sheet | One row per | Columns |
|---|---|---|
| About | fact | project, run, source and its SHA-256, round, when it was written, what it is (recommended by Reframe, model output for review), the counts, and the review downloads read or ignored |
| Domains | domain | name, kind, description, business functions, requirements |
| Business functions | function | domain, name, description, risk, capabilities, requirements, business rules, who signed it off and when |
| Capabilities | capability | domain, function, number, title, user story, risk, what it touches, requirements, open questions, decision tables |
| Requirements | requirement | domain, function, capability, ID, functional or non-functional, EARS pattern, the requirement, the business rules behind it (ID and name), their programs and source lines, kept from an earlier review |
| Business rules | recommended rule | domain, function, ID, name, the rule, kind, decision, confidence and why, program, source lines, whether the code runs and how it is reached, what it depends on, worked examples, requirements that cite it, possible defect, the AWS Transform and Claude rules it came from, round, who agreed it |
| Decision tables | table row or gap | domain, function, capability, table, conditions, values, outcome, the rule it cites, or "Gap" with the note for an SME |
| Open questions | question a requirement left | domain, function, capability, ID, question, status |
| SME list | SME question | ID, kind, defect call, question, owner, status, answer, settled by, where it came from, evidence |

Requirements, business rules, capabilities and open questions also carry two review columns: **Mark**, the reviewers' marks combined as the next round combines them (*Needs change*, then *Question*, then *Agree*), and **Reviewers' marks**, each reviewer's own mark and comment. Only downloads from the reconciled review of the same snapshot are read; others are listed as ignored on About, with the reason. The last column of those sheets is the item's **Key**, as the page names it, cleaned like every other cell (an AWS Transform ID becomes the stand-in `reframe publish` gives it). Marks downloaded from the run's own page and from a published copy are both matched.

**Kept safe.** Every cell is written as text, never as a formula, so a value that starts with `=` stays text. Every cell is cleaned as `reframe publish` cleans its copy (account ID, ARNs, S3 locations, IDs, e-mail addresses, local paths, the AWS profile); if anything is left, nothing is written and the sheet and row are named. The file is written with the standard library, so Reframe gains no dependency.

**Not read back.** The workbook is for reading and planning. Answers go in the SME list CSV (`reconcile/questions.csv`) and marks in the page's review downloads, which `reframe reconcile --context` reads; About says so.

## 8. The design as a backlog (S-13)

Teams plan the build in Jira or Azure DevOps. `reframe export --to jira` and `reframe export --to azure-devops` write the design's capabilities as that tool's CSV import file, so nobody types the backlog in again.

| Command | What it does |
|---|---|
| `reframe export --to jira` | Writes `outputs/design/<project>-<run>-jira.csv` |
| `reframe export --to azure-devops` | Writes `outputs/design/<project>-<run>-azure-devops.csv` |
| `--out <file or folder>` | Writes it there instead; a folder, made if need be, gets the same file name |

It needs the design's final specifications (`reframe design`), not only the reconciliation. The specifications already hold the acceptance criteria, written in Given/When/Then from the rules' worked examples (pipeline 4, D6), and the backlog keeps the AI-DLC package's IDs. A story, its requirements, rules, criteria and golden cases are named the same in the backlog, the package and the golden datasets. (Updated 26 November 2026 from "written from the rules": the specifications are where the criteria are written, so the backlog takes them from there.) It runs nothing, uses no AWS and no Claude, and needs no credentials: a person imports the file.

| Tool | Rows | Linked by |
|---|---|---|
| Jira | An Epic per business function, then a Story per capability | `Issue ID` and `Parent` (each story's epic), mapped at import |
| Azure DevOps | An Epic per domain, a Feature per business function, a User Story per capability | The `Title 1`, `Title 2` and `Title 3` columns, as Azure DevOps's import builds a hierarchy |

**A story** has:
- **Title:** the capability's ID and title.
- **Description:** the user story, and whether it is final or draft (draft: confirm it with the owner before building). Then the requirements and the business rules, each with its ID and class, and the open questions. Then the traceability: the package folder, the run key, how it runs, its risk and what it touches, and its golden dataset.
- **Acceptance criteria:** each with its ID and the rules it checks. For Jira they are a column to map to your field, and in the description too; for Azure DevOps they go in the Acceptance Criteria field.
- **Priority and tags:** priority comes from the capability's risk. Labels (Jira) or tags (Azure DevOps) are `reframe`, the status, `risk-<level>`, and the domain or the function's code.

Jira's text is in its wiki markup; Azure DevOps's fields are HTML, escaped. A cell that starts with `=`, `+`, `-` or `@` gets a leading space, so a spreadsheet that opens the file does not run it. Every cell is cleaned as `reframe publish` cleans its copy; if anything is left, nothing is written.

**On CardDemo** (run fa1f61, on a copy, 26 November 2026), each file took under a second:
- **Jira:** 11 epics and 154 stories (52 final).
- **Azure DevOps:** 5 epics, 11 features and 154 user stories.
- **Both:** 1,136 requirements and 1,503 acceptance criteria.

The largest cell is 23,659 characters, within Jira's limit of 32,767 for a text field.
