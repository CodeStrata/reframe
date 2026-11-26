# Requirements: Look up house and motor policy details (UP-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk high

## Introduction

Returns a house or motor policy to policy administrators: its dates, broker, payment and property or vehicle details. A house policy must be returned only when both the customer number and the policy number match. An empty broker ID or payment must come back as zero.

**User story:** As a policy administrator, I want to retrieve a house or motor policy's details, so that I can see its dates, broker, payment and property or vehicle information.

## Requirements

### Requirement 1: UP-REQ-F-051 (business rule)

#### Acceptance criteria

1. When a house policy inquiry ('01IHOU') finds a policy matching both the customer number and the policy number, the system shall return the issue, expiry and last-changed dates, broker's reference, property type, bedrooms, value, house name, house number and postcode. (rules UP-BR-073)
2. GIVEN House policy 0000000002 belongs to customer 0000000001 WHEN A '01IHOU' inquiry arrives for customer 0000000001 and policy 0000000002 THEN The reply holds the policy's issue, expiry and last-changed dates, broker's reference, property type, bedrooms, value, house name, house number and postcode (UP-C09-AC-05; UP-BR-073)
3. GIVEN House policy 0000000002 belongs to customer 0000000001 WHEN A '01IHOU' inquiry arrives for customer 0000000007 and policy 0000000002 THEN No house details are returned, because the policy does not match both the customer number and the policy number (UP-C09-AC-06; UP-BR-073)

### Requirement 2: UP-REQ-F-052 (business rule)

#### Acceptance criteria

1. When a house or motor policy is returned, the system shall return the broker id and the payment as recorded on the policy, and shall return either one as zero when it is empty (null). (rules UP-BR-074)
2. GIVEN request: '01IHOU'; stored broker id: null; stored payment: 250 WHEN a house or motor policy is returned THEN Broker id is returned as 0 and payment as 250. (UP-C09-AC-01; UP-BR-074)
3. GIVEN request: '01IMOT'; stored broker id: 12345; stored payment: null WHEN a house or motor policy is returned THEN Broker id 12345 is returned and payment is returned as 0. (UP-C09-AC-02; UP-BR-074)

### Requirement 3: UP-REQ-F-053 (design note)

#### Acceptance criteria

1. When house policy data has been returned, the system shall write 'FINAL' in the first 5 positions of the free space straight after the house details, marking the end of the policy data. (rules UP-BR-075)
2. GIVEN request: '01IHOU'; policy found: yes WHEN house policy data has been returned THEN 'FINAL' follows the postcode in the reply area. (UP-C09-AC-03; UP-BR-075)

### Requirement 4: UP-REQ-F-054 (design note)

#### Acceptance criteria

1. When motor policy data has been returned, the system shall write 'FINAL' in the first 5 positions of the free space straight after the motor details (after the accidents count), marking the end of the policy data. (rules UP-BR-076)
2. GIVEN request: '01IMOT'; policy found: yes WHEN motor policy data has been returned THEN 'FINAL' follows the accidents count in the reply area. (UP-C09-AC-04; UP-BR-076)
