# Design: Record a confirmed new transaction (OATM-C33)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Records a validated, confirmed new transaction. It gets the next transaction number (the highest on file plus 1, as 16 zero-padded digits) and is written with the entered details and the card found for the account. The user sees 'Transaction added successfully. Your Tran ID is <number>.'. Numbers must never be duplicated or reused, and a failed write must say so and save nothing.

Runs as online. Journeys: J04.

## Screens and components

### Add transaction (S-TRANSACTION-ADD)

Enter a transaction against an account or card, see what to fix at each field, confirm the summary and record it.

Prototype: `ui-reference/index.html#/S-TRANSACTION-ADD`. Replaces the legacy screens COTRN2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Add this transaction? | dialog | Summary of the transaction with 'Confirm to add this transaction...'. Confirm adds it; Cancel returns to the form with nothing added. Buttons replace typing Y/N, so 'Invalid value. Valid values are (Y/N)...' cannot arise. |  |  | OATM-REQ-F-277 |
| Result | message | Success in green: 'Transaction added successfully. Your Tran ID is <id>.' and the form clears; failures: 'Tran ID already exist...', 'Unable to Add Transaction...', 'Transaction ID NOT found...' |  |  | OATM-REQ-F-278, OATM-REQ-F-282, OATM-REQ-F-283 |


## Data models

#### CVACT03Y

File record of COTRN02C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVTRA05Y

File record of COTRN02C. Source: `app/cpy/CVTRA05Y.cpy`.

