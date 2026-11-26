# Requirements: Route policy inquiries by request type (UP-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk medium

## Introduction

Sends each policy inquiry to the right lookup for its request ID. The lookups are endowment, house, motor, and four commercial searches: by customer and policy, by policy number alone, by customer, and by postcode. The request ID must match in any letter case. Any ID other than '01IEND', '01IHOU', '01IMOT', '01ICOM', '02ICOM', '03ICOM' or '05ICOM' must get code '99' and no policy data.

**User story:** As a customer service user, I want my policy inquiry routed to the right lookup for the policy type I ask for, so that I get the correct endowment, house, motor or commercial policy information.

## Requirements

### Requirement 1: UP-REQ-F-014 (design note)

#### Acceptance criteria

1. When a policy inquiry is received with a request, the system shall start with return code '00', which is returned unless a later step sets another code, and use the supplied customer number and policy number as the lookup keys, keeping both for any error message it writes. (rules UP-BR-034, UP-BR-035)
2. GIVEN request: '01IHOU'; policy found: yes WHEN Policy Inquiry runs THEN Return code '00'. (UP-C04-AC-01; UP-BR-034)
3. GIVEN customer number: 0000000001; policy number: 0000000005; request ID: 01IMOT WHEN a policy inquiry is received with a request THEN Return code starts as '00' and customer 0000000001 / policy 0000000005 are used for the motor lookup (UP-C04-AC-02; UP-BR-035)

### Requirement 2: UP-REQ-F-015 (business rule)

#### Acceptance criteria

1. The system shall match the policy inquiry request ID regardless of letter case, converting it to upper case before choosing the lookup. (rules UP-BR-036)
2. GIVEN request ID: 01ihou WHEN Policy Inquiry service runs THEN Treated as '01IHOU' and a house policy lookup is performed (UP-C04-AC-03; UP-BR-036)

### Requirement 3: UP-REQ-F-016 (business rule)

#### Acceptance criteria

1. If the request ID, after upper-casing, is not '01IEND', '01IHOU', '01IMOT', '01ICOM', '02ICOM', '03ICOM' or '05ICOM', then the system shall return code '99' and perform no lookup, returning no policy data. (rules UP-BR-037)
2. GIVEN request ID: 04ICOM WHEN the request ID, after upper-casing, is not '01IEND', '01IHOU', '01IMOT', '01ICOM', '02ICOM', '03ICOM' or '05ICOM' THEN Return code '99'; no policy data returned (UP-C04-AC-04; UP-BR-037)
3. GIVEN request ID: 01IXYZ WHEN the request ID, after upper-casing, is not '01IEND', '01IHOU', '01IMOT', '01ICOM', '02ICOM', '03ICOM' or '05ICOM' THEN Return code '99'; no policy data returned (UP-C04-AC-05; UP-BR-037)

### Requirement 4: UP-REQ-F-017 (business rule)

#### Acceptance criteria

1. When the request ID is '01IEND', the system shall clear the endowment details and retrieve the endowment policy for the given customer and policy number. (rules UP-BR-038)
2. GIVEN request ID: 01IEND; customer number: 0000000001; policy number: 0000000002 WHEN the request ID is '01IEND' THEN Endowment details of policy 0000000002 for customer 0000000001 are retrieved (UP-C04-AC-06; UP-BR-038)

### Requirement 5: UP-REQ-F-018 (business rule)

#### Acceptance criteria

1. When the request ID is '01IHOU', the system shall clear the house details and retrieve the house policy for the given customer and policy number. (rules UP-BR-039)
2. GIVEN request ID: 01IHOU; customer number: 0000000001; policy number: 0000000003 WHEN the request ID is '01IHOU' THEN House details of policy 0000000003 for customer 0000000001 are retrieved (UP-C04-AC-07; UP-BR-039)

### Requirement 6: UP-REQ-F-019 (business rule)

#### Acceptance criteria

1. When the request ID is '01IMOT', the system shall clear the motor details and retrieve the motor policy for the given customer and policy number. (rules UP-BR-040)
2. GIVEN request ID: 01IMOT; customer number: 0000000001; policy number: 0000000004 WHEN the request ID is '01IMOT' THEN Motor details of policy 0000000004 for customer 0000000001 are retrieved (UP-C04-AC-08; UP-BR-040)

### Requirement 7: UP-REQ-F-020 (business rule)

#### Acceptance criteria

1. When the request ID is '01ICOM', the system shall clear the commercial details and retrieve the commercial policy matching both the given customer number and policy number. (rules UP-BR-041)
2. GIVEN request ID: 01ICOM; customer number: 0000000001; policy number: 0000000006 WHEN the request ID is '01ICOM' THEN Commercial policy 0000000006 of customer 0000000001 is retrieved (UP-C04-AC-09; UP-BR-041)

### Requirement 8: UP-REQ-F-021 (business rule)

#### Acceptance criteria

1. When the request ID is '02ICOM', the system shall clear the commercial details and retrieve the commercial policy by policy number alone, whatever customer number is supplied. (rules UP-BR-042)
2. GIVEN request ID: 02ICOM; policy number: 0000000006 WHEN the request ID is '02ICOM' THEN Commercial policy 0000000006 is retrieved without checking the customer (UP-C04-AC-10; UP-BR-042)

### Requirement 9: UP-REQ-F-022 (business rule)

#### Acceptance criteria

1. When the request ID is '03ICOM', the system shall clear the commercial details and retrieve the list of commercial policies held by the given customer number. (rules UP-BR-043)
2. GIVEN request ID: 03ICOM; customer number: 0000000001 WHEN the request ID is '03ICOM' THEN All commercial policies of customer 0000000001 are listed (UP-C04-AC-11; UP-BR-043)

### Requirement 10: UP-REQ-F-023 (business rule)

#### Acceptance criteria

1. When the request ID is '05ICOM', the system shall clear the commercial details and retrieve the list of commercial policies whose property postcode equals the supplied postcode (CA-B-POSTCODE). (rules UP-BR-044)
2. GIVEN request ID: 05ICOM; postcode: PO167GZ WHEN the request ID is '05ICOM' THEN All commercial policies with postcode PO167GZ are listed (UP-C04-AC-12; UP-BR-044)
