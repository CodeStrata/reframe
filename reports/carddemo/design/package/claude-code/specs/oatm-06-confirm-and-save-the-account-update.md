# Confirm and save the account update (OATM-C06)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Lets the operator confirm validated changes and saves them to the account and customer records. The save goes through only if nobody else has changed those records since they were shown. It must never overwrite another user's update. Every confirmed value, including the account group, must be saved to its own field and never into another field.

**User story:** As an operator, I want to confirm validated changes and have them saved only if nobody else has changed the record meanwhile, so that I do not overwrite another user's update.

## Requirements

### Requirement 1: OATM-REQ-F-059 (business rule)

#### Acceptance criteria

1. When the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation ('N'), and not PF12 after the account details are fetched, the system shall reject the requested key operation and treat the request as Enter, while allowed keys keep their requested operation. (rules OATM-BR-058)
2. GIVEN key pressed: PF5; update state: changes not yet validated (not 'N') WHEN the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation (`'N'`), and not PF12 after the account details are fetched THEN PF5 is not allowed; the request is treated as Enter and the screen is processed again (OATM-C06-AC-01; OATM-BR-058)
3. GIVEN key pressed: PF5; update state: 'N' (changes OK, awaiting confirmation) WHEN the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation (`'N'`), and not PF12 after the account details are fetched THEN PF5 is valid and the save goes ahead (OATM-C06-AC-02; OATM-BR-058)
4. GIVEN key pressed: PF12; account details: not yet fetched WHEN the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation (`'N'`), and not PF12 after the account details are fetched THEN PF12 is not allowed; the request is treated as Enter (OATM-C06-AC-03; OATM-BR-058)

### Requirement 2: OATM-REQ-F-060 (error handling)

#### Acceptance criteria

1. If any stored account or customer value differs from the value fetched when the details were shown, then the system shall flag 'Record changed by some one else. Please review' and stop the save. (rules OATM-BR-059)
2. GIVEN credit limit when details were shown: 5000.00; credit limit in file at save (PF5): 7000.00 WHEN any stored account or customer value differs from the value fetched when the details were shown THEN Save stops, nothing is rewritten, the details are shown again with 'Record changed by some one else. Please review' (OATM-C06-AC-04; OATM-BR-059)
3. GIVEN customer last name when shown: SMITH; customer last name in file at save: smith WHEN any stored account or customer value differs from the value fetched when the details were shown THEN Treated as unchanged (case is ignored) and the save continues (OATM-C06-AC-05; OATM-BR-059)
4. GIVEN all account and customer values: same as when shown WHEN any stored account or customer value differs from the value fetched when the details were shown THEN Save continues to rewrite the account and customer records (OATM-C06-AC-06; OATM-BR-059)

### Requirement 3: OATM-REQ-F-061 (design note)

#### Acceptance criteria

1. When a confirmed account update is saved, the system shall rewrite the account record from a layout that has no ZIP field, so that the entered account group ID goes into the stored ZIP position (offsets 103-112) and the stored group-ID position is overwritten with whatever the unset filler area holds. (rules OATM-BR-060)
2. GIVEN account 00000000099 has stored ZIP and account group values, and the operator has changed the account group to 'GOLDGROUP1' and confirmed the update WHEN the update is saved THEN legacy behaviour to reconcile against: the stored ZIP position (offsets 103-112) holds 'GOLDGROUP1', and the stored group-ID position holds the content of the unset filler area instead of the entered group (OATM-C06-AC-07; OATM-BR-060)

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
| Save changes | **primary button** | Runs every check; with no change shows 'No change detected with respect to values fetched.' and saves nothing; when all checks pass, a confirmation dialog lists each change (old to new) with Confirm and Cancel; success shows 'Changes committed to database' and the account returns to view | If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved. |  | OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061 |


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
| OATM-BR-058 | Restrict permitted keys by update state | business rule | WHEN the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation (`'N'`), and not PF12 after the account details are fetched, THE Account Update Key Permission SHALL reject the requested key operation and treat the request as Enter; allowed keys are marked valid and keep their requested operation | medium | app/cbl/COACTUPC.cbl:898-899,905-912,914-916, app/cbl/COACTUPC.cbl:905-959 |
| OATM-BR-059 | Detect changes made by another user | error handling | IF any stored account or customer value differs from the value fetched when the details were shown, THEN THE Account Update Concurrency Check SHALL flag 'Record changed by some one else. Please review' and stop the save | medium | app/cbl/COACTUPC.cbl:4109,4115,4117,4119,4121,4123,4125,4127-4129,4131-4133,4135-4137,4139-4145,4152-4179,4181-4191, app/cbl/COACTUPC.cbl:4109-4192 |
| OATM-BR-060 | Persisted record formatting and account record layout | design note | WHEN a confirmed account update is saved, THE account update program SHALL rewrite the account record from a layout that has no ZIP field, so the account group ID entered goes into the stored ZIP position (offsets 103-112), and the stored group-ID position is overwritten with whatever the unset filler area holds. | medium | app/cbl/COACTUPC.cbl:418-433, app/cpy/CVACT01Y.cpy:4-16, app/cbl/COACTUPC.cbl:3956, app/cbl/COACTUPC.cbl:4002 |

### Worked examples

- OATM-BR-058: key pressed = PF5; update state = changes not yet validated (not 'N') → PF5 is not allowed; the request is treated as Enter and the screen is processed again
- OATM-BR-058: key pressed = PF5; update state = 'N' (changes OK, awaiting confirmation) → PF5 is valid and the save goes ahead
- OATM-BR-058: key pressed = PF12; account details = not yet fetched → PF12 is not allowed; the request is treated as Enter
- OATM-BR-059: credit limit when details were shown = 5000.00; credit limit in file at save (PF5) = 7000.00 → Save stops, nothing is rewritten, the details are shown again with 'Record changed by some one else. Please review'
- OATM-BR-059: customer last name when shown = SMITH; customer last name in file at save = smith → Treated as unchanged (case is ignored) and the save continues
- OATM-BR-059: all account and customer values = same as when shown → Save continues to rewrite the account and customer records

## Decision tables

None.

## Design notes

- OATM-BR-060: This is a layout defect in the legacy program: it writes the account through a layout that has no ZIP field, so the account group lands in the ZIP position and the group field gets filler. The new account record must keep ZIP and account group as separate named fields and save each confirmed value to its own field. The acceptance criterion above only records the legacy result for reconciliation. The business owner must decide whether to keep it before anyone treats it as required. Data migration should expect ZIP values on rewritten accounts that are really group IDs.

## Open questions

- SME-062: What should the account update screen do in each of these cases: exit (PF3), first entry before any details are fetched, arriving from the menu, a completed save, a failed save, cancel (PF12), details shown, and answering 'N' to confirmation (PF5)? (Business analyst) On OATM-BR-058.
- SME-066: When account update saves changes, the account record is written before the customer record. Must both be saved together, so that if the customer save fails the account change is rolled back? How critical is this, given it changes balances, limits and regulated customer data? (Account servicing SME / architecture team) On OATM-BR-059.
- DEF-159: Is this intended? The account update record layout leaves out the account ZIP field, so every save shifts the group ID into the ZIP position and overwrites the real group ID with filler. The next read then shows a wrong group ID, and the account ZIP is lost. (Subject-matter expert) On OATM-BR-060.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).
