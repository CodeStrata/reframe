# Design: Validate changed account and customer fields (OATM-C04)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Checks every account and customer field once the operator has changed a fetched account, and only moves the update to awaiting confirmation when all checks pass. Amounts must be present and valid currency numbers but may be negative or zero. It must never let an invalid field through to confirmation, and shows only the first error found.

Runs as online. Journeys: J02.

## Screens and components

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Fix these fields | message | A summary listing every field in error, each linking to its field, in screen order; focus moves to the summary. Each field also shows its own message (the 3270 screen showed only the first message). |  |  | OATM-REQ-F-033 |
| Account status | radio | Active (Y) / Inactive (N) | Required: 'Account Status must be supplied.'; only Active or Inactive: 'Account Status must be Y or N.' |  | OATM-REQ-F-034 |
| Open date | date |  | Year, month and day must all be supplied: 'Open Date : Year must be supplied.', 'Open Date : Month must be supplied.', 'Open Date : Day must be supplied.'. The year must be 4 digits: 'Open Date must be 4 digit number.', starting 19 or 20: 'Open Date : Century is not valid.'. 'Open Date: Month must be a number between 1 and 12.'; 'Open Date:day must be a number between 1 and 31.'; 'Open Date:Cannot have 31 days in this month.'; 'Open Date:Cannot have 30 days in this month.'; 'Open Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Open Date validation error ...'. |  | OATM-REQ-F-035 |
| Expiry date | date |  | Year, month and day must all be supplied: 'Expiry Date : Year must be supplied.', 'Expiry Date : Month must be supplied.', 'Expiry Date : Day must be supplied.'. The year must be 4 digits: 'Expiry Date must be 4 digit number.', starting 19 or 20: 'Expiry Date : Century is not valid.'. 'Expiry Date: Month must be a number between 1 and 12.'; 'Expiry Date:day must be a number between 1 and 31.'; 'Expiry Date:Cannot have 31 days in this month.'; 'Expiry Date:Cannot have 30 days in this month.'; 'Expiry Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Expiry Date validation error ...'. |  | OATM-REQ-F-035 |
| Reissue date | date |  | Year, month and day must all be supplied: 'Reissue Date : Year must be supplied.', 'Reissue Date : Month must be supplied.', 'Reissue Date : Day must be supplied.'. The year must be 4 digits: 'Reissue Date must be 4 digit number.', starting 19 or 20: 'Reissue Date : Century is not valid.'. 'Reissue Date: Month must be a number between 1 and 12.'; 'Reissue Date:day must be a number between 1 and 31.'; 'Reissue Date:Cannot have 31 days in this month.'; 'Reissue Date:Cannot have 30 days in this month.'; 'Reissue Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Reissue Date validation error ...'. |  | OATM-REQ-F-035 |
| Credit limit | money |  | Required: 'Credit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Credit Limit is not valid'; negative and zero amounts are accepted. |  | OATM-REQ-F-036 |
| Cash credit limit | money |  | Required: 'Cash Credit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Cash Credit Limit is not valid'; negative and zero amounts are accepted. |  | OATM-REQ-F-036 |
| Current balance | money |  | Required: 'Current Balance must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Current Balance is not valid'; negative and zero amounts are accepted. |  | OATM-REQ-F-036 |
| Current cycle credit | money |  | Required: 'Current Cycle Credit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Current Cycle Credit Limit is not valid'; negative and zero amounts are accepted. |  | OATM-REQ-F-036 |
| Current cycle debit | money |  | Required: 'Current Cycle Debit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Current Cycle Debit Limit is not valid'; negative and zero amounts are accepted. |  | OATM-REQ-F-036 |
| First name | text |  | Required: 'First Name must be supplied.'; letters and spaces only: 'First Name can have alphabets only.'. |  | OATM-REQ-F-042 |
| Middle name (optional) | text |  | Optional; letters and spaces only: 'Middle Name can have alphabets only.'. |  | OATM-REQ-F-042 |
| Last name | text |  | Required: 'Last Name must be supplied.'; letters and spaces only: 'Last Name can have alphabets only.'. |  | OATM-REQ-F-042 |
| Social Security number | text | One field, formatted NNN-NN-NNNN as typed | First 3 digits must be supplied, numeric and not zero: 'SSN: First 3 chars must be supplied.' / 'SSN: First 3 chars must be all numeric.' / 'SSN: First 3 chars must not be zero.'; and not 666 or 900-999: 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'. The 4th-5th digits and the last 4 digits must each be supplied, numeric and not zero (messages 'SSN 4th & 5th chars ...' and 'SSN Last 4 chars ...'). |  | OATM-REQ-F-040 |
| Date of birth | date |  | Year, month and day must all be supplied: 'Date of Birth : Year must be supplied.', 'Date of Birth : Month must be supplied.', 'Date of Birth : Day must be supplied.'. The year must be 4 digits: 'Date of Birth must be 4 digit number.', starting 19 or 20: 'Date of Birth : Century is not valid.'. 'Date of Birth: Month must be a number between 1 and 12.'; 'Date of Birth:day must be a number between 1 and 31.'; 'Date of Birth:Cannot have 31 days in this month.'; 'Date of Birth:Cannot have 30 days in this month.'; 'Date of Birth:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Date of Birth validation error ...'. Must be before today: 'Date of Birth:cannot be in the future '. |  | OATM-REQ-F-035 |
| FICO score | number |  | Required: 'FICO Score must be supplied.'; 3 digits: 'FICO Score must be all numeric.'; not zero: 'FICO Score must not be zero.'; 300 to 850 inclusive: 'FICO Score: should be between 300 and 850'. |  | OATM-REQ-F-041 |
| Primary card holder | radio | Yes (Y) / No (N) | Required: 'Primary Card Holder must be supplied.'; only Yes or No: 'Primary Card Holder must be Y or N.' |  | OATM-REQ-F-034 |
| City | text |  | Required: 'City must be supplied.'; letters and spaces only: 'City can have alphabets only.'. |  | OATM-REQ-F-042 |
| State | select | US state codes | Required: 'State must be supplied.'; letters and spaces only: 'State can have alphabets only.'. Must be a US state code: 'State: is not a valid state code'; must match the ZIP code: 'Invalid zip code for state'. |  | OATM-REQ-F-043 |
| Check changes | button | Checks every changed field; when all pass, opens the save confirmation |  |  | OATM-REQ-F-044 |


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
| OATM-BR-034 | Validate each changed account field | business rule | WHEN account details have been fetched and the entered values differ from the fetched ones, and the changes are not already validated or saved, THE Account Update validation SHALL check every account and customer field and mark the changes not OK ('E') until all checks pass. | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |
| OATM-BR-035 | Validate account status, dates and amounts | business rule | WHEN the operator has changed a fetched account and the changes are not yet confirmed, THE Account Update validation SHALL mark the changes as not OK ('E') and check the account status as Y/N, the open, expiry and reissue dates as calendar dates, and the five amounts as signed currency numbers. | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-036 | Validate each changed account field | business rule | THE Account Update validation SHALL require the account status and the primary card holder flag to be Y or N; the open, expiry, reissue and birth dates to be valid dates, with the birth date passing an extra date-of-birth check; and the credit limit, cash credit limit, current balance, cycle credit and cycle debit to be valid signed amounts. | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |
| OATM-BR-037 | Validate signed monetary amount | business rule | WHEN an amount is not supplied (blank or '*'), THE Account Update validation SHALL reject it with the message '<field> must be supplied.' (for example 'Credit Limit must be supplied.'). | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-038 | Validate signed monetary amount | business rule | WHEN a supplied amount is not a valid currency number, THE Account Update validation SHALL reject it with the message '<field> is not valid', using the names 'Credit Limit', 'Cash Credit Limit', 'Current Balance', 'Current Cycle Credit Limit' or 'Current Cycle Debit Limit'. | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-039 | Validate signed monetary amount | business rule | THE Account Update validation SHALL accept any valid currency number for the five amounts, including negative values and zero, without a range or sign check, and SHALL show only the first error message found on the screen. | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-040 | Validate each changed account field | business rule | THE Account Update validation SHALL reject an SSN whose first 3 digits are 000, 666 or 900-999 (': should not be 000, 666, or between 900 and 999'), and SHALL require the FICO score to be 3 digits between 300 and 850 (': should be between 300 and 850'). | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |
| OATM-BR-041 | Validate each changed account field | business rule | THE Account Update validation SHALL require the first and last names (25 characters), city (50) and country (3) to be letters only; allow the middle name (25) to be blank but letters only; and require address line 1 (50). | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |
| OATM-BR-042 | Validate each changed account field | business rule | THE Account Update validation SHALL require the state to be a valid 2-letter US state code (': is not a valid state code'), the ZIP to be 5 digits, the state and ZIP to match each other, both phone numbers to be valid US numbers, and the EFT account id to be 10 digits. | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |
| OATM-BR-043 | Validate each changed account field | business rule | WHEN all field checks pass, THE Account Update validation SHALL set the stage to changes validated but not confirmed ('N'). | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |

