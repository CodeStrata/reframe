# Update the customer's personal and contact details (CRCM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Record Management · Customer Record Creation and Maintenance · runs as scheduled job · risk high

## Introduction

Updates an existing customer's name, date of birth, address, phone numbers and email in the customer database, then passes the change on so that the customer file is updated too. Every supplied field replaces the stored one, so a blank field blanks the stored value. An unknown customer must return '01' with no error log, and any other failure must return '90' and be logged.

**User story:** As a customer service user, I want to update an existing customer's personal and contact details, so that the stored customer record stays current.

## Requirements

### Requirement 1: CRCM-REQ-F-022 (design note)

#### Acceptance criteria

1. When a customer update request is received, the system shall first set the return code to '00' (success) and then update the customer record whose customer number matches the request. (rules CRCM-BR-030)
2. GIVEN customer number: 1000042 WHEN a customer update request is received THEN Return code starts as '00' and the update of customer 1000042 is attempted. (CRCM-C06-AC-01; CRCM-BR-030)

### Requirement 2: CRCM-REQ-F-023 (business rule)

#### Acceptance criteria

1. When a customer update is processed, the system shall overwrite the first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email address of the matching customer with the supplied values, unconditionally, so a blank supplied value blanks the stored value. (rules CRCM-BR-031)
2. GIVEN customer number: 1000042; last name: SMITH; email address: (blank) WHEN a customer update is processed THEN Customer 1000042 is stored with last name SMITH and a blank email address; return code '00'. (CRCM-C06-AC-02; CRCM-BR-031)

### Requirement 3: CRCM-REQ-F-024 (error handling)

#### Acceptance criteria

1. If no customer matches the supplied customer number, then the system shall set the return code to '01' (customer not found) without writing an error log entry. (rules CRCM-BR-032)
2. GIVEN customer number: 9999999999; customer exists: no WHEN no customer matches the supplied customer number THEN Return code '01'; nothing is logged. (CRCM-C06-AC-03; CRCM-BR-032)

### Requirement 4: CRCM-REQ-F-025 (error handling)

#### Acceptance criteria

1. If the customer update fails for any reason other than customer not found, then the system shall set the return code to '90' and log an error message with date, time, customer number, the request ' UPDATE CUST ' and the database return code, followed by up to the first 90 bytes of the request. (rules CRCM-BR-033)
2. GIVEN customer number: 1000042; database result: SQLCODE -911 WHEN the customer update fails for any reason other than customer not found THEN Return code '90'; an error message naming ' UPDATE CUST ', customer 1000042 and SQLCODE -911 is written to the log queue. (CRCM-C06-AC-04; CRCM-BR-033)

### Requirement 5: CRCM-REQ-F-026 (design note)

#### Acceptance criteria

1. When the customer details update step has completed, the system shall pass the customer request data and return code, with a length of 225, on to the customer file update step. (rules CRCM-BR-034)
2. GIVEN CA-REQUEST-ID: 01UCUS; CA-CUSTOMER-NUM: 0000000001; CA-LAST-NAME: SMITH WHEN the customer details update step has completed THEN After the customer row is updated, LGUCDB01 links to 'LGUCVS01' with the same customer request area, passing its first 225 bytes (request ID, return code, customer number and customer details), then returns to its caller. (CRCM-C06-AC-05; CRCM-BR-034)

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGUCDB01): see data-contracts.md.
- LGPOLICY (working storage of LGUCDB01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CRCM-BR-030 | Default outcome to success and update | design note | WHEN a customer update request is received, THE Customer Details Maintenance SHALL first set the return code to '00' (success) and then update the customer record whose customer number matches the request. | high | base/src/lgucdb01.cbl:123-134, base/src/lgucdb01.cbl:152-181, base/src/lgucdb01.cbl:189-222 |
| CRCM-BR-031 | Update customer personal and contact details | business rule | WHEN a customer update is processed, THE Customer Details Maintenance SHALL overwrite first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email address of the matching customer with the supplied values, unconditionally, so a blank supplied value blanks the stored value. | high | base/src/lgucdb01.cbl:123-134, base/src/lgucdb01.cbl:152-181, base/src/lgucdb01.cbl:189-222 |
| CRCM-BR-032 | Report customer not found | error handling | WHEN no customer matches the supplied customer number, THE Customer Details Maintenance SHALL set the return code to '01' (customer not found) without writing an error log entry. | high | base/src/lgucdb01.cbl:123-134, base/src/lgucdb01.cbl:152-181, base/src/lgucdb01.cbl:189-222 |
| CRCM-BR-033 | Update customer personal and contact details | error handling | WHEN the customer update fails for any reason other than customer not found, THE Customer Details Maintenance SHALL set the return code to '90' and log an error message with date, time, customer number, the request ' UPDATE CUST ' and the database return code, followed by up to the first 90 bytes of the request. | high | base/src/lgucdb01.cbl:123-134, base/src/lgucdb01.cbl:152-181, base/src/lgucdb01.cbl:189-222 |
| CRCM-BR-034 | Pass request to follow-on program | design note | WHEN the customer details update step has completed, THE Customer Update Orchestration SHALL delegate to the follow-on program (`LGUCVS01`), passing the customer request data and return code with a length of 225 | medium | base/src/lgucdb01.cbl:136-139, base/src/lgucdb01.cbl:133-143 |

### Worked examples

- CRCM-BR-030: customer number = 1000042 → Return code starts as '00' and the update of customer 1000042 is attempted.
- CRCM-BR-031: customer number = 1000042; last name = SMITH; email address = (blank) → Customer 1000042 is stored with last name SMITH and a blank email address; return code '00'.
- CRCM-BR-032: customer number = 9999999999; customer exists = no → Return code '01'; nothing is logged.
- CRCM-BR-033: customer number = 1000042; database result = SQLCODE -911 → Return code '90'; an error message naming ' UPDATE CUST ', customer 1000042 and SQLCODE -911 is written to the log queue.
- CRCM-BR-034: CA-REQUEST-ID = 01UCUS; CA-CUSTOMER-NUM = 0000000001; CA-LAST-NAME = SMITH → After the customer row is updated, LGUCDB01 links to 'LGUCVS01' with the same customer request area, passing its first 225 bytes (request ID, return code, customer number and customer details), then returns to its caller.

## Decision tables

#### Customer details update outcome

| Customer matching the customer number | Database update | Return code and logging | Rule |
|---|---|---|---|
| Found | Succeeds | Return code '00'; details overwritten with supplied values | CRCM-BR-031 |
| Not found | - | Return code '01'; no error log entry | CRCM-BR-032 |
| Found | Fails | Return code '90'; error ' UPDATE CUST ' logged | CRCM-BR-033 |


## Design notes

- CRCM-BR-030: Default the outcome to '00', then update the customer row found by a keyed lookup on the customer number in the request. The update has to tell 'no matching row' (outcome '01') apart from any other database failure (outcome '90').
- CRCM-BR-034: When the database update step has finished, hand the customer record (225 bytes of customer data) and its return code to the customer-file update step, which brings the customer file into line with the database.

## Open questions

- SME-088: When a customer's details are updated, the second copy of the customer record is always replaced afterwards. Should that copy be replaced only when the main database update succeeded, and not when the customer was not found or the update failed? (Data architect) On CRCM-BR-034, CRCM-BR-030, CRCM-BR-031, CRCM-BR-032, CRCM-BR-033.
- SME-089: A customer update writes to two stores. If the second write fails, the first is not undone. Should the two updates succeed or fail together? (Solution architect) On CRCM-BR-034, CRCM-BR-030, CRCM-BR-031, CRCM-BR-032, CRCM-BR-033.
- SME-090: When a customer update fails for a reason other than 'customer not found', what result code should the caller receive? (Business analyst, customer maintenance) On CRCM-BR-034, CRCM-BR-030, CRCM-BR-031, CRCM-BR-032, CRCM-BR-033.
- SME-091: A customer details update returns a number of policies set to '00'. What is this field for in the reply, and should it be kept? (Business analyst, customer maintenance) On CRCM-BR-034, CRCM-BR-030, CRCM-BR-031, CRCM-BR-032, CRCM-BR-033.
- DEF-019: Is this intended? After the customer table update, the program always goes on to update the customer file (LGUCVS01) even when the table update returned '01' or '90', so the file copy can be changed when the database was not; the policy delete path (LGDPDB01) instead returns before its file step on a database error. (Subject-matter expert) On CRCM-BR-030, CRCM-BR-031, CRCM-BR-032, CRCM-BR-033.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).
