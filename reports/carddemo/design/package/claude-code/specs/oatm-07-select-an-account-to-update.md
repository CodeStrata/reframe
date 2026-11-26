# Select an account to update (OATM-C07)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Lets the operator enter an 11-digit account number to start an update; until an account is fetched only that number is checked. A valid number triggers the cross-reference, account and customer lookups, and details are shown only when all three are found. A blank, non-numeric or all-zero number must never lead to a lookup.

**User story:** As an operator, I want to enter an account number and see the account and customer details, so that I can review and update them.

## Requirements

### Requirement 1: OATM-REQ-F-062 (design note)

#### Acceptance criteria

1. When the operator submits the account update screen, the system shall treat an account number of '*' or blank as not supplied and otherwise take the entered value as the account to search for. (rules OATM-BR-061)
2. GIVEN Account number entered: '*' WHEN the operator submits the account update screen THEN The account number is treated as not supplied (OATM-C07-AC-01; OATM-BR-061)
3. GIVEN Account number entered: 00000012345 WHEN the operator submits the account update screen THEN 00000012345 is used as the account to search for (OATM-C07-AC-02; OATM-BR-061)

### Requirement 2: OATM-REQ-F-063 (business rule)

#### Acceptance criteria

1. While no account details have been fetched yet, the system shall check only the account number and ignore every other field on the screen. (rules OATM-BR-062)
2. GIVEN Account details fetched: No; Account number entered: 00000012345; Active status entered: X WHEN no account details have been fetched yet THEN Only the account number is checked; the active status is not checked (OATM-C07-AC-03; OATM-BR-062)

### Requirement 3: OATM-REQ-F-064 (business rule)

#### Acceptance criteria

1. If no account details have been fetched yet and the account number is blank or '*', then the system shall show the error 'No input received', set the current account number to zeros and read no account. (rules OATM-BR-063)
2. GIVEN Account number entered: (blank) WHEN no account details have been fetched yet and the account number is blank or '*' THEN Error 'No input received' is shown and no account is read (OATM-C07-AC-04; OATM-BR-063)
3. GIVEN Account number entered: '*' WHEN no account details have been fetched yet and the account number is blank or '*' THEN Error 'No input received' is shown and no account is read (OATM-C07-AC-05; OATM-BR-063)

### Requirement 4: OATM-REQ-F-065 (business rule)

#### Acceptance criteria

1. If no account details have been fetched yet and the account number supplied is not numeric or is all zeros, then the system shall show 'Account Number if supplied must be a 11 digit Non-Zero Number', set the current account number to zeros and read no account. (rules OATM-BR-064)
2. GIVEN no account details have been fetched yet and the operator enters account number '1234ABC5678' WHEN the screen is submitted THEN the message 'Account Number if supplied must be a 11 digit Non-Zero Number' is shown, the current account number is set to zeros and no account is read (OATM-C07-AC-10; OATM-BR-064)
3. GIVEN no account details have been fetched yet and the operator enters account number '00000000000' WHEN the screen is submitted THEN the message 'Account Number if supplied must be a 11 digit Non-Zero Number' is shown, the current account number is set to zeros and no account is read (OATM-C07-AC-11; OATM-BR-064)

### Requirement 5: OATM-REQ-F-066 (business rule)

#### Acceptance criteria

1. While no account details have been fetched yet, when the account number is an 11-digit non-zero number, the system shall accept it as the current account and go on to look the account up. (rules OATM-BR-065)
2. GIVEN Account number entered: 00000012345 WHEN no account details have been fetched yet and the account number is an 11-digit non-zero number THEN 00000012345 becomes the current account and its details are looked up (OATM-C07-AC-06; OATM-BR-065)

### Requirement 6: OATM-REQ-F-067 (business rule)

#### Acceptance criteria

