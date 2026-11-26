# Capture entered changes (OATM-C03)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Takes what the operator typed on the update screen and turns it into proposed new values for the account and customer. A blank or '*' entry means 'not supplied', never a value to save. Amounts typed as currency (with '$', commas, sign or decimals) are converted to numbers with two decimal places. It must never confuse 'left blank' with a real value, and must never lose or round an entered amount wrongly.

**User story:** As an operator, I want the values I type to be captured as proposed changes, with blank or '*' entries treated as not supplied, so that the system knows exactly what I intend to change.

## Requirements

### Requirement 1: OATM-REQ-F-025 (design note)

#### Acceptance criteria

1. When the operator submits changes and the account group entry is '*' or blank, the system shall treat the group as not supplied, and otherwise take the entered group as the proposed group. (rules OATM-BR-026)
2. GIVEN account group: '*' WHEN the operator submits changes and the account group entry is '*' or blank THEN Proposed group is not supplied (OATM-C03-AC-01; OATM-BR-026)
3. GIVEN account group: GOLD WHEN the operator submits changes and the account group entry is '*' or blank THEN Proposed group is GOLD (OATM-C03-AC-02; OATM-BR-026)

### Requirement 2: OATM-REQ-F-026 (design note)

#### Acceptance criteria

1. When the operator submits changes and the country code entry is '*' or blank, the system shall treat the country code as not supplied, and otherwise take the entered value as the proposed country code. (rules OATM-BR-027)
2. GIVEN country code: (blank) WHEN the operator submits changes and the country code entry is '*' or blank THEN Country code not supplied, so the later required-field check fails (OATM-C03-AC-03; OATM-BR-027)
3. GIVEN country code: USA WHEN the operator submits changes and the country code entry is '*' or blank THEN Proposed country code USA (OATM-C03-AC-04; OATM-BR-027)

### Requirement 3: OATM-REQ-F-027 (design note)

#### Acceptance criteria

1. When account details are already on the update screen and the operator submits the customer number field as '*' or blank, the system shall treat the customer number as not supplied, and otherwise take the entered customer number as the proposed value to compare with the stored one and write to the customer record on save. (rules OATM-BR-028)
2. GIVEN Account details shown: yes; Customer number entered: * WHEN account details are already on the update screen and the operator submits the customer number field as '*' or blank THEN The proposed customer number is set to not supplied (low-values) (OATM-C03-AC-05; OATM-BR-028)
3. GIVEN Account details shown: yes; Customer number entered: 000000123 WHEN account details are already on the update screen and the operator submits the customer number field as '*' or blank THEN The proposed customer number is 000000123 (OATM-C03-AC-06; OATM-BR-028)
4. GIVEN Account details shown: no (only the account number was entered); Customer number entered: 000000123 WHEN account details are already on the update screen and the operator submits the customer number field as '*' or blank THEN The customer number is not staged; only the account number is read (OATM-C03-AC-07; OATM-BR-028)

### Requirement 4: OATM-REQ-F-028 (design note)

#### Acceptance criteria

1. When account details are already on the update screen and the operator submits the government-issued ID field as '*' or blank, the system shall treat the government ID as not supplied, and otherwise take the entered value as the proposed government ID to compare with the stored one and write to the customer record on save. (rules OATM-BR-029)
2. GIVEN Account details shown: yes; Government ID entered: (blank) WHEN account details are already on the update screen and the operator submits the government-issued ID field as '*' or blank THEN The proposed government ID is set to not supplied (low-values) (OATM-C03-AC-08; OATM-BR-029)

### Requirement 5: OATM-REQ-F-029 (design note)

#### Acceptance criteria

1. When the operator submits changes to a fetched account and any of the credit limit, cash credit limit, current balance, current cycle credit or current cycle debit is blank or '*', the system shall treat that amount as not supplied. (rules OATM-BR-030)
2. GIVEN Credit limit entered: * WHEN the operator submits changes to a fetched account and any of the five amount fields (credit limit, cash credit limit, current balance, current cycle credit, current cycle debit) is blank or '*' THEN Credit limit is treated as not supplied (OATM-C03-AC-09; OATM-BR-030)
3. GIVEN Cycle debit entered: (blank) WHEN the operator submits changes to a fetched account and any of the five amount fields (credit limit, cash credit limit, current balance, current cycle credit, current cycle debit) is blank or '*' THEN Cycle debit is treated as not supplied (OATM-C03-AC-10; OATM-BR-030)

