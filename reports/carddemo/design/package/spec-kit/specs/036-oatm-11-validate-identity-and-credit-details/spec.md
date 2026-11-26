# Feature specification: Validate identity and credit details

**Feature:** OATM-C11 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C11)

As an operator, I want the SSN, date of birth and FICO score checked when I change customer details, so that only plausible identity and credit data is saved.

Checks the customer's Social Security Number, date of birth and FICO score when the operator changes details. The SSN must be in three supplied, numeric, non-zero parts with an allowed first group, the birth date must be before today, and the FICO score must be between 300 and 850. Implausible identity or credit data must never be saved.

**Acceptance scenarios:**

1. **Given** Date of birth: 1985-04-12, **when** changed details are checked, **then** Accepted (OATM-C11-AC-01)
2. **Given** SSN: 912-12-3456, **when** the first three SSN characters are numeric and equal 666 or fall between 900 and 999, **then** Rejected with the same message. (OATM-C11-AC-02)
3. **Given** SSN: 123-45-6789, **when** the first three SSN characters are numeric and equal 666 or fall between 900 and 999, **then** Accepted. (OATM-C11-AC-03)
4. **Given** Today: 2026-11-23; Date of birth: 1980-05-14, **when** a valid calendar date of birth is today or later, **then** Accepted. (OATM-C11-AC-04)
5. **Given** FICO score: 300, **when** a numeric, non-zero FICO score is below 300 or above 850, **then** Accepted (OATM-C11-AC-05)
6. **Given** a changed account where the operator enters '*' as the first three SSN characters, **when** the SSN is validated, **then** the first part is treated as not supplied and rejected with 'SSN: First 3 chars must be supplied.' (OATM-C11-AC-06)
7. **Given** a changed account where the operator enters SSN parts '123', '45' and '6789', **when** the changes are captured, **then** '123', '45' and '6789' are taken as the proposed SSN parts (OATM-C11-AC-07)
8. **Given** a changed account where the SSN is '123', blank, '6789', **when** the SSN is validated, **then** the input is rejected with 'SSN 4th & 5th chars must be supplied.' (OATM-C11-AC-08)
9. **Given** a changed account where the SSN is '123', '4A', '6789', **when** the SSN is validated, **then** the input is rejected with 'SSN 4th & 5th chars must be all numeric.' (OATM-C11-AC-09)
10. **Given** a changed account where the SSN is '123', '45', '0000', **when** the SSN is validated, **then** the input is rejected with 'SSN Last 4 chars must not be zero.' (OATM-C11-AC-10)
11. **Given** a changed account where the FICO score is left blank or entered as '*', **when** the FICO score is validated, **then** it is treated as not supplied and rejected with 'FICO Score must be supplied.' (OATM-C11-AC-11)
12. **Given** a changed account where the FICO score is entered as '7A0', **when** the FICO score is validated, **then** it is rejected with 'FICO Score must be all numeric.' (OATM-C11-AC-12)
13. **Given** a changed account where the FICO score is entered as '000', **when** the FICO score is validated, **then** it is rejected with 'FICO Score must not be zero.' (OATM-C11-AC-13)

## Requirements

### Functional requirements

- **OATM-REQ-F-095** (design note): When the operator enters a Social Security Number part as '*' or leaves it blank, the system shall treat that part as not supplied, and otherwise take the entered part as the proposed value. Rules: OATM-BR-098.
- **OATM-REQ-F-096** (business rule): If the first three SSN characters are blank, not all numeric or zero, then the system shall reject them with 'SSN: First 3 chars must be supplied.', 'SSN: First 3 chars must be all numeric.' or 'SSN: First 3 chars must not be zero.' respectively, and shall not check the other two SSN parts. Rules: OATM-BR-099, OATM-BR-100.
- **OATM-REQ-F-097** (business rule): If the first three SSN characters are numeric and equal 666 or fall between 900 and 999, then the system shall reject them with 'SSN: First 3 chars: should not be 000, 666, or between 900 and 999'. Rules: OATM-BR-101.
- **OATM-REQ-F-098** (business rule): When the first three SSN characters are numeric and non-zero, the system shall require the 4th-5th characters and the last 4 characters each to be supplied, all numeric and non-zero, giving 'SSN 4th & 5th chars …' or 'SSN Last 4 chars …' with 'must be supplied.', 'must be all numeric.' or 'must not be zero.'. Rules: OATM-BR-102.
- **OATM-REQ-F-099** (business rule): If a valid calendar date of birth is today or later, then the system shall reject it, flag the day, month and year fields, and show 'Date of Birth:cannot be in the future ' if no earlier error message is already set. Rules: OATM-BR-103, OATM-BR-100.
- **OATM-REQ-F-100** (business rule): If the FICO score is entered as blank or '*', then the system shall treat it as not supplied and reject it with 'FICO Score must be supplied.'. Rules: OATM-BR-104.
- **OATM-REQ-F-101** (business rule): If the FICO score is not all three digits, then the system shall reject it with 'FICO Score must be all numeric.', and if it is zero, the system shall reject it with 'FICO Score must not be zero.'. Rules: OATM-BR-105.
- **OATM-REQ-F-102** (business rule): If a numeric, non-zero FICO score is below 300 or above 850, then the system shall mark the FICO score in error and reject the input with 'FICO Score: should be between 300 and 850', accepting 300 and 850 themselves. Rules: OATM-BR-106.

### Business rules

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

### Decision table gaps

- SSN first three characters checks: No rule says whether the 4th-5th and last 4 characters are still checked when the first three are 666 or 900-999.
