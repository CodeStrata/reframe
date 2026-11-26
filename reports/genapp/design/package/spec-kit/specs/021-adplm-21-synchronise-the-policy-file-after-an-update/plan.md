# Implementation plan: Synchronise the policy file after an update (ADPLM-C21)

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

- LGCMAREA (working storage of LGUPVS01): see data-contracts.md.

## Design notes

- ADPLM-BR-160: Build the policy-file key from the policy type letter (the fourth character of the request ID), the customer number and the policy number. Use typed fields for the request instead of a length the caller passes in.
- ADPLM-BR-161: Same key as the delete and lookup paths: the type letter, then the 10-digit customer number, then the 10-digit policy number. Put the key build in one shared function so that all policy-file operations agree.
- ADPLM-BR-162: Do a keyed read with a row lock (select for update) on the policy-file record, then a full replace of that record in the same transaction.

## Decision tables

#### Policy file details applied by policy type letter

| Policy type letter (fourth character of request ID) | Details copied into the policy-file record | Rule |
|---|---|---|
| 'E' | With-profits, equities and managed-fund indicators, fund name and life assured copied | ADPLM-BR-163 |
| 'H' | Property type, number of bedrooms, value, postcode and house name copied | ADPLM-BR-164 |
| 'M' | Vehicle make, model, value and registration number copied | ADPLM-BR-165 |
| 'C' | Business postcode, business status and business customer copied | ADPLM-BR-166 |
| any other letter | Policy details blanked and record rewritten with blank details | ADPLM-BR-167 |
| 'E', 'H' or 'M' | **Gap:** Fewer fields reach the policy file than the database update changes (for example term and sum assured for endowment, house number for house, colour, CC, year, premium and accidents for motor); confirm whether the policy file should hold only this subset. | |
| any other letter | **Gap:** An unrecognised request type passed on by the update service (return code '99') would reach this step and blank the stored policy details; confirm whether that is intended. | |

