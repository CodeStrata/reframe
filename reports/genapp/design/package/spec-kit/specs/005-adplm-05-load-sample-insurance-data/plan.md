# Implementation plan: Load sample insurance data (ADPLM-C05)

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

- ADPLM-BR-028: A seed-data script that runs only in demo and test environments. It inserts customers 1 to 10 with explicit customer numbers, so automatic numbering is not used, and stores a single blank (' ') where a house name, phone or email is absent instead of leaving the field null.
- ADPLM-BR-030: Seed script for policies 1 to 10, each with an explicit number and linked to its customer. Types: C for 10, 9 and 7; E for 5 and 4; H for 6 and 8; M for 1, 3 and 2. It uses the listed dates, broker id 0, an empty broker reference, payment 0 and commission 0. Run it after the customer seed so the customer links are satisfied.
- ADPLM-BR-031: Seed rows for endowment policies 5 and 4 with the listed values: 5 is N/N/N, 'SHEPPA', term 10, 50000, 'Shep'; 4 is Y/Y/N, 'LIONTMR', term 5, 12500, 'J. MORRIS'. Run after the policy seed.
- ADPLM-BR-032: Seed rows for house details on policies 6, 7 and 8 with the listed property type, bedrooms, value, name, number and postcode. Run after the policy seed.
- ADPLM-BR-033: Seed rows for motor details on policies 1, 3 and 2 with the listed make, model, value, premium, accidents, registration, colour, engine size and year. Run after the policy seed.
- ADPLM-BR-034: Seed row for commercial cover on policy 10 ('HURSLEY PARK', 'SO212JN'): fire 3/8000, crime 3/25000, flood 5/2000, weather 4/5000, status 1, and 'ACTIVE' in the rejection reason field, stored exactly as given.
- ADPLM-BR-035: Seed row for commercial cover on policy 9 ('TURF MOOR', 'BB104BX'): fire 1/44000, crime 2/25000, flood 3/15000, weather 4/6000, status 1, and 'ACTIVE' in the rejection reason field, stored exactly as given.

## Decision tables

None.
