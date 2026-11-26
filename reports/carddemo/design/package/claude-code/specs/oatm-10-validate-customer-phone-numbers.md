# Validate customer phone numbers (OATM-C10)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Checks each customer phone number the operator enters as a North American number: area code from the list of general-purpose codes, then a 3-digit prefix and a 4-digit line number, none of them zero. Phones are optional, so a fully blank number is accepted. Every failing part is flagged, but only the first message is shown.

**User story:** As an operator, I want any phone number I enter checked as a North American number, so that only valid contact numbers are saved while phones stay optional.

## Requirements

### Requirement 1: OATM-REQ-F-082 (design note)

#### Acceptance criteria

1. When the operator enters '*' or leaves blank any part of phone number 1 or phone number 2 (area code, prefix or line number), the system shall treat that part as not supplied before validating it. (rules OATM-BR-085)
2. GIVEN Phone 1 area code: '*'; Phone 1 prefix: (blank) WHEN the operator enters '*' or leaves blank any part of phone number 1 or phone number 2 (area code, prefix or line number) on the account update screen THEN Both parts are treated as not supplied (OATM-C10-AC-01; OATM-BR-085)

### Requirement 2: OATM-REQ-F-083 (business rule)

#### Acceptance criteria

1. When the area code, prefix and line number of a phone number are all not supplied, the system shall accept the phone number as omitted and skip all further checks on it. (rules OATM-BR-086, OATM-BR-087)
2. GIVEN Phone 2 area code: (blank); Phone 2 prefix: (blank); Phone 2 line number: (blank) WHEN the area code, prefix and line number of a phone number are all not supplied THEN Phone number 2 is accepted; no error (OATM-C10-AC-02; OATM-BR-086)
3. GIVEN Phone number 2: (blank) WHEN account update runs THEN Accepted (OATM-C10-AC-03; OATM-BR-087)

### Requirement 3: OATM-REQ-F-084 (business rule)

#### Acceptance criteria

1. If any part of a phone number is supplied but its area code is not, then the system shall flag an input error with '<Phone Number 1 or 2>: Area code must be supplied.' and go on to check the prefix. (rules OATM-BR-088, OATM-BR-087)
2. GIVEN Phone number 2: (blank) WHEN account update runs THEN Accepted (OATM-C10-AC-03; OATM-BR-087)

### Requirement 4: OATM-REQ-F-085 (business rule)

#### Acceptance criteria

1. If a supplied area code is not all digits, then the system shall flag an input error with '<Phone Number 1 or 2>: Area code must be A 3 digit number.' and go on to check the prefix. (rules OATM-BR-089)
2. GIVEN a changed account where Phone Number 1 has area code '2A1', prefix '555' and line number '1234' WHEN the phone number is validated THEN an input error is flagged with 'Phone Number 1: Area code must be A 3 digit number.' and the prefix is still checked (OATM-C10-AC-07; OATM-BR-089)

### Requirement 5: OATM-REQ-F-086 (business rule)

#### Acceptance criteria

1. If a supplied area code is 000, then the system shall flag an input error with '<Phone Number 1 or 2>: Area code cannot be zero' and go on to check the prefix. (rules OATM-BR-090)
2. GIVEN a changed account where Phone Number 2 has area code '000', prefix '555' and line number '1234' WHEN the phone number is validated THEN an input error is flagged with 'Phone Number 2: Area code cannot be zero' and the prefix is still checked (OATM-C10-AC-08; OATM-BR-090)

### Requirement 6: OATM-REQ-F-087 (business rule)

#### Acceptance criteria

1. If a supplied numeric, non-zero area code is not one of the listed North American general-purpose area codes (410 codes between '201' and '989', not every number in that range), then the system shall flag an input error with '<Phone Number 1 or 2>: Not valid North America general purpose area code'. (rules OATM-BR-091)
2. GIVEN Phone 1: (212) 555-1234 WHEN a supplied numeric, non-zero area code is not one of the listed North American general-purpose area codes (410 codes between '201' and '989', not every number in that range) THEN Area code accepted (OATM-C10-AC-04; OATM-BR-091)

### Requirement 7: OATM-REQ-F-088 (business rule)

#### Acceptance criteria

1. If the prefix of a phone number being checked is not supplied, then the system shall flag an input error with '<Phone Number 1 or 2>: Prefix code must be supplied.' and go on to check the line number. (rules OATM-BR-092)
2. GIVEN a changed account where Phone Number 1 has area code '212', a blank prefix and line number '1234' WHEN the phone number is validated THEN an input error is flagged with 'Phone Number 1: Prefix code must be supplied.' and the line number is still checked (OATM-C10-AC-09; OATM-BR-092)

