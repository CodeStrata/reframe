# Implementation plan: Provision the insurance database (ADPLM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C03-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ADPLM-REQ-F-019, ADPLM-REQ-F-020, ADPLM-REQ-F-021_
  - _Rules: ADPLM-BR-019, ADPLM-BR-020, ADPLM-BR-021_
- [ ] 2. ADPLM-C03-T2 [api] Build the scheduled job
  - ADPLM-BR-012: A versioned schema migration creates the customer table (name, date of birth, address, phones, email) and the customer security table (password value, state, password-change count), each with a unique key on customer number. The migration runner stops at the first failed step (severity above 4), so later migrations do not run on a broken schema.
  - ADPLM-BR-013: A migration creates the policy table (customer, issue and expiry dates, policy type, last-changed timestamp, broker id, broker reference, payment, commission). It has a unique key on policy number and a non-unique index on customer number to support lookups of a customer's policies. It runs only after the earlier migrations succeed.
  - ADPLM-BR-014: A migration creates the endowment details table, keyed on policy number. A foreign key to the policy table cascades deletes, so deleting a policy removes its endowment details. It runs only after the earlier migrations succeed.
  - ADPLM-BR-015: A migration creates the house details table, one row per policy: property type, bedrooms, value, house name, house number and postcode. It has a unique key on policy number and a foreign key to the policy. It runs only after the earlier migrations succeed.
  - ADPLM-BR-016: A migration creates the motor details table, one row per policy: make, model, value, registration, colour, engine size, year of manufacture, premium and accidents. It has a unique key on policy number and a foreign key to the policy. It runs only after the earlier migrations succeed.
  - ADPLM-BR-017: A migration creates the commercial property table, one row per policy: request, start and renewal dates, address, postcode, location, customer, property type, a peril indicator and premium for each of fire, crime, flood and weather, status and rejection reason. It has a unique key on policy number and a foreign key to the policy. It runs only after the earlier migrations succeed.
  - ADPLM-BR-018: A migration creates the claim table (claim date, amount paid, claim value, cause, observations) with a unique key on claim number and a foreign key to its policy. It runs only after the earlier migrations succeed.
  - _Requirements: ADPLM-REQ-F-012, ADPLM-REQ-F-013, ADPLM-REQ-F-014, ADPLM-REQ-F-015, ADPLM-REQ-F-016, ADPLM-REQ-F-017, ADPLM-REQ-F-018_
  - _Rules: ADPLM-BR-012, ADPLM-BR-013, ADPLM-BR-014, ADPLM-BR-015, ADPLM-BR-016, ADPLM-BR-017, ADPLM-BR-018_
  - _After: ADPLM-C03-T1_
- [ ] 3. ADPLM-C03-T3 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-012, ADPLM-REQ-F-013, ADPLM-REQ-F-014, ADPLM-REQ-F-015, ADPLM-REQ-F-016, ADPLM-REQ-F-017, ADPLM-REQ-F-018, ADPLM-REQ-F-019, ADPLM-REQ-F-020, ADPLM-REQ-F-021_
  - _Criteria: ADPLM-C03-AC-01, ADPLM-C03-AC-02, ADPLM-C03-AC-03, ADPLM-C03-AC-04, ADPLM-C03-AC-05, ADPLM-C03-AC-06, ADPLM-C03-AC-07, ADPLM-C03-AC-08, ADPLM-C03-AC-09, ADPLM-C03-AC-10, ADPLM-C03-AC-11, ADPLM-C03-AC-12, ADPLM-C03-AC-13_
  - _After: ADPLM-C03-T1, ADPLM-C03-T2_
- [ ] 4. ADPLM-C03-T4 [compliance] Review the handling of money, personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-012, ADPLM-REQ-F-013, ADPLM-REQ-F-014, ADPLM-REQ-F-015, ADPLM-REQ-F-016, ADPLM-REQ-F-017, ADPLM-REQ-F-018, ADPLM-REQ-F-019, ADPLM-REQ-F-020, ADPLM-REQ-F-021_
  - _After: ADPLM-C03-T1, ADPLM-C03-T2_
