# Set up reference data backups (TTRDM-C22)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as scheduled job · risk medium

## Introduction

A one-time setup job for operations that creates the backup history for the transaction type, transaction category and disclosure group reference data, and stores a first backup copy of each. Each backup runs only when the earlier steps succeeded, and the transaction type history keeps at most five copies.

**User story:** As an operations user, I want to create the backup generations for transaction type, category and disclosure group reference data, so that earlier versions of the reference data can be kept.

## Requirements

### Requirement 1: TTRDM-REQ-F-147 (design note)

#### Acceptance criteria

1. The system shall first define the transaction type backup generation group (AWS.M2.CARDDEMO.TRANTYPE.BKUP), keeping at most 5 generations and deleting the oldest when a sixth is added, before any reference data is loaded. (rules TTRDM-BR-159)
2. GIVEN generations of AWS.M2.CARDDEMO.TRANTYPE.BKUP: 5 already exist; new backup: 1 more created WHEN Transaction Reference Backup Setup runs THEN The oldest generation is removed and scratched, leaving 5 (TTRDM-C22-AC-01; TTRDM-BR-159)

### Requirement 2: TTRDM-REQ-F-148 (design note)

#### Acceptance criteria

1. When the step that defines the transaction type backup group ended with return code 0, the system shall copy the transaction type reference data (AWS.M2.CARDDEMO.TRANTYPE.PS) into a new, cataloged first generation of the transaction type backup (AWS.M2.CARDDEMO.TRANTYPE.BKUP), with fixed-length 60-byte records. (rules TTRDM-BR-160)
2. GIVEN step 10 return code: 0 WHEN the step that defines the transaction type backup group ended with return code 0 THEN A new generation of AWS.M2.CARDDEMO.TRANTYPE.BKUP is created and cataloged, holding a copy of AWS.M2.CARDDEMO.TRANTYPE.PS (TTRDM-C22-AC-02; TTRDM-BR-160)
3. GIVEN step 10 return code: 12 WHEN the step that defines the transaction type backup group ended with return code 0 THEN The copy step is skipped (TTRDM-C22-AC-03; TTRDM-BR-160)

### Requirement 3: TTRDM-REQ-F-149 (design note)

#### Acceptance criteria

1. When every earlier step of the setup job ended with return code 0, the system shall copy the transaction category reference data (AWS.M2.CARDDEMO.TRANCATG.PS) into a new, cataloged first generation of the transaction category backup (AWS.M2.CARDDEMO.TRANCATG.PS.BKUP), with fixed-length 60-byte records. (rules TTRDM-BR-161)
2. GIVEN return codes of steps 10-30: all 0 WHEN every earlier step of the setup job ended with return code 0 THEN A new generation of AWS.M2.CARDDEMO.TRANCATG.PS.BKUP is created and cataloged, holding a copy of AWS.M2.CARDDEMO.TRANCATG.PS (TTRDM-C22-AC-04; TTRDM-BR-161)
3. GIVEN step 30 return code: 12 WHEN every earlier step of the setup job ended with return code 0 THEN The copy step is skipped (TTRDM-C22-AC-05; TTRDM-BR-161)

### Requirement 4: TTRDM-REQ-F-150 (design note)

#### Acceptance criteria

