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

- CAFM-BR-172: Needs a scheduled load job that takes two input files, the summary file (AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO) and the detail file (AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO), and inserts their contents into the live pending authorization store while it stays available to other users.
- CAFM-BR-173: The load runs in two passes: the whole summary file to its end, then the whole detail file to its end. Details are never processed before all summaries are in, so each detail can find its parent.
- CAFM-BR-174: Same two-pass order: details are attached to their summary by account ID only after every summary has been loaded. In a relational model this is the parent table loaded before the child table, with the account ID as the foreign key.

## Decision tables

#### Loading a pending authorization detail record

| Account ID numeric | Summary found | Detail insert status | What the load does | Rule |
|---|---|---|---|---|
| No | not looked up | not attempted | Skip the record silently; read next detail | CAFM-BR-175 |
| Yes | No | not attempted | Skip the detail; no error message; run continues | CAFM-BR-177 |
| Yes | Yes | blank | Insert detail; display 'CHILD SEGMENT INSERTED SUCCESS' | CAFM-BR-178 |
| Yes | Yes | 'II' | Display 'CHILD SEGMENT ALREADY IN DB'; existing detail unchanged; continue | CAFM-BR-178 |
| Yes | Yes | any other status | Display 'INSERT CALL FAIL FOR CHILD:' and 'IMS LOAD ABENDING ...'; return code 16 | CAFM-BR-179 |

