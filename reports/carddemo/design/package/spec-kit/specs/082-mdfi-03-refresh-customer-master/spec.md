# Feature specification: Refresh customer master

**Feature:** MDFI-C03 · Master Data File Initialization · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (MDFI-C03)

As a CardDemo operations team member, I want to rebuild the customer master from the customer flat file while online access to it is suspended, so that customer data is reloaded completely and online users do not read it mid-rebuild.

Rebuilds the customer master from the customer flat file while online access to customers is suspended, so that the reload is complete and no online user reads a half-built customer store. Each customer is keyed by a 9-character customer ID at the start of its 500-byte record. The refresh must load every record, print a report of what it copied, and always bring online access back once the load ends.

**Acceptance scenarios:**

1. **Given** CICS region: CICSAWSA; file: CUSTDAT, **when** Customer Master Refresh job runs, **then** The file is set closed ('CEMT SET FIL(CUSTDAT ) CLO') before the reload and opened ('CEMT SET FIL(CUSTDAT ) OPE') after it. (MDFI-C03-AC-01)
2. **Given** customer master: exists with old data, **when** Customer Master Refresh job runs, **then** It is deleted and an empty master is defined with key length 9 at offset 0 and record size 500. (MDFI-C03-AC-02)
3. **Given** customer master: does not exist, **when** Customer Master Refresh job runs, **then** The delete fails with a condition code of 8 or less, which is reset to 0, and the job goes on to define the master. (MDFI-C03-AC-03)
4. **Given** customer flat file: 50 customer records, **when** Customer Master Refresh job runs, **then** The customer master holds the same 50 records, keyed by customer ID, and the copy report is written to the job output. (MDFI-C03-AC-04)

## Requirements

### Functional requirements

- **MDFI-REQ-F-006** (design note): The system shall close the customer file (CUSTDAT) in the online CICS region before the refresh and reopen it after the load, so that online users cannot read the customer master while it is rebuilt. Rules: MDFI-BR-006.
- **MDFI-REQ-F-007** (design note): The system shall delete the existing keyed customer master (AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS) and define it anew with a 9-character customer key at the start of each 500-byte record, treating a master that does not yet exist as no error. Rules: MDFI-BR-007.
- **MDFI-REQ-F-008** (design note): The system shall copy every record of the customer flat file (AWS.M2.CARDDEMO.CUSTDATA.PS) into the newly defined keyed customer master and print a processing report of the copy. Rules: MDFI-BR-008.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| MDFI-BR-006 | Load customer master from flat file | design note | THE Customer Master Refresh job SHALL close the customer file (CUSTDAT) in the online CICS region before the refresh and reopen it after the load, so online users cannot read the customer master while it is rebuilt. | medium | app/jcl/CUSTFILE.jcl:22-27, app/jcl/CUSTFILE.jcl:32-38, app/jcl/CUSTFILE.jcl:43-59, app/jcl/CUSTFILE.jcl:64-72 |
| MDFI-BR-007 | Load customer master from flat file | design note | THE Customer Master Refresh job SHALL delete the existing keyed customer master (AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS) and define it anew with a 9-character customer key at the start of each 500-byte record, treating a master that does not yet exist as no error. | medium | app/jcl/CUSTFILE.jcl:22-27, app/jcl/CUSTFILE.jcl:32-38, app/jcl/CUSTFILE.jcl:43-59, app/jcl/CUSTFILE.jcl:64-72 |
| MDFI-BR-008 | Load customer master from flat file | design note | THE Customer Master Refresh job SHALL copy every record of the customer flat file (AWS.M2.CARDDEMO.CUSTDATA.PS) into the newly defined keyed customer master and print a processing report of the copy. | medium | app/jcl/CUSTFILE.jcl:22-27, app/jcl/CUSTFILE.jcl:32-38, app/jcl/CUSTFILE.jcl:43-59, app/jcl/CUSTFILE.jcl:64-72 |

### Key entities

None found in the source.

### Needs clarification

- SME-240: When loading customers from the flat file, what should happen if a customer already exists in the customer master: replace it, reject the record, or stop the load? (Data migration) On MDFI-BR-008.
- SME-241: What must the customer load's processing report contain (counts, errors, statuses)? (Batch operations) On MDFI-BR-008.
- SME-242: If the customer load stops after writing some records, how should it be restarted or recovered? (Batch operations) On MDFI-BR-008.
- SME-243: During the customer load, other processes can read or change the customer files. Is that acceptable, or must the files be locked for the load? (Data migration) On MDFI-BR-008.

### Decision table gaps

None.
