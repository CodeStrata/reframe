# Design: Set up reference data backups (TTRDM-C22)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Sets up the backup history for the transaction type, transaction category and disclosure group reference data, and takes the first backup of each, so earlier versions can be recovered. At most five transaction type backups are kept, and the oldest is removed when a sixth is added. A backup must only be taken if the steps before it succeeded.

Runs as scheduled job.

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

- TTRDM-BR-159: The new application needs versioned backup storage for the transaction type reference data, such as dated snapshots or object versions. It must keep at most 5 versions and remove the oldest automatically when a sixth is written. The retention policy has to exist before any backup is written.
- TTRDM-BR-160: This is a setup step that runs only after the retention policy step succeeds. It copies the current transaction type extract (60-character records) into the first backup version and records it so later jobs can find it.
- TTRDM-BR-161: This setup step runs only if every earlier step succeeded. It snapshots the current transaction category extract (60-character records) as the first backup version of the category data.
- TTRDM-BR-162: This setup step runs only if every earlier step succeeded. It snapshots the current disclosure group extract (50-character records) as the first backup version of the disclosure group data.

## Open questions

- SME-249: How many versions of each reference data backup (transaction types, categories, disclosure groups) must be kept, and what happens when that limit is reached? (Batch operations) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-250: Are 'disclosure group' and 'discount group' the same business data, and which name should the new system use? (Business data owner) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-251: The reference data backups use fixed-length records of different lengths. Must the new backups keep that fixed layout, or only the same content? (Data architecture) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-252: The backup job notes it can be restarted at the transaction category step. Is restarting from that point required, and what happens to a transaction type backup already made before the restart? (Batch operations) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- SME-253: Must the backup job set up the transaction type backup history first, before any reference data is copied into any backup? (Batch operations) On TTRDM-BR-162, TTRDM-BR-160, TTRDM-BR-159, TTRDM-BR-161.
- DEF-129: Is this intended? STEP50, which defines the disclosure group backup group, has no COND, so it runs even after an earlier step fails. STEP60, which loads that group, is then skipped because of the earlier failure, so the job can leave an empty disclosure group backup group behind. (Subject-matter expert) On TTRDM-BR-162.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).