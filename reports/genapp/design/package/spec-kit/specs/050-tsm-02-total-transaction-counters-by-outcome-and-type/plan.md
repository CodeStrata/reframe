# Implementation plan: Total transaction counters by outcome and type (TSM-C02)

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

None found in the source.

## Design notes

None.

## Decision tables

#### Counter inclusion by counter ending

| Counter in pool 'GENA' | Total the counter is added to | Rule |
|---|---|---|
| Ending '00' (17 success counters) | Added to the successful-transaction total | TSM-BR-003 |
| Ending '99' (17 error counters, 'GENA01ICUS99' to 'GENA01DCOM99') | Added to the error total | TSM-BR-004 |
| 'GENAOTHER' | Not included in the error total | TSM-BR-004 |
| 'GENAOTHER' | Left out of the successful-transaction total | TSM-BR-003 |

#### Transaction type totals by action and business area

| Action | Business area | Counter included in the type total | Rule |
|---|---|---|---|
| Inquiry | Customer, Motor, Endowment, House, Commercial | Inquiry total includes 'GENA01ICUS00', 'GENA01IMOT00', 'GENA01IEND00', 'GENA01IHOU00', 'GENA01ICOM00' | TSM-BR-005 |
| Add | Customer, Motor, Endowment, House, Commercial | Add total includes 'GENA01ACUS00', 'GENA01AMOT00', 'GENA01AEND00', 'GENA01AHOU00', 'GENA01ACOM00' | TSM-BR-006 |
| Update | Motor, Endowment, House | Update total includes 'GENA01UMOT00', 'GENA01UEND00', 'GENA01UHOU00' | TSM-BR-007 |
| Update | Customer, Commercial | No update counter included | TSM-BR-007 |
| Delete | Motor, Endowment, House, Commercial | Delete total includes 'GENA01DMOT00', 'GENA01DEND00', 'GENA01DHOU00', 'GENA01DCOM00' | TSM-BR-008 |
| Delete | Customer | No delete counter included | TSM-BR-008 |

