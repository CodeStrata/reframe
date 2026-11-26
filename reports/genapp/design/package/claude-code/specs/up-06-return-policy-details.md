# Return policy details (UP-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk high

## Introduction

Returns the full details of an endowment, house, motor or commercial policy, so customer service users can answer questions about cover, dates and premiums. A policy must be returned only when its policy number belongs to the given customer number and it has details of the requested type. An empty broker ID or payment must come back as zero, and commercial dates must be reported as issue (start date), expiry (renewal date) and last-changed (request date).

**User story:** As a customer service user, I want the details of a customer's endowment, house, motor or commercial policy returned to me, so that I can answer questions about the policy's cover, dates and premiums.

## Requirements

### Requirement 1: UP-REQ-F-030 (business rule)

#### Acceptance criteria

1. When an endowment ('01IEND'), house ('01IHOU'), motor ('01IMOT') or commercial ('01ICOM') policy inquiry is made, the system shall return the policy only when the policy number belongs to the given customer number and the policy has details of the requested type. (rules UP-BR-051, UP-BR-052)
2. GIVEN request: '01IHOU'; customer number: 0000000001; policy number: 0000000005 (a house policy of customer 1) WHEN an endowment ('01IEND'), house ('01IHOU'), motor ('01IMOT') or commercial ('01ICOM') policy inquiry is made THEN The house policy details are returned with return code '00'. (UP-C06-AC-01; UP-BR-051)
3. GIVEN request: '01IHOU'; customer number: 0000000001; policy number: 0000000009 (owned by another customer) WHEN an endowment ('01IEND'), house ('01IHOU'), motor ('01IMOT') or commercial ('01ICOM') policy inquiry is made THEN No policy is returned; return code '01'. (UP-C06-AC-02; UP-BR-051)
4. GIVEN Request: '01IEND'; Customer number: 0000000001; Policy number: 0000000005 (an endowment policy owned by customer 0000000001) WHEN an endowment policy inquiry (request '01IEND') is made THEN The endowment policy is found and its details are prepared for return. (UP-C06-AC-03; UP-BR-052)

### Requirement 2: UP-REQ-F-031 (business rule)

#### Acceptance criteria

1. When an endowment policy inquiry ('01IEND') is made, the system shall read the common policy details together with the endowment details. (rules UP-BR-052)
2. GIVEN Request: '01IEND'; Customer number: 0000000001; Policy number: 0000000005 (an endowment policy owned by customer 0000000001) WHEN an endowment policy inquiry (request '01IEND') is made THEN The endowment policy is found and its details are prepared for return. (UP-C06-AC-03; UP-BR-052)

### Requirement 3: UP-REQ-F-032 (design note)

#### Acceptance criteria

1. When a policy is found, the system shall work out the reply length needed as 33 bytes of header plus the policy length for its type: endowment 124 plus the length of any padding data, house 130, motor 137, commercial 1174. (rules UP-BR-053, UP-BR-054)
2. GIVEN request: '01IMOT'; policy found: yes WHEN the policy is found THEN Required reply length is 170 (33 + 137). (UP-C06-AC-04; UP-BR-053)
3. GIVEN request: '01IHOU'; policy found: yes WHEN the policy is found THEN Required reply length is 163 (33 + 130). (UP-C06-AC-05; UP-BR-053)
4. GIVEN Padding data length: 40 WHEN an endowment policy is found THEN Space needed is 33 + 124 + 40 = 197 bytes. (UP-C06-AC-06; UP-BR-054)
5. GIVEN Padding data: absent (null) WHEN an endowment policy is found THEN Space needed is 33 + 124 = 157 bytes. (UP-C06-AC-07; UP-BR-054)

### Requirement 4: UP-REQ-F-033 (business rule)

#### Acceptance criteria

1. When an endowment policy is found and the caller's area is large enough, the system shall return the common policy details and the 52 characters of fixed endowment details, with term and sum assured as whole numbers, and the padding data when it is present. (rules UP-BR-055)
2. GIVEN Term: 25; Sum assured: 100000; Padding data: absent WHEN an endowment policy is found and the caller's area is large enough THEN The reply carries the issue, expiry and last-changed dates, term 25, sum assured 100000 and the endowment flags, fund name and life assured; no padding data is returned. (UP-C06-AC-08; UP-BR-055)

