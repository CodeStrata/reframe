# Design: Find the account to update (OATM-C01)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Lets an operator enter an account id and fetches the linked card cross-reference, account and customer records so the details can be reviewed and updated. It records what was fetched as the original snapshot that later change detection and the concurrency check compare against. It must never present or update details for an account or customer that was not actually found, and must stop at the first missing record with the right message.

Runs as online. Journeys: J02.

## Screens and components

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account number | search | 11-digit account number; the only editable field until an account is fetched | Required: 'No input received' when blank; 'Account Number if supplied must be a 11 digit Non-Zero Number' when not numeric or all zeros; 'Account:<number> not found in Cross ref file' when the account has no card cross-reference. |  |  |
| Guidance | message | 'Enter or update id of account to update' before an account is fetched; then 'Update account details presented above.' and, once checked, a prompt to review and save |  |  | OATM-REQ-F-001, OATM-REQ-F-002, OATM-REQ-F-003 |


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
| OATM-BR-001 | Prompt for account id on first entry | formatting | WHEN the account update screen is shown on first entry to the function, THE Account Update messaging SHALL set the information message to 'Enter or update id of account to update'. | medium | app/cbl/COACTUPC.cbl:2955-2959, app/cbl/COACTUPC.cbl:468-469 |
| OATM-BR-002 | Prompt for account id when details missing | formatting | WHEN the account update screen is shown, it is not a first entry, and no account details have been fetched yet, THE Account Update messaging SHALL set the information message to 'Enter or update id of account to update'. | medium | app/cbl/COACTUPC.cbl:2955-2961, app/cbl/COACTUPC.cbl:656-658 |
| OATM-BR-003 | Default to search prompt and show messages | historical artifact | WHEN no update stage matches and the information message is blank, THE Account Update messaging SHALL default it to 'Enter or update id of account to update'; every valid stage is matched earlier, so this fallback does not normally apply. | medium | app/cbl/COACTUPC.cbl:2955-2982, app/cbl/COACTUPC.cbl:656-668 |
| OATM-BR-004 | Resolve customer from card cross-reference | design note | WHEN the account is found in the card cross-reference (by account ID), THE account update SHALL take the customer ID and card number from it for the session and go on to read the account and customer. | medium | app/cbl/COACTUPC.cbl:3608-3626, app/cbl/COACTUPC.cbl:3650-3696, app/cbl/COACTUPC.cbl:389-404, app/cbl/COACTUPC.cbl:581 |
| OATM-BR-005 | Resolve customer from card cross-reference | business rule | WHEN the account is not in the card cross-reference, THE account update SHALL flag the account as invalid, stop the lookup and show 'Account:<account> not found in Cross ref file. Resp:<resp> Reas:<reason>'. | medium | app/cbl/COACTUPC.cbl:3608-3626, app/cbl/COACTUPC.cbl:3650-3696, app/cbl/COACTUPC.cbl:389-404, app/cbl/COACTUPC.cbl:581 |
| OATM-BR-006 | Resolve customer from card cross-reference | error handling | WHEN the cross-reference read fails for any other reason, THE account update SHALL flag the account as invalid, stop the lookup and show 'File Error: READ on CXACAIX returned RESP <resp>,RESP2 <reason>'. | medium | app/cbl/COACTUPC.cbl:3608-3626, app/cbl/COACTUPC.cbl:3650-3696, app/cbl/COACTUPC.cbl:389-404, app/cbl/COACTUPC.cbl:581 |
| OATM-BR-007 | Read account master record | design note | WHEN the account master read (ACCTDAT) succeeds, THE Account Update retrieval SHALL mark the account as found. | medium | app/cbl/COACTUPC.cbl:3701-3748, app/cbl/COACTUPC.cbl:389-400 |
| OATM-BR-008 | Read account master record | error handling | WHEN the account is not on the account master, THE Account Update retrieval SHALL flag an input error, mark the account search invalid and, if no message is already set, report 'Account:<id> not found in Acct Master file.Resp:<resp> Reas:<reason>'. | medium | app/cbl/COACTUPC.cbl:3701-3748, app/cbl/COACTUPC.cbl:389-400 |
| OATM-BR-009 | Read account master record | error handling | WHEN the account master read fails for any other reason, THE Account Update retrieval SHALL flag an input error, mark the account search invalid and report 'File Error: READ on ACCTDAT returned RESP <resp>...'. | medium | app/cbl/COACTUPC.cbl:3701-3748, app/cbl/COACTUPC.cbl:389-400 |
| OATM-BR-010 | Read customer master record | design note | WHEN the customer master read (CUSTDAT) for the account's customer succeeds, THE Account Update retrieval SHALL mark the customer as found. | medium | app/cbl/COACTUPC.cbl:3752-3797, app/cbl/COACTUPC.cbl:3631-3634 |
| OATM-BR-011 | Read customer master record | error handling | WHEN the customer is not on the customer master, THE Account Update retrieval SHALL flag an input error, mark the customer search invalid and, if no message is already set, report 'CustId:<id> not found in customer master.Resp: <resp> REAS:<reason>'. | medium | app/cbl/COACTUPC.cbl:3752-3797, app/cbl/COACTUPC.cbl:3631-3634 |
| OATM-BR-012 | Read customer master record | error handling | WHEN the customer master read fails for any other reason, THE Account Update retrieval SHALL flag an input error, mark the customer search invalid and report 'File Error: READ on CUSTDAT returned RESP <resp>...'. | medium | app/cbl/COACTUPC.cbl:3752-3797, app/cbl/COACTUPC.cbl:3631-3634 |
| OATM-BR-013 | Store fetched details as original snapshot | design note | WHEN the account is found in the card cross-reference, THE Account Update retrieval SHALL save the account id, customer id, customer names, account status and card number as the session context. | medium | app/cbl/COACTUPC.cbl:3801-3885, app/cbl/COACTUPC.cbl:3608-3647 |
| OATM-BR-014 | Store fetched details as original snapshot | design note | WHEN the account is found in the card cross-reference, THE Account Update retrieval SHALL copy the fetched account and customer values into the original snapshot, splitting the open, expiry, reissue and birth dates (YYYY-MM-DD) into year, month and day. | medium | app/cbl/COACTUPC.cbl:3801-3885, app/cbl/COACTUPC.cbl:3608-3647 |

