# Implementation plan: Look up a single commercial policy (UP-C07)

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

- UP-BR-062: In a '01ICOM' or '02ICOM' reply, the marker 'FINAL' goes in the first 5 positions of the free space after the rejection reason, so callers can find where the data ends. Keep it in the reply layout while existing callers depend on it.

## Decision tables

#### Commercial policy single inquiry outcomes

| Request type | Policy lookup result | Caller's area at least 33 + 1174 bytes | Response returned | Rule |
|---|---|---|---|---|
| '01ICOM' | Found | Not stated | Policy data returned with 'FINAL' after the rejection reason | UP-BR-062 |
| '02ICOM' | Found | No | Return code '98', no policy details | UP-BR-064 |
| '02ICOM' | Found | Yes | Owning customer number, common and commercial details returned, ended with 'FINAL' | UP-BR-065 |
| '02ICOM' | Failed for a reason other than not found | Any | Return code '90' and ' SELECT Commercial ' error logged | UP-BR-066 |
| '02ICOM' | Not found | Any | **Gap:** No rule says what return code or response is given when the policy number does not exist. | |
| '01ICOM' | Not found | Any | **Gap:** No rule covers a customer-and-policy inquiry that finds no matching policy. | |
| '01ICOM' | Failed for a reason other than not found | Any | **Gap:** No rule covers a database failure on the customer-and-policy inquiry. | |
| '01ICOM' | Found | No | **Gap:** No rule says whether the caller's area size is checked for the customer-and-policy inquiry. | |

