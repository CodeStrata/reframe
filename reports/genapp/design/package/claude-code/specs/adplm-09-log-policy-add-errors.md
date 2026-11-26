# Log policy add errors (ADPLM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Records every error raised while adding a policy, with enough context (when, which program, which customer and policy, the database error code and the start of the request) for support analysts to investigate. A failed add must never go unlogged.

**User story:** As a support analyst, I want every policy add error recorded with its context, so that failed requests can be investigated.

## Requirements

### Requirement 1: ADPLM-REQ-F-055 (side effect)

#### Acceptance criteria

1. When the policy add service logs an error, the system shall write a message holding date, time, program 'LGAPDB01', customer number, policy number, the failing request and the SQLCODE, plus up to the first 90 bytes of the request data, through the error queue program (LGSTSQ). (rules ADPLM-BR-060)
2. GIVEN An add-policy request for customer 0000000099, which is not on the customer table, so the policy insert fails with SQLCODE -530 WHEN The policy add service logs the error THEN A message is written through the error queue program (LGSTSQ) holding the current date, the current time, program 'LGAPDB01', customer number 0000000099, the policy number, the failing request and SQLCODE -530, followed by the first 90 bytes of the request data (ADPLM-C09-AC-01; ADPLM-BR-060)
3. GIVEN A failing add-policy request whose request data is shorter than 90 bytes WHEN The policy add service logs the error THEN The logged request data contains the whole request and nothing beyond it, because no more than the first 90 bytes are ever logged (ADPLM-C09-AC-02; ADPLM-BR-060)

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGAPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGAPDB01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-060 | Insert policy and return assigned identifiers | side effect | WHEN the policy add service logs an error, THE policy add service SHALL write a message holding date, time, program 'LGAPDB01', customer number, policy number, the failing request and the SQLCODE, plus up to the first 90 bytes of the request data, through the error queue program (LGSTSQ). | high | base/src/lgapdb01.cbl:184-207, base/src/lgapdb01.cbl:219, base/src/lgapdb01.cbl:261-321, base/src/lgapdb01.cbl:562-594 |

### Worked examples

None.

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-031: When saving a new policy fails for a reason other than the customer not existing, what outcome code should the caller get back? (Policy administration business analyst) On ADPLM-BR-060.
- SME-032: What format (data type and length) should the policy number have when the policy data store assigns it? (Data architecture team) On ADPLM-BR-060.
- DEF-012: Is this intended? After a successful insert, neither the IDENTITY_VAL_LOCAL() call nor the read-back of LASTCHANGED is checked for an SQL error, so a failed read-back would still return '00' with a blank or stale timestamp. (Subject-matter expert) On ADPLM-BR-060.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).
