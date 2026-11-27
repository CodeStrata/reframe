# Feature specification: Load disclosure group and category balance masters

**Feature:** DTPR-C12 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C12)

As a card operations team, I want the disclosure group master and the transaction category balance file loaded from their flat files, so that interest calculation and posting work from current reference and balance data.

Loads the disclosure group master (interest rates by group, type and category) and the transaction category balance file from their flat files. The disclosure master is fully replaced on each load. It serves the card operations team, so interest and posting work from current data. It must replace the disclosure groups completely rather than merge them, it must not fail when there is no previous master, and nothing else may write to these files during the load.

**Acceptance scenarios:**

1. **Given** Existing master: 10 records; Flat file: 4 records, **when** Load disclosure group master from flat file applies, **then** After the job the master holds only the 4 records from the flat file (DTPR-C12-AC-01)
2. **Given** Existing master: none, **when** Load disclosure group master from flat file applies, **then** The delete step ends with return code 0 and the master is defined and loaded (DTPR-C12-AC-02)
3. **Given** Disclosure group flat file: 3 records of 50 bytes, **when** Disclosure Group Master Load runs, **then** The disclosure group master holds the same 3 records after the job (DTPR-C12-AC-03)
4. **Given** Records in flat category balance file: 120, **when** Transaction Category Balance Load runs, **then** The keyed category balance file holds the same 120 records after the load. (DTPR-C12-AC-04)
5. **Given** Another job using the keyed file: yes, **when** Transaction Category Balance Load runs, **then** The load waits for or is refused exclusive use of the keyed file; the flat file can still be read by others. (DTPR-C12-AC-05)

## Requirements

### Functional requirements

- **DTPR-REQ-F-067** (design note): Before loading, the system shall delete any existing disclosure group master and define it afresh as a keyed file of 50-byte records with a 16-byte key, so that the master is fully replaced rather than updated. Rules: DTPR-BR-074.
- **DTPR-REQ-N-006** (design note): If no disclosure group master exists when the load deletes it, then the system shall not treat this as an error. Rules: DTPR-BR-074.
- **DTPR-REQ-F-068** (design note): The system shall copy every record of the disclosure group flat file (AWS.M2.CARDDEMO.DISCGRP.PS, read shared) into the disclosure group master (AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS), holding the master for exclusive use during the load. Rules: DTPR-BR-075.
- **DTPR-REQ-F-069** (design note): The system shall copy every transaction category balance record from the flat file (AWS.M2.CARDDEMO.TCATBALF.PS, read shared with other jobs) into the keyed category balance file (AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS), holding the keyed file for exclusive use during the load. Rules: DTPR-BR-076.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-074 | Load disclosure group master from flat file | design note | BEFORE loading, THE Disclosure Group Master Load SHALL delete any existing disclosure group master and define it afresh as a keyed file of 50-byte records with a 16-byte key, so the master is fully replaced rather than updated, and a missing master is not treated as an error. | medium | app/jcl/DISCGRP.jcl:22-28, app/jcl/DISCGRP.jcl:33-49, app/jcl/DISCGRP.jcl:54-61 |
| DTPR-BR-075 | Load disclosure group master from flat file | design note | THE Disclosure Group Master Load SHALL copy every record of the disclosure group flat file (AWS.M2.CARDDEMO.DISCGRP.PS, read shared) into the disclosure group master (AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS), holding the master for exclusive use during the load. | medium | app/jcl/DISCGRP.jcl:22-28, app/jcl/DISCGRP.jcl:33-49, app/jcl/DISCGRP.jcl:54-61 |
| DTPR-BR-076 | Load category balances into keyed file | design note | THE Transaction Category Balance Load SHALL copy every transaction category balance record from the flat file (AWS.M2.CARDDEMO.TCATBALF.PS) into the keyed category balance file (AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS), reading the flat file shared with other jobs and holding the keyed file for exclusive use during the load. | medium | app/jcl/TCATBALF.jcl:54-61, app/jcl/TCATBALF.jcl:22-49 |

### Key entities

None found in the source.

### Needs clarification

- SME-250: Are 'disclosure group' and 'discount group' the same business data, and which name should the new system use? (Business data owner) On DTPR-BR-075.
- SME-254: When loading the disclosure group master, should the load replace existing records, add to them, or require an empty store? (Batch operations) On DTPR-BR-075.
- SME-255: When loading the disclosure group master, how should duplicate keys and failed writes be handled, and can the load be safely re-run after an interruption? (Batch operations) On DTPR-BR-075.
- SME-282: When loading category balances, should existing records be cleared, replaced, or kept, and how should a record whose key already exists be handled? (Batch operations / data owner) On DTPR-BR-076.
- SME-283: If the category balance load fails partway, what recovery is required (keep the partial load, roll back, or restart)? (Batch operations) On DTPR-BR-076.
- SME-284: What must the operations listing from the category balance load contain (for example, record counts or error details)? (Batch operations) On DTPR-BR-076.

### Decision table gaps

None.
