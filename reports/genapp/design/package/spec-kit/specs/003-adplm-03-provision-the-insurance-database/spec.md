# Feature specification: Provision the insurance database

**Feature:** ADPLM-C03 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C03)

As an application administrator, I want the insurance database tables created with automatic numbering when the setup job has run cleanly, so that customers, policies, product details and claims can be stored.

Creates the insurance database: customers and their security details, policies, the endowment, house, motor and commercial product details, and claims. It also sets up automatic numbering of customers, policies and claims starting at 1000001. It is for the administrators who set up an environment. It must create the tables only when the earlier set-up steps ran cleanly, and it must never hand out a duplicate customer, policy or claim number.

**Acceptance scenarios:**

1. **Given** highest return code of earlier steps: 4, **when** no earlier step of the setup job ended with a return code above 4, **then** Both tables are created with indexes iCustomer and iCustomer_secure (ADPLM-C03-AC-01)
2. **Given** highest return code of earlier steps: 12, **when** no earlier step of the setup job ended with a return code above 4, **then** The step is skipped and neither table is created (ADPLM-C03-AC-02)
3. **Given** highest return code of earlier steps: 0, **when** no earlier step of the setup job ended with a return code above 4, **then** The policy table is created with indexes iPolicy (unique) and iPolicy2 (customer number) (ADPLM-C03-AC-03)
4. **Given** highest return code of earlier steps: 0, **when** no earlier step of the database set-up job has ended with a return code above 4, **then** The endowment table and its unique index on policy number are created; deleting policy 5 later also deletes its endowment row. (ADPLM-C03-AC-04)
5. **Given** highest return code of earlier steps: 8, **when** no earlier step of the database set-up job has ended with a return code above 4, **then** The step is bypassed and the endowment table is not created. (ADPLM-C03-AC-05)
6. **Given** highest return code of earlier steps: 0, **when** no earlier step of the setup job ended with a return code above 4, **then** The house table is created with its unique policy-number index (ADPLM-C03-AC-06)
7. **Given** highest return code of earlier steps: 0, **when** no earlier step of the setup job ended with a return code above 4, **then** The motor table is created with unique index iMotor (ADPLM-C03-AC-07)
8. **Given** highest return code of earlier steps: 0, **when** no earlier step of the setup job ended with a return code above 4, **then** The Commercial table is created with fire, crime, flood and weather peril and premium columns (ADPLM-C03-AC-08)
9. **Given** highest return code of earlier steps: 4, **when** no earlier step of the setup job ended with a return code above 4, **then** The claim table and its unique claim-number index are created (ADPLM-C03-AC-09)
10. **Given** highest return code of earlier steps: 8, **when** no earlier step of the setup job ended with a return code above 4, **then** The step is skipped and the claim table is not created (ADPLM-C03-AC-10)
11. **Given** customers already created by the system: none, **when** Insurance Database Provisioning runs, **then** The first new customer gets number 1000001 (ADPLM-C03-AC-11)
12. **Given** policies already created by the system: none, **when** Insurance Database Provisioning runs, **then** The first new policy gets number 1000001 (ADPLM-C03-AC-12)
13. **Given** claims already created by the system: none, **when** Insurance Database Provisioning runs, **then** The first new claim gets number 1000001, the next 1000002 (ADPLM-C03-AC-13)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-012** (design note): When no earlier step of the setup job ended with a return code above 4, the system shall create the customer table (customer) holding name, date of birth, address, phones and email, and the customer security table (customer_secure) holding password value, state and password-change count, each with a unique index on customer number. Rules: ADPLM-BR-012.
- **ADPLM-REQ-F-013** (design note): When no earlier step of the setup job ended with a return code above 4, the system shall create the policy table (policy) holding customer, issue and expiry dates, policy type, last-changed timestamp, broker id, broker reference, payment and commission, with a unique index on policy number and a non-unique index on customer number. Rules: ADPLM-BR-013.
- **ADPLM-REQ-F-014** (design note): When no earlier step of the database set-up job has ended with a return code above 4, the system shall create the endowment details table, keyed on the policy number and linked to its parent policy, with a unique index on the policy number. Rules: ADPLM-BR-014.
- **ADPLM-REQ-F-015** (design note): When no earlier step of the setup job ended with a return code above 4, the system shall create the house details table (house), one row per policy (policyNumber), holding property type, bedrooms, value, house name, house number and postcode, with a unique index on the policy number. Rules: ADPLM-BR-015.
- **ADPLM-REQ-F-016** (design note): When no earlier step of the setup job ended with a return code above 4, the system shall create the motor details table (motor), one row per policy, holding make, model, value, registration, colour, engine size, year of manufacture, premium and accidents, with a unique index on the policy number. Rules: ADPLM-BR-016.
- **ADPLM-REQ-F-017** (design note): When no earlier step of the setup job ended with a return code above 4, the system shall create the commercial property table (Commercial), one row per policy, holding request, start and renewal dates, address, postcode, location, customer, property type, a peril indicator and premium for each of fire, crime, flood and weather, a status and a rejection reason, with a unique index on the policy number. Rules: ADPLM-BR-017.
- **ADPLM-REQ-F-018** (design note): When no earlier step of the setup job ended with a return code above 4, the system shall create the claim table (Claim) linked to a policy (PolicyNumber), holding claim date, amount paid, claim value, cause and observations, with a unique index on the claim number. Rules: ADPLM-BR-018.
- **ADPLM-REQ-F-019** (business rule): The system shall number customers automatically (customerNumber) starting at 1000001 and increasing by 1, unless a number is supplied. Rules: ADPLM-BR-019.
- **ADPLM-REQ-F-020** (business rule): The system shall number policies automatically (policyNumber) starting at 1000001 and increasing by 1, unless a number is supplied. Rules: ADPLM-BR-020.
- **ADPLM-REQ-F-021** (business rule): The system shall number claims automatically (ClaimNumber) starting at 1000001 and increasing by 1, unless a number is supplied. Rules: ADPLM-BR-021.

### Business rules

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

### Key entities

None found in the source.

### Needs clarification

- SME-009: The claim table has no standard name in the list of data entities. What should the new system call it? (Data architecture) On ADPLM-BR-021, ADPLM-BR-015, ADPLM-BR-017, ADPLM-BR-020, ADPLM-BR-016, ADPLM-BR-019, ADPLM-BR-014.
- SME-010: Customer, policy and claim numbers are generated automatically. What data type and length must these numbers have? (Data architecture) On ADPLM-BR-021, ADPLM-BR-015, ADPLM-BR-017, ADPLM-BR-020, ADPLM-BR-016, ADPLM-BR-019, ADPLM-BR-014.

### Decision table gaps

None.
