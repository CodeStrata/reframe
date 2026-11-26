# Feature specification: Set up reference data backups

**Feature:** TTRDM-C22 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C22)

As an operations user, I want to create the backup generations for transaction type, category and disclosure group reference data, so that earlier versions of the reference data can be kept.

A one-time setup job for operations that creates the backup history for the transaction type, transaction category and disclosure group reference data, and stores a first backup copy of each. Each backup runs only when the earlier steps succeeded, and the transaction type history keeps at most five copies.

**Acceptance scenarios:**

1. **Given** generations of AWS.M2.CARDDEMO.TRANTYPE.BKUP: 5 already exist; new backup: 1 more created, **when** Transaction Reference Backup Setup runs, **then** The oldest generation is removed and scratched, leaving 5 (TTRDM-C22-AC-01)
2. **Given** step 10 return code: 0, **when** the step that defines the transaction type backup group ended with return code 0, **then** A new generation of AWS.M2.CARDDEMO.TRANTYPE.BKUP is created and cataloged, holding a copy of AWS.M2.CARDDEMO.TRANTYPE.PS (TTRDM-C22-AC-02)
3. **Given** step 10 return code: 12, **when** the step that defines the transaction type backup group ended with return code 0, **then** The copy step is skipped (TTRDM-C22-AC-03)
4. **Given** return codes of steps 10-30: all 0, **when** every earlier step of the setup job ended with return code 0, **then** A new generation of AWS.M2.CARDDEMO.TRANCATG.PS.BKUP is created and cataloged, holding a copy of AWS.M2.CARDDEMO.TRANCATG.PS (TTRDM-C22-AC-04)
5. **Given** step 30 return code: 12, **when** every earlier step of the setup job ended with return code 0, **then** The copy step is skipped (TTRDM-C22-AC-05)
6. **Given** return codes of steps 10-50: all 0, **when** every earlier step of the setup job ended with return code 0, **then** A new generation of AWS.M2.CARDDEMO.DISCGRP.BKUP is created and cataloged, holding a copy of AWS.M2.CARDDEMO.DISCGRP.PS (TTRDM-C22-AC-06)
7. **Given** step 10 return code: 12 (transaction type backup group already defined), **when** every earlier step of the setup job ended with return code 0, **then** The disclosure group copy step is skipped (TTRDM-C22-AC-07)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-147** (design note): The system shall first define the transaction type backup generation group (AWS.M2.CARDDEMO.TRANTYPE.BKUP), keeping at most 5 generations and deleting the oldest when a sixth is added, before any reference data is loaded. Rules: TTRDM-BR-159.
- **TTRDM-REQ-F-148** (design note): When the step that defines the transaction type backup group ended with return code 0, the system shall copy the transaction type reference data (AWS.M2.CARDDEMO.TRANTYPE.PS) into a new, cataloged first generation of the transaction type backup (AWS.M2.CARDDEMO.TRANTYPE.BKUP), with fixed-length 60-byte records. Rules: TTRDM-BR-160.
- **TTRDM-REQ-F-149** (design note): When every earlier step of the setup job ended with return code 0, the system shall copy the transaction category reference data (AWS.M2.CARDDEMO.TRANCATG.PS) into a new, cataloged first generation of the transaction category backup (AWS.M2.CARDDEMO.TRANCATG.PS.BKUP), with fixed-length 60-byte records. Rules: TTRDM-BR-161.
- **TTRDM-REQ-F-150** (design note): When every earlier step of the setup job ended with return code 0, the system shall copy the disclosure group reference data (AWS.M2.CARDDEMO.DISCGRP.PS) into a new, cataloged first generation of the disclosure group backup (AWS.M2.CARDDEMO.DISCGRP.BKUP), with fixed-length 50-byte records. Rules: TTRDM-BR-162.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-159 | Prepare the transaction type backup | design note | THE Transaction Reference Backup Setup SHALL first define the transaction type backup generation group (AWS.M2.CARDDEMO.TRANTYPE.BKUP), keeping at most 5 generations and deleting the oldest when a sixth is added, before any reference data is loaded. | medium | app/jcl/DEFGDGD.jcl:22-32 |
| TTRDM-BR-160 | Load first transaction type backup generation | design note | WHEN the step that defines the transaction type backup group ended with return code 0, THE Transaction Reference Backup Setup SHALL copy the transaction type reference data (AWS.M2.CARDDEMO.TRANTYPE.PS) into a new, cataloged first generation of the transaction type backup (AWS.M2.CARDDEMO.TRANTYPE.BKUP), with fixed-length 60-byte records. | medium | app/jcl/DEFGDGD.jcl:24-43 |
| TTRDM-BR-161 | Load first transaction category generation | design note | WHEN every earlier step of the setup job ended with return code 0, THE Transaction Reference Backup Setup SHALL copy the transaction category reference data (AWS.M2.CARDDEMO.TRANCATG.PS) into a new, cataloged first generation of the transaction category backup (AWS.M2.CARDDEMO.TRANCATG.PS.BKUP), with fixed-length 60-byte records. | medium | app/jcl/DEFGDGD.jcl:47-66 |
| TTRDM-BR-162 | Load first disclosure group generation | design note | WHEN every earlier step of the setup job ended with return code 0, THE Transaction Reference Backup Setup SHALL copy the disclosure group reference data (AWS.M2.CARDDEMO.DISCGRP.PS) into a new, cataloged first generation of the disclosure group backup (AWS.M2.CARDDEMO.DISCGRP.BKUP), with fixed-length 50-byte records. | medium | app/jcl/DEFGDGD.jcl:82-89 |

### Key entities

None found in the source.

### Needs clarification

- SME-249: How many versions of each reference data backup (transaction types, categories, disclosure groups) must be kept, and what happens when that limit is reached? (Batch operations) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-250: Are 'disclosure group' and 'discount group' the same business data, and which name should the new system use? (Business data owner) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-251: The reference data backups use fixed-length records of different lengths. Must the new backups keep that fixed layout, or only the same content? (Data architecture) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-252: The backup job notes it can be restarted at the transaction category step. Is restarting from that point required, and what happens to a transaction type backup already made before the restart? (Batch operations) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-253: Must the backup job set up the transaction type backup history first, before any reference data is copied into any backup? (Batch operations) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- DEF-129: Is this intended? STEP50, which defines the disclosure group backup group, has no COND, so it runs even after an earlier step fails. STEP60, which loads that group, is then skipped because of the earlier failure, so the job can leave an empty disclosure group backup group behind. (Subject-matter expert) On TTRDM-BR-162.

### Decision table gaps

None.
