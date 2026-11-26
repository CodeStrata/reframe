# Design: Load customer and policy data stores (ADPLM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Fills the new customer store and policy store with every record from the supplied customer and policy input files, so the online application starts with its existing records already in place. It is run by application administrators as part of setting up an environment. Each load runs only if its store was created successfully, and it must copy every record, with none dropped or changed.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-001 | Load second data store from input | design note | WHEN the step that defines the policy data store (DEFINE2) ends with a return code of 7 or less, or did not run, THE data store setup job SHALL copy every record from the supplied policy input data set into the new policy data store (KSDSPOLY); WHEN DEFINE2 ends above 7, it SHALL skip the load. | medium | base/cntl/adef121.jcl:37-52, base/cntl/adef121.jcl:65-73 |
| ADPLM-BR-002 | Load first data store from input | design note | WHEN the step that defines the customer data store (DEFINE1) ends with a return code of 7 or less, or did not run, THE data store setup job SHALL copy every record from the supplied customer input data set into the new customer data store (KSDSCUST); WHEN DEFINE1 ends above 7, it SHALL skip the load. | medium | base/cntl/adef121.jcl:12-27, base/cntl/adef121.jcl:55-63 |

### Worked examples

- ADPLM-BR-001: DEFINE2 return code = 0 → all policy records are copied into KSDSPOLY
- ADPLM-BR-001: DEFINE2 return code = 8 → the policy load step is skipped
- ADPLM-BR-002: DEFINE1 return code = 0 → all customer records are copied into KSDSCUST
- ADPLM-BR-002: DEFINE1 return code = 12 → the customer load step is skipped

## Decision tables

None.

## Design notes

- ADPLM-BR-001: A one-time bulk import step in the environment set-up pipeline. It copies every record from the supplied policy extract into the policy store and depends on the step that creates the store: run the import when that step succeeded (severity 7 or less) or was skipped, and skip it when that step failed with a severity above 7. Report how many records were read and how many were written so the load can be reconciled.
- ADPLM-BR-002: The same guarded bulk import for customers. Copy every record from the supplied customer extract into the customer store, but only when the step that creates the store succeeded (severity 7 or less) or did not run. Skip the import when that step failed with a severity above 7. Report the record counts.

## Open questions

- SME-001: The two data loads are identified only by legacy labels. Which data stores are the input and the target for the first load and for the second load? (Application data owner) On ADPLM-BR-001, ADPLM-BR-002.
- SME-002: Each load copies every record into its target store. Is the target store empty before the load, or are existing records replaced, merged, or rejected as duplicates? (Application data owner) On ADPLM-BR-001, ADPLM-BR-002.
- SME-003: If a load stops partway through, should a rerun start again from the beginning, and must the target store be cleared first? (Batch operations) On ADPLM-BR-001, ADPLM-BR-002.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (4 in all).