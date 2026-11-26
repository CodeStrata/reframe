# Feature specification: Load reference data into keyed files

**Feature:** TTRDM-C24 · Transaction Type Reference Data Maintenance · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (TTRDM-C24)

As an operations user, I want to reload the keyed transaction type and category files from their flat files, so that online and batch programs read current reference data.

Reloads the keyed transaction type and category lookup stores from their latest flat files, so online screens and batch programs read current reference data. Each store is emptied and rebuilt in full. Every record in the file must be loaded, with none lost and none left over from the previous load.

**Acceptance scenarios:**

1. **Given** transaction category flat file: 18 category records; keyed category file before the run: exists with older records, **when** Transaction Category Reference Load runs, **then** The keyed file is deleted, redefined empty and loaded with exactly the 18 records from the flat file; the older records are gone. (TTRDM-C24-AC-01)
2. **Given** keyed category file before the run: does not exist, **when** Transaction Category Reference Load runs, **then** The failed delete is ignored (return code reset to 0), the file is defined and the flat-file records are loaded. (TTRDM-C24-AC-02)
3. **Given** transaction type flat file: 7 type records (codes 01 to 07); keyed type file before the run: exists with older records, **when** Transaction Type Reference Load runs, **then** The keyed file is deleted, redefined empty and loaded with exactly the 7 records; earlier contents are not kept. (TTRDM-C24-AC-03)

## Requirements

### Functional requirements

- **TTRDM-REQ-F-160** (design note): The system shall copy every record of the transaction category flat file (AWS.M2.CARDDEMO.TRANCATG.PS, read shared) into the keyed transaction category file (AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS, held exclusively), which the same job has just deleted and redefined empty, keyed on the first 6 characters of each 60-character record. Rules: TTRDM-BR-172.
- **TTRDM-REQ-F-161** (design note): The system shall copy every record of the transaction type flat file (AWS.M2.CARDDEMO.TRANTYPE.PS, read shared) into the keyed transaction type file (AWS.M2.CARDDEMO.TRANTYPE.VSAM.KSDS, held exclusively), which the same job has just deleted and redefined empty, keyed on the first 2 characters of each 60-character record. Rules: TTRDM-BR-173.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| TTRDM-BR-172 | Load transaction categories into keyed store | design note | THE Transaction Category Reference Load SHALL copy every record of the transaction category flat file (AWS.M2.CARDDEMO.TRANCATG.PS, read shared) into the keyed transaction category file (AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS, held exclusively), which the same job has just deleted and redefined empty, keyed on the first 6 characters of each 60-character record. | medium | app/jcl/TRANCATG.jcl:22-27, app/jcl/TRANCATG.jcl:33-49, app/jcl/TRANCATG.jcl:54-61 |
| TTRDM-BR-173 | Load transaction type master from flat file | design note | THE Transaction Type Reference Load SHALL copy every record of the transaction type flat file (AWS.M2.CARDDEMO.TRANTYPE.PS, read shared) into the keyed transaction type file (AWS.M2.CARDDEMO.TRANTYPE.VSAM.KSDS, held exclusively), which the same job has just deleted and redefined empty, keyed on the first 2 characters of each 60-character record. | medium | app/jcl/TRANTYPE.jcl:22-27, app/jcl/TRANTYPE.jcl:33-49, app/jcl/TRANTYPE.jcl:54-61 |

### Key entities

None found in the source.

### Needs clarification

- SME-286: When loading transaction categories, should records already in the store be replaced, merged, or rejected as duplicates? (Reference data owner) On TTRDM-BR-172.
- SME-287: If the transaction category load fails partway, should the partly loaded store be restored, or the load rerun from the start? (Batch operations team) On TTRDM-BR-172.
- SME-296: When loading the transaction type store, should records already present be cleared, replaced, or kept? (Reference data owner) On TTRDM-BR-173.
- SME-297: For the transaction type load, what should happen when a record cannot be written (for example, a duplicate key) or the load is interrupted, and must it be safe to rerun? (Batch operations team) On TTRDM-BR-173.

### Decision table gaps

None.
