# Design: Confirm and save the account update (OATM-C06)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Lets the operator confirm validated changes and saves them to the account and customer records, but only if nobody else has changed those records since they were fetched. Only the keys allowed at each stage take effect; anything else is treated as Enter. It must never overwrite another user's update, and the legacy save places the account group into the stored ZIP position, which the new design must deliberately decide whether to keep.

Runs as online. Journeys: J02.

## Screens and components

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Save these changes? | dialog | Each changed field with its old and new value; all fields are locked while it is open |  |  | OATM-REQ-F-059 |
| Save changes | button | Saves the account and customer together, or neither | If the stored record changed since it was fetched: 'Record changed by some one else. Please review' and nothing is saved. |  | OATM-REQ-F-060 |


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

- OATM-BR-060: The legacy save writes the account from a layout without a ZIP field, so the entered group lands in the stored ZIP position (offsets 103-112) and the group field gets unset filler. The new account store should have distinct group and ZIP columns; whether to reproduce this shift for data compatibility (e.g. while the legacy file is still read by other jobs) or correct it is a decision to record, and any migration must account for existing records with the group in the ZIP position.

## Open questions

- SME-062: What should the account update screen do in each of these cases: exit (PF3), first entry before any details are fetched, arriving from the menu, a completed save, a failed save, cancel (PF12), details shown, and answering 'N' to confirmation (PF5)? (Business analyst) On OATM-BR-058.
- SME-066: When account update saves changes, the account record is written before the customer record. Must both be saved together, so that if the customer save fails the account change is rolled back? How critical is this, given it changes balances, limits and regulated customer data? (Account servicing SME / architecture team) On OATM-BR-059.
- DEF-159: Is this intended? The account update record layout leaves out the account ZIP field, so every save shifts the group ID into the ZIP position and overwrites the real group ID with filler. The next read then shows a wrong group ID, and the account ZIP is lost. (Subject-matter expert) On OATM-BR-060.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).