1. When account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid, the system shall look up the card cross-reference, then the account, then the customer, stopping at the first one not found, and shall show the details (state 'S') only when all three are found. (rules OATM-BR-066)
2. GIVEN account number: 00000000001; cross-reference, account and customer: all exist WHEN account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid THEN Details are shown and state becomes 'S' (OATM-C07-AC-07; OATM-BR-066)
3. GIVEN account number: 00000000099; account master record: missing WHEN account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid THEN Lookup stops with 'Did not find this account in account master file'; details are not shown (OATM-C07-AC-08; OATM-BR-066)
4. GIVEN key: PF12; update state: 'E' WHEN account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid THEN Account is re-read, pending edits are discarded and state returns to 'S' (OATM-C07-AC-09; OATM-BR-066)

## Screens and components

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account number | search | 11-digit account number; the only editable field until an account is fetched | Required: 'No input received' when blank; 'Account Number if supplied must be a 11 digit Non-Zero Number' when not numeric or all zeros; 'Account:<number> not found in Cross ref file' when the account has no card cross-reference. |  | OATM-REQ-F-062, OATM-REQ-F-063, OATM-REQ-F-064 |
| Fetch account | button |  |  |  | OATM-REQ-F-067 |
| Discard changes | button | Re-fetches the stored values; available once an account is fetched |  |  | OATM-REQ-F-067 |


## Data models

#### CSMSG02Y

File record of COACTUPC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

#### CVACT01Y

File record of COACTUPC. Source: `app/cpy/CVACT01Y.cpy`.

Record `ACCOUNT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| ACCT-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| ACCT-CURR-BAL |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CASH-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-OPEN-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-REISSUE-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-CURR-CYC-CREDIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CURR-CYC-DEBIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| ACCT-GROUP-ID |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(178) | text, 178 characters |  |  |  |

#### CVACT03Y

File record of COACTUPC. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCUS01Y

File record of COACTUPC. Source: `app/cpy/CVCUS01Y.cpy`.

Record `CUSTOMER-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-FIRST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-MIDDLE-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-LAST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-ADDR-LINE-1 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-2 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-3 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-STATE-CD |  | X(02) | text, 2 characters |  |  |  |
| CUST-ADDR-COUNTRY-CD |  | X(03) | text, 3 characters |  |  |  |
| CUST-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| CUST-PHONE-NUM-1 |  | X(15) | text, 15 characters |  |  |  |
| CUST-PHONE-NUM-2 |  | X(15) | text, 15 characters |  |  |  |
| CUST-SSN |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-GOVT-ISSUED-ID |  | X(20) | text, 20 characters |  |  |  |
| CUST-DOB-YYYY-MM-DD |  | X(10) | text, 10 characters |  |  |  |
| CUST-EFT-ACCOUNT-ID |  | X(10) | text, 10 characters |  |  |  |
| CUST-PRI-CARD-HOLDER-IND |  | X(01) | text, 1 character |  |  |  |
| CUST-FICO-CREDIT-SCORE |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| FILLER |  | X(168) | text, 168 characters |  |  |  |

