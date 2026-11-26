# Feature specification: Replace the customer's record in the customer file

**Feature:** CRCM-C07 · Customer Record Creation and Maintenance · Customer Record Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CRCM-C07)

As a customer service user, I want a customer update to also replace the customer's record in the customer file, so that the customer file matches the updated details.

Keeps the customer file in line with a customer update by replacing the customer's whole stored record with the updated data, found by customer number and locked while it is changed. If the record cannot be read for update, including when the customer is not on the file, the service returns '81'. If the rewrite fails, it returns '82'. Both failures are logged and stop processing, and it must never apply a partial update.

**Acceptance scenarios:**

1. **Given** customer number: 0001000099; customer on file: no, **when** the customer record cannot be read for update for any reason, including the customer not being on the file, **then** Return code '81', error message logged, task abends with 'LGV1'; nothing is rewritten. (CRCM-C07-AC-01)
2. **Given** customer number: 0001000042; rewrite result: failed, **when** rewriting the locked customer record fails, **then** Return code '82', error message logged, task abends with 'LGV2'. (CRCM-C07-AC-02)
3. **Given** The customer file KSDSCUST holds a record for customer number 0000001234 with last name 'SMITH', and a customer update for 0000001234 carries 225 bytes of customer data with last name 'JONES', **when** The customer update reaches the customer file step, **then** The record for 0000001234 is read by its 10-digit customer number and locked for update, and the whole stored record is replaced with the 225 bytes from the request, so the stored last name is 'JONES' and every other field matches the request (CRCM-C07-AC-03)

## Requirements

### Functional requirements

- **CRCM-REQ-F-027** (business rule): When a customer update reaches the customer file step, the system shall read the customer's record in the customer file (KSDSCUST) by the 10-digit customer number, lock it for update, and replace the whole stored record with the 225 bytes of customer data from the request. Rules: CRCM-BR-035.
- **CRCM-REQ-F-028** (error handling): If the customer record cannot be read for update for any reason, including the customer not being on the file, then the system shall set return code '81', write an error message with date, time, customer number and response codes to the error queue, and end the task abnormally with code 'LGV1'. Rules: CRCM-BR-036.
- **CRCM-REQ-F-029** (error handling): If rewriting the locked customer record fails, then the system shall set return code '82', write an error message with date, time, customer number and response codes to the error queue, and end the task abnormally with code 'LGV2'. Rules: CRCM-BR-037.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CRCM-BR-035 | Replace stored customer record | business rule | WHEN a customer update reaches the customer file step, THE Customer Update SHALL read the customer's record in the customer file (KSDSCUST) by the 10-digit customer number and lock it for update, then replace the whole stored record with the 225 bytes of customer data from the request. | high | base/src/lgucvs01.cbl:50, base/src/lgucvs01.cbl:67-96, base/src/lgucvs01.cbl:104-120, base/src/lgucdb01.cbl:136-139 |
| CRCM-BR-036 | Customer update requires an existing record and fully replaces it | error handling | WHEN the customer record cannot be read for update for any reason, including the customer not being on the file, THE Customer Update SHALL set return code '81', write an error message with date, time, customer number and response codes to the error queue (via LGSTSQ), and end the task abnormally with code 'LGV1'. | high | base/src/lgucvs01.cbl:50, base/src/lgucvs01.cbl:67-96, base/src/lgucvs01.cbl:104-120, base/src/lgucdb01.cbl:136-139 |
| CRCM-BR-037 | Replace stored customer record | error handling | WHEN rewriting the locked customer record fails, THE Customer Update SHALL set return code '82', write an error message with date, time, customer number and response codes to the error queue (via LGSTSQ), and end the task abnormally with code 'LGV2'. | high | base/src/lgucvs01.cbl:50, base/src/lgucvs01.cbl:67-96, base/src/lgucvs01.cbl:104-120, base/src/lgucdb01.cbl:136-139 |

### Key entities

- LGCMAREA (file record)

### Needs clarification

- SME-088: When a customer's details are updated, the second copy of the customer record is always replaced afterwards. Should that copy be replaced only when the main database update succeeded, and not when the customer was not found or the update failed? (Data architect) On CRCM-BR-037.
- SME-089: A customer update writes to two stores. If the second write fails, the first is not undone. Should the two updates succeed or fail together? (Solution architect) On CRCM-BR-037.
- SME-090: When a customer update fails for a reason other than 'customer not found', what result code should the caller receive? (Business analyst, customer maintenance) On CRCM-BR-037.
- SME-091: A customer details update returns a number of policies set to '00'. What is this field for in the reply, and should it be kept? (Business analyst, customer maintenance) On CRCM-BR-037.
- DEF-020: Is this intended? The caller (LGUCDB01) links to this step even when its DB2 customer update found no customer (return code '01') or failed ('90'), so a DB2 failure can be followed by a VSAM update or an LGV1 abend. Also, the read failure logs the same ' Re-write KSDSCUST ' message text as a rewrite failure. (Subject-matter expert) On CRCM-BR-037.

### Decision table gaps

None.
