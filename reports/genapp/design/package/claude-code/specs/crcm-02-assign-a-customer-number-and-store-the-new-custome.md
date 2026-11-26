# Assign a customer number and store the new customer (CRCM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Record Management · Customer Record Creation and Maintenance · runs as scheduled job · risk high

## Introduction

Gives each new customer a unique customer number, stores the customer's personal and contact details under it and returns the number to the caller. The number normally comes from a shared counter, and the database assigns it when the counter does not respond. If the customer cannot be stored, the service must return code '90' with no customer number and must not create the customer-file copy or the security record.

**User story:** As a customer service user, I want each new customer to be stored under a new customer number, so that the customer can be identified in later requests.

## Requirements

### Requirement 1: CRCM-REQ-F-005 (business rule)

#### Acceptance criteria

1. When the shared customer-number counter 'GENACUSTNUM' in pool 'GENA' returns a value normally, the system shall store the new customer under that value as the customer number and return it to the caller. (rules CRCM-BR-009, CRCM-BR-010)
2. GIVEN counter GENACUSTNUM response: NORMAL; counter value: 1000042; last name: SMITH WHEN the shared customer-number counter 'GENACUSTNUM' in pool 'GENA' returns a value normally THEN The customer row is stored with customer number 1000042 and the caller receives customer number 0001000042. (CRCM-C02-AC-01; CRCM-BR-009)
3. GIVEN counter value: 1000042; first name: JOHN; house number: 12 WHEN the customer-number counter supplied the number THEN The customer row 1000042 is stored with first name JOHN and house number 12. (CRCM-C02-AC-02; CRCM-BR-010)

### Requirement 2: CRCM-REQ-F-006 (business rule)

#### Acceptance criteria

1. If the request to the customer-number counter does not respond normally, then the system shall mark the counter unavailable ('NO'), let the database assign the customer number, read back the number the database assigned and return that number to the caller. (rules CRCM-BR-011)
2. GIVEN counter GENACUSTNUM response: not NORMAL (e.g. counter not defined); number the database assigns: 5003 WHEN the request to the customer-number counter does not respond normally THEN The customer row is stored with customer number 5003 and the caller receives customer number 0000005003. (CRCM-C02-AC-03; CRCM-BR-011)

### Requirement 3: CRCM-REQ-F-007 (design note)

#### Acceptance criteria

1. The system shall store on the new customer row the first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email address given in the request, whichever way the customer number was assigned. (rules CRCM-BR-012, CRCM-BR-010)
2. GIVEN counter value: 1000042; first name: JOHN; house number: 12 WHEN the customer-number counter supplied the number THEN The customer row 1000042 is stored with first name JOHN and house number 12. (CRCM-C02-AC-02; CRCM-BR-010)
3. GIVEN first name: JOHN; last name: SMITH; date of birth: 1980-05-01; postcode: AB1 2CD WHEN customer add runs THEN The new customer row holds JOHN, SMITH, 1980-05-01 and AB1 2CD along with the other supplied contact details. (CRCM-C02-AC-04; CRCM-BR-012)

### Requirement 4: CRCM-REQ-F-008 (error handling)

#### Acceptance criteria

1. If the database rejects the new customer row for any reason (for example a duplicate customer number or an invalid date of birth), on either numbering path, then the system shall set return code '90' and return to the caller at once without returning a customer number, so neither the customer file copy nor the customer security record is created. (rules CRCM-BR-013, CRCM-BR-014)
2. GIVEN counter GENACUSTNUM response: not NORMAL; database insert result: SQLCODE -180 WHEN storing the new customer row fails on either numbering path THEN Return code '90' is given back and no customer number is read back or returned. (CRCM-C02-AC-05; CRCM-BR-013)
3. GIVEN counter value: 1000042; database insert result: SQLCODE -803 (customer number already exists) WHEN the database rejects the new customer row for any reason (for example a duplicate customer number or an invalid date of birth), on either numbering path THEN Return code '90'; no customer file copy and no security record are created. (CRCM-C02-AC-06; CRCM-BR-014)
4. GIVEN counter GENACUSTNUM response: not NORMAL; database insert result: SQLCODE -180 (invalid date of birth) WHEN the database rejects the new customer row for any reason (for example a duplicate customer number or an invalid date of birth), on either numbering path THEN Return code '90'; no customer file copy and no security record are created. (CRCM-C02-AC-07; CRCM-BR-014)

