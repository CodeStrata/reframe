# Load disclosure group and category balance masters (DTPR-C12)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Loads the disclosure group master (interest rates by group, type and category) and the transaction category balance file from their flat files. The disclosure master is fully replaced on each load. It serves the card operations team, so interest and posting work from current data. It must replace the disclosure groups completely rather than merge them, it must not fail when there is no previous master, and nothing else may write to these files during the load.

**User story:** As a card operations team, I want the disclosure group master and the transaction category balance file loaded from their flat files, so that interest calculation and posting work from current reference and balance data.

## Requirements

### Requirement 1: DTPR-REQ-F-067 (design note)

#### Acceptance criteria

1. Before loading, the system shall delete any existing disclosure group master and define it afresh as a keyed file of 50-byte records with a 16-byte key, so that the master is fully replaced rather than updated. (rules DTPR-BR-074)
2. GIVEN Existing master: 10 records; Flat file: 4 records WHEN Load disclosure group master from flat file applies THEN After the job the master holds only the 4 records from the flat file (DTPR-C12-AC-01; DTPR-BR-074)
3. GIVEN Existing master: none WHEN Load disclosure group master from flat file applies THEN The delete step ends with return code 0 and the master is defined and loaded (DTPR-C12-AC-02; DTPR-BR-074)

### Requirement 2: DTPR-REQ-N-006 (design note)

#### Acceptance criteria

1. If no disclosure group master exists when the load deletes it, then the system shall not treat this as an error. (rules DTPR-BR-074)
2. GIVEN Existing master: 10 records; Flat file: 4 records WHEN Load disclosure group master from flat file applies THEN After the job the master holds only the 4 records from the flat file (DTPR-C12-AC-01; DTPR-BR-074)
3. GIVEN Existing master: none WHEN Load disclosure group master from flat file applies THEN The delete step ends with return code 0 and the master is defined and loaded (DTPR-C12-AC-02; DTPR-BR-074)

### Requirement 3: DTPR-REQ-F-068 (design note)

#### Acceptance criteria

1. The system shall copy every record of the disclosure group flat file (AWS.M2.CARDDEMO.DISCGRP.PS, read shared) into the disclosure group master (AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS), holding the master for exclusive use during the load. (rules DTPR-BR-075)
2. GIVEN Disclosure group flat file: 3 records of 50 bytes WHEN Disclosure Group Master Load runs THEN The disclosure group master holds the same 3 records after the job (DTPR-C12-AC-03; DTPR-BR-075)

### Requirement 4: DTPR-REQ-F-069 (design note)

#### Acceptance criteria

1. The system shall copy every transaction category balance record from the flat file (AWS.M2.CARDDEMO.TCATBALF.PS, read shared with other jobs) into the keyed category balance file (AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS), holding the keyed file for exclusive use during the load. (rules DTPR-BR-076)
2. GIVEN Records in flat category balance file: 120 WHEN Transaction Category Balance Load runs THEN The keyed category balance file holds the same 120 records after the load. (DTPR-C12-AC-04; DTPR-BR-076)
3. GIVEN Another job using the keyed file: yes WHEN Transaction Category Balance Load runs THEN The load waits for or is refused exclusive use of the keyed file; the flat file can still be read by others. (DTPR-C12-AC-05; DTPR-BR-076)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-074 | Load disclosure group master from flat file | design note | BEFORE loading, THE Disclosure Group Master Load SHALL delete any existing disclosure group master and define it afresh as a keyed file of 50-byte records with a 16-byte key, so the master is fully replaced rather than updated, and a missing master is not treated as an error. | medium | app/jcl/DISCGRP.jcl:22-28, app/jcl/DISCGRP.jcl:33-49, app/jcl/DISCGRP.jcl:54-61 |
| DTPR-BR-075 | Load disclosure group master from flat file | design note | THE Disclosure Group Master Load SHALL copy every record of the disclosure group flat file (AWS.M2.CARDDEMO.DISCGRP.PS, read shared) into the disclosure group master (AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS), holding the master for exclusive use during the load. | medium | app/jcl/DISCGRP.jcl:22-28, app/jcl/DISCGRP.jcl:33-49, app/jcl/DISCGRP.jcl:54-61 |
| DTPR-BR-076 | Load category balances into keyed file | design note | THE Transaction Category Balance Load SHALL copy every transaction category balance record from the flat file (AWS.M2.CARDDEMO.TCATBALF.PS) into the keyed category balance file (AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS), reading the flat file shared with other jobs and holding the keyed file for exclusive use during the load. | medium | app/jcl/TCATBALF.jcl:54-61, app/jcl/TCATBALF.jcl:22-49 |

### Worked examples

- DTPR-BR-074: Existing master = 10 records; Flat file = 4 records → After the job the master holds only the 4 records from the flat file
- DTPR-BR-074: Existing master = none → The delete step ends with return code 0 and the master is defined and loaded
- DTPR-BR-075: Disclosure group flat file = 3 records of 50 bytes → The disclosure group master holds the same 3 records after the job
- DTPR-BR-076: Records in flat category balance file = 120 → The keyed category balance file holds the same 120 records after the load.
- DTPR-BR-076: Another job using the keyed file = yes → The load waits for or is refused exclusive use of the keyed file; the flat file can still be read by others.

## Decision tables

None.

## Design notes

- DTPR-BR-074: Make the disclosure group load a full replace: clear or recreate the store, keyed on the 16-character key of group ID, type and category over 50-byte records, before loading. Treat an absent previous store as normal, not an error.
- DTPR-BR-075: Bulk-load every record of the disclosure group feed into the keyed disclosure group store. Load it as one unit (in a single transaction, or by swapping in a staging table) so the interest job never sees a partly loaded rate table.
- DTPR-BR-076: Bulk-load every category balance record from the flat feed into the category balance store, keyed on account ID, type and category. Hold exclusive write access during the load, and schedule it so it never overlaps the posting or interest jobs.

## Open questions

- SME-250: Are 'disclosure group' and 'discount group' the same business data, and which name should the new system use? (Business data owner) On DTPR-BR-075.
- SME-254: When loading the disclosure group master, should the load replace existing records, add to them, or require an empty store? (Batch operations) On DTPR-BR-075.
- SME-255: When loading the disclosure group master, how should duplicate keys and failed writes be handled, and can the load be safely re-run after an interruption? (Batch operations) On DTPR-BR-075.
- SME-282: When loading category balances, should existing records be cleared, replaced, or kept, and how should a record whose key already exists be handled? (Batch operations / data owner) On DTPR-BR-076.
- SME-283: If the category balance load fails partway, what recovery is required (keep the partial load, roll back, or restart)? (Batch operations) On DTPR-BR-076.
- SME-284: What must the operations listing from the category balance load contain (for example, record counts or error details)? (Batch operations) On DTPR-BR-076.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).
