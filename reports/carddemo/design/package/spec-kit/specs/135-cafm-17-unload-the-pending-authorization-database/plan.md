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

- CAFM-BR-162: Needs a scheduled full-database export of pending authorizations that reads the live data without locking out online users, writes a new variable-length extract (records up to 27990 bytes) under a fixed name, and removes the extract if the job fails so no partial file is left registered as complete.
- CAFM-BR-163: The export walks all account summaries in storage order and, for each with a numeric account id, writes the summary and then all its details, so every detail follows its parent summary in the output. In a relational model this is an ordered scan of summaries joined to their details.
- CAFM-BR-165: Reaching the end of the summaries is the normal finish of the export, not an error; the job completes successfully.
- CAFM-BR-166: For each exported summary, every detail belonging to that account is read in turn and each successfully read detail is written to the detail export file.
- CAFM-BR-167: Running out of details for a summary is normal: log 'CHILD SEG FLAG GE : Y', reset the per-summary state and move on to the next summary. It must not be treated as an error or stop the job.

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

