# Requirements: Update the customer's personal and contact details (CRCM-C06)

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
