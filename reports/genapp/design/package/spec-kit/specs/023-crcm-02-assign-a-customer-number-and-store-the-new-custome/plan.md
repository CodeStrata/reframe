# Implementation plan: Assign a customer number and store the new customer (CRCM-C02)

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

- LGCMAREA (working storage of LGACDB01): see data-contracts.md.
- LGPOLICY (working storage of LGACDB01): see data-contracts.md.

## Design notes

- CRCM-BR-010: When the shared customer-number counter supplies the number, insert the customer row under that explicit key, together with the supplied name, date of birth, address, phone numbers and email. The key must be unique, so a clash with an existing customer is rejected rather than overwritten.
- CRCM-BR-012: Both numbering paths, counter-issued or database-generated, must write the same nine fields: first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email. A single insert routine, with the key either supplied or generated, keeps the two paths consistent.

## Decision tables

#### Customer numbering and insert outcome

| Customer-number counter responds normally | New customer row stored | Customer number and return code | Rule |
|---|---|---|---|
| Yes | Yes | Customer stored under the counter value; that number returned to the caller | CRCM-BR-009 |
| No | Yes | Counter marked unavailable ('NO'); database-assigned number read back and returned to the caller | CRCM-BR-011 |
| Yes | No | Return code '90'; return at once without a customer number | CRCM-BR-014 |
| No | No | Return code '90'; return at once without a customer number | CRCM-BR-014 |

