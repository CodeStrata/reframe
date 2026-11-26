# Requirements: Carry sensitive customer and card data in the export (CPBM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Customer Profile Branch Migration · runs as scheduled job · risk high

## Introduction

The migration file carries customers' identity data and cards' security data in full so the target branch receives complete records: SSN, government ID, date of birth, EFT account and FICO score on customer records, and the full 16-digit card number and 3-digit CVV on card records. These values are copied unmasked, so the file holds highly sensitive data and the team must protect it accordingly. The values must never be truncated, masked or altered on the way out.

**User story:** As a branch migration operator, I want the export to carry the customer's identity data and the card's security data, so that the target branch receives complete customer and card records.

## Requirements

### Requirement 1: CPBM-REQ-N-001 (business rule)

#### Acceptance criteria

1. The system shall copy sensitive data unmasked into the export file: the customer's SSN, government-issued ID, date of birth, EFT account and FICO score on 'C' records, and the card number and CVV code on 'D' records. (rules CPBM-BR-009)
2. GIVEN card CVV: 123 WHEN Branch Migration Export runs THEN The 'D' export record holds CVV 123 as-is. (CPBM-C02-AC-01; CPBM-BR-009)
3. GIVEN customer SSN: 123456789 WHEN Branch Migration Export runs THEN The 'C' export record holds SSN 123456789 as-is. (CPBM-C02-AC-02; CPBM-BR-009)

### Requirement 2: CPBM-REQ-N-002 (business rule)

#### Acceptance criteria

1. When a customer export record (type 'C') is written, the system shall copy the customer's full 9-digit Social Security Number (EXP-CUST-SSN) unmasked, along with government-issued ID, date of birth and EFT account ID. (rules CPBM-BR-010)
2. GIVEN Customer SSN on file: 123456789; Government-issued ID: DL-4455667 WHEN a customer export record (type 'C') is written THEN The 'C' export record holds SSN 123456789 and ID DL-4455667 exactly as on file, with no masking. (CPBM-C02-AC-03; CPBM-BR-010)

### Requirement 3: CPBM-REQ-N-003 (business rule)

#### Acceptance criteria

1. When a card export record (type 'D') is written, the system shall copy the card's 3-digit CVV code (EXP-CARD-CVV-CD) unmasked, stored as a binary number, together with the full 16-digit card number. (rules CPBM-BR-011)
2. GIVEN Card number: 4111111111111111; CVV code: 123 WHEN a card export record (type 'D') is written THEN The 'D' export record holds card number 4111111111111111 and CVV 123 (in binary form); neither is masked. (CPBM-C02-AC-04; CPBM-BR-011)
