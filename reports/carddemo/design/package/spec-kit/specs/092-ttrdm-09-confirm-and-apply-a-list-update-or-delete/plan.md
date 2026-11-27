# Implementation plan: Confirm and apply a list update or delete (TTRDM-C09)

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
| Transaction types | **data table** | Type code and description in code order, 20 rows a page. Row actions: Edit description in place (a labelled field; Enter opens a dialog showing old and new description), Open (full edit screen) and Delete (a dialog naming the code and description). Changing a filter cancels an edit in progress. Outcomes: 'Highlighted row was updated', 'Highlighted row deleted', 'Please delete associated child records first'. Empty state: 'No records found for this search condition. Use Add transaction type to create the first one.' | In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes. | S-TRANTYPE-EDIT | TTRDM-REQ-F-066, TTRDM-REQ-F-067, TTRDM-REQ-F-068, TTRDM-REQ-F-074, TTRDM-REQ-F-076 |


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

None.

## Decision tables

#### F10 confirmation handling

| Delete or update pending | Filters or selected row changed since prompt | Effect of F10 | Rule |
|---|---|---|---|
| No | Any | Treat F10 as Enter and show the list again | TTRDM-BR-074 |
| Yes | Yes | Treat F10 as Enter instead of carrying out the change | TTRDM-BR-075 |
| Yes | No | Delete the type if marked 'D', or save the new description if marked 'U' | TTRDM-BR-076 |

#### Outcome of the confirmed database change

| Confirmed action | Database result | Message and state after the change | Rule |
|---|---|---|---|
| Update ('U') | Success | Commit; show 'HIGHLIGHTED row was updated' (if no deletion confirmed in same request); redisplay page | TTRDM-BR-080 |
| Update ('U') | SQLCODE +100 | Show 'Record not found. Deleted by others ?'; update stays pending | TTRDM-BR-081 |
| Update ('U') | SQLCODE -911 | Show 'Deadlock. Someone else updating ?'; input error; update stays pending | TTRDM-BR-082 |
| Update ('U') | Any other negative code | Show 'Update failed with' and error details; update stays pending | TTRDM-BR-083 |
| Delete ('D') | Success | Commit; show 'HIGHLIGHTED row deleted.Hit Enter to continue'; restart from first page with filters cleared | TTRDM-BR-084 |
| Delete ('D') | SQLCODE -532 | Delete nothing; delete stays pending; show 'Please delete associated child records first:' and error details | TTRDM-BR-085 |
| Delete ('D') | Any other database reason | Show 'Delete failed with message:' and error details; delete not done | TTRDM-BR-086 |
| Delete ('D') | SQLCODE +100 | **Gap:** No rule says whether deleting a type code that no longer exists is treated as success or as 'any other database reason'. | |
| Update ('U') | Positive code other than +100 | **Gap:** No rule covers an update returning a positive warning code other than +100. | |

