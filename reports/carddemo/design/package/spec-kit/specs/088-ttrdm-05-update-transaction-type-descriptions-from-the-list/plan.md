# Implementation plan: Update transaction type descriptions from the list (TTRDM-C05)

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
| No matching transaction types | message | Error under the filters: 'No transaction types match these filters. Change or clear the filters.'; on a database error: 'The transaction types could not be read. Try again.' | Supplied filters must match at least one type: 'No transaction types match these filters.' (legacy 'No Records found for these filter conditions') |  | TTRDM-REQ-F-050, TTRDM-REQ-F-051 |
| Edit description | button | Turns the description of this row into an input; one row is edited at a time, so other row actions are disabled meanwhile | One row action at a time, so the legacy errors 'Please select only 1 action' and 'Action code selected is invalid' cannot occur. |  | TTRDM-REQ-F-041, TTRDM-REQ-F-048, TTRDM-REQ-F-049 |
| Description | text | New description of the row being edited, up to 50 characters; the row is highlighted | Required; letters, digits and spaces only. Messages: 'Enter a description.' (legacy 'Transaction Desc must be supplied.'), 'Description can only contain letters, digits and spaces.' (legacy 'Transaction Desc can have numbers or alphabets only.'). If unchanged: 'No changes to save.' (legacy 'No change detected with respect to values fetched.') |  | TTRDM-REQ-F-042, TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046, TTRDM-REQ-F-047 |


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

- TTRDM-BR-048: The list form posts the two filters plus seven row entries, each with an action, a type code and a description. Bind them to a request model with a fixed list of 7 rows. Map a description of '*' or all spaces to 'not entered', and trim any other description.
- TTRDM-BR-049: Normalise row descriptions when reading the request: a blank value or a lone '*' becomes null (not entered), and any other value is trimmed at both ends. Validation and change detection work on the normalised value.

## Decision tables

#### Updated description check for a row marked 'U'

| Entered description vs stored (ignoring case and leading/trailing spaces) | Description entered (not blank or '*') | Only letters, digits and spaces | Validation result | Rule |
|---|---|---|---|---|
| Same | - | - | Show 'No change detected with respect to database values.'; skip remaining checks | TTRDM-BR-050 |
| Different | No | - | Reject; show 'Transaction Desc must be supplied.' unless an earlier message is set | TTRDM-BR-052 |
| Different | Yes | No | Reject; show 'Transaction Desc can have numbers or alphabets only.' unless an earlier message is set | TTRDM-BR-053 |
| Different | Yes | Yes | Treat row as changed; first 50 characters checked as required 'Transaction Desc' | TTRDM-BR-051 |
| Different | Yes | Yes | **Gap:** No rule states what happens next for a valid changed description (how the update is confirmed and saved), nor how a row marked 'D' is confirmed and deleted online. | |
| Different | Yes | Yes (over 50 characters) | **Gap:** Only the first 50 characters are checked; rules do not say what happens to text beyond 50 characters. | |

