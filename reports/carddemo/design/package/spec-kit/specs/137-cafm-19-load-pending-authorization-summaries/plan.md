# Implementation plan: Load pending authorization summaries (CAFM-C19)

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

None.

## Decision tables

#### Summary insert outcome

| Summary insert status | Load action | Rule |
|---|---|---|
| blank | Summary inserted; display 'ROOT INSERT SUCCESS' | CAFM-BR-181 |
| 'II' (summary already in database) | Display 'ROOT SEGMENT ALREADY IN DB'; leave existing summary unchanged; continue with next record | CAFM-BR-182 |
| any other status | Display 'ROOT INSERT FAILED :' with status and 'IMS LOAD ABENDING ...'; stop with return code 16 | CAFM-BR-183 |

