# Design: Create the new customer's security record (CRCM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Creates the sign-on security record for every new customer: the customer number, the initial password, a password change count of zero and the state 'N'. Only a new-customer security request (type '02ACUS') may add a record, and any other type is refused with '99'. It must never skip a new customer or add a security record for a request that is not a new-customer request.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGACDB01): see data-contracts.md.
- LGPOLICY (working storage of LGACDB01, LGACDB02): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CRCM-BR-021 | Request customer security record creation | business rule | WHEN a new customer has been added and assigned a customer number, THE Customer Security Setup SHALL delegate to the customer security program (`LGACDB02`) with request type `'02ACUS'`, the new customer number, initial password `'5732fec825535eeafb8fac50fee3a8aa'`, attempt count `'0000'` and state `'N'` | medium | base/src/lgacdb01.cbl:171-172,179-184,186-189, base/src/lgacdb01.cbl:179-189 |
| CRCM-BR-022 | Route new customer security add request | business rule | WHEN the security add request type is '02ACUS' (new customer), THE customer security registration SHALL convert the customer number and password change count to numbers and add the customer's security record. | medium | base/src/lgacdb02.cbl:143-152 |
| CRCM-BR-023 | Insert customer security record | business rule | WHEN a new-customer security add is requested, THE customer security registration SHALL insert the customer number, password, state indicator and password change count into the customer secure table (CUSTOMER_SECURE). | medium | base/src/lgacdb02.cbl:161-184, base/src/lgacdb02.cbl:192-208 |
| CRCM-BR-024 | Route new customer security add request | business rule | WHEN the security add request type is anything other than '02ACUS', THE customer security registration SHALL set return code '99' and return without adding a record. | medium | base/src/lgacdb02.cbl:143-152 |
| CRCM-BR-025 | Insert customer security record | error handling | WHEN inserting the security record fails, THE customer security registration SHALL set return code '98', log an error labelled ' INSERT SECURITY' with the SQL code, date and time, and return to the caller. | medium | base/src/lgacdb02.cbl:161-184, base/src/lgacdb02.cbl:192-208 |

### Worked examples

- CRCM-BR-021: CA-REQUEST-ID = '01ACUS'; Assigned customer number = 1000042 → LGACDB01 LINKs to 'LGACDB02' with D2-REQUEST-ID '02ACUS', D2-CUSTOMER-NUM 1000042, D2-CUSTSECR-PASS '5732fec825535eeafb8fac50fee3a8aa', D2-CUSTSECR-COUNT '0000' and D2-CUSTSECR-STATE 'N'
- CRCM-BR-022: request type = '02ACUS'; customer number = 0000000123; change count = '0000' → A security record is inserted for customer 123 with 0 password changes
- CRCM-BR-023: customer number = 0000000123; password = '5732fec825535eeafb8fac50fee3a8aa'; state = 'N'; change count = '0000' → A CUSTOMER_SECURE row is added for customer 123
- CRCM-BR-025: insert result = SQL code -803 → Return code '98'; ' INSERT SECURITY' error logged

## Decision tables

#### Customer security record add

| Security request type | Security record insert | Result | Rule |
|---|---|---|---|
| '02ACUS' | Succeeds | Security record added to CUSTOMER_SECURE | CRCM-BR-023 |
| '02ACUS' | Fails | Return code '98'; error ' INSERT SECURITY' logged | CRCM-BR-025 |
| Other than '02ACUS' | - | Return code '99'; no record added | CRCM-BR-024 |


## Design notes

None.

## Open questions

- SME-015: Every new customer gets the same fixed initial password. Is this shared default password meant to be used in production, and should the new system keep it or create a separate password for each customer? (Security team) On CRCM-BR-021, CRCM-BR-024, CRCM-BR-025.
- SME-024: When an add-customer request is shorter than the required 90 characters, the rules disagree: some say the return code is '98', and others say the request comes back with the default '00'. Which return code must the new system give for a short request? (Business analyst) On CRCM-BR-021, CRCM-BR-024, CRCM-BR-025.
- SME-025: After a new customer is inserted, the customer record is written to the VSAM customer file and a customer security record is created. In what order must these happen, and must both happen for every new customer? (Solution architect) On CRCM-BR-021, CRCM-BR-024, CRCM-BR-025.
- SME-026: Is the VSAM customer file still the main record for any process? If writing to the VSAM file or creating the security record fails after the customer has been inserted into the database, must the database insert be rolled back, and which store is the master copy after a partial failure? (Solution architect) On CRCM-BR-021, CRCM-BR-024, CRCM-BR-025.
- SME-027: When the counter is unavailable, the database generates the customer number instead. What format must customer numbers have, and how is it guaranteed that numbers from the two methods never clash, given that the VSAM customer key is 10 characters? (Data architect) On CRCM-BR-021, CRCM-BR-024, CRCM-BR-025.
- SME-028: Customer security requests with a request type other than '02ACUS' are passed to handling outside this process. Should the new system reject these requests, ignore them, or handle them somewhere else? (Business analyst) On CRCM-BR-021, CRCM-BR-024, CRCM-BR-025.
- SME-029: What do security state 'N' and the count field mean (for example, 'N' means new or must change password, and count means failed logins)? What other states exist, and which process increases the count and moves a customer out of state 'N'? (Security officer) On CRCM-BR-021.
- DEF-041: Is this intended? The caller (LGACDB01) does not check the return code after linking to LGACDB02, so a failed security insert leaves a new customer without a security record and the failure is not reported to the user. (Subject-matter expert) On CRCM-BR-025.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).