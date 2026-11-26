# Design: Provision the insurance database (ADPLM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Creates the insurance database: customers and their security details, policies, the endowment, house, motor and commercial product details, and claims. It also sets up automatic numbering of customers, policies and claims starting at 1000001. It is for the administrators who set up an environment. It must create the tables only when the earlier set-up steps ran cleanly, and it must never hand out a duplicate customer, policy or claim number.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-012 | Create the claim table | design note | WHEN no earlier step of the setup job ended with a return code above 4, THE Insurance Database Provisioning SHALL create the customer table (customer) holding name, date of birth, address, phones and email, and the customer security table (customer_secure) holding password value, state and password-change count, each with a unique index on customer number. | medium | base/cntl/db2cre.jcl:99, base/cntl/db2cre.jcl:110-144 |
| ADPLM-BR-013 | Create the claim table | design note | WHEN no earlier step of the setup job ended with a return code above 4, THE Insurance Database Provisioning SHALL create the policy table (policy) holding customer, issue and expiry dates, policy type, last-changed timestamp, broker id, broker reference, payment and commission, with a unique index on policy number and a non-unique index on customer number. | medium | base/cntl/db2cre.jcl:150, base/cntl/db2cre.jcl:161-185, base/cntl/db2cre.jcl:214-216, base/cntl/db2cre.jcl:250 |
| ADPLM-BR-014 | Create the claim table | design note | WHEN no earlier step of the database set-up job has ended with a return code above 4, THE Insurance Database Provisioning SHALL create the endowment details table, keyed on the policy number, linked to its parent policy so that deleting the policy deletes its endowment details, with a unique index on the policy number. | medium | base/cntl/db2cre.jcl:189-192, base/cntl/db2cre.jcl:202-222 |
| ADPLM-BR-015 | Create the claim table | design note | WHEN no earlier step of the setup job ended with a return code above 4, THE Insurance Database Provisioning SHALL create the house details table (house), one row per policy (policyNumber), holding property type, bedrooms, value, house name, house number and postcode, with a unique index on the policy number. | medium | base/cntl/db2cre.jcl:229, base/cntl/db2cre.jcl:240-256 |
| ADPLM-BR-016 | Create the claim table | design note | WHEN no earlier step of the setup job ended with a return code above 4, THE Insurance Database Provisioning SHALL create the motor details table (motor), one row per policy, holding make, model, value, registration, colour, engine size, year of manufacture, premium and accidents, with a unique index on the policy number. | medium | base/cntl/db2cre.jcl:264, base/cntl/db2cre.jcl:275-294 |
| ADPLM-BR-017 | Create the claim table | design note | WHEN no earlier step of the setup job ended with a return code above 4, THE Insurance Database Provisioning SHALL create the commercial property table (Commercial), one row per policy, holding request, start and renewal dates, address, postcode, location, customer, property type, a peril indicator and premium for each of fire, crime, flood and weather, a status and a rejection reason, with a unique index on the policy number. | medium | base/cntl/db2cre.jcl:302, base/cntl/db2cre.jcl:313-342 |
| ADPLM-BR-018 | Create the claim table | design note | WHEN no earlier step of the setup job ended with a return code above 4, THE Insurance Database Provisioning SHALL create the claim table (Claim) linked to a policy (PolicyNumber), holding claim date, amount paid, claim value, cause and observations, with a unique index on the claim number. | medium | base/cntl/db2cre.jcl:350, base/cntl/db2cre.jcl:361-379 |
| ADPLM-BR-019 | Create the claim table | business rule | THE Insurance Database Provisioning SHALL number customers automatically (customerNumber) starting at 1000001 and increasing by 1, unless a number is supplied. | medium | base/cntl/db2cre.jcl:99, base/cntl/db2cre.jcl:110-144 |
| ADPLM-BR-020 | Create the claim table | business rule | THE Insurance Database Provisioning SHALL number policies automatically (policyNumber) starting at 1000001 and increasing by 1, unless a number is supplied. | medium | base/cntl/db2cre.jcl:150, base/cntl/db2cre.jcl:161-185, base/cntl/db2cre.jcl:214-216, base/cntl/db2cre.jcl:250 |
| ADPLM-BR-021 | Create the claim table | business rule | THE Insurance Database Provisioning SHALL number claims automatically (ClaimNumber) starting at 1000001 and increasing by 1, unless a number is supplied. | medium | base/cntl/db2cre.jcl:350, base/cntl/db2cre.jcl:361-379 |

