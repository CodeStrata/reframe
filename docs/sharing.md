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

## 5. A link that asks for the AWS sign-in (S-05 to S-08)

The owner's goal (23 November 2026): an engineer finishes a run and sends a link; the architect or stakeholder opens it in a browser and signs in with their own AWS identity, with nothing to download.

**What the spike found (S-05).**
- The organization's IAM Identity Center runs in `us-west-2` and belongs to another account, the one that manages the organization. The run's account reaches it only as a member.
- An application for Reframe's reports can only be added there by an Identity Center administrator, in the console. AWS offers no API for a custom SAML application.
- Everything else lives in the run's account.

**How it works.**
- **CloudFront** serves the private reports bucket through origin access control, over HTTPS on its own `cloudfront.net` address. The bucket stays private: CloudFront is the only thing allowed to read it.
- **Amazon Cognito** handles the sign-in: a user pool whose only way in is the organization's IAM Identity Center, federated as a SAML identity provider. Nobody gets a separate password, and the user pool has no users of its own.
- **An edge function** (Lambda@Edge, Node.js, viewer request) checks every request before CloudFront serves anything:
  - a request with a valid Cognito session cookie (a JWT, its signature checked against the user pool's keys, issuer, audience and expiry) is served;
  - a request without one is sent to the sign-in, straight to IAM Identity Center;
  - the sign-in returns to `/_reframe/callback`, which exchanges the code for tokens and sets the session cookie, marked secure, HTTP-only and same-site.
- **Who may open reports** is decided in IAM Identity Center, by assigning the Reframe reports application to people or groups.

**Commands.**
- `reframe publish --to aws` uploads as before and prints the report's link.
- `reframe reports url <project>/<run>` prints the link again.
- `reframe reports site` shows the settings the Identity Center administrator needs for the application:
  - the assertion consumer service URL;
  - the audience;
  - the attribute for e-mail.
- `reframe reports site --idp-metadata <url>` connects the application once the administrator gives its metadata URL.

**Until that is done,** the link exists but nobody can sign in, so nothing is exposed.

**Removal.** `reframe reports teardown` also removes CloudFront, the edge function and the user pool, by the store's records. AWS keeps an edge function's copies for a while after CloudFront stops using it. If it can't be deleted yet, teardown says so, and running it again later finishes the job.
