# Feature specification: Copy the new customer to the customer file

**Feature:** CRCM-C03 · Customer Record Creation and Maintenance · Customer Record Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CRCM-C03)

As a customer service user, I want each newly added customer to be written to the customer file as well, so that the customer details are held in every store.

After a new customer is stored, writes a copy of the full customer record to the customer file, keyed by the 10-digit customer number, so every store holds the same details. If that write fails for any reason, including a customer number that already exists, it must return code '80', log the failure with the request data and stop. It must never leave the failure unrecorded.

**Acceptance scenarios:**

1. **Given** customer number: 0001000042; first name: Jane; last name: Smith; date of birth: 1980-05-14; postcode: SO21 2JN, **when** a new customer has been added, **then** A 225-byte record with key 0001000042 is written to KSDSCUST (CRCM-C03-AC-01)
2. **Given** customer number: 0001000042; KSDSCUST already holds key: 0001000042, **when** the write to the customer file KSDSCUST does not complete normally for any reason (for example the customer number already exists), **then** Return code '80' is set, an error is logged, and the task abends with 'LGV0' (CRCM-C03-AC-02)
3. **Given** request length: 225 bytes, **when** the failure is logged and request data was received, **then** A second message 'COMMAREA=' plus the first 90 bytes of the request is logged (CRCM-C03-AC-03)
4. **Given** A new-customer request has passed validation and the customer row has been inserted successfully under the assigned customer number 0000001234, **when** Customer registration continues to the customer copy step, **then** The copy step receives the full 225-byte customer request data, and the customer number field in that data holds 0000001234 (CRCM-C03-AC-04)
5. **Given** A new customer 0000001234 has been added, and the customer file KSDSCUST already holds a record under customer number 0000001234, **when** The add-customer file step tries to write the new customer to KSDSCUST and the write fails, **then** A log message is written that holds the current date in MMDDYYYY form, the time in HHMMSS form, 'LGACVS01', customer number 0000001234, 'Write file KSDSCUST' and the response codes of the failed write (CRCM-C03-AC-05)

## Requirements

### Functional requirements

- **CRCM-REQ-F-010** (design note): When a new-customer request has been inserted successfully, the system shall pass the full 225-byte request data, including the assigned customer number, to the customer copy step. Rules: CRCM-BR-016.
- **CRCM-REQ-F-011** (design note): When a new customer has been added, the system shall write a 225-byte record to the customer file KSDSCUST, keyed by the 10-digit customer number, holding the customer number, first and last name, date of birth, house name, house number, postcode, number of policies, mobile phone, home phone and email address. Rules: CRCM-BR-017.
- **CRCM-REQ-F-012** (error handling): If the write to the customer file KSDSCUST does not complete normally for any reason (for example the customer number already exists), then the system shall set return code '80', log the failure with its response codes, and abend the task with code 'LGV0' without a dump. Rules: CRCM-BR-018.
- **CRCM-REQ-F-013** (side effect): If writing a new customer to the customer file KSDSCUST fails, then the system shall log a message with the date (MMDDYYYY), time (HHMMSS), 'LGACVS01', the customer number, 'Write file KSDSCUST' and the response codes. Rules: CRCM-BR-019.
- **CRCM-REQ-F-014** (side effect): When a customer file write failure is logged, if request data was received, then the system shall also log 'COMMAREA=' followed by the first 90 bytes of the request, or the whole request if it is shorter than 91 bytes. Rules: CRCM-BR-020.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CRCM-BR-016 | Register customer and hand off to copy program | design note | WHEN a validated new-customer request has been inserted successfully, THE Customer Registration SHALL delegate to the customer copy program (`LGACVS01`) with the full 225-byte request data, including the assigned customer number | medium | base/src/lgacdb01.cbl:171-172,174-177, base/src/lgacdb01.cbl:174-177 |
| CRCM-BR-017 | Write new customer record | design note | WHEN a new customer has been added, THE add-customer file step SHALL write a 225-byte record to the customer file KSDSCUST, keyed by the 10-digit customer number, holding the customer number, first and last name, date of birth, house name, house number, postcode, number of policies, mobile phone, home phone and email address. | high | base/src/lgacvs01.cbl:49, base/src/lgacvs01.cbl:66-81, base/src/lgcmarea.cpy:10-25 |
| CRCM-BR-018 | Write new customer record | error handling | WHEN the write to the customer file KSDSCUST does not complete normally for any reason (for example the customer number already exists), THE add-customer file step SHALL set return code '80', log the failure with its response codes, and abend the task with code 'LGV0' without a dump. | high | base/src/lgacvs01.cbl:49, base/src/lgacvs01.cbl:66-81, base/src/lgcmarea.cpy:10-25 |
| CRCM-BR-019 | VSAM customer-file failures are recorded in an audit log with a timestamp and the request data | side effect | WHEN writing a new customer to the customer file KSDSCUST fails, THE add-customer file step SHALL log a message with the date (MMDDYYYY), time (HHMMSS), 'LGACVS01', the customer number, 'Write file KSDSCUST' and the response codes, through the shared logging program (LGSTSQ). | medium | base/src/lgacvs01.cbl:30-47, base/src/lgacvs01.cbl:89-120 |
| CRCM-BR-020 | VSAM customer-file failures are recorded in an audit log with a timestamp and the request data | side effect | WHEN the failure is logged and request data was received, THE add-customer file step SHALL also log 'COMMAREA=' followed by the first 90 bytes of the request, or the whole request if it is shorter than 91 bytes. | medium | base/src/lgacvs01.cbl:30-47, base/src/lgacvs01.cbl:89-120 |

### Key entities

- LGCMAREA (file record)
- LGPOLICY (working storage)

### Needs clarification

- SME-015: Every new customer gets the same fixed initial password. Is this shared default password meant to be used in production, and should the new system keep it or create a separate password for each customer? (Security team) On CRCM-BR-016, CRCM-BR-018.
- SME-024: When an add-customer request is shorter than the required 90 characters, the rules disagree: some say the return code is '98', and others say the request comes back with the default '00'. Which return code must the new system give for a short request? (Business analyst) On CRCM-BR-016, CRCM-BR-018.
- SME-025: After a new customer is inserted, the customer record is written to the VSAM customer file and a customer security record is created. In what order must these happen, and must both happen for every new customer? (Solution architect) On CRCM-BR-016, CRCM-BR-018.
- SME-026: Is the VSAM customer file still the main record for any process? If writing to the VSAM file or creating the security record fails after the customer has been inserted into the database, must the database insert be rolled back, and which store is the master copy after a partial failure? (Solution architect) On CRCM-BR-016, CRCM-BR-018.
- SME-027: When the counter is unavailable, the database generates the customer number instead. What format must customer numbers have, and how is it guaranteed that numbers from the two methods never clash, given that the VSAM customer key is 10 characters? (Data architect) On CRCM-BR-016, CRCM-BR-018.
- SME-028: Customer security requests with a request type other than '02ACUS' are passed to handling outside this process. Should the new system reject these requests, ignore them, or handle them somewhere else? (Business analyst) On CRCM-BR-016, CRCM-BR-018.
- DEF-011: Confirm this is deliberate: The return code '80' is set just before the task abends, and the CICS RETURN after the abend never runs, so the caller never sees the '80' code; the add then fails as an abend instead of a return code. (Subject-matter expert) On CRCM-BR-018.

### Decision table gaps

None.
