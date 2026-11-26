# Feature specification: Update transaction type descriptions from the list

**Feature:** TTRDM-C05 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C05)

As an administrator, I want to mark a listed transaction type for update or delete and change its description on the list screen, so that I can correct reference data online with clear validation feedback.

On the transaction type list an administrator can mark one row 'U' and type a new description in place. The description is checked before anything is saved: it must be supplied, must actually differ from the stored one (ignoring case and surrounding spaces), and may hold only letters, digits and spaces. The screen must never save an invalid or unchanged description, and must show the user exactly which field is wrong.

**Acceptance scenarios:**

1. **Given** row 3 description: *, **when** the operator submits the transaction type list screen, **then** Row 3 description is treated as not entered (TTRDM-C05-AC-01)
2. **Given** Entered description: *, **when** a row's description field holds only '*' or is blank, **then** The description counts as not entered (TTRDM-C05-AC-02)
3. **Given** Stored description: Payment; Action: U; Entered description: payment, **when** a transaction type row marked 'U' is submitted and the entered description matches the stored description, ignoring upper/lower case and leading or trailing spaces, **then** Message 'No change detected with respect to database values.' (TTRDM-C05-AC-03)
4. **Given** Stored description: Payment; Action: U; Entered description: PAYMENT, **when** a transaction type row marked 'U' is submitted and the entered description matches the stored description, ignoring upper/lower case and leading or trailing spaces, **then** Message 'No change detected with respect to database values.' (TTRDM-C05-AC-04)
5. **Given** Stored description: Payment; Action: U; Entered description: Bill Payment, **when** the entered description of a row marked 'U' differs from the stored description, **then** The row counts as changed and the description passes the checks (TTRDM-C05-AC-05)
6. **Given** Action: U; Entered description: Cash Advance 2, **when** a changed description contains any character other than a letter, a digit or a space, **then** Description accepted (TTRDM-C05-AC-06)
7. **Given** Action: U; Entered description:, **when** a description entered for update fails its checks, **then** The description field shows '*' in red (TTRDM-C05-AC-07)
8. **Given** row action: D, **when** a row is not the single valid 'U' action on the screen, or it is but the typed description does not differ from the stored one, **then** Row shows the stored description (TTRDM-C05-AC-08)
9. **Given** Type code filter: A1, **when** the submitted screen has an input error, **then** The list screen is shown again with 'TYPE CODE FILTER,IF SUPPLIED MUST BE A 2 DIGIT NUMBER' (TTRDM-C05-AC-09)
10. **Given** Type code filter: blank; Row error: invalid row action; First type code on page: 05, **when** the submitted screen has an input error but both the type code filter and the description filter are acceptable, **then** The page is re-read from type 05 and shown with the error message (TTRDM-C05-AC-10)
11. **Given** Type code filter: X9, **when** the submitted screen has an input error but both the type code filter and the description filter are acceptable, **then** The list is not re-read; the screen is redisplayed with the filter error (TTRDM-C05-AC-11)
12. **Given** Transaction type '01' is shown on the list with stored description 'Purchase' and no other message has been set, **when** The user marks the row for '01' with 'U', clears its description (or enters only '*') and presses Enter, **then** The input is rejected, nothing is saved, and the message 'Transaction Desc must be supplied.' is shown (TTRDM-C05-AC-12)
13. **Given** Transaction type '01' is shown on the list with stored description 'Purchase', **when** The user marks only the row for '01' with 'U', types 'Retail Purchase' as its description and presses Enter, **then** The redisplayed row for '01' shows 'Retail Purchase', not the stored 'Purchase' (TTRDM-C05-AC-13)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-041** (design note): When the operator submits the transaction type list screen, the system shall capture the type code and description filters and, for each of the 7 rows, the action code, the type code and the description. Rules: TTRDM-BR-048.
- **TTRDM-REQ-F-042** (design note): When a row's description field holds only '*' or is blank, the system shall treat the description as not entered, and otherwise shall use the entered text with leading and trailing spaces removed. Rules: TTRDM-BR-048, TTRDM-BR-049.
- **TTRDM-REQ-F-043** (business rule): When a transaction type row marked 'U' is submitted and the entered description matches the stored description, ignoring upper/lower case and leading or trailing spaces, the system shall show 'No change detected with respect to database values.' and skip the remaining description checks for that row. Rules: TTRDM-BR-050.
- **TTRDM-REQ-F-044** (business rule): When the entered description of a row marked 'U' differs from the stored description, the system shall treat the row as changed and check the first 50 characters of the description as a required letters-and-digits field named 'Transaction Desc'. Rules: TTRDM-BR-051.
- **TTRDM-REQ-F-045** (business rule): If a changed description is not entered (blank or '*'), then the system shall reject the input and show 'Transaction Desc must be supplied.', unless an earlier message has already been set. Rules: TTRDM-BR-052.
- **TTRDM-REQ-F-046** (business rule): If a changed description contains any character other than a letter, a digit or a space, then the system shall reject the input and show 'Transaction Desc can have numbers or alphabets only.', unless an earlier message has already been set. Rules: TTRDM-BR-053.
- **TTRDM-REQ-F-047** (formatting): If a description entered for update fails its checks, then the system shall show that description in red with the cursor on it, and shall show a description that was not entered as '*'. Rules: TTRDM-BR-054.
- **TTRDM-REQ-F-048** (formatting): When a row is marked 'U' as the only valid action on the screen and the operator has typed a description that differs from the stored one and is not blank, the system shall show the operator's typed description on that row instead of the stored description. Rules: TTRDM-BR-055.
- **TTRDM-REQ-F-049** (formatting): When a row is not the single valid 'U' action on the screen, or it is but the typed description does not differ from the stored one, the system shall show the stored transaction type description on that row. Rules: TTRDM-BR-056.
- **TTRDM-REQ-F-050** (business rule): If the submitted screen has an input error, then the system shall show the error message and stay on the list screen rather than act on any key pressed. Rules: TTRDM-BR-057.
- **TTRDM-REQ-F-051** (formatting): If the submitted screen has an input error but both the type code filter and the description filter are acceptable, then the system shall re-read the current page starting from its first type code before showing the error. Rules: TTRDM-BR-058.

