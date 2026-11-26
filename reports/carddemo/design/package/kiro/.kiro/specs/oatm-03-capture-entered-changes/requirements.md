# Requirements: Capture entered changes (OATM-C03)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Captures what the operator typed on the Update account screen as proposed new values, treating any field left blank or entered as '*' as not supplied. Amounts entered in currency form are converted to numbers with two decimals. It must never mistake a blank or '*' for a real value to compare or save.

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
