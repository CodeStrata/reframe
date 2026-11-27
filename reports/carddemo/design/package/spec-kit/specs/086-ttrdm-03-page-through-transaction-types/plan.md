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

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction types | **data table** | Type code and description in code order, 20 rows a page. Row actions: Edit description in place (a labelled field; Enter opens a dialog showing old and new description), Open (full edit screen) and Delete (a dialog naming the code and description). Changing a filter cancels an edit in progress. Outcomes: 'Highlighted row was updated', 'Highlighted row deleted', 'Please delete associated child records first'. Empty state: 'No records found for this search condition. Use Add transaction type to create the first one.' | In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes. | S-TRANTYPE-EDIT | TTRDM-REQ-F-017 |


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

- TTRDM-BR-024: Page queries read in type-code order from the page's start code with a limit (fetching one extra row, e.g. 8, is a simple way to know whether a next page exists). If fewer rows come back than the page holds, stop and record that there is no next page.

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

