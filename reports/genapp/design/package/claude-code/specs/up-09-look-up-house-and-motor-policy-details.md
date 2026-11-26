# Look up house and motor policy details (UP-C09)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGIPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGIPDB01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-073 | Return house policy details with end marker | business rule | WHEN a house policy inquiry ('01IHOU') finds a policy matching both the customer number and the policy number, THE House Policy Inquiry SHALL return the issue, expiry and last-changed dates, broker's reference, property type, bedrooms, value, house name, house number and postcode. | high | base/src/lgipdb01.cbl:441-508, base/src/lgipdb01.cbl:529-606, base/src/lgipdb01.cbl:243-245, base/src/lgpolicy.cpy:42-51 |
| UP-BR-074 | Return house policy details with end marker | business rule | WHEN a house or motor policy is returned, THE Policy Inquiry SHALL return the broker id and the payment only when they are recorded on the policy; when either is empty (null) it SHALL be returned as zero. | high | base/src/lgipdb01.cbl:441-508, base/src/lgipdb01.cbl:529-606, base/src/lgipdb01.cbl:243-245, base/src/lgpolicy.cpy:42-51 |
| UP-BR-075 | Return house policy details with end marker | design note | WHEN house policy data has been returned, THE House Policy Inquiry SHALL write 'FINAL' in the first 5 positions of the free space straight after the house details, marking the end of the policy data. | high | base/src/lgipdb01.cbl:441-508, base/src/lgipdb01.cbl:529-606, base/src/lgipdb01.cbl:243-245, base/src/lgpolicy.cpy:42-51 |
| UP-BR-076 | Mark end of motor policy data | design note | WHEN motor policy data has been returned, THE Motor Policy Inquiry SHALL write 'FINAL' in the first 5 positions of the free space straight after the motor details (after the accidents count), marking the end of the policy data. | high | base/src/lgipdb01.cbl:441-508, base/src/lgipdb01.cbl:529-606, base/src/lgipdb01.cbl:243-245, base/src/lgpolicy.cpy:42-51 |

### Worked examples

- UP-BR-074: request = '01IHOU'; stored broker id = null; stored payment = 250 → Broker id is returned as 0 and payment as 250.
- UP-BR-074: request = '01IMOT'; stored broker id = 12345; stored payment = null → Broker id 12345 is returned and payment is returned as 0.
- UP-BR-075: request = '01IHOU'; policy found = yes → 'FINAL' follows the postcode in the reply area.
- UP-BR-076: request = '01IMOT'; policy found = yes → 'FINAL' follows the accidents count in the reply area.

## Decision tables

None.

## Design notes

- UP-BR-075: A house reply ends with 'FINAL' in the first 5 positions of the free space straight after the house details. Callers use it to find where the policy data ends.
- UP-BR-076: A motor reply ends with 'FINAL' in the first 5 positions of the free space straight after the motor details, after the accidents count. Callers use it to find where the policy data ends.

## Open questions

- SME-059: When commercial policies are listed by customer (03ICOM) or by postcode (05ICOM), should the caller get every matching policy or only one? Should the list by customer stop at 20 policies (today a 21st can slip through), and should the postcode search also be limited? (Commercial underwriting SME) On UP-BR-075, UP-BR-076.
- SME-064: A policy inquiry ends its policy data with a 'FINAL' marker, but the evidence cited for this rule turned out to come from the endowment inquiry. Which policy types should end with this marker, and do the systems that receive the data rely on it? (Subject-matter expert) On UP-BR-076.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).