### Requirement 6: OATM-REQ-F-030 (design note)

#### Acceptance criteria

1. When an entered amount reads as a valid currency number (an optional '$', thousands commas, a sign and decimals allowed), the system shall convert it to the proposed new numeric amount with two decimal places. (rules OATM-BR-031)
2. GIVEN Credit limit entered: $5,000.00 WHEN an entered amount reads as a valid currency number (an optional '$', thousands commas, a sign and decimals allowed) THEN Proposed credit limit is 5000.00 (OATM-C03-AC-11; OATM-BR-031)
3. GIVEN Current balance entered: -250.5 WHEN an entered amount reads as a valid currency number (an optional '$', thousands commas, a sign and decimals allowed) THEN Proposed current balance is -250.50 (OATM-C03-AC-12; OATM-BR-031)

### Requirement 7: OATM-REQ-F-031 (design note)

#### Acceptance criteria

1. When the operator submits the account update screen after the account details are shown, the system shall treat each year, month or day part of the open, expiry and reissue dates entered as '*' or left blank as not supplied, and take any other entry as typed. (rules OATM-BR-032)
2. GIVEN Expiry month entry: 05 WHEN the operator submits the account update screen after the account details are shown THEN The expiry month is taken as 05. (OATM-C03-AC-13; OATM-BR-032)

### Requirement 8: OATM-REQ-F-032 (design note)

#### Acceptance criteria

1. When the operator enters a date of birth part (year, month or day) as '*' or leaves it blank, the system shall treat that part as not supplied, and otherwise take the entered part as the proposed value. (rules OATM-BR-033)
2. GIVEN Date of birth year: * WHEN the operator enters a date of birth part as '*' or leaves it blank THEN The year is treated as not supplied and fails the date check. (OATM-C03-AC-14; OATM-BR-033)
3. GIVEN Date of birth year: 1980; Month: 05; Day: 14 WHEN the operator enters a date of birth part as '*' or leaves it blank THEN 1980-05-14 is taken as the proposed date of birth. (OATM-C03-AC-15; OATM-BR-033)

## Screens and components

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

- OATM-BR-026: Model the proposed account group as an optional value: blank or '*' input becomes 'absent' (null), not an empty string. Any other input becomes the proposed group.
- OATM-BR-027: Treat blank or '*' country code input as absent (null). Otherwise take the entered value as the proposed country code.
- OATM-BR-028: Treat a blank or '*' customer number as absent (null); otherwise it is the proposed value. Change detection compares it with the stored customer number, and it is written to the customer record on save.
- OATM-BR-029: Treat a blank or '*' government-issued ID as absent (null); otherwise it is the proposed value. Change detection compares it with the stored ID, and it is written to the customer record on save.
- OATM-BR-030: Hold each of the five amounts as an optional input: credit limit, cash credit limit, current balance, current cycle credit and current cycle debit. Blank or '*' means absent, which validation then reports as 'must be supplied.'.
- OATM-BR-031: Parse entered amounts with a currency parser that accepts an optional '$', thousands commas, a sign and decimals. Convert to an exact decimal with two places (a decimal type, never floating point). Input that does not parse stays as entered text so validation can report it as not valid.
- OATM-BR-032: Capture the open, expiry and reissue dates as three separate optional parts (year, month, day). A blank or '*' part is absent; any other part is kept exactly as typed so date validation can check it.
- OATM-BR-033: Capture the date of birth as three separate optional parts (year, month, day). A blank or '*' part is absent; any other part is kept as typed for validation.

## Open questions

- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-026, OATM-BR-027, OATM-BR-028, OATM-BR-029, OATM-BR-031, OATM-BR-032, OATM-BR-033.
- DEF-011: Confirm this is deliberate: The amount check accepts any signed currency number, so a negative or zero credit limit, cash credit limit or cycle amount passes validation and can be saved. (Subject-matter expert) On OATM-BR-031.
- DEF-036: Is this intended? When the date service returns a non-zero severity, the check jumps to the end of the final-check paragraph (EDIT-DATE-LE-EXIT). It then runs on into the statement that marks the whole date valid (WS-EDIT-DATE-IS-VALID). The rejected date's year, month and day flags are therefore reset to valid, the field is not marked as in error, and for Date of Birth the future-date check still runs. The input-error state and the message do stay set. (Subject-matter expert) On OATM-BR-032.
- DEF-037: Is this intended? A date of birth equal to today is rejected with a message saying it is in the future, which it is not. (Subject-matter expert) On OATM-BR-033.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).
