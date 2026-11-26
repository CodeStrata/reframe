# Design: Load sample insurance data (ADPLM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Loads a fixed set of sample data for demonstrating and testing the application: ten customers with security records, ten policies, and their endowment, house, motor and commercial cover details. It is for administrators preparing a demo or test environment. The values must be loaded exactly as listed, and the shared sample password value must never reach a production environment.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-028 | Load the ten sample customer profiles | design note | THE Insurance Sample Data Load SHALL insert sample customers numbered 1 to 10 into the customer table with name, date of birth, house name, house number, postcode, home phone, mobile phone and email, storing a blank (' ') where a house name, phone or email is absent. | medium | base/cntl/db2cre.jcl:412, base/cntl/db2cre.jcl:425-446, base/cntl/db2cre.jcl:697-718, base/cntl/db2cre.jcl:731-752 |
| ADPLM-BR-029 | Create initial customer credentials | business rule | THE Insurance Sample Data Load SHALL give each sample customer 1 to 10 a security record (customer_secure) with the same stored password value '5732fec825535eeafb8fac50fee3a8aa', state 'N' (state_indicator) and 0 password changes (pass_changes). | medium | base/cntl/db2cre.jcl:448-457, base/cntl/db2cre.jcl:754-763 |
| ADPLM-BR-030 | Register the ten sample policies | design note | THE Insurance Sample Data Load SHALL insert policies 1 to 10 linked to their customers, with type 'C' (commercial, policies 10, 9, 7), 'E' (endowment, 5, 4), 'H' (house, 6, 8) or 'M' (motor, 1, 3, 2), the listed issue, expiry and last-changed dates, broker id 0, empty broker reference, payment 0 and commission 0. | medium | base/cntl/db2cre.jcl:765-1002 |
| ADPLM-BR-031 | Add endowment details for policies 4 and 5 | design note | THE Insurance Sample Data Load SHALL insert endowment details for policy 5 (equities 'N', with-profits 'N', managed fund 'N', fund 'SHEPPA', term 10, sum assured 50000, life assured 'Shep') and policy 4 (equities 'Y', with-profits 'Y', managed fund 'N', fund 'LIONTMR', term 5, sum assured 12500, life assured 'J. MORRIS'). | medium | base/cntl/db2cre.jcl:1004-1040 |
| ADPLM-BR-032 | Add house property details | design note | THE Insurance Sample Data Load SHALL insert house details for policy 6 ('HOUSE', 5 bedrooms, value 1500000, number '5', postcode 'SO211UP'), policy 7 ('FARM', 8 bedrooms, value 3750000, 'HOME FARM', number '4', postcode 'SO529ED') and policy 8 ('FLAT', 1 bedroom, value 260000, number '12b', postcode 'E15WW'). | medium | base/cntl/db2cre.jcl:1042-1091 |
| ADPLM-BR-033 | Add motor vehicle details | design note | THE Insurance Sample Data Load SHALL insert motor details for policy 1 ('FORD' 'KA', value 8500, premium 450, 0 accidents), policy 3 ('DENNIS' 'ENGINE', value 23500, premium 2850, 12 accidents) and policy 2 ('VOLKSWAGEN' 'BEETLE', value 600, premium 700, 1 accident), with registration, colour, engine size and year of manufacture. | medium | base/cntl/db2cre.jcl:1093-1160 |
| ADPLM-BR-034 | Add commercial property cover details | design note | THE Insurance Sample Data Load SHALL add commercial property cover for policy 10 (IBM offices at 'HURSLEY PARK', 'SO212JN') with fire peril 3/premium 8000, crime 3/25000, flood 5/2000, weather 4/5000, status 1 and 'ACTIVE' recorded in the rejection reason field. | medium | base/cntl/db2cre.jcl:412, base/cntl/db2cre.jcl:1162-1247, base/cntl/db2cre.jcl:313-337 |
| ADPLM-BR-035 | Add commercial property cover details | design note | THE Insurance Sample Data Load SHALL add commercial property cover for policy 9 (Burnley Football Club stadium at 'TURF MOOR', 'BB104BX') with fire peril 1/premium 44000, crime 2/25000, flood 3/15000, weather 4/6000, status 1 and 'ACTIVE' recorded in the rejection reason field. | medium | base/cntl/db2cre.jcl:412, base/cntl/db2cre.jcl:1162-1247, base/cntl/db2cre.jcl:313-337 |

### Worked examples

