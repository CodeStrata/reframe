# Requirements: Store product details for a new policy (ADPLM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk high

## Introduction

Stores the endowment, house, motor or commercial details of a new policy under its newly assigned policy number. It is for policy administrators. Details are stored exactly as supplied, with no premium calculated or status derived. If the product details cannot be stored, the whole new policy must be undone so no half-created policy remains.

**User story:** As a policy administrator, I want the endowment, house, motor or commercial details of a new policy stored under its policy number, so that each policy holds the cover details supplied for its product.

## Requirements

### Requirement 1: ADPLM-REQ-F-047 (business rule)

#### Acceptance criteria

1. When an Endowment add request ('01AEND') is longer than its required length of 152 bytes (28-byte header plus 124 bytes of endowment details), the system shall store the endowment row for the new policy number with with-profits, equities, managed fund, fund name, term, sum assured and life assured, plus the extra bytes beyond 152 as free-form padding data (PADDINGDATA). (rules ADPLM-BR-052)
2. GIVEN request: '01AEND'; request length: 252 bytes WHEN an Endowment add request ('01AEND') is longer than its required length (28-byte header plus 124 bytes of endowment details, 152 in all) THEN The endowment row is stored with the 100 bytes beyond 152 as padding data. (ADPLM-C08-AC-01; ADPLM-BR-052)

### Requirement 2: ADPLM-REQ-F-048 (business rule)

#### Acceptance criteria

1. When an Endowment add request ('01AEND') is exactly its required length of 152 bytes, the system shall store the endowment row with the same details but without any padding data. (rules ADPLM-BR-053)
2. GIVEN request: '01AEND'; request length: 152 bytes WHEN an Endowment add request ('01AEND') is exactly its required length of 152 bytes THEN The endowment row is stored; the padding data column is left out. (ADPLM-C08-AC-02; ADPLM-BR-053)

### Requirement 3: ADPLM-REQ-F-049 (error handling)

#### Acceptance criteria

1. If the endowment row cannot be stored, then the system shall set return code '90', log the error (date, time, customer and policy number, SQL code, and the first 90 bytes of the request) and end abnormally with code 'LGSQ' so the policy row already added is backed out. (rules ADPLM-BR-054)
2. GIVEN request: '01AEND'; endowment insert: fails WHEN the endowment row cannot be stored THEN Return code '90', error logged, task abends 'LGSQ' and the new policy row is rolled back. (ADPLM-C08-AC-03; ADPLM-BR-054)

### Requirement 4: ADPLM-REQ-F-050 (business rule)

#### Acceptance criteria

1. When a House add request ('01AHOU') has had its policy row created, the system shall store the house details (property type, bedrooms, value, house name, house number, postcode) under the new policy number. (rules ADPLM-BR-055)
2. GIVEN request: '01AHOU'; new policy number: 2000123; bedrooms: 3; value: 250000; postcode: SO21 2JN WHEN a House add request ('01AHOU') has had its policy row created THEN A house row for policy 2000123 is stored with 3 bedrooms, value 250000 and postcode SO21 2JN. (ADPLM-C08-AC-04; ADPLM-BR-055)

### Requirement 5: ADPLM-REQ-F-051 (business rule)

#### Acceptance criteria

1. When a motor policy is added, the system shall store the premium and the number of accidents exactly as supplied in the request, without changing the premium for accidents, engine size or vehicle value. (rules ADPLM-BR-056)
2. GIVEN request identifier: '01AMOT'; vehicle value: 15000; engine size (cc): 1600; premium: 450; accidents: 2 WHEN a motor policy is added THEN The MOTOR row stores PREMIUM 450 and ACCIDENTS 2, as supplied. (ADPLM-C08-AC-05; ADPLM-BR-056)
3. GIVEN request identifier: '01AMOT'; premium: 300; accidents: 0 WHEN a motor policy is added THEN The MOTOR row stores PREMIUM 300 and ACCIDENTS 0. (ADPLM-C08-AC-06; ADPLM-BR-056)

### Requirement 6: ADPLM-REQ-F-052 (business rule)

#### Acceptance criteria

1. When a Commercial add request ('01ACOM') has its policy row created, the system shall store the commercial row for the new policy number with the policy's last-changed timestamp as request date, the issue date as start date and the expiry date as renewal date. (rules ADPLM-BR-057)
2. GIVEN issue date: 2026-03-01; expiry date: 2027-03-01 WHEN a Commercial add request ('01ACOM') has its policy row created THEN Start date 2026-03-01, renewal date 2027-03-01, request date = the new policy's last-changed timestamp. (ADPLM-C08-AC-07; ADPLM-BR-057)

### Requirement 7: ADPLM-REQ-F-053 (design note)

#### Acceptance criteria

1. The system shall store the commercial address, postcode, latitude, longitude, customer name, property type, fire, crime, flood and weather perils and premiums, status and rejection reason exactly as supplied, without calculating any premium or deriving any status. (rules ADPLM-BR-058)
2. GIVEN fire premium: 500; status: 0; rejection reason: blank WHEN policy add service runs THEN Fire premium 500, status 0 and a blank rejection reason are stored as given. (ADPLM-C08-AC-08; ADPLM-BR-058)

### Requirement 8: ADPLM-REQ-F-054 (error handling)

#### Acceptance criteria

1. If the commercial row cannot be stored, then the system shall set return code '90', log the error and end abnormally with code 'LGSQ' so the policy row already added is backed out. (rules ADPLM-BR-059)
2. GIVEN request: '01ACOM'; commercial insert: fails WHEN the commercial row cannot be stored THEN Return code '90', error logged, task abends 'LGSQ' and the policy row is rolled back. (ADPLM-C08-AC-09; ADPLM-BR-059)
