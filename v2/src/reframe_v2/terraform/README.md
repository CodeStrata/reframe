# Reframe Terraform

Written out by `reframe bootstrap --terraform <dir>`; nothing here runs on its own, and writing it makes no AWS call.

| Folder | What it creates | Who applies it |
| --- | --- | --- |
| `bootstrap/` | The Reframe state bucket for one account and region. Its own state stays local, because the bucket does not exist yet | An administrator, once |
| `project/` | One repository's resources: the source bucket and the sandbox role, and, for the Bedrock backend, the invoke policy. State is kept in the state bucket with S3 locking | `reframe run --provision` |
| `modules/` | The pieces both use | |

Every resource carries the default tags `ManagedBy=reframe`, `ReframeProject` and `ReframeRun` (specification section 8). Terraform 1.10 or later is required, for S3 state locking without DynamoDB.

The Neptune knowledge graph and the reimagine connector role are not here yet; they follow in a later P2 story.