1. When every earlier step of the setup job ended with return code 0, the system shall copy the disclosure group reference data (AWS.M2.CARDDEMO.DISCGRP.PS) into a new, cataloged first generation of the disclosure group backup (AWS.M2.CARDDEMO.DISCGRP.BKUP), with fixed-length 50-byte records. (rules TTRDM-BR-162)
2. GIVEN return codes of steps 10-50: all 0 WHEN every earlier step of the setup job ended with return code 0 THEN A new generation of AWS.M2.CARDDEMO.DISCGRP.BKUP is created and cataloged, holding a copy of AWS.M2.CARDDEMO.DISCGRP.PS (TTRDM-C22-AC-06; TTRDM-BR-162)
3. GIVEN step 10 return code: 12 (transaction type backup group already defined) WHEN every earlier step of the setup job ended with return code 0 THEN The disclosure group copy step is skipped (TTRDM-C22-AC-07; TTRDM-BR-162)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-159 | Prepare the transaction type backup | design note | THE Transaction Reference Backup Setup SHALL first define the transaction type backup generation group (AWS.M2.CARDDEMO.TRANTYPE.BKUP), keeping at most 5 generations and deleting the oldest when a sixth is added, before any reference data is loaded. | medium | app/jcl/DEFGDGD.jcl:22-32 |
| TTRDM-BR-160 | Load first transaction type backup generation | design note | WHEN the step that defines the transaction type backup group ended with return code 0, THE Transaction Reference Backup Setup SHALL copy the transaction type reference data (AWS.M2.CARDDEMO.TRANTYPE.PS) into a new, cataloged first generation of the transaction type backup (AWS.M2.CARDDEMO.TRANTYPE.BKUP), with fixed-length 60-byte records. | medium | app/jcl/DEFGDGD.jcl:24-43 |
| TTRDM-BR-161 | Load first transaction category generation | design note | WHEN every earlier step of the setup job ended with return code 0, THE Transaction Reference Backup Setup SHALL copy the transaction category reference data (AWS.M2.CARDDEMO.TRANCATG.PS) into a new, cataloged first generation of the transaction category backup (AWS.M2.CARDDEMO.TRANCATG.PS.BKUP), with fixed-length 60-byte records. | medium | app/jcl/DEFGDGD.jcl:47-66 |
| TTRDM-BR-162 | Load first disclosure group generation | design note | WHEN every earlier step of the setup job ended with return code 0, THE Transaction Reference Backup Setup SHALL copy the disclosure group reference data (AWS.M2.CARDDEMO.DISCGRP.PS) into a new, cataloged first generation of the disclosure group backup (AWS.M2.CARDDEMO.DISCGRP.BKUP), with fixed-length 50-byte records. | medium | app/jcl/DEFGDGD.jcl:82-89 |

### Worked examples

- TTRDM-BR-159: generations of AWS.M2.CARDDEMO.TRANTYPE.BKUP = 5 already exist; new backup = 1 more created → The oldest generation is removed and scratched, leaving 5
- TTRDM-BR-160: step 10 return code = 0 → A new generation of AWS.M2.CARDDEMO.TRANTYPE.BKUP is created and cataloged, holding a copy of AWS.M2.CARDDEMO.TRANTYPE.PS
- TTRDM-BR-160: step 10 return code = 12 → The copy step is skipped
- TTRDM-BR-161: return codes of steps 10-30 = all 0 → A new generation of AWS.M2.CARDDEMO.TRANCATG.PS.BKUP is created and cataloged, holding a copy of AWS.M2.CARDDEMO.TRANCATG.PS
- TTRDM-BR-161: step 30 return code = 12 → The copy step is skipped
- TTRDM-BR-162: return codes of steps 10-50 = all 0 → A new generation of AWS.M2.CARDDEMO.DISCGRP.BKUP is created and cataloged, holding a copy of AWS.M2.CARDDEMO.DISCGRP.PS
- TTRDM-BR-162: step 10 return code = 12 (transaction type backup group already defined) → The disclosure group copy step is skipped

## Decision tables

None.

## Design notes

- TTRDM-BR-159: A versioned backup location for transaction type snapshots, such as a versioned object-store prefix or a backup table keyed by snapshot date. It needs a retention policy that keeps the five newest versions and removes the oldest when a sixth is written. It must exist before the first snapshot is taken.
- TTRDM-BR-160: A job step that runs only when the backup location was set up successfully. It writes a first snapshot of the current transaction type reference data, unchanged and in its 60-character record layout, as a new recorded version in that location.
- TTRDM-BR-161: A job step that runs only when every earlier step succeeded. It writes a first snapshot of the current transaction category reference data, unchanged and in its 60-character record layout, as a new recorded version in the category backup location.
- TTRDM-BR-162: A job step that runs only when every earlier step succeeded. It writes a first snapshot of the current disclosure group reference data, unchanged and in its 50-character record layout, as a new recorded version in the disclosure group backup location.

## Open questions

- SME-249: How many versions of each reference data backup (transaction types, categories, disclosure groups) must be kept, and what happens when that limit is reached? (Batch operations) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-250: Are 'disclosure group' and 'discount group' the same business data, and which name should the new system use? (Business data owner) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-251: The reference data backups use fixed-length records of different lengths. Must the new backups keep that fixed layout, or only the same content? (Data architecture) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-252: The backup job notes it can be restarted at the transaction category step. Is restarting from that point required, and what happens to a transaction type backup already made before the restart? (Batch operations) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-253: Must the backup job set up the transaction type backup history first, before any reference data is copied into any backup? (Batch operations) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- DEF-129: Is this intended? STEP50, which defines the disclosure group backup group, has no COND, so it runs even after an earlier step fails. STEP60, which loads that group, is then skipped because of the earlier failure, so the job can leave an empty disclosure group backup group behind. (Subject-matter expert) On TTRDM-BR-162.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).
