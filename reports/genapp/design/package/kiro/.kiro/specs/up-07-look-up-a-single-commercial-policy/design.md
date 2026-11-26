# Design: Look up a single commercial policy (UP-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Returns one commercial policy to policy administrators, found by customer and policy number or by policy number alone. It shows the policy's peril values, premiums, status and owning customer exactly as stored, with no recalculation. When the policy is found by policy number alone, the reply must name the customer who owns it, not the one the caller supplied, and a reply area smaller than 33 + 1174 bytes must get code '98'.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGIPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGIPDB01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-061 | Return commercial policy by customer and policy | formatting | WHEN a commercial policy is returned, THE Commercial Policy Inquiry SHALL report the peril values, premiums and status exactly as stored, converted to plain numbers, and the rejection reason as stored text, with no recalculation. | high | base/src/lgipdb01.cbl:627-708, base/src/lgipdb01.cbl:808-813, base/src/lgpolicy.cpy:83-99, base/src/lgcmarea.cpy:78-94 |
| UP-BR-062 | Return commercial policy by customer and policy | design note | WHEN commercial policy data has been returned for a customer-and-policy ('01ICOM') or policy-number ('02ICOM') inquiry, THE Commercial Policy Inquiry SHALL write 'FINAL' in the first 5 positions of the free space after the rejection reason. | high | base/src/lgipdb01.cbl:627-708, base/src/lgipdb01.cbl:808-813, base/src/lgpolicy.cpy:83-99, base/src/lgcmarea.cpy:78-94 |
| UP-BR-063 | Retrieve commercial policy by policy only | business rule | WHEN a commercial policy inquiry by policy number (request '02ICOM') is made, THE Policy Inquiry SHALL look up the commercial policy by policy number alone, without checking that it belongs to the customer number supplied. | high | base/src/lgipdb01.cbl:295-297, base/src/lgipdb01.cbl:726-829, base/src/lgipdb01.cbl:993-1030, base/src/lgpolicy.cpy:27 |
| UP-BR-064 | Return commercial policy by policy number | error handling | WHEN a commercial policy is found by policy number, THE Policy Inquiry SHALL work out the space needed as 33 plus 1174 bytes, and if the caller's area is smaller SHALL set return code '98' and return without policy details. | high | base/src/lgipdb01.cbl:295-297, base/src/lgipdb01.cbl:726-829, base/src/lgipdb01.cbl:993-1030, base/src/lgpolicy.cpy:27 |
| UP-BR-065 | Return commercial policy by policy number | business rule | WHEN a commercial policy is found by policy number and the caller's area is large enough, THE Policy Inquiry SHALL return the owning customer number in place of the one supplied, with the common policy and commercial details, and mark the end of the data with 'FINAL'. | high | base/src/lgipdb01.cbl:295-297, base/src/lgipdb01.cbl:726-829, base/src/lgipdb01.cbl:993-1030, base/src/lgpolicy.cpy:27 |
| UP-BR-066 | Retrieve commercial policy by policy only | error handling | WHEN the commercial policy lookup by policy number fails for any reason other than the policy not being found, THE Policy Inquiry SHALL set return code '90' and log an error message labelled ' SELECT Commercial ' with the date, time, customer number, policy number and database code, plus up to the first 90 bytes of the request. | high | base/src/lgipdb01.cbl:295-297, base/src/lgipdb01.cbl:726-829, base/src/lgipdb01.cbl:993-1030, base/src/lgpolicy.cpy:27 |

### Worked examples

- UP-BR-062: request = '01ICOM'; policy found = yes → 'FINAL' follows the rejection reason in the reply area.
- UP-BR-063: Request = '02ICOM'; Policy number = 0000000012 (owned by customer 0000000003); Customer number = blank or any other customer → Policy 0000000012 is found.
- UP-BR-064: Caller's area length = 1000 → Return code '98'; no policy data is returned.
- UP-BR-064: Caller's area length = 32500 → The policy is returned.
- UP-BR-066: Database lookup result = unexpected error (for example SQLCODE -911) → Return code '90'; a ' SELECT Commercial ' error message is written to the error queue.
- UP-BR-066: Database lookup result = no row (SQLCODE 100) → Return code '01'; no error message is logged.

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


## Design notes

- UP-BR-062: In a '01ICOM' or '02ICOM' reply, the marker 'FINAL' goes in the first 5 positions of the free space after the rejection reason, so callers can find where the data ends. Keep it in the reply layout while existing callers depend on it.

## Open questions

- SME-059: When commercial policies are listed by customer (03ICOM) or by postcode (05ICOM), should the caller get every matching policy or only one? Should the list by customer stop at 20 policies (today a 21st can slip through), and should the postcode search also be limited? (Commercial underwriting SME) On UP-BR-062, UP-BR-065, UP-BR-066.
- SME-062: What are the valid status values for a commercial policy and what does each mean (for example quoted, accepted, rejected)? Which part of the system sets them? (Commercial underwriting SME) On UP-BR-061.
- SME-063: Anyone with a policy number can look up a commercial policy (02ICOM) without any check that the policy belongs to their customer. Is this meant to be a back-office lookup? Should the new system check customer ownership or user role? (Security / compliance officer) On UP-BR-065.
- DEF-017: Confirm this is deliberate: The '98' reply-too-small check can never trigger: the only caller, LGIPOL01, always passes a 32500-byte area, far more than the 1207 bytes needed. (Subject-matter expert) On UP-BR-061, UP-BR-062.
- DEF-026: Confirm this is deliberate: An inquiry by policy number alone returns any commercial policy, and the owning customer's number, to the caller, without checking that the caller's customer owns the policy. The header comment and the calling screen (which uses '02ICOM' only when no customer number is given) show this is intended as a lookup by policy number. (Subject-matter expert) On UP-BR-065, UP-BR-066.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).