### Worked examples

- OATM-BR-034: changed field = credit limit 5000.00 to 7000.00 → All fields are checked; if any fail, the stage becomes 'E' and the screen asks for corrections
- OATM-BR-035: Changes made = credit limit changed from 5000.00 to 6000.00 → Status, open/expiry/reissue dates and all five amounts are checked before the change can be confirmed
- OATM-BR-035: Changes made = none → No field checks run
- OATM-BR-036: account status = X → Rejected; the account status must be Y or N
- OATM-BR-036: expiry date = 2025-13-01 → Rejected as an invalid date
- OATM-BR-039: Cash credit limit entered = -100 → Accepted as -100.00
- OATM-BR-039: Credit limit entered = 12a; Current balance entered = (blank) → Only 'Credit Limit is not valid' is shown
- OATM-BR-040: SSN = 666-12-3456 → Rejected with ': should not be 000, 666, or between 900 and 999'
- OATM-BR-040: FICO score = 900 → Rejected with ': should be between 300 and 850'
- OATM-BR-041: first name = J0hn → Rejected because the name contains a digit
- OATM-BR-041: middle name = (blank) → Accepted
- OATM-BR-042: state = ZZ → Rejected with ': is not a valid state code'
- OATM-BR-042: EFT account id = 12345 → Rejected because 10 digits are required
- OATM-BR-043: all changed fields = valid → Stage 'N'; the screen prompts 'Changes validated.Press F5 to save'

