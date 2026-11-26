# Update transaction type descriptions from the list (TTRDM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk medium

## Introduction

Lets administrators change a transaction type's description directly on a list row marked 'U', with checks before anything is saved. A changed description must be supplied and may hold only letters, digits and spaces. An unchanged one is reported as 'No change detected with respect to database values.'. The screen must never save, or appear to accept, a description that failed these checks.

**User story:** As an administrator, I want to mark a listed transaction type for update or delete and change its description on the list screen, so that I can correct reference data online with clear validation feedback.

## Requirements

### Requirement 1: TTRDM-REQ-F-041 (design note)

#### Acceptance criteria

1. When the operator submits the transaction type list screen, the system shall capture the type code and description filters and, for each of the 7 rows, the action code, the type code and the description. (rules TTRDM-BR-048)
2. GIVEN row 3 description: * WHEN the operator submits the transaction type list screen THEN Row 3 description is treated as not entered (TTRDM-C05-AC-01; TTRDM-BR-048)

### Requirement 2: TTRDM-REQ-F-042 (design note)

#### Acceptance criteria

1. When a row's description field holds only '*' or is blank, the system shall treat the description as not entered, and otherwise shall use the entered text with leading and trailing spaces removed. (rules TTRDM-BR-048, TTRDM-BR-049)
2. GIVEN row 3 description: * WHEN the operator submits the transaction type list screen THEN Row 3 description is treated as not entered (TTRDM-C05-AC-01; TTRDM-BR-048)
3. GIVEN Entered description: * WHEN a row's description field holds only '*' or is blank THEN The description counts as not entered (TTRDM-C05-AC-02; TTRDM-BR-049)

### Requirement 3: TTRDM-REQ-F-043 (business rule)

#### Acceptance criteria

1. When a transaction type row marked 'U' is submitted and the entered description matches the stored description, ignoring upper/lower case and leading or trailing spaces, the system shall show 'No change detected with respect to database values.' and skip the remaining description checks for that row. (rules TTRDM-BR-050)
2. GIVEN Stored description: Payment; Action: U; Entered description: payment WHEN a transaction type row marked 'U' is submitted and the entered description matches the stored description, ignoring upper/lower case and leading or trailing spaces THEN Message 'No change detected with respect to database values.' (TTRDM-C05-AC-03; TTRDM-BR-050)
3. GIVEN Stored description: Payment; Action: U; Entered description: PAYMENT WHEN a transaction type row marked 'U' is submitted and the entered description matches the stored description, ignoring upper/lower case and leading or trailing spaces THEN Message 'No change detected with respect to database values.' (TTRDM-C05-AC-04; TTRDM-BR-050)

### Requirement 4: TTRDM-REQ-F-044 (business rule)

#### Acceptance criteria

1. When the entered description of a row marked 'U' differs from the stored description, the system shall treat the row as changed and check the first 50 characters of the description as a required letters-and-digits field named 'Transaction Desc'. (rules TTRDM-BR-051)
2. GIVEN Stored description: Payment; Action: U; Entered description: Bill Payment WHEN the entered description of a row marked 'U' differs from the stored description THEN The row counts as changed and the description passes the checks (TTRDM-C05-AC-05; TTRDM-BR-051)

### Requirement 5: TTRDM-REQ-F-045 (business rule)

#### Acceptance criteria

1. If a changed description is not entered (blank or '*'), then the system shall reject the input and show 'Transaction Desc must be supplied.', unless an earlier message has already been set. (rules TTRDM-BR-052)
2. GIVEN row 3 shows type '02' with stored description 'Payment', and no other message has been set WHEN the administrator marks row 3 'U', clears its description to blank (or types '*') and presses Enter THEN the input is rejected, the message 'Transaction Desc must be supplied.' is shown and nothing is saved (TTRDM-C05-AC-12; TTRDM-BR-052)

### Requirement 6: TTRDM-REQ-F-046 (business rule)

#### Acceptance criteria

1. If a changed description contains any character other than a letter, a digit or a space, then the system shall reject the input and show 'Transaction Desc can have numbers or alphabets only.', unless an earlier message has already been set. (rules TTRDM-BR-053)
2. GIVEN Action: U; Entered description: Cash Advance 2 WHEN a changed description contains any character other than a letter, a digit or a space THEN Description accepted (TTRDM-C05-AC-06; TTRDM-BR-053)

### Requirement 7: TTRDM-REQ-F-047 (formatting)

#### Acceptance criteria

1. If a description entered for update fails its checks, then the system shall show that description in red with the cursor on it, and shall show a description that was not entered as '*'. (rules TTRDM-BR-054)
2. GIVEN Action: U; Entered description: WHEN a description entered for update fails its checks THEN The description field shows '*' in red (TTRDM-C05-AC-07; TTRDM-BR-054)