### Requirement 5: UP-REQ-F-034 (design note)

#### Acceptance criteria

1. When an endowment policy is found and returned, the system shall write the end-of-data marker 'FINAL' in the padding area straight after the padding data, at position 1 plus the padding length (position 1 when there is no padding). (rules UP-BR-056)
2. GIVEN Padding data length: 40 WHEN an endowment policy is found and returned THEN 'FINAL' is written at positions 41-45 of the padding area. (UP-C06-AC-09; UP-BR-056)
3. GIVEN Padding data: absent (null) WHEN an endowment policy is found and returned THEN 'FINAL' is written at positions 1-5 of the padding area. (UP-C06-AC-10; UP-BR-056)

### Requirement 6: UP-REQ-F-035 (business rule)

#### Acceptance criteria

1. When a motor policy is found and the caller's area is large enough, the system shall return the common policy details, the 65 bytes of motor details, and the premium and accident count. (rules UP-BR-057)
2. GIVEN Make: FORD; Premium: 450; Accidents: 1 WHEN a motor policy is found and the caller's area is large enough THEN The reply carries the vehicle details, premium 450 and accident count 1. (UP-C06-AC-11; UP-BR-057)

### Requirement 7: UP-REQ-F-036 (business rule)

#### Acceptance criteria

1. When an endowment or motor policy is returned and its broker ID or payment is empty in the database, the system shall return that value as zero, and otherwise return the stored value. (rules UP-BR-058)
2. GIVEN Broker ID: empty (null); Payment: 250 WHEN an endowment or motor policy is returned and its broker ID or payment is empty in the database THEN Broker ID is returned as 0000000000 and payment as 000250. (UP-C06-AC-12; UP-BR-058)
3. GIVEN Broker ID: 1234567890; Payment: empty (null) WHEN an endowment or motor policy is returned and its broker ID or payment is empty in the database THEN Broker ID 1234567890 is returned and payment as 000000. (UP-C06-AC-13; UP-BR-058)

### Requirement 8: UP-REQ-F-037 (business rule)

#### Acceptance criteria

1. When a commercial policy inquiry by customer and policy number ('01ICOM') finds a matching policy, the system shall return the policy dates and the address, postcode, latitude, longitude, customer name, property type, the fire, crime, flood and weather peril and premium values, the status and the rejection reason. (rules UP-BR-059)
2. GIVEN request: '01ICOM'; customer number: 1; policy number: 7 WHEN a commercial policy inquiry by customer and policy number ('01ICOM') finds a matching policy THEN Return code '00'; the commercial details of policy 7 are returned. (UP-C06-AC-14; UP-BR-059)

### Requirement 9: UP-REQ-F-038 (formatting)

#### Acceptance criteria

