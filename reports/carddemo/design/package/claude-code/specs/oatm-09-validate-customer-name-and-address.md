# Validate customer name and address (OATM-C09)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Checks the customer's names, address line 1, city, state, ZIP and country when the operator changes details, including that the state is a valid US state code and matches the ZIP prefix. Middle name and address line 2 are optional. It must never save a missing required name or address part, non-letter characters in names, or a state and ZIP that do not belong together.

**User story:** As an operator, I want customer names and address details checked when I change them, so that only well-formed and consistent names and addresses are saved.

## Requirements

### Requirement 1: OATM-REQ-F-073 (design note)

#### Acceptance criteria

1. When the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, state, ZIP code or EFT account id, the system shall treat that entry as not supplied, and otherwise take the entered value as the proposed new value, holding the city as address line 3. (rules OATM-BR-074, OATM-BR-075)
2. GIVEN Middle name entry: * WHEN the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, or EFT account id on the account update screen THEN The middle name is treated as not supplied (OATM-C09-AC-01; OATM-BR-074)
3. GIVEN ZIP entered: 10001 WHEN the operator enters '*' or leaves the state or the ZIP code blank on the account update screen THEN ZIP 10001 is taken for editing (OATM-C09-AC-02; OATM-BR-075)

### Requirement 2: OATM-REQ-F-074 (business rule)

#### Acceptance criteria

1. If the first name, last name, city, state or country is not supplied after the operator changes account or customer details, then the system shall reject the input with '<field> must be supplied.' (for example 'First Name must be supplied.') and mark the field blank ('B'). (rules OATM-BR-076)
2. GIVEN a fetched account is shown and the operator changes details and clears the First Name WHEN the changes are validated THEN the input is rejected with 'First Name must be supplied.' and the First Name field is marked blank ('B') (OATM-C09-AC-12; OATM-BR-076)
3. GIVEN a fetched account is shown, all earlier fields are valid, and the operator enters '*' as the City WHEN the changes are validated THEN the input is rejected with 'City must be supplied.' and the City field is marked blank ('B') (OATM-C09-AC-13; OATM-BR-076)

### Requirement 3: OATM-REQ-F-075 (business rule)

#### Acceptance criteria

1. If a supplied first name, last name, city, state or country contains any character other than the letters A-Z or a-z and spaces, then the system shall reject it with '<field> can have alphabets only.' and mark the field invalid ('0'). (rules OATM-BR-077)
2. GIVEN Last name: Van Dyke WHEN a supplied first name, last name, city, state or country contains any character other than the letters A-Z or a-z and spaces THEN Accepted (OATM-C09-AC-03; OATM-BR-077)

### Requirement 4: OATM-REQ-F-076 (business rule)

#### Acceptance criteria

1. If a supplied middle name contains anything other than letters and spaces, then the system shall reject it with 'Middle Name can have alphabets only.', and the system shall accept a blank middle name. (rules OATM-BR-078)
2. GIVEN Middle name: (blank) WHEN the middle name is left blank THEN Accepted (OATM-C09-AC-04; OATM-BR-078)

### Requirement 5: OATM-REQ-F-077 (business rule)

#### Acceptance criteria

1. If address line 1 is not supplied, then the system shall reject the input with 'Address Line 1 must be supplied.' and mark it blank ('B'), accepting any other content and not checking address line 2 at all. (rules OATM-BR-079)
2. GIVEN Address line 1: 12-B Main St. WHEN address line 1 is not supplied THEN Accepted (OATM-C09-AC-05; OATM-BR-079)

### Requirement 6: OATM-REQ-F-078 (business rule)

#### Acceptance criteria

1. If the state is present and passes the letters-only check but is not one of the valid US state codes, then the system shall reject the change, flag the state as in error, and show 'State: is not a valid state code' if no earlier error message has been set. (rules OATM-BR-080, OATM-BR-081)
2. GIVEN State: XX WHEN the state passes the letters-only check but is not a valid US state code THEN Rejected as an invalid state (OATM-C09-AC-06; OATM-BR-080)
3. GIVEN State: TX WHEN the state passes the letters-only check but is not a valid US state code THEN Accepted (OATM-C09-AC-07; OATM-BR-080)
4. GIVEN State: NY WHEN the state entered is present and alphabetic but is not one of the valid US state codes THEN State accepted by this check (OATM-C09-AC-08; OATM-BR-081)

### Requirement 7: OATM-REQ-F-079 (business rule)

#### Acceptance criteria