### Requirement 8: OATM-REQ-F-089 (business rule)

#### Acceptance criteria

1. If a supplied prefix is not all digits, then the system shall flag an input error with '<Phone Number 1 or 2>: Prefix code must be A 3 digit number.' and go on to check the line number. (rules OATM-BR-093)
2. GIVEN a changed account where Phone Number 1 has area code '212', prefix '5X5' and line number '1234' WHEN the phone number is validated THEN an input error is flagged with 'Phone Number 1: Prefix code must be A 3 digit number.' and the line number is still checked (OATM-C10-AC-10; OATM-BR-093)

### Requirement 9: OATM-REQ-F-090 (business rule)

#### Acceptance criteria

1. If a supplied prefix is 000, then the system shall flag an input error with '<Phone Number 1 or 2>: Prefix code cannot be zero' and go on to check the line number, accepting any other three-digit prefix (for example 555). (rules OATM-BR-094)
2. GIVEN Phone 1: (212) 555-1234 WHEN a supplied prefix is 000 THEN Prefix accepted (OATM-C10-AC-05; OATM-BR-094)

### Requirement 10: OATM-REQ-F-091 (business rule)

#### Acceptance criteria

1. If the line number of a phone number being checked is not supplied, then the system shall flag an input error with '<Phone Number 1 or 2>: Line number code must be supplied.'. (rules OATM-BR-095)
2. GIVEN a changed account where Phone Number 2 has area code '212', prefix '555' and the line number left blank WHEN the phone number is validated THEN an input error is flagged with 'Phone Number 2: Line number code must be supplied.' (OATM-C10-AC-11; OATM-BR-095)

### Requirement 11: OATM-REQ-F-092 (business rule)

#### Acceptance criteria

1. If a supplied line number is not all digits, then the system shall flag an input error with '<Phone Number 1 or 2>: Line number code must be A 4 digit number.'. (rules OATM-BR-096)
2. GIVEN a changed account where Phone Number 1 has area code '212', prefix '555' and line number '12B4' WHEN the phone number is validated THEN an input error is flagged with 'Phone Number 1: Line number code must be A 4 digit number.' (OATM-C10-AC-12; OATM-BR-096)

### Requirement 12: OATM-REQ-F-093 (business rule)

#### Acceptance criteria

1. If a supplied line number is 0000, then the system shall flag an input error with '<Phone Number 1 or 2>: Line number code cannot be zero', accepting any other four-digit line number. (rules OATM-BR-097)
2. GIVEN Phone 1: (212) 555-1234 WHEN a supplied line number is 0000 THEN Phone number 1 accepted (OATM-C10-AC-06; OATM-BR-097)

### Requirement 13: OATM-REQ-F-094 (formatting)

#### Acceptance criteria

1. When more than one phone number part fails its checks, the system shall flag every failing part in error but show only the first message raised, with no later message replacing one already set. (rules OATM-BR-073)
2. GIVEN a changed account where no earlier error is set and Phone Number 1 has area code '000', prefix '000' and line number '0000' WHEN the phone number is validated THEN the area code, prefix and line number are all flagged in error, and only the message 'Phone Number 1: Area code cannot be zero' is shown (OATM-C10-AC-13; OATM-BR-073)

