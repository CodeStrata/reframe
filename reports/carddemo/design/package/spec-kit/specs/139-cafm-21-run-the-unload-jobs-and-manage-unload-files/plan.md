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

- CAFM-BR-194: A scheduled batch job (legacy DBUNLDGS) that reads the whole pending authorization store, summaries with their details, with read-only shared access so online users are not locked out.
- CAFM-BR-195: This job writes to two standing output files, root (summary) and child (detail), that already exist. Only this job may write to them while it runs, and both are kept whether the job succeeds or fails, so downstream users must check the job's outcome before trusting their contents.
- CAFM-BR-196: A second scheduled batch job (legacy PAUDBUNL) that reads the pending authorization store with shared read-only access and writes summaries to the first output file and details to the second.
- CAFM-BR-197: The root unload file, of fixed 100-byte records, is created new on each run and published only when the job succeeds; on failure it is deleted (write under a temporary name and rename on success).
- CAFM-BR-198: The child unload file, of fixed 206-byte records, is created new on each run and published only when the job succeeds; on failure it is deleted, the same as the root file.

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

