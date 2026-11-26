# Requirements: Validate customer phone numbers (OATM-C10)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Checks each customer phone number the operator enters as a North American number. The area code must be a listed general-purpose code, the prefix 3 non-zero digits and the line number 4 non-zero digits. A phone number left fully blank is optional and accepted. A partly entered or malformed number must never be saved. Each part is checked and flagged, but only the first message is shown.

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
2. GIVEN an account is shown for update with changes WHEN the operator enters Phone Number 1 as area code '2A1', prefix '555', line '1234' and submits THEN an input error is flagged with 'Phone Number 1: Area code must be A 3 digit number.' and the prefix is still checked (OATM-C10-AC-07; OATM-BR-089)

### Requirement 5: OATM-REQ-F-086 (business rule)

#### Acceptance criteria

1. If a supplied area code is 000, then the system shall flag an input error with '<Phone Number 1 or 2>: Area code cannot be zero' and go on to check the prefix. (rules OATM-BR-090)
2. GIVEN an account is shown for update with changes WHEN the operator enters Phone Number 2 as area code '000', prefix '555', line '1234' and submits THEN an input error is flagged with 'Phone Number 2: Area code cannot be zero' and the prefix is still checked (OATM-C10-AC-08; OATM-BR-090)

### Requirement 6: OATM-REQ-F-087 (business rule)

#### Acceptance criteria

1. If a supplied numeric, non-zero area code is not one of the listed North American general-purpose area codes (410 codes between '201' and '989', not every number in that range), then the system shall flag an input error with '<Phone Number 1 or 2>: Not valid North America general purpose area code'. (rules OATM-BR-091)
2. GIVEN Phone 1: (212) 555-1234 WHEN a supplied numeric, non-zero area code is not one of the listed North American general-purpose area codes (410 codes between '201' and '989', not every number in that range) THEN Area code accepted (OATM-C10-AC-04; OATM-BR-091)

### Requirement 7: OATM-REQ-F-088 (business rule)

#### Acceptance criteria

1. If the prefix of a phone number being checked is not supplied, then the system shall flag an input error with '<Phone Number 1 or 2>: Prefix code must be supplied.' and go on to check the line number. (rules OATM-BR-092)
2. GIVEN an account is shown for update with changes WHEN the operator enters Phone Number 1 with area code '212', the prefix blank and line '1234', and submits THEN an input error is flagged with 'Phone Number 1: Prefix code must be supplied.' and the line number is still checked (OATM-C10-AC-09; OATM-BR-092)

### Requirement 8: OATM-REQ-F-089 (business rule)

#### Acceptance criteria

1. If a supplied prefix is not all digits, then the system shall flag an input error with '<Phone Number 1 or 2>: Prefix code must be A 3 digit number.' and go on to check the line number. (rules OATM-BR-093)
2. GIVEN an account is shown for update with changes WHEN the operator enters Phone Number 1 as area code '212', prefix '5X5', line '1234' and submits THEN an input error is flagged with 'Phone Number 1: Prefix code must be A 3 digit number.' and the line number is still checked (OATM-C10-AC-10; OATM-BR-093)

### Requirement 9: OATM-REQ-F-090 (business rule)

#### Acceptance criteria

1. If a supplied prefix is 000, then the system shall flag an input error with '<Phone Number 1 or 2>: Prefix code cannot be zero' and go on to check the line number, accepting any other three-digit prefix (for example 555). (rules OATM-BR-094)
2. GIVEN Phone 1: (212) 555-1234 WHEN a supplied prefix is 000 THEN Prefix accepted (OATM-C10-AC-05; OATM-BR-094)

### Requirement 10: OATM-REQ-F-091 (business rule)

#### Acceptance criteria

1. If the line number of a phone number being checked is not supplied, then the system shall flag an input error with '<Phone Number 1 or 2>: Line number code must be supplied.'. (rules OATM-BR-095)
2. GIVEN an account is shown for update with changes WHEN the operator enters Phone Number 2 as area code '212', prefix '555' with the line number blank, and submits THEN an input error is flagged with 'Phone Number 2: Line number code must be supplied.' (OATM-C10-AC-11; OATM-BR-095)

### Requirement 11: OATM-REQ-F-092 (business rule)

#### Acceptance criteria

1. If a supplied line number is not all digits, then the system shall flag an input error with '<Phone Number 1 or 2>: Line number code must be A 4 digit number.'. (rules OATM-BR-096)
2. GIVEN an account is shown for update with changes WHEN the operator enters Phone Number 1 as area code '212', prefix '555', line '12B4' and submits THEN an input error is flagged with 'Phone Number 1: Line number code must be A 4 digit number.' (OATM-C10-AC-12; OATM-BR-096)

### Requirement 12: OATM-REQ-F-093 (business rule)

#### Acceptance criteria

1. If a supplied line number is 0000, then the system shall flag an input error with '<Phone Number 1 or 2>: Line number code cannot be zero', accepting any other four-digit line number. (rules OATM-BR-097)
2. GIVEN Phone 1: (212) 555-1234 WHEN a supplied line number is 0000 THEN Phone number 1 accepted (OATM-C10-AC-06; OATM-BR-097)

### Requirement 13: OATM-REQ-F-094 (formatting)

#### Acceptance criteria

1. When more than one phone number part fails its checks, the system shall flag every failing part in error but show only the first message raised, with no later message replacing one already set. (rules OATM-BR-073)
2. GIVEN an account is shown for update with changes WHEN the operator enters Phone Number 1 as area code '000', prefix '5X5', line '12B4' and submits THEN the area code, prefix and line number are all flagged in error, but the screen shows only 'Phone Number 1: Area code cannot be zero' (OATM-C10-AC-13; OATM-BR-073)
