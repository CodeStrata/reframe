# Implementation plan: Accept and check an add-customer request (CRCM-C01)

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

- LGCMAREA (working storage of LGACDB01, LGACUS01): see data-contracts.md.
- LGPOLICY (working storage of LGACDB01, LGACUS01): see data-contracts.md.

## Design notes

- CRCM-BR-001: Start every add-customer response with outcome '00' (success) and a policy count of '00'. Later checks overwrite the outcome only when they fail, so a caller always gets a defined outcome and policy count.
- CRCM-BR-002: The customer-add data step must also default its outcome to '00' before it validates the request, so only a failed check or a failed store sets a non-success code.
- CRCM-BR-008: Once the request passes the presence and minimum-length checks, the intake hands the complete request to the customer-creation service, which assigns the number and stores the customer. It then returns that service's outcome to the caller unchanged. In the new application this is an internal service call with a typed customer payload, not a fixed 32,500-byte buffer.

## Decision tables

#### Add-customer request checks

| Request data received | Request length | Request handling | Rule |
|---|---|---|---|
| No | - | Log ' NO COMMAREA RECEIVED' and end the task abnormally with abend code 'LGCA' | CRCM-BR-003 |
| Yes | Shorter than 90 bytes | Set return code '98' and return without adding the customer | CRCM-BR-007 |
| Yes | At least 90 bytes | Pass the whole request on to insert the new customer | CRCM-BR-008 |

