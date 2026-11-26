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

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Transaction type (S-TRANTYPE-EDIT)

Look up a transaction type by code to change its description or delete it, or add a new type when the code is not on file; each save or delete is confirmed and can be cancelled.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Find a transaction type | form | Type code; empty on a fresh start. From Add transaction type, an unknown code goes straight to adding. |  |  | TTRDM-REQ-F-108, TTRDM-REQ-F-109, TTRDM-REQ-F-115 |
| Type code | text | 2-digit transaction type code, shown with a leading zero (e.g. 07) | Required; a number other than zero. Messages: 'Enter a type code.' (legacy 'Tran Type code must be supplied.'), 'Type code must be a number.' (legacy 'Tran Type code must be numeric.'), 'Type code must not be 00.' (legacy 'Tran Type code must not be zero.'). Only the first problem is shown. |  | TTRDM-REQ-F-110, TTRDM-REQ-F-111, TTRDM-REQ-F-112, TTRDM-REQ-F-113, TTRDM-REQ-F-114 |
| Find | button | Looks the code up; not available while a delete is being confirmed |  |  | TTRDM-REQ-F-116 |

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Maintain a transaction type | link |  |  | S-TRANTYPE-EDIT | TTRDM-REQ-F-108 |


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

- TTRDM-BR-122: Code validation needs to run before the lookup, as a step in the search action. It applies only when the screen is neither adding a new record nor waiting for confirmation of changes. In those two modes, an Enter press must not re-validate the search code or look it up again.

## Decision tables

#### Transaction type search code check

| Code supplied (not blank or '*') | Code is a number | Code equals zero | Search result | Rule |
|---|---|---|---|---|
| No | - | - | Show 'Tran Type code must be supplied.'; no lookup | TTRDM-BR-123 |
| Yes | No | - | Show 'Tran Type code must be numeric.'; search code invalid; no lookup | TTRDM-BR-124 |
| Yes | Yes | Yes | Show 'Tran Type code must not be zero.'; search code invalid; no lookup | TTRDM-BR-125 |
| Yes | Yes | No | Accept; pad to two digits with leading zero; use as lookup key | TTRDM-BR-126 |

