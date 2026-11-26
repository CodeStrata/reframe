# Implementation plan: Add a policy to the policy database (ADPLM-C10)

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

- LGCMAREA (working storage of LGAPDB01, LGAPOL01): see data-contracts.md.
- LGPOLICY (working storage of LGAPDB01): see data-contracts.md.

## Design notes

- ADPLM-BR-062: Every request that has data starts with result code '00'. Validation and persistence steps overwrite it only when they fail.
- ADPLM-BR-064: The entry service checks only that the 28-character header is present, then passes the whole request to the policy registration service (LGAPDB01). That service does the product-specific length check and the inserts inside a single transaction, and the entry service returns its result to the caller.

## Decision tables

#### Add-policy request screening

| Request data received | Request length | Add-policy service action | Rule |
|---|---|---|---|
| No | - | Log ' NO COMMAREA RECEIVED' and abend with code 'LGCA' | ADPLM-BR-061 |
| Yes | Shorter than 28 bytes | Set return code '98' and return without adding the policy | ADPLM-BR-063 |
| Yes | At least 28 bytes | Pass the whole 32,500-byte request to LGAPDB01 to insert the policy, then return | ADPLM-BR-064 |

