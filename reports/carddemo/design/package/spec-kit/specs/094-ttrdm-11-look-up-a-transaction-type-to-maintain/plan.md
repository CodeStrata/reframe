# Implementation plan: Look up a transaction type to maintain (TTRDM-C11)

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
| Find a transaction type | form | Type code; empty on a fresh start. From Add transaction type, an unknown code goes straight to adding. |  |  | TTRDM-REQ-F-085 |
| Type code | text | 2-digit transaction type code, shown with a leading zero (e.g. 07) | Required; a number other than zero. Messages: 'Enter a type code.' (legacy 'Tran Type code must be supplied.'), 'Type code must be a number.' (legacy 'Tran Type code must be numeric.'), 'Type code must not be 00.' (legacy 'Tran Type code must not be zero.'). Only the first problem is shown. |  | TTRDM-REQ-F-080, TTRDM-REQ-F-081, TTRDM-REQ-F-082, TTRDM-REQ-F-083, TTRDM-REQ-F-084 |
| Find | button | Looks the code up; not available while a delete is being confirmed |  |  | TTRDM-REQ-F-089 |
| Type not on file | message | Information: 'Type 07 is not on file. Add it as a new transaction type?' next to the Add as new type button | Code must exist to change or delete: 'No transaction type with this code.' (legacy 'No record found for this key in database') |  | TTRDM-REQ-F-086, TTRDM-REQ-F-087, TTRDM-REQ-F-088 |
| Add as new type | button | Starts a new transaction type with the code entered; focus moves to Description |  |  | TTRDM-REQ-F-090 |


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

- TTRDM-BR-095: Before each lookup by type code, clear the saved 'original' transaction type and the info message in the screen's session state, so that a failed lookup cannot leave the previous type's values behind.
- TTRDM-BR-096: Look up the transaction type by its primary key (the two-digit type code). On a hit, set a 'found' flag and keep the code and description as the values on file, used for display and change detection.
- TTRDM-BR-097: On a successful lookup, save the stored code and description, at its full stored length, as the 'original' snapshot in session state; later edits are compared against it. When the lookup finds nothing or fails, save no snapshot.
- TTRDM-BR-100: In the not-found state, if the same code is submitted again without F5, keep the code and description already in session state and ignore the posted form values, including any typed description, before the code is looked up again.

## Decision tables

#### Search key checks (state neither 'R' nor 'N')

| Transaction type code | Record already fetched | Result of search key editing | Rule |
|---|---|---|---|
| Blank | Any | Show 'Tran Type code must be supplied.', mark code '*' in red, ask for a code | TTRDM-BR-089 |
| Not numeric | Any | Show 'Tran Type code must be numeric.', highlight code in red, ask for a code | TTRDM-BR-090 |
| Zero | Any | Show 'Tran Type code must not be zero.', highlight code in red, ask for a code | TTRDM-BR-091 |
| Valid non-zero number | No | Store code as two digits with leading zero and search the table | TTRDM-BR-094 |
| Valid non-zero number | Yes | **Gap:** These rules do not say how the code is handled once a record has been fetched; change detection rules (R54, R58) may apply but do not state the code checks. | |

