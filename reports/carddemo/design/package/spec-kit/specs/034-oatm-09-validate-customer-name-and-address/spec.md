# Feature specification: Validate customer name and address

**Feature:** OATM-C09 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C09)

As an operator, I want customer names and address details checked when I change them, so that only well-formed and consistent names and addresses are saved.

Checks the customer's names, address line 1, city, state, ZIP and country when the operator changes details, including that the state is a valid US state code and matches the ZIP prefix. Middle name and address line 2 are optional. It must never save a missing required name or address part, non-letter characters in names, or a state and ZIP that do not belong together.

**Acceptance scenarios:**

1. **Given** Middle name entry: *, **when** the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, or EFT account id on the account update screen, **then** The middle name is treated as not supplied (OATM-C09-AC-01)
2. **Given** ZIP entered: 10001, **when** the operator enters '*' or leaves the state or the ZIP code blank on the account update screen, **then** ZIP 10001 is taken for editing (OATM-C09-AC-02)
3. **Given** Last name: Van Dyke, **when** a supplied first name, last name, city, state or country contains any character other than the letters A-Z or a-z and spaces, **then** Accepted (OATM-C09-AC-03)
4. **Given** Middle name: (blank), **when** the middle name is left blank, **then** Accepted (OATM-C09-AC-04)
5. **Given** Address line 1: 12-B Main St., **when** address line 1 is not supplied, **then** Accepted (OATM-C09-AC-05)
6. **Given** State: XX, **when** the state passes the letters-only check but is not a valid US state code, **then** Rejected as an invalid state (OATM-C09-AC-06)
7. **Given** State: TX, **when** the state passes the letters-only check but is not a valid US state code, **then** Accepted (OATM-C09-AC-07)
8. **Given** State: NY, **when** the state entered is present and alphabetic but is not one of the valid US state codes, **then** State accepted by this check (OATM-C09-AC-08)
9. **Given** State: NY; ZIP: 10001, **when** both the state and the ZIP code have passed their own edits, **then** 'NY10' is a valid combination; the address passes the cross-check (OATM-C09-AC-09)
10. **Given** State: XX; ZIP: 90210, **when** both the state and the ZIP code have passed their own edits, **then** Cross-check is not performed because the state already failed its own edit (OATM-C09-AC-10)
11. **Given** State: NY; ZIP: 90210, **when** the state and first two ZIP digits are not a valid combination, **then** Change rejected with 'Invalid zip code for state'; state and ZIP both flagged (OATM-C09-AC-11)
12. **Given** a fetched account is shown and the operator changes details and clears the First Name, **when** the changes are validated, **then** the input is rejected with 'First Name must be supplied.' and the First Name field is marked blank ('B') (OATM-C09-AC-12)
13. **Given** a fetched account is shown, all earlier fields are valid, and the operator enters '*' as the City, **when** the changes are validated, **then** the input is rejected with 'City must be supplied.' and the City field is marked blank ('B') (OATM-C09-AC-13)
14. **Given** a changed account where all earlier fields are valid and the ZIP is blank, **when** the changes are validated, **then** the input is rejected with 'ZIP must be supplied.' and the ZIP is flagged 'B' (OATM-C09-AC-14)
15. **Given** a changed account where all earlier fields are valid and the ZIP is '12A45', **when** the changes are validated, **then** the input is rejected with '<field> must be all numeric.' naming the ZIP field and the ZIP is flagged '0' (OATM-C09-AC-15)
16. **Given** a changed account where all earlier fields are valid and the ZIP is '00000', **when** the changes are validated, **then** the input is rejected with '<field> must not be zero.' naming the ZIP field and the ZIP is flagged '0' (OATM-C09-AC-16)

## Requirements

### Functional requirements

