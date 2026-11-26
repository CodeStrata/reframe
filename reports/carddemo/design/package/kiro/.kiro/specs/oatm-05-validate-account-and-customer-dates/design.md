# Design: Validate account and customer dates (OATM-C05)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Checks the open, expiry, reissue and birth dates part by part and then as real calendar dates whenever the operator changes account details. Each message names the date it concerns and only the first error is shown. Impossible dates such as 31 April, 30 February or 29 February in a non-leap year must never be saved.

Runs as online. Journeys: J02.

## Screens and components

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Open date | date |  | Year, month and day must all be supplied: 'Open Date : Year must be supplied.', 'Open Date : Month must be supplied.', 'Open Date : Day must be supplied.'. The year must be 4 digits: 'Open Date must be 4 digit number.', starting 19 or 20: 'Open Date : Century is not valid.'. 'Open Date: Month must be a number between 1 and 12.'; 'Open Date:day must be a number between 1 and 31.'; 'Open Date:Cannot have 31 days in this month.'; 'Open Date:Cannot have 30 days in this month.'; 'Open Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Open Date validation error ...'. |  | OATM-REQ-F-045, OATM-REQ-F-046 |
| Expiry date | date |  | Year, month and day must all be supplied: 'Expiry Date : Year must be supplied.', 'Expiry Date : Month must be supplied.', 'Expiry Date : Day must be supplied.'. The year must be 4 digits: 'Expiry Date must be 4 digit number.', starting 19 or 20: 'Expiry Date : Century is not valid.'. 'Expiry Date: Month must be a number between 1 and 12.'; 'Expiry Date:day must be a number between 1 and 31.'; 'Expiry Date:Cannot have 31 days in this month.'; 'Expiry Date:Cannot have 30 days in this month.'; 'Expiry Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Expiry Date validation error ...'. |  | OATM-REQ-F-045, OATM-REQ-F-046 |
| Reissue date | date |  | Year, month and day must all be supplied: 'Reissue Date : Year must be supplied.', 'Reissue Date : Month must be supplied.', 'Reissue Date : Day must be supplied.'. The year must be 4 digits: 'Reissue Date must be 4 digit number.', starting 19 or 20: 'Reissue Date : Century is not valid.'. 'Reissue Date: Month must be a number between 1 and 12.'; 'Reissue Date:day must be a number between 1 and 31.'; 'Reissue Date:Cannot have 31 days in this month.'; 'Reissue Date:Cannot have 30 days in this month.'; 'Reissue Date:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Reissue Date validation error ...'. |  | OATM-REQ-F-045, OATM-REQ-F-046 |
| Date of birth | date |  | Year, month and day must all be supplied: 'Date of Birth : Year must be supplied.', 'Date of Birth : Month must be supplied.', 'Date of Birth : Day must be supplied.'. The year must be 4 digits: 'Date of Birth must be 4 digit number.', starting 19 or 20: 'Date of Birth : Century is not valid.'. 'Date of Birth: Month must be a number between 1 and 12.'; 'Date of Birth:day must be a number between 1 and 31.'; 'Date of Birth:Cannot have 31 days in this month.'; 'Date of Birth:Cannot have 30 days in this month.'; 'Date of Birth:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Date of Birth validation error ...'. Must be before today: 'Date of Birth:cannot be in the future '. |  |  |


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
| OATM-BR-044 | Validate the four account and customer dates | business rule | WHEN the entered values differ from the stored account and are not awaiting or past confirmation, THE Account Update validation SHALL check the 'Open Date', 'Expiry Date', 'Reissue Date' and 'Date of Birth' in that order with the same date check, prefix each message with the date's name, and show only the first error message found. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-045 | Reject missing date year | business rule | WHEN the year of a date is blank, THE Date Validation SHALL reject the date with '<date name> : Year must be supplied.' and still go on to check the month and day. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-046 | Reject non-numeric date year | business rule | WHEN the year of a date is not a four-digit number, THE Date Validation SHALL reject the date with '<date name> must be 4 digit number.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-047 | Restrict date century to 19 or 20 | business rule | WHEN a numeric year does not start with 19 or 20, THE Date Validation SHALL reject the date with '<date name> : Century is not valid.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-048 | Reject missing date month | business rule | WHEN the month of a date is blank, THE Date Validation SHALL reject the date with '<date name> : Month must be supplied.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-049 | Reject month outside 1 to 12 | business rule | WHEN the month of a date is not a number from 1 to 12, THE Date Validation SHALL reject the date with '<date name>: Month must be a number between 1 and 12.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-050 | Reject missing date day | business rule | WHEN the day of a date is blank, THE Date Validation SHALL reject the date with '<date name> : Day must be supplied.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-051 | Reject non-numeric date day | business rule | WHEN the day of a date is not a number or is outside 1 to 31, THE Date Validation SHALL reject the date with '<date name>:day must be a number between 1 and 31.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-052 | Reject day 31 in short months | business rule | WHEN the day is 31 and the month is not 1, 3, 5, 7, 8, 10 or 12, THE Date Validation SHALL reject the date with '<date name>:Cannot have 31 days in this month.' and stop checking that date. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-053 | Reject day 30 in February | business rule | WHEN the date is 30 February, THE Date Validation SHALL reject it with '<date name>:Cannot have 30 days in this month.' and stop checking that date. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-054 | Reject February 29 in non-leap years | business rule | WHEN the date is 29 February and the year is not a leap year (a year ending in 00 must divide by 400, any other year by 4), THE Date Validation SHALL reject it with '<date name>:Not a leap year.Cannot have 29 days in this month.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-055 | Stop date check on prior failures | business rule | WHEN any of the year, month or day of a date has failed its check, THE Date Validation SHALL stop checking that date without the final date-service check. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-056 | Verify date with date utility | business rule | WHEN a date passes all the earlier checks, THE Date Validation SHALL confirm it with the date service (CSUTLDTC) in format 'YYYYMMDD', and SHALL reject it with '<date name> validation error Sev code: <severity> Message code: <message number>' if the service returns a non-zero severity. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-057 | Confirm date with date utility | error handling | WHEN the date service rejects a date, THE Date Validation SHALL still mark the date's year, month and day as valid afterwards, so only the error message and the screen's input-error state record the failure. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |

