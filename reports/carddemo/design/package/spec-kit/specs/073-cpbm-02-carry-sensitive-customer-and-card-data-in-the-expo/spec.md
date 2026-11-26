# Feature specification: Carry sensitive customer and card data in the export

**Feature:** CPBM-C02 · Customer Profile Branch Migration · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CPBM-C02)

As a branch migration operator, I want the export to carry the customer's identity data and the card's security data, so that the target branch receives complete customer and card records.

The migration file carries customers' identity data and cards' security data in full so the target branch receives complete records: SSN, government ID, date of birth, EFT account and FICO score on customer records, and the full 16-digit card number and 3-digit CVV on card records. These values are copied unmasked, so the file holds highly sensitive data and the team must protect it accordingly. The values must never be truncated, masked or altered on the way out.

**Acceptance scenarios:**

1. **Given** card CVV: 123, **when** Branch Migration Export runs, **then** The 'D' export record holds CVV 123 as-is. (CPBM-C02-AC-01)
2. **Given** customer SSN: 123456789, **when** Branch Migration Export runs, **then** The 'C' export record holds SSN 123456789 as-is. (CPBM-C02-AC-02)
3. **Given** Customer SSN on file: 123456789; Government-issued ID: DL-4455667, **when** a customer export record (type 'C') is written, **then** The 'C' export record holds SSN 123456789 and ID DL-4455667 exactly as on file, with no masking. (CPBM-C02-AC-03)
4. **Given** Card number: 4111111111111111; CVV code: 123, **when** a card export record (type 'D') is written, **then** The 'D' export record holds card number 4111111111111111 and CVV 123 (in binary form); neither is masked. (CPBM-C02-AC-04)

## Requirements

### Functional requirements

- **CPBM-REQ-N-001** (business rule): The system shall copy sensitive data unmasked into the export file: the customer's SSN, government-issued ID, date of birth, EFT account and FICO score on 'C' records, and the card number and CVV code on 'D' records. Rules: CPBM-BR-009.
- **CPBM-REQ-N-002** (business rule): When a customer export record (type 'C') is written, the system shall copy the customer's full 9-digit Social Security Number (EXP-CUST-SSN) unmasked, along with government-issued ID, date of birth and EFT account ID. Rules: CPBM-BR-010.
- **CPBM-REQ-N-003** (business rule): When a card export record (type 'D') is written, the system shall copy the card's 3-digit CVV code (EXP-CARD-CVV-CD) unmasked, stored as a binary number, together with the full 16-digit card number. Rules: CPBM-BR-011.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CPBM-BR-009 | Export each customer as type C record | business rule | THE Branch Migration Export SHALL copy sensitive data unmasked into the export file: the customer's SSN, government-issued ID, date of birth, EFT account and FICO score on 'C' records, and the card number and CVV code on 'D' records. | high | app/cbl/CBEXPORT.cbl:243-310, app/cbl/CBEXPORT.cbl:312-373, app/cbl/CBEXPORT.cbl:376-428, app/cbl/CBEXPORT.cbl:431-493 |
| CPBM-BR-010 | Sensitive customer and card data exported in clear | business rule | WHEN a customer export record (type 'C') is written, THE customer data export SHALL copy the customer's full 9-digit Social Security Number (EXP-CUST-SSN) unmasked, along with government-issued ID, date of birth and EFT account ID. | medium | app/cbl/CBEXPORT.cbl:269-298, app/cbl/CBEXPORT.cbl:522-537, app/cpy/CVEXPORT.cpy:35-36, app/cpy/CVEXPORT.cpy:93-96 |
| CPBM-BR-011 | Sensitive customer and card data exported in clear | business rule | WHEN a card export record (type 'D') is written, THE customer data export SHALL copy the card's 3-digit CVV code (EXP-CARD-CVV-CD) unmasked, stored as a binary number, together with the full 16-digit card number. | medium | app/cbl/CBEXPORT.cbl:269-298, app/cbl/CBEXPORT.cbl:522-537, app/cpy/CVEXPORT.cpy:35-36, app/cpy/CVEXPORT.cpy:93-96 |

### Key entities

- CVACT01Y (file record)
- CVACT02Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CVEXPORT (file record)
- CVTRA05Y (file record)

### Needs clarification

- SME-018: Does the first record in the data export get sequence number 1? (Migration team) On CPBM-BR-009.
- SME-019: Every exported record is stamped with branch 0001 and region NORTH. Is that right for all customers, or should branch and region come from customer or account data, or from a run setting? (Data migration lead) On CPBM-BR-009.
- SME-020: When the export is rerun, should it replace or add to the previous export contents, and how should a run that ended abnormally be recovered? (Batch operations) On CPBM-BR-009.
- SME-021: Customer SSNs and card verification codes are copied into the export unmasked. Must the new export protect or leave out these values? (Security team) On CPBM-BR-009.
- SME-022: If the export cannot open one of its files, should the run end abnormally? (Batch operations) On CPBM-BR-009.
- DEF-088: Confirm this is deliberate: The card's CVV code and the customer's SSN and government ID go into the migration file unmasked. Storing a CVV after authorisation is not allowed under PCI DSS. (Subject-matter expert) On CPBM-BR-009.
- DEF-173: Confirm this is deliberate: The migration export file holds full SSNs and card CVV codes in clear. Storing a CVV after authorization goes against PCI DSS, and the SSN is unprotected personal data. The field-by-field copy shows the full values were meant to be exported, but nothing shows the security risk was considered. (Subject-matter expert) On CPBM-BR-011.

### Decision table gaps

None.
