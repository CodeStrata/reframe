# Requirements: Validate account flags and EFT account (OATM-C12)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Checks the account status and primary card holder flags and the EFT account id when the operator changes account details. Both flags must be supplied as Y or N, and the EFT account id must be ten digits and not zero. A missing or malformed flag or funds-transfer account must never be saved, and the cursor goes to the field in error.

**User story:** As an operator, I want the account status, primary card holder indicator and EFT account id checked, so that only valid flags and a well-formed funds transfer account are saved.

## Requirements

### Requirement 1: OATM-REQ-F-103 (design note)

#### Acceptance criteria

1. When the operator submits account changes and leaves the Account Status or Primary Card Holder entry blank or as '*', the system shall treat that entry as not supplied (low-values) rather than as a value to save. (rules OATM-BR-107)
2. GIVEN Account Status entry: '*' WHEN the operator submits account changes and leaves the Account Status or Primary Card Holder entry blank or as '*' THEN Account Status is treated as not supplied (OATM-C12-AC-01; OATM-BR-107)
3. GIVEN Primary Card Holder entry: 'Y' WHEN the operator submits account changes and leaves the Account Status or Primary Card Holder entry blank or as '*' THEN 'Y' is taken as the proposed Primary Card Holder value (OATM-C12-AC-02; OATM-BR-107)

### Requirement 2: OATM-REQ-F-104 (business rule)

#### Acceptance criteria

1. If changed account details are validated and the Account Status or Primary Card Holder value is not supplied (blank, low-values or '0'), then the system shall reject the input with '<field> must be supplied.' (e.g. 'Account Status must be supplied.', 'Primary Card Holder must be supplied.') and place the cursor on that field. (rules OATM-BR-108, OATM-BR-087)
2. GIVEN Phone number 2: (blank) WHEN account update runs THEN Accepted (OATM-C12-AC-03; OATM-BR-087)

### Requirement 3: OATM-REQ-F-105 (business rule)

#### Acceptance criteria

1. If changed account details are validated and a supplied Account Status or Primary Card Holder value is anything other than 'Y' or 'N', then the system shall reject the input with '<field> must be Y or N.' (e.g. 'Account Status must be Y or N.', 'Primary Card Holder must be Y or N.') and place the cursor on that field. (rules OATM-BR-109, OATM-BR-087)
2. GIVEN Phone number 2: (blank) WHEN account update runs THEN Accepted (OATM-C12-AC-03; OATM-BR-087)
3. GIVEN Account Status: 'N' WHEN changed account details are validated and a supplied Account Status or Primary Card Holder value is anything other than 'Y' or 'N' THEN Accepted (OATM-C12-AC-04; OATM-BR-109)

### Requirement 4: OATM-REQ-F-106 (business rule)

#### Acceptance criteria

1. If the EFT account id (10 positions) is blank, not all digits, or zero, then the system shall reject it with '<field> must be supplied.' (flag 'B'), '<field> must be all numeric.' (flag '0') or '<field> must not be zero.' (flag '0') respectively. (rules OATM-BR-082, OATM-BR-074)
2. GIVEN Middle name entry: * WHEN the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, or EFT account id on the account update screen THEN The middle name is treated as not supplied (OATM-C12-AC-05; OATM-BR-074)
