# Requirements: Import and split the migration file into target files (CPBM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Customer Profile Branch Migration · runs as scheduled job · risk high

## Introduction

Reads the combined migration file in sequence-number order and splits it back into separate customer, account, card cross-reference, transaction and card files for the target branch. Each record is routed by its type code and copied field for field, with no business validation. It must never drop, change or reject a record of a known type: the target data must match what was exported exactly.

**User story:** As a branch migration operator, I want the combined migration file split back into separate customer, account, cross-reference, transaction and card files, so that the target branch receives normalized master data.

## Requirements

### Requirement 1: CPBM-REQ-F-013 (design note)

#### Acceptance criteria

1. The system shall run the import program against the shared export file (AWS.M2.CARDDEMO.EXPORT.DATA) and create new cataloged customer (500-byte), account (300-byte), card cross-reference (50-byte) and transaction (350-byte) import files plus a 132-byte import error file. (rules CPBM-BR-017)
2. GIVEN step outcome: normal end WHEN import job runs THEN AWS.M2.CARDDEMO.CUSTDATA.IMPORT, ACCTDATA.IMPORT, CARDXREF.IMPORT, TRANSACT.IMPORT and IMPORT.ERRORS are cataloged. (CPBM-C05-AC-01; CPBM-BR-017)
3. GIVEN step outcome: abend WHEN import job runs THEN All five new import files are deleted. (CPBM-C05-AC-02; CPBM-BR-017)

### Requirement 2: CPBM-REQ-F-014 (design note)

#### Acceptance criteria

1. The system shall not allocate a card import file in the import job, although the import program writes card records ('D') to one. (rules CPBM-BR-018)
2. GIVEN CARDOUT DD in job: absent WHEN import job runs THEN No card import dataset is cataloged by the job. (CPBM-C05-AC-03; CPBM-BR-018)

### Requirement 3: CPBM-REQ-F-015 (business rule)

#### Acceptance criteria

1. While records remain in the branch migration export file, read in export sequence-number order, the system shall count each record read and route it by record type: 'C' to the customer import file, 'A' to the account import file, 'X' to the card cross-reference import file, 'T' to the transaction import file and 'D' to the card import file. (rules CPBM-BR-019)
2. GIVEN record type: 'X' WHEN records remain in the branch migration export file (read in export sequence-number order) THEN A card cross-reference record is written to the cross-reference import file (XREFOUT) and the cross-references-imported count goes up by 1. (CPBM-C05-AC-04; CPBM-BR-019)
3. GIVEN record type: 'D' WHEN records remain in the branch migration export file (read in export sequence-number order) THEN A card record is written to the card import file (CARDOUT) and the cards-imported count goes up by 1. (CPBM-C05-AC-05; CPBM-BR-019)

### Requirement 4: CPBM-REQ-F-016 (business rule)

#### Acceptance criteria

1. When a customer record ('C') is imported, the system shall write a customer record copying the exported customer number, first, middle and last name, three address lines, state, country, zip, two phone numbers, social security number, government id, date of birth, EFT account, primary card holder indicator and FICO score. (rules CPBM-BR-020)
2. GIVEN social security number: 123456789; FICO score: 720 WHEN a customer record ('C') is imported THEN A customer record with SSN 123456789 and FICO 720 is written to CUSTOUT and the customers-imported count goes up by 1. (CPBM-C05-AC-06; CPBM-BR-020)

### Requirement 5: CPBM-REQ-F-017 (design note)

#### Acceptance criteria

1. When an account record ('A') is imported, the system shall write an account record copying the exported account number, active status, current balance, credit limit, cash credit limit, open, expiration and reissue dates, current-cycle credit and debit, zip code and group id. (rules CPBM-BR-021)
2. GIVEN account number: 00000000011; credit limit: 5000.00 WHEN an account record ('A') is imported THEN An account record with account 00000000011 and credit limit 5000.00 is written to ACCTOUT and the accounts-imported count goes up by 1. (CPBM-C05-AC-07; CPBM-BR-021)

### Requirement 6: CPBM-REQ-F-018 (design note)

#### Acceptance criteria

1. When a card cross-reference record ('X') is imported, the system shall write a cross-reference record with the exported card number, customer number and account number. (rules CPBM-BR-022)
2. GIVEN card number: 4111111111111111; customer number: 000000001; account number: 00000000011 WHEN a card cross-reference record ('X') is imported THEN A cross-reference record with those three values is written to XREFOUT. (CPBM-C05-AC-08; CPBM-BR-022)

### Requirement 7: CPBM-REQ-F-019 (design note)

#### Acceptance criteria

1. When a transaction record ('T') is imported, the system shall write a transaction record copying the exported transaction id, type, category, source, description, amount, merchant id, name, city and zip, card number, origination and processing timestamps. (rules CPBM-BR-023)
2. GIVEN the migration file holds a 'T' record with transaction id, type, category, source, description, amount, merchant id, merchant name, city and zip, card number, origination timestamp and processing timestamp WHEN the import processes that record THEN one transaction record is written to the transaction import file carrying each of those values unchanged (CPBM-C05-AC-10; CPBM-BR-023)
3. GIVEN writing the transaction record fails WHEN the import processes a 'T' record THEN the import run ends abnormally (CPBM-C05-AC-11; CPBM-BR-023)

### Requirement 8: CPBM-REQ-F-020 (business rule)

#### Acceptance criteria

1. When a card record ('D') is imported, the system shall write a card record with the exported card number, account number, CVV code, embossed name, expiration date and active status. (rules CPBM-BR-024)
2. GIVEN the migration file holds a 'D' record with a 16-digit card number, account number, CVV code, embossed name, expiration date and active status WHEN the import processes that record THEN one card record is written to the card import file carrying the card number, account number, CVV code, embossed name, expiration date and active status unchanged (CPBM-C05-AC-12; CPBM-BR-024)
3. GIVEN writing the card record fails WHEN the import processes a 'D' record THEN the import run ends abnormally (CPBM-C05-AC-13; CPBM-BR-024)

### Requirement 9: CPBM-REQ-F-021 (business rule)

#### Acceptance criteria

1. The system shall write imported customer, account, cross-reference, transaction and card records exactly as received, with no business validation of status codes, balances, limits or dates, and shall never send them to the error file. (rules CPBM-BR-025)
2. GIVEN account active status: 'Q'; current balance: 9999.00; credit limit: 500.00 WHEN import batch runs THEN The account is written with status 'Q' and the balance over its limit, and is counted as imported; no error record is written. (CPBM-C05-AC-09; CPBM-BR-025)
