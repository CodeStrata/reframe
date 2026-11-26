# Requirements: Confirm a transaction before it is added (OATM-C34)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Makes the operator explicitly confirm a valid transaction before it is added. 'Y' or 'y' adds it. 'N', 'n' or blank asks 'Confirm to add this transaction...', and any other value gets 'Invalid value. Valid values are (Y/N)...'. No transaction may ever be added without an explicit 'Y'.

**User story:** As an operator entering a transaction, I want the system to ask me to confirm before adding it and to reject an invalid confirmation, so that no transaction is added without my explicit confirmation.

## Requirements

### Requirement 1: OATM-REQ-F-284 (business rule)

#### Acceptance criteria

1. When every field passes validation and Confirm is 'N', 'n' or left blank, the system shall redisplay the Transaction Add screen with 'Confirm to add this transaction...' and the cursor on Confirm, and add nothing. (rules OATM-BR-301)
2. GIVEN All fields: valid; Confirm: N WHEN every field passes validation and Confirm is 'N', 'n' or left blank THEN 'Confirm to add this transaction...' is shown and nothing is written (OATM-C34-AC-01; OATM-BR-301)
3. GIVEN All fields: valid; Confirm: (blank) WHEN every field passes validation and Confirm is 'N', 'n' or left blank THEN 'Confirm to add this transaction...' is shown and nothing is written (OATM-C34-AC-02; OATM-BR-301)

### Requirement 2: OATM-REQ-F-285 (business rule)

#### Acceptance criteria

1. If every field passes validation and Confirm holds any value other than 'Y', 'N', 'n' or blank, then the system shall redisplay the Transaction Add screen with 'Invalid value. Valid values are (Y/N)...' and the cursor on Confirm, and add nothing. (rules OATM-BR-302)
2. GIVEN All fields: valid; Confirm: X WHEN every field passes validation and Confirm holds any other value THEN 'Invalid value. Valid values are (Y/N)...' is shown and nothing is written (OATM-C34-AC-03; OATM-BR-302)
