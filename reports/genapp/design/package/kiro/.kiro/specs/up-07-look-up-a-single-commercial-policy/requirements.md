# Requirements: Look up a single commercial policy (UP-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk high

## Introduction

Returns one commercial policy to policy administrators, found by customer and policy number or by policy number alone. It shows the policy's peril values, premiums, status and owning customer exactly as stored, with no recalculation. When the policy is found by policy number alone, the reply must name the customer who owns it, not the one the caller supplied, and a reply area smaller than 33 + 1174 bytes must get code '98'.

**User story:** As a policy administrator, I want to retrieve a commercial policy by customer and policy number or by policy number alone, so that I can see its stored peril values, premiums, status and owning customer.

## Requirements

### Requirement 1: UP-REQ-F-039 (formatting)

#### Acceptance criteria

1. When a commercial policy is returned, the system shall report the peril values, premiums and status exactly as stored, converted to plain numbers, and the rejection reason as stored text, with no recalculation. (rules UP-BR-061)
2. GIVEN A commercial policy is stored with fire peril 3, fire premium 150, crime peril 2, crime premium 75, flood peril 1, flood premium 40, weather peril 4, weather premium 90, status 1 and rejection reason 'Inspection pending' WHEN The policy is returned by a commercial inquiry THEN The reply holds those values as plain numbers: fire peril 3, fire premium 150, crime peril 2, crime premium 75, flood peril 1, flood premium 40, weather peril 4, weather premium 90 and status 1. The rejection reason is the stored text 'Inspection pending', and nothing is recalculated (UP-C07-AC-07; UP-BR-061)

### Requirement 2: UP-REQ-F-040 (design note)

#### Acceptance criteria

1. When commercial policy data has been returned for a customer-and-policy ('01ICOM') or policy-number ('02ICOM') inquiry, the system shall write 'FINAL' in the first 5 positions of the free space after the rejection reason. (rules UP-BR-062)
2. GIVEN request: '01ICOM'; policy found: yes WHEN commercial policy data has been returned for a customer-and-policy ('01ICOM') or policy-number ('02ICOM') inquiry THEN 'FINAL' follows the rejection reason in the reply area. (UP-C07-AC-01; UP-BR-062)

### Requirement 3: UP-REQ-F-041 (business rule)

#### Acceptance criteria

1. When a commercial policy inquiry by policy number (request '02ICOM') is made, the system shall look up the commercial policy by policy number alone, without checking that it belongs to the customer number supplied. (rules UP-BR-063)
2. GIVEN Request: '02ICOM'; Policy number: 0000000012 (owned by customer 0000000003); Customer number: blank or any other customer WHEN a commercial policy inquiry by policy number (request '02ICOM') is made THEN Policy 0000000012 is found. (UP-C07-AC-02; UP-BR-063)

### Requirement 4: UP-REQ-F-042 (error handling)

#### Acceptance criteria

1. If a commercial policy is found by policy number and the caller's area is smaller than 33 plus 1174 bytes, then the system shall set return code '98' and return without policy details. (rules UP-BR-064)
2. GIVEN Caller's area length: 1000 WHEN a commercial policy is found by policy number THEN Return code '98'; no policy data is returned. (UP-C07-AC-03; UP-BR-064)
3. GIVEN Caller's area length: 32500 WHEN a commercial policy is found by policy number THEN The policy is returned. (UP-C07-AC-04; UP-BR-064)

### Requirement 5: UP-REQ-F-043 (business rule)

#### Acceptance criteria

1. When a commercial policy is found by policy number and the caller's area is large enough, the system shall return the owning customer number in place of the one supplied, with the common policy and commercial details, and mark the end of the data with 'FINAL'. (rules UP-BR-065)
2. GIVEN Commercial policy 0000000005 is owned by customer 0000000003, and the caller's reply area is at least 33 + 1174 bytes WHEN A '02ICOM' inquiry arrives with policy number 0000000005 and customer number 0000000009 THEN The reply carries customer number 0000000003 in place of 0000000009, with the common policy details and commercial details, and the data ends with 'FINAL' (UP-C07-AC-08; UP-BR-065)

### Requirement 6: UP-REQ-F-044 (error handling)

#### Acceptance criteria

1. If the commercial policy lookup by policy number fails for any reason other than the policy not being found, then the system shall set return code '90' and log an error message labelled ' SELECT Commercial ' with the date, time, customer number, policy number and database code, plus up to the first 90 bytes of the request. (rules UP-BR-066)
2. GIVEN Database lookup result: unexpected error (for example SQLCODE -911) WHEN the commercial policy lookup by policy number fails for any reason other than the policy not being found THEN Return code '90'; a ' SELECT Commercial ' error message is written to the error queue. (UP-C07-AC-05; UP-BR-066)
3. GIVEN Database lookup result: no row (SQLCODE 100) WHEN the commercial policy lookup by policy number fails for any reason other than the policy not being found THEN Return code '01'; no error message is logged. (UP-C07-AC-06; UP-BR-066)
