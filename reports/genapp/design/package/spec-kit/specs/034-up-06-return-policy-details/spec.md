# Feature specification: Return policy details

**Feature:** UP-C06 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C06)

As a customer service user, I want the details of a customer's endowment, house, motor or commercial policy returned to me, so that I can answer questions about the policy's cover, dates and premiums.

Returns the full details of an endowment, house, motor or commercial policy, so customer service users can answer questions about cover, dates and premiums. A policy must be returned only when its policy number belongs to the given customer number and it has details of the requested type. An empty broker ID or payment must come back as zero, and commercial dates must be reported as issue (start date), expiry (renewal date) and last-changed (request date).

**Acceptance scenarios:**

1. **Given** request: '01IHOU'; customer number: 0000000001; policy number: 0000000005 (a house policy of customer 1), **when** an endowment ('01IEND'), house ('01IHOU'), motor ('01IMOT') or commercial ('01ICOM') policy inquiry is made, **then** The house policy details are returned with return code '00'. (UP-C06-AC-01)
2. **Given** request: '01IHOU'; customer number: 0000000001; policy number: 0000000009 (owned by another customer), **when** an endowment ('01IEND'), house ('01IHOU'), motor ('01IMOT') or commercial ('01ICOM') policy inquiry is made, **then** No policy is returned; return code '01'. (UP-C06-AC-02)
3. **Given** Request: '01IEND'; Customer number: 0000000001; Policy number: 0000000005 (an endowment policy owned by customer 0000000001), **when** an endowment policy inquiry (request '01IEND') is made, **then** The endowment policy is found and its details are prepared for return. (UP-C06-AC-03)
4. **Given** request: '01IMOT'; policy found: yes, **when** the policy is found, **then** Required reply length is 170 (33 + 137). (UP-C06-AC-04)
5. **Given** request: '01IHOU'; policy found: yes, **when** the policy is found, **then** Required reply length is 163 (33 + 130). (UP-C06-AC-05)
6. **Given** Padding data length: 40, **when** an endowment policy is found, **then** Space needed is 33 + 124 + 40 = 197 bytes. (UP-C06-AC-06)
7. **Given** Padding data: absent (null), **when** an endowment policy is found, **then** Space needed is 33 + 124 = 157 bytes. (UP-C06-AC-07)
8. **Given** Term: 25; Sum assured: 100000; Padding data: absent, **when** an endowment policy is found and the caller's area is large enough, **then** The reply carries the issue, expiry and last-changed dates, term 25, sum assured 100000 and the endowment flags, fund name and life assured; no padding data is returned. (UP-C06-AC-08)
9. **Given** Padding data length: 40, **when** an endowment policy is found and returned, **then** 'FINAL' is written at positions 41-45 of the padding area. (UP-C06-AC-09)
10. **Given** Padding data: absent (null), **when** an endowment policy is found and returned, **then** 'FINAL' is written at positions 1-5 of the padding area. (UP-C06-AC-10)
11. **Given** Make: FORD; Premium: 450; Accidents: 1, **when** a motor policy is found and the caller's area is large enough, **then** The reply carries the vehicle details, premium 450 and accident count 1. (UP-C06-AC-11)
12. **Given** Broker ID: empty (null); Payment: 250, **when** an endowment or motor policy is returned and its broker ID or payment is empty in the database, **then** Broker ID is returned as 0000000000 and payment as 000250. (UP-C06-AC-12)
13. **Given** Broker ID: 1234567890; Payment: empty (null), **when** an endowment or motor policy is returned and its broker ID or payment is empty in the database, **then** Broker ID 1234567890 is returned and payment as 000000. (UP-C06-AC-13)
14. **Given** request: '01ICOM'; customer number: 1; policy number: 7, **when** a commercial policy inquiry by customer and policy number ('01ICOM') finds a matching policy, **then** Return code '00'; the commercial details of policy 7 are returned. (UP-C06-AC-14)
15. **Given** request date: 2024-01-10; start date: 2024-02-01; renewal date: 2025-02-01, **when** a commercial policy is returned by any commercial inquiry ('01ICOM', '02ICOM', '03ICOM', '05ICOM'), **then** Last changed 2024-01-10, issue date 2024-02-01, expiry date 2025-02-01. (UP-C06-AC-15)

## Requirements

### Functional requirements

- **UP-REQ-F-030** (business rule): When an endowment ('01IEND'), house ('01IHOU'), motor ('01IMOT') or commercial ('01ICOM') policy inquiry is made, the system shall return the policy only when the policy number belongs to the given customer number and the policy has details of the requested type. Rules: UP-BR-051, UP-BR-052.
- **UP-REQ-F-031** (business rule): When an endowment policy inquiry ('01IEND') is made, the system shall read the common policy details together with the endowment details. Rules: UP-BR-052.
- **UP-REQ-F-032** (design note): When a policy is found, the system shall work out the reply length needed as 33 bytes of header plus the policy length for its type: endowment 124 plus the length of any padding data, house 130, motor 137, commercial 1174. Rules: UP-BR-053, UP-BR-054.
- **UP-REQ-F-033** (business rule): When an endowment policy is found and the caller's area is large enough, the system shall return the common policy details and the 52 characters of fixed endowment details, with term and sum assured as whole numbers, and the padding data when it is present. Rules: UP-BR-055.
- **UP-REQ-F-034** (design note): When an endowment policy is found and returned, the system shall write the end-of-data marker 'FINAL' in the padding area straight after the padding data, at position 1 plus the padding length (position 1 when there is no padding). Rules: UP-BR-056.
- **UP-REQ-F-035** (business rule): When a motor policy is found and the caller's area is large enough, the system shall return the common policy details, the 65 bytes of motor details, and the premium and accident count. Rules: UP-BR-057.
- **UP-REQ-F-036** (business rule): When an endowment or motor policy is returned and its broker ID or payment is empty in the database, the system shall return that value as zero, and otherwise return the stored value. Rules: UP-BR-058.
- **UP-REQ-F-037** (business rule): When a commercial policy inquiry by customer and policy number ('01ICOM') finds a matching policy, the system shall return the policy dates and the address, postcode, latitude, longitude, customer name, property type, the fire, crime, flood and weather peril and premium values, the status and the rejection reason. Rules: UP-BR-059.
- **UP-REQ-F-038** (formatting): When a commercial policy is returned by any commercial inquiry ('01ICOM', '02ICOM', '03ICOM', '05ICOM'), the system shall report the stored request date as the last-changed date, the start date as the issue date and the renewal date as the expiry date. Rules: UP-BR-060.

### Business rules

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

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- SME-059: When commercial policies are listed by customer (03ICOM) or by postcode (05ICOM), should the caller get every matching policy or only one? Should the list by customer stop at 20 policies (today a 21st can slip through), and should the postcode search also be limited? (Commercial underwriting SME) On UP-BR-056, UP-BR-051, UP-BR-053, UP-BR-058, UP-BR-059.
- SME-060: When a policy has no broker or payment recorded, should the inquiry return zero, or show it as 'not set'? Should a missing broker reference be handled the same way? (Policy administration lead) On UP-BR-058.
- SME-061: A commercial policy inquiry reports the policy's request date as its 'last changed' time, which is used elsewhere to stop two people overwriting each other's changes. Is that intended, or should 'last changed' come from the main policy record? (Data architect / DBA) On UP-BR-060.
- DEF-017: Confirm this is deliberate: The '98' reply-too-small check can never trigger: the only caller, LGIPOL01, always passes a 32500-byte area, far more than the 1207 bytes needed. (Subject-matter expert) On UP-BR-059.

### Decision table gaps

None.
