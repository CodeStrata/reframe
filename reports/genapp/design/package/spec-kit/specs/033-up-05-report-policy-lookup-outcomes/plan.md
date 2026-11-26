# Implementation plan: Report policy lookup outcomes (UP-C05)

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

- LGCMAREA (working storage of LGIPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGIPDB01): see data-contracts.md.

## Design notes

None.

## Decision tables

#### Policy lookup outcome

| Policy type | Lookup result | Caller's area large enough | Return code and logging | Rule |
|---|---|---|---|---|
| Endowment, house, motor or commercial (01 requests) | No matching policy | - | Return code '01', no error log | UP-BR-045 |
| Commercial by policy number alone (02ICOM) | No matching policy | - | Return code '01' | UP-BR-046 |
| Endowment, house, motor or commercial (01 requests) | Other failure | - | Return code '90', error log via LGSTSQ | UP-BR-047 |
| Commercial by policy number alone (02ICOM) | Other failure | - | Return code '90', error message to error log queue | UP-BR-048 |
| Endowment | Policy found | No | Return code '98', no policy details | UP-BR-050 |
| House, motor or commercial | Policy found | No | **Gap:** Reply sizes are worked out for house, motor and commercial (R46), but no rule says what happens when the caller's area is too small for them; confirm whether return code '98' applies. | |
| Commercial list by customer (03ICOM) or by postcode (05ICOM) | No matching policy or other failure | - | **Gap:** No rule gives the return code or logging when a 03ICOM or 05ICOM lookup finds nothing or fails. | |

