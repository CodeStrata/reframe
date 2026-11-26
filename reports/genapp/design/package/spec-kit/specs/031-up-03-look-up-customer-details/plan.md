# Implementation plan: Look up customer details (UP-C03)

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

- LGCMAREA (working storage of LGICDB01, LGICUS01): see data-contracts.md.
- LGPOLICY (working storage of LGICDB01, LGICUS01): see data-contracts.md.

## Design notes

- UP-BR-025: Every customer inquiry reply starts as a success: return code '00' and number of policies '00' are set before any check runs. Later checks overwrite them only on failure.
- UP-BR-029: Once a request passes the length check, the inquiry calls the customer data service (LGICDB01 today) with the whole request (32500 bytes today). It passes that service's reply and return code back to the caller unchanged. In the new application this is a call from the inquiry API to the customer lookup service, keyed by customer number.

## Decision tables

#### Customer inquiry outcome

| Request data received | Request length | Customer lookup result | Return code and logging | Rule |
|---|---|---|---|---|
| No (length zero) | - | - | Log ' NO COMMAREA RECEIVED' and abend 'LGCA' | UP-BR-023 |
| Yes | Under 90 bytes | Not attempted | Return code '98', no lookup | UP-BR-026 |
| Yes | At least 90 bytes | Customer found | Return customer details, return code '00' | UP-BR-030 |
| Yes | At least 90 bytes | Not found (SQLCODE 100) | Return code '01', no error log | UP-BR-031 |
| Yes | At least 90 bytes | Deadlock or timeout (SQLCODE -913) | Return code '01', no error log | UP-BR-032 |
| Yes | At least 90 bytes | Any other database error | Return code '90', error log via LGSTSQ | UP-BR-033 |

