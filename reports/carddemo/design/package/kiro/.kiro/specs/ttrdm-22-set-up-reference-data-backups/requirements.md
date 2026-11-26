# Requirements: Set up reference data backups (TTRDM-C22)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as scheduled job · risk medium

## Introduction

Sets up the backup history for the transaction type, transaction category and disclosure group reference data, and takes the first backup of each, so earlier versions can be recovered. At most five transaction type backups are kept, and the oldest is removed when a sixth is added. A backup must only be taken if the steps before it succeeded.

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
