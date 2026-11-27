# Design: Read transactions by processed timestamp (UP-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Gives batch processes a way to read transactions in the order they were processed, by keeping a secondary index on the processed timestamp of the transaction master. Many transactions may share a timestamp. The index must include every transaction on the master.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-051 | Build transaction alternate index | design note | THE Transaction Alternate Index Setup SHALL read every record of the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) and fill the alternate index (AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX) with entries keyed on each transaction's processed timestamp, so transactions can be read by processed timestamp. | medium | app/jcl/TRANIDX.jcl:46-54, app/jcl/TRANIDX.jcl:25-28, app/cpy/CVTRA05Y.cpy:4-18 |
| UP-BR-052 | Define transaction alternate-key access path | design note | THE Transaction Alternate Index Setup SHALL define an access path (AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX.PATH) over the transaction alternate index that the job defines in the step before. That index is keyed on the transaction processed timestamp, and many transactions may share the same timestamp. This path is how transaction records are read by processed timestamp. | medium | app/jcl/TRANIDX.jcl:19-34, app/jcl/TRANIDX.jcl:36-44, app/cpy/CVTRA05Y.cpy:4-18 |

### Worked examples

- UP-BR-052: Job = TRANIDX; Alternate index = AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX defined in STEP20 → STEP25 defines path AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX.PATH, so transactions can be read by processed timestamp

## Decision tables

None.

## Design notes

- UP-BR-051: A non-unique secondary index on the transaction table's processed-timestamp column, covering every existing row. In a relational database this is a CREATE INDEX, which the database keeps up to date, not a separate rebuild job.
- UP-BR-052: Expose a query or repository method that reads transactions by processed timestamp (exact match or range, in timestamp order) using that non-unique index. It must allow many transactions per timestamp.

## Open questions

None.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).