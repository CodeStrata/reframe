# Update a policy in the database with a timestamp check (ADPLM-C20)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Updates a policy's product details (endowment, house or motor) and its common details (issue and expiry dates, broker and broker reference) only if no one else has changed the policy since the caller read it. The check compares the caller's last-changed timestamp with the stored one. It must never overwrite a concurrent change and never alter the payment recorded on the policy, and the caller must get the new last-changed timestamp back.

**User story:** As a policy administrator, I want a policy's product details and common details updated only when no one else has changed it since I read it, so that concurrent changes are not overwritten.

## Requirements

### Requirement 1: ADPLM-REQ-F-126 (error handling)

#### Acceptance criteria

1. If the policy update database program is called without any request data, then the system shall log the error ' NO COMMAREA RECEIVED' and end the task abnormally with code 'LGCA' (no dump), without attempting any database work. (rules ADPLM-BR-136)
2. GIVEN Request data length: 0 WHEN the policy update database program is called without any request data THEN The message ' NO COMMAREA RECEIVED' is logged and the task ends with abend 'LGCA'; no policy is read or changed (ADPLM-C20-AC-01; ADPLM-BR-136)

### Requirement 2: ADPLM-REQ-F-127 (design note)

#### Acceptance criteria

1. The system shall start each policy update with outcome '00' and use the request's customer number and policy number to find the policy to update. (rules ADPLM-BR-137)
2. GIVEN Customer number: 1; Policy number: 5 WHEN policy update database program runs THEN The program looks for policy 5 of customer 1, starting with outcome '00' (ADPLM-C20-AC-02; ADPLM-BR-137)

### Requirement 3: ADPLM-REQ-F-128 (business rule)

#### Acceptance criteria

1. When the policy row for the customer and policy number is read and its last-changed timestamp equals the one the caller supplied, the system shall update the endowment, house or motor details and then the common policy details, giving the policy a new last-changed timestamp. (rules ADPLM-BR-138)
2. GIVEN Motor policy 0000000003 for customer 0000000001 has last-changed timestamp '2026-11-20-10.00.00.000000', and an '01UMOT' request supplies that same timestamp WHEN The policy update runs THEN The motor details and the common policy details are updated, and the policy's last-changed timestamp is replaced by a new value different from '2026-11-20-10.00.00.000000' (ADPLM-C20-AC-24; ADPLM-BR-138)

### Requirement 4: ADPLM-REQ-F-129 (business rule)

#### Acceptance criteria

1. When the policy row is found and its last-changed timestamp matches the caller's, where the request is a motor update ('01UMOT'), the system shall replace the motor record's make, model, value, registration, colour, CC, year of manufacture, premium and accidents with the request values, matching the record by policy number. (rules ADPLM-BR-139, ADPLM-BR-140)
2. GIVEN Request type: '01UMOT'; Stored premium / accidents: 400 / 0; Request premium / accidents: 650 / 2 WHEN a motor update ('01UMOT') passes the timestamp check THEN The motor record for the policy now has premium 650 and accidents 2, and every other motor field as supplied (ADPLM-C20-AC-03; ADPLM-BR-139)
3. GIVEN request type: '01UMOT'; policy number: 9; timestamps: match; premium: 650 WHEN the policy row is found, its last-changed timestamp matches the caller's, and the request is '01UMOT' THEN The motor row for policy 9 is updated with premium 650 and the other motor details supplied. (ADPLM-C20-AC-04; ADPLM-BR-140)

### Requirement 5: ADPLM-REQ-F-130 (business rule)

#### Acceptance criteria

1. When the policy row is found and its last-changed timestamp matches the caller's, where the request is a house update ('01UHOU'), the system shall replace the house record's property type, bedrooms, value, house name, house number and postcode with the request values, matching the record by policy number. (rules ADPLM-BR-141, ADPLM-BR-142)
2. GIVEN Request type: '01UHOU'; Request bedrooms: 4; Request postcode: SO21 2JN WHEN a house update ('01UHOU') passes the timestamp check THEN The house record for the policy now has 4 bedrooms and postcode SO21 2JN (ADPLM-C20-AC-05; ADPLM-BR-141)
3. GIVEN request type: '01UHOU'; policy number: 7; timestamps: match; bedrooms: 4 WHEN the policy row is found, its last-changed timestamp matches the caller's, and the request is '01UHOU' THEN The house row for policy 7 is updated to 4 bedrooms along with the other house details supplied. (ADPLM-C20-AC-06; ADPLM-BR-142)

