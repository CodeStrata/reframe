# Requirements: Assign a customer number and store the new customer (CRCM-C02)

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