- COCOM01Y (working storage of COACTUPC): see data-contracts.md.
- COTTL01Y (working storage of COACTUPC): see data-contracts.md.
- CSDAT01Y (working storage of COACTUPC): see data-contracts.md.
- CSLKPCDY (working storage of COACTUPC): see data-contracts.md.
- CSMSG01Y (working storage of COACTUPC): see data-contracts.md.
- CSSETATY (working storage of COACTUPC): see data-contracts.md.
- CSSTRPFY (working storage of COACTUPC): see data-contracts.md.
- CSUSR01Y (working storage of COACTUPC): see data-contracts.md.
- CSUTLDPY (working storage of COACTUPC): see data-contracts.md.
- CSUTLDWY (working storage of COACTUPC): see data-contracts.md.
- CVCRD01Y (working storage of COACTUPC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-061 | Capture account id entry | design note | WHEN the operator submits the account update screen, THE account update screen SHALL treat an account number of '*' or blank as not supplied and otherwise take the entered value as the account to search for. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-062 | Skip edits when details not fetched | business rule | WHEN no account details have been fetched yet, THE account update screen SHALL check only the account number and ignore every other field on the screen. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-063 | Reject missing account number | business rule | WHEN no account details have been fetched yet and the account number is blank or '*', THE account update screen SHALL show the error 'No input received', set the current account number to zeros and read no account. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-064 | Require 11-digit non-zero account number | business rule | WHEN no account details have been fetched yet and the account number supplied is not numeric or is all zeros, THE account update screen SHALL show 'Account Number if supplied must be a 11 digit Non-Zero Number', set the current account number to zeros and read no account. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-065 | Require 11-digit non-zero account number | business rule | WHEN no account details have been fetched yet and the account number is an 11-digit non-zero number, THE account update screen SHALL accept it as the current account and go on to look the account up. | high | app/cbl/COACTUPC.cbl:1051-1062, app/cbl/COACTUPC.cbl:1429-1449, app/cbl/COACTUPC.cbl:1783-1818, app/cbl/COACTUPC.cbl:480-490 |
| OATM-BR-066 | Retrieve account and customer details for update | business rule | WHEN account details are not yet fetched, or the operator presses PF12 to cancel changes, and the account number entered is valid, THE account update screen SHALL look up the card cross-reference, then the account, then the customer, stopping at the first one not found, and SHALL show the details (state 'S') only when all three are found. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |

### Worked examples

- OATM-BR-061: Account number entered = '*' → The account number is treated as not supplied
- OATM-BR-061: Account number entered = 00000012345 → 00000012345 is used as the account to search for
- OATM-BR-062: Account details fetched = No; Account number entered = 00000012345; Active status entered = X → Only the account number is checked; the active status is not checked
- OATM-BR-063: Account number entered = (blank) → Error 'No input received' is shown and no account is read
- OATM-BR-063: Account number entered = '*' → Error 'No input received' is shown and no account is read
- OATM-BR-065: Account number entered = 00000012345 → 00000012345 becomes the current account and its details are looked up
- OATM-BR-066: account number = 00000000001; cross-reference, account and customer = all exist → Details are shown and state becomes 'S'
- OATM-BR-066: account number = 00000000099; account master record = missing → Lookup stops with 'Did not find this account in account master file'; details are not shown
- OATM-BR-066: key = PF12; update state = 'E' → Account is re-read, pending edits are discarded and state returns to 'S'

## Decision tables

#### Account number check before details are fetched

| Account details fetched | Account number entry | Screen response | Rule |
|---|---|---|---|
| No | Blank or '*' | Show 'No input received', set account number to zeros, read no account | OATM-BR-063 |
| No | Not numeric or all zeros | Show 'Account Number if supplied must be a 11 digit Non-Zero Number', set account number to zeros, read no account | OATM-BR-064 |
| No | 11-digit non-zero number | Accept as current account and look the account up | OATM-BR-065 |
| No | Numeric, non-zero, fewer than 11 digits entered | **Gap:** No rule states whether a shorter numeric entry is accepted (e.g. padded) or rejected with the 11-digit message. | |


## Design notes

- OATM-BR-061: Input binding for the account number: blank or '*' becomes null (not supplied), otherwise the entered text is kept as the search key for the account-number validation.

## Open questions

- SME-054: When saving an account update, a failure to lock the customer record is reported as a successful save. Is that intended, or should it be reported as a lock error? (Account servicing business owner) On OATM-BR-066.
- SME-055: When the customer for an account cannot be found during account update, a 'not found' message is shown but the customer is not marked as not found. Should the new system explicitly mark the customer as not found? (Account servicing business owner) On OATM-BR-062, OATM-BR-063, OATM-BR-065, OATM-BR-066.
- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-062.
- DEF-040: Is this intended? For a blank account number, the 'Account number not provided' message set in 1210-EDIT-ACCOUNT is always overwritten by 'No input received' in 1200-EDIT-MAP-INPUTS, so the more specific message is never shown on this path. (Subject-matter expert) On OATM-BR-062, OATM-BR-063, OATM-BR-065.
- DEF-074: Is this intended? The decision step has a branch that turns a committed save ('C') back into 'details shown' and clears the account and card number when there is no calling transaction, but it can never run: the main dispatch catches state 'C' first on the next interaction and resets the screen itself. The field edits also skip the 'C' state check for the same reason. (Subject-matter expert) On OATM-BR-066.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (11 in all).
