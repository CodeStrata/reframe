# Feature specification: Validate customer phone numbers

**Feature:** OATM-C10 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C10)

As an operator, I want any phone number I enter checked as a North American number, so that only valid contact numbers are saved while phones stay optional.

Checks each customer phone number the operator enters as a North American number. The area code must be a listed general-purpose code, the prefix 3 non-zero digits and the line number 4 non-zero digits. A phone number left fully blank is optional and accepted. A partly entered or malformed number must never be saved. Each part is checked and flagged, but only the first message is shown.

**Acceptance scenarios:**

1. **Given** Phone 1 area code: '*'; Phone 1 prefix: (blank), **when** the operator enters '*' or leaves blank any part of phone number 1 or phone number 2 (area code, prefix or line number) on the account update screen, **then** Both parts are treated as not supplied (OATM-C10-AC-01)
2. **Given** Phone 2 area code: (blank); Phone 2 prefix: (blank); Phone 2 line number: (blank), **when** the area code, prefix and line number of a phone number are all not supplied, **then** Phone number 2 is accepted; no error (OATM-C10-AC-02)
3. **Given** Phone number 2: (blank), **when** account update runs, **then** Accepted (OATM-C10-AC-03)
4. **Given** Phone 1: (212) 555-1234, **when** a supplied numeric, non-zero area code is not one of the listed North American general-purpose area codes (410 codes between '201' and '989', not every number in that range), **then** Area code accepted (OATM-C10-AC-04)
5. **Given** Phone 1: (212) 555-1234, **when** a supplied prefix is 000, **then** Prefix accepted (OATM-C10-AC-05)
6. **Given** Phone 1: (212) 555-1234, **when** a supplied line number is 0000, **then** Phone number 1 accepted (OATM-C10-AC-06)
7. **Given** an account is shown for update with changes, **when** the operator enters Phone Number 1 as area code '2A1', prefix '555', line '1234' and submits, **then** an input error is flagged with 'Phone Number 1: Area code must be A 3 digit number.' and the prefix is still checked (OATM-C10-AC-07)
8. **Given** an account is shown for update with changes, **when** the operator enters Phone Number 2 as area code '000', prefix '555', line '1234' and submits, **then** an input error is flagged with 'Phone Number 2: Area code cannot be zero' and the prefix is still checked (OATM-C10-AC-08)
9. **Given** an account is shown for update with changes, **when** the operator enters Phone Number 1 with area code '212', the prefix blank and line '1234', and submits, **then** an input error is flagged with 'Phone Number 1: Prefix code must be supplied.' and the line number is still checked (OATM-C10-AC-09)
10. **Given** an account is shown for update with changes, **when** the operator enters Phone Number 1 as area code '212', prefix '5X5', line '1234' and submits, **then** an input error is flagged with 'Phone Number 1: Prefix code must be A 3 digit number.' and the line number is still checked (OATM-C10-AC-10)
11. **Given** an account is shown for update with changes, **when** the operator enters Phone Number 2 as area code '212', prefix '555' with the line number blank, and submits, **then** an input error is flagged with 'Phone Number 2: Line number code must be supplied.' (OATM-C10-AC-11)
12. **Given** an account is shown for update with changes, **when** the operator enters Phone Number 1 as area code '212', prefix '555', line '12B4' and submits, **then** an input error is flagged with 'Phone Number 1: Line number code must be A 4 digit number.' (OATM-C10-AC-12)
13. **Given** an account is shown for update with changes, **when** the operator enters Phone Number 1 as area code '000', prefix '5X5', line '12B4' and submits, **then** the area code, prefix and line number are all flagged in error, but the screen shows only 'Phone Number 1: Area code cannot be zero' (OATM-C10-AC-13)

## Requirements

### Functional requirements

