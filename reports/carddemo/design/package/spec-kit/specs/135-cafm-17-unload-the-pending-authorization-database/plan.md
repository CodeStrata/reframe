# Implementation plan: Unload the pending authorization database (CAFM-C17)

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

- CIPAUDTY (working storage of DBUNLDGS): see data-contracts.md.
- CIPAUSMY (working storage of DBUNLDGS): see data-contracts.md.
- IMSFUNCS (working storage of DBUNLDGS): see data-contracts.md.
- PADFLPCB (working storage of DBUNLDGS): see data-contracts.md.
- PASFLPCB (working storage of DBUNLDGS): see data-contracts.md.
- PAUTBPCB (working storage of DBUNLDGS): see data-contracts.md.

## Design notes

- CAFM-BR-162: A scheduled full extract of the pending authorization store into a single new file of variable-length records (up to 27990 bytes), read without locking out online users. The file must only be published when the job succeeds: write to a temporary name and rename on success, or delete it on failure, so a failed run never leaves a usable-looking extract.
- CAFM-BR-163: The extract walks all summaries in a stable order (by account id) and, for each one with a numeric account id, writes the summary and then all its details before moving to the next summary. With a relational store this is a query of summaries ordered by account id joined to their details, streamed out so memory use does not grow with volume.
- CAFM-BR-165: The job ends normally when there are no more summaries to read; reaching the end of the data is a normal finish, not an error.
- CAFM-BR-166: For each summary, every one of its details is written to the separate detail file, in the order they are held under that summary (newest first in the legacy store), so a reload can attach each detail to its summary.
- CAFM-BR-167: Running out of details for a summary is a normal step, not an error: log 'CHILD SEG FLAG GE : Y', reset the per-summary state and continue with the next summary.

## Decision tables

#### Unloading a pending authorization summary

| Summary read status | Account id numeric | Summary write status | What the unload does | Rule |
|---|---|---|---|---|
| blank | Yes | blank | Summary written; unload its details | CAFM-BR-163 |
| blank | No | not written | Skip the summary and its details | CAFM-BR-164 |
| 'GB' | n/a | not written | Stop reading and finish the run | CAFM-BR-165 |
| any other status | n/a | not written | Print 'AUTH SUM GN FAILED :' and 'DBUNLDGS ABENDING ...'; return code 16; end | CAFM-BR-168 |
| blank | Yes | non-blank | Print 'GSAM PARENT FAIL :'; return code 16; end | CAFM-BR-170 |

#### Unloading the details of a summary

| Detail read status | Detail write status | What the unload does | Rule |
|---|---|---|---|
| blank | blank | Detail written; read next detail | CAFM-BR-166 |
| 'GE' | not written | Print 'CHILD SEG FLAG GE : Y'; stop reading details; clear status for next summary | CAFM-BR-167 |
| any other status | not written | Print 'GNP CALL FAILED :'; return code 16; end | CAFM-BR-169 |
| blank | non-blank | Print 'GSAM PARENT FAIL :'; return code 16; end | CAFM-BR-171 |

