# Feature specification: Record a new policy in the policy file

**Feature:** ADPLM-C11 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C11)

As an insurance policy administrator, I want each new policy written to the policy file under its policy key with its type-specific details, so that the policy can be found by type, customer and policy number.

Writes each new policy to the policy file under a key made of its type letter, customer number and policy number, together with a short summary of its product details, so the policy can be found by type, customer and number. It is for policy administrators. It must never overwrite an existing record: a duplicate key or any other write failure returns code '80' and is logged.

**Acceptance scenarios:**

1. **Given** request code: 01AEND; with-profits: Y; equities: N; managed fund: Y; fund name: GROWTHFUND; life assured: JOHN SMITH, **when** the new policy is an endowment policy (type 'E'), **then** The record holds Y, N, Y, GROWTHFUND and JOHN SMITH (ADPLM-C11-AC-01)
2. **Given** request code: 01AMOT; make: FORD; model: FOCUS; value: 012000; registration: AB12CDE, **when** the new policy is a motor policy (type 'M'), **then** The record holds FORD, FOCUS, 012000 and AB12CDE (ADPLM-C11-AC-02)
3. **Given** policy key: M00000000010000000007; KSDSPOLY: already holds that key, **when** the policy-file write does not succeed for any reason, including a record with the same key already existing, **then** Return code is '80' (ADPLM-C11-AC-03)
4. **Given** KSDSPOLY: file closed, **when** the policy-file write does not succeed for any reason, including a record with the same key already existing, **then** Return code is '80' (ADPLM-C11-AC-04)
5. **Given** An add request with request code '01AMOT' for customer number 0000000005, for which the database has just assigned policy number 0001000012, **when** The policy-file record is built, **then** Its key is 'M00000000050001000012': the type letter 'M' (the 4th character of '01AMOT'), then the 10-digit customer number '0000000005', then the 10-digit policy number '0001000012', 21 characters in all (ADPLM-C11-AC-05)
6. **Given** An add request with request code '01AEND' for customer number 0000000001 and newly assigned policy number 0001000013, **when** The policy-file record is built, **then** Its key starts with 'E' and is 'E00000000010001000013' (ADPLM-C11-AC-06)
7. **Given** A new house policy (type 'H') with property type 'DETACHED', 3 bedrooms, value 250000, postcode 'SO211UP' and house name 'ROSE COTTAGE', **when** The policy-file record is built, **then** It holds property type 'DETACHED' in a 15-character field, bedrooms as 3 digits ('003'), value as 8 digits ('00250000'), postcode 'SO211UP' in an 8-character field, and house name 'ROSE COTT' (only the first 9 characters) (ADPLM-C11-AC-07)
8. **Given** A new commercial policy (type 'C') with postcode 'BB104BX', status 1 and customer name 'Burnley Football Club Stadium Holdings', **when** The policy-file record is built, **then** It holds postcode 'BB104BX' in an 8-character field, status '0001' (4 digits), and customer name 'Burnley Football Club Stadium H' (only the first 31 characters) (ADPLM-C11-AC-08)
9. **Given** The details for new motor policy key 'M00000000050001000012' have been assembled, and no record with that key exists, **when** The policy file update writes the record, **then** A 64-byte record is added to the policy file (KSDSPOLY) and a keyed read of 'M00000000050001000012' returns it (ADPLM-C11-AC-09)
10. **Given** A record with key 'M00000000050001000012' already exists in the policy file, and a new policy with the same key is being written, **when** The policy-file write fails, **then** A message is logged through LGSTSQ with the date, time, program 'LGAPVS01', policy number 0001000012, customer number 0000000005, ' Write file KSDSPOLY' and the RESP and RESP2 codes, followed by a second message 'COMMAREA=' holding the first 90 bytes of the request (ADPLM-C11-AC-10)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-062** (design note): When a new policy is added, the system shall key the policy-file record by the policy type letter (the 4th character of the request code: 'E', 'H', 'M' or 'C'), followed by the 10-digit customer number and the 10-digit policy number the database has just assigned. Rules: ADPLM-BR-067.
- **ADPLM-REQ-F-063** (design note): When the new policy is an endowment policy (type 'E'), the system shall store the with-profits, equities and managed-fund indicators (one character each), the fund name (10 characters) and the life assured name (30 characters) in the policy-file record. Rules: ADPLM-BR-068.
- **ADPLM-REQ-F-064** (design note): When the new policy is a house policy (type 'H'), the system shall store the property type (15 characters), number of bedrooms (3 digits), insured value (8 digits), postcode (8 characters) and only the first 9 characters of the house name in the policy-file record. Rules: ADPLM-BR-069.
- **ADPLM-REQ-F-065** (design note): When the new policy is a motor policy (type 'M'), the system shall store the vehicle make (15 characters), model (15 characters), insured value (6 digits) and registration number (7 characters) in the policy-file record. Rules: ADPLM-BR-070.
- **ADPLM-REQ-F-066** (design note): When the new policy is a commercial policy (type 'C'), the system shall store the premises postcode (8 characters), the status code (4 digits) and the first 31 characters of the customer name in the policy-file record. Rules: ADPLM-BR-071.
- **ADPLM-REQ-F-067** (design note): When the policy details have been assembled, the system shall write a 64-byte record to the policy file (KSDSPOLY) under the 21-character policy key. Rules: ADPLM-BR-072.
- **ADPLM-REQ-F-068** (error handling): If the policy-file write does not succeed for any reason, including a record with the same key already existing, then the system shall set return code '80' and return to its caller at once. Rules: ADPLM-BR-073.
- **ADPLM-REQ-F-069** (side effect): If the policy-file write fails, then the system shall log a message (through LGSTSQ) with the date, time, program 'LGAPVS01', policy number, customer number, ' Write file KSDSPOLY' and the RESP and RESP2 codes, followed by a second message holding the first 90 bytes of the request ('COMMAREA='). Rules: ADPLM-BR-074.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-067 | Build policy record key | design note | WHEN a new policy is added, THE policy file update SHALL key the policy-file record by the policy type letter (the 4th character of the request code: 'E', 'H', 'M' or 'C'), followed by the 10-digit customer number and the 10-digit policy number the database has just assigned. | high | base/src/lgapvs01.cbl:25-46, base/src/lgapvs01.cbl:99-101, base/src/lgapvs01.cbl:117-122, base/src/lgapdb01.cbl:307-313 |
| ADPLM-BR-068 | Populate endowment policy details | design note | WHEN the new policy is an endowment policy (type 'E'), THE policy file update SHALL store the with-profits, equities and managed-fund indicators (one character each), the fund name (10 characters) and the life assured name (30 characters) in the policy-file record. | medium | base/src/lgapvs01.cbl:35-40, base/src/lgapvs01.cbl:110-115 |
| ADPLM-BR-069 | Populate house policy details | design note | WHEN the new policy is a house policy (type 'H'), THE policy file update SHALL store the property type (15 characters), number of bedrooms (3 digits), insured value (8 digits), postcode (8 characters) and only the first 9 characters of the house name in the policy-file record. | high | base/src/lgapvs01.cbl:25-46, base/src/lgapvs01.cbl:99-101, base/src/lgapvs01.cbl:117-122, base/src/lgapdb01.cbl:307-313 |
| ADPLM-BR-070 | Populate motor policy details | design note | WHEN the new policy is a motor policy (type 'M'), THE policy file update SHALL store the vehicle make (15 characters), model (15 characters), insured value (6 digits) and registration number (7 characters) in the policy-file record. | medium | base/src/lgapvs01.cbl:47-51, base/src/lgapvs01.cbl:124-128 |
| ADPLM-BR-071 | Populate commercial policy details | design note | WHEN the new policy is a commercial policy (type 'C'), THE policy file update SHALL store the premises postcode (8 characters), the status code (4 digits) and the first 31 characters of the customer name in the policy-file record. | medium | base/src/lgapvs01.cbl:31-34, base/src/lgapvs01.cbl:105-108, base/src/lgcmarea.cpy:79, base/src/lgcmarea.cpy:82 |
| ADPLM-BR-072 | Add policy record to policy store | design note | WHEN the policy details have been assembled, THE policy file update SHALL write a 64-byte record to the policy file (KSDSPOLY) under the 21-character policy key. | high | base/src/lgapvs01.cbl:135-147, base/src/lgapvs01.cbl:155-188, base/src/lgapvs01.cbl:58-77 |
| ADPLM-BR-073 | Add policy record to policy store | error handling | WHEN the policy-file write does not succeed for any reason, including a record with the same key already existing, THE policy file update SHALL set return code '80' and return to its caller at once. | high | base/src/lgapvs01.cbl:135-147, base/src/lgapvs01.cbl:155-188, base/src/lgapvs01.cbl:58-77 |
| ADPLM-BR-074 | Add policy record to policy store | side effect | WHEN the policy-file write fails, THE policy file update SHALL log a message (through LGSTSQ) with the date, time, program 'LGAPVS01', policy number, customer number, ' Write file KSDSPOLY' and the RESP and RESP2 codes, followed by a second message holding the first 90 bytes of the request ('COMMAREA='). | high | base/src/lgapvs01.cbl:135-147, base/src/lgapvs01.cbl:155-188, base/src/lgapvs01.cbl:58-77 |