## Screens and components

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Fix these fields | message | A summary listing every field in error, each linking to its field, in screen order; focus moves to the summary. Each field also shows its own message (the 3270 screen showed only the first message). |  |  | OATM-REQ-F-094 |
| Primary card holder | radio | Yes (Y) / No (N) | Required: 'Primary Card Holder must be supplied.'; only Yes or No: 'Primary Card Holder must be Y or N.' |  |  |
| Phone 1 (optional) | text | One field, formatted (aaa)ppp-nnnn | Optional; leave all of it blank to omit. If any part is entered: the area code must be supplied ('Phone Number 1: Area code must be supplied.'), 3 digits ('Phone Number 1: Area code must be A 3 digit number.'), not 000 ('Phone Number 1: Area code cannot be zero') and a general-purpose North American area code ('Phone Number 1: Not valid North America general purpose area code'); the prefix must be supplied, 3 digits and not 000 ('Phone Number 1: Prefix code must be supplied.' / 'Phone Number 1: Prefix code must be A 3 digit number.' / 'Phone Number 1: Prefix code cannot be zero'); the line number must be supplied, 4 digits and not 0000 ('Phone Number 1: Line number code must be supplied.' / 'Phone Number 1: Line number code must be A 4 digit number.' / 'Phone Number 1: Line number code cannot be zero'). |  | OATM-REQ-F-082, OATM-REQ-F-083, OATM-REQ-F-087 |
| Phone 2 (optional) | text | One field, formatted (aaa)ppp-nnnn | Optional; leave all of it blank to omit. If any part is entered: the area code must be supplied ('Phone Number 2: Area code must be supplied.'), 3 digits ('Phone Number 2: Area code must be A 3 digit number.'), not 000 ('Phone Number 2: Area code cannot be zero') and a general-purpose North American area code ('Phone Number 2: Not valid North America general purpose area code'); the prefix must be supplied, 3 digits and not 000 ('Phone Number 2: Prefix code must be supplied.' / 'Phone Number 2: Prefix code must be A 3 digit number.' / 'Phone Number 2: Prefix code cannot be zero'); the line number must be supplied, 4 digits and not 0000 ('Phone Number 2: Line number code must be supplied.' / 'Phone Number 2: Line number code must be A 4 digit number.' / 'Phone Number 2: Line number code cannot be zero'). |  | OATM-REQ-F-082, OATM-REQ-F-083, OATM-REQ-F-087 |


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
| OATM-BR-085 | Stage customer phone number parts | design note | WHEN the operator enters '*' or leaves blank any part of phone number 1 or phone number 2 (area code, prefix or line number) on the account update screen, THE Account Update SHALL treat that part as not supplied before validating it. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-086 | Accept a fully blank phone number | business rule | WHEN the area code, prefix and line number of a phone number are all not supplied, THE Account Update SHALL accept the phone number as omitted and skip all further checks on it, since a phone number is not mandatory. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-087 | Validate phones, EFT id and holder flag | business rule | THE account update SHALL accept blank phone numbers 1 and 2, edit any phone number that is entered as a North American number, and require the primary card holder indicator, rejecting a blank with 'Primary Card Holder must be supplied.' and any value other than 'Y' or 'N' with 'Primary Card Holder must be Y or N.' | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-088 | Reject missing phone area code | business rule | WHEN any part of a phone number is supplied but its area code is not, THE Account Update SHALL flag an input error with '<Phone Number 1 or 2>: Area code must be supplied.' and go on to check the prefix. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-089 | Reject non-numeric phone area code | business rule | WHEN a supplied area code is not all digits, THE Account Update SHALL flag an input error with '<Phone Number 1 or 2>: Area code must be A 3 digit number.' and go on to check the prefix. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-090 | Reject zero phone area code | business rule | WHEN a supplied area code is 000, THE Account Update SHALL flag an input error with '<Phone Number 1 or 2>: Area code cannot be zero' and go on to check the prefix. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-091 | Require recognised general-purpose area code | business rule | WHEN a supplied numeric, non-zero area code is not one of the listed North American general-purpose area codes (410 codes between '201' and '989', not every number in that range), THE Account Update SHALL flag an input error with '<Phone Number 1 or 2>: Not valid North America general purpose area code'; otherwise it SHALL accept the area code. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-092 | Reject missing phone prefix | business rule | WHEN the prefix of a phone number being checked is not supplied, THE Account Update SHALL flag an input error with '<Phone Number 1 or 2>: Prefix code must be supplied.' and go on to check the line number. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-093 | Reject non-numeric phone prefix | business rule | WHEN a supplied prefix is not all digits, THE Account Update SHALL flag an input error with '<Phone Number 1 or 2>: Prefix code must be A 3 digit number.' and go on to check the line number. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-094 | Reject zero phone prefix | business rule | WHEN a supplied prefix is 000, THE Account Update SHALL flag an input error with '<Phone Number 1 or 2>: Prefix code cannot be zero' and go on to check the line number; any other three-digit prefix (for example 555) SHALL be accepted. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-095 | Reject missing phone line number | business rule | WHEN the line number of a phone number being checked is not supplied, THE Account Update SHALL flag an input error with '<Phone Number 1 or 2>: Line number code must be supplied.'. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-096 | Reject non-numeric phone line number | business rule | WHEN a supplied line number is not all digits, THE Account Update SHALL flag an input error with '<Phone Number 1 or 2>: Line number code must be A 4 digit number.'. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-097 | Reject zero phone line number | business rule | WHEN a supplied line number is 0000, THE Account Update SHALL flag an input error with '<Phone Number 1 or 2>: Line number code cannot be zero'; any other four-digit line number SHALL be accepted. | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |
| OATM-BR-073 | Validate phone area code | formatting | WHEN more than one phone number part fails its checks, THE Account Update SHALL flag every failing part in error but show only the first message raised on the screen (no later message replaces one already set). | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |

