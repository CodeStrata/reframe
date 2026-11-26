# Implementation plan: Record a new policy in the policy file (ADPLM-C11)

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

- LGCMAREA (working storage of LGAPVS01): see data-contracts.md.

## Design notes

- ADPLM-BR-067: Build a composite key: the policy type letter, the customer number zero-padded to 10 digits, and the policy number zero-padded to 10 digits, 21 characters in all. Records are then found by keyed lookup on the full key, or by prefix (type, or type plus customer) for range browsing.
- ADPLM-BR-068: Map the endowment summary into fixed-width fields: with-profits, equities and managed-fund indicators of 1 character each, fund name of 10 characters and life assured of 30 characters. Values are padded or truncated to those widths.
- ADPLM-BR-069: Map the house summary into fixed-width fields: property type of 15 characters, bedrooms of 3 digits, value of 8 digits, postcode of 8 characters, and only the first 9 characters of the house name (truncated on purpose).
- ADPLM-BR-070: Map the motor summary into fixed-width fields: make of 15 characters, model of 15 characters, value of 6 digits and registration of 7 characters.
- ADPLM-BR-071: Map the commercial summary into fixed-width fields: postcode of 8 characters, status of 4 digits, and the first 31 characters of the customer name.
- ADPLM-BR-072: Insert the 64-character summary record into the policy key-value or index store under the 21-character key, using insert-only semantics, so an existing key is never overwritten and the write fails instead.

## Decision tables

#### Policy-file details stored by policy type

| Policy type | Details stored in the policy-file record | Rule |
|---|---|---|
| E (endowment) | With-profits, equities and managed-fund indicators, fund name (10), life assured name (30) | ADPLM-BR-068 |
| H (house) | Property type (15), bedrooms (3 digits), insured value (8 digits), postcode (8), first 9 characters of house name | ADPLM-BR-069 |
| M (motor) | Vehicle make (15), model (15), insured value (6 digits), registration number (7) | ADPLM-BR-070 |
| C (commercial) | Premises postcode (8), status code (4 digits), first 31 characters of customer name | ADPLM-BR-071 |
| Any other policy type letter | **Gap:** No rule says what details are stored, or whether the record is written, when the 4th character of the request code is not 'E', 'H', 'M' or 'C'. | |

