# Implementation plan: Delete a policy (ADPLM-C14)

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

- LGCMAREA (working storage of LGDPDB01, LGDPOL01): see data-contracts.md.

## Design notes

- ADPLM-BR-084: Set the response code to '00' as soon as a request with data is accepted. Only a later validation failure or the outcome of the database delete may replace it.
- ADPLM-BR-087: Compare the request identifier case-insensitively, for example by upper-casing it before matching against '01DEND', '01DMOT', '01DHOU' and '01DCOM', so that '01dend' behaves like '01DEND'.
- ADPLM-BR-093: Define the endowment, house, motor and commercial detail tables with a foreign key to the policy table and ON DELETE CASCADE. Deleting the policy row then removes its details in the same transaction, with no separate delete statements.

## Decision tables

#### Delete-policy request screening

| Request data received | Request length | Upper-cased request identifier | Delete-policy action | Rule |
|---|---|---|---|---|
| No | - | - | Log 'NO COMMAREA RECEIVED' and abend with code 'LGCA' | ADPLM-BR-083 |
| Yes | Shorter than 28 bytes | - | Set return code '98' and return without deleting anything | ADPLM-BR-086 |
| Yes | At least 28 bytes | '01DEND', '01DMOT', '01DHOU' or '01DCOM' | Pass the 32,500-byte request to LGDPDB01 to delete the policy and return its return code | ADPLM-BR-088 |
| Yes | At least 28 bytes | Any other value | Set return code '99' and delete nothing | ADPLM-BR-090 |

#### Policy row delete outcome

| Request type recognised | Database delete result | Policy deletion action | Rule |
|---|---|---|---|
| No | - | Set return code '99' and delete nothing | ADPLM-BR-089 |
| Yes | Complete success | Type-specific details removed in cascade; pass request to LGDPVS01 to remove the policy-file record | ADPLM-BR-094 |
| Yes | Anything other than complete success (including no matching policy) | Set return code '90', log the error and return without removing the policy-file record | ADPLM-BR-095 |