### Requirement 8: TTRDM-REQ-F-048 (formatting)

#### Acceptance criteria

1. When a row is marked 'U' as the only valid action on the screen and the operator has typed a description that differs from the stored one and is not blank, the system shall show the operator's typed description on that row instead of the stored description. (rules TTRDM-BR-055)
2. GIVEN row 2 shows type '01' with stored description 'Purchase', and no other row has an action WHEN the administrator marks row 2 'U', types 'Retail Purchase' as its description and presses Enter THEN row 2 shows 'Retail Purchase' rather than 'Purchase' when the page is shown again (TTRDM-C05-AC-13; TTRDM-BR-055)

### Requirement 9: TTRDM-REQ-F-049 (formatting)

#### Acceptance criteria

1. When a row is not the single valid 'U' action on the screen, or it is but the typed description does not differ from the stored one, the system shall show the stored transaction type description on that row. (rules TTRDM-BR-056)
2. GIVEN row action: D WHEN a row is not the single valid 'U' action on the screen, or it is but the typed description does not differ from the stored one THEN Row shows the stored description (TTRDM-C05-AC-08; TTRDM-BR-056)

### Requirement 10: TTRDM-REQ-F-050 (business rule)

#### Acceptance criteria

1. If the submitted screen has an input error, then the system shall show the error message and stay on the list screen rather than act on any key pressed. (rules TTRDM-BR-057)
2. GIVEN Type code filter: A1 WHEN the submitted screen has an input error THEN The list screen is shown again with 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER' (TTRDM-C05-AC-09; TTRDM-BR-057)

### Requirement 11: TTRDM-REQ-F-051 (formatting)

#### Acceptance criteria

1. If the submitted screen has an input error but both the type code filter and the description filter are acceptable, then the system shall re-read the current page starting from its first type code before showing the error. (rules TTRDM-BR-058)
2. GIVEN Type code filter: blank; Row error: invalid row action; First type code on page: 05 WHEN the submitted screen has an input error but both the type code filter and the description filter are acceptable THEN The page is re-read from type 05 and shown with the error message (TTRDM-C05-AC-10; TTRDM-BR-058)
3. GIVEN Type code filter: X9 WHEN the submitted screen has an input error but both the type code filter and the description filter are acceptable THEN The list is not re-read; the screen is redisplayed with the filter error (TTRDM-C05-AC-11; TTRDM-BR-058)

## Screens and components

### Transaction types (S-TRANTYPE-LIST)

Find transaction types by code or description, correct a description in place, or delete an obsolete type, confirming each change; start adding a new type.

Prototype: `ui-reference/index.html#/S-TRANTYPE-LIST`. Replaces the legacy screens CTRTLIA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| No matching transaction types | message | Error under the filters: 'No transaction types match these filters. Change or clear the filters.'; on a database error: 'The transaction types could not be read. Try again.' | Supplied filters must match at least one type: 'No transaction types match these filters.' (legacy 'No Records found for these filter conditions') |  | TTRDM-REQ-F-050, TTRDM-REQ-F-051 |
| Edit description | button | Turns the description of this row into an input; one row is edited at a time, so other row actions are disabled meanwhile | One row action at a time, so the legacy errors 'Please select only 1 action' and 'Action code selected is invalid' cannot occur. |  | TTRDM-REQ-F-041, TTRDM-REQ-F-048, TTRDM-REQ-F-049 |
| Description | text | New description of the row being edited, up to 50 characters; the row is highlighted | Required; letters, digits and spaces only. Messages: 'Enter a description.' (legacy 'Transaction Desc must be supplied.'), 'Description can only contain letters, digits and spaces.' (legacy 'Transaction Desc can have numbers or alphabets only.'). If unchanged: 'No changes to save.' (legacy 'No change detected with respect to values fetched.') |  | TTRDM-REQ-F-042, TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046, TTRDM-REQ-F-047 |


