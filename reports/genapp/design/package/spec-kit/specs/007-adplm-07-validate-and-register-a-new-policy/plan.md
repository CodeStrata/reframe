# Implementation plan: Validate and register a new policy (ADPLM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as scheduled job.

## Data model

- LGCMAREA (working storage of LGAPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGAPDB01): see data-contracts.md.

## Design notes

- ADPLM-BR-038: Each request has a context object whose result code starts at '00' (success). It carries the request's customer number, which is used both for the policy insert and in any error log entry.
- ADPLM-BR-051: Once the database registration finishes without stopping early, pass the full request, including the assigned policy number, to the policy-file writer (LGAPVS01, capability 11) as the next step. A direct service call is enough. The full request is 32,500 bytes in the legacy system, but the new interface needs only the populated request fields.

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

