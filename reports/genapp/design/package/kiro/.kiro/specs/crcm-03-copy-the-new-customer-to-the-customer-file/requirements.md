# Requirements: Copy the new customer to the customer file (CRCM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Record Management · Customer Record Creation and Maintenance · runs as scheduled job · risk high

## Introduction

After a new customer is stored, writes a copy of the full customer record to the customer file, keyed by the 10-digit customer number, so every store holds the same details. If that write fails for any reason, including a customer number that already exists, it must return code '80', log the failure with the request data and stop. It must never leave the failure unrecorded.

**User story:** As a customer service user, I want each newly added customer to be written to the customer file as well, so that the customer details are held in every store.

## Requirements

### Requirement 1: CRCM-REQ-F-010 (design note)

#### Acceptance criteria

1. When a new-customer request has been inserted successfully, the system shall pass the full 225-byte request data, including the assigned customer number, to the customer copy step. (rules CRCM-BR-016)
2. GIVEN A new-customer request has passed validation and the customer row has been inserted successfully under the assigned customer number 0000001234 WHEN Customer registration continues to the customer copy step THEN The copy step receives the full 225-byte customer request data, and the customer number field in that data holds 0000001234 (CRCM-C03-AC-04; CRCM-BR-016)

### Requirement 2: CRCM-REQ-F-011 (design note)

#### Acceptance criteria

1. When a new customer has been added, the system shall write a 225-byte record to the customer file KSDSCUST, keyed by the 10-digit customer number, holding the customer number, first and last name, date of birth, house name, house number, postcode, number of policies, mobile phone, home phone and email address. (rules CRCM-BR-017)
2. GIVEN customer number: 0001000042; first name: Jane; last name: Smith; date of birth: 1980-05-14; postcode: SO21 2JN WHEN a new customer has been added THEN A 225-byte record with key 0001000042 is written to KSDSCUST (CRCM-C03-AC-01; CRCM-BR-017)

### Requirement 3: CRCM-REQ-F-012 (error handling)

#### Acceptance criteria

1. If the write to the customer file KSDSCUST does not complete normally for any reason (for example the customer number already exists), then the system shall set return code '80', log the failure with its response codes, and abend the task with code 'LGV0' without a dump. (rules CRCM-BR-018)
2. GIVEN customer number: 0001000042; KSDSCUST already holds key: 0001000042 WHEN the write to the customer file KSDSCUST does not complete normally for any reason (for example the customer number already exists) THEN Return code '80' is set, an error is logged, and the task abends with 'LGV0' (CRCM-C03-AC-02; CRCM-BR-018)

### Requirement 4: CRCM-REQ-F-013 (side effect)

#### Acceptance criteria

1. If writing a new customer to the customer file KSDSCUST fails, then the system shall log a message with the date (MMDDYYYY), time (HHMMSS), 'LGACVS01', the customer number, 'Write file KSDSCUST' and the response codes. (rules CRCM-BR-019)
2. GIVEN A new customer 0000001234 has been added, and the customer file KSDSCUST already holds a record under customer number 0000001234 WHEN The add-customer file step tries to write the new customer to KSDSCUST and the write fails THEN A log message is written that holds the current date in MMDDYYYY form, the time in HHMMSS form, 'LGACVS01', customer number 0000001234, 'Write file KSDSCUST' and the response codes of the failed write (CRCM-C03-AC-05; CRCM-BR-019)

### Requirement 5: CRCM-REQ-F-014 (side effect)

#### Acceptance criteria

1. When a customer file write failure is logged, if request data was received, then the system shall also log 'COMMAREA=' followed by the first 90 bytes of the request, or the whole request if it is shorter than 91 bytes. (rules CRCM-BR-020)
2. GIVEN request length: 225 bytes WHEN the failure is logged and request data was received THEN A second message 'COMMAREA=' plus the first 90 bytes of the request is logged (CRCM-C03-AC-03; CRCM-BR-020)
