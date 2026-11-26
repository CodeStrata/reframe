# Store product details for a new policy (ADPLM-C08)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGAPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGAPDB01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-052 | Create endowment policy details | business rule | WHEN an Endowment add request ('01AEND') is longer than its required length (28-byte header plus 124 bytes of endowment details, 152 in all), THE policy add service SHALL store the endowment row for the new policy number with with-profits, equities, managed fund, fund name, term, sum assured and life assured, plus the extra bytes beyond 152 as free-form padding data (PADDINGDATA). | high | base/src/lgapdb01.cbl:182-188, base/src/lgpolicy.cpy:24, base/src/lgapdb01.cbl:327-397, base/src/lgapdb01.cbl:562-594 |
| ADPLM-BR-053 | Create endowment policy details | business rule | WHEN an Endowment add request ('01AEND') is exactly its required length of 152 bytes, THE policy add service SHALL store the endowment row with the same details but without any padding data. | high | base/src/lgapdb01.cbl:182-188, base/src/lgpolicy.cpy:24, base/src/lgapdb01.cbl:327-397, base/src/lgapdb01.cbl:562-594 |
| ADPLM-BR-054 | Create endowment policy details | error handling | WHEN the endowment row cannot be stored, THE policy add service SHALL set return code '90', log the error (date, time, customer and policy number, SQL code, and the first 90 bytes of the request) and end abnormally with code 'LGSQ' so the policy row already added is backed out. | high | base/src/lgapdb01.cbl:182-188, base/src/lgpolicy.cpy:24, base/src/lgapdb01.cbl:327-397, base/src/lgapdb01.cbl:562-594 |
| ADPLM-BR-055 | Create house policy details | business rule | WHEN a House add request ('01AHOU') has had its policy row created, THE policy add service SHALL store the house details (property type, bedrooms, value, house name, house number, postcode) under the new policy number. | high | base/src/lgapdb01.cbl:223-241, base/src/lgapdb01.cbl:389-395, base/src/lgapdb01.cbl:402-435, base/src/lgapdb01.cbl:440-481 |
| ADPLM-BR-056 | Motor and house details stored without rating | business rule | WHEN a motor policy is added, THE Policy Registration SHALL store the premium and the number of accidents exactly as supplied in the request, without changing the premium for accidents, engine size or vehicle value. | medium | base/src/lgapdb01.cbl:440-471 |
| ADPLM-BR-057 | Create commercial policy details | business rule | WHEN a Commercial add request ('01ACOM') has its policy row created, THE policy add service SHALL store the commercial row for the new policy number with the policy's last-changed timestamp as request date, the issue date as start date and the expiry date as renewal date. | high | base/src/lgapdb01.cbl:315-321, base/src/lgapdb01.cbl:486-555 |
| ADPLM-BR-058 | Add commercial policy details | design note | THE policy add service SHALL store the commercial address, postcode, latitude, longitude, customer name, property type, fire, crime, flood and weather perils and premiums, status and rejection reason exactly as supplied, without calculating any premium or deriving any status. | high | base/src/lgapdb01.cbl:315-321, base/src/lgapdb01.cbl:486-555 |
| ADPLM-BR-059 | Create commercial policy details | error handling | WHEN the commercial row cannot be stored, THE policy add service SHALL set return code '90', log the error and end abnormally with code 'LGSQ' so the policy row already added is backed out. | high | base/src/lgapdb01.cbl:315-321, base/src/lgapdb01.cbl:486-555 |

### Worked examples

- ADPLM-BR-052: request = '01AEND'; request length = 252 bytes → The endowment row is stored with the 100 bytes beyond 152 as padding data.
- ADPLM-BR-053: request = '01AEND'; request length = 152 bytes → The endowment row is stored; the padding data column is left out.
- ADPLM-BR-054: request = '01AEND'; endowment insert = fails → Return code '90', error logged, task abends 'LGSQ' and the new policy row is rolled back.
- ADPLM-BR-055: request = '01AHOU'; new policy number = 2000123; bedrooms = 3; value = 250000; postcode = SO21 2JN → A house row for policy 2000123 is stored with 3 bedrooms, value 250000 and postcode SO21 2JN.
- ADPLM-BR-056: request identifier = '01AMOT'; vehicle value = 15000; engine size (cc) = 1600; premium = 450; accidents = 2 → The MOTOR row stores PREMIUM 450 and ACCIDENTS 2, as supplied.
- ADPLM-BR-056: request identifier = '01AMOT'; premium = 300; accidents = 0 → The MOTOR row stores PREMIUM 300 and ACCIDENTS 0.
- ADPLM-BR-057: issue date = 2026-03-01; expiry date = 2027-03-01 → Start date 2026-03-01, renewal date 2027-03-01, request date = the new policy's last-changed timestamp.
- ADPLM-BR-058: fire premium = 500; status = 0; rejection reason = blank → Fire premium 500, status 0 and a blank rejection reason are stored as given.
- ADPLM-BR-059: request = '01ACOM'; commercial insert = fails → Return code '90', error logged, task abends 'LGSQ' and the policy row is rolled back.

## Decision tables

None.

## Design notes

- ADPLM-BR-058: A plain field-to-column mapping for the commercial details: address, postcode, latitude, longitude, customer name, property type, the four perils and premiums, status and rejection reason, stored exactly as supplied. There is no rating engine or status derivation in this step.

## Open questions

- SME-033: If the main policy record is saved but saving its type-specific details (endowment, house, motor or commercial) then fails, should the main policy record be removed so that the two are always saved together or not at all? (Policy administration business analyst) On ADPLM-BR-054, ADPLM-BR-059, ADPLM-BR-055.
- SME-035: Motor and house policies are stored with whatever premium the caller supplies. Is the premium meant to be calculated somewhere else before this step, or is it intended that the caller supplies it? (Underwriting / pricing lead) On ADPLM-BR-056.
- SME-036: When a commercial policy is added, what do its status codes mean (for example, 0 = accepted and anything else = rejected)? Are the premiums for each peril calculated earlier, by the caller or another program, rather than at this step? (Commercial underwriting SME) On ADPLM-BR-058.
- DEF-003: Is this intended? The only caller in the source (LGAPOL01) always links with a length of 32500, so the request is always treated as carrying 32348 bytes of padding; that is moved into a 3900-byte work field (WS-VARY-CHAR), overrunning it, and the no-padding insert can never be chosen on that path. (Subject-matter expert) On ADPLM-BR-053, ADPLM-BR-054.
- DEF-024: Confirm this is deliberate: Return code '90' is set before the abend, but the abend ends the task so the caller never receives it, and the RETURN after each abend can never run. (Subject-matter expert) On ADPLM-BR-055.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (9 in all).