- **OATM-REQ-F-082** (design note): When the operator enters '*' or leaves blank any part of phone number 1 or phone number 2 (area code, prefix or line number), the system shall treat that part as not supplied before validating it. Rules: OATM-BR-085.
- **OATM-REQ-F-083** (business rule): When the area code, prefix and line number of a phone number are all not supplied, the system shall accept the phone number as omitted and skip all further checks on it. Rules: OATM-BR-086, OATM-BR-087.
- **OATM-REQ-F-084** (business rule): If any part of a phone number is supplied but its area code is not, then the system shall flag an input error with '<Phone Number 1 or 2>: Area code must be supplied.' and go on to check the prefix. Rules: OATM-BR-088, OATM-BR-087.
- **OATM-REQ-F-085** (business rule): If a supplied area code is not all digits, then the system shall flag an input error with '<Phone Number 1 or 2>: Area code must be A 3 digit number.' and go on to check the prefix. Rules: OATM-BR-089.
- **OATM-REQ-F-086** (business rule): If a supplied area code is 000, then the system shall flag an input error with '<Phone Number 1 or 2>: Area code cannot be zero' and go on to check the prefix. Rules: OATM-BR-090.
- **OATM-REQ-F-087** (business rule): If a supplied numeric, non-zero area code is not one of the listed North American general-purpose area codes (410 codes between '201' and '989', not every number in that range), then the system shall flag an input error with '<Phone Number 1 or 2>: Not valid North America general purpose area code'. Rules: OATM-BR-091.
- **OATM-REQ-F-088** (business rule): If the prefix of a phone number being checked is not supplied, then the system shall flag an input error with '<Phone Number 1 or 2>: Prefix code must be supplied.' and go on to check the line number. Rules: OATM-BR-092.
- **OATM-REQ-F-089** (business rule): If a supplied prefix is not all digits, then the system shall flag an input error with '<Phone Number 1 or 2>: Prefix code must be A 3 digit number.' and go on to check the line number. Rules: OATM-BR-093.
- **OATM-REQ-F-090** (business rule): If a supplied prefix is 000, then the system shall flag an input error with '<Phone Number 1 or 2>: Prefix code cannot be zero' and go on to check the line number, accepting any other three-digit prefix (for example 555). Rules: OATM-BR-094.
- **OATM-REQ-F-091** (business rule): If the line number of a phone number being checked is not supplied, then the system shall flag an input error with '<Phone Number 1 or 2>: Line number code must be supplied.'. Rules: OATM-BR-095.
- **OATM-REQ-F-092** (business rule): If a supplied line number is not all digits, then the system shall flag an input error with '<Phone Number 1 or 2>: Line number code must be A 4 digit number.'. Rules: OATM-BR-096.
- **OATM-REQ-F-093** (business rule): If a supplied line number is 0000, then the system shall flag an input error with '<Phone Number 1 or 2>: Line number code cannot be zero', accepting any other four-digit line number. Rules: OATM-BR-097.
- **OATM-REQ-F-094** (formatting): When more than one phone number part fails its checks, the system shall flag every failing part in error but show only the first message raised, with no later message replacing one already set. Rules: OATM-BR-073.

### Business rules

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

### Key entities

- CSMSG02Y (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSLKPCDY (working storage)
- CSMSG01Y (working storage)
- CSSETATY (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CSUTLDPY (working storage)
- CSUTLDWY (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-085.
- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-095, OATM-BR-096, OATM-BR-097, OATM-BR-073, OATM-BR-086, OATM-BR-088, OATM-BR-089, OATM-BR-090, OATM-BR-091, OATM-BR-092, OATM-BR-093, OATM-BR-094.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-073, OATM-BR-086.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-073, OATM-BR-086.
- DEF-038: Confirm this is deliberate: The name, city, state and country fields accept only the letters A-Z and a-z and spaces. Real names and places with apostrophes, hyphens or periods ('O'Brien', 'St. Louis') are rejected. Separately, the blank-phone check tests the area-code part twice where it should test the line-number part. (Subject-matter expert) On OATM-BR-087.
- DEF-041: Is this intended? The 'phone not supplied' test checks the area code twice and never checks that the line number is blank-spaces (third condition tests area code = spaces OR line number = low-values). Because the screen input turns blanks into low-values first, this has no visible effect today, but a number arriving with a spaces area code and prefix would be accepted as omitted even with a line number entered. (Subject-matter expert) On OATM-BR-085, OATM-BR-095, OATM-BR-096, OATM-BR-097, OATM-BR-073, OATM-BR-086, OATM-BR-088, OATM-BR-089, OATM-BR-090, OATM-BR-091, OATM-BR-092, OATM-BR-093, OATM-BR-094.

### Decision table gaps

None.
