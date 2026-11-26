# Implementation plan: Page through transaction types (TTRDM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

### Transaction types (S-TRANTYPE-LIST)

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Apply filters | button |  |  |  | TTRDM-REQ-F-028 |
| Transaction types | table | Columns: type code, description. Pages in ascending type-code order with Previous and Next page controls and the page number; Previous is disabled on page 1, Next on the last page. |  |  | TTRDM-REQ-F-017, TTRDM-REQ-F-018, TTRDM-REQ-F-019, TTRDM-REQ-F-020, TTRDM-REQ-F-021, TTRDM-REQ-F-022, TTRDM-REQ-F-023, TTRDM-REQ-F-024, TTRDM-REQ-F-025, TTRDM-REQ-F-026, TTRDM-REQ-F-027, TTRDM-REQ-F-029, TTRDM-REQ-F-030, TTRDM-REQ-F-031 |


## Data model

- COCOM01Y (working storage of COTRTLIC): see data-contracts.md.
- COTTL01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDAT01Y (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RPY (working storage of COTRTLIC): see data-contracts.md.
- CSDB2RWY (working storage of COTRTLIC): see data-contracts.md.
- CSMSG01Y (working storage of COTRTLIC): see data-contracts.md.
- CSSTRPFY (working storage of COTRTLIC): see data-contracts.md.
- CSUSR01Y (working storage of COTRTLIC): see data-contracts.md.
- CVACT02Y (working storage of COTRTLIC): see data-contracts.md.
- CVCRD01Y (working storage of COTRTLIC): see data-contracts.md.

## Design notes

- TTRDM-BR-024: Read the page as a keyset query ordered by type code, from the page's start code, with the active filters, taking up to 8 rows (7 to show plus 1 to look ahead). When fewer than 8 come back, stop and record that there is no next page. Do not treat running out of rows as an error.

## Decision tables

#### Paging key outcome

| Key pressed | On first page | Next page exists | Last page already shown | Page and message shown | Rule |
|---|---|---|---|---|---|
| F8 | - | Yes | - | Show page from stored next type code; page number + 1; clear row selections | TTRDM-BR-026 |
| F8 | - | No (types run out while reading) | - | Record no next page; show 'No more pages for these search conditions' if no other message pending | TTRDM-BR-025 |
| F8 | - | No | No | Show 'Type U to update, D to delete any record'; remember last page shown | TTRDM-BR-028 |
| F8 | - | No | Yes | Show same page again with 'No more pages to display' | TTRDM-BR-029 |
| F7 | No | - | - | Show the 7 types before current first code; page number - 1; clear selections; mark next page exists | TTRDM-BR-030 |
| F7 | Yes | - | - | Show first page again with 'No previous pages to display' (if no input errors) | TTRDM-BR-031 |
| F8 | - | No | No | **Gap:** R16 and R22/R46 both apply when F8 reaches the end for the first time: rules do not settle whether 'Type U to update, D to delete any record' or 'No more pages for these search conditions' is shown. | |
| F7 | Yes | - | - | **Gap:** R49 applies only with no input errors; no rule states the page shown on F7 from the first page when an input error exists beyond R30/R31's general redisplay. | |