- ADPLM-BR-028: customer number = 1 → Customer 1 is 'Andrew' 'Pandy', born '1950-07-11', house name ' ', house number '34', postcode 'PI101OO'
- ADPLM-BR-028: customer number = 9 → Customer 9 'Micky' 'Murphy' has home phone, mobile and email all ' '
- ADPLM-BR-029: customer number = 7 → Security record: password value '5732fec825535eeafb8fac50fee3a8aa', state 'N', password changes 0
- ADPLM-BR-030: policy number = 10 → Policy 10 for customer 1, type 'C', issued '2011-08-22', expires '2012-08-21', broker id 0, payment 0, commission 0
- ADPLM-BR-030: policy number = 6 → Policy 6 for customer 4, type 'H', issued '2011-09-01', expires '2011-12-31'
- ADPLM-BR-031: policy number = 4 → Endowment row: fund 'LIONTMR', term 5, sum assured 12500, life assured 'J. MORRIS'
- ADPLM-BR-031: policy number = 5 → Endowment row: fund 'SHEPPA', term 10, sum assured 50000, life assured 'Shep'
- ADPLM-BR-032: policy number = 7 → House row: 'FARM', 8 bedrooms, value 3750000, house name 'HOME FARM', postcode 'SO529ED'
- ADPLM-BR-032: policy number = 8 → House row: 'FLAT', 1 bedroom, value 260000, house name ' ', postcode 'E15WW'
- ADPLM-BR-033: policy number = 3 → Motor row: 'DENNIS' 'ENGINE', reg 'FIRE1', 'RED', 5000 cc, made '1973-05-13', premium 2850, 12 accidents
- ADPLM-BR-033: policy number = 2 → Motor row: 'VOLKSWAGEN' 'BEETLE', reg 'A567WWR', 'PURPLE', premium 700, 1 accident
- ADPLM-BR-034: policy number = 10 → Commercial row for 'IBM', property type 'OFFICES', start 2011-08-25, renewal 2011-08-24, fire premium 8000, status 1, rejection reason 'ACTIVE'.
- ADPLM-BR-035: policy number = 9 → Commercial row for 'Burnley Football Club', property type 'STADIUM', start 2011-08-01, renewal 2011-07-30, fire premium 44000, status 1, rejection reason 'ACTIVE'.

## Decision tables

None.

## Design notes

- ADPLM-BR-028: A seed-data script that runs only in demo and test environments. It inserts customers 1 to 10 with explicit customer numbers, so automatic numbering is not used, and stores a single blank (' ') where a house name, phone or email is absent instead of leaving the field null.
- ADPLM-BR-030: Seed script for policies 1 to 10, each with an explicit number and linked to its customer. Types: C for 10, 9 and 7; E for 5 and 4; H for 6 and 8; M for 1, 3 and 2. It uses the listed dates, broker id 0, an empty broker reference, payment 0 and commission 0. Run it after the customer seed so the customer links are satisfied.
- ADPLM-BR-031: Seed rows for endowment policies 5 and 4 with the listed values: 5 is N/N/N, 'SHEPPA', term 10, 50000, 'Shep'; 4 is Y/Y/N, 'LIONTMR', term 5, 12500, 'J. MORRIS'. Run after the policy seed.
- ADPLM-BR-032: Seed rows for house details on policies 6, 7 and 8 with the listed property type, bedrooms, value, name, number and postcode. Run after the policy seed.
- ADPLM-BR-033: Seed rows for motor details on policies 1, 3 and 2 with the listed make, model, value, premium, accidents, registration, colour, engine size and year. Run after the policy seed.
- ADPLM-BR-034: Seed row for commercial cover on policy 10 ('HURSLEY PARK', 'SO212JN'): fire 3/8000, crime 3/25000, flood 5/2000, weather 4/5000, status 1, and 'ACTIVE' in the rejection reason field, stored exactly as given.
- ADPLM-BR-035: Seed row for commercial cover on policy 9 ('TURF MOOR', 'BB104BX'): fire 1/44000, crime 2/25000, flood 3/15000, weather 4/6000, status 1, and 'ACTIVE' in the rejection reason field, stored exactly as given.

## Open questions

- SME-011: The sample customers and policies are numbered 1 to 10, but generated customer and policy numbers start at 1000001. Should the sample records keep their numbers below the generated range, or should they get generated numbers? (Data architecture) On ADPLM-BR-028, ADPLM-BR-031, ADPLM-BR-032, ADPLM-BR-033, ADPLM-BR-029, ADPLM-BR-030, ADPLM-BR-035.
- SME-012: The sample commercial policies have status 1 and the text 'ACTIVE' in the rejection reason field. Is the rejection reason field meant to hold status text? (Business analyst) On ADPLM-BR-028, ADPLM-BR-031, ADPLM-BR-032, ADPLM-BR-033, ADPLM-BR-029, ADPLM-BR-030, ADPLM-BR-035.
- SME-013: In two sample commercial policies, the renewal date is earlier than the start date (renewal 2011-08-24, start 2011-08-25; renewal 2011-07-30, start 2011-08-01). Is this intended sample data, or is it an error? (Business analyst) On ADPLM-BR-028, ADPLM-BR-031, ADPLM-BR-032, ADPLM-BR-033, ADPLM-BR-029, ADPLM-BR-030, ADPLM-BR-035.
- SME-014: All ten sample customer logins share the same password value. Should the sample data in the new system keep this shared password? (Security team) On ADPLM-BR-028, ADPLM-BR-031, ADPLM-BR-032, ADPLM-BR-033, ADPLM-BR-029, ADPLM-BR-030, ADPLM-BR-035.
- DEF-031: Is this intended? The INSERT step has no COND parameter, so it runs even when the table-creation steps were skipped for a return code above 4, and the sample numbers 1 to 10 sit outside the generated range that starts at 1000001. (Subject-matter expert) On ADPLM-BR-028.
- DEF-033: Confirm this is deliberate: All ten sample customers share one hard-coded password value in the setup job. (Subject-matter expert) On ADPLM-BR-029.
- DEF-039: Is this intended? The sample commercial rows put 'ACTIVE' into the rejection reason column and give renewal dates a day or two before the start dates (2011-08-24 vs 2011-08-25; 2011-07-30 vs 2011-08-01); the INSERT step also has no COND, so it runs even if the table-creation steps failed. (Subject-matter expert) On ADPLM-BR-035.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).