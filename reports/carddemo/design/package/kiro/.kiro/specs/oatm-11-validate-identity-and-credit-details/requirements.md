# Requirements: Validate identity and credit details (OATM-C11)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Checks the customer's Social Security Number, date of birth and FICO score when the operator changes details. The SSN must be in three supplied, numeric, non-zero parts with an allowed first group, the birth date must be before today, and the FICO score must be between 300 and 850. Implausible identity or credit data must never be saved.

**User story:** As an operator, I want the SSN, date of birth and FICO score checked when I change customer details, so that only plausible identity and credit data is saved.

## Requirements

### Requirement 1: OATM-REQ-F-095 (design note)

#### Acceptance criteria

1. When the operator enters a Social Security Number part as '*' or leaves it blank, the system shall treat that part as not supplied, and otherwise take the entered part as the proposed value. (rules OATM-BR-098)
2. GIVEN a changed account where the operator enters '*' as the first three SSN characters WHEN the SSN is validated THEN the first part is treated as not supplied and rejected with 'SSN: First 3 chars must be supplied.' (OATM-C11-AC-06; OATM-BR-098)
3. GIVEN a changed account where the operator enters SSN parts '123', '45' and '6789' WHEN the changes are captured THEN '123', '45' and '6789' are taken as the proposed SSN parts (OATM-C11-AC-07; OATM-BR-098)

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
2. GIVEN a changed account where the SSN is '123', blank, '6789' WHEN the SSN is validated THEN the input is rejected with 'SSN 4th & 5th chars must be supplied.' (OATM-C11-AC-08; OATM-BR-102)
3. GIVEN a changed account where the SSN is '123', '4A', '6789' WHEN the SSN is validated THEN the input is rejected with 'SSN 4th & 5th chars must be all numeric.' (OATM-C11-AC-09; OATM-BR-102)
4. GIVEN a changed account where the SSN is '123', '45', '0000' WHEN the SSN is validated THEN the input is rejected with 'SSN Last 4 chars must not be zero.' (OATM-C11-AC-10; OATM-BR-102)

### Requirement 5: OATM-REQ-F-099 (business rule)

#### Acceptance criteria

1. If a valid calendar date of birth is today or later, then the system shall reject it, flag the day, month and year fields, and show 'Date of Birth:cannot be in the future ' if no earlier error message is already set. (rules OATM-BR-103, OATM-BR-100)
2. GIVEN Date of birth: 1985-04-12 WHEN changed details are checked THEN Accepted (OATM-C11-AC-01; OATM-BR-100)
3. GIVEN Today: 2026-11-23; Date of birth: 1980-05-14 WHEN a valid calendar date of birth is today or later THEN Accepted. (OATM-C11-AC-04; OATM-BR-103)

### Requirement 6: OATM-REQ-F-100 (business rule)

#### Acceptance criteria

1. If the FICO score is entered as blank or '*', then the system shall treat it as not supplied and reject it with 'FICO Score must be supplied.'. (rules OATM-BR-104)
2. GIVEN a changed account where the FICO score is left blank or entered as '*' WHEN the FICO score is validated THEN it is treated as not supplied and rejected with 'FICO Score must be supplied.' (OATM-C11-AC-11; OATM-BR-104)

### Requirement 7: OATM-REQ-F-101 (business rule)

#### Acceptance criteria

1. If the FICO score is not all three digits, then the system shall reject it with 'FICO Score must be all numeric.', and if it is zero, the system shall reject it with 'FICO Score must not be zero.'. (rules OATM-BR-105)
2. GIVEN a changed account where the FICO score is entered as '7A0' WHEN the FICO score is validated THEN it is rejected with 'FICO Score must be all numeric.' (OATM-C11-AC-12; OATM-BR-105)
3. GIVEN a changed account where the FICO score is entered as '000' WHEN the FICO score is validated THEN it is rejected with 'FICO Score must not be zero.' (OATM-C11-AC-13; OATM-BR-105)

### Requirement 8: OATM-REQ-F-102 (business rule)

#### Acceptance criteria

1. If a numeric, non-zero FICO score is below 300 or above 850, then the system shall mark the FICO score in error and reject the input with 'FICO Score: should be between 300 and 850', accepting 300 and 850 themselves. (rules OATM-BR-106)
2. GIVEN FICO score: 300 WHEN a numeric, non-zero FICO score is below 300 or above 850 THEN Accepted (OATM-C11-AC-05; OATM-BR-106)
