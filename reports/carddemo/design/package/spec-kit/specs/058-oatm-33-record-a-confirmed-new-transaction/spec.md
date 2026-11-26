# Feature specification: Record a confirmed new transaction

**Feature:** OATM-C33 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C33)

As a staff user, I want a confirmed, valid transaction to be numbered and written to the transaction file with a clear confirmation or error, so that the account's activity is recorded accurately.

Records a validated, confirmed new transaction. It gets the next transaction number (the highest on file plus 1, as 16 zero-padded digits) and is written with the entered details and the card found for the account. The user sees 'Transaction added successfully. Your Tran ID is <number>.'. Numbers must never be duplicated or reused, and a failed write must say so and save nothing.

**Acceptance scenarios:**

1. **Given** All fields: valid; Confirm: y, **when** every Transaction Add field passes validation and Confirm is 'Y' or 'y', **then** The transaction is added (OATM-C33-AC-01)
2. **Given** Highest transaction number on file: 0000000000001234; Confirm: Y, **when** a confirmed transaction is added, **then** The new transaction is numbered 0000000000001235 (OATM-C33-AC-02)
3. **Given** Transactions on file: none (end of file reached); Confirm: Y, **when** reading backward finds no transaction on the file (end of file), **then** The new transaction is numbered 0000000000000001 (OATM-C33-AC-03)
4. **Given** Transaction file browse result: error other than not found or end of file, **when** the lookup of the highest transaction number fails, **then** No transaction is added and the screen shows 'Unable to lookup Transaction...' (OATM-C33-AC-04)
5. **Given** Card number: 4111111111111111; Amount: +00000050.00; Confirm: Y; Next number: 0000000000001235, **when** a confirmed transaction has been given its new number, **then** TRANSACT gains record 0000000000001235 for card 4111111111111111 with amount 50.00 (OATM-C33-AC-05)
6. **Given** Account ID: 00000000001; Card on file for account: 4111111111111111, **when** a confirmed transaction has been given its new number, **then** The record is written with card number 4111111111111111 (OATM-C33-AC-06)
7. **Given** Write result: duplicate key, **when** writing the new transaction fails because the number already exists, **then** The screen shows 'Tran ID already exist...' and nothing is added (OATM-C33-AC-07)
8. **Given** Write result: file not open, **when** writing the new transaction fails for any other reason, **then** The screen shows 'Unable to Add Transaction...' (OATM-C33-AC-08)
9. **Given** a validated Add Transaction form with Confirm 'Y', and the highest transaction number on file is 0000000000000041, **when** the user presses Enter and the new transaction is written successfully, **then** every field on the screen is cleared and the message 'Transaction added successfully. Your Tran ID is 0000000000000042.' is shown in green (OATM-C33-AC-09)

## Requirements

### Functional requirements

- **OATM-REQ-F-277** (business rule): When every Transaction Add field passes validation and Confirm is 'Y' or 'y', the system shall add the transaction. Rules: OATM-BR-293.
- **OATM-REQ-F-278** (business rule): When a confirmed transaction is added, the system shall find the highest transaction number on the transaction file by reading backward from the end, and give the new transaction that number plus 1 as a 16-digit, zero-padded number. Rules: OATM-BR-294.
- **OATM-REQ-F-279** (business rule): When reading backward finds no transaction on the file (end of file), the system shall count the highest number as zero, so the new transaction is numbered 0000000000000001. Rules: OATM-BR-295.
- **OATM-REQ-F-280** (error handling): If the lookup of the highest transaction number fails, then the system shall add nothing and show 'Transaction ID NOT found...' when the start position is not found, or 'Unable to lookup Transaction...' for any other error, with the cursor on Account ID. Rules: OATM-BR-296.
- **OATM-REQ-F-281** (business rule): When a confirmed transaction has been given its new number, the system shall write a new record to the transaction file (TRANSACT) with that number, the entered type, category, source, description, amount, merchant ID, name, city and zip, origination and processing dates, and the card number found for the entered account or card. Rules: OATM-BR-297.
- **OATM-REQ-F-282** (formatting): When the new transaction is written successfully, the system shall clear every field and show in green 'Transaction added successfully. Your Tran ID is <number>.' Rules: OATM-BR-298.
- **OATM-REQ-F-283** (error handling): If writing the new transaction fails because the number already exists, then the system shall show 'Tran ID already exist...' with the cursor on Account ID and keep the entries. Rules: OATM-BR-299.
- **OATM-REQ-N-015** (error handling): If writing the new transaction fails for any other reason, then the system shall show 'Unable to Add Transaction...' with the cursor on Account ID and log the response codes. Rules: OATM-BR-300.

### Business rules

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

### Key entities

- CVACT03Y (file record)
- CVTRA05Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CVACT01Y (working storage)

### Needs clarification

- SME-177: What type and length should the transaction number have in the transaction master store, so that new transaction numbers meet that format? (Data architect) On OATM-BR-300, OATM-BR-294, OATM-BR-295, OATM-BR-297, OATM-BR-298, OATM-BR-293.
- SME-178: When the origination and processing dates entered as YYYY-MM-DD are stored as timestamps, what time portion and timestamp format should be used? (Data architect) On OATM-BR-300, OATM-BR-294, OATM-BR-295, OATM-BR-297, OATM-BR-298, OATM-BR-293.
- SME-179: New transactions are numbered 'highest existing number + 1'. Must this scheme be kept, or should a central sequence or counter be used so that numbers cannot clash with other postings made at the same time or with transactions created by batch jobs? (Solution architect) On OATM-BR-296.
- DEF-015: Is this intended? The next number is taken as highest-plus-one with no lock, so two users adding at the same moment can get the same number; the second write then fails with 'Tran ID already exist...' and the user must try again. (Subject-matter expert) On OATM-BR-294, OATM-BR-295, OATM-BR-296.
- DEF-060: Is this intended? The type and category codes are written as entered without checking that they exist in the reference tables; they are only checked for being present and numeric. (Subject-matter expert) On OATM-BR-297, OATM-BR-298.

### Decision table gaps

- Transaction numbering and write outcome: No rule states what the screen does when validation passes but Confirm is blank or a value other than 'Y'/'y'.