### Worked examples

- OATM-BR-044: Changes = none compared with stored data → No date is checked.
- OATM-BR-047: Expiry Date = 1999-12-31 → The year passes.
- OATM-BR-054: Open Date = 2024-02-29 → Accepted.
- OATM-BR-054: Open Date = 1900-02-29 → Rejected as not a leap year; 2000-02-29 is accepted.
- OATM-BR-055: Expiry Date = 2024-13-01 → The month error is raised and the date service is not called.
- OATM-BR-056: Open Date = 2024-02-29; Date service severity = 0 → The date is accepted.
- OATM-BR-057: Date of Birth = a date the date service rejects → The error message is set, but the date counts as valid, so the future-birth-date check still runs on it.

## Decision tables

#### Date part checks

| Year | Month | Day | Date check result | Rule |
|---|---|---|---|---|
| Blank | - | - | Reject '<date name> : Year must be supplied.'; continue checking month and day | OATM-BR-045 |
| Not a four-digit number | - | - | Reject '<date name> must be 4 digit number.' | OATM-BR-046 |
| Numeric, not starting 19 or 20 | - | - | Reject '<date name> : Century is not valid.' | OATM-BR-047 |
| - | Blank | - | Reject '<date name> : Month must be supplied.' | OATM-BR-048 |
| - | Not a number 1 to 12 | - | Reject '<date name>: Month must be a number between 1 and 12.' | OATM-BR-049 |
| - | - | Blank | Reject '<date name> : Day must be supplied.' | OATM-BR-050 |
| - | - | Not a number or outside 1 to 31 | Reject '<date name>:day must be a number between 1 and 31.' | OATM-BR-051 |
| - | Not 1, 3, 5, 7, 8, 10 or 12 | 31 | Reject '<date name>:Cannot have 31 days in this month.'; stop | OATM-BR-052 |
| - | 2 | 30 | Reject '<date name>:Cannot have 30 days in this month.'; stop | OATM-BR-053 |
| Not a leap year | 2 | 29 | Reject '<date name>:Not a leap year.Cannot have 29 days in this month.' | OATM-BR-054 |
| Any part failed | Any part failed | Any part failed | Stop checking; no date-service check | OATM-BR-055 |
| Valid | Valid | Valid | Confirm with date service (CSUTLDTC); reject on non-zero severity | OATM-BR-056 |
| Not a four-digit number / not 19 or 20 | - | - | **Gap:** R53 says checking continues after a blank year; no rule says whether month and day are still checked after the other year, month or day failures. | |
| - | - | - | **Gap:** The extra date-of-birth check named in R10 is not described by any rule. | |


## Design notes

None.

## Open questions

- SME-059: When the date-checking utility rejects a date, the date is still marked valid even though an input error is raised. Should a rejected date stay invalid, including for later checks such as 'date of birth cannot be in the future'? (Account servicing business owner) On OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056, OATM-BR-057, OATM-BR-044, OATM-BR-045, OATM-BR-046, OATM-BR-047, OATM-BR-048, OATM-BR-049, OATM-BR-050, OATM-BR-051.
- SME-060: Should date validation check that the month is numeric before checking that it is between 1 and 12? (Account servicing business owner) On OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056, OATM-BR-057, OATM-BR-045, OATM-BR-046, OATM-BR-047, OATM-BR-048, OATM-BR-049, OATM-BR-050, OATM-BR-051.
- SME-061: Only years in the 1900s and 2000s are accepted for all four account and customer dates. Should this restriction still apply to card expiry and reissue dates? (Account servicing business owner) On OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056, OATM-BR-057, OATM-BR-045, OATM-BR-046, OATM-BR-047, OATM-BR-048, OATM-BR-049, OATM-BR-050, OATM-BR-051.
- SME-065: When a date's year fails validation, should the whole date check stop, or should the month and day still be checked? (Business analyst) On OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056, OATM-BR-057, OATM-BR-044, OATM-BR-047, OATM-BR-049, OATM-BR-051.
- DEF-036: Is this intended? When the date service returns a non-zero severity, the check jumps to the end of the final-check paragraph (EDIT-DATE-LE-EXIT). It then runs on into the statement that marks the whole date valid (WS-EDIT-DATE-IS-VALID). The rejected date's year, month and day flags are therefore reset to valid, the field is not marked as in error, and for Date of Birth the future-date check still runs. The input-error state and the message do stay set. (Subject-matter expert) On OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056, OATM-BR-057, OATM-BR-044, OATM-BR-045, OATM-BR-046, OATM-BR-047, OATM-BR-048, OATM-BR-049, OATM-BR-050, OATM-BR-051.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (18 in all).