Record `TRAN-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-ID |  | X(16) | text, 16 characters |  |  |  |
| TRAN-TYPE-CD |  | X(02) | text, 2 characters |  |  |  |
| TRAN-CAT-CD |  | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-SOURCE |  | X(10) | text, 10 characters |  |  |  |
| TRAN-DESC |  | X(100) | text, 100 characters |  |  |  |
| TRAN-AMT |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-NAME |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-CITY |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-ZIP |  | X(10) | text, 10 characters |  |  |  |
| TRAN-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| TRAN-ORIG-TS |  | X(26) | text, 26 characters |  |  |  |
| TRAN-PROC-TS |  | X(26) | text, 26 characters |  |  |  |
| FILLER |  | X(20) | text, 20 characters |  |  |  |

- COCOM01Y (working storage of COTRN02C): see data-contracts.md.
- COTTL01Y (working storage of COTRN02C): see data-contracts.md.
- CSDAT01Y (working storage of COTRN02C): see data-contracts.md.
- CSMSG01Y (working storage of COTRN02C): see data-contracts.md.
- CVACT01Y (working storage of COTRN02C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-293 | Add transaction upon confirmation | business rule | WHEN every Transaction Add field passes validation and Confirm is 'Y' or 'y', THE Transaction Add screen SHALL add the transaction. | high | app/cbl/COTRN02C.cbl:160-188, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-294 | Assign next transaction number | business rule | WHEN a confirmed transaction is added, THE transaction add screen SHALL find the highest transaction number on the transaction file by reading backward from the end, and give the new transaction that number plus 1 as a 16-digit, zero-padded number. | high | app/cbl/COTRN02C.cbl:442-451, app/cbl/COTRN02C.cbl:642-668, app/cbl/COTRN02C.cbl:673-697, app/cbl/COTRN02C.cbl:57 |
| OATM-BR-295 | Default transaction number for empty store | business rule | WHEN reading backward finds no transaction on the file (end of file), THE transaction add screen SHALL count the highest number as zero, so the new transaction is numbered 0000000000000001. | high | app/cbl/COTRN02C.cbl:442-451, app/cbl/COTRN02C.cbl:642-668, app/cbl/COTRN02C.cbl:673-697, app/cbl/COTRN02C.cbl:57 |
| OATM-BR-296 | New transaction ID = highest existing ID + 1 | error handling | WHEN the lookup of the highest transaction number fails, THE transaction add screen SHALL add nothing and show 'Transaction ID NOT found...' when the start position is not found, or 'Unable to lookup Transaction...' for any other error, with the cursor on Account ID. | high | app/cbl/COTRN02C.cbl:442-451, app/cbl/COTRN02C.cbl:642-668, app/cbl/COTRN02C.cbl:673-697, app/cbl/COTRN02C.cbl:57 |
| OATM-BR-297 | Build and record new transaction | business rule | WHEN a confirmed transaction has been given its new number, THE transaction add screen SHALL write a new record to the transaction file (TRANSACT) with that number, the entered type, category, source, description, amount, merchant ID, name, city and zip, origination and processing dates, and the card number found for the entered account or card. | high | app/cbl/COTRN02C.cbl:450-466, app/cbl/COTRN02C.cbl:711-734, app/cbl/COTRN02C.cbl:762-779 |
| OATM-BR-298 | Confirm successful transaction addition | formatting | WHEN the new transaction is written successfully, THE transaction add screen SHALL clear every field and show in green 'Transaction added successfully. Your Tran ID is <number>.' | high | app/cbl/COTRN02C.cbl:450-466, app/cbl/COTRN02C.cbl:711-734, app/cbl/COTRN02C.cbl:762-779 |
| OATM-BR-299 | Report transaction recording failure | error handling | WHEN writing the new transaction fails because the number already exists, THE transaction add screen SHALL show 'Tran ID already exist...' with the cursor on Account ID and keep the entries. | medium | app/cbl/COTRN02C.cbl:735-749 |
| OATM-BR-300 | Report transaction recording failure | error handling | WHEN writing the new transaction fails for any other reason, THE transaction add screen SHALL show 'Unable to Add Transaction...' with the cursor on Account ID and log the response codes. | medium | app/cbl/COTRN02C.cbl:735-749 |

### Worked examples

- OATM-BR-293: All fields = valid; Confirm = y → The transaction is added
- OATM-BR-294: Highest transaction number on file = 0000000000001234; Confirm = Y → The new transaction is numbered 0000000000001235
- OATM-BR-295: Transactions on file = none (end of file reached); Confirm = Y → The new transaction is numbered 0000000000000001
- OATM-BR-296: Transaction file browse result = error other than not found or end of file → No transaction is added and the screen shows 'Unable to lookup Transaction...'
- OATM-BR-297: Card number = 4111111111111111; Amount = +00000050.00; Confirm = Y; Next number = 0000000000001235 → TRANSACT gains record 0000000000001235 for card 4111111111111111 with amount 50.00
- OATM-BR-297: Account ID = 00000000001; Card on file for account = 4111111111111111 → The record is written with card number 4111111111111111
- OATM-BR-299: Write result = duplicate key → The screen shows 'Tran ID already exist...' and nothing is added
- OATM-BR-300: Write result = file not open → The screen shows 'Unable to Add Transaction...'

## Decision tables

#### Transaction numbering and write outcome

| Highest-number lookup result | Write result | Result | Rule |
|---|---|---|---|
| highest number found | - | New number = highest + 1, 16-digit zero-padded | OATM-BR-294 |
| end of file (no transactions) | - | New number 0000000000000001 | OATM-BR-295 |
| start position not found | not attempted | Add nothing; 'Transaction ID NOT found...', cursor on Account ID | OATM-BR-296 |
| other error | not attempted | Add nothing; 'Unable to lookup Transaction...', cursor on Account ID | OATM-BR-296 |
| number assigned | success | Clear fields; green 'Transaction added successfully. Your Tran ID is <number>.' | OATM-BR-298 |
| number assigned | number already exists | 'Tran ID already exist...', cursor on Account ID, keep entries | OATM-BR-299 |
| number assigned | other failure | 'Unable to Add Transaction...', cursor on Account ID, log response codes | OATM-BR-300 |
| all fields valid | Confirm not 'Y' or 'y' | **Gap:** No rule states what the screen does when validation passes but Confirm is blank or a value other than 'Y'/'y'. | |


## Design notes

None.

## Open questions

- SME-177: What type and length should the transaction number have in the transaction master store, so that new transaction numbers meet that format? (Data architect) On OATM-BR-300, OATM-BR-294, OATM-BR-295, OATM-BR-297, OATM-BR-298, OATM-BR-293.
- SME-178: When the origination and processing dates entered as YYYY-MM-DD are stored as timestamps, what time portion and timestamp format should be used? (Data architect) On OATM-BR-300, OATM-BR-294, OATM-BR-295, OATM-BR-297, OATM-BR-298, OATM-BR-293.
- SME-179: New transactions are numbered 'highest existing number + 1'. Must this scheme be kept, or should a central sequence or counter be used so that numbers cannot clash with other postings made at the same time or with transactions created by batch jobs? (Solution architect) On OATM-BR-296.
- DEF-015: Is this intended? The next number is taken as highest-plus-one with no lock, so two users adding at the same moment can get the same number; the second write then fails with 'Tran ID already exist...' and the user must try again. (Subject-matter expert) On OATM-BR-294, OATM-BR-295, OATM-BR-296.
- DEF-060: Is this intended? The type and category codes are written as entered without checking that they exist in the reference tables; they are only checked for being present and numeric. (Subject-matter expert) On OATM-BR-297, OATM-BR-298.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (9 in all).