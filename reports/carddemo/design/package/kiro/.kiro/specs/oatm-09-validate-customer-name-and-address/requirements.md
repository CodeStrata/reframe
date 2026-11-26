# Requirements: Validate customer name and address (OATM-C09)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Checks the customer's names, address line 1, city, state, ZIP and country when the operator changes details, including that the state is a valid US state code and matches the ZIP prefix. Middle name and address line 2 are optional. It must never save a missing required name or address part, non-letter characters in names, or a state and ZIP that do not belong together.

**User story:** As an operator, I want customer names and address details checked when I change them, so that only well-formed and consistent names and addresses are saved.

## Requirements

### Requirement 1: OATM-REQ-F-073 (design note)

#### Acceptance criteria

1. When the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, state, ZIP code or EFT account id, the system shall treat that entry as not supplied, and otherwise take the entered value as the proposed new value, holding the city as address line 3. (rules OATM-BR-074, OATM-BR-075)
2. GIVEN Middle name entry: * WHEN the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, or EFT account id on the account update screen THEN The middle name is treated as not supplied (OATM-C09-AC-01; OATM-BR-074)
3. GIVEN ZIP entered: 10001 WHEN the operator enters '*' or leaves the state or the ZIP code blank on the account update screen THEN ZIP 10001 is taken for editing (OATM-C09-AC-02; OATM-BR-075)

### Requirement 2: OATM-REQ-F-074 (business rule)

#### Acceptance criteria

1. If the first name, last name, city, state or country is not supplied after the operator changes account or customer details, then the system shall reject the input with '<field> must be supplied.' (for example 'First Name must be supplied.') and mark the field blank ('B'). (rules OATM-BR-076)
2. GIVEN a fetched account is shown and the operator changes details and clears the First Name WHEN the changes are validated THEN the input is rejected with 'First Name must be supplied.' and the First Name field is marked blank ('B') (OATM-C09-AC-12; OATM-BR-076)
3. GIVEN a fetched account is shown, all earlier fields are valid, and the operator enters '*' as the City WHEN the changes are validated THEN the input is rejected with 'City must be supplied.' and the City field is marked blank ('B') (OATM-C09-AC-13; OATM-BR-076)

### Requirement 3: OATM-REQ-F-075 (business rule)

#### Acceptance criteria

1. If a supplied first name, last name, city, state or country contains any character other than the letters A-Z or a-z and spaces, then the system shall reject it with '<field> can have alphabets only.' and mark the field invalid ('0'). (rules OATM-BR-077)
2. GIVEN Last name: Van Dyke WHEN a supplied first name, last name, city, state or country contains any character other than the letters A-Z or a-z and spaces THEN Accepted (OATM-C09-AC-03; OATM-BR-077)

### Requirement 4: OATM-REQ-F-076 (business rule)

#### Acceptance criteria

1. If a supplied middle name contains anything other than letters and spaces, then the system shall reject it with 'Middle Name can have alphabets only.', and the system shall accept a blank middle name. (rules OATM-BR-078)
2. GIVEN Middle name: (blank) WHEN the middle name is left blank THEN Accepted (OATM-C09-AC-04; OATM-BR-078)

### Requirement 5: OATM-REQ-F-077 (business rule)

#### Acceptance criteria

1. If address line 1 is not supplied, then the system shall reject the input with 'Address Line 1 must be supplied.' and mark it blank ('B'), accepting any other content and not checking address line 2 at all. (rules OATM-BR-079)
2. GIVEN Address line 1: 12-B Main St. WHEN address line 1 is not supplied THEN Accepted (OATM-C09-AC-05; OATM-BR-079)

### Requirement 6: OATM-REQ-F-078 (business rule)

#### Acceptance criteria

1. If the state is present and passes the letters-only check but is not one of the valid US state codes, then the system shall reject the change, flag the state as in error, and show 'State: is not a valid state code' if no earlier error message has been set. (rules OATM-BR-080, OATM-BR-081)
2. GIVEN State: XX WHEN the state passes the letters-only check but is not a valid US state code THEN Rejected as an invalid state (OATM-C09-AC-06; OATM-BR-080)
3. GIVEN State: TX WHEN the state passes the letters-only check but is not a valid US state code THEN Accepted (OATM-C09-AC-07; OATM-BR-080)
4. GIVEN State: NY WHEN the state entered is present and alphabetic but is not one of the valid US state codes THEN State accepted by this check (OATM-C09-AC-08; OATM-BR-081)

### Requirement 7: OATM-REQ-F-079 (business rule)

#### Acceptance criteria

1. If the ZIP code (5 positions) is blank, not all digits, or zero, then the system shall reject it with 'ZIP must be supplied.' (flag 'B'), '<field> must be all numeric.' (flag '0') or '<field> must not be zero.' (flag '0') respectively. (rules OATM-BR-082)
2. GIVEN a changed account where all earlier fields are valid and the ZIP is blank WHEN the changes are validated THEN the input is rejected with 'ZIP must be supplied.' and the ZIP is flagged 'B' (OATM-C09-AC-14; OATM-BR-082)
3. GIVEN a changed account where all earlier fields are valid and the ZIP is '12A45' WHEN the changes are validated THEN the input is rejected with '<field> must be all numeric.' naming the ZIP field and the ZIP is flagged '0' (OATM-C09-AC-15; OATM-BR-082)
4. GIVEN a changed account where all earlier fields are valid and the ZIP is '00000' WHEN the changes are validated THEN the input is rejected with '<field> must not be zero.' naming the ZIP field and the ZIP is flagged '0' (OATM-C09-AC-16; OATM-BR-082)

### Requirement 8: OATM-REQ-F-080 (business rule)

#### Acceptance criteria

1. When both the state and the ZIP code have passed their own edits, the system shall check that the state together with the first two digits of the ZIP code is a known valid state/ZIP-prefix combination. (rules OATM-BR-083)
2. GIVEN State: NY; ZIP: 10001 WHEN both the state and the ZIP code have passed their own edits THEN 'NY10' is a valid combination; the address passes the cross-check (OATM-C09-AC-09; OATM-BR-083)
3. GIVEN State: XX; ZIP: 90210 WHEN both the state and the ZIP code have passed their own edits THEN Cross-check is not performed because the state already failed its own edit (OATM-C09-AC-10; OATM-BR-083)

### Requirement 9: OATM-REQ-F-081 (business rule)

#### Acceptance criteria

1. If the state and first two ZIP digits are not a valid combination, then the system shall reject the change, flag both the state and the ZIP code as in error, and show 'Invalid zip code for state' if no earlier error message has been set. (rules OATM-BR-084)
2. GIVEN State: NY; ZIP: 90210 WHEN the state and first two ZIP digits are not a valid combination THEN Change rejected with 'Invalid zip code for state'; state and ZIP both flagged (OATM-C09-AC-11; OATM-BR-084)
