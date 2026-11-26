# Requirements: Return policy details (UP-C06)

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