### Requirement 6: ADPLM-REQ-F-131 (business rule)

#### Acceptance criteria

1. When the policy row is found and its last-changed timestamp matches the caller's, where the request is an endowment update ('01UEND'), the system shall replace the endowment record's with-profits, equities, managed-fund and fund-name values, term, sum assured and life assured with the request values, matching the record by policy number. (rules ADPLM-BR-143, ADPLM-BR-144)
2. GIVEN Request type: '01UEND'; Request term: 25; Request sum assured: 150000 WHEN an endowment update ('01UEND') passes the timestamp check THEN The endowment record for the policy now has term 25 and sum assured 150000 (ADPLM-C20-AC-07; ADPLM-BR-143)
3. GIVEN request type: '01UEND'; policy number: 5; timestamps: match; sum assured: 50000 WHEN the policy row is found, its last-changed timestamp matches the caller's, and the request is '01UEND' THEN The endowment row for policy 5 is updated with sum assured 50000 and the other endowment details supplied. (ADPLM-C20-AC-08; ADPLM-BR-144)

### Requirement 7: ADPLM-REQ-F-132 (error handling)

#### Acceptance criteria

1. If the endowment, house or motor update finds no record for the policy number, then the system shall set outcome '01'. (rules ADPLM-BR-145, ADPLM-BR-146)
2. GIVEN Request type: '01UMOT'; Motor record for policy: none WHEN the product-detail update finds no record for the policy number THEN The outcome is set to '01' (ADPLM-C20-AC-09; ADPLM-BR-145)
3. GIVEN Request type: '01UMOT'; Motor update result: SQL error -904 WHEN the product-detail update finds no record for the policy number THEN The outcome is set to '90' and an error message is logged (ADPLM-C20-AC-10; ADPLM-BR-145)
4. GIVEN request type: '01UHOU'; house row for policy 7: missing WHEN the endowment, house or motor update finds no row for the policy number THEN The outcome code is set to '01'. (ADPLM-C20-AC-11; ADPLM-BR-146)

### Requirement 8: ADPLM-REQ-F-133 (error handling)

#### Acceptance criteria

1. If the endowment, house or motor update fails for any reason other than a missing record, then the system shall set outcome '90' and write an error message with the date, time, customer number, policy number and SQL code, plus up to 90 bytes of the request, to the error log. (rules ADPLM-BR-145, ADPLM-BR-147)
2. GIVEN Request type: '01UMOT'; Motor record for policy: none WHEN the product-detail update finds no record for the policy number THEN The outcome is set to '01' (ADPLM-C20-AC-09; ADPLM-BR-145)
3. GIVEN Request type: '01UMOT'; Motor update result: SQL error -904 WHEN the product-detail update finds no record for the policy number THEN The outcome is set to '90' and an error message is logged (ADPLM-C20-AC-10; ADPLM-BR-145)
4. GIVEN request type: '01UMOT'; motor update: fails with a database error WHEN the endowment, house or motor update fails for any reason other than a missing row THEN The outcome code is set to '90' and an error message ' UPDATE MOTOR ' with the SQL code is logged. (ADPLM-C20-AC-12; ADPLM-BR-147)

### Requirement 9: ADPLM-REQ-F-134 (error handling)

#### Acceptance criteria

1. If the endowment, house or motor update leaves an outcome other than '00', then the system shall close the policy retrieval and return to the caller without updating the common policy record or the policy file, and because the close resets the outcome, the caller receives '00' when the close succeeds. (rules ADPLM-BR-148, ADPLM-BR-149)
2. GIVEN Request type: '01UMOT'; Motor record for policy: none WHEN the product-detail update fails THEN The policy record is unchanged, the VSAM file is not updated, and the caller receives outcome '00' (ADPLM-C20-AC-13; ADPLM-BR-148)
3. GIVEN request type: '01UEND'; endowment row: missing (code '01'); cursor close: succeeds WHEN the endowment, house or motor update leaves an outcome code other than '00' THEN The policy row keeps its old dates, broker and timestamp, the policy file is not rewritten, and the caller receives '00'. (ADPLM-C20-AC-14; ADPLM-BR-149)

### Requirement 10: ADPLM-REQ-F-135 (business rule)

#### Acceptance criteria

