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

Browse and filter transaction types, correct a description in place, or delete an obsolete type, each confirmed in a dialog that repeats what will change; also where a type is found by code to change or delete it. Row actions replace U/D codes and F10; the pager replaces F7/F8.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Add or change a transaction type (S-TRANTYPE-EDIT)

Add a new transaction type or change an existing one's description in one step: enter the code, see its description or start a new one if it is not on file, then save. Replaces the F5 create, Enter check and F5 confirm sequence; delete is the Delete row action on the list.

Prototype: `ui-reference/index.html#/S-TRANTYPE-EDIT`. Replaces the legacy screens CTRTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction type code | **lookup field** | Two-digit code, stored with a leading zero (1 becomes 01). Search shows the existing description, or 'No record found for this key in database. Enter a description to add it.' and the form switches to adding. Read-only when opened from a list row. | 'Tran Type code must be supplied. Enter a two-digit code.'; 'Tran Type code must be numeric. Enter digits only.'; 'Tran Type code must not be zero. Enter a code from 01 to 99.' Only the first failing check is shown. |  | TTRDM-REQ-F-080, TTRDM-REQ-F-081, TTRDM-REQ-F-082, TTRDM-REQ-F-088 |


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

- TTRDM-BR-095: Each lookup starts by clearing the 'original' snapshot and the information message held in the screen's state, so a failed lookup can never leave the previous type's values behind.
- TTRDM-BR-096: A keyed read of the transaction type table by its two-digit code. On a hit, return a 'found' result with code and description; the description is used both for display and as the baseline for change detection.
- TTRDM-BR-097: Hold the fetched code and description, at their stored length, as an 'original' snapshot in the edit session (or as a version/ETag) to compare against the user's later edits. On not-found or a read error, leave the snapshot empty.
- TTRDM-BR-100: In the not-found state, if the same code is submitted again without choosing Add, keep the code and description already held in the edit session and ignore the submitted form values, including any description typed.

## Decision tables

#### Search key checks (state neither 'R' nor 'N')

| Transaction type code | Record already fetched | Result of search key editing | Rule |
|---|---|---|---|
| Blank | Any | Show 'Tran Type code must be supplied.', mark code '*' in red, ask for a code | TTRDM-BR-089 |
| Not numeric | Any | Show 'Tran Type code must be numeric.', highlight code in red, ask for a code | TTRDM-BR-090 |
| Zero | Any | Show 'Tran Type code must not be zero.', highlight code in red, ask for a code | TTRDM-BR-091 |
| Valid non-zero number | No | Store code as two digits with leading zero and search the table | TTRDM-BR-094 |
| Valid non-zero number | Yes | **Gap:** These rules do not say how the code is handled once a record has been fetched; change detection rules (R54, R58) may apply but do not state the code checks. | |

