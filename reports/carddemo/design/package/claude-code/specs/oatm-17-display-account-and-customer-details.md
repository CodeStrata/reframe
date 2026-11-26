# Display account and customer details (OATM-C17)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Shows an account's financial details and its cardholder's profile together on one screen for users reviewing an account. Each part is shown only when its record was actually found. As agreed, the customer's full Social Security number is shown unmasked as NNN-NN-NNNN, so that screen needs proper access control. The cursor always returns to the account number field.

**User story:** As a user, I want to see an account's financial details and its customer's profile on one screen, so that I can review the account and the cardholder.

## Requirements

### Requirement 1: OATM-REQ-F-137 (formatting)

#### Acceptance criteria

1. When the account was found in the account master file, the system shall show the account status, current balance, credit limit, cash credit limit, current cycle credit, current cycle debit, open date, expiration date, reissue date and group id. (rules OATM-BR-140)
2. GIVEN account number: 00000012345; account master: found, status Y, balance 1500.00, credit limit 5000.00 WHEN the account was found in the account master file THEN Screen shows status Y, balance 1500.00, credit limit 5000.00 and the other account fields (OATM-C17-AC-01; OATM-BR-140)

### Requirement 2: OATM-REQ-F-138 (formatting)

#### Acceptance criteria

1. When the account's customer was found in the customer master file, the system shall show the customer id, FICO score, date of birth, first, middle and last name, address lines, city, state, zip, country, both phone numbers, government-issued id, EFT account id and primary card holder indicator. (rules OATM-BR-141, OATM-BR-142)
2. GIVEN Account number entered: 00000000002; Customer found in master: no (record not found) WHEN the customer was found in the customer master THEN No customer identity, contact or SSN fields are filled in on the screen. (OATM-C17-AC-02; OATM-BR-141)
3. GIVEN customer number: 000000001; customer master: found WHEN the account's customer was found in the customer master file THEN All customer fields shown with the account details (OATM-C17-AC-03; OATM-BR-142)
4. GIVEN account master: found; customer master: not found WHEN the account's customer was found in the customer master file THEN Account fields shown, customer fields empty, error 'Did not find associated customer in master file' (OATM-C17-AC-04; OATM-BR-142)

### Requirement 3: OATM-REQ-N-005 (business rule)

#### Acceptance criteria

1. When the customer is found, the system shall show the customer's full Social Security number, unmasked, in the form NNN-NN-NNNN. (rules OATM-BR-141, OATM-BR-143)
2. GIVEN Account number entered: 00000000002; Customer found in master: no (record not found) WHEN the customer was found in the customer master THEN No customer identity, contact or SSN fields are filled in on the screen. (OATM-C17-AC-02; OATM-BR-141)
3. GIVEN customer SSN: 123456789 WHEN the customer is found THEN Screen shows 123-45-6789 (OATM-C17-AC-05; OATM-BR-143)

### Requirement 4: OATM-REQ-F-139 (formatting)

#### Acceptance criteria

1. When the account view screen is shown with no session data passed (started directly), the system shall show no account or customer details and show the information line 'Enter or update id of account to display'. (rules OATM-BR-144)
2. GIVEN session data passed: none (transaction CAVW typed directly) WHEN the account view screen is shown with no session data passed (started directly) THEN Empty screen with info line 'Enter or update id of account to display' (OATM-C17-AC-06; OATM-BR-144)

### Requirement 5: OATM-REQ-F-140 (formatting)

#### Acceptance criteria

1. While session data exists, the system shall show the account number the user entered in the account number field, or leave the field empty when no account number was entered. (rules OATM-BR-145)
2. GIVEN entered account number: 00000012345 WHEN session data exists THEN Account number field shows 00000012345 (OATM-C17-AC-07; OATM-BR-145)
3. GIVEN entered account number: (blank) WHEN session data exists THEN Account number field is empty (OATM-C17-AC-08; OATM-BR-145)

### Requirement 6: OATM-REQ-F-141 (formatting)

#### Acceptance criteria