1. When the policy's last-changed timestamp matches the one in the request and no product-detail update has failed, the system shall set the policy's issue date, expiry date, broker ID and broker's reference to the request values and set its last-changed timestamp to the current database timestamp. (rules ADPLM-BR-150)
2. GIVEN Request type: '01UMOT'; Request last-changed: 2026-11-20-10.15.00.000000; Stored last-changed: 2026-11-20-10.15.00.000000; Request expiry date: 2027-11-20; Request broker ID: 1234 WHEN the policy's last-changed timestamp matches the one in the request and no product-detail update has failed THEN The policy now has expiry date 2027-11-20, broker ID 1234 and a new last-changed timestamp from the time of the update (ADPLM-C20-AC-15; ADPLM-BR-150)

### Requirement 11: ADPLM-REQ-F-136 (design note)

#### Acceptance criteria

1. When the policy record has been updated, the system shall read the new last-changed timestamp back, looking the policy up by policy number only, and return it to the caller in the request. (rules ADPLM-BR-151)
2. GIVEN Policy number: 5; Timestamp assigned by the update: 2026-11-25-09.30.12.345678 WHEN the policy record has been updated THEN The request handed back to the caller carries last-changed 2026-11-25-09.30.12.345678 (ADPLM-C20-AC-16; ADPLM-BR-151)

### Requirement 12: ADPLM-REQ-F-137 (error handling)

#### Acceptance criteria

1. If reading back the new timestamp fails, then the system shall roll back the whole unit of work, set outcome '90' and log an error message with date, time, customer number, policy number, SQL code and the first 90 bytes of the request. (rules ADPLM-BR-152)
2. GIVEN Timestamp read-back result: SQL error -911 WHEN reading back the new timestamp fails THEN The motor and policy changes are rolled back, the outcome is set to '90' and an error message is written to the error queue (ADPLM-C20-AC-17; ADPLM-BR-152)

### Requirement 13: ADPLM-REQ-F-138 (historical artifact)

#### Acceptance criteria

1. The system shall not store the request's payment amount during a policy update, so that a policy update never changes the payment (or commission) recorded on the policy. (rules ADPLM-BR-153)
2. GIVEN Stored payment: 100; Request payment: 250 WHEN policy update database program runs THEN The policy's payment stays 100 (ADPLM-C20-AC-18; ADPLM-BR-153)

### Requirement 14: ADPLM-REQ-F-139 (business rule)

#### Acceptance criteria

1. If the caller's last-changed timestamp differs from the stored policy timestamp, then the system shall change no policy tables and set outcome '02', which the close that follows resets to '00' when it succeeds. (rules ADPLM-BR-154)
2. GIVEN Policy 0000000003 for customer 0000000001 has last-changed timestamp '2026-11-20-10.00.00.000000', and an update request supplies '2026-11-19-09.00.00.000000' WHEN The policy update runs THEN No policy, endowment, house or motor table is changed, and outcome '02' is set, which the close that follows resets to '00' when it succeeds (ADPLM-C20-AC-25; ADPLM-BR-154)

### Requirement 15: ADPLM-REQ-F-140 (error handling)

#### Acceptance criteria

1. If no policy row matches the customer and policy number, then the system shall make no database update and set outcome '01', which the close that follows resets to '00' when it succeeds. (rules ADPLM-BR-155)
2. GIVEN customer: 1; policy: 999 (does not exist for customer 1) WHEN no policy row matches the customer and policy number THEN Nothing is updated. The code is set to '01' and then reset to '00' by the close. (ADPLM-C20-AC-19; ADPLM-BR-155)

### Requirement 16: ADPLM-REQ-F-141 (error handling)

#### Acceptance criteria

1. If reading the policy row fails for a reason other than not found, then the system shall set outcome '90' and write an error message with the SQL code to the error log, and the close that follows resets the outcome to '00' when it succeeds. (rules ADPLM-BR-156)
2. GIVEN policy read: fails with a database error WHEN reading the policy row fails for a reason other than not found THEN An error message ' FETCH ROW ' with the SQL code is logged, and the code is set to '90' and then reset to '00' by the close. (ADPLM-C20-AC-20; ADPLM-BR-156)

### Requirement 17: ADPLM-REQ-F-142 (side effect)

#### Acceptance criteria