1. When a commercial policy is returned by any commercial inquiry ('01ICOM', '02ICOM', '03ICOM', '05ICOM'), the system shall report the stored request date as the last-changed date, the start date as the issue date and the renewal date as the expiry date. (rules UP-BR-060)
2. GIVEN request date: 2024-01-10; start date: 2024-02-01; renewal date: 2025-02-01 WHEN a commercial policy is returned by any commercial inquiry ('01ICOM', '02ICOM', '03ICOM', '05ICOM') THEN Last changed 2024-01-10, issue date 2024-02-01, expiry date 2025-02-01. (UP-C06-AC-15; UP-BR-060)

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGIPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGIPDB01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-051 | Retrieve house policy and size reply | business rule | WHEN an endowment ('01IEND'), house ('01IHOU'), motor ('01IMOT') or commercial ('01ICOM') policy inquiry is made, THE Policy Inquiry SHALL return the policy only when the policy number belongs to the given customer number and the policy has details of the requested type. | high | base/src/lgipdb01.cbl:327-431, base/src/lgipdb01.cbl:441-523, base/src/lgipdb01.cbl:529-621, base/src/lgipdb01.cbl:627-724 |
| UP-BR-052 | Retrieve endowment policy and size response | business rule | WHEN an endowment policy inquiry (request '01IEND') is made, THE Policy Inquiry SHALL look up the policy only where the policy number belongs to the requested customer number, reading the common policy details together with the endowment details. | high | base/src/lgipdb01.cbl:327-368, base/src/lgipdb01.cbl:370-417, base/src/lgipdb01.cbl:73, base/src/lgipdb01.cbl:78 |
| UP-BR-053 | Retrieve house policy and size reply | design note | WHEN the policy is found, THE Policy Inquiry SHALL work out the reply length needed as 33 bytes of header plus the policy length for its type: endowment 124 plus the length of any padding data, house 130, motor 137, commercial 1174. | high | base/src/lgipdb01.cbl:327-431, base/src/lgipdb01.cbl:441-523, base/src/lgipdb01.cbl:529-621, base/src/lgipdb01.cbl:627-724 |
| UP-BR-054 | Retrieve endowment policy and size response | design note | WHEN an endowment policy is found, THE Policy Inquiry SHALL work out the space needed for the reply as 33 bytes of header plus 124 bytes of policy data plus the length of the policy's free-form padding data when that data is present. | high | base/src/lgipdb01.cbl:327-368, base/src/lgipdb01.cbl:370-417, base/src/lgipdb01.cbl:73, base/src/lgipdb01.cbl:78 |
| UP-BR-055 | Return endowment details to caller | business rule | WHEN an endowment policy is found and the caller's area is large enough, THE Policy Inquiry SHALL return the common policy details and the 52 characters of fixed endowment details, with term and sum assured as whole numbers, and the padding data when it is present. | high | base/src/lgipdb01.cbl:243-245, base/src/lgipdb01.cbl:393-414, base/src/lgipdb01.cbl:584-603, base/src/lgpolicy.cpy:41-73 |
| UP-BR-056 | Mark end of endowment policy data | design note | WHEN an endowment policy is found and returned, THE Policy Inquiry SHALL write the end-of-data marker 'FINAL' in the padding area straight after the padding data, at position 1 plus the padding length (position 1 when there is no padding). | high | base/src/lgipdb01.cbl:327-368, base/src/lgipdb01.cbl:370-417, base/src/lgipdb01.cbl:73, base/src/lgipdb01.cbl:78 |
| UP-BR-057 | Return motor policy details to caller | business rule | WHEN a motor policy is found and the caller's area is large enough, THE Policy Inquiry SHALL return the common policy details, the 65 bytes of motor details, and the premium and accident count. | high | base/src/lgipdb01.cbl:243-245, base/src/lgipdb01.cbl:393-414, base/src/lgipdb01.cbl:584-603, base/src/lgpolicy.cpy:41-73 |
| UP-BR-058 | Return endowment details to caller | business rule | WHEN an endowment or motor policy is returned and its broker ID or payment is empty in the database, THE Policy Inquiry SHALL return that value as zero; otherwise it SHALL return the stored value. | high | base/src/lgipdb01.cbl:243-245, base/src/lgipdb01.cbl:393-414, base/src/lgipdb01.cbl:584-603, base/src/lgpolicy.cpy:41-73 |
| UP-BR-059 | Return commercial policy by customer and policy | business rule | WHEN a commercial policy inquiry by customer and policy number ('01ICOM') finds a matching policy, THE Commercial Policy Inquiry SHALL return the policy dates and the address, postcode, latitude, longitude, customer name, property type, the fire, crime, flood and weather peril and premium values, the status and the rejection reason. | high | base/src/lgipdb01.cbl:627-708, base/src/lgipdb01.cbl:808-813, base/src/lgpolicy.cpy:83-99, base/src/lgcmarea.cpy:78-94 |
| UP-BR-060 | Commercial policy dates mapped from request/start/renewal dates | formatting | WHEN a commercial policy is returned by any commercial inquiry ('01ICOM', '02ICOM', '03ICOM', '05ICOM'), THE Commercial Policy Inquiry SHALL report the stored request date as the last-changed date, the start date as the issue date and the renewal date as the expiry date. | medium | base/src/lgipdb01.cbl:631-654, base/src/lgipdb01.cbl:734-760, base/src/lgipdb01.cbl:865-872, base/src/lgipdb01.cbl:946-954 |

