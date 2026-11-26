# Security and public-content policy

This repository holds no deployed service. Security reporting and publication discipline still apply.

## Never publish

Credentials, tokens, private keys, session data, account/bucket/role identifiers, private endpoints, employer or client inventories, personal/customer data, internal logs, raw AWS Transform artifacts, or private artifact locations. Renaming an internal export does not make it public-safe. Use newly authored generic text and clearly labeled synthetic examples.

Keep private evidence outside the checkout, including ignored files. `.gitignore` is a convenience, not a security control; it does not protect already tracked files or history. Check diffs and commits before publication. Do not include sensitive details in issue bodies, PR descriptions, screenshots, or commit messages.

## Report privately

Do not open a public issue containing an exploit, secret, or private data. Use the repository's **Security > Report a vulnerability** option if available. Private vulnerability reporting has not been verified as enabled for this foundation. If unavailable, ask the owner through a public issue for a private reporting channel, without describing the sensitive finding or attaching evidence. No monitored security email or response SLA is claimed.

## If material is exposed

Stop further publication, notify the owner privately, and revoke or rotate exposed credentials immediately. Assess scope and access; coordinate any history cleanup with the owner. Deleting a file in a later commit does not remove it from Git history, forks, caches, or downloads. Do not republish the sensitive value in the cleanup report.

## What Reframe does to protect you

- **Recorded changes.** Every change Reframe makes in AWS or GitHub has an intent and a receipt in the run folder.
- **Consent first.** Teardown deletes only what those records say Reframe created, after you type `yes`. Publishing to GitHub Pages, which is public, also waits for a typed `yes`.
- **Cleaned copies.** `reframe publish` removes account IDs, ARNs, S3 locations, resource names, profile names, e-mail addresses and local paths, and refuses to write if any are left.
- **No keys kept.** Reframe stores no credentials. It signs in with your AWS CLI profile, Claude Code's own sign-in and your `gh` sign-in.
- **A private bucket.** `reframe publish --to aws` uploads the run's own `source/` and `results/` uncleaned, so give read access to the bucket only to people who may see the code.