1. When the database update step finishes without an early return, including when the timestamps differ, the policy is not found or the policy read fails, the system shall pass the first 225 bytes of the request to the policy file update, which rewrites the policy file record with the details supplied, and then return to the caller. (rules ADPLM-BR-157, ADPLM-BR-158)
2. GIVEN request type: '01UMOT'; timestamps: differ WHEN the timestamps differ THEN The motor policy is not changed in the database, but the policy file record is rewritten with the make, model, value and registration supplied. (ADPLM-C20-AC-21; ADPLM-BR-157)
3. GIVEN Request type: '01UMOT'; Database update: successful WHEN the database update step finishes without an early return THEN LGUPVS01 is called with the request, then control returns to the caller (ADPLM-C20-AC-22; ADPLM-BR-158)

### Requirement 18: ADPLM-REQ-F-143 (error handling)

#### Acceptance criteria

1. If the policy cursor cannot be opened, a product-detail update fails, the cursor cannot be closed, or the update was rolled back, then the system shall return to the caller without calling the policy file update. (rules ADPLM-BR-159)
2. GIVEN Opening the policy cursor: SQL error -913 WHEN the policy cursor cannot be opened, a product-detail update fails THEN The outcome is '90', an error is logged and LGUPVS01 is not called (ADPLM-C20-AC-23; ADPLM-BR-159)

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGUPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGUPDB01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-136 | Policy update requires a request payload | error handling | WHEN the policy update database program is called without any request data, THE program SHALL log the error ' NO COMMAREA RECEIVED' and end the task abnormally with code 'LGCA' (no dump), without attempting any database work. | medium | base/src/lgupdb01.cbl:183-187, base/src/lgupdb01.cbl:502-518 |
| ADPLM-BR-137 | Orchestrate policy update and forward request | design note | THE policy update database program SHALL start each request with outcome '00' and use the request's customer number and policy number to find the policy to update. | high | base/src/lgupdb01.cbl:189-199, base/src/lgupdb01.cbl:207-216, base/src/lgupdb01.cbl:259-270, base/src/lgupdb01.cbl:302-307 |
| ADPLM-BR-138 | Verify policy timestamp matches before update | business rule | WHEN the policy row for the customer and policy number is read and its last-changed timestamp equals the one the caller supplied, THE policy update SHALL proceed to update the endowment, house or motor details and then the common policy details, giving the policy a new last-changed timestamp. | high | base/src/lgupdb01.cbl:128-143, base/src/lgupdb01.cbl:207-212, base/src/lgupdb01.cbl:273-360, base/src/lgupdb01.cbl:362-381 |
| ADPLM-BR-139 | Update motor policy details | business rule | WHEN a motor update ('01UMOT') passes the timestamp check, THE policy update database program SHALL replace the motor record's make, model, value, registration, colour, CC, year of manufacture, premium and accidents with the request values, matching the record by policy number. | high | base/src/lgupdb01.cbl:283-307, base/src/lgupdb01.cbl:362-381, base/src/lgupdb01.cbl:387-418, base/src/lgupdb01.cbl:424-454 |
| ADPLM-BR-140 | Route update by policy type | business rule | WHEN the policy row is found, its last-changed timestamp matches the caller's, and the request is '01UMOT', THE policy update SHALL update the motor row for the policy number with the make, model, value, registration, colour, engine cc, year of manufacture, premium and accidents supplied. | high | base/src/lgupdb01.cbl:275-307, base/src/lgupdb01.cbl:360-380, base/src/lgupdb01.cbl:387-418, base/src/lgupdb01.cbl:424-454 |
| ADPLM-BR-141 | Product detail fields are replaced wholesale from the request | business rule | WHEN a house update ('01UHOU') passes the timestamp check, THE policy update database program SHALL replace the house record's property type, bedrooms, value, house name, house number and postcode with the request values, matching the record by policy number. | high | base/src/lgupdb01.cbl:283-307, base/src/lgupdb01.cbl:362-381, base/src/lgupdb01.cbl:387-418, base/src/lgupdb01.cbl:424-454 |
| ADPLM-BR-142 | Route update by policy type | business rule | WHEN the policy row is found, its last-changed timestamp matches the caller's, and the request is '01UHOU', THE policy update SHALL update the house row for the policy number with the property type, bedrooms, value, house name, house number and postcode supplied. | high | base/src/lgupdb01.cbl:275-307, base/src/lgupdb01.cbl:360-380, base/src/lgupdb01.cbl:387-418, base/src/lgupdb01.cbl:424-454 |
| ADPLM-BR-143 | Product detail fields are replaced wholesale from the request | business rule | WHEN an endowment update ('01UEND') passes the timestamp check, THE policy update database program SHALL replace the endowment record's with-profits, equities, managed-fund and fund-name values, term, sum assured and life assured with the request values, matching the record by policy number. | high | base/src/lgupdb01.cbl:283-307, base/src/lgupdb01.cbl:362-381, base/src/lgupdb01.cbl:387-418, base/src/lgupdb01.cbl:424-454 |
| ADPLM-BR-144 | Route update by policy type | business rule | WHEN the policy row is found, its last-changed timestamp matches the caller's, and the request is '01UEND', THE policy update SHALL update the endowment row for the policy number with the with-profits, equities, managed-fund, fund name, term, sum assured and life assured values supplied. | high | base/src/lgupdb01.cbl:275-307, base/src/lgupdb01.cbl:360-380, base/src/lgupdb01.cbl:387-418, base/src/lgupdb01.cbl:424-454 |
| ADPLM-BR-145 | Update motor policy details | error handling | WHEN the product-detail update finds no record for the policy number, THE policy update database program SHALL set outcome '01'. WHEN it fails for any other reason, the program SHALL set outcome '90' and log an error message with the SQL code. | high | base/src/lgupdb01.cbl:283-307, base/src/lgupdb01.cbl:362-381, base/src/lgupdb01.cbl:387-418, base/src/lgupdb01.cbl:424-454 |
| ADPLM-BR-146 | Update endowment policy details | error handling | WHEN the endowment, house or motor update finds no row for the policy number, THE policy update SHALL set the outcome code to '01'. | high | base/src/lgupdb01.cbl:275-307, base/src/lgupdb01.cbl:360-380, base/src/lgupdb01.cbl:387-418, base/src/lgupdb01.cbl:424-454 |
| ADPLM-BR-147 | Update endowment policy details | error handling | WHEN the endowment, house or motor update fails for any reason other than a missing row, THE policy update SHALL set the outcome code to '90' and write an error message with the date, time, customer number, policy number and SQL code, plus up to 90 bytes of the request, to the error log (LGSTSQ). | high | base/src/lgupdb01.cbl:275-307, base/src/lgupdb01.cbl:360-380, base/src/lgupdb01.cbl:387-418, base/src/lgupdb01.cbl:424-454 |
| ADPLM-BR-148 | Update motor policy details | error handling | WHEN the product-detail update fails, THE policy update database program SHALL close the policy cursor and return to the caller without updating the policy record or the VSAM policy file; closing the cursor resets the outcome to '00', so the caller is told the update succeeded. | high | base/src/lgupdb01.cbl:283-307, base/src/lgupdb01.cbl:362-381, base/src/lgupdb01.cbl:387-418, base/src/lgupdb01.cbl:424-454 |
| ADPLM-BR-149 | Abandon update after policy-type failure | error handling | WHEN the endowment, house or motor update leaves an outcome code other than '00', THE policy update SHALL close the policy retrieval and return to the caller without updating the common policy row or the policy file. Because the close resets the code, the caller receives '00' when the close succeeds. | high | base/src/lgupdb01.cbl:275-307, base/src/lgupdb01.cbl:360-380, base/src/lgupdb01.cbl:387-418, base/src/lgupdb01.cbl:424-454 |
| ADPLM-BR-150 | Update common policy data and timestamp | business rule | WHEN the policy's last-changed timestamp matches the one in the request and no product-detail update has failed, THE policy update database program SHALL set the policy's issue date, expiry date, broker ID and broker's reference to the request values and set its last-changed timestamp to the current database timestamp. | high | base/src/lgupdb01.cbl:126-143, base/src/lgupdb01.cbl:278, base/src/lgupdb01.cbl:302-342, base/src/lgupdb01.cbl:360-380 |
| ADPLM-BR-151 | Update common policy data and timestamp | design note | WHEN the policy record has been updated, THE policy update database program SHALL read the new last-changed timestamp back (looking the policy up by policy number only) and return it to the caller in the request. | high | base/src/lgupdb01.cbl:126-143, base/src/lgupdb01.cbl:278, base/src/lgupdb01.cbl:302-342, base/src/lgupdb01.cbl:360-380 |
| ADPLM-BR-152 | Update common policy data and timestamp | error handling | WHEN reading back the new timestamp fails, THE policy update database program SHALL roll back the whole unit of work, set outcome '90' and log an error message with date, time, customer number, policy number, SQL code and the first 90 bytes of the request. | high | base/src/lgupdb01.cbl:126-143, base/src/lgupdb01.cbl:278, base/src/lgupdb01.cbl:302-342, base/src/lgupdb01.cbl:360-380 |
| ADPLM-BR-153 | Policy header update stamps a new last-changed timestamp | historical artifact | THE policy update database program SHALL copy the request's payment amount into a working field but SHALL NOT store it, so a policy update never changes the payment (or commission) recorded on the policy. | high | base/src/lgupdb01.cbl:126-143, base/src/lgupdb01.cbl:278, base/src/lgupdb01.cbl:302-342, base/src/lgupdb01.cbl:360-380 |
| ADPLM-BR-154 | Reject update on timestamp mismatch | business rule | WHEN the caller's last-changed timestamp differs from the stored policy timestamp, THE policy update SHALL change no policy tables and set the outcome code to '02'. The close that follows resets the code to '00' when it succeeds. | high | base/src/lgupdb01.cbl:128-143, base/src/lgupdb01.cbl:207-212, base/src/lgupdb01.cbl:273-360, base/src/lgupdb01.cbl:362-381 |
| ADPLM-BR-155 | Report policy not found | error handling | WHEN no policy row matches the customer and policy number, THE policy update SHALL make no database update and set the outcome code to '01'. The close that follows resets the code to '00' when it succeeds. | high | base/src/lgupdb01.cbl:128-143, base/src/lgupdb01.cbl:207-212, base/src/lgupdb01.cbl:273-360, base/src/lgupdb01.cbl:362-381 |
| ADPLM-BR-156 | Optimistic concurrency check on policy last-changed timestamp | error handling | WHEN reading the policy row fails for a reason other than not found, THE policy update SHALL set the outcome code to '90' and write an error message with the SQL code to the error log (LGSTSQ). The close that follows resets the code to '00' when it succeeds. | high | base/src/lgupdb01.cbl:128-143, base/src/lgupdb01.cbl:207-212, base/src/lgupdb01.cbl:273-360, base/src/lgupdb01.cbl:362-381 |
| ADPLM-BR-157 | Optimistic concurrency check on policy last-changed timestamp | side effect | WHEN the timestamps differ, the policy is not found, or the policy read fails, THE policy update SHALL still pass the request to the policy file update (LGUPVS01), which rewrites the policy file record with the details supplied. | high | base/src/lgupdb01.cbl:128-143, base/src/lgupdb01.cbl:207-212, base/src/lgupdb01.cbl:273-360, base/src/lgupdb01.cbl:362-381 |
| ADPLM-BR-158 | Orchestrate policy update and forward request | side effect | WHEN the database update step finishes without an early return, THE policy update database program SHALL pass the first 225 bytes of the request to the VSAM policy update program (LGUPVS01) and then return to the caller. | high | base/src/lgupdb01.cbl:189-199, base/src/lgupdb01.cbl:207-216, base/src/lgupdb01.cbl:259-270, base/src/lgupdb01.cbl:302-307 |
| ADPLM-BR-159 | Synchronise policy change to the VSAM policy store after the DB2 update | error handling | WHEN the policy cursor cannot be opened, a product-detail update fails, the cursor cannot be closed, or the update was rolled back, THE policy update database program SHALL return to the caller without calling the VSAM policy update program (LGUPVS01). | high | base/src/lgupdb01.cbl:189-199, base/src/lgupdb01.cbl:207-216, base/src/lgupdb01.cbl:259-270, base/src/lgupdb01.cbl:302-307 |

