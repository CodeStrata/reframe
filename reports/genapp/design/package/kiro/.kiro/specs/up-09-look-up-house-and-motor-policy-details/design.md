# Design: Look up house and motor policy details (UP-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Returns a house or motor policy to policy administrators: its dates, broker, payment and property or vehicle details. A house policy must be returned only when both the customer number and the policy number match. An empty broker ID or payment must come back as zero.

Runs as scheduled job.

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