# Design: Validate and register a new policy (ADPLM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Checks an add-policy request, records it as a master policy with a database-assigned policy number, and returns that number and the last-changed timestamp to the caller. It is for policy administrators. It must never create a policy for an unknown request type, for a request too short for its product, or for a customer who does not exist, and each of these failures must return its own code ('99', '98', '70').

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGAPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGAPDB01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-038 | Determine policy type and required length | design note | THE policy add service SHALL start each request with return code '00' and keep the request's customer number for the database insert and for any error message. | high | base/src/lgapdb01.cbl:172-207, base/src/lgapdb01.cbl:209-213, base/src/lgapdb01.cbl:218-246, base/src/lgpolicy.cpy:24-27 |
| ADPLM-BR-039 | End processing for unknown request type | business rule | WHEN an add-policy request has any request ID other than '01AEND', '01AHOU', '01AMOT' or '01ACOM', THE policy add service SHALL return code '99' to the caller at once, without creating any policy. | high | base/src/lgapdb01.cbl:172-207, base/src/lgapdb01.cbl:209-213, base/src/lgapdb01.cbl:218-246, base/src/lgpolicy.cpy:24-27 |
| ADPLM-BR-040 | Reject request shorter than required length | business rule | WHEN an add-policy request is shorter than the 28-byte header plus the full detail length for its type (Endowment '01AEND' 124, House '01AHOU' 130, Motor '01AMOT' 137, Commercial '01ACOM' 1174), THE policy add service SHALL return code '98' to the caller and record nothing. | high | base/src/lgapdb01.cbl:181-213, base/src/lgpolicy.cpy:24-27, base/src/lgapdb01.cbl:65 |
| ADPLM-BR-041 | Determine policy type and required data length | business rule | WHEN an add-policy request is shorter than the 28-character header plus the full record length for its type (124 endowment, 130 house, 137 motor, 1174 commercial), THE policy add service SHALL return code '98' and insert nothing. | high | base/src/lgapdb01.cbl:172-207, base/src/lgapdb01.cbl:209-213, base/src/lgapdb01.cbl:218-246, base/src/lgpolicy.cpy:24-27 |
| ADPLM-BR-042 | Determine policy type and required data length | business rule | WHEN an add-policy request has request ID '01AEND', '01AHOU', '01AMOT' or '01ACOM', THE policy add service SHALL record the new policy's type as 'E' (endowment), 'H' (house), 'M' (motor) or 'C' (commercial) respectively. | high | base/src/lgapdb01.cbl:172-207, base/src/lgapdb01.cbl:209-213, base/src/lgapdb01.cbl:218-246, base/src/lgpolicy.cpy:24-27 |
| ADPLM-BR-043 | Create common policy record | business rule | WHEN a recognised add-policy request ('01AEND', '01AHOU', '01AMOT' or '01ACOM') passes the length check, THE policy add service SHALL insert a policy row holding a database-assigned policy number, the customer number, issue and expiry dates, the policy type ('E', 'H', 'M' or 'C'), the current timestamp as last-changed, broker ID, broker's reference and payment. | high | base/src/lgapdb01.cbl:184-207, base/src/lgapdb01.cbl:219, base/src/lgapdb01.cbl:261-321, base/src/lgapdb01.cbl:562-594 |
| ADPLM-BR-044 | Route to type-specific policy detail insert | business rule | WHEN an add-policy request with request identifier '01AEND', '01AHOU', '01AMOT' or '01ACOM' has passed the length check, THE Policy Registration SHALL first record the policy in the main policy table, then record the endowment, house, motor or commercial details that match the request identifier. | medium | base/src/lgapdb01.cbl:184-213, base/src/lgapdb01.cbl:219, base/src/lgapdb01.cbl:223-241, base/src/lgapdb01.cbl:261-311 |
| ADPLM-BR-045 | Route policy creation by policy type | business rule | WHEN a recognised add-policy request passes the length check, THE policy add service SHALL first insert the master policy row and then the detail row for its type (endowment, house, motor or commercial), then pass the request on to program LGAPVS01. | high | base/src/lgapdb01.cbl:172-207, base/src/lgapdb01.cbl:209-213, base/src/lgapdb01.cbl:218-246, base/src/lgpolicy.cpy:24-27 |
| ADPLM-BR-046 | Create master policy record | business rule | WHEN the policy row is inserted successfully, THE policy add service SHALL set return code '00' and return to the caller the assigned policy number and the last-changed timestamp read back from the stored policy row. | high | base/src/lgapdb01.cbl:184-207, base/src/lgapdb01.cbl:219, base/src/lgapdb01.cbl:261-321, base/src/lgapdb01.cbl:562-594 |
| ADPLM-BR-047 | Stop when policy record insert fails | business rule | WHEN the new policy row is rejected because the customer number is not on the customer table (SQL code -530), THE policy add service SHALL set return code '70', log the error with the customer number, and return to the caller without storing any type-specific details. | high | base/src/lgapdb01.cbl:176-179, base/src/lgapdb01.cbl:261-305, base/src/lgapdb01.cbl:562-594 |
| ADPLM-BR-048 | Insert policy and return assigned identifiers | error handling | WHEN the database rejects the policy insert because a referenced record does not exist (SQLCODE -530, e.g. an unknown customer), THE policy add service SHALL set return code '70', log the error and return to the caller without adding product details. | high | base/src/lgapdb01.cbl:184-207, base/src/lgapdb01.cbl:219, base/src/lgapdb01.cbl:261-321, base/src/lgapdb01.cbl:562-594 |
| ADPLM-BR-049 | Stop when policy record insert fails | error handling | WHEN the new policy row cannot be stored for any other reason, THE policy add service SHALL set return code '90', log the error, and return to the caller without storing any type-specific details. | high | base/src/lgapdb01.cbl:176-179, base/src/lgapdb01.cbl:261-305, base/src/lgapdb01.cbl:562-594 |
| ADPLM-BR-050 | Insert policy and return assigned identifiers | error handling | WHEN the policy insert fails for any other reason, THE policy add service SHALL set return code '90', log the error and return to the caller without adding product details. | high | base/src/lgapdb01.cbl:184-207, base/src/lgapdb01.cbl:219, base/src/lgapdb01.cbl:261-321, base/src/lgapdb01.cbl:562-594 |
| ADPLM-BR-051 | Pass request to follow-on program | design note | WHEN policy registration processing completes without ending early, THE Policy Registration SHALL delegate to the follow-on program (`LGAPVS01`) with the full request data, length 32500 | medium | base/src/lgapdb01.cbl:243-246, base/src/lgapdb01.cbl:243-246 |