## Decision tables

#### Amount field validation

| Amount entry | Validation result | Rule |
|---|---|---|
| Not supplied (blank or '*') | Reject with '<field> must be supplied.' | OATM-BR-037 |
| Supplied, not a valid currency number | Reject with '<field> is not valid' | OATM-BR-038 |
| Valid currency number (including negative or zero) | Accept, no range or sign check | OATM-BR-039 |

#### Validation stage

| Entered values differ from fetched | Changes already validated or saved | All field checks pass | Update stage | Rule |
|---|---|---|---|---|
| Yes | No | No | Changes not OK ('E') | OATM-BR-034 |
| Yes | No | - | Mark not OK ('E') and check status, dates and five amounts | OATM-BR-035 |
| Yes | No | Yes | Changes validated but not confirmed ('N') | OATM-BR-043 |
| No | No | - | **Gap:** No rule says what happens when the operator submits without changing any value. | |


## Design notes

None.

## Open questions

- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-038.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-038.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-038.
- DEF-011: Confirm this is deliberate: The amount check accepts any signed currency number, so a negative or zero credit limit, cash credit limit or cycle amount passes validation and can be saved. (Subject-matter expert) On OATM-BR-035, OATM-BR-038, OATM-BR-039.
- DEF-113: Confirm this is deliberate: The SSN middle and last parts, the government id and address line 2 get no content check beyond the SSN edit, and address line 2 is deliberately left optional. (Subject-matter expert) On OATM-BR-043.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (18 in all).