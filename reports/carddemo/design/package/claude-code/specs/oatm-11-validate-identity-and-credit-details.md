# Validate identity and credit details (OATM-C11)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Checks the customer's Social Security Number, date of birth and FICO credit score when the operator changes customer details. The SSN must have valid, non-zero parts and must not start with 000, 666 or 900-999. The date of birth must be in the past. The FICO score must be three digits between 300 and 850. Implausible identity or credit data must never be saved.

**User story:** As an operator, I want the SSN, date of birth and FICO score checked when I change customer details, so that only plausible identity and credit data is saved.

## Requirements

### Requirement 1: OATM-REQ-F-095 (design note)

#### Acceptance criteria

1. When the operator enters a Social Security Number part as '*' or leaves it blank, the system shall treat that part as not supplied, and otherwise take the entered part as the proposed value. (rules OATM-BR-098)
2. GIVEN an account is shown for update with the stored SSN 123-45-6789 WHEN the operator enters '*' in the first SSN part, leaves the 4th-5th part blank, enters '6789' as the last part, and submits THEN the first and 4th-5th parts are treated as not supplied and the last part '6789' is taken as the proposed value (OATM-C11-AC-06; OATM-BR-098)

### Requirement 2: OATM-REQ-F-096 (business rule)

#### Acceptance criteria

1. If the first three SSN characters are blank, not all numeric or zero, then the system shall reject them with 'SSN: First 3 chars must be supplied.', 'SSN: First 3 chars must be all numeric.' or 'SSN: First 3 chars must not be zero.' respectively, and shall not check the other two SSN parts. (rules OATM-BR-099, OATM-BR-100)
2. GIVEN Date of birth: 1985-04-12 WHEN changed details are checked THEN Accepted (OATM-C11-AC-01; OATM-BR-100)

### Requirement 3: OATM-REQ-F-097 (business rule)

#### Acceptance criteria

1. If the first three SSN characters are numeric and equal 666 or fall between 900 and 999, then the system shall reject them with 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'. (rules OATM-BR-101)
2. GIVEN SSN: 912-12-3456 WHEN the first three SSN characters are numeric and equal 666 or fall between 900 and 999 THEN Rejected with the same message. (OATM-C11-AC-02; OATM-BR-101)
3. GIVEN SSN: 123-45-6789 WHEN the first three SSN characters are numeric and equal 666 or fall between 900 and 999 THEN Accepted. (OATM-C11-AC-03; OATM-BR-101)

### Requirement 4: OATM-REQ-F-098 (business rule)

#### Acceptance criteria

1. When the first three SSN characters are numeric and non-zero, the system shall require the 4th-5th characters and the last 4 characters each to be supplied, all numeric and non-zero, giving 'SSN 4th & 5th chars …' or 'SSN Last 4 chars …' with 'must be supplied.', 'must be all numeric.' or 'must not be zero.'. (rules OATM-BR-102)
2. GIVEN an account is shown for update with changes and the first three SSN characters are '123' WHEN the operator leaves the SSN 4th and 5th characters blank and submits THEN the input is rejected with a message that starts 'SSN 4th & 5th chars' and ends 'must be supplied.' (OATM-C11-AC-07; OATM-BR-102)
3. GIVEN an account is shown for update with changes and the first three SSN characters are '123' WHEN the operator enters '45' as the 4th-5th characters and '12A4' as the last 4 characters, and submits THEN the input is rejected with a message that starts 'SSN Last 4 chars' and ends 'must be all numeric.' (OATM-C11-AC-08; OATM-BR-102)
4. GIVEN an account is shown for update with changes and the first three SSN characters are '123' WHEN the operator enters '00' as the 4th-5th characters and submits THEN the input is rejected with a message that starts 'SSN 4th & 5th chars' and ends 'must not be zero.' (OATM-C11-AC-09; OATM-BR-102)

### Requirement 5: OATM-REQ-F-099 (business rule)

#### Acceptance criteria

1. If a valid calendar date of birth is today or later, then the system shall reject it, flag the day, month and year fields, and show 'Date of Birth:cannot be in the future ' if no earlier error message is already set. (rules OATM-BR-103, OATM-BR-100)
2. GIVEN Date of birth: 1985-04-12 WHEN changed details are checked THEN Accepted (OATM-C11-AC-01; OATM-BR-100)
3. GIVEN Today: 2026-11-23; Date of birth: 1980-05-14 WHEN a valid calendar date of birth is today or later THEN Accepted. (OATM-C11-AC-04; OATM-BR-103)

### Requirement 6: OATM-REQ-F-100 (business rule)

#### Acceptance criteria

1. If the FICO score is entered as blank or '*', then the system shall treat it as not supplied and reject it with 'FICO Score must be supplied.'. (rules OATM-BR-104)
2. GIVEN an account is shown for update with changes WHEN the operator clears the FICO score (or enters '*') and submits THEN the FICO score is treated as not supplied and the input is rejected with 'FICO Score must be supplied.' (OATM-C11-AC-10; OATM-BR-104)

### Requirement 7: OATM-REQ-F-101 (business rule)

#### Acceptance criteria

