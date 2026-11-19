# Reframe Terraform

Written out by `reframe bootstrap --terraform <dir>`; nothing here runs on its own, and writing it makes no AWS call.

| Folder | What it creates | Who applies it |
| --- | --- | --- |
| `bootstrap/` | The Reframe state bucket for one account and region. Its own state stays local, because the bucket does not exist yet | An administrator, once |
| `project/` | One repository's resources: the source bucket and the sandbox role; for the Bedrock backend, the invoke policy; with `reimagine = true`, the Neptune knowledge graph and the reimagine connector role. State is kept in the state bucket with S3 locking | `reframe run --provision` |
| `modules/` | The pieces both use | |

Every resource carries the default tags `ManagedBy=reframe`, `ReframeProject` and `ReframeRun` (specification section 8). Terraform 1.10 or later is required, for S3 state locking without DynamoDB.

The Neptune graph is built from nothing: its own VPC, two private subnets in different Availability Zones, an S3 gateway endpoint, security groups, the Serverless cluster and its bulk-loader role. Nothing is assumed to exist. It meets what AWS checks for the reimagine connector (engine 1.4.5.1 or later, IAM authentication, storage encryption, serverless scaling). The project outputs the connector's configuration and role; the AWS Transform adapter creates the connector from them.

Neptune Serverless bills per NCU-hour for every instance while the cluster runs, job or not. `neptune_max_capacity` (default 8 NCUs) and `neptune_instance_count` (default 1) bound it.
