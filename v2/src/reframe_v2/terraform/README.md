# Reframe Terraform

Written out by `reframe bootstrap --terraform <dir>`; nothing here runs on its own, and writing it makes no AWS call.

| Folder | What it creates | Who applies it |
| --- | --- | --- |
| `bootstrap/` | The Reframe state bucket for one account and region. Its own state stays local, because the bucket does not exist yet | An administrator, once |
| `project/` | One repository's resources: the source bucket and the sandbox role; for the Bedrock backend, the invoke policy; with `reimagine = true`, the Neptune knowledge graph and the reimagine connector role. State is kept in the state bucket with S3 locking | `reframe run --provision` |
| `modules/` | The pieces both use | |

Every resource carries the default tags `ManagedBy=reframe`, `ReframeProject` and `ReframeRun` (specification section 8). Terraform 1.10 or later is required, for S3 state locking without DynamoDB.

First, `reframe graph` lists the region's Neptune clusters read-only and offers any that can serve the reimagine connector, by name. A cluster you choose goes in as `existing_graph`: it is used as it is, never tagged, changed or deleted, and only the connector role is created for it. Otherwise a new Serverless cluster goes in the account's default VPC (`graph_network`): Terraform adds its security groups, its bulk-loader role and, on route tables that lack one, the S3 gateway endpoint the bulk loader needs, and creates no VPC, subnet or route table. Either way the graph meets what AWS checks for the reimagine connector (engine 1.4.5.1 or later, IAM authentication, storage encryption, serverless scaling, two Availability Zones), and the project outputs the connector's configuration and role; the AWS Transform adapter creates the connector from them. `reframe graph --tfvars <file>` writes these variables.

Neptune Serverless bills per NCU-hour for every instance while the cluster runs, job or not. `neptune_max_capacity` (default 8 NCUs) and `neptune_instance_count` (default 1) bound it.

For a test, set `disposable = true` in both compositions so nothing is left when the test ends. Destroy `project/` first, then `bootstrap/`. Destroying `project/` deletes the source bucket with every object version in it, and deletes a graph Reframe created without a final snapshot. Destroying `bootstrap/` then deletes the state bucket. Copy what the run produced to the local project folder before you destroy anything. By default, `disposable` is `false`: a bucket that still holds data is not destroyed, and a deleted graph leaves a final snapshot. An existing graph you chose is never touched either way.
