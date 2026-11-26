# Implementation plan: Load pending authorizations into the database (CAFM-C18)

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

- CIPAUDTY (working storage of PAUDBLOD): see data-contracts.md.
- CIPAUSMY (working storage of PAUDBLOD): see data-contracts.md.
- IMSFUNCS (working storage of PAUDBLOD): see data-contracts.md.
- PAUTBPCB (working storage of PAUDBLOD): see data-contracts.md.

## Design notes

- CAFM-BR-172: A batch load job that takes two input files, a summary file and a detail file, and inserts their records into the pending authorization store while online use continues (it must not need exclusive access to the store).
- CAFM-BR-173: The load runs in two phases: read the whole summary file and insert every summary, and only then read the detail file. This order guarantees each detail's parent summary already exists when the detail is inserted.
- CAFM-BR-174: Each detail is attached to its summary by account id: look up the summary by account id (a keyed lookup) and insert the detail under it, for example as a child row with a foreign key to the summary. A detail whose summary cannot be found is skipped, not loaded as an orphan.

## Decision tables

#### Loading a pending authorization detail record

| Account ID numeric | Summary found | Detail insert status | What the load does | Rule |
|---|---|---|---|---|
| No | not looked up | not attempted | Skip the record silently; read next detail | CAFM-BR-175 |
| Yes | No | not attempted | Skip the detail; no error message; run continues | CAFM-BR-177 |
| Yes | Yes | blank | Insert detail; display 'CHILD SEGMENT INSERTED SUCCESS' | CAFM-BR-178 |
| Yes | Yes | 'II' | Display 'CHILD SEGMENT ALREADY IN DB'; existing detail unchanged; continue | CAFM-BR-178 |
| Yes | Yes | any other status | Display 'INSERT CALL FAIL FOR CHILD:' and 'IMS LOAD ABENDING ...'; return code 16 | CAFM-BR-179 |