### Worked examples

- OATM-BR-001: entry = first entry from the main menu → Message 'Enter or update id of account to update'
- OATM-BR-002: account id entered = 00000000099 (not found); update stage = not fetched → Message 'Enter or update id of account to update'
- OATM-BR-003: update stage = unrecognised value; information message = blank → Message 'Enter or update id of account to update'
- OATM-BR-004: Account ID = 00000000011; Cross-reference = found, customer 000000011 → Customer 000000011 and its card number become the session customer and card.
- OATM-BR-007: account id = 00000000001; account master = record exists → Account marked found
- OATM-BR-010: customer id from cross-reference = 000000001; customer master = record exists → Customer marked found
- OATM-BR-013: account id = 00000000001; cross-reference = found → The session context holds the account, customer and card number for later screens
- OATM-BR-014: stored expiry date = 2027-08-31 → Snapshot expiry year 2027, month 08, day 31

## Decision tables

#### Outcome of each record read during account lookup

| Record read | Read result | Lookup outcome | Rule |
|---|---|---|---|
| Card cross-reference | Found | Take customer ID and card number for the session; go on to read account and customer | OATM-BR-004 |
| Card cross-reference | Not found | Flag account invalid, stop lookup, show 'Account:<account> not found in Cross ref file. Resp:<resp> Reas:<reason>' | OATM-BR-005 |
| Card cross-reference | Other failure | Flag account invalid, stop lookup, show 'File Error: READ on CXACAIX returned RESP <resp>,RESP2 <reason>' | OATM-BR-006 |
| Account master | Found | Mark account as found | OATM-BR-007 |
| Account master | Not found | Flag input error, mark account search invalid, report 'Account:<id> not found in Acct Master file...' if no message already set | OATM-BR-008 |
| Account master | Other failure | Flag input error, mark account search invalid, report 'File Error: READ on ACCTDAT returned RESP <resp>...' | OATM-BR-009 |
| Customer master | Found | Mark customer as found | OATM-BR-010 |
| Customer master | Not found | Flag input error, mark customer search invalid, report 'CustId:<id> not found in customer master...' if no message already set | OATM-BR-011 |
| Customer master | Other failure | Flag input error, mark customer search invalid, report 'File Error: READ on CUSTDAT returned RESP <resp>...' | OATM-BR-012 |
| Account master | Not found / Other failure | **Gap:** No rule says whether the customer master is still read after the account master read fails, or whether the screen then shows details. | |

#### Information message before account details are shown

| First entry | Account details fetched | Update stage matched | Information message | Rule |
|---|---|---|---|---|
| Yes | - | - | 'Enter or update id of account to update' | OATM-BR-001 |
| No | No | - | 'Enter or update id of account to update' | OATM-BR-002 |
| - | - | No stage matches (message blank) | Default to 'Enter or update id of account to update' | OATM-BR-003 |


## Design notes

- OATM-BR-004: Needs a keyed lookup from account id to its card link (customer id and card number), via an index on account id over the card-account-customer cross-reference; the customer id it returns drives the customer read, and the card number is kept in the session.
- OATM-BR-007: Needs a read of the account record by its account id primary key; a successful read sets an 'account found' state that the screen uses to decide whether account fields can be shown.
- OATM-BR-010: Needs a read of the customer record by the customer id taken from the cross-reference; a successful read sets a 'customer found' state used for showing customer fields.
- OATM-BR-013: Keep account id, customer id, customer names, account status and card number in the operator's server-side session (or a signed request token) so they carry over between screen submissions and to the next screen.
- OATM-BR-014: Store an immutable snapshot of the fetched account and customer values for the session, with open, expiry, reissue and birth dates held as year, month and day parts; it is the baseline for change detection and for the optimistic check that nobody else changed the record before save (a version or timestamp column can serve the same purpose).

## Open questions

- SME-055: When the customer for an account cannot be found during account update, a 'not found' message is shown but the customer is not marked as not found. Should the new system explicitly mark the customer as not found? (Account servicing business owner) On OATM-BR-006, OATM-BR-009, OATM-BR-012, OATM-BR-014.
- DEF-116: Is this intended? When the account is not on the account master, the 'not found' state is never set (that line is commented out), so the check at 3627 never stops processing. The program goes on to read the customer, stores account data it never read, and can show the screen as if details were found. (Subject-matter expert) On OATM-BR-009.
- DEF-117: Is this intended? The 'customer not found' state is never set (that line is commented out), so the program still stores the unread customer record as the original snapshot and in the shared context. The screen stays in 'not fetched' because the customer was not found. (Subject-matter expert) On OATM-BR-012.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).