### Requirement 5: CRCM-REQ-F-009 (side effect)

#### Acceptance criteria

1. If the new customer row cannot be stored, then the system shall send an error message to the error queue holding the date, time, program 'LGACDB01', the request ' INSERT CUSTOMER' and the database result code, followed by a second message with up to the first 90 characters of the request. (rules CRCM-BR-015, CRCM-BR-013)
2. GIVEN counter GENACUSTNUM response: not NORMAL; database insert result: SQLCODE -180 WHEN storing the new customer row fails on either numbering path THEN Return code '90' is given back and no customer number is read back or returned. (CRCM-C02-AC-05; CRCM-BR-013)

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGACDB01): see data-contracts.md.
- LGPOLICY (working storage of LGACDB01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CRCM-BR-009 | Obtain new customer number from counter | business rule | WHEN the shared customer-number counter 'GENACUSTNUM' in pool 'GENA' returns a value normally, THE customer add SHALL store the new customer under that value as the customer number and return it to the caller (CA-CUSTOMER-NUM). | high | base/src/lgacdb01.cbl:37-39, base/src/lgacdb01.cbl:73, base/src/lgacdb01.cbl:171-172, base/src/lgacdb01.cbl:199-211 |
| CRCM-BR-010 | Insert customer with counter-issued number | design note | WHEN the customer-number counter supplied the number, THE customer add SHALL store the customer row under that number with the supplied name, date of birth, address, phone numbers and email address. | high | base/src/lgacdb01.cbl:171-189, base/src/lgacdb01.cbl:219-249, base/src/lgacdb01.cbl:274-278, base/src/lgacdb01.cbl:295-327 |
| CRCM-BR-011 | Obtain new customer number from counter | business rule | WHEN the request to the customer-number counter does not respond normally, THE customer add SHALL mark the counter unavailable ('NO'), let the database assign the customer number, read back the number the database assigned (IDENTITY_VAL_LOCAL) and return that number to the caller. | high | base/src/lgacdb01.cbl:37-39, base/src/lgacdb01.cbl:73, base/src/lgacdb01.cbl:171-172, base/src/lgacdb01.cbl:199-211 |
| CRCM-BR-012 | Insert customer with counter-assigned number | design note | THE customer add SHALL store on the new customer row the first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email address given in the request, whichever way the customer number was assigned. | high | base/src/lgacdb01.cbl:37-39, base/src/lgacdb01.cbl:73, base/src/lgacdb01.cbl:171-172, base/src/lgacdb01.cbl:199-211 |
| CRCM-BR-013 | Insert customer with generated number and return it | error handling | WHEN storing the new customer row fails on either numbering path, THE customer add SHALL set return code '90', log an error message and return to the caller at once without returning a customer number. | high | base/src/lgacdb01.cbl:37-39, base/src/lgacdb01.cbl:73, base/src/lgacdb01.cbl:171-172, base/src/lgacdb01.cbl:199-211 |
| CRCM-BR-014 | Insert customer with counter-issued number | error handling | WHEN the database rejects the new customer row for any reason (for example a duplicate customer number or an invalid date of birth), on either numbering path, THE customer add SHALL set return code '90' and return to the caller at once, so neither the customer file copy (LGACVS01) nor the customer security record (LGACDB02) is created. | high | base/src/lgacdb01.cbl:171-189, base/src/lgacdb01.cbl:219-249, base/src/lgacdb01.cbl:274-278, base/src/lgacdb01.cbl:295-327 |
| CRCM-BR-015 | Insert customer with counter-assigned number | side effect | WHEN the new customer row cannot be stored, THE customer add SHALL send an error message to the error queue (through LGSTSQ) holding the date, time, program 'LGACDB01', the request ' INSERT CUSTOMER' and the database result code, followed by a second message with up to the first 90 characters of the request. | high | base/src/lgacdb01.cbl:171-189, base/src/lgacdb01.cbl:219-249, base/src/lgacdb01.cbl:274-278, base/src/lgacdb01.cbl:295-327 |

### Worked examples

- CRCM-BR-009: counter GENACUSTNUM response = NORMAL; counter value = 1000042; last name = SMITH → The customer row is stored with customer number 1000042 and the caller receives customer number 0001000042.
- CRCM-BR-010: counter value = 1000042; first name = JOHN; house number = 12 → The customer row 1000042 is stored with first name JOHN and house number 12.
- CRCM-BR-011: counter GENACUSTNUM response = not NORMAL (e.g. counter not defined); number the database assigns = 5003 → The customer row is stored with customer number 5003 and the caller receives customer number 0000005003.
- CRCM-BR-012: first name = JOHN; last name = SMITH; date of birth = 1980-05-01; postcode = AB1 2CD → The new customer row holds JOHN, SMITH, 1980-05-01 and AB1 2CD along with the other supplied contact details.
- CRCM-BR-013: counter GENACUSTNUM response = not NORMAL; database insert result = SQLCODE -180 → Return code '90' is given back and no customer number is read back or returned.
- CRCM-BR-014: counter value = 1000042; database insert result = SQLCODE -803 (customer number already exists) → Return code '90'; no customer file copy and no security record are created.
- CRCM-BR-014: counter GENACUSTNUM response = not NORMAL; database insert result = SQLCODE -180 (invalid date of birth) → Return code '90'; no customer file copy and no security record are created.

## Decision tables

#### Customer numbering and insert outcome

| Customer-number counter responds normally | New customer row stored | Customer number and return code | Rule |
|---|---|---|---|
| Yes | Yes | Customer stored under the counter value; that number returned to the caller | CRCM-BR-009 |
| No | Yes | Counter marked unavailable ('NO'); database-assigned number read back and returned to the caller | CRCM-BR-011 |
| Yes | No | Return code '90'; return at once without a customer number | CRCM-BR-014 |
| No | No | Return code '90'; return at once without a customer number | CRCM-BR-014 |


## Design notes

- CRCM-BR-010: When the shared customer-number counter supplies the number, insert the customer row under that explicit key, together with the supplied name, date of birth, address, phone numbers and email. The key must be unique, so a clash with an existing customer is rejected rather than overwritten.
- CRCM-BR-012: Both numbering paths, counter-issued or database-generated, must write the same nine fields: first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email. A single insert routine, with the key either supplied or generated, keeps the two paths consistent.

## Open questions

- SME-015: Every new customer gets the same fixed initial password. Is this shared default password meant to be used in production, and should the new system keep it or create a separate password for each customer? (Security team) On CRCM-BR-011, CRCM-BR-013, CRCM-BR-014, CRCM-BR-015.
- SME-024: When an add-customer request is shorter than the required 90 characters, the rules disagree: some say the return code is '98', and others say the request comes back with the default '00'. Which return code must the new system give for a short request? (Business analyst) On CRCM-BR-011, CRCM-BR-013, CRCM-BR-014, CRCM-BR-015.
- SME-025: After a new customer is inserted, the customer record is written to the VSAM customer file and a customer security record is created. In what order must these happen, and must both happen for every new customer? (Solution architect) On CRCM-BR-011, CRCM-BR-013, CRCM-BR-014, CRCM-BR-015.
- SME-026: Is the VSAM customer file still the main record for any process? If writing to the VSAM file or creating the security record fails after the customer has been inserted into the database, must the database insert be rolled back, and which store is the master copy after a partial failure? (Solution architect) On CRCM-BR-011, CRCM-BR-013, CRCM-BR-014, CRCM-BR-015.
- SME-027: When the counter is unavailable, the database generates the customer number instead. What format must customer numbers have, and how is it guaranteed that numbers from the two methods never clash, given that the VSAM customer key is 10 characters? (Data architect) On CRCM-BR-011, CRCM-BR-013, CRCM-BR-014, CRCM-BR-015.
- SME-028: Customer security requests with a request type other than '02ACUS' are passed to handling outside this process. Should the new system reject these requests, ignore them, or handle them somewhere else? (Business analyst) On CRCM-BR-011, CRCM-BR-013, CRCM-BR-014, CRCM-BR-015.
- DEF-010: Is this intended? The error message has a customer-number slot that is never filled, so a failed-insert log entry always shows a blank customer number (' CNUM=' followed by spaces), even when the counter had supplied one. (Subject-matter expert) On CRCM-BR-014, CRCM-BR-015.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).
