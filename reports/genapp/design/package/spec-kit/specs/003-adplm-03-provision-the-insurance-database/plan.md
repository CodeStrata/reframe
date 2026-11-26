# Implementation plan: Provision the insurance database (ADPLM-C03)

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

None found in the source.

## Design notes

- ADPLM-BR-012: A versioned schema migration creates the customer table (name, date of birth, address, phones, email) and the customer security table (password value, state, password-change count), each with a unique key on customer number. The migration runner stops at the first failed step (severity above 4), so later migrations do not run on a broken schema.
- ADPLM-BR-013: A migration creates the policy table (customer, issue and expiry dates, policy type, last-changed timestamp, broker id, broker reference, payment, commission). It has a unique key on policy number and a non-unique index on customer number to support lookups of a customer's policies. It runs only after the earlier migrations succeed.
- ADPLM-BR-014: A migration creates the endowment details table, keyed on policy number. A foreign key to the policy table cascades deletes, so deleting a policy removes its endowment details. It runs only after the earlier migrations succeed.
- ADPLM-BR-015: A migration creates the house details table, one row per policy: property type, bedrooms, value, house name, house number and postcode. It has a unique key on policy number and a foreign key to the policy. It runs only after the earlier migrations succeed.
- ADPLM-BR-016: A migration creates the motor details table, one row per policy: make, model, value, registration, colour, engine size, year of manufacture, premium and accidents. It has a unique key on policy number and a foreign key to the policy. It runs only after the earlier migrations succeed.
- ADPLM-BR-017: A migration creates the commercial property table, one row per policy: request, start and renewal dates, address, postcode, location, customer, property type, a peril indicator and premium for each of fire, crime, flood and weather, status and rejection reason. It has a unique key on policy number and a foreign key to the policy. It runs only after the earlier migrations succeed.
- ADPLM-BR-018: A migration creates the claim table (claim date, amount paid, claim value, cause, observations) with a unique key on claim number and a foreign key to its policy. It runs only after the earlier migrations succeed.

## Decision tables

None.
