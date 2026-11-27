# Implementation plan: Unload all pending authorizations (CAFM-C20)

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

- CAFM-BR-185: The job walks all summaries one by one in a stable order (by account id), finishing each summary and its details before moving to the next; stream the results rather than loading them all into memory.
- CAFM-BR-187: The summary file holds one fixed 100-byte record per summary, the summary exactly as stored. The new application needs a defined summary export layout of the same fields, byte-compatible with the legacy layout for as long as anything still reads these files.
- CAFM-BR-189: When there are no more summaries, the job closes both output files and ends normally (return code 0); reaching the end of the data is not an error.
- CAFM-BR-191: The detail file holds one fixed 206-byte record per detail: the parent account id (6 bytes, packed decimal in the legacy layout) followed by the 200-byte detail as stored. The account id prefix is what lets a reload attach each detail to its summary, so the new export must always carry it; keep packed decimal only while legacy consumers need it.
- CAFM-BR-192: Running out of details for a summary is a normal step: log 'CHILD SEG FLAG GE : ' with the end flag and continue with the next summary.

## Decision tables

#### Summary read outcome

| Summary read status | Account id numeric | Unload action | Rule |
|---|---|---|---|
| blank | yes | Write summary unchanged to summary unload file; unload every detail under it | CAFM-BR-186 |
| blank | no | Write neither summary nor details; no message; go on to next summary | CAFM-BR-188 |
| 'GB' (end of database) | n/a | Stop reading summaries; close both unload files; end normally | CAFM-BR-189 |
| any other status | n/a | Display 'AUTH SUM GN FAILED :' with status and key feedback and 'IMSUNLOD ABENDING ...'; end with return code 16 without closing files | CAFM-BR-190 |

#### Detail read outcome

| Detail read status | Unload action | Rule |
|---|---|---|
| blank | Write 206-byte record (parent account id + 200-byte detail image) to detail unload file | CAFM-BR-191 |
| 'GE' (no more details) | Stop reading details for this summary; display 'CHILD SEG FLAG GE : '; go on to next summary | CAFM-BR-192 |
| any other status | Display 'GNP CALL FAILED :' and 'KFB AREA IN CHILD:' and 'IMSUNLOD ABENDING ...'; end with return code 16 without closing files | CAFM-BR-193 |

