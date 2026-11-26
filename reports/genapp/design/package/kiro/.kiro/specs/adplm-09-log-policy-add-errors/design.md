# Design: Log policy add errors (ADPLM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Records every error raised while adding a policy, with enough context (when, which program, which customer and policy, the database error code and the start of the request) for support analysts to investigate. A failed add must never go unlogged.

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