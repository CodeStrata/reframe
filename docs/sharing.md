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

## 4. A static site on AWS (S-03, S-04)

For clients on AWS, the reports are served from their own account:

- **Infrastructure:** a Terraform root of its own, `site`, apart from any run, creates:
  - a private S3 bucket (encrypted, versioned, public access blocked);
  - a CloudFront distribution that reads the bucket through origin access control, over HTTPS with CloudFront's own certificate, or a custom domain and certificate when the owner gives them.
- **Publishing:** `reframe publish --run <id> --to aws` makes the cleaned copy of section 2 and uploads it under the run's path, then prints the address.
- **Lifetime:** the site outlives the runs. It is removed only by its own teardown, which lists what the site's records say it created, asks for consent and deletes by those records.
- **Who can open it (S-04)** is the owner's choice, to be settled before it is built: anyone with the link, an IP allow list, or a sign-in in front of CloudFront.
