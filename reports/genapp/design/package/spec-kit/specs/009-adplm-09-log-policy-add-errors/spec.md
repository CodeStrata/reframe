# Feature specification: Log policy add errors

**Feature:** ADPLM-C09 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C09)

As a support analyst, I want every policy add error recorded with its context, so that failed requests can be investigated.

Records every error raised while adding a policy, with enough context (when, which program, which customer and policy, the database error code and the start of the request) for support analysts to investigate. A failed add must never go unlogged.

**Acceptance scenarios:**

1. **Given** An add-policy request for customer 0000000099, which is not on the customer table, so the policy insert fails with SQLCODE -530, **when** The policy add service logs the error, **then** A message is written through the error queue program (LGSTSQ) holding the current date, the current time, program 'LGAPDB01', customer number 0000000099, the policy number, the failing request and SQLCODE -530, followed by the first 90 bytes of the request data (ADPLM-C09-AC-01)
2. **Given** A failing add-policy request whose request data is shorter than 90 bytes, **when** The policy add service logs the error, **then** The logged request data contains the whole request and nothing beyond it, because no more than the first 90 bytes are ever logged (ADPLM-C09-AC-02)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-055** (side effect): When the policy add service logs an error, the system shall write a message holding date, time, program 'LGAPDB01', customer number, policy number, the failing request and the SQLCODE, plus up to the first 90 bytes of the request data, through the error queue program (LGSTSQ). Rules: ADPLM-BR-060.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-060 | Insert policy and return assigned identifiers | side effect | WHEN the policy add service logs an error, THE policy add service SHALL write a message holding date, time, program 'LGAPDB01', customer number, policy number, the failing request and the SQLCODE, plus up to the first 90 bytes of the request data, through the error queue program (LGSTSQ). | high | base/src/lgapdb01.cbl:184-207, base/src/lgapdb01.cbl:219, base/src/lgapdb01.cbl:261-321, base/src/lgapdb01.cbl:562-594 |

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- SME-031: When saving a new policy fails for a reason other than the customer not existing, what outcome code should the caller get back? (Policy administration business analyst) On ADPLM-BR-060.
- SME-032: What format (data type and length) should the policy number have when the policy data store assigns it? (Data architecture team) On ADPLM-BR-060.
- DEF-012: Is this intended? After a successful insert, neither the IDENTITY_VAL_LOCAL() call nor the read-back of LASTCHANGED is checked for an SQL error, so a failed read-back would still return '00' with a blank or stale timestamp. (Subject-matter expert) On ADPLM-BR-060.

### Decision table gaps

None.
