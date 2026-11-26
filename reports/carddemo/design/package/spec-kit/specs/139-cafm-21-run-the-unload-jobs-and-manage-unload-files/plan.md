# Implementation plan: Run the unload jobs and manage unload files (CAFM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as scheduled job.

## Data model

- CIPAUDTY (working storage of PAUDBUNL): see data-contracts.md.
- CIPAUSMY (working storage of PAUDBUNL): see data-contracts.md.
- IMSFUNCS (working storage of PAUDBUNL): see data-contracts.md.
- PAUTBPCB (working storage of PAUDBUNL): see data-contracts.md.

## Design notes

- CAFM-BR-194: Needs a scheduled batch job running the summary-and-detail unload (DBUNLDGS in the legacy) with read-only, shared access to the pending authorization data and its index, so online use is not blocked while it runs.
- CAFM-BR-195: This job writes to two existing output files, the summary file (AWS.M2.CARDDEMO.PAUTDB.ROOT.GSAM) and the detail file (AWS.M2.CARDDEMO.PAUTDB.CHILD.GSAM). No other process may write to them during the run, and they are kept whether the job succeeds or fails, so downstream steps must check the job status before using them.
- CAFM-BR-196: Needs a second scheduled export job (PAUDBUNL in the legacy) that reads the pending authorization data and its index with shared, read-only access and writes summaries to the first output file and details to the second.
- CAFM-BR-197: The job creates a new summary export file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) of fixed 100-byte records. It is published or registered only when the job succeeds and is deleted when the job fails, for example by writing to a temporary location and renaming it on success.
- CAFM-BR-198: The job creates a new detail export file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO) of fixed 206-byte records. It is published only when the job succeeds and deleted when the job fails, the same way as the summary file.

## Decision tables

#### Unload file disposition by step outcome

| Unload job | Output file | Step outcome | File disposition | Rule |
|---|---|---|---|---|
| UNLDGSAM | root-segment and child-segment GSAM files | ends normally | Keep both files | CAFM-BR-195 |
| UNLDGSAM | root-segment and child-segment GSAM files | fails | Keep both files | CAFM-BR-195 |
| UNLDPADB | root unload file (ROOT.FILEO) | ends normally | Catalog the file | CAFM-BR-197 |
| UNLDPADB | root unload file (ROOT.FILEO) | fails | Delete the file | CAFM-BR-197 |
| UNLDPADB | child unload file (CHILD.FILEO) | ends normally | Catalog the file | CAFM-BR-198 |
| UNLDPADB | child unload file (CHILD.FILEO) | fails | Delete the file | CAFM-BR-198 |

