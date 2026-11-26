# Feature specification: Store product details for a new policy

**Feature:** ADPLM-C08 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C08)

As a policy administrator, I want the endowment, house, motor or commercial details of a new policy stored under its policy number, so that each policy holds the cover details supplied for its product.

Stores the endowment, house, motor or commercial details of a new policy under its newly assigned policy number. It is for policy administrators. Details are stored exactly as supplied, with no premium calculated or status derived. If the product details cannot be stored, the whole new policy must be undone so no half-created policy remains.

**Acceptance scenarios:**

1. **Given** request: '01AEND'; request length: 252 bytes, **when** an Endowment add request ('01AEND') is longer than its required length (28-byte header plus 124 bytes of endowment details, 152 in all), **then** The endowment row is stored with the 100 bytes beyond 152 as padding data. (ADPLM-C08-AC-01)
2. **Given** request: '01AEND'; request length: 152 bytes, **when** an Endowment add request ('01AEND') is exactly its required length of 152 bytes, **then** The endowment row is stored; the padding data column is left out. (ADPLM-C08-AC-02)
3. **Given** request: '01AEND'; endowment insert: fails, **when** the endowment row cannot be stored, **then** Return code '90', error logged, task abends 'LGSQ' and the new policy row is rolled back. (ADPLM-C08-AC-03)
4. **Given** request: '01AHOU'; new policy number: 2000123; bedrooms: 3; value: 250000; postcode: SO21 2JN, **when** a House add request ('01AHOU') has had its policy row created, **then** A house row for policy 2000123 is stored with 3 bedrooms, value 250000 and postcode SO21 2JN. (ADPLM-C08-AC-04)
5. **Given** request identifier: '01AMOT'; vehicle value: 15000; engine size (cc): 1600; premium: 450; accidents: 2, **when** a motor policy is added, **then** The MOTOR row stores PREMIUM 450 and ACCIDENTS 2, as supplied. (ADPLM-C08-AC-05)
6. **Given** request identifier: '01AMOT'; premium: 300; accidents: 0, **when** a motor policy is added, **then** The MOTOR row stores PREMIUM 300 and ACCIDENTS 0. (ADPLM-C08-AC-06)
7. **Given** issue date: 2026-03-01; expiry date: 2027-03-01, **when** a Commercial add request ('01ACOM') has its policy row created, **then** Start date 2026-03-01, renewal date 2027-03-01, request date = the new policy's last-changed timestamp. (ADPLM-C08-AC-07)
8. **Given** fire premium: 500; status: 0; rejection reason: blank, **when** policy add service runs, **then** Fire premium 500, status 0 and a blank rejection reason are stored as given. (ADPLM-C08-AC-08)
9. **Given** request: '01ACOM'; commercial insert: fails, **when** the commercial row cannot be stored, **then** Return code '90', error logged, task abends 'LGSQ' and the policy row is rolled back. (ADPLM-C08-AC-09)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-047** (business rule): When an Endowment add request ('01AEND') is longer than its required length of 152 bytes (28-byte header plus 124 bytes of endowment details), the system shall store the endowment row for the new policy number with with-profits, equities, managed fund, fund name, term, sum assured and life assured, plus the extra bytes beyond 152 as free-form padding data (PADDINGDATA). Rules: ADPLM-BR-052.
- **ADPLM-REQ-F-048** (business rule): When an Endowment add request ('01AEND') is exactly its required length of 152 bytes, the system shall store the endowment row with the same details but without any padding data. Rules: ADPLM-BR-053.
- **ADPLM-REQ-F-049** (error handling): If the endowment row cannot be stored, then the system shall set return code '90', log the error (date, time, customer and policy number, SQL code, and the first 90 bytes of the request) and end abnormally with code 'LGSQ' so the policy row already added is backed out. Rules: ADPLM-BR-054.
- **ADPLM-REQ-F-050** (business rule): When a House add request ('01AHOU') has had its policy row created, the system shall store the house details (property type, bedrooms, value, house name, house number, postcode) under the new policy number. Rules: ADPLM-BR-055.
- **ADPLM-REQ-F-051** (business rule): When a motor policy is added, the system shall store the premium and the number of accidents exactly as supplied in the request, without changing the premium for accidents, engine size or vehicle value. Rules: ADPLM-BR-056.
- **ADPLM-REQ-F-052** (business rule): When a Commercial add request ('01ACOM') has its policy row created, the system shall store the commercial row for the new policy number with the policy's last-changed timestamp as request date, the issue date as start date and the expiry date as renewal date. Rules: ADPLM-BR-057.
- **ADPLM-REQ-F-053** (design note): The system shall store the commercial address, postcode, latitude, longitude, customer name, property type, fire, crime, flood and weather perils and premiums, status and rejection reason exactly as supplied, without calculating any premium or deriving any status. Rules: ADPLM-BR-058.
- **ADPLM-REQ-F-054** (error handling): If the commercial row cannot be stored, then the system shall set return code '90', log the error and end abnormally with code 'LGSQ' so the policy row already added is backed out. Rules: ADPLM-BR-059.

### Business rules

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

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- SME-033: If the main policy record is saved but saving its type-specific details (endowment, house, motor or commercial) then fails, should the main policy record be removed so that the two are always saved together or not at all? (Policy administration business analyst) On ADPLM-BR-054, ADPLM-BR-059, ADPLM-BR-055.
- SME-035: Motor and house policies are stored with whatever premium the caller supplies. Is the premium meant to be calculated somewhere else before this step, or is it intended that the caller supplies it? (Underwriting / pricing lead) On ADPLM-BR-056.
- SME-036: When a commercial policy is added, what do its status codes mean (for example, 0 = accepted and anything else = rejected)? Are the premiums for each peril calculated earlier, by the caller or another program, rather than at this step? (Commercial underwriting SME) On ADPLM-BR-058.
- DEF-003: Is this intended? The only caller in the source (LGAPOL01) always links with a length of 32500, so the request is always treated as carrying 32348 bytes of padding; that is moved into a 3900-byte work field (WS-VARY-CHAR), overrunning it, and the no-padding insert can never be chosen on that path. (Subject-matter expert) On ADPLM-BR-053, ADPLM-BR-054.
- DEF-024: Confirm this is deliberate: Return code '90' is set before the abend, but the abend ends the task so the caller never receives it, and the RETURN after each abend can never run. (Subject-matter expert) On ADPLM-BR-055.

### Decision table gaps

None.