### Worked examples

- OATM-BR-085: Phone 1 area code = '*'; Phone 1 prefix = (blank) → Both parts are treated as not supplied
- OATM-BR-086: Phone 2 area code = (blank); Phone 2 prefix = (blank); Phone 2 line number = (blank) → Phone number 2 is accepted; no error
- OATM-BR-087: Phone number 2 = (blank) → Accepted
- OATM-BR-091: Phone 1 = (212) 555-1234 → Area code accepted
- OATM-BR-094: Phone 1 = (212) 555-1234 → Prefix accepted
- OATM-BR-097: Phone 1 = (212) 555-1234 → Phone number 1 accepted

## Decision tables

#### Phone number part checks

| Phone part | Any part of the phone supplied | Part supplied | All digits | Zero | Listed general-purpose area code | Validation result | Rule |
|---|---|---|---|---|---|---|---|
| All parts | No | - | - | - | - | Accept phone as omitted, skip further checks | OATM-BR-086 |
| Area code | Yes | No | - | - | - | 'Area code must be supplied.', go on to prefix | OATM-BR-088 |
| Area code | Yes | Yes | No | - | - | 'Area code must be A 3 digit number.', go on to prefix | OATM-BR-089 |
| Area code | Yes | Yes | Yes | Yes | - | 'Area code cannot be zero', go on to prefix | OATM-BR-090 |
| Area code | Yes | Yes | Yes | No | No | 'Not valid North America general purpose area code' | OATM-BR-091 |
| Area code | Yes | Yes | Yes | No | Yes | Accept area code | OATM-BR-091 |
| Prefix | Yes | No | - | - | - | 'Prefix code must be supplied.', go on to line number | OATM-BR-092 |
| Prefix | Yes | Yes | No | - | - | 'Prefix code must be A 3 digit number.', go on to line number | OATM-BR-093 |
| Prefix | Yes | Yes | Yes | Yes | - | 'Prefix code cannot be zero', go on to line number | OATM-BR-094 |
| Prefix | Yes | Yes | Yes | No | - | Accept prefix | OATM-BR-094 |
| Line number | Yes | No | - | - | - | 'Line number code must be supplied.' | OATM-BR-095 |
| Line number | Yes | Yes | No | - | - | 'Line number code must be A 4 digit number.' | OATM-BR-096 |
| Line number | Yes | Yes | Yes | Yes | - | 'Line number code cannot be zero' | OATM-BR-097 |
| Line number | Yes | Yes | Yes | No | - | Accept line number | OATM-BR-097 |


## Design notes

- OATM-BR-085: Input binding for the area code, prefix and line number of each phone: blank or '*' becomes null per part before the phone validator runs, so a phone with all three parts null counts as omitted.

## Open questions

- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-085.
- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-095, OATM-BR-096, OATM-BR-097, OATM-BR-073, OATM-BR-086, OATM-BR-088, OATM-BR-089, OATM-BR-090, OATM-BR-091, OATM-BR-092, OATM-BR-093, OATM-BR-094.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-073, OATM-BR-086.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-073, OATM-BR-086.
- DEF-038: Confirm this is deliberate: The name, city, state and country fields accept only the letters A-Z and a-z and spaces. Real names and places with apostrophes, hyphens or periods ('O'Brien', 'St. Louis') are rejected. Separately, the blank-phone check tests the area-code part twice where it should test the line-number part. (Subject-matter expert) On OATM-BR-087.
- DEF-041: Is this intended? The 'phone not supplied' test checks the area code twice and never checks that the line number is blank-spaces (third condition tests area code = spaces OR line number = low-values). Because the screen input turns blanks into low-values first, this has no visible effect today, but a number arriving with a spaces area code and prefix would be accepted as omitted even with a line number entered. (Subject-matter expert) On OATM-BR-085, OATM-BR-095, OATM-BR-096, OATM-BR-097, OATM-BR-073, OATM-BR-086, OATM-BR-088, OATM-BR-089, OATM-BR-090, OATM-BR-091, OATM-BR-092, OATM-BR-093, OATM-BR-094.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).
