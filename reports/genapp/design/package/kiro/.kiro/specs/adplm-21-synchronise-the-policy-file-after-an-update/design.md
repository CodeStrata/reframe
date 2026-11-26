# Design: Synchronise the policy file after an update (ADPLM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Rewrites a policy's policy-file record with the updated details after a policy update, so that the policy file stays in step with the policy database. It copies the fields for the policy's type (endowment, house, motor or commercial) and blanks the details for any other type. It must replace the whole record, and a failed read or rewrite must stop the update and be logged.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGUPVS01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-160 | Derive policy type and customer key | design note | THE policy file update SHALL build the policy-file key from the policy type letter (the fourth character of the request ID), the customer number and the policy number, and SHALL use the length of the caller's data as the read length. | medium | base/src/lgupvs01.cbl:27-30, base/src/lgupvs01.cbl:100-104, base/src/lgupvs01.cbl:137-143 |
| ADPLM-BR-161 | Build policy key from request | design note | WHEN a policy update request is received, THE policy file update SHALL take the policy type letter from the fourth character of the request ID, put it with the customer number and policy number into the policy-file key, and use the length of the caller's data as the read length. | medium | base/src/lgupvs01.cbl:27-30, base/src/lgupvs01.cbl:100-104, base/src/lgupvs01.cbl:137-143 |
| ADPLM-BR-162 | Rewrite updated policy record | design note | WHEN a policy update reaches the policy file step, THE policy file update SHALL read the policy-file record (KSDSPOLY) for update using the policy type letter, customer number and policy number from the request as the key. | high | base/src/lgupvs01.cbl:26-52, base/src/lgupvs01.cbl:100-104, base/src/lgupvs01.cbl:120-125, base/src/lgupvs01.cbl:137-166 |
| ADPLM-BR-163 | Apply endowment policy details | business rule | WHEN the policy type is endowment ('E', the fourth character of the request ID), THE policy file update SHALL copy the with-profits, equities and managed-fund indicators, the fund name and the life assured from the request into the policy-file record. | medium | base/src/lgupvs01.cbl:36-41, base/src/lgupvs01.cbl:113-118 |
| ADPLM-BR-164 | Apply house policy details | business rule | WHEN the policy type is house ('H', the fourth character of the request ID), THE policy file update SHALL copy the property type, number of bedrooms, value, postcode and house name from the request into the policy-file record. | high | base/src/lgupvs01.cbl:26-52, base/src/lgupvs01.cbl:100-104, base/src/lgupvs01.cbl:120-125, base/src/lgupvs01.cbl:137-166 |
| ADPLM-BR-165 | Apply motor policy details | business rule | WHEN the policy type is motor ('M', the fourth character of the request ID), THE policy file update SHALL copy the vehicle make, model, value and registration number from the request into the policy-file record. | medium | base/src/lgupvs01.cbl:48-52, base/src/lgupvs01.cbl:127-131 |
| ADPLM-BR-166 | Apply commercial policy details | business rule | WHEN the policy type is commercial ('C', the fourth character of the request ID), THE policy file update SHALL copy the business postcode, business status and business customer from the request into the policy-file record. | medium | base/src/lgupvs01.cbl:32-35, base/src/lgupvs01.cbl:106-111 |
| ADPLM-BR-167 | Blank details for unrecognised policy type | business rule | WHEN the policy type letter (fourth character of the request ID) is not 'C', 'E', 'H' or 'M', THE policy file update SHALL blank out the policy details and rewrite the record with blank details. | medium | base/src/lgupvs01.cbl:133-135, base/src/lgupvs01.cbl:155-159 |
| ADPLM-BR-168 | Rewrite updated policy record | business rule | WHEN the record has been read for update, THE policy file update SHALL rewrite the whole policy-file record with the key and the policy details built from the request, replacing all previously stored details. | high | base/src/lgupvs01.cbl:26-52, base/src/lgupvs01.cbl:100-104, base/src/lgupvs01.cbl:120-125, base/src/lgupvs01.cbl:137-166 |
| ADPLM-BR-169 | Updating a policy replaces the whole policy-file record and requires it to already exist | error handling | WHEN the read for update fails for any reason (record not found or any other file error), THE policy file update SHALL set return code '81', write an error log entry and abend the transaction with code 'LGV3'. | high | base/src/lgupvs01.cbl:26-52, base/src/lgupvs01.cbl:100-104, base/src/lgupvs01.cbl:120-125, base/src/lgupvs01.cbl:137-166 |
| ADPLM-BR-170 | Rewrite updated policy record | error handling | WHEN the rewrite of the policy-file record fails, THE policy file update SHALL set return code '82', write an error log entry and abend the transaction with code 'LGV4'. | high | base/src/lgupvs01.cbl:26-52, base/src/lgupvs01.cbl:100-104, base/src/lgupvs01.cbl:120-125, base/src/lgupvs01.cbl:137-166 |
| ADPLM-BR-171 | Rewrite updated policy record | side effect | WHEN the read or rewrite fails, THE policy file update SHALL log (through LGSTSQ) a message with date, time, program 'LGUPVS01', customer number, ' Re-write KSDSPOLY ' and the file response codes, followed by a message with up to the first 90 characters of the request. | high | base/src/lgupvs01.cbl:26-52, base/src/lgupvs01.cbl:100-104, base/src/lgupvs01.cbl:120-125, base/src/lgupvs01.cbl:137-166 |