1. The system shall show 'Enter or update id of account to display' on the information line when no information message has been set, and always show the current error message, if there is one, on the error line. (rules OATM-BR-146)
2. GIVEN information message: (none); error message: 'Did not find this account in account master file' WHEN no information message has been set THEN Info line 'Enter or update id of account to display', error line 'Did not find this account in account master file' (OATM-C17-AC-09; OATM-BR-146)

### Requirement 7: OATM-REQ-F-142 (formatting)

#### Acceptance criteria

1. The system shall place the cursor on the account number field every time the account view screen is shown, whether or not the input had an error. (rules OATM-BR-147)
2. GIVEN Account number: ABC12345678 WHEN account view runs THEN The cursor is on the account number field (OATM-C17-AC-10; OATM-BR-147)
3. GIVEN Account number: 00000012345 (valid) WHEN account view runs THEN The cursor is also on the account number field (OATM-C17-AC-11; OATM-BR-147)

## Screens and components

### Account (S-ACCOUNT-VIEW)

Find an account by number and review its status, dates, balances and limits together with the cardholder's profile, address and contacts, with direct links (new) to update it or pay its balance.

Prototype: `ui-reference/index.html#/S-ACCOUNT-VIEW`. Replaces the legacy screens CACTVWA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account number | search | 11-digit account number; has focus whenever the screen opens | Required: 'No input received' when blank; must be 11 digits and not all zeros: 'Account Filter must be a non-zero 11 digit number'. |  |  |
| Guidance | message | 'Enter or update id of account to display' until an account is shown |  |  | OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141 |
| Status | display | Active or Inactive (stored Y/N) |  |  | OATM-REQ-F-137 |
| Customer ID | display | 9-digit customer number |  |  | OATM-REQ-F-138 |
| Social Security number | display | SSN as NNN-NN-NNNN |  |  | OATM-REQ-N-005 |


## Data models

#### CSMSG02Y

File record of COACTVWC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

#### CVACT01Y

File record of COACTVWC. Source: `app/cpy/CVACT01Y.cpy`.

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

File record of COACTVWC. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCUS01Y

File record of COACTVWC. Source: `app/cpy/CVCUS01Y.cpy`.

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