### Worked examples

- UP-BR-051: request = '01IHOU'; customer number = 0000000001; policy number = 0000000005 (a house policy of customer 1) → The house policy details are returned with return code '00'.
- UP-BR-051: request = '01IHOU'; customer number = 0000000001; policy number = 0000000009 (owned by another customer) → No policy is returned; return code '01'.
- UP-BR-052: Request = '01IEND'; Customer number = 0000000001; Policy number = 0000000005 (an endowment policy owned by customer 0000000001) → The endowment policy is found and its details are prepared for return.
- UP-BR-053: request = '01IMOT'; policy found = yes → Required reply length is 170 (33 + 137).
- UP-BR-053: request = '01IHOU'; policy found = yes → Required reply length is 163 (33 + 130).
- UP-BR-054: Padding data length = 40 → Space needed is 33 + 124 + 40 = 197 bytes.
- UP-BR-054: Padding data = absent (null) → Space needed is 33 + 124 = 157 bytes.
- UP-BR-055: Term = 25; Sum assured = 100000; Padding data = absent → The reply carries the issue, expiry and last-changed dates, term 25, sum assured 100000 and the endowment flags, fund name and life assured; no padding data is returned.
- UP-BR-056: Padding data length = 40 → 'FINAL' is written at positions 41-45 of the padding area.
- UP-BR-056: Padding data = absent (null) → 'FINAL' is written at positions 1-5 of the padding area.
- UP-BR-057: Make = FORD; Premium = 450; Accidents = 1 → The reply carries the vehicle details, premium 450 and accident count 1.
- UP-BR-058: Broker ID = empty (null); Payment = 250 → Broker ID is returned as 0000000000 and payment as 000250.
- UP-BR-058: Broker ID = 1234567890; Payment = empty (null) → Broker ID 1234567890 is returned and payment as 000000.
- UP-BR-059: request = '01ICOM'; customer number = 1; policy number = 7 → Return code '00'; the commercial details of policy 7 are returned.
- UP-BR-060: request date = 2024-01-10; start date = 2024-02-01; renewal date = 2025-02-01 → Last changed 2024-01-10, issue date 2024-02-01, expiry date 2025-02-01.

## Decision tables

None.

## Design notes

- UP-BR-053: Before replying, the inquiry works out the space the reply needs: 33 bytes of header plus the length for the policy type. That is 124 for endowment plus any padding data, 130 for house, 137 for motor and 1174 for commercial. In a message-based API this becomes a check that the reply fits the caller's limit, with '98' when it does not.
- UP-BR-054: For an endowment policy, the space needed is 33 + 124 bytes plus the length of the policy's free-form padding data when present. The padding length must be read with the policy, so the size check and the reply use the same value.
- UP-BR-056: An endowment reply ends with the end-of-data marker 'FINAL', written straight after the padding data: at position 1 plus the padding length, or position 1 when there is none. Callers use it to find where the policy data ends. An API with explicit field lengths may not need it, but it must stay while existing callers read it.

## Open questions

- SME-059: When commercial policies are listed by customer (03ICOM) or by postcode (05ICOM), should the caller get every matching policy or only one? Should the list by customer stop at 20 policies (today a 21st can slip through), and should the postcode search also be limited? (Commercial underwriting SME) On UP-BR-056, UP-BR-051, UP-BR-053, UP-BR-058, UP-BR-059.
- SME-060: When a policy has no broker or payment recorded, should the inquiry return zero, or show it as 'not set'? Should a missing broker reference be handled the same way? (Policy administration lead) On UP-BR-058.
- SME-061: A commercial policy inquiry reports the policy's request date as its 'last changed' time, which is used elsewhere to stop two people overwriting each other's changes. Is that intended, or should 'last changed' come from the main policy record? (Data architect / DBA) On UP-BR-060.
- DEF-017: Confirm this is deliberate: The '98' reply-too-small check can never trigger: the only caller, LGIPOL01, always passes a 32500-byte area, far more than the 1207 bytes needed. (Subject-matter expert) On UP-BR-059.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).
