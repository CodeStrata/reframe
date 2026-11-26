# Implementation plan: Capture entered changes (OATM-C03)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account group (optional) | text | Up to 10 characters |  |  | OATM-REQ-F-025 |
| Credit limit | money |  | Required: 'Credit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Credit Limit is not valid'; negative and zero amounts are accepted. |  | OATM-REQ-F-029, OATM-REQ-F-030 |
| Cash credit limit | money |  | Required: 'Cash Credit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Cash Credit Limit is not valid'; negative and zero amounts are accepted. |  | OATM-REQ-F-029, OATM-REQ-F-030 |
| Current balance | money |  | Required: 'Current Balance must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Current Balance is not valid'; negative and zero amounts are accepted. |  | OATM-REQ-F-029, OATM-REQ-F-030 |
| Current cycle credit | money |  | Required: 'Current Cycle Credit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Current Cycle Credit Limit is not valid'; negative and zero amounts are accepted. |  | OATM-REQ-F-029, OATM-REQ-F-030 |
| Current cycle debit | money |  | Required: 'Current Cycle Debit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Current Cycle Debit Limit is not valid'; negative and zero amounts are accepted. |  | OATM-REQ-F-029, OATM-REQ-F-030 |
| Customer ID | display | Customer number; not editable |  |  | OATM-REQ-F-027 |
| Date of birth | date |  | Year, month and day must all be supplied: 'Date of Birth : Year must be supplied.', 'Date of Birth : Month must be supplied.', 'Date of Birth : Day must be supplied.'. The year must be 4 digits: 'Date of Birth must be 4 digit number.', starting 19 or 20: 'Date of Birth : Century is not valid.'. 'Date of Birth: Month must be a number between 1 and 12.'; 'Date of Birth:day must be a number between 1 and 31.'; 'Date of Birth:Cannot have 31 days in this month.'; 'Date of Birth:Cannot have 30 days in this month.'; 'Date of Birth:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Date of Birth validation error ...'. Must be before today: 'Date of Birth:cannot be in the future '. |  | OATM-REQ-F-032 |
| Country | display | Country code; not editable |  |  | OATM-REQ-F-026 |
| Government-issued ID reference | text | Up to 20 characters |  |  | OATM-REQ-F-028 |


## Data model

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

## Design notes

- OATM-BR-026: Input binding for account group: map blank or '*' to an explicit 'not supplied' value (null), otherwise keep the entered text as the proposed group.
- OATM-BR-027: Input binding for country code: map blank or '*' to null (not supplied), otherwise keep the entered value as the proposed country code.
- OATM-BR-028: Input binding for customer number once details are shown: blank or '*' becomes null; any other value is carried as the proposed value, compared with the snapshot and written to the customer record on save.
- OATM-BR-029: Input binding for government-issued ID once details are shown: blank or '*' becomes null; otherwise the entered value is the proposed ID, compared with the snapshot and written to the customer record on save.
- OATM-BR-030: Input binding for the five amounts (credit limit, cash credit limit, current balance, current cycle credit, current cycle debit): blank or '*' becomes null (not supplied) so validation can report it as missing.
- OATM-BR-031: A currency parser that accepts an optional '$', thousands commas, a sign and decimals, and yields a decimal amount at scale 2 (use a decimal type, not floating point); unparseable text stays as entered for validation to reject.
- OATM-BR-032: Input binding for open, expiry and reissue dates as separate year, month and day parts: each part that is blank or '*' becomes null, any other entry is kept exactly as typed for the date checks.
- OATM-BR-033: Input binding for date of birth parts (year, month, day): blank or '*' becomes null, otherwise the part is kept as the proposed value.

## Decision tables

#### Capture of each entered field

| Field | Entry is '*' or blank | Captured value | Rule |
|---|---|---|---|
| Account group | Yes | Not supplied | OATM-BR-026 |
| Account group | No | Entered group is the proposed group | OATM-BR-026 |
| Country code | Yes | Not supplied | OATM-BR-027 |
| Country code | No | Entered value is the proposed country code | OATM-BR-027 |
| Customer number | Yes | Not supplied | OATM-BR-028 |
| Customer number | No | Entered value is the proposed customer number | OATM-BR-028 |
| Government ID | Yes | Not supplied | OATM-BR-029 |
| Government ID | No | Entered value is the proposed government ID | OATM-BR-029 |
| Any of the five amounts | Yes | Not supplied | OATM-BR-030 |
| Any of the five amounts | No (valid currency number) | Converted to proposed amount with two decimal places | OATM-BR-031 |
| Open, expiry or reissue date part | Yes | Not supplied | OATM-BR-032 |
| Open, expiry or reissue date part | No | Taken as typed | OATM-BR-032 |
| Date of birth part | Yes | Not supplied | OATM-BR-033 |
| Date of birth part | No | Taken as the proposed value | OATM-BR-033 |
| Status, SSN, FICO score, names, address lines, city, state, ZIP, phones, EFT account, primary-holder flag | Yes / No | **Gap:** No rule says how '*' or blank entries are captured for these fields. | |
| Any of the five amounts | No (not a valid currency number) | **Gap:** No rule says what proposed amount is held when the entry is not a valid currency number (validation rejects it, see R43). | |

