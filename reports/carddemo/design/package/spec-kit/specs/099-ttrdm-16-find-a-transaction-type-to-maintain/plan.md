# Implementation plan: Find a transaction type to maintain (TTRDM-C16)

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

### Add or change a transaction type (S-TRANTYPE-EDIT)

Add a new transaction type or change an existing one's description in one step: enter the code, see its description or start a new one if it is not on file, then save. Replaces the F5 create, Enter check and F5 confirm sequence; delete is the Delete row action on the list.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction type code | **lookup field** | Two-digit code, stored with a leading zero (1 becomes 01). Search shows the existing description, or 'No record found for this key in database. Enter a description to add it.' and the form switches to adding. Read-only when opened from a list row. | 'Tran Type code must be supplied. Enter a two-digit code.'; 'Tran Type code must be numeric. Enter digits only.'; 'Tran Type code must not be zero. Enter a code from 01 to 99.' Only the first failing check is shown. |  | TTRDM-REQ-F-110, TTRDM-REQ-F-111, TTRDM-REQ-F-112, TTRDM-REQ-F-113, TTRDM-REQ-F-115 |


## Data model

#### CSMSG02Y

File record of COTRTUPC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

- COCOM01Y (working storage of COTRTUPC): see data-contracts.md.
- COTTL01Y (working storage of COTRTUPC): see data-contracts.md.
- CSDAT01Y (working storage of COTRTUPC): see data-contracts.md.
- CSMSG01Y (working storage of COTRTUPC): see data-contracts.md.
- CSSETATY (working storage of COTRTUPC): see data-contracts.md.
- CSSTRPFY (working storage of COTRTUPC): see data-contracts.md.
- CSUSR01Y (working storage of COTRTUPC): see data-contracts.md.
- CSUTLDWY (working storage of COTRTUPC): see data-contracts.md.
- CVCRD01Y (working storage of COTRTUPC): see data-contracts.md.

## Design notes

- TTRDM-BR-122: The search request needs server-side validation of the type code (supplied, numeric, non-zero) that runs before any database lookup. It applies only when the screen is in search mode, meaning not while adding a new record and not while awaiting confirmation. The validator stops at the first failure. Only a valid code, normalised to two digits, is used as the key for the single-row lookup by primary key.

## Decision tables

#### Transaction type search code check

| Code supplied (not blank or '*') | Code is a number | Code equals zero | Search result | Rule |
|---|---|---|---|---|
| No | - | - | Show 'Tran Type code must be supplied.'; no lookup | TTRDM-BR-123 |
| Yes | No | - | Show 'Tran Type code must be numeric.'; search code invalid; no lookup | TTRDM-BR-124 |
| Yes | Yes | Yes | Show 'Tran Type code must not be zero.'; search code invalid; no lookup | TTRDM-BR-125 |
| Yes | Yes | No | Accept; pad to two digits with leading zero; use as lookup key | TTRDM-BR-126 |

