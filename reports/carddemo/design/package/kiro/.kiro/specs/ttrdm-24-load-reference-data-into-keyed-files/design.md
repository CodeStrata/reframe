# Design: Load reference data into keyed files (TTRDM-C24)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

A scheduled job for operations that rebuilds the keyed transaction type and transaction category stores from their flat extract files, so that online screens and batch programs read current reference data. Each store is emptied and reloaded with every record from its file. No record may be lost or left over from the previous load.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-172 | Load transaction categories into keyed store | design note | THE Transaction Category Reference Load SHALL copy every record of the transaction category flat file (AWS.M2.CARDDEMO.TRANCATG.PS, read shared) into the keyed transaction category file (AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS, held exclusively), which the same job has just deleted and redefined empty, keyed on the first 6 characters of each 60-character record. | medium | app/jcl/TRANCATG.jcl:22-27, app/jcl/TRANCATG.jcl:33-49, app/jcl/TRANCATG.jcl:54-61 |
| TTRDM-BR-173 | Load transaction type master from flat file | design note | THE Transaction Type Reference Load SHALL copy every record of the transaction type flat file (AWS.M2.CARDDEMO.TRANTYPE.PS, read shared) into the keyed transaction type file (AWS.M2.CARDDEMO.TRANTYPE.VSAM.KSDS, held exclusively), which the same job has just deleted and redefined empty, keyed on the first 2 characters of each 60-character record. | medium | app/jcl/TRANTYPE.jcl:22-27, app/jcl/TRANTYPE.jcl:33-49, app/jcl/TRANTYPE.jcl:54-61 |

### Worked examples

- TTRDM-BR-172: transaction category flat file = 18 category records; keyed category file before the run = exists with older records → The keyed file is deleted, redefined empty and loaded with exactly the 18 records from the flat file; the older records are gone.
- TTRDM-BR-172: keyed category file before the run = does not exist → The failed delete is ignored (return code reset to 0), the file is defined and the flat-file records are loaded.
- TTRDM-BR-173: transaction type flat file = 7 type records (codes 01 to 07); keyed type file before the run = exists with older records → The keyed file is deleted, redefined empty and loaded with exactly the 7 records; earlier contents are not kept.

## Decision tables

None.

## Design notes

- TTRDM-BR-172: A full-refresh load of the transaction category lookup store (a table or cache keyed by type code plus category code, the first 6 characters of each 60-character record). Truncate or recreate it, then load every record from the category extract, which is read without locking it. Hold the store exclusively, or swap it in atomically, so readers never see a half-loaded store.
- TTRDM-BR-173: A full-refresh load of the transaction type lookup store, keyed by the 2-character type code at the start of each 60-character record. Truncate or recreate it, then load every record from the transaction type extract, which is read without locking it. Hold the store exclusively, or swap it in atomically, so readers never see a half-loaded store.

## Open questions

- SME-286: When loading transaction categories, should records already in the store be replaced, merged, or rejected as duplicates? (Reference data owner) On TTRDM-BR-172.
- SME-287: If the transaction category load fails partway, should the partly loaded store be restored, or the load rerun from the start? (Batch operations team) On TTRDM-BR-172.
- SME-296: When loading the transaction type store, should records already present be cleared, replaced, or kept? (Reference data owner) On TTRDM-BR-173.
- SME-297: For the transaction type load, what should happen when a record cannot be written (for example, a duplicate key) or the load is interrupted, and must it be safe to rerun? (Batch operations team) On TTRDM-BR-173.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).