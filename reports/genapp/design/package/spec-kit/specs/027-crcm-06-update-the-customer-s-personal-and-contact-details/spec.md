# Feature specification: Update the customer's personal and contact details

**Feature:** CRCM-C06 · Customer Record Creation and Maintenance · Customer Record Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CRCM-C06)

As a customer service user, I want to update an existing customer's personal and contact details, so that the stored customer record stays current.

Updates an existing customer's name, date of birth, address, phone numbers and email in the customer database, then passes the change on so that the customer file is updated too. Every supplied field replaces the stored one, so a blank field blanks the stored value. An unknown customer must return '01' with no error log, and any other failure must return '90' and be logged.

**Acceptance scenarios:**

1. **Given** customer number: 1000042, **when** a customer update request is received, **then** Return code starts as '00' and the update of customer 1000042 is attempted. (CRCM-C06-AC-01)
2. **Given** customer number: 1000042; last name: SMITH; email address: (blank), **when** a customer update is processed, **then** Customer 1000042 is stored with last name SMITH and a blank email address; return code '00'. (CRCM-C06-AC-02)
3. **Given** customer number: 9999999999; customer exists: no, **when** no customer matches the supplied customer number, **then** Return code '01'; nothing is logged. (CRCM-C06-AC-03)
4. **Given** customer number: 1000042; database result: SQLCODE -911, **when** the customer update fails for any reason other than customer not found, **then** Return code '90'; an error message naming ' UPDATE CUST ', customer 1000042 and SQLCODE -911 is written to the log queue. (CRCM-C06-AC-04)
5. **Given** CA-REQUEST-ID: 01UCUS; CA-CUSTOMER-NUM: 0000000001; CA-LAST-NAME: SMITH, **when** the customer details update step has completed, **then** After the customer row is updated, LGUCDB01 links to 'LGUCVS01' with the same customer request area, passing its first 225 bytes (request ID, return code, customer number and customer details), then returns to its caller. (CRCM-C06-AC-05)

## Requirements

### Functional requirements

- **CRCM-REQ-F-022** (design note): When a customer update request is received, the system shall first set the return code to '00' (success) and then update the customer record whose customer number matches the request. Rules: CRCM-BR-030.
- **CRCM-REQ-F-023** (business rule): When a customer update is processed, the system shall overwrite the first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email address of the matching customer with the supplied values, unconditionally, so a blank supplied value blanks the stored value. Rules: CRCM-BR-031.
- **CRCM-REQ-F-024** (error handling): If no customer matches the supplied customer number, then the system shall set the return code to '01' (customer not found) without writing an error log entry. Rules: CRCM-BR-032.
- **CRCM-REQ-F-025** (error handling): If the customer update fails for any reason other than customer not found, then the system shall set the return code to '90' and log an error message with date, time, customer number, the request ' UPDATE CUST ' and the database return code, followed by up to the first 90 bytes of the request. Rules: CRCM-BR-033.
- **CRCM-REQ-F-026** (design note): When the customer details update step has completed, the system shall pass the customer request data and return code, with a length of 225, on to the customer file update step. Rules: CRCM-BR-034.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CRCM-BR-030 | Default outcome to success and update | design note | WHEN a customer update request is received, THE Customer Details Maintenance SHALL first set the return code to '00' (success) and then update the customer record whose customer number matches the request. | high | base/src/lgucdb01.cbl:123-134, base/src/lgucdb01.cbl:152-181, base/src/lgucdb01.cbl:189-222 |
| CRCM-BR-031 | Update customer personal and contact details | business rule | WHEN a customer update is processed, THE Customer Details Maintenance SHALL overwrite first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email address of the matching customer with the supplied values, unconditionally, so a blank supplied value blanks the stored value. | high | base/src/lgucdb01.cbl:123-134, base/src/lgucdb01.cbl:152-181, base/src/lgucdb01.cbl:189-222 |
| CRCM-BR-032 | Report customer not found | error handling | WHEN no customer matches the supplied customer number, THE Customer Details Maintenance SHALL set the return code to '01' (customer not found) without writing an error log entry. | high | base/src/lgucdb01.cbl:123-134, base/src/lgucdb01.cbl:152-181, base/src/lgucdb01.cbl:189-222 |
| CRCM-BR-033 | Update customer personal and contact details | error handling | WHEN the customer update fails for any reason other than customer not found, THE Customer Details Maintenance SHALL set the return code to '90' and log an error message with date, time, customer number, the request ' UPDATE CUST ' and the database return code, followed by up to the first 90 bytes of the request. | high | base/src/lgucdb01.cbl:123-134, base/src/lgucdb01.cbl:152-181, base/src/lgucdb01.cbl:189-222 |
| CRCM-BR-034 | Pass request to follow-on program | design note | WHEN the customer details update step has completed, THE Customer Update Orchestration SHALL delegate to the follow-on program (`LGUCVS01`), passing the customer request data and return code with a length of 225 | medium | base/src/lgucdb01.cbl:136-139, base/src/lgucdb01.cbl:133-143 |

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- SME-088: When a customer's details are updated, the second copy of the customer record is always replaced afterwards. Should that copy be replaced only when the main database update succeeded, and not when the customer was not found or the update failed? (Data architect) On CRCM-BR-034, CRCM-BR-030, CRCM-BR-031, CRCM-BR-032, CRCM-BR-033.
- SME-089: A customer update writes to two stores. If the second write fails, the first is not undone. Should the two updates succeed or fail together? (Solution architect) On CRCM-BR-034, CRCM-BR-030, CRCM-BR-031, CRCM-BR-032, CRCM-BR-033.
- SME-090: When a customer update fails for a reason other than 'customer not found', what result code should the caller receive? (Business analyst, customer maintenance) On CRCM-BR-034, CRCM-BR-030, CRCM-BR-031, CRCM-BR-032, CRCM-BR-033.
- SME-091: A customer details update returns a number of policies set to '00'. What is this field for in the reply, and should it be kept? (Business analyst, customer maintenance) On CRCM-BR-034, CRCM-BR-030, CRCM-BR-031, CRCM-BR-032, CRCM-BR-033.
- DEF-019: Is this intended? After the customer table update, the program always goes on to update the customer file (LGUCVS01) even when the table update returned '01' or '90', so the file copy can be changed when the database was not; the policy delete path (LGDPDB01) instead returns before its file step on a database error. (Subject-matter expert) On CRCM-BR-030, CRCM-BR-031, CRCM-BR-032, CRCM-BR-033.

### Decision table gaps

None.
