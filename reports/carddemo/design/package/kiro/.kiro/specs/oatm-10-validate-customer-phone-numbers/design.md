# Design: Validate customer phone numbers (OATM-C10)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Checks each customer phone number the operator enters as a North American number. The area code must be a listed general-purpose code, the prefix 3 non-zero digits and the line number 4 non-zero digits. A phone number left fully blank is optional and accepted. A partly entered or malformed number must never be saved. Each part is checked and flagged, but only the first message is shown.

Runs as online. Journeys: J02.

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
| Phone and payments | **summary card** | Phone 1 and Phone 2 (optional), each as labelled Area code, Prefix and Line number; EFT account ID; Primary card holder as a choice of Yes or No | A phone may be left wholly blank; otherwise '<Phone Number 1 or 2>: Area code must be supplied.', ': Area code must be A 3 digit number.', ': Area code cannot be zero', ': Not valid North America general purpose area code' (from the list of general-purpose codes), ': Prefix code must be supplied.', ': Prefix code must be A 3 digit number.', ': Prefix code cannot be zero', ': Line number code must be supplied.', ': Line number code must be A 4 digit number.', ': Line number code cannot be zero'. EFT account ID: 'EFT Account Id must be supplied.', all numeric, 10 digits, not zero. Primary card holder: 'Primary Card Holder must be supplied.' and must be Yes or No ('must be Y or N.'). |  | OATM-REQ-F-082, OATM-REQ-F-083, OATM-REQ-F-084, OATM-REQ-F-085, OATM-REQ-F-086, OATM-REQ-F-087, OATM-REQ-F-088, OATM-REQ-F-089, OATM-REQ-F-090, OATM-REQ-F-091, OATM-REQ-F-092, OATM-REQ-F-093, OATM-REQ-F-094 |


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

- OATM-BR-085: Capture phone numbers 1 and 2 as three optional parts each (area code, prefix, line number). Blank or '*' parts are absent before validation, so a phone with all parts absent counts as omitted. Area-code validation needs a reference list of the North American general-purpose area codes.

## Open questions

- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-085.
- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-095, OATM-BR-096, OATM-BR-097, OATM-BR-073, OATM-BR-086, OATM-BR-088, OATM-BR-089, OATM-BR-090, OATM-BR-091, OATM-BR-092, OATM-BR-093, OATM-BR-094.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-073, OATM-BR-086.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-073, OATM-BR-086.
- DEF-038: Confirm this is deliberate: The name, city, state and country fields accept only the letters A-Z and a-z and spaces. Real names and places with apostrophes, hyphens or periods ('O'Brien', 'St. Louis') are rejected. Separately, the blank-phone check tests the area-code part twice where it should test the line-number part. (Subject-matter expert) On OATM-BR-087.
- DEF-041: Is this intended? The 'phone not supplied' test checks the area code twice and never checks that the line number is blank-spaces (third condition tests area code = spaces OR line number = low-values). Because the screen input turns blanks into low-values first, this has no visible effect today, but a number arriving with a spaces area code and prefix would be accepted as omitted even with a line number entered. (Subject-matter expert) On OATM-BR-085, OATM-BR-095, OATM-BR-096, OATM-BR-097, OATM-BR-073, OATM-BR-086, OATM-BR-088, OATM-BR-089, OATM-BR-090, OATM-BR-091, OATM-BR-092, OATM-BR-093, OATM-BR-094.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).