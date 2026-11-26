# Requirements: Update transaction type descriptions from the list (TTRDM-C05)

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
