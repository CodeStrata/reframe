# Spike P2-02: the graph in Neptune

22 November 2026, on a live pipeline 1 run of CardDemo with a new Neptune Serverless graph (engine 1.4.5.1, IAM authentication on). No identifiers are recorded here.

## What AWS Transform writes

- AWS Transform writes its knowledge graph as **RDF N-Quads** (`.nq`) into the run's source bucket under `transform-output/<job>/<id>/kg_sync/`, then loads it into Neptune. So the graph is queried with **SPARQL**, not Gremlin or openCypher.
- **The files** (25 for CardDemo, 121 MB):
  - `code-analysis/` (components, executables, jobs, screens, transactions, scheduler tasks);
  - `data-analysis/` (data dictionary, 75 MB, and data lineage);
  - `business-function-discovery/` (business domains and functions);
  - `bre/` (business rules, one file per business function and one for the unassigned programs, written in batches).
- **The vocabulary** is AWS's own:
  - classes and properties live under `http://aws.amazon.com/transformkg/ontology/`, and resources under `http://aws.amazon.com/transformkg/data/<id>/<id>/`;
  - everything sits in **one named graph per job**, `http://aws.amazon.com/transformkg/graph/<id>/<id>`.
- **On the run, the graph held 235,657 quads.** The main node types: 9,100 record fields, 4,149 data-movement elements, 2,103 rule items, 600 data-source fields, 334 data sources, 250 business rules (each with a slice and an evidence pack), 144 executables (programs), 56 jobs, 25 transactions, 21 screens, 15 business functions, 5 business domains.
- **Programs are `o:Executable` with `o:name`** (for example `executable_COACTUPC`). This is the anchor that lets Claude's results be joined to AWS's.

## How a load reaches the private cluster

The cluster has no public endpoint. Its security group admits port 8182 only from the run's "app" security group, which the reimagine connector uses. A small function inside the run's VPC is enough:

- **Network:** an AWS Lambda function (Python 3.12, no extra packages) in the run's app subnets with the app security group. The run's Terraform already allows that group to reach the cluster on 8182 and S3 through the gateway endpoint.
- **Requests:** the function signs requests with SigV4 for `neptune-db` (botocore, which is in the Lambda runtime). It supports four actions:
  - `load`: `POST /loader` with format `nquads`, reading from the run's bucket through the cluster's existing bulk-loader role;
  - `status`: `GET /loader/<id>`;
  - `sparql`: queries;
  - `update`: SPARQL Update, for example `DROP GRAPH`.
- **IAM:** the function's role gets `neptune-db:connect`, `StartLoaderJob`, `GetLoaderJobStatus`, `ReadDataViaQuery`, `WriteDataViaQuery` and `DeleteDataViaQuery` on the cluster's resource ID, the Lambda network-interface permissions, and its own log group.
- **Reframe** invokes the function with `aws lambda invoke` using the exported credentials it already uses for Terraform.

## What was tried

| Step | Result |
|---|---|
| Create the function, role and log group (Terraform, a plan that only creates) | 5 resources, applied in 4 minutes (most of it the VPC attachment) |
| SPARQL: count quads per named graph | One AWS graph, 235,657 quads |
| SPARQL: count nodes per type | 38 types, as above |
| Upload a 5-quad file to `s3://<run bucket>/reframe/claude-graph/` and bulk-load it | `LOAD_COMPLETED` in 3 seconds: 5 records, no errors |
| Count the new named graph `urn:reframe:graph:claude:<run>` | 5 |
| Join a Claude rule to AWS's program by name (`c:citesModule` → `o:Executable` with the same `o:name`) | Matched |
| `DROP SILENT GRAPH <urn:reframe:graph:claude:<run>>`, then count | 0 in Claude's graph; AWS's graph still 235,657 |
| Destroy the function, role and log group | 12 seconds |
| Wait for AWS to release the function's two network interfaces | About 19 minutes; until then both show "in use" |

## Findings that shape the build

1. **Format:** Claude's graph is written as N-Quads in its own named graph, `urn:reframe:graph:claude:<run>`, with Reframe's small vocabulary under `urn:reframe:claude:ontology:`. Every resource IRI starts `urn:reframe:claude:<run>:`. The graph records the snapshot's SHA-256.
2. **Linking:** Claude's modules carry the program name, so a SPARQL join reaches AWS's `o:Executable` without copying anything into AWS's graph.
3. **Removal:** on an existing cluster, `DROP GRAPH` on Reframe's own named graph removes exactly what Reframe loaded, by the run's recorded graph IRI, and nothing of AWS's.
4. **The loader function** belongs in the project Terraform root, created only when pipeline 2 runs, with receipts like the rest.
5. **Teardown order:** after the function is deleted, its two Lambda network interfaces stay "in use" for a while. The security group and subnets can't be deleted until AWS releases them. Teardown must delete the function first, then wait for its interfaces to go (about 19 minutes here; Reframe waits up to 45), then destroy the network.
6. **Retrieval:** the `kg_sync/` files are AWS Transform's own graph. Reframe still does not download them; the graph is read with SPARQL when needed.
