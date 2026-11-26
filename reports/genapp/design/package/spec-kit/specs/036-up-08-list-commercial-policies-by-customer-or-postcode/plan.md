# Implementation plan: List commercial policies by customer or postcode (UP-C08)

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

#### Commercial policy list outcomes

| Request type | List started | Matching policies read | List closed | Response returned | Rule |
|---|---|---|---|---|---|
| '03ICOM' or '05ICOM' | No | - | - | Return code '89', error written to the error queue, request ended | UP-BR-070 |
| '03ICOM' or '05ICOM' | Yes | None | Yes | Return code '00' with no policy details | UP-BR-072 |
| '03ICOM' | Yes | 1 to 20 | Yes | Only the last row read is in the response | UP-BR-067 |
| '03ICOM' | Yes | More than 20 | Yes | Reading stops after the 21st row; 21st row in the response, return code '00' | UP-BR-068 |
| '05ICOM' | Yes | Any number (no limit) | Yes | Only the last row read is in the response | UP-BR-069 |
| '03ICOM' or '05ICOM' | Yes | Any | No | Return code '88', error written to the error queue, request ended | UP-BR-071 |
| '03ICOM' or '05ICOM' | Yes | Read fails part-way | Any | **Gap:** No rule says what happens if reading a row fails after the list has started. | |

