# Requirements: Record a confirmed new transaction (OATM-C33)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Records a validated, confirmed transaction. It gives the transaction the next number after the highest one on file, as 16 zero-padded digits (0000000000000001 when the file is empty), and writes it with the card found for the entered account or card. It must never reuse an existing number or lose the operator's entries on a failed write. On success it shows the new Tran ID.

**User story:** As a staff user, I want a confirmed, valid transaction to be numbered and written to the transaction file with a clear confirmation or error, so that the account's activity is recorded accurately.

## Requirements

### Requirement 1: OATM-REQ-F-277 (business rule)

#### Acceptance criteria

1. When every Transaction Add field passes validation and Confirm is 'Y' or 'y', the system shall add the transaction. (rules OATM-BR-293)
2. GIVEN All fields: valid; Confirm: y WHEN every Transaction Add field passes validation and Confirm is 'Y' or 'y' THEN The transaction is added (OATM-C33-AC-01; OATM-BR-293)

### Requirement 2: OATM-REQ-F-278 (business rule)

#### Acceptance criteria

1. When a confirmed transaction is added, the system shall find the highest transaction number on the transaction file by reading backward from the end, and give the new transaction that number plus 1 as a 16-digit, zero-padded number. (rules OATM-BR-294)
2. GIVEN Highest transaction number on file: 0000000000001234; Confirm: Y WHEN a confirmed transaction is added THEN The new transaction is numbered 0000000000001235 (OATM-C33-AC-02; OATM-BR-294)

### Requirement 3: OATM-REQ-F-279 (business rule)

#### Acceptance criteria

1. When reading backward finds no transaction on the file (end of file), the system shall count the highest number as zero, so the new transaction is numbered 0000000000000001. (rules OATM-BR-295)
2. GIVEN Transactions on file: none (end of file reached); Confirm: Y WHEN reading backward finds no transaction on the file (end of file) THEN The new transaction is numbered 0000000000000001 (OATM-C33-AC-03; OATM-BR-295)

### Requirement 4: OATM-REQ-F-280 (error handling)

#### Acceptance criteria

1. If the lookup of the highest transaction number fails, then the system shall add nothing and show 'Transaction ID NOT found...' when the start position is not found, or 'Unable to lookup Transaction...' for any other error, with the cursor on Account ID. (rules OATM-BR-296)
2. GIVEN Transaction file browse result: error other than not found or end of file WHEN the lookup of the highest transaction number fails THEN No transaction is added and the screen shows 'Unable to lookup Transaction...' (OATM-C33-AC-04; OATM-BR-296)

### Requirement 5: OATM-REQ-F-281 (business rule)

#### Acceptance criteria

1. When a confirmed transaction has been given its new number, the system shall write a new record to the transaction file (TRANSACT) with that number, the entered type, category, source, description, amount, merchant ID, name, city and zip, origination and processing dates, and the card number found for the entered account or card. (rules OATM-BR-297)
2. GIVEN Card number: 4111111111111111; Amount: +00000050.00; Confirm: Y; Next number: 0000000000001235 WHEN a confirmed transaction has been given its new number THEN TRANSACT gains record 0000000000001235 for card 4111111111111111 with amount 50.00 (OATM-C33-AC-05; OATM-BR-297)
3. GIVEN Account ID: 00000000001; Card on file for account: 4111111111111111 WHEN a confirmed transaction has been given its new number THEN The record is written with card number 4111111111111111 (OATM-C33-AC-06; OATM-BR-297)

### Requirement 6: OATM-REQ-F-282 (formatting)

#### Acceptance criteria

1. When the new transaction is written successfully, the system shall clear every field and show in green 'Transaction added successfully. Your Tran ID is <number>.' (rules OATM-BR-298)
2. GIVEN a validated transaction with Confirm 'Y' whose new number is 0000000000000301, and the write to the transaction file succeeds WHEN the add completes THEN every field on the Add Transaction screen is cleared and the message 'Transaction added successfully. Your Tran ID is 0000000000000301.' is shown in green (OATM-C33-AC-09; OATM-BR-298)

### Requirement 7: OATM-REQ-F-283 (error handling)

#### Acceptance criteria

1. If writing the new transaction fails because the number already exists, then the system shall show 'Tran ID already exist...' with the cursor on Account ID and keep the entries. (rules OATM-BR-299)
2. GIVEN Write result: duplicate key WHEN writing the new transaction fails because the number already exists THEN The screen shows 'Tran ID already exist...' and nothing is added (OATM-C33-AC-07; OATM-BR-299)

### Requirement 8: OATM-REQ-N-015 (error handling)

#### Acceptance criteria

1. If writing the new transaction fails for any other reason, then the system shall show 'Unable to Add Transaction...' with the cursor on Account ID and log the response codes. (rules OATM-BR-300)
2. GIVEN Write result: file not open WHEN writing the new transaction fails for any other reason THEN The screen shows 'Unable to Add Transaction...' (OATM-C33-AC-08; OATM-BR-300)