1. If the ZIP code (5 positions) is blank, not all digits, or zero, then the system shall reject it with 'ZIP must be supplied.' (flag 'B'), '<field> must be all numeric.' (flag '0') or '<field> must not be zero.' (flag '0') respectively. (rules OATM-BR-082)
2. GIVEN a changed account where all earlier fields are valid and the ZIP is blank WHEN the changes are validated THEN the input is rejected with 'ZIP must be supplied.' and the ZIP is flagged 'B' (OATM-C09-AC-14; OATM-BR-082)
3. GIVEN a changed account where all earlier fields are valid and the ZIP is '12A45' WHEN the changes are validated THEN the input is rejected with '<field> must be all numeric.' naming the ZIP field and the ZIP is flagged '0' (OATM-C09-AC-15; OATM-BR-082)
4. GIVEN a changed account where all earlier fields are valid and the ZIP is '00000' WHEN the changes are validated THEN the input is rejected with '<field> must not be zero.' naming the ZIP field and the ZIP is flagged '0' (OATM-C09-AC-16; OATM-BR-082)

### Requirement 8: OATM-REQ-F-080 (business rule)

#### Acceptance criteria

1. When both the state and the ZIP code have passed their own edits, the system shall check that the state together with the first two digits of the ZIP code is a known valid state/ZIP-prefix combination. (rules OATM-BR-083)
2. GIVEN State: NY; ZIP: 10001 WHEN both the state and the ZIP code have passed their own edits THEN 'NY10' is a valid combination; the address passes the cross-check (OATM-C09-AC-09; OATM-BR-083)
3. GIVEN State: XX; ZIP: 90210 WHEN both the state and the ZIP code have passed their own edits THEN Cross-check is not performed because the state already failed its own edit (OATM-C09-AC-10; OATM-BR-083)

### Requirement 9: OATM-REQ-F-081 (business rule)

#### Acceptance criteria

1. If the state and first two ZIP digits are not a valid combination, then the system shall reject the change, flag both the state and the ZIP code as in error, and show 'Invalid zip code for state' if no earlier error message has been set. (rules OATM-BR-084)
2. GIVEN State: NY; ZIP: 90210 WHEN the state and first two ZIP digits are not a valid combination THEN Change rejected with 'Invalid zip code for state'; state and ZIP both flagged (OATM-C09-AC-11; OATM-BR-084)

## Screens and components

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| First name | text |  | Required: 'First Name must be supplied.'; letters and spaces only: 'First Name can have alphabets only.'. |  | OATM-REQ-F-073, OATM-REQ-F-074 |
| Middle name (optional) | text |  | Optional; letters and spaces only: 'Middle Name can have alphabets only.'. |  | OATM-REQ-F-076 |
| Last name | text |  | Required: 'Last Name must be supplied.'; letters and spaces only: 'Last Name can have alphabets only.'. |  | OATM-REQ-F-074, OATM-REQ-F-075 |
| Address line 1 | text |  | Required: 'Address Line 1 must be supplied.' |  | OATM-REQ-F-077 |
| City | text |  | Required: 'City must be supplied.'; letters and spaces only: 'City can have alphabets only.'. |  | OATM-REQ-F-074, OATM-REQ-F-075 |
| State | select | US state codes | Required: 'State must be supplied.'; letters and spaces only: 'State can have alphabets only.'. Must be a US state code: 'State: is not a valid state code'; must match the ZIP code: 'Invalid zip code for state'. |  | OATM-REQ-F-078, OATM-REQ-F-081 |
| ZIP code | text |  | Required: 'Zip must be supplied.'; 5 digits: 'Zip must be all numeric.'; not zero: 'Zip must not be zero.'; its first two digits must belong to the chosen state: 'Invalid zip code for state'. |  | OATM-REQ-F-079, OATM-REQ-F-080, OATM-REQ-F-081 |
| EFT account ID | text |  | Required: 'EFT Account Id must be supplied.'; 10 digits: 'EFT Account Id must be all numeric.'; not zero: 'EFT Account Id must not be zero.' |  |  |


## Data models

#### CSMSG02Y

File record of COACTUPC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

#### CVACT01Y

File record of COACTUPC. Source: `app/cpy/CVACT01Y.cpy`.

Record `ACCOUNT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| ACCT-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| ACCT-CURR-BAL |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CASH-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-OPEN-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-REISSUE-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-CURR-CYC-CREDIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CURR-CYC-DEBIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| ACCT-GROUP-ID |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(178) | text, 178 characters |  |  |  |

#### CVACT03Y

File record of COACTUPC. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCUS01Y

File record of COACTUPC. Source: `app/cpy/CVCUS01Y.cpy`.

Record `CUSTOMER-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-FIRST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-MIDDLE-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-LAST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-ADDR-LINE-1 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-2 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-3 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-STATE-CD |  | X(02) | text, 2 characters |  |  |  |
| CUST-ADDR-COUNTRY-CD |  | X(03) | text, 3 characters |  |  |  |
| CUST-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| CUST-PHONE-NUM-1 |  | X(15) | text, 15 characters |  |  |  |
| CUST-PHONE-NUM-2 |  | X(15) | text, 15 characters |  |  |  |
| CUST-SSN |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-GOVT-ISSUED-ID |  | X(20) | text, 20 characters |  |  |  |
| CUST-DOB-YYYY-MM-DD |  | X(10) | text, 10 characters |  |  |  |
| CUST-EFT-ACCOUNT-ID |  | X(10) | text, 10 characters |  |  |  |
| CUST-PRI-CARD-HOLDER-IND |  | X(01) | text, 1 character |  |  |  |
| CUST-FICO-CREDIT-SCORE |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| FILLER |  | X(168) | text, 168 characters |  |  |  |

