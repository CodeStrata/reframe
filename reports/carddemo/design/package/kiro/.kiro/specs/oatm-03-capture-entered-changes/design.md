# Design: Capture entered changes (OATM-C03)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Captures what the operator typed on the Update account screen as proposed new values, treating any field left blank or entered as '*' as not supplied. Amounts entered in currency form are converted to numbers with two decimals. It must never mistake a blank or '*' for a real value to compare or save.

Runs as online. Journeys: J02.

## Screens and components

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
| OATM-BR-026 | Stage entered account group | design note | WHEN the operator submits changes and the account group entry is '*' or blank, THE Account Update entry capture SHALL treat the group as not supplied (ACUP-NEW-GROUP-ID set to low-values); otherwise it SHALL take the entered group as the proposed group. | medium | app/cbl/COACTUPC.cbl:1211-1218, app/cbl/COACTUPC.cbl:1056-1062 |
| OATM-BR-027 | Stage country code entry | design note | WHEN the operator submits changes and the country code entry is '*' or blank, THE Account Update entry capture SHALL treat the country code as not supplied; otherwise it SHALL take the entered value as the proposed country code. | medium | app/cbl/COACTUPC.cbl:1343-1348 |
| OATM-BR-028 | Stage customer identifier entry | design note | WHEN account details are already on the update screen and the operator submits the customer number field as '*' or blank, THE account update screen SHALL treat the customer number as not supplied (low-values); otherwise it SHALL take the entered customer number as the proposed value, which is compared with the stored one and written to the customer record on save. | medium | app/cbl/COACTUPC.cbl:1220-1229, app/cbl/COACTUPC.cbl:1060-1062, app/cbl/COACTUPC.cbl:1708-1711, app/cbl/COACTUPC.cbl:4009 |
| OATM-BR-029 | Stage government identifier entry | design note | WHEN account details are already on the update screen and the operator submits the government-issued ID field as '*' or blank, THE account update screen SHALL treat the government ID as not supplied (low-values); otherwise it SHALL take the entered value as the proposed government ID, which is compared with the stored one and written to the customer record on save. | medium | app/cbl/COACTUPC.cbl:1399-1406, app/cbl/COACTUPC.cbl:1060-1062, app/cbl/COACTUPC.cbl:1755-1758, app/cbl/COACTUPC.cbl:4045-4046 |
| OATM-BR-030 | Stage entered credit limit amount | design note | WHEN the operator submits changes to a fetched account and any of the five amount fields (credit limit, cash credit limit, current balance, current cycle credit, current cycle debit) is blank or '*', THE Account Update screen SHALL treat that amount as not supplied. | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-031 | Convert entered credit limit | design note | WHEN an entered amount reads as a valid currency number (an optional '$', thousands commas, a sign and decimals allowed), THE Account Update screen SHALL convert it to the proposed new numeric amount, with two decimal places. | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-032 | Stage entered account open date | design note | WHEN the operator submits the account update screen after the account details are shown, THE Account Update screen SHALL treat each year, month or day part of the open, expiry and reissue dates entered as '*' or left blank as not supplied, and take any other entry as typed. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-033 | Stage date of birth parts | design note | WHEN the operator enters a date of birth part as '*' or leaves it blank, THE account update screen SHALL treat that part (year, month or day) as not supplied; otherwise it SHALL take the entered part as the proposed value. | high | app/cbl/COACTUPC.cbl:1254-1275, app/cbl/COACTUPC.cbl:1533-1543, app/cpy/CSUTLDPY.cpy:341-370 |

### Worked examples

- OATM-BR-026: account group = '*' → Proposed group is not supplied
- OATM-BR-026: account group = GOLD → Proposed group is GOLD
- OATM-BR-027: country code = (blank) → Country code not supplied, so the later required-field check fails
- OATM-BR-027: country code = USA → Proposed country code USA
- OATM-BR-028: Account details shown = yes; Customer number entered = * → The proposed customer number is set to not supplied (low-values)
- OATM-BR-028: Account details shown = yes; Customer number entered = 000000123 → The proposed customer number is 000000123
- OATM-BR-028: Account details shown = no (only the account number was entered); Customer number entered = 000000123 → The customer number is not staged; only the account number is read
- OATM-BR-029: Account details shown = yes; Government ID entered = (blank) → The proposed government ID is set to not supplied (low-values)
- OATM-BR-030: Credit limit entered = * → Credit limit is treated as not supplied
- OATM-BR-030: Cycle debit entered = (blank) → Cycle debit is treated as not supplied
- OATM-BR-031: Credit limit entered = $5,000.00 → Proposed credit limit is 5000.00
- OATM-BR-031: Current balance entered = -250.5 → Proposed current balance is -250.50
- OATM-BR-032: Expiry month entry = 05 → The expiry month is taken as 05.
- OATM-BR-033: Date of birth year = * → The year is treated as not supplied and fails the date check.
- OATM-BR-033: Date of birth year = 1980; Month = 05; Day = 14 → 1980-05-14 is taken as the proposed date of birth.

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


## Design notes

- OATM-BR-026: Input binding for account group: map blank or '*' to an explicit 'not supplied' value (null), otherwise keep the entered text as the proposed group.
- OATM-BR-027: Input binding for country code: map blank or '*' to null (not supplied), otherwise keep the entered value as the proposed country code.
- OATM-BR-028: Input binding for customer number once details are shown: blank or '*' becomes null; any other value is carried as the proposed value, compared with the snapshot and written to the customer record on save.
- OATM-BR-029: Input binding for government-issued ID once details are shown: blank or '*' becomes null; otherwise the entered value is the proposed ID, compared with the snapshot and written to the customer record on save.
- OATM-BR-030: Input binding for the five amounts (credit limit, cash credit limit, current balance, current cycle credit, current cycle debit): blank or '*' becomes null (not supplied) so validation can report it as missing.
- OATM-BR-031: A currency parser that accepts an optional '$', thousands commas, a sign and decimals, and yields a decimal amount at scale 2 (use a decimal type, not floating point); unparseable text stays as entered for validation to reject.
- OATM-BR-032: Input binding for open, expiry and reissue dates as separate year, month and day parts: each part that is blank or '*' becomes null, any other entry is kept exactly as typed for the date checks.
- OATM-BR-033: Input binding for date of birth parts (year, month, day): blank or '*' becomes null, otherwise the part is kept as the proposed value.

## Open questions

- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-026, OATM-BR-027, OATM-BR-028, OATM-BR-029, OATM-BR-031, OATM-BR-032, OATM-BR-033.
- DEF-011: Confirm this is deliberate: The amount check accepts any signed currency number, so a negative or zero credit limit, cash credit limit or cycle amount passes validation and can be saved. (Subject-matter expert) On OATM-BR-031.
- DEF-036: Is this intended? When the date service returns a non-zero severity, the check jumps to the end of the final-check paragraph (EDIT-DATE-LE-EXIT). It then runs on into the statement that marks the whole date valid (WS-EDIT-DATE-IS-VALID). The rejected date's year, month and day flags are therefore reset to valid, the field is not marked as in error, and for Date of Birth the future-date check still runs. The input-error state and the message do stay set. (Subject-matter expert) On OATM-BR-032.
- DEF-037: Is this intended? A date of birth equal to today is rejected with a message saying it is in the future, which it is not. (Subject-matter expert) On OATM-BR-033.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).