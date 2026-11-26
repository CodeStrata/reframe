# Implementation plan: Update a policy in the database with a timestamp check (ADPLM-C20)

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

- LGCMAREA (working storage of LGUPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGUPDB01): see data-contracts.md.

## Design notes

- ADPLM-BR-137: Start every update with outcome '00'. Find the policy by a keyed lookup on customer number plus policy number, and read it inside the same transaction as the update.
- ADPLM-BR-151: After the update, read the new last-changed timestamp, keyed by policy number, or take it from the update's RETURNING clause, and put it in the response so that the caller can make its next change.

## Decision tables

#### Policy database update outcome

| Policy row read | Timestamp matches caller's | Product-detail update result | Database changes, outcome returned and whether the policy file is updated | Rule |
|---|---|---|---|---|
| found | yes | succeeded | Product details and common policy details updated with new last-changed timestamp; request passed to policy file update | ADPLM-BR-138 |
| found | yes | no record for policy number | Outcome '01'; cursor closed, reset to '00'; no common policy or policy file update | ADPLM-BR-149 |
| found | yes | failed for another reason | Outcome '90' and error logged; cursor closed, reset to '00'; no common policy or policy file update | ADPLM-BR-148 |
| found | no | not attempted | No policy tables changed; outcome '02', reset to '00' by successful close; request still passed to policy file update | ADPLM-BR-154 |
| not found | not applicable | not attempted | No database update; outcome '01', reset to '00' by successful close; request still passed to policy file update | ADPLM-BR-155 |
| failed (other than not found) | not applicable | not attempted | Outcome '90' and SQL code logged, reset to '00' by successful close; request still passed to policy file update | ADPLM-BR-156 |
| found | yes | succeeded | **Gap:** No rule says what happens if the update of the common policy details itself (issue date, expiry date, broker ID, broker's reference) fails; only failure of the timestamp read-back is covered (R17). | |
| found | no | not attempted | **Gap:** A timestamp mismatch, missing policy or failed read still rewrites the policy file with the request details (R14) and the caller can receive '00'; confirm whether this is intended business behaviour. | |

