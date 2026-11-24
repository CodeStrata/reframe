# Reframe specification: sharing the results

Status: draft for the owner's agreement. Stories S-01 to S-04 in [the plan](plan.md), in their own epic, outside pipelines 1 and 2.

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
