# Requirements: Load sample insurance data (ADPLM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Loads a fixed set of sample data for demonstrating and testing the application: ten customers with security records, ten policies, and their endowment, house, motor and commercial cover details. It is for administrators preparing a demo or test environment. The values must be loaded exactly as listed, and the shared sample password value must never reach a production environment.

**User story:** As an application administrator, I want sample customers, credentials, policies and product details loaded into the database, so that the application can be demonstrated and tested with realistic data.

## Requirements

### Requirement 1: ADPLM-REQ-F-026 (design note)

#### Acceptance criteria

1. The system shall insert sample customers numbered 1 to 10 into the customer table with name, date of birth, house name, house number, postcode, home phone, mobile phone and email, storing a blank (' ') where a house name, phone or email is absent. (rules ADPLM-BR-028)
2. GIVEN customer number: 1 WHEN Insurance Sample Data Load runs THEN Customer 1 is 'Andrew' 'Pandy', born '1950-07-11', house name ' ', house number '34', postcode 'PI101OO' (ADPLM-C05-AC-01; ADPLM-BR-028)
3. GIVEN customer number: 9 WHEN Insurance Sample Data Load runs THEN Customer 9 'Micky' 'Murphy' has home phone, mobile and email all ' ' (ADPLM-C05-AC-02; ADPLM-BR-028)

### Requirement 2: ADPLM-REQ-F-027 (business rule)

#### Acceptance criteria

1. The system shall give each sample customer 1 to 10 a security record (customer_secure) with the same stored password value '5732fec825535eeafb8fac50fee3a8aa', state 'N' (state_indicator) and 0 password changes (pass_changes). (rules ADPLM-BR-029)
2. GIVEN customer number: 7 WHEN Insurance Sample Data Load runs THEN Security record: password value '5732fec825535eeafb8fac50fee3a8aa', state 'N', password changes 0 (ADPLM-C05-AC-03; ADPLM-BR-029)

### Requirement 3: ADPLM-REQ-F-028 (design note)

#### Acceptance criteria

1. The system shall insert policies 1 to 10 linked to their customers, with type 'C' (commercial, policies 10, 9, 7), 'E' (endowment, 5, 4), 'H' (house, 6, 8) or 'M' (motor, 1, 3, 2), the listed issue, expiry and last-changed dates, broker id 0, empty broker reference, payment 0 and commission 0. (rules ADPLM-BR-030)
2. GIVEN policy number: 10 WHEN Insurance Sample Data Load runs THEN Policy 10 for customer 1, type 'C', issued '2011-08-22', expires '2012-08-21', broker id 0, payment 0, commission 0 (ADPLM-C05-AC-04; ADPLM-BR-030)
3. GIVEN policy number: 6 WHEN Insurance Sample Data Load runs THEN Policy 6 for customer 4, type 'H', issued '2011-09-01', expires '2011-12-31' (ADPLM-C05-AC-05; ADPLM-BR-030)

### Requirement 4: ADPLM-REQ-F-029 (design note)

#### Acceptance criteria

1. The system shall insert endowment details for policy 5 (equities 'N', with-profits 'N', managed fund 'N', fund 'SHEPPA', term 10, sum assured 50000, life assured 'Shep') and policy 4 (equities 'Y', with-profits 'Y', managed fund 'N', fund 'LIONTMR', term 5, sum assured 12500, life assured 'J. MORRIS'). (rules ADPLM-BR-031)
2. GIVEN policy number: 4 WHEN Insurance Sample Data Load runs THEN Endowment row: fund 'LIONTMR', term 5, sum assured 12500, life assured 'J. MORRIS' (ADPLM-C05-AC-06; ADPLM-BR-031)
3. GIVEN policy number: 5 WHEN Insurance Sample Data Load runs THEN Endowment row: fund 'SHEPPA', term 10, sum assured 50000, life assured 'Shep' (ADPLM-C05-AC-07; ADPLM-BR-031)

### Requirement 5: ADPLM-REQ-F-030 (design note)

#### Acceptance criteria

1. The system shall insert house details for policy 6 ('HOUSE', 5 bedrooms, value 1500000, number '5', postcode 'SO211UP'), policy 7 ('FARM', 8 bedrooms, value 3750000, 'HOME FARM', number '4', postcode 'SO529ED') and policy 8 ('FLAT', 1 bedroom, value 260000, number '12b', postcode 'E15WW'). (rules ADPLM-BR-032)
2. GIVEN policy number: 7 WHEN Insurance Sample Data Load runs THEN House row: 'FARM', 8 bedrooms, value 3750000, house name 'HOME FARM', postcode 'SO529ED' (ADPLM-C05-AC-08; ADPLM-BR-032)
3. GIVEN policy number: 8 WHEN Insurance Sample Data Load runs THEN House row: 'FLAT', 1 bedroom, value 260000, house name ' ', postcode 'E15WW' (ADPLM-C05-AC-09; ADPLM-BR-032)

### Requirement 6: ADPLM-REQ-F-031 (design note)

#### Acceptance criteria

1. The system shall insert motor details for policy 1 ('FORD' 'KA', value 8500, premium 450, 0 accidents), policy 3 ('DENNIS' 'ENGINE', value 23500, premium 2850, 12 accidents) and policy 2 ('VOLKSWAGEN' 'BEETLE', value 600, premium 700, 1 accident), with registration, colour, engine size and year of manufacture. (rules ADPLM-BR-033)
2. GIVEN policy number: 3 WHEN Insurance Sample Data Load runs THEN Motor row: 'DENNIS' 'ENGINE', reg 'FIRE1', 'RED', 5000 cc, made '1973-05-13', premium 2850, 12 accidents (ADPLM-C05-AC-10; ADPLM-BR-033)
3. GIVEN policy number: 2 WHEN Insurance Sample Data Load runs THEN Motor row: 'VOLKSWAGEN' 'BEETLE', reg 'A567WWR', 'PURPLE', premium 700, 1 accident (ADPLM-C05-AC-11; ADPLM-BR-033)

### Requirement 7: ADPLM-REQ-F-032 (design note)

#### Acceptance criteria

1. The system shall add commercial property cover for policy 10 (IBM offices at 'HURSLEY PARK', 'SO212JN') with fire peril 3/premium 8000, crime 3/25000, flood 5/2000, weather 4/5000, status 1 and 'ACTIVE' recorded in the rejection reason field. (rules ADPLM-BR-034)
2. GIVEN policy number: 10 WHEN Insurance Sample Data Load runs THEN Commercial row for 'IBM', property type 'OFFICES', start 2011-08-25, renewal 2011-08-24, fire premium 8000, status 1, rejection reason 'ACTIVE'. (ADPLM-C05-AC-12; ADPLM-BR-034)

### Requirement 8: ADPLM-REQ-F-033 (design note)

#### Acceptance criteria

1. The system shall add commercial property cover for policy 9 (Burnley Football Club stadium at 'TURF MOOR', 'BB104BX') with fire peril 1/premium 44000, crime 2/25000, flood 3/15000, weather 4/6000, status 1 and 'ACTIVE' recorded in the rejection reason field. (rules ADPLM-BR-035)
2. GIVEN policy number: 9 WHEN Insurance Sample Data Load runs THEN Commercial row for 'Burnley Football Club', property type 'STADIUM', start 2011-08-01, renewal 2011-07-30, fire premium 44000, status 1, rejection reason 'ACTIVE'. (ADPLM-C05-AC-13; ADPLM-BR-035)
