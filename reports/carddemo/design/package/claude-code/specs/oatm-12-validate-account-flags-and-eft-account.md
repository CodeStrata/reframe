# Validate account flags and EFT account (OATM-C12)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Checks the account status and the primary card holder indicator, each of which must be Y or N. It also checks the electronic funds transfer (EFT) account id, which must be 10 non-zero digits. A blank or '*' entry is not supplied and is rejected. A flag other than Y or N, or a malformed transfer account, must never be saved.

**User story:** As an operator, I want the account status, primary card holder indicator and EFT account id checked, so that only valid flags and a well-formed funds transfer account are saved.

## Requirements

### Requirement 1: OATM-REQ-F-103 (design note)

#### Acceptance criteria

1. When the operator submits account changes and leaves the Account Status or Primary Card Holder entry blank or as '*', the system shall treat that entry as not supplied (low-values) rather than as a value to save. (rules OATM-BR-107)
2. GIVEN Account Status entry: '*' WHEN the operator submits account changes and leaves the Account Status or Primary Card Holder entry blank or as '*' THEN Account Status is treated as not supplied (OATM-C12-AC-01; OATM-BR-107)
3. GIVEN Primary Card Holder entry: 'Y' WHEN the operator submits account changes and leaves the Account Status or Primary Card Holder entry blank or as '*' THEN 'Y' is taken as the proposed Primary Card Holder value (OATM-C12-AC-02; OATM-BR-107)

### Requirement 2: OATM-REQ-F-104 (business rule)

#### Acceptance criteria

1. If changed account details are validated and the Account Status or Primary Card Holder value is not supplied (blank, low-values or '0'), then the system shall reject the input with '<field> must be supplied.' (e.g. 'Account Status must be supplied.', 'Primary Card Holder must be supplied.') and place the cursor on that field. (rules OATM-BR-108, OATM-BR-087)
2. GIVEN Phone number 2: (blank) WHEN account update runs THEN Accepted (OATM-C12-AC-03; OATM-BR-087)

### Requirement 3: OATM-REQ-F-105 (business rule)

#### Acceptance criteria

1. If changed account details are validated and a supplied Account Status or Primary Card Holder value is anything other than 'Y' or 'N', then the system shall reject the input with '<field> must be Y or N.' (e.g. 'Account Status must be Y or N.', 'Primary Card Holder must be Y or N.') and place the cursor on that field. (rules OATM-BR-109, OATM-BR-087)
2. GIVEN Phone number 2: (blank) WHEN account update runs THEN Accepted (OATM-C12-AC-03; OATM-BR-087)
3. GIVEN Account Status: 'N' WHEN changed account details are validated and a supplied Account Status or Primary Card Holder value is anything other than 'Y' or 'N' THEN Accepted (OATM-C12-AC-04; OATM-BR-109)

### Requirement 4: OATM-REQ-F-106 (business rule)

#### Acceptance criteria

1. If the EFT account id (10 positions) is blank, not all digits, or zero, then the system shall reject it with '<field> must be supplied.' (flag 'B'), '<field> must be all numeric.' (flag '0') or '<field> must not be zero.' (flag '0') respectively. (rules OATM-BR-082, OATM-BR-074)
2. GIVEN Middle name entry: * WHEN the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, or EFT account id on the account update screen THEN The middle name is treated as not supplied (OATM-C12-AC-05; OATM-BR-074)

## Screens and components

### Account (S-ACCOUNT-VIEW)

Look up an account by account number or card number and show its status, balances, limits and dates beside the customer profile on one screen, while the caller waits. Tab order: search, the cards, then Update account.

Prototype: `ui-reference/index.html#/S-ACCOUNT-VIEW`. Replaces the legacy screens CACTVWA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Update account (S-ACCOUNT-EDIT)

Change an account's and its customer's details after confirming the caller. Each field is checked as it is left and again on save; every failing field shows its own message and a summary lists them all. Save asks for confirmation, listing each change from old to new value. Tab order: account and status, dates, amounts, customer identity, name and address, contact, then Save changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Status and group | **summary card** | Account status as a choice of Active or Inactive (stored Y/N); Account group (optional, up to 10 characters) | Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values. |  | OATM-REQ-F-103, OATM-REQ-F-104, OATM-REQ-F-105 |
| Name and address | **summary card** | First name, Middle name (optional), Last name; Address line 1, Address line 2 (optional); City; State (a choice of US state codes); ZIP; Country | '<field> must be supplied.' for First Name, Last Name, City, State, Country and Address Line 1; '<field> can have alphabets only.' for names, city, state and country; 'Middle Name can have alphabets only.'; 'State: is not a valid state code'; ZIP: 'ZIP must be supplied.', must be all numeric, 5 digits and not zero; 'Invalid zip code for state' - check the state and ZIP together. |  |  |
| Phone and payments | **summary card** | Phone 1 and Phone 2 (optional), each as labelled Area code, Prefix and Line number; EFT account ID; Primary card holder as a choice of Yes or No | A phone may be left wholly blank; otherwise '<Phone Number 1 or 2>: Area code must be supplied.', ': Area code must be A 3 digit number.', ': Area code cannot be zero', ': Not valid North America general purpose area code' (from the list of general-purpose codes), ': Prefix code must be supplied.', ': Prefix code must be A 3 digit number.', ': Prefix code cannot be zero', ': Line number code must be supplied.', ': Line number code must be A 4 digit number.', ': Line number code cannot be zero'. EFT account ID: 'EFT Account Id must be supplied.', all numeric, 10 digits, not zero. Primary card holder: 'Primary Card Holder must be supplied.' and must be Yes or No ('must be Y or N.'). |  | OATM-REQ-F-106 |


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
| OATM-BR-107 | Stage entered account active status | design note | WHEN the operator submits account changes and leaves the Account Status or Primary Card Holder entry blank or as '*', THE Account Update screen SHALL treat that entry as not supplied (low-values) rather than as a value to save. | high | app/cbl/COACTUPC.cbl:1064-1070, app/cbl/COACTUPC.cbl:1419-1424, app/cbl/COACTUPC.cbl:1458-1476, app/cbl/COACTUPC.cbl:1657-1662 |
| OATM-BR-108 | Validate yes or no indicator | business rule | WHEN changed account details are validated and the Account Status or Primary Card Holder value is not supplied (blank, low-values or '0'), THE Account Update screen SHALL reject the input with '<field> must be supplied.' (e.g. 'Account Status must be supplied.') and place the cursor on that field. | high | app/cbl/COACTUPC.cbl:1064-1070, app/cbl/COACTUPC.cbl:1419-1424, app/cbl/COACTUPC.cbl:1458-1476, app/cbl/COACTUPC.cbl:1657-1662 |
| OATM-BR-087 | Validate phones, EFT id and holder flag | business rule | THE account update SHALL accept blank phone numbers 1 and 2, edit any phone number that is entered as a North American number, and require the primary card holder indicator, rejecting a blank with 'Primary Card Holder must be supplied.' and any value other than 'Y' or 'N' with 'Primary Card Holder must be Y or N.' | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-109 | Validate yes or no indicator | business rule | WHEN changed account details are validated and a supplied Account Status or Primary Card Holder value is anything other than 'Y' or 'N', THE Account Update screen SHALL reject the input with '<field> must be Y or N.' (e.g. 'Account Status must be Y or N.') and place the cursor on that field. | high | app/cbl/COACTUPC.cbl:1064-1070, app/cbl/COACTUPC.cbl:1419-1424, app/cbl/COACTUPC.cbl:1458-1476, app/cbl/COACTUPC.cbl:1657-1662 |
| OATM-BR-082 | Validate required non-zero numeric value | business rule | WHEN the ZIP code (5 positions) or the EFT account id (10 positions) is checked, THE account update SHALL reject a blank value with '<field> must be supplied.' (flag 'B'), a value that is not all digits with '<field> must be all numeric.' (flag '0'), and a zero value with '<field> must not be zero.' (flag '0'). | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-074 | Stage electronic funds transfer account | design note | WHEN the operator enters '*' or leaves blank the first, middle or last name, address line 1 or 2, city, or EFT account id on the account update screen, THE account update SHALL treat that entry as not supplied; otherwise it SHALL take the entered value as the proposed new value (the city is held as address line 3). | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |

### Worked examples

- OATM-BR-107: Account Status entry = '*' → Account Status is treated as not supplied
- OATM-BR-107: Primary Card Holder entry = 'Y' → 'Y' is taken as the proposed Primary Card Holder value
- OATM-BR-087: Phone number 2 = (blank) → Accepted
- OATM-BR-109: Account Status = 'N' → Accepted
- OATM-BR-074: Middle name entry = * → The middle name is treated as not supplied

## Decision tables

#### Account Status and Primary Card Holder checks

| Value supplied | Value is 'Y' or 'N' | Validation result | Rule |
|---|---|---|---|
| No (blank, low-values or '0') | - | Reject with '<field> must be supplied.', cursor on field | OATM-BR-108 |
| Yes | No | Reject with '<field> must be Y or N.', cursor on field | OATM-BR-109 |
| No (blank) | - | Reject with 'Primary Card Holder must be supplied.' | OATM-BR-087 |


## Design notes

- OATM-BR-107: Treat blank or '*' entries for Account Status and Primary Card Holder as absent (null), never as a value to save. Validation then rejects an absent or non-Y/N value. Store each flag as a two-valued field (Y/N or boolean).
- OATM-BR-074: Treat a blank or '*' EFT account id as absent (null); otherwise it is the proposed value for the 10-digit supplied, numeric and non-zero checks. Store it as a 10-character digit string so leading zeros are kept.

## Open questions

- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-074, OATM-BR-107.
- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-082, OATM-BR-109.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-082, OATM-BR-109.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-082, OATM-BR-109.
- DEF-038: Confirm this is deliberate: The name, city, state and country fields accept only the letters A-Z and a-z and spaces. Real names and places with apostrophes, hyphens or periods ('O'Brien', 'St. Louis') are rejected. Separately, the blank-phone check tests the area-code part twice where it should test the line-number part. (Subject-matter expert) On OATM-BR-074, OATM-BR-082.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).