### Worked examples

- ADPLM-BR-038: customer number = 0000000001; request ID = '01AEND' → Return code starts as '00' and customer 1 is used for the new policy row.
- ADPLM-BR-040: request = '01AMOT'; request length = 150 bytes → Return code '98' (Motor needs 165 bytes); no policy is inserted.
- ADPLM-BR-040: request = '01ACOM'; request length = 1202 bytes → Length check passes (Commercial needs 1202 bytes); the policy is added.
- ADPLM-BR-041: request ID = '01AMOT'; request length = 150 → Return code '98'; no policy is created (165 is required for motor).
- ADPLM-BR-041: request ID = '01AHOU'; request length = 158 → The length check passes and processing continues.
- ADPLM-BR-042: request ID = '01AMOT' → The policy is recorded with type 'M' (motor).
- ADPLM-BR-042: request ID = '01ACOM' → The policy is recorded with type 'C' (commercial).
- ADPLM-BR-043: request = '01AHOU'; customer number = 1000001; issue date = 2026-01-01; expiry date = 2027-01-01; broker ID = 55; payment = 300 → A policy row is stored with a new number (e.g. 2000123), type 'H', last-changed = the current timestamp, broker 55 and payment 300.
- ADPLM-BR-043: request = '01AMOT'; customer number = 1000002 → A policy row is stored with type 'M' and a database-assigned number.
- ADPLM-BR-044: request identifier = '01AMOT' → A POLICY row of type 'M' is inserted, then a MOTOR row with the new policy number.
- ADPLM-BR-044: request identifier = '01AHOU' → A POLICY row of type 'H' is inserted, then a HOUSE row with the new policy number.
- ADPLM-BR-044: request identifier = '01ACOM' → A POLICY row of type 'C' is inserted, then a COMMERCIAL row with the new policy number.
- ADPLM-BR-045: request ID = '01AHOU' → A POLICY row is inserted, then a HOUSE row for the new policy number, then LGAPVS01 is called.
- ADPLM-BR-046: policy insert = succeeds, number 2000123 assigned → Return code '00'; the caller receives policy number 2000123 and the stored last-changed timestamp, e.g. 2026-11-25-10.15.30.000000.
- ADPLM-BR-047: customer number = 9999999 (not on file) → Return code '70', error logged with CNUM=9999999, no policy or detail row stored.
- ADPLM-BR-048: customer number = 9999999 (not on file); request = '01AHOU' → No policy is added; return code '70'; an error message is logged.
- ADPLM-BR-049: policy insert = fails with a database error other than -530 → Return code '90', error logged, nothing further stored.
- ADPLM-BR-050: policy insert = fails with SQLCODE -911 → No policy is added; return code '90'; an error message is logged.
- ADPLM-BR-051: CA-REQUEST-ID = '01AMOT'; CA-CUSTOMER-NUM = 1000042; Policy and motor inserts = succeed → LGAPDB01 LINKs to 'LGAPVS01' with the full request data, length 32500

## Decision tables

#### Add-policy request outcome

