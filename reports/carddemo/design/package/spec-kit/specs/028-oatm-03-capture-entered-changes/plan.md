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

### Account (S-ACCOUNT-VIEW)

Look up an account by account number or card number and show its status, balances, limits and dates beside the customer profile on one screen, while the caller waits. Tab order: search, the cards, then Update account.

Prototype: `ui-reference/index.html#/S-ACCOUNT-VIEW`. Replaces the legacy screens CACTVWA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Update account (S-ACCOUNT-EDIT)

Change an account's and its customer's details after confirming the caller. Each field is checked as it is left and again on save; every failing field shows its own message and a summary lists them all. Save asks for confirmation, listing each change from old to new value. Tab order: account and status, dates, amounts, customer identity, name and address, contact, then Save changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Status and group | **summary card** | Account status as a choice of Active or Inactive (stored Y/N); Account group (optional, up to 10 characters) | Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values. |  | OATM-REQ-F-025 |
| Account dates | **summary card** | Opened, Expiry and Reissue dates, each as labelled Day, Month and Year inputs | For each date, in the rule's words: '<date> : Year must be supplied.', '<date> must be 4 digit number.', '<date> : Century is not valid.' (year must start 19 or 20), '<date> : Month must be supplied.', '<date>: Month must be a number between 1 and 12.', '<date> : Day must be supplied.', '<date>:day must be a number between 1 and 31.', '<date>:Cannot have 31 days in this month.', '<date>:Cannot have 30 days in this month.', '<date>:Not a leap year.Cannot have 29 days in this month.', and a final calendar check '<date> validation error'. The message sits under the part to fix. |  | OATM-REQ-F-031 |
| Limits and balances | **summary card** | Credit limit, Cash credit limit, Current balance, Current cycle credit, Current cycle debit; money inputs, right-aligned, two decimals, $ and commas accepted | Each amount is required: '<field> must be supplied.' (e.g. 'Credit Limit must be supplied.'), and must be a currency number: '<field> is not valid' - enter an amount such as 1,250.00. Negative values and zero are accepted. |  | OATM-REQ-F-029, OATM-REQ-F-030 |
| Customer identity | **summary card** | Customer ID (read-only); SSN as three labelled parts (3-2-4); Date of birth as Day, Month, Year; FICO score; Government-issued ID (optional) | SSN: 'SSN: First 3 chars must be supplied.', 'SSN: First 3 chars must be all numeric.', 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'; the 4th & 5th and last 4 characters must each be supplied, all numeric and non-zero. Date of birth: the date checks above, and 'Date of Birth:cannot be in the future '. FICO: 'FICO Score must be supplied.', 'FICO Score must be all numeric.', 'FICO Score must not be zero.', 'FICO Score: should be between 300 and 850'. |  | OATM-REQ-F-027, OATM-REQ-F-028, OATM-REQ-F-032 |
| Name and address | **summary card** | First name, Middle name (optional), Last name; Address line 1, Address line 2 (optional); City; State (a choice of US state codes); ZIP; Country | '<field> must be supplied.' for First Name, Last Name, City, State, Country and Address Line 1; '<field> can have alphabets only.' for names, city, state and country; 'Middle Name can have alphabets only.'; 'State: is not a valid state code'; ZIP: 'ZIP must be supplied.', must be all numeric, 5 digits and not zero; 'Invalid zip code for state' - check the state and ZIP together. |  | OATM-REQ-F-026 |


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

- OATM-BR-026: Model the proposed account group as an optional value: blank or '*' input becomes 'absent' (null), not an empty string. Any other input becomes the proposed group.
- OATM-BR-027: Treat blank or '*' country code input as absent (null). Otherwise take the entered value as the proposed country code.
- OATM-BR-028: Treat a blank or '*' customer number as absent (null); otherwise it is the proposed value. Change detection compares it with the stored customer number, and it is written to the customer record on save.
- OATM-BR-029: Treat a blank or '*' government-issued ID as absent (null); otherwise it is the proposed value. Change detection compares it with the stored ID, and it is written to the customer record on save.
- OATM-BR-030: Hold each of the five amounts as an optional input: credit limit, cash credit limit, current balance, current cycle credit and current cycle debit. Blank or '*' means absent, which validation then reports as 'must be supplied.'.
- OATM-BR-031: Parse entered amounts with a currency parser that accepts an optional '$', thousands commas, a sign and decimals. Convert to an exact decimal with two places (a decimal type, never floating point). Input that does not parse stays as entered text so validation can report it as not valid.
- OATM-BR-032: Capture the open, expiry and reissue dates as three separate optional parts (year, month, day). A blank or '*' part is absent; any other part is kept exactly as typed so date validation can check it.
- OATM-BR-033: Capture the date of birth as three separate optional parts (year, month, day). A blank or '*' part is absent; any other part is kept as typed for validation.

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