### Business rules

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

### Key entities

- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSDB2RPY (working storage)
- CSDB2RWY (working storage)
- CSMSG01Y (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CVACT02Y (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-183: The transaction-type code filter's error message says 'MUST BE A 2 DIGIT NUMBER', but the system only checks that the value is numeric. Should numbers that are not exactly 2 digits be refused? (Reference data product owner) On TTRDM-BR-048, TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053.
- SME-186: When counting transaction types fails, what diagnostic details should the operator see, and does the failure end the session on that screen? (Reference data product owner) On TTRDM-BR-048, TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053.
- SME-187: When one submission on the transaction-type list has several errors (an invalid action code, more than one action, or missing required text), which message should the operator see first? (Business analyst) On TTRDM-BR-048, TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053.
- SME-188: The error message 'Error reading TRANSACTION_TYPE table ' ends with a space. Does that trailing space matter in the message shown to the operator? (Business analyst) On TTRDM-BR-048, TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053.
- DEF-029: Is this intended? The 'No change detected' case only sets a message and does not mark the input as an error, so the row stays ready for update; pressing F10 then still runs the database update. A change only in upper/lower case (e.g. 'Payment' to 'payment') is reported as no change but is saved on F10. (Subject-matter expert) On TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-049, TTRDM-BR-052, TTRDM-BR-053, TTRDM-BR-054.

### Decision table gaps

- Updated description check for a row marked 'U': No rule states what happens next for a valid changed description (how the update is confirmed and saved), nor how a row marked 'D' is confirmed and deleted online.
- Updated description check for a row marked 'U': Only the first 50 characters are checked; rules do not say what happens to text beyond 50 characters.