- COCOM01Y (working storage of COACTVWC): see data-contracts.md.
- COTTL01Y (working storage of COACTVWC): see data-contracts.md.
- CSDAT01Y (working storage of COACTVWC): see data-contracts.md.
- CSMSG01Y (working storage of COACTVWC): see data-contracts.md.
- CSSTRPFY (working storage of COACTVWC): see data-contracts.md.
- CSUSR01Y (working storage of COACTVWC): see data-contracts.md.
- CVACT02Y (working storage of COACTVWC): see data-contracts.md.
- CVCRD01Y (working storage of COACTVWC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-140 | Display account financial details | formatting | WHEN the account was found in the account master file, THE Account View Screen SHALL show the account status, current balance, credit limit, cash credit limit, current cycle credit, current cycle debit, open date, expiration date, reissue date and group id. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-141 | Display customer profile with formatted SSN | formatting | WHEN the customer was found in the customer master, THE Account View Screen Display SHALL display the customer identity, contact, credit score and indicators, with the SSN formatted as NNN-NN-NNNN | medium | app/cbl/COACTVWC.cbl:493-494,496-523,525, app/cbl/COACTVWC.cbl:493-507 |
| OATM-BR-142 | Account and customer details displayed only when found in master files | formatting | WHEN the account's customer was found in the customer master file, THE Account View Screen SHALL show the customer id, FICO score, date of birth, first, middle and last name, address lines, city, state, zip, country, both phone numbers, government-issued id, EFT account id and primary card holder indicator. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-143 | Account and customer details displayed only when found in master files | business rule | WHEN the customer is found, THE Account View Screen SHALL show the customer's full Social Security number, unmasked, in the form NNN-NN-NNNN. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-144 | Show prompt or entered account number | formatting | WHEN the account view screen is shown with no session data passed (started directly), THE Account View Screen SHALL show no account or customer details and SHALL show the information line 'Enter or update id of account to display'. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-145 | Show prompt or entered account number | formatting | WHEN session data exists, THE Account View Screen SHALL show the account number the user entered in the account number field, or leave the field empty when no account number was entered. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-146 | Set default prompt and screen messages | formatting | WHEN no information message has been set, THE Account View Screen SHALL show 'Enter or update id of account to display' on the information line, and SHALL always show the current error message, if there is one, on the error line. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-147 | Account ID search key must be a non-zero 11-digit number | formatting | THE account view SHALL place the cursor on the account number field every time the screen is shown, whether or not the input had an error. | high | app/cbl/COACTVWC.cbl:622-643, app/cbl/COACTVWC.cbl:649-685, app/cbl/COACTVWC.cbl:117-124, app/cbl/COACTVWC.cbl:362-367 |

### Worked examples

- OATM-BR-140: account number = 00000012345; account master = found, status Y, balance 1500.00, credit limit 5000.00 → Screen shows status Y, balance 1500.00, credit limit 5000.00 and the other account fields
- OATM-BR-141: Account number entered = 00000000002; Customer found in master = no (record not found) → No customer identity, contact or SSN fields are filled in on the screen.
- OATM-BR-142: customer number = 000000001; customer master = found → All customer fields shown with the account details
- OATM-BR-142: account master = found; customer master = not found → Account fields shown, customer fields empty, error 'Did not find associated customer in master file'
- OATM-BR-143: customer SSN = 123456789 → Screen shows 123-45-6789
- OATM-BR-144: session data passed = none (transaction CAVW typed directly) → Empty screen with info line 'Enter or update id of account to display'
- OATM-BR-145: entered account number = 00000012345 → Account number field shows 00000012345
- OATM-BR-145: entered account number = (blank) → Account number field is empty
- OATM-BR-146: information message = (none); error message = 'Did not find this account in account master file' → Info line 'Enter or update id of account to display', error line 'Did not find this account in account master file'
- OATM-BR-147: Account number = ABC12345678 → The cursor is on the account number field
- OATM-BR-147: Account number = 00000012345 (valid) → The cursor is also on the account number field

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-067: When an account number is entered on the account view screen and the account is not found, or the file cannot be read, should the lookup stop at that point? (Currently it stops only on one exact message, 'Did not find this account in account master file', and the real not-found path produces a different message.) (Business analyst) On OATM-BR-141, OATM-BR-145, OATM-BR-140, OATM-BR-146.
- SME-068: On the account view screen, if the account number is left blank, which message should the operator see: 'Account number not provided' or 'No input received'? (Business analyst) On OATM-BR-141, OATM-BR-145, OATM-BR-140, OATM-BR-146.
- SME-069: On the account view screen, the error message says the account number must be 'a non-zero 11 digit number', but only 'numeric and non-zero' is checked. Should exactly 11 digits be required? Should the message keep its current double space? (Business analyst) On OATM-BR-141, OATM-BR-145, OATM-BR-140, OATM-BR-146.
- SME-070: On the account view screen, if the customer record is found but the account record is not, should the account's financial details still be shown? After a successful lookup, should the screen show a success message ('Displaying details of given Account') instead of the input prompt? (Customer service operations lead) On OATM-BR-141, OATM-BR-145, OATM-BR-140, OATM-BR-146.
- SME-072: The account view shows every user the customer's full, unmasked Social Security number. Is that acceptable under privacy policy, or should the new system show only the last 4 digits or limit the full number to certain roles? (Privacy and compliance officer) On OATM-BR-141.
- DEF-044: Is this intended? A blank account number first sets the message 'Account number not provided', which is then replaced at once with 'No input received', so the more specific message can never be shown. The 'only if no message yet' guard in front of it has no effect. (Subject-matter expert) On OATM-BR-147.
- DEF-091: Is this intended? The success message 'Displaying details of given Account' is defined but never set, and the account read clears the information message. As a result, the info line still says 'Enter or update id of account to display' after an account is shown successfully. (Subject-matter expert) On OATM-BR-145, OATM-BR-140, OATM-BR-146.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (11 in all).
