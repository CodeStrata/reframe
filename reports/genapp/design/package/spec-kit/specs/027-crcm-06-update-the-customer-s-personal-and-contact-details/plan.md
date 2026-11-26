# Implementation plan: Update the customer's personal and contact details (CRCM-C06)

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

- LGCMAREA (working storage of LGUCDB01): see data-contracts.md.
- LGPOLICY (working storage of LGUCDB01): see data-contracts.md.

## Design notes

- CRCM-BR-030: Default the outcome to '00', then update the customer row found by a keyed lookup on the customer number in the request. The update has to tell 'no matching row' (outcome '01') apart from any other database failure (outcome '90').
- CRCM-BR-034: When the database update step has finished, hand the customer record (225 bytes of customer data) and its return code to the customer-file update step, which brings the customer file into line with the database.

## Decision tables

#### Customer details update outcome

| Customer matching the customer number | Database update | Return code and logging | Rule |
|---|---|---|---|
| Found | Succeeds | Return code '00'; details overwritten with supplied values | CRCM-BR-031 |
| Not found | - | Return code '01'; no error log entry | CRCM-BR-032 |
| Found | Fails | Return code '90'; error ' UPDATE CUST ' logged | CRCM-BR-033 |