| Request ID | Length check | Policy row insert | Type detail insert | Return code and result | Rule |
|---|---|---|---|---|---|
| Other than '01AEND', '01AHOU', '01AMOT', '01ACOM' | Not applicable | Not attempted | Not attempted | Return code '99'; no policy created | ADPLM-BR-039 |
| '01AEND', '01AHOU', '01AMOT' or '01ACOM' | Shorter than header plus detail length | Not attempted | Not attempted | Return code '98'; nothing recorded | ADPLM-BR-040 |
| '01AEND', '01AHOU', '01AMOT' or '01ACOM' | Passed | Rejected, customer not on customer table (SQL code -530) | Not attempted | Return code '70'; error logged; no type-specific details stored | ADPLM-BR-047 |
| '01AEND', '01AHOU', '01AMOT' or '01ACOM' | Passed | Failed for any other reason | Not attempted | Return code '90'; error logged; no type-specific details stored | ADPLM-BR-049 |
| '01AEND' | Passed | Succeeded | Failed | Return code '90'; error logged; abnormal end 'LGSQ' backs out the policy row |  |
| '01ACOM' | Passed | Succeeded | Failed | Return code '90'; error logged; abnormal end 'LGSQ' backs out the policy row |  |
| '01AEND', '01AHOU', '01AMOT' or '01ACOM' | Passed | Succeeded | Succeeded | Return code '00'; policy number and last-changed timestamp returned; request passed to LGAPVS01 | ADPLM-BR-046 |
| '01AHOU' | Passed | Succeeded | Failed | **Gap:** No rule says what happens when the house details cannot be stored after the policy row is added (return code, logging, back-out). | |
| '01AMOT' | Passed | Succeeded | Failed | **Gap:** No rule says what happens when the motor details cannot be stored after the policy row is added (return code, logging, back-out). | |


## Design notes

- ADPLM-BR-038: Each request has a context object whose result code starts at '00' (success). It carries the request's customer number, which is used both for the policy insert and in any error log entry.
- ADPLM-BR-051: Once the database registration finishes without stopping early, pass the full request, including the assigned policy number, to the policy-file writer (LGAPVS01, capability 11) as the next step. A direct service call is enough. The full request is 32,500 bytes in the legacy system, but the new interface needs only the populated request fields.

## Open questions

- SME-030: When an add-policy request arrives with no request data at all, what should happen: should it be rejected with a specific code, or should processing just stop? (Policy administration business analyst) On ADPLM-BR-040, ADPLM-BR-042, ADPLM-BR-039.
- SME-031: When saving a new policy fails for a reason other than the customer not existing, what outcome code should the caller get back? (Policy administration business analyst) On ADPLM-BR-044, ADPLM-BR-045, ADPLM-BR-047, ADPLM-BR-049, ADPLM-BR-043, ADPLM-BR-046, ADPLM-BR-050.
- SME-032: What format (data type and length) should the policy number have when the policy data store assigns it? (Data architecture team) On ADPLM-BR-044, ADPLM-BR-045, ADPLM-BR-047, ADPLM-BR-049, ADPLM-BR-043, ADPLM-BR-046, ADPLM-BR-050.
- SME-034: When adding a policy is rejected for a bad reference, does that always mean the customer does not exist, or can it also mean the broker is unknown? Should an unknown broker be reported differently? (Data architect / DBA) On ADPLM-BR-047.
- SME-037: After a policy is added, it is passed on to a follow-on step (LGAPVS01). What does that step do for the business, for example keeping a file copy or an audit record? Should the whole add fail if that step fails? (Policy administration SME) On ADPLM-BR-051.
- SME-038: The name of the person whose life is assured on an endowment policy is supplied as 31 characters but stored in 30. Is it intended that the 31st character is dropped? (Policy administration business analyst) On ADPLM-BR-051.
- SME-039: New policies are recorded in two places, the policy database and a separate policy file. Does the new system need to keep both, and if so, which one is the official record? (Data architecture team) On ADPLM-BR-051.
- DEF-005: Is this intended? LGAPOL01, the only caller in the source, always links with a length of 32500, so this check can never fail on that path; it guards only callers that pass the true length. (Subject-matter expert) On ADPLM-BR-040.
- DEF-006: Is this intended? The length check can never fail when the request comes through LGAPOL01, because LGAPOL01 always links to LGAPDB01 with a fixed length of 32500, so a short request is not caught here. The second 'request not recognised' branch at detail routing is also dead code, since unknown request IDs have already been returned with '99'. (Subject-matter expert) On ADPLM-BR-042, ADPLM-BR-039, ADPLM-BR-045.
- DEF-012: Is this intended? After a successful insert, neither the IDENTITY_VAL_LOCAL() call nor the read-back of LASTCHANGED is checked for an SQL error, so a failed read-back would still return '00' with a blank or stale timestamp. (Subject-matter expert) On ADPLM-BR-043, ADPLM-BR-046, ADPLM-BR-050.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (21 in all).