# Tasks: Load sample insurance data (ADPLM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C05-T1 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-027. Rules: ADPLM-BR-029.
  - Keep each business rule exactly as specified.
- [ ] ADPLM-C05-T2 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-026, ADPLM-REQ-F-028, ADPLM-REQ-F-029, ADPLM-REQ-F-030, ADPLM-REQ-F-031, ADPLM-REQ-F-032, ADPLM-REQ-F-033. Rules: ADPLM-BR-028, ADPLM-BR-030, ADPLM-BR-031, ADPLM-BR-032, ADPLM-BR-033, ADPLM-BR-034, ADPLM-BR-035. After: ADPLM-C05-T1.
  - ADPLM-BR-028: A seed-data script that runs only in demo and test environments. It inserts customers 1 to 10 with explicit customer numbers, so automatic numbering is not used, and stores a single blank (' ') where a house name, phone or email is absent instead of leaving the field null.
  - ADPLM-BR-030: Seed script for policies 1 to 10, each with an explicit number and linked to its customer. Types: C for 10, 9 and 7; E for 5 and 4; H for 6 and 8; M for 1, 3 and 2. It uses the listed dates, broker id 0, an empty broker reference, payment 0 and commission 0. Run it after the customer seed so the customer links are satisfied.
  - ADPLM-BR-031: Seed rows for endowment policies 5 and 4 with the listed values: 5 is N/N/N, 'SHEPPA', term 10, 50000, 'Shep'; 4 is Y/Y/N, 'LIONTMR', term 5, 12500, 'J. MORRIS'. Run after the policy seed.
  - ADPLM-BR-032: Seed rows for house details on policies 6, 7 and 8 with the listed property type, bedrooms, value, name, number and postcode. Run after the policy seed.
  - ADPLM-BR-033: Seed rows for motor details on policies 1, 3 and 2 with the listed make, model, value, premium, accidents, registration, colour, engine size and year. Run after the policy seed.
  - ADPLM-BR-034: Seed row for commercial cover on policy 10 ('HURSLEY PARK', 'SO212JN'): fire 3/8000, crime 3/25000, flood 5/2000, weather 4/5000, status 1, and 'ACTIVE' in the rejection reason field, stored exactly as given.
  - ADPLM-BR-035: Seed row for commercial cover on policy 9 ('TURF MOOR', 'BB104BX'): fire 1/44000, crime 2/25000, flood 3/15000, weather 4/6000, status 1, and 'ACTIVE' in the rejection reason field, stored exactly as given.
- [ ] ADPLM-C05-T3 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-026, ADPLM-REQ-F-027, ADPLM-REQ-F-028, ADPLM-REQ-F-029, ADPLM-REQ-F-030, ADPLM-REQ-F-031, ADPLM-REQ-F-032, ADPLM-REQ-F-033. Criteria: ADPLM-C05-AC-01, ADPLM-C05-AC-02, ADPLM-C05-AC-03, ADPLM-C05-AC-04, ADPLM-C05-AC-05, ADPLM-C05-AC-06, ADPLM-C05-AC-07, ADPLM-C05-AC-08, ADPLM-C05-AC-09, ADPLM-C05-AC-10, ADPLM-C05-AC-11, ADPLM-C05-AC-12, ADPLM-C05-AC-13. After: ADPLM-C05-T1, ADPLM-C05-T2.
  - 13 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C05-T4 [compliance] Review the handling of money, personal data, security. Requirements: ADPLM-REQ-F-026, ADPLM-REQ-F-027, ADPLM-REQ-F-028, ADPLM-REQ-F-029, ADPLM-REQ-F-030, ADPLM-REQ-F-031, ADPLM-REQ-F-032, ADPLM-REQ-F-033. After: ADPLM-C05-T1, ADPLM-C05-T2.
  - Check storage, logs, screens and audit against the rules.
