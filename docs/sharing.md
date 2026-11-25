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

The review marks in a published copy stay in each reader's browser, as in the original.

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
| `reframe publish [--run <id>] --to aws` | Makes the cleaned copy of section 2 and uploads it under `<project>/<run>/` in the bucket, with a receipt. |
| `reframe reports` | Lists the reports in the bucket: project, run, source and when each was published. |
| `reframe reports open <project>/<run>` | Downloads that report with your AWS sign-in into `~/.reframe/reports-store/cache/`, and opens it in your browser. |
| `reframe reports teardown` | Lists the bucket and how many objects it holds from the store's own records, asks for `yes`, and removes the bucket with its contents. |

**Who can open them (S-04).** Only someone whose AWS sign-in may read the bucket: `s3:ListBucket` and `s3:GetObject` on it. That is anyone the account already trusts with S3 reads, and no one else. Readers can also download a report from the S3 console. Nothing is reachable without signing in to the account.

**Tried and dropped.** A link that opens a report in the browser after the AWS sign-in, so a reader needs no Reframe and no download, was built (S-05 to S-08) and dropped by the owner on 23 November 2026. It needed the organization's IAM Identity Center administrator to add an application by hand, and added CloudFront, a Cognito user pool and an edge function to the account. The reports stay in the bucket, opened as above.

## 6. Opening and downloading by project (S-09 to S-11)

The owner's direction (24 November 2026): an engineer runs and publishes; an architect or stakeholder gets the project's name and opens or downloads the report with their own AWS sign-in. Nothing is hosted, and nothing is readable without that sign-in.

**Any computer in the account (S-09).** The store's records, and so the bucket's name, are only on the computer that published. On any other computer Reframe finds it by its tags (`ManagedBy=reframe`, `ReframeStore=reports`) in the reader's region, using the reader's sign-in; if it finds more than one it lists them and stops. A reader without permission for the tag index (`tag:GetResources`) is served by listing the account's `reframe-reports-…` buckets (`s3:ListAllMyBuckets`) and reading their tags; each found bucket is checked to exist, since the tag index can list a deleted one for a while. Finding by tag is used only for reading. Removing the bucket still needs the publisher's records (`reframe reports teardown`).

**By project name (S-10).**

| Command | What it does |
|---|---|
| `reframe reports open <project>` | Downloads the project's latest published run and opens its index page |
| `reframe reports open <project> --run <run>` | The same for an older run (`reframe reports` lists them) |
| `reframe reports download <project> [--run <run>] --to <folder>` | Saves the copy in a folder, to keep or send on; warns, as `publish` does, about a macOS-protected folder |

**Without Reframe (S-11).** `reframe publish --to aws` also uploads `report.zip`, the same cleaned copy in one file, with everything in one folder `<project>-<run>/`, next to the pages. `reframe reports open` and `download` leave it out. A reader signs in to the AWS console, opens the bucket in S3, and downloads `<project>/<run>/report.zip`: the console downloads single files, not folders. They unzip it and open `index.html`.

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
