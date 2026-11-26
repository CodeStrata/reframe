# Feature specification: Read transactions by processed timestamp

**Feature:** UP-C11 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C11)

As a CardDemo batch process, I want an alternate index on the transaction master keyed on processed timestamp, so that transactions can be read by when they were processed.

Gives batch processes a way to read transactions in the order they were processed, by keeping a secondary index on the processed timestamp of the transaction master. Many transactions may share a timestamp. The index must include every transaction on the master.

**Acceptance scenarios:**

1. **Given** Job: TRANIDX; Alternate index: AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX defined in STEP20, **when** Transaction Alternate Index Setup runs, **then** STEP25 defines path AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX.PATH, so transactions can be read by processed timestamp (UP-C11-AC-01)
2. **Given** A transaction master holding three transactions, two of them with the same processed timestamp, **when** The alternate index is built, **then** The index holds an entry for every one of the three transactions, keyed on its processed timestamp. Reading by that timestamp returns both transactions that share it. (UP-C11-AC-02)

## Requirements

### Functional requirements

- **UP-REQ-F-048** (design note): The system shall read every record of the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) and fill the alternate index (AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX) with entries keyed on each transaction's processed timestamp. Rules: UP-BR-051.
- **UP-REQ-F-049** (design note): The system shall define an access path (AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX.PATH) over the transaction alternate index, keyed on the transaction processed timestamp where many transactions may share the same timestamp, through which transaction records are read by processed timestamp. Rules: UP-BR-052.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-051 | Build transaction alternate index | design note | THE Transaction Alternate Index Setup SHALL read every record of the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) and fill the alternate index (AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX) with entries keyed on each transaction's processed timestamp, so transactions can be read by processed timestamp. | medium | app/jcl/TRANIDX.jcl:46-54, app/jcl/TRANIDX.jcl:25-28, app/cpy/CVTRA05Y.cpy:4-18 |
| UP-BR-052 | Define transaction alternate-key access path | design note | THE Transaction Alternate Index Setup SHALL define an access path (AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX.PATH) over the transaction alternate index that the job defines in the step before. That index is keyed on the transaction processed timestamp, and many transactions may share the same timestamp. This path is how transaction records are read by processed timestamp. | medium | app/jcl/TRANIDX.jcl:19-34, app/jcl/TRANIDX.jcl:36-44, app/cpy/CVTRA05Y.cpy:4-18 |

### Key entities

None found in the source.

### Needs clarification

None.

### Decision table gaps

None.
