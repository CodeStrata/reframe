# Implementation plan: Change a transaction type description (TTRDM-C17)

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
| Description | text | Description, up to 50 characters; editable once a type is found or being added | Required; letters, digits and spaces only. Messages: 'Enter a description.' (legacy 'Transaction Desc must be supplied.'), 'Description can only contain letters, digits and spaces.' (legacy 'Transaction Desc can have numbers or alphabets only.') |  | TTRDM-REQ-F-117, TTRDM-REQ-F-118, TTRDM-REQ-F-119, TTRDM-REQ-F-120 |
| No changes | message | Information: 'No changes to save. The description matches the stored value.' | Description must differ from the stored value (ignoring case and surrounding spaces): 'No changes to save.' (legacy 'No change detected with respect to values fetched.') |  | TTRDM-REQ-F-122, TTRDM-REQ-F-129 |
| Save | button | Checks the description and opens the save confirmation; available only when something changed | Actions not available in the current step are disabled rather than rejected (legacy 'Invalid key pressed'). |  | TTRDM-REQ-F-121 |
| Save this transaction type? | dialog | Shows code and old/new description (or 'New type'); Save writes it, Cancel shows 'Update was cancelled' and keeps the edits |  |  | TTRDM-REQ-F-123, TTRDM-REQ-F-128 |
| Result | message | Success: 'Changes saved.' / 'Transaction type 07 added.' / 'Transaction type 07 deleted.', then ready for a new code. Blocked: 'This transaction type is still used by other records and cannot be deleted.' Busy: 'Someone else is changing this record. Try again.' Other: 'The change failed: <reason>. Try again.' |  |  | TTRDM-REQ-F-124, TTRDM-REQ-F-125, TTRDM-REQ-F-126, TTRDM-REQ-F-127 |


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

- TTRDM-BR-131: Description input needs normalising before validation and comparison. Remove leading and trailing spaces, and treat an empty value or a lone '*' as 'not supplied' (null). Validation then sees a missing description rather than a literal '*' or blanks.

## Decision tables

#### Description check

| Description blank (spaces or '*') | Description has characters other than letters, digits and spaces | Screen result | Rule |
|---|---|---|---|
| Yes | - | Show 'Transaction Desc must be supplied.'; stay in state 'E' | TTRDM-BR-132 |
| No | Yes | Show 'Transaction Desc can have numbers or alphabets only.'; stay in state 'E' | TTRDM-BR-133 |
| No | No | Move to state 'N'; show 'Changes validated.Press F5 to save' | TTRDM-BR-134 |

#### Outcome of saving a confirmed description change

| Database result of the update | Saved state and message | Rule |
|---|---|---|
| Success | Commit; state 'C'; 'Changes committed to database' | TTRDM-BR-138 |
| No row found (SQLCODE +100) | Insert as new row; commit; 'Changes committed to database' |  |
| Record lock (SQLCODE -911) | State 'L'; 'Changes unsuccessful'; 'Could not lock record for update' | TTRDM-BR-139 |
| Other negative SQLCODE | Error 'Error updating: TRANSACTION_TYPE Table. SQLCODE:…' yet state 'C' and 'Changes committed to database' | TTRDM-BR-140 |
| Other database failure | State 'F'; 'Changes unsuccessful' | TTRDM-BR-137 |
| Other negative SQLCODE | **Gap:** R16 says the outcome is set to committed ('C') with 'Changes committed to database', while R31 says any other database failure ends in state 'F' with 'Changes unsuccessful'; an expert must confirm which outcome is intended. | |