### Key entities

- LGCMAREA (working storage)

### Needs clarification

- SME-038: The name of the person whose life is assured on an endowment policy is supplied as 31 characters but stored in 30. Is it intended that the 31st character is dropped? (Policy administration business analyst) On ADPLM-BR-068, ADPLM-BR-070, ADPLM-BR-071, ADPLM-BR-074, ADPLM-BR-067, ADPLM-BR-069.
- SME-039: New policies are recorded in two places, the policy database and a separate policy file. Does the new system need to keep both, and if so, which one is the official record? (Data architecture team) On ADPLM-BR-068, ADPLM-BR-070, ADPLM-BR-071, ADPLM-BR-074, ADPLM-BR-067, ADPLM-BR-069.
- DEF-015: Is this intended? If the policy-file write fails, the policy and policy-type rows that LGAPDB01 has already inserted into DB2 are not rolled back, because the program ends with a normal return and no rollback. The policy then exists in DB2 but not in KSDSPOLY, while the caller gets '80'. (Subject-matter expert) On ADPLM-BR-073, ADPLM-BR-074.
- DEF-025: Confirm this is deliberate: The house name is cut from 20 characters to 9, and the house number is not stored at all in the policy-file record. (Subject-matter expert) On ADPLM-BR-067, ADPLM-BR-069.
- DEF-035: Confirm this is deliberate: The commercial customer name is cut from 255 characters to 31, and the address, risk perils and premiums are not stored in the policy-file record. (Subject-matter expert) On ADPLM-BR-071.

### Decision table gaps

- Policy-file details stored by policy type: No rule says what details are stored, or whether the record is written, when the 4th character of the request code is not 'E', 'H', 'M' or 'C'.
