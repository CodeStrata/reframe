# Requirements: Look up a single transaction (OATM-C28)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Opens the Transaction View for a signed-on user. If they came from the transaction list with a transaction picked, its ID is pre-filled and looked up straight away. If the transaction ID is left empty, the screen must refuse to look anything up and say 'Tran ID can NOT be empty...'.

**User story:** As a signed-on user, I want to open the transaction view, with the transaction I picked already filled in, and be told when I leave the ID empty, so that I can see the details of one transaction.

## Requirements

### Requirement 1: OATM-REQ-F-226 (formatting)

#### Acceptance criteria

1. While the caller's data is present and the program is not being re-entered, when the transaction view is opened, the system shall reset the screen, position the cursor on the transaction ID entry field, pre-fill the ID and perform the transaction lookup where a transaction was pre-selected on a prior screen (CDEMO-CT01-TRN-SELECTED not spaces or low-values), and then display the transaction view screen. (rules OATM-BR-239)
2. GIVEN Opened from: Main menu option 7 'Transaction View'; CDEMO-CT01-TRN-SELECTED: spaces WHEN the caller's data is present and the program is not being re-entered (`CDEMO-PGM-REENTER` not true), WHEN the transaction view is opened, optionally with a transaction pre-selected on a prior screen (`CDEMO-CT01-TRN-SELECTED` not spaces or low-values) THEN An empty Transaction View screen is shown with the cursor on the Tran ID field (OATM-C28-AC-01; OATM-BR-239)

### Requirement 2: OATM-REQ-F-227 (business rule)

#### Acceptance criteria

1. If the entered transaction ID (TRNIDINI) is spaces or low-values, then the system shall flag an error, show the message 'Tran ID can NOT be empty...' and redisplay the screen with the cursor on the transaction ID field. (rules OATM-BR-240)
2. GIVEN Key pressed: Enter; Tran ID (TRNIDINI): (blank) WHEN the entered transaction ID (`TRNIDINI`) is spaces or low-values THEN The screen is redisplayed with 'Tran ID can NOT be empty...' and the cursor on the Tran ID field; no lookup is done (OATM-C28-AC-02; OATM-BR-240)