### Worked examples

- ADPLM-BR-012: highest return code of earlier steps = 4 → Both tables are created with indexes iCustomer and iCustomer_secure
- ADPLM-BR-012: highest return code of earlier steps = 12 → The step is skipped and neither table is created
- ADPLM-BR-013: highest return code of earlier steps = 0 → The policy table is created with indexes iPolicy (unique) and iPolicy2 (customer number)
- ADPLM-BR-014: highest return code of earlier steps = 0 → The endowment table and its unique index on policy number are created; deleting policy 5 later also deletes its endowment row.
- ADPLM-BR-014: highest return code of earlier steps = 8 → The step is bypassed and the endowment table is not created.
- ADPLM-BR-015: highest return code of earlier steps = 0 → The house table is created with its unique policy-number index
- ADPLM-BR-016: highest return code of earlier steps = 0 → The motor table is created with unique index iMotor
- ADPLM-BR-017: highest return code of earlier steps = 0 → The Commercial table is created with fire, crime, flood and weather peril and premium columns
- ADPLM-BR-018: highest return code of earlier steps = 4 → The claim table and its unique claim-number index are created
- ADPLM-BR-018: highest return code of earlier steps = 8 → The step is skipped and the claim table is not created
- ADPLM-BR-019: customers already created by the system = none → The first new customer gets number 1000001
- ADPLM-BR-020: policies already created by the system = none → The first new policy gets number 1000001
- ADPLM-BR-021: claims already created by the system = none → The first new claim gets number 1000001, the next 1000002

## Decision tables

None.

## Design notes

- ADPLM-BR-012: A versioned schema migration creates the customer table (name, date of birth, address, phones, email) and the customer security table (password value, state, password-change count), each with a unique key on customer number. The migration runner stops at the first failed step (severity above 4), so later migrations do not run on a broken schema.
- ADPLM-BR-013: A migration creates the policy table (customer, issue and expiry dates, policy type, last-changed timestamp, broker id, broker reference, payment, commission). It has a unique key on policy number and a non-unique index on customer number to support lookups of a customer's policies. It runs only after the earlier migrations succeed.
- ADPLM-BR-014: A migration creates the endowment details table, keyed on policy number. A foreign key to the policy table cascades deletes, so deleting a policy removes its endowment details. It runs only after the earlier migrations succeed.
- ADPLM-BR-015: A migration creates the house details table, one row per policy: property type, bedrooms, value, house name, house number and postcode. It has a unique key on policy number and a foreign key to the policy. It runs only after the earlier migrations succeed.
- ADPLM-BR-016: A migration creates the motor details table, one row per policy: make, model, value, registration, colour, engine size, year of manufacture, premium and accidents. It has a unique key on policy number and a foreign key to the policy. It runs only after the earlier migrations succeed.
- ADPLM-BR-017: A migration creates the commercial property table, one row per policy: request, start and renewal dates, address, postcode, location, customer, property type, a peril indicator and premium for each of fire, crime, flood and weather, status and rejection reason. It has a unique key on policy number and a foreign key to the policy. It runs only after the earlier migrations succeed.
- ADPLM-BR-018: A migration creates the claim table (claim date, amount paid, claim value, cause, observations) with a unique key on claim number and a foreign key to its policy. It runs only after the earlier migrations succeed.

## Open questions

- SME-009: The claim table has no standard name in the list of data entities. What should the new system call it? (Data architecture) On ADPLM-BR-021, ADPLM-BR-015, ADPLM-BR-017, ADPLM-BR-020, ADPLM-BR-016, ADPLM-BR-019, ADPLM-BR-014.
- SME-010: Customer, policy and claim numbers are generated automatically. What data type and length must these numbers have? (Data architecture) On ADPLM-BR-021, ADPLM-BR-015, ADPLM-BR-017, ADPLM-BR-020, ADPLM-BR-016, ADPLM-BR-019, ADPLM-BR-014.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).