### Worked examples

- ADPLM-BR-160: request ID = '01UMOT'; customer number = 0000000002; policy number = 0000000007 → Key is 'M' + 0000000002 + 0000000007
- ADPLM-BR-161: request ID = '01UEND'; customer number = 0000000003; policy number = 0000000010 → Key is 'E' + 0000000003 + 0000000010
- ADPLM-BR-162: request ID = '01UHOU'; customer number = 0000000001; policy number = 0000000005 → The record with key 'H' + 0000000001 + 0000000005 is read and locked for update
- ADPLM-BR-163: request ID = '01UEND'; with-profits = Y; fund name = GROWTHFUND; life assured = JANE SMITH → The rewritten record holds with-profits Y, fund GROWTHFUND, life assured JANE SMITH
- ADPLM-BR-164: request ID = '01UHOU'; stored house value = 00250000; requested house value = 00275000; bedrooms = 003 → The rewritten record holds house value 00275000 and 3 bedrooms
- ADPLM-BR-165: request ID = '01UMOT'; make = FORD; model = FOCUS; value = 012000; registration = AB12CDE → The rewritten record holds FORD FOCUS, value 012000, registration AB12CDE
- ADPLM-BR-168: request ID = '01UHOU'; stored postcode = AB1 2CD; requested postcode = XY9 8ZZ → The policy-file record now holds postcode XY9 8ZZ and every other house detail from the request
- ADPLM-BR-169: policy number = 0000000099 (not on the policy file) → Return code '81', error logged, transaction abends 'LGV3'
- ADPLM-BR-170: read for update = successful; rewrite = fails → Return code '82', error logged, transaction abends 'LGV4'

## Decision tables

#### Policy file details applied by policy type letter

| Policy type letter (fourth character of request ID) | Details copied into the policy-file record | Rule |
|---|---|---|
| 'E' | With-profits, equities and managed-fund indicators, fund name and life assured copied | ADPLM-BR-163 |
| 'H' | Property type, number of bedrooms, value, postcode and house name copied | ADPLM-BR-164 |
| 'M' | Vehicle make, model, value and registration number copied | ADPLM-BR-165 |
| 'C' | Business postcode, business status and business customer copied | ADPLM-BR-166 |
| any other letter | Policy details blanked and record rewritten with blank details | ADPLM-BR-167 |
| 'E', 'H' or 'M' | **Gap:** Fewer fields reach the policy file than the database update changes (for example term and sum assured for endowment, house number for house, colour, CC, year, premium and accidents for motor); confirm whether the policy file should hold only this subset. | |
| any other letter | **Gap:** An unrecognised request type passed on by the update service (return code '99') would reach this step and blank the stored policy details; confirm whether that is intended. | |


## Design notes

- ADPLM-BR-160: Build the policy-file key from the policy type letter (the fourth character of the request ID), the customer number and the policy number. Use typed fields for the request instead of a length the caller passes in.
- ADPLM-BR-161: Same key as the delete and lookup paths: the type letter, then the 10-digit customer number, then the 10-digit policy number. Put the key build in one shared function so that all policy-file operations agree.
- ADPLM-BR-162: Do a keyed read with a row lock (select for update) on the policy-file record, then a full replace of that record in the same transaction.

## Open questions

- SME-098: If reading or rewriting the second copy of a policy record fails, the program stops abruptly. What result should the caller receive, and should the codes '81' (read failed) and '82' (rewrite failed) be returned? (Policy business analyst) On ADPLM-BR-160, ADPLM-BR-163, ADPLM-BR-166, ADPLM-BR-165, ADPLM-BR-167, ADPLM-BR-161, ADPLM-BR-164, ADPLM-BR-171.
- SME-099: The second copy of the policy record receives only some of the policy details on update (for example house number, motor colour, engine size, year, premium, accidents, endowment term and sum assured are left out). Is that intended? (Policy business analyst) On ADPLM-BR-160, ADPLM-BR-163, ADPLM-BR-166, ADPLM-BR-165, ADPLM-BR-167, ADPLM-BR-161, ADPLM-BR-164, ADPLM-BR-171.
- DEF-023: Is this intended? The error log has a policy number slot (' PNUM=') that is never filled, so logged failures always show a blank policy number. Also, LGUPDB01 resets the return code to '00' when it closes its cursor and always links to this program, so the policy file can be rewritten even when the database update was refused (policy not found '01' or timestamp mismatch '02'). (Subject-matter expert) On ADPLM-BR-164, ADPLM-BR-171.
- DEF-032: Is this intended? An update request with an unrecognised request ID is not stopped: LGUPOL01 sets return code '99' but still performs the update, and LGUPDB01 overwrites the code with '00', so commercial or unknown types still reach the policy-file rewrite. (Subject-matter expert) On ADPLM-BR-166.
- DEF-040: Is this intended? An unknown policy type wipes the stored policy details instead of being rejected, because LGUPOL01 does not stop on return code '99' and LGUPDB01 resets it to '00'. (Subject-matter expert) On ADPLM-BR-167.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (12 in all).