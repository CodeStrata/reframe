# Feature specification: Validate account flags and EFT account

**Feature:** OATM-C12 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C12)

As an operator, I want the account status, primary card holder indicator and EFT account id checked, so that only valid flags and a well-formed funds transfer account are saved.

Checks the account status and primary card holder flags and the EFT account id when the operator changes account details. Both flags must be supplied as Y or N, and the EFT account id must be ten digits and not zero. A missing or malformed flag or funds-transfer account must never be saved, and the cursor goes to the field in error.

**Acceptance scenarios:**

1. **Given** Account Status entry: '*', **when** the operator submits account changes and leaves the Account Status or Primary Card Holder entry blank or as '*', **then** Account Status is treated as not supplied (OATM-C12-AC-01)
2. **Given** Primary Card Holder entry: 'Y', **when** the operator submits account changes and leaves the Account Status or Primary Card Holder entry blank or as '*', **then** 'Y' is taken as the proposed Primary Card Holder value (OATM-C12-AC-02)
3. **Given** Phone number 2: (blank), **when** account update runs, **then** Accepted (OATM-C12-AC-03)
4. **Given** Account Status: 'N', **when** changed account details are validated and a supplied Account Status or Primary Card Holder value is anything other than 'Y' or 'N', **then** Accepted (OATM-C12-AC-04)
5. **Given** Middle name entry: *, **when** the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, or EFT account id on the account update screen, **then** The middle name is treated as not supplied (OATM-C12-AC-05)

## Requirements

### Functional requirements

- **OATM-REQ-F-103** (design note): When the operator submits account changes and leaves the Account Status or Primary Card Holder entry blank or as '*', the system shall treat that entry as not supplied (low-values) rather than as a value to save. Rules: OATM-BR-107.
- **OATM-REQ-F-104** (business rule): If changed account details are validated and the Account Status or Primary Card Holder value is not supplied (blank, low-values or '0'), then the system shall reject the input with '<field> must be supplied.' (e.g. 'Account Status must be supplied.', 'Primary Card Holder must be supplied.') and place the cursor on that field. Rules: OATM-BR-108, OATM-BR-087.
- **OATM-REQ-F-105** (business rule): If changed account details are validated and a supplied Account Status or Primary Card Holder value is anything other than 'Y' or 'N', then the system shall reject the input with '<field> must be Y or N.' (e.g. 'Account Status must be Y or N.', 'Primary Card Holder must be Y or N.') and place the cursor on that field. Rules: OATM-BR-109, OATM-BR-087.
- **OATM-REQ-F-106** (business rule): If the EFT account id (10 positions) is blank, not all digits, or zero, then the system shall reject it with '<field> must be supplied.' (flag 'B'), '<field> must be all numeric.' (flag '0') or '<field> must not be zero.' (flag '0') respectively. Rules: OATM-BR-082, OATM-BR-074.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-107 | Stage entered account active status | design note | WHEN the operator submits account changes and leaves the Account Status or Primary Card Holder entry blank or as '*', THE Account Update screen SHALL treat that entry as not supplied (low-values) rather than as a value to save. | high | app/cbl/COACTUPC.cbl:1064-1070, app/cbl/COACTUPC.cbl:1419-1424, app/cbl/COACTUPC.cbl:1458-1476, app/cbl/COACTUPC.cbl:1657-1662 |
| OATM-BR-108 | Validate yes or no indicator | business rule | WHEN changed account details are validated and the Account Status or Primary Card Holder value is not supplied (blank, low-values or '0'), THE Account Update screen SHALL reject the input with '<field> must be supplied.' (e.g. 'Account Status must be supplied.') and place the cursor on that field. | high | app/cbl/COACTUPC.cbl:1064-1070, app/cbl/COACTUPC.cbl:1419-1424, app/cbl/COACTUPC.cbl:1458-1476, app/cbl/COACTUPC.cbl:1657-1662 |
| OATM-BR-087 | Validate phones, EFT id and holder flag | business rule | THE account update SHALL accept blank phone numbers 1 and 2, edit any phone number that is entered as a North American number, and require the primary card holder indicator, rejecting a blank with 'Primary Card Holder must be supplied.' and any value other than 'Y' or 'N' with 'Primary Card Holder must be Y or N.' | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-109 | Validate yes or no indicator | business rule | WHEN changed account details are validated and a supplied Account Status or Primary Card Holder value is anything other than 'Y' or 'N', THE Account Update screen SHALL reject the input with '<field> must be Y or N.' (e.g. 'Account Status must be Y or N.') and place the cursor on that field. | high | app/cbl/COACTUPC.cbl:1064-1070, app/cbl/COACTUPC.cbl:1419-1424, app/cbl/COACTUPC.cbl:1458-1476, app/cbl/COACTUPC.cbl:1657-1662 |
| OATM-BR-082 | Validate required non-zero numeric value | business rule | WHEN the ZIP code (5 positions) or the EFT account id (10 positions) is checked, THE account update SHALL reject a blank value with '<field> must be supplied.' (flag 'B'), a value that is not all digits with '<field> must be all numeric.' (flag '0'), and a zero value with '<field> must not be zero.' (flag '0'). | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-074 | Stage electronic funds transfer account | design note | WHEN the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, or EFT account id on the account update screen, THE account update SHALL treat that entry as not supplied; otherwise it SHALL take the entered value as the proposed new value (the city is held as address line 3). | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |

### Key entities

- CSMSG02Y (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSLKPCDY (working storage)
- CSMSG01Y (working storage)
- CSSETATY (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CSUTLDPY (working storage)
- CSUTLDWY (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-074, OATM-BR-107.
- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-082, OATM-BR-109.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-082, OATM-BR-109.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-082, OATM-BR-109.
- DEF-038: Confirm this is deliberate: The name, city, state and country fields accept only the letters A-Z and a-z and spaces. Real names and places with apostrophes, hyphens or periods ('O'Brien', 'St. Louis') are rejected. Separately, the blank-phone check tests the area-code part twice where it should test the line-number part. (Subject-matter expert) On OATM-BR-074, OATM-BR-082.

### Decision table gaps

None.
