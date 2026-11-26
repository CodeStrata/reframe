# Design: Record a new policy in the policy file (ADPLM-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Writes each new policy to the policy file under a key made of its type letter, customer number and policy number, together with a short summary of its product details, so the policy can be found by type, customer and number. It is for policy administrators. It must never overwrite an existing record: a duplicate key or any other write failure returns code '80' and is logged.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGAPVS01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- ADPLM-BR-068: request code = 01AEND; with-profits = Y; equities = N; managed fund = Y; fund name = GROWTHFUND; life assured = JOHN SMITH → The record holds Y, N, Y, GROWTHFUND and JOHN SMITH
- ADPLM-BR-070: request code = 01AMOT; make = FORD; model = FOCUS; value = 012000; registration = AB12CDE → The record holds FORD, FOCUS, 012000 and AB12CDE
- ADPLM-BR-073: policy key = M00000000010000000007; KSDSPOLY = already holds that key → Return code is '80'
- ADPLM-BR-073: KSDSPOLY = file closed → Return code is '80'

## Decision tables

#### Policy-file details stored by policy type

| Policy type | Details stored in the policy-file record | Rule |
|---|---|---|
| E (endowment) | With-profits, equities and managed-fund indicators, fund name (10), life assured name (30) | ADPLM-BR-068 |
| H (house) | Property type (15), bedrooms (3 digits), insured value (8 digits), postcode (8), first 9 characters of house name | ADPLM-BR-069 |
| M (motor) | Vehicle make (15), model (15), insured value (6 digits), registration number (7) | ADPLM-BR-070 |
| C (commercial) | Premises postcode (8), status code (4 digits), first 31 characters of customer name | ADPLM-BR-071 |
| Any other policy type letter | **Gap:** No rule says what details are stored, or whether the record is written, when the 4th character of the request code is not 'E', 'H', 'M' or 'C'. | |


## Design notes

- ADPLM-BR-067: Build a composite key: the policy type letter, the customer number zero-padded to 10 digits, and the policy number zero-padded to 10 digits, 21 characters in all. Records are then found by keyed lookup on the full key, or by prefix (type, or type plus customer) for range browsing.
- ADPLM-BR-068: Map the endowment summary into fixed-width fields: with-profits, equities and managed-fund indicators of 1 character each, fund name of 10 characters and life assured of 30 characters. Values are padded or truncated to those widths.
- ADPLM-BR-069: Map the house summary into fixed-width fields: property type of 15 characters, bedrooms of 3 digits, value of 8 digits, postcode of 8 characters, and only the first 9 characters of the house name (truncated on purpose).
- ADPLM-BR-070: Map the motor summary into fixed-width fields: make of 15 characters, model of 15 characters, value of 6 digits and registration of 7 characters.
- ADPLM-BR-071: Map the commercial summary into fixed-width fields: postcode of 8 characters, status of 4 digits, and the first 31 characters of the customer name.
- ADPLM-BR-072: Insert the 64-character summary record into the policy key-value or index store under the 21-character key, using insert-only semantics, so an existing key is never overwritten and the write fails instead.

## Open questions

- SME-038: The name of the person whose life is assured on an endowment policy is supplied as 31 characters but stored in 30. Is it intended that the 31st character is dropped? (Policy administration business analyst) On ADPLM-BR-068, ADPLM-BR-070, ADPLM-BR-071, ADPLM-BR-074, ADPLM-BR-067, ADPLM-BR-069.
- SME-039: New policies are recorded in two places, the policy database and a separate policy file. Does the new system need to keep both, and if so, which one is the official record? (Data architecture team) On ADPLM-BR-068, ADPLM-BR-070, ADPLM-BR-071, ADPLM-BR-074, ADPLM-BR-067, ADPLM-BR-069.
- DEF-015: Is this intended? If the policy-file write fails, the policy and policy-type rows that LGAPDB01 has already inserted into DB2 are not rolled back, because the program ends with a normal return and no rollback. The policy then exists in DB2 but not in KSDSPOLY, while the caller gets '80'. (Subject-matter expert) On ADPLM-BR-073, ADPLM-BR-074.
- DEF-025: Confirm this is deliberate: The house name is cut from 20 characters to 9, and the house number is not stored at all in the policy-file record. (Subject-matter expert) On ADPLM-BR-067, ADPLM-BR-069.
- DEF-035: Confirm this is deliberate: The commercial customer name is cut from 255 characters to 31, and the address, risk perils and premiums are not stored in the policy-file record. (Subject-matter expert) On ADPLM-BR-071.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (10 in all).