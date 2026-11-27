# Design: Calculate monthly interest as system transactions (DTPR-C08)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## Overview

The scheduled monthly interest job, run at billing-cycle close for a supplied processing date. It turns interest on category balances into system transactions and writes them to a new system transaction file of 350-byte records. It serves the card operations team. It must run before transactions are combined, and it must never leave a partial system transaction file when it fails.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-063 | Run interest step producing system transactions | design note | THE Interest Calculation job SHALL run the interest program (CBACT04C) with the processing date supplied as an external parameter, '2022071800' in the delivered job, reading the transaction category balances, card cross-reference (by card and by account), account master and disclosure groups in shared mode. | medium | app/jcl/INTCALC.jcl:22-41, app/cbl/CBACT04C.cbl:28-56, app/cbl/CBACT04C.cbl:175-180, app/cbl/CBACT04C.cbl:473-480 |
| DTPR-BR-064 | Run interest step producing system transactions | design note | THE Interest Calculation job SHALL write the generated system transactions to a new generation of the system transaction file (AWS.M2.CARDDEMO.SYSTRAN) of fixed 350-byte records, cataloged when the step ends normally and deleted if the step fails. | medium | app/jcl/INTCALC.jcl:22-41, app/cbl/CBACT04C.cbl:28-56, app/cbl/CBACT04C.cbl:175-180, app/cbl/CBACT04C.cbl:473-480 |
| DTPR-BR-065 | Run interest step producing system transactions | business rule | THE Interest Calculation job SHALL run monthly, at billing-cycle close, before the job that combines the system transactions (COMBTRAN). | medium | app/jcl/INTCALC.jcl:22-41, app/cbl/CBACT04C.cbl:28-56, app/cbl/CBACT04C.cbl:175-180, app/cbl/CBACT04C.cbl:473-480 |

### Worked examples

- DTPR-BR-063: Job parameter = '2022071800' → The interest program runs with processing date 2022071800 and the input files remain open to other readers
- DTPR-BR-064: Step outcome = normal end → A new SYSTRAN generation is cataloged
- DTPR-BR-064: Step outcome = abend → The new SYSTRAN generation is deleted
- DTPR-BR-065: Billing cycle = closes 31 July → The interest job runs once for that cycle, then COMBTRAN runs

## Decision tables

None.

## Design notes

- DTPR-BR-063: Run a scheduled monthly job that takes the processing date as a run parameter (the delivered job used '2022071800') rather than the system clock, so a run can be repeated or backdated. It reads category balances, the card cross-reference by card and by account, accounts and disclosure groups without locking out other readers.
- DTPR-BR-064: Write the generated interest transactions as one new, versioned batch output (a new file version or a batch-tagged table load) in the 350-byte transaction layout. Publish it only if the job succeeds and discard it on failure, so the combine step never picks up a partial batch.

## Open questions

- SME-012: Interest transaction IDs are made from the run date plus a sequence number. What type and length must the ID and the sequence part have, and what should happen if the sequence runs out of digits? (Data architecture team) On DTPR-BR-065.
- SME-013: If the interest run fails, the interest transactions are discarded but accounts already updated with interest are not rolled back. Should account updates and interest transactions be saved together as one unit, and how should a restart avoid charging interest twice? (Batch operations) On DTPR-BR-065.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (4 in all).