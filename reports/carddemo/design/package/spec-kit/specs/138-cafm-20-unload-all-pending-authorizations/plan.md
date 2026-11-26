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

- CAFM-BR-185: The export reads summaries one after another in storage order until there are none left, and finishes each summary (including its details) before moving to the next. A streaming or paged ordered scan is fine; loading everything into memory is not required.
- CAFM-BR-187: Each summary goes to the summary export file as its full 100-byte record image, unchanged, so the file can be reloaded as it is. If the new store changes the summary layout, an explicit fixed 100-byte export format must be defined to keep compatibility.
- CAFM-BR-189: End of summaries is the normal finish: close both export files and end the job successfully.
- CAFM-BR-191: Each detail goes to the detail export file as a 206-byte record: the parent account id (6-byte packed decimal) followed by the 200-byte detail image. The account prefix is what links each detail back to its summary on reload, so it must always be present.
- CAFM-BR-192: Running out of details for the current summary is normal: log 'CHILD SEG FLAG GE : ' with the end flag and continue with the next summary, without treating it as an error.

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

