# Requirements: Log policy add errors (ADPLM-C09)

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