1. If the FICO score is not all three digits, then the system shall reject it with 'FICO Score must be all numeric.', and if it is zero, the system shall reject it with 'FICO Score must not be zero.'. (rules OATM-BR-105)
2. GIVEN an account is shown for update with changes WHEN the operator enters FICO score '7A0' and submits THEN the input is rejected with 'FICO Score must be all numeric.' (OATM-C11-AC-11; OATM-BR-105)
3. GIVEN an account is shown for update with changes WHEN the operator enters FICO score '000' and submits THEN the input is rejected with 'FICO Score must not be zero.' (OATM-C11-AC-12; OATM-BR-105)

### Requirement 8: OATM-REQ-F-102 (business rule)

#### Acceptance criteria

1. If a numeric, non-zero FICO score is below 300 or above 850, then the system shall mark the FICO score in error and reject the input with 'FICO Score: should be between 300 and 850', accepting 300 and 850 themselves. (rules OATM-BR-106)
2. GIVEN FICO score: 300 WHEN a numeric, non-zero FICO score is below 300 or above 850 THEN Accepted (OATM-C11-AC-05; OATM-BR-106)

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
| Customer identity | **summary card** | Customer ID (read-only); SSN as three labelled parts (3-2-4); Date of birth as Day, Month, Year; FICO score; Government-issued ID (optional) | SSN: 'SSN: First 3 chars must be supplied.', 'SSN: First 3 chars must be all numeric.', 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'; the 4th & 5th and last 4 characters must each be supplied, all numeric and non-zero. Date of birth: the date checks above, and 'Date of Birth:cannot be in the future '. FICO: 'FICO Score must be supplied.', 'FICO Score must be all numeric.', 'FICO Score must not be zero.', 'FICO Score: should be between 300 and 850'. |  | OATM-REQ-F-095, OATM-REQ-F-096, OATM-REQ-F-097, OATM-REQ-F-098, OATM-REQ-F-099, OATM-REQ-F-100, OATM-REQ-F-101, OATM-REQ-F-102 |


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
| OATM-BR-098 | Stage social security number parts | design note | WHEN the operator enters a Social Security Number part as '*' or leaves it blank, THE account update screen SHALL treat that part as not supplied; otherwise it SHALL take the entered part as the proposed value. | high | app/cbl/COACTUPC.cbl:1231-1252, app/cbl/COACTUPC.cbl:1529-1531, app/cbl/COACTUPC.cbl:2431-2491, app/cbl/COACTUPC.cbl:118-123 |
| OATM-BR-099 | Validate social security number | business rule | WHEN the first three SSN characters are blank, not all numeric or zero, THE account update validation SHALL reject them with 'SSN: First 3 chars must be supplied.', 'SSN: First 3 chars must be all numeric.' or 'SSN: First 3 chars must not be zero.' respectively, and SHALL not check the other two SSN parts. | high | app/cbl/COACTUPC.cbl:1231-1252, app/cbl/COACTUPC.cbl:1529-1531, app/cbl/COACTUPC.cbl:2431-2491, app/cbl/COACTUPC.cbl:118-123 |
| OATM-BR-100 | Validate SSN, birth date and FICO | business rule | WHEN changed details are checked, THE account update SHALL also check the SSN and require the date of birth to be a valid date earlier than today, rejecting a later date or today with 'Date of Birth:cannot be in the future '. | high | app/cbl/COACTUPC.cbl:1277-1284, app/cbl/COACTUPC.cbl:1529-1556, app/cbl/COACTUPC.cbl:845-849, app/cbl/COACTUPC.cbl:2109-2176 |
| OATM-BR-101 | Validate social security number | business rule | WHEN the first three SSN characters are numeric and equal 666 or fall between 900 and 999, THE account update validation SHALL reject them with 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'. | high | app/cbl/COACTUPC.cbl:1231-1252, app/cbl/COACTUPC.cbl:1529-1531, app/cbl/COACTUPC.cbl:2431-2491, app/cbl/COACTUPC.cbl:118-123 |
| OATM-BR-102 | Validate social security number | business rule | WHEN the first three SSN characters are numeric and non-zero, THE account update validation SHALL require the 4th-5th characters and the last 4 characters each to be supplied, all numeric and non-zero, giving 'SSN 4th & 5th chars …' or 'SSN Last 4 chars …' with 'must be supplied.', 'must be all numeric.' or 'must not be zero.'. | high | app/cbl/COACTUPC.cbl:1231-1252, app/cbl/COACTUPC.cbl:1529-1531, app/cbl/COACTUPC.cbl:2431-2491, app/cbl/COACTUPC.cbl:118-123 |
| OATM-BR-103 | Reject future date of birth | business rule | WHEN a valid calendar date of birth is today or later, THE account update validation SHALL reject it, flag the day, month and year fields, and show 'Date of Birth:cannot be in the future ' if no earlier error message is already set. | high | app/cbl/COACTUPC.cbl:1254-1275, app/cbl/COACTUPC.cbl:1533-1543, app/cpy/CSUTLDPY.cpy:341-370 |
| OATM-BR-104 | Stage credit score entry | business rule | WHEN the FICO score is entered as blank or '*', THE account update SHALL treat it as not supplied and reject it with 'FICO Score must be supplied.' | high | app/cbl/COACTUPC.cbl:1277-1284, app/cbl/COACTUPC.cbl:1529-1556, app/cbl/COACTUPC.cbl:845-849, app/cbl/COACTUPC.cbl:2109-2176 |
| OATM-BR-105 | Validate SSN, birth date and FICO | business rule | WHEN the FICO score is not all three digits, THE account update SHALL reject it with 'FICO Score must be all numeric.', and WHEN it is zero, SHALL reject it with 'FICO Score must not be zero.' | high | app/cbl/COACTUPC.cbl:1277-1284, app/cbl/COACTUPC.cbl:1529-1556, app/cbl/COACTUPC.cbl:845-849, app/cbl/COACTUPC.cbl:2109-2176 |
| OATM-BR-106 | Validate FICO score range | business rule | WHEN a numeric, non-zero FICO score is below 300 or above 850, THE account update SHALL mark the FICO score in error and reject the input with 'FICO Score: should be between 300 and 850'; 300 and 850 themselves are accepted. | high | app/cbl/COACTUPC.cbl:1277-1284, app/cbl/COACTUPC.cbl:1529-1556, app/cbl/COACTUPC.cbl:845-849, app/cbl/COACTUPC.cbl:2109-2176 |

### Worked examples

- OATM-BR-100: Date of birth = 1985-04-12 → Accepted
- OATM-BR-101: SSN = 912-12-3456 → Rejected with the same message.
- OATM-BR-101: SSN = 123-45-6789 → Accepted.
- OATM-BR-103: Today = 2026-11-23; Date of birth = 1980-05-14 → Accepted.
- OATM-BR-106: FICO score = 300 → Accepted

## Decision tables

#### FICO score checks

| Supplied (not blank or '*') | All three digits | Zero | Between 300 and 850 inclusive | Validation result | Rule |
|---|---|---|---|---|---|
| No | - | - | - | Reject with 'FICO Score must be supplied.' | OATM-BR-104 |
| Yes | No | - | - | Reject with 'FICO Score must be all numeric.' | OATM-BR-105 |
| Yes | Yes | Yes | - | Reject with 'FICO Score must not be zero.' | OATM-BR-105 |
| Yes | Yes | No | No | Mark in error, reject with 'FICO Score: should be between 300 and 850' | OATM-BR-106 |
| Yes | Yes | No | Yes | Accept | OATM-BR-106 |

#### SSN first three characters checks

| Supplied | All numeric | Zero | 666 or 900-999 | Validation result | Rule |
|---|---|---|---|---|---|
| No | - | - | - | 'SSN: First 3 chars must be supplied.'; other parts not checked | OATM-BR-099 |
| Yes | No | - | - | 'SSN: First 3 chars must be all numeric.'; other parts not checked | OATM-BR-099 |
| Yes | Yes | Yes | - | 'SSN: First 3 chars must not be zero.'; other parts not checked | OATM-BR-099 |
| Yes | Yes | No | Yes | 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999' | OATM-BR-101 |
| Yes | Yes | No | No | Go on to check 4th-5th and last 4 characters | OATM-BR-102 |
| Yes | Yes | No | Yes | **Gap:** No rule says whether the 4th-5th and last 4 characters are still checked when the first three are 666 or 900-999. | |


## Design notes

- OATM-BR-098: Capture the SSN as three optional parts (3, 2 and 4 characters). Blank or '*' parts are absent; others are kept as typed for the supplied, numeric, non-zero and forbidden-range checks. The SSN is sensitive personal data: mask it on screen and in logs, and protect it in storage.

## Open questions

- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-104, OATM-BR-098.
- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-103, OATM-BR-106, OATM-BR-102.
- SME-058: Please supply the complete, authoritative list of valid state and ZIP-prefix combinations. Is this rough check enough, or is a finer-grained address check required? (Data governance team) On OATM-BR-106, OATM-BR-102.
- SME-059: When the date-checking utility rejects a date, the date is still marked valid even though an input error is raised. Should a rejected date stay invalid, including for later checks such as 'date of birth cannot be in the future'? (Account servicing business owner) On OATM-BR-103.
- SME-060: Should date validation check that the month is numeric before checking that it is between 1 and 12? (Account servicing business owner) On OATM-BR-103.
- SME-061: Only years in the 1900s and 2000s are accepted for all four account and customer dates. Should this restriction still apply to card expiry and reissue dates? (Account servicing business owner) On OATM-BR-103.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-103, OATM-BR-106, OATM-BR-102.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-103, OATM-BR-106, OATM-BR-102.
- DEF-037: Is this intended? A date of birth equal to today is rejected with a message saying it is in the future, which it is not. (Subject-matter expert) On OATM-BR-103.
- DEF-042: Is this intended? The IF on part 1 being valid has no END-IF, so the SSN 4th-5th and last-4 checks are skipped whenever part 1 is blank, non-numeric or zero; the 000 branch of the forbidden-value message can never be shown. (Subject-matter expert) On OATM-BR-098, OATM-BR-102.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (12 in all).