### Worked examples

- ADPLM-BR-136: Request data length = 0 → The message ' NO COMMAREA RECEIVED' is logged and the task ends with abend 'LGCA'; no policy is read or changed
- ADPLM-BR-137: Customer number = 1; Policy number = 5 → The program looks for policy 5 of customer 1, starting with outcome '00'
- ADPLM-BR-139: Request type = '01UMOT'; Stored premium / accidents = 400 / 0; Request premium / accidents = 650 / 2 → The motor record for the policy now has premium 650 and accidents 2, and every other motor field as supplied
- ADPLM-BR-140: request type = '01UMOT'; policy number = 9; timestamps = match; premium = 650 → The motor row for policy 9 is updated with premium 650 and the other motor details supplied.
- ADPLM-BR-141: Request type = '01UHOU'; Request bedrooms = 4; Request postcode = SO21 2JN → The house record for the policy now has 4 bedrooms and postcode SO21 2JN
- ADPLM-BR-142: request type = '01UHOU'; policy number = 7; timestamps = match; bedrooms = 4 → The house row for policy 7 is updated to 4 bedrooms along with the other house details supplied.
- ADPLM-BR-143: Request type = '01UEND'; Request term = 25; Request sum assured = 150000 → The endowment record for the policy now has term 25 and sum assured 150000
- ADPLM-BR-144: request type = '01UEND'; policy number = 5; timestamps = match; sum assured = 50000 → The endowment row for policy 5 is updated with sum assured 50000 and the other endowment details supplied.
- ADPLM-BR-145: Request type = '01UMOT'; Motor record for policy = none → The outcome is set to '01'
- ADPLM-BR-145: Request type = '01UMOT'; Motor update result = SQL error -904 → The outcome is set to '90' and an error message is logged
- ADPLM-BR-146: request type = '01UHOU'; house row for policy 7 = missing → The outcome code is set to '01'.
- ADPLM-BR-147: request type = '01UMOT'; motor update = fails with a database error → The outcome code is set to '90' and an error message ' UPDATE MOTOR ' with the SQL code is logged.
- ADPLM-BR-148: Request type = '01UMOT'; Motor record for policy = none → The policy record is unchanged, the VSAM file is not updated, and the caller receives outcome '00'
- ADPLM-BR-149: request type = '01UEND'; endowment row = missing (code '01'); cursor close = succeeds → The policy row keeps its old dates, broker and timestamp, the policy file is not rewritten, and the caller receives '00'.
- ADPLM-BR-150: Request type = '01UMOT'; Request last-changed = 2026-11-20-10.15.00.000000; Stored last-changed = 2026-11-20-10.15.00.000000; Request expiry date = 2027-11-20; Request broker ID = 1234 → The policy now has expiry date 2027-11-20, broker ID 1234 and a new last-changed timestamp from the time of the update
- ADPLM-BR-151: Policy number = 5; Timestamp assigned by the update = 2026-11-25-09.30.12.345678 → The request handed back to the caller carries last-changed 2026-11-25-09.30.12.345678
- ADPLM-BR-152: Timestamp read-back result = SQL error -911 → The motor and policy changes are rolled back, the outcome is set to '90' and an error message is written to the error queue
- ADPLM-BR-153: Stored payment = 100; Request payment = 250 → The policy's payment stays 100
- ADPLM-BR-155: customer = 1; policy = 999 (does not exist for customer 1) → Nothing is updated. The code is set to '01' and then reset to '00' by the close.
- ADPLM-BR-156: policy read = fails with a database error → An error message ' FETCH ROW ' with the SQL code is logged, and the code is set to '90' and then reset to '00' by the close.
- ADPLM-BR-157: request type = '01UMOT'; timestamps = differ → The motor policy is not changed in the database, but the policy file record is rewritten with the make, model, value and registration supplied.
- ADPLM-BR-158: Request type = '01UMOT'; Database update = successful → LGUPVS01 is called with the request, then control returns to the caller
- ADPLM-BR-159: Opening the policy cursor = SQL error -913 → The outcome is '90', an error is logged and LGUPVS01 is not called