## Data models

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

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-048 | Capture filters and row entries | design note | WHEN the operator submits the transaction type list screen, THE transaction type list SHALL capture the type code and description filters and, for each of the 7 rows, the action code, the type code and the description, treating a description of '*' or all spaces as not entered and trimming any other description. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:930-953, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:55, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:60 |
| TTRDM-BR-049 | Treat blank or asterisk description as unsupplied | design note | WHEN a row's description field holds only '*' or is blank, THE Transaction Type List screen SHALL treat the description as not entered; otherwise it SHALL use the entered text with leading and trailing spaces removed. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:940-953, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1026-1031, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1060-1090, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1181-1234 |
| TTRDM-BR-050 | Detect unchanged update description | business rule | WHEN a transaction type row marked 'U' is submitted and the entered description matches the stored description, ignoring upper/lower case and leading or trailing spaces, THE Transaction Type List screen SHALL show 'No change detected with respect to database values.' and skip the remaining description checks for that row. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:940-953, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1026-1031, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1060-1090, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1181-1234 |
| TTRDM-BR-051 | Require valid updated description | business rule | WHEN the entered description of a row marked 'U' differs from the stored description, THE Transaction Type List screen SHALL treat the row as changed and check the first 50 characters of the description as a required letters-and-digits field named 'Transaction Desc'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:940-953, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1026-1031, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1060-1090, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1181-1234 |
| TTRDM-BR-052 | Reject missing required text | business rule | WHEN a changed description is not entered (blank or '*'), THE Transaction Type List screen SHALL reject the input and show 'Transaction Desc must be supplied.', unless an earlier message has already been set. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:940-953, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1026-1031, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1060-1090, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1181-1234 |
| TTRDM-BR-053 | Restrict text to letters and digits | business rule | WHEN a changed description contains any character other than a letter, a digit or a space, THE Transaction Type List screen SHALL reject the input and show 'Transaction Desc can have numbers or alphabets only.', unless an earlier message has already been set. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:940-953, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1026-1031, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1060-1090, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1181-1234 |
| TTRDM-BR-054 | Require transaction description for update | formatting | WHEN a description entered for update fails its checks, THE Transaction Type List screen SHALL show that description in red with the cursor on it, and SHALL show a description that was not entered as '*'. | high | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:940-953, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1026-1031, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1060-1090, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1181-1234 |
| TTRDM-BR-055 | Show entered changed description | formatting | WHEN a row is marked 'U' as the only valid action on the screen and the operator has typed a description that differs from the stored one and is not blank, THE transaction type list SHALL show the operator's typed description on that row instead of the stored description. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1404-1419, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1064-1076, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:944-951 |
| TTRDM-BR-056 | Show stored description when unchanged | formatting | WHEN a row is not the single valid 'U' action on the screen, or it is but the typed description does not differ from the stored one, THE transaction type list SHALL show the stored transaction type description on that row. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1404-1425, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1062-1076 |
| TTRDM-BR-057 | Redisplay list after input errors | business rule | WHEN the submitted screen has an input error, THE Transaction Type List screen SHALL show the error message and stay on the list screen rather than act on any key pressed. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:698-720, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1111-1118 |
| TTRDM-BR-058 | Redisplay list after input errors | formatting | WHEN the submitted screen has an input error but both the type code filter and the description filter are acceptable, THE Transaction Type List screen SHALL re-read the current page starting from its first type code before showing the error. | medium | app/app-transaction-type-db2/cbl/COTRTLIC.cbl:698-720, app/app-transaction-type-db2/cbl/COTRTLIC.cbl:1111-1118 |

### Worked examples

- TTRDM-BR-048: row 3 description = * → Row 3 description is treated as not entered
- TTRDM-BR-049: Entered description = * → The description counts as not entered
- TTRDM-BR-050: Stored description = Payment; Action = U; Entered description = payment → Message 'No change detected with respect to database values.'
- TTRDM-BR-050: Stored description = Payment; Action = U; Entered description = PAYMENT → Message 'No change detected with respect to database values.'
- TTRDM-BR-051: Stored description = Payment; Action = U; Entered description = Bill Payment → The row counts as changed and the description passes the checks
- TTRDM-BR-053: Action = U; Entered description = Cash Advance 2 → Description accepted
- TTRDM-BR-054: Action = U; Entered description = → The description field shows '*' in red
- TTRDM-BR-056: row action = D → Row shows the stored description
- TTRDM-BR-057: Type code filter = A1 → The list screen is shown again with 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER'
- TTRDM-BR-058: Type code filter = blank; Row error = invalid row action; First type code on page = 05 → The page is re-read from type 05 and shown with the error message
- TTRDM-BR-058: Type code filter = X9 → The list is not re-read; the screen is redisplayed with the filter error

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


## Design notes

- TTRDM-BR-048: The list form posts the two filters plus seven row entries, each with an action, a type code and a description. Bind them to a request model with a fixed list of 7 rows. Map a description of '*' or all spaces to 'not entered', and trim any other description.
- TTRDM-BR-049: Normalise row descriptions when reading the request: a blank value or a lone '*' becomes null (not entered), and any other value is trimmed at both ends. Validation and change detection work on the normalised value.

## Open questions

- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-048, TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-048, TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-048, TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-048, TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053.
- DEF-029: Is this intended? The 'No change detected' case only sets a message and does not mark the input as an error, so the row stays ready for update; pressing F10 then still runs the database update. A change only in upper/lower case (e.g. 'Payment' to 'payment') is reported as no change but is saved on F10. (Subject-matter expert) On TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-049, TTRDM-BR-052, TTRDM-BR-053, TTRDM-BR-054.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).
