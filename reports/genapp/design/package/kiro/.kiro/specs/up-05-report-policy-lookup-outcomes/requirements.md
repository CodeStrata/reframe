# Requirements: Report policy lookup outcomes (UP-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk high

## Introduction

Tells customer service users and calling applications why a policy could not be returned: '01' when the customer or policy does not match, '98' when the caller's reply area is too small, and '90' when the database failed. A plain not-found must never be logged. Every '90' failure must reach the error log with the customer, policy, lookup and database code, so support staff can investigate.

**User story:** As a customer service user, I want a clear outcome code when a policy cannot be returned, so that I know whether the policy does not exist, my request area was too small, or the system failed, and support staff can investigate failures.

## Requirements

### Requirement 1: UP-REQ-F-024 (error handling)

#### Acceptance criteria

1. If no policy matches the customer number and policy number for the requested policy type, then the system shall set return code '01' (customer or policy not valid) and write no error log. (rules UP-BR-045)
2. GIVEN request: '01IMOT'; customer number: 0000000002; policy number: 0000000777 (does not exist) WHEN no policy matches the customer number and policy number for the requested policy type THEN Return code '01'; no policy data and no error log. (UP-C05-AC-01; UP-BR-045)

### Requirement 2: UP-REQ-F-025 (error handling)

#### Acceptance criteria

1. If a commercial inquiry by policy number alone ('02ICOM') finds no matching policy, then the system shall return code '01'. (rules UP-BR-046)
2. GIVEN request: '02ICOM'; policy number: 9999999999 (not on file) WHEN a commercial inquiry by policy number alone ('02ICOM') finds no matching policy THEN Return code '01'; no policy data is returned. (UP-C05-AC-02; UP-BR-046)

### Requirement 3: UP-REQ-F-026 (error handling)

#### Acceptance criteria

1. If the policy lookup fails for any reason other than no matching policy, then the system shall set return code '90' and write an error log. (rules UP-BR-047)
2. GIVEN request: '01IEND'; database result: unavailable (SQLCODE -904) WHEN the policy lookup fails for any reason other than no matching policy THEN Return code '90' and an error log is written. (UP-C05-AC-03; UP-BR-047)

### Requirement 4: UP-REQ-F-027 (error handling)

#### Acceptance criteria

1. If a commercial inquiry by policy number alone ('02ICOM') fails for any reason other than the policy not existing, then the system shall return code '90' and write an error message with date, time, customer number, policy number and database code to the error log queue. (rules UP-BR-048)
2. GIVEN request: '02ICOM'; database result: SQLCODE -904 (resource unavailable) WHEN a commercial inquiry by policy number alone ('02ICOM') fails for any reason other than the policy not existing THEN Return code '90'; an error message is logged. (UP-C05-AC-04; UP-BR-048)

### Requirement 5: UP-REQ-F-028 (side effect)

#### Acceptance criteria

1. When a policy lookup fails with return code '90', the system shall send the error log program (LGSTSQ) a message with date, time, 'LGIPDB01', customer number, policy number, the lookup label (' SELECT ENDOW ', ' SELECT HOUSE ', ' SELECT MOTOR ' or ' SELECT Commercial ') and the database code, then a second message with up to the first 90 bytes of the request. (rules UP-BR-049)
2. GIVEN A house policy inquiry ('01IHOU') for customer number 0000000001 and policy number 0000000001, where the house policy lookup fails with a database error other than not found WHEN The inquiry sets return code '90' THEN The error log program (LGSTSQ) first receives a message with the date, time, 'LGIPDB01', customer number 0000000001, policy number 0000000001, the label ' SELECT HOUSE ' and the database code. It then receives a second message with up to the first 90 bytes of the request (UP-C05-AC-07; UP-BR-049)
3. GIVEN An endowment, motor or commercial policy inquiry whose lookup fails with return code '90' WHEN The error is logged THEN The first message carries the label ' SELECT ENDOW ', ' SELECT MOTOR ' or ' SELECT Commercial ' to match the lookup, with the date, time, 'LGIPDB01', customer number, policy number and database code. The second message carries up to the first 90 bytes of the request (UP-C05-AC-08; UP-BR-049)

### Requirement 6: UP-REQ-F-029 (error handling)

#### Acceptance criteria

1. If the caller's request area is smaller than the space needed for the endowment reply, then the system shall set return code '98' and return to the caller without any policy details. (rules UP-BR-050)
2. GIVEN Caller's area length: 150; Space needed: 197 WHEN the caller's request area is smaller than the space needed for the endowment reply THEN Return code '98'; no policy data is returned and no 'FINAL' marker is written. (UP-C05-AC-05; UP-BR-050)
3. GIVEN Caller's area length: 200; Space needed: 197 WHEN the caller's request area is smaller than the space needed for the endowment reply THEN The policy data is returned. (UP-C05-AC-06; UP-BR-050)