- COCOM01Y (working storage of COACTUPC): see data-contracts.md.
- COTTL01Y (working storage of COACTUPC): see data-contracts.md.
- CSDAT01Y (working storage of COACTUPC): see data-contracts.md.
- CSLKPCDY (working storage of COACTUPC): see data-contracts.md.
- CSMSG01Y (working storage of COACTUPC): see data-contracts.md.
- CSSETATY (working storage of COACTUPC): see data-contracts.md.
- CSSTRPFY (working storage of COACTUPC): see data-contracts.md.
- CSUSR01Y (working storage of COACTUPC): see data-contracts.md.
- CSUTLDPY (working storage of COACTUPC): see data-contracts.md.
- CSUTLDWY (working storage of COACTUPC): see data-contracts.md.
- CVCRD01Y (working storage of COACTUPC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- OATM-BR-074: Middle name entry = * → The middle name is treated as not supplied
- OATM-BR-075: ZIP entered = 10001 → ZIP 10001 is taken for editing
- OATM-BR-077: Last name = Van Dyke → Accepted
- OATM-BR-078: Middle name = (blank) → Accepted
- OATM-BR-079: Address line 1 = 12-B Main St. → Accepted
- OATM-BR-080: State = XX → Rejected as an invalid state
- OATM-BR-080: State = TX → Accepted
- OATM-BR-081: State = NY → State accepted by this check
- OATM-BR-083: State = NY; ZIP = 10001 → 'NY10' is a valid combination; the address passes the cross-check
- OATM-BR-083: State = XX; ZIP = 90210 → Cross-check is not performed because the state already failed its own edit
- OATM-BR-084: State = NY; ZIP = 90210 → Change rejected with 'Invalid zip code for state'; state and ZIP both flagged

## Decision tables

#### Required alphabetic fields (first name, last name, city, state, country)

| Field supplied | Letters and spaces only | Valid US state code (state only) | Validation result | Rule |
|---|---|---|---|---|
| No | - | - | Reject with '<field> must be supplied.', flag 'B' | OATM-BR-076 |
| Yes | No | - | Reject with '<field> can have alphabets only.', flag '0' | OATM-BR-077 |
| Yes | Yes | No | Reject state, flag it, show 'State: is not a valid state code' if no earlier message | OATM-BR-081 |


## Design notes

- OATM-BR-074: Input binding for first, middle and last name, address lines 1 and 2, city and EFT account id: blank or '*' becomes null; otherwise the value is the proposed new value. The city maps to the customer's third address line in the stored record.
- OATM-BR-075: Input binding for state and ZIP: blank or '*' becomes null (empty); otherwise the entered value goes to the state and ZIP validators.

## Open questions

- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-074, OATM-BR-075.
- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-077, OATM-BR-078, OATM-BR-079, OATM-BR-082, OATM-BR-081, OATM-BR-084.
- SME-058: Please supply the complete, authoritative list of valid state and ZIP-prefix combinations. Is this rough check enough, or is a finer-grained address check required? (Data governance team) On OATM-BR-081, OATM-BR-083, OATM-BR-084.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-077, OATM-BR-078, OATM-BR-079, OATM-BR-082, OATM-BR-081, OATM-BR-084.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-077, OATM-BR-078, OATM-BR-079, OATM-BR-082, OATM-BR-081, OATM-BR-084.
- DEF-038: Confirm this is deliberate: The name, city, state and country fields accept only the letters A-Z and a-z and spaces. Real names and places with apostrophes, hyphens or periods ('O'Brien', 'St. Louis') are rejected. Separately, the blank-phone check tests the area-code part twice where it should test the line-number part. (Subject-matter expert) On OATM-BR-074, OATM-BR-077, OATM-BR-078, OATM-BR-079, OATM-BR-082.
- DEF-043: Confirm this is deliberate: The ZIP check only compares the first two ZIP digits with the state, so a ZIP in the wrong area of a valid prefix is accepted; the code comment calls it a crude edit, so this looks intended. (Subject-matter expert) On OATM-BR-075, OATM-BR-081, OATM-BR-083, OATM-BR-084.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (16 in all).