- **OATM-REQ-F-073** (design note): When the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, state, ZIP code or EFT account id, the system shall treat that entry as not supplied, and otherwise take the entered value as the proposed new value, holding the city as address line 3. Rules: OATM-BR-074, OATM-BR-075.
- **OATM-REQ-F-074** (business rule): If the first name, last name, city, state or country is not supplied after the operator changes account or customer details, then the system shall reject the input with '<field> must be supplied.' (for example 'First Name must be supplied.') and mark the field blank ('B'). Rules: OATM-BR-076.
- **OATM-REQ-F-075** (business rule): If a supplied first name, last name, city, state or country contains any character other than the letters A-Z or a-z and spaces, then the system shall reject it with '<field> can have alphabets only.' and mark the field invalid ('0'). Rules: OATM-BR-077.
- **OATM-REQ-F-076** (business rule): If a supplied middle name contains anything other than letters and spaces, then the system shall reject it with 'Middle Name can have alphabets only.', and the system shall accept a blank middle name. Rules: OATM-BR-078.
- **OATM-REQ-F-077** (business rule): If address line 1 is not supplied, then the system shall reject the input with 'Address Line 1 must be supplied.' and mark it blank ('B'), accepting any other content and not checking address line 2 at all. Rules: OATM-BR-079.
- **OATM-REQ-F-078** (business rule): If the state is present and passes the letters-only check but is not one of the valid US state codes, then the system shall reject the change, flag the state as in error, and show 'State: is not a valid state code' if no earlier error message has been set. Rules: OATM-BR-080, OATM-BR-081.
- **OATM-REQ-F-079** (business rule): If the ZIP code (5 positions) is blank, not all digits, or zero, then the system shall reject it with 'ZIP must be supplied.' (flag 'B'), '<field> must be all numeric.' (flag '0') or '<field> must not be zero.' (flag '0') respectively. Rules: OATM-BR-082.
- **OATM-REQ-F-080** (business rule): When both the state and the ZIP code have passed their own edits, the system shall check that the state together with the first two digits of the ZIP code is a known valid state/ZIP-prefix combination. Rules: OATM-BR-083.
- **OATM-REQ-F-081** (business rule): If the state and first two ZIP digits are not a valid combination, then the system shall reject the change, flag both the state and the ZIP code as in error, and show 'Invalid zip code for state' if no earlier error message has been set. Rules: OATM-BR-084.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-074 | Stage electronic funds transfer account | design note | WHEN the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, or EFT account id on the account update screen, THE account update SHALL treat that entry as not supplied; otherwise it SHALL take the entered value as the proposed new value (the city is held as address line 3). | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-075 | Stage state code entry | design note | WHEN the operator enters '*' or leaves the state or the ZIP code blank on the account update screen, THE account update SHALL treat that field as not supplied (empty); otherwise it SHALL take the value entered for editing. | high | app/cbl/COACTUPC.cbl:1336-1341, app/cbl/COACTUPC.cbl:1350-1355, app/cbl/COACTUPC.cbl:1592-1609, app/cbl/COACTUPC.cbl:1664-1669 |
| OATM-BR-076 | Validate required alphabetic text | business rule | WHEN the first name, last name, city, state or country is not supplied after the operator changes account or customer details, THE account update SHALL reject the input with '<field> must be supplied.' (for example 'First Name must be supplied.') and mark the field blank ('B'). | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-077 | Validate required alphabetic text | business rule | WHEN a supplied first name, last name, city, state or country contains any character other than the letters A-Z or a-z and spaces, THE account update SHALL reject it with '<field> can have alphabets only.' and mark the field invalid ('0'). | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-078 | Validate optional alphabetic text | business rule | WHEN the middle name is left blank, THE account update SHALL accept it; WHEN a supplied middle name contains anything other than letters and spaces, THE account update SHALL reject it with 'Middle Name can have alphabets only.' | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-079 | Require mandatory text present | business rule | WHEN address line 1 is not supplied, THE account update SHALL reject the input with 'Address Line 1 must be supplied.' and mark it blank ('B'); any other content is accepted, and address line 2 is not checked at all. | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-080 | Validate customer names and address | business rule | WHEN the state passes the letters-only check but is not a valid US state code, THE account update SHALL reject it. | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-081 | Validate US state code | business rule | WHEN the state entered is present and alphabetic but is not one of the valid US state codes, THE account update SHALL reject the change, flag the state as in error, and show 'State: is not a valid state code' if no earlier error message has been set. | high | app/cbl/COACTUPC.cbl:1336-1341, app/cbl/COACTUPC.cbl:1350-1355, app/cbl/COACTUPC.cbl:1592-1609, app/cbl/COACTUPC.cbl:1664-1669 |
| OATM-BR-082 | Validate required non-zero numeric value | business rule | WHEN the ZIP code (5 positions) or the EFT account id (10 positions) is checked, THE account update SHALL reject a blank value with '<field> must be supplied.' (flag 'B'), a value that is not all digits with '<field> must be all numeric.' (flag '0'), and a zero value with '<field> must not be zero.' (flag '0'). | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-083 | Cross-check state against ZIP | business rule | WHEN both the state and the ZIP code have passed their own edits, THE account update SHALL check that the state together with the first two digits of the ZIP code is a known valid state/ZIP-prefix combination. | high | app/cbl/COACTUPC.cbl:1336-1341, app/cbl/COACTUPC.cbl:1350-1355, app/cbl/COACTUPC.cbl:1592-1609, app/cbl/COACTUPC.cbl:1664-1669 |
| OATM-BR-084 | Validate state and ZIP consistency | business rule | WHEN the state and first two ZIP digits are not a valid combination, THE account update SHALL reject the change, flag both the state and the ZIP code as in error, and show 'Invalid zip code for state' if no earlier error message has been set. | high | app/cbl/COACTUPC.cbl:1336-1341, app/cbl/COACTUPC.cbl:1350-1355, app/cbl/COACTUPC.cbl:1592-1609, app/cbl/COACTUPC.cbl:1664-1669 |

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

- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-074, OATM-BR-075.
- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-077, OATM-BR-078, OATM-BR-079, OATM-BR-082, OATM-BR-081, OATM-BR-084.
- SME-058: Please supply the complete, authoritative list of valid state and ZIP-prefix combinations. Is this rough check enough, or is a finer-grained address check required? (Data governance team) On OATM-BR-081, OATM-BR-083, OATM-BR-084.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-077, OATM-BR-078, OATM-BR-079, OATM-BR-082, OATM-BR-081, OATM-BR-084.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-077, OATM-BR-078, OATM-BR-079, OATM-BR-082, OATM-BR-081, OATM-BR-084.
- DEF-038: Confirm this is deliberate: The name, city, state and country fields accept only the letters A-Z and a-z and spaces. Real names and places with apostrophes, hyphens or periods ('O'Brien', 'St. Louis') are rejected. Separately, the blank-phone check tests the area-code part twice where it should test the line-number part. (Subject-matter expert) On OATM-BR-074, OATM-BR-077, OATM-BR-078, OATM-BR-079, OATM-BR-082.
- DEF-043: Confirm this is deliberate: The ZIP check only compares the first two ZIP digits with the state, so a ZIP in the wrong area of a valid prefix is accepted; the code comment calls it a crude edit, so this looks intended. (Subject-matter expert) On OATM-BR-075, OATM-BR-081, OATM-BR-083, OATM-BR-084.

### Decision table gaps

None.