## Decision tables

#### Policy database update outcome

| Policy row read | Timestamp matches caller's | Product-detail update result | Database changes, outcome returned and whether the policy file is updated | Rule |
|---|---|---|---|---|
| found | yes | succeeded | Product details and common policy details updated with new last-changed timestamp; request passed to policy file update | ADPLM-BR-138 |
| found | yes | no record for policy number | Outcome '01'; cursor closed, reset to '00'; no common policy or policy file update | ADPLM-BR-149 |
| found | yes | failed for another reason | Outcome '90' and error logged; cursor closed, reset to '00'; no common policy or policy file update | ADPLM-BR-148 |
| found | no | not attempted | No policy tables changed; outcome '02', reset to '00' by successful close; request still passed to policy file update | ADPLM-BR-154 |
| not found | not applicable | not attempted | No database update; outcome '01', reset to '00' by successful close; request still passed to policy file update | ADPLM-BR-155 |
| failed (other than not found) | not applicable | not attempted | Outcome '90' and SQL code logged, reset to '00' by successful close; request still passed to policy file update | ADPLM-BR-156 |
| found | yes | succeeded | **Gap:** No rule says what happens if the update of the common policy details itself (issue date, expiry date, broker ID, broker's reference) fails; only failure of the timestamp read-back is covered (R17). | |
| found | no | not attempted | **Gap:** A timestamp mismatch, missing policy or failed read still rewrites the policy file with the request details (R14) and the caller can receive '00'; confirm whether this is intended business behaviour. | |


## Design notes

- ADPLM-BR-137: Start every update with outcome '00'. Find the policy by a keyed lookup on customer number plus policy number, and read it inside the same transaction as the update.
- ADPLM-BR-151: After the update, read the new last-changed timestamp, keyed by policy number, or take it from the update's RETURNING clause, and put it in the response so that the caller can make its next change.

## Open questions

- SME-092: A policy update with an unrecognised request type gets error code '99' but still goes on to update the common policy data, and the '99' is overwritten. Should such requests be stopped before any update? (Policy business analyst) On ADPLM-BR-138, ADPLM-BR-154, ADPLM-BR-155, ADPLM-BR-152, ADPLM-BR-158, ADPLM-BR-148, ADPLM-BR-144, ADPLM-BR-147, ADPLM-BR-149.
- SME-093: If the type-specific part of a policy update (endowment, house or motor) succeeds but the common policy update then fails, nothing is undone. Should both parts succeed or fail together? (Application architect) On ADPLM-BR-138, ADPLM-BR-154, ADPLM-BR-155, ADPLM-BR-152, ADPLM-BR-158, ADPLM-BR-148, ADPLM-BR-144, ADPLM-BR-147, ADPLM-BR-149.
- SME-094: The payment amount is captured on a policy update but thrown away. Should payment be updatable this way? (Policy administration lead) On ADPLM-BR-153.
- SME-095: After a policy update, the second copy of the policy record is always updated. Should it be updated only when the main database update succeeded? (Mainframe application SME) On ADPLM-BR-159.
- SME-096: A policy update is rejected if the policy was changed by someone else since it was read (last-changed timestamp check), to stop one user's edit silently overwriting another's. Please confirm this rule is described correctly and must be kept. (Subject-matter expert) On ADPLM-BR-157.
- DEF-004: Is this intended? The cursor-close routine always overwrites the outcome code with '00', so a timestamp mismatch ('02'), a missing policy ('01') and a read failure ('90') all reach the caller as success, and the motor screen shows 'Motor Policy Updated'. The program also links to LGUPVS01 in these cases, so the policy file is rewritten while the database is not. Separately, after the common policy update the program checks the SQL code of the follow-up timestamp read rather than of the update itself. (Subject-matter expert) On ADPLM-BR-138, ADPLM-BR-154, ADPLM-BR-155, ADPLM-BR-157.
- DEF-014: Is this intended? The program checks the SQLCODE only after the timestamp read-back SELECT, so a failed UPDATE POLICY is not detected when the read-back succeeds. After the rollback, the cursor (declared WITH HOLD) is closed by the rollback. The CLOSE-PCURSOR step then gets -501, sets the outcome back to '00' and returns, so the caller sees success instead of '90'. (Subject-matter expert) On ADPLM-BR-152, ADPLM-BR-153.
- DEF-021: Is this intended? When the timestamps do not match ('02') or the policy is not found ('01'), the program still reaches the LGUPVS01 link, and closing the cursor resets the outcome to '00'. The caller is told the update succeeded although DB2 was not updated. On a timestamp mismatch, the VSAM policy record is rewritten with the request data, so it no longer matches DB2. (Subject-matter expert) On ADPLM-BR-158, ADPLM-BR-159.
- DEF-022: Is this intended? When a product-detail update fails with '01' or '90', CLOSE-PCURSOR overwrites the outcome with '00' before the early return. The caller is therefore told the update succeeded although nothing was changed. (Subject-matter expert) On ADPLM-BR-143, ADPLM-BR-148.
- DEF-028: Is this intended? When the type-specific update fails with '01' or '90', the cursor-close routine overwrites the code with '00' before the program returns, so the caller is told that the update succeeded. For example, the motor screen shows 'Motor Policy Updated' when nothing was changed. (Subject-matter expert) On ADPLM-BR-144, ADPLM-BR-147, ADPLM-BR-149.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (25 in all).
