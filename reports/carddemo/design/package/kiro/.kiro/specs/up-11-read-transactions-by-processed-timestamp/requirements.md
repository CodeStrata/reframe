# Requirements: Read transactions by processed timestamp (UP-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk low

## Introduction

Gives batch processes a way to read transactions in the order they were processed, by keeping a secondary index on the processed timestamp of the transaction master. Many transactions may share a timestamp. The index must include every transaction on the master.

**User story:** As a CardDemo batch process, I want an alternate index on the transaction master keyed on processed timestamp, so that transactions can be read by when they were processed.

## Requirements

### Requirement 1: UP-REQ-F-048 (design note)

#### Acceptance criteria

1. The system shall read every record of the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) and fill the alternate index (AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX) with entries keyed on each transaction's processed timestamp. (rules UP-BR-051)
2. GIVEN A transaction master holding three transactions, two of them with the same processed timestamp WHEN The alternate index is built THEN The index holds an entry for every one of the three transactions, keyed on its processed timestamp. Reading by that timestamp returns both transactions that share it. (UP-C11-AC-02; UP-BR-051)

### Requirement 2: UP-REQ-F-049 (design note)

#### Acceptance criteria

1. The system shall define an access path (AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX.PATH) over the transaction alternate index, keyed on the transaction processed timestamp where many transactions may share the same timestamp, through which transaction records are read by processed timestamp. (rules UP-BR-052)
2. GIVEN Job: TRANIDX; Alternate index: AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX defined in STEP20 WHEN Transaction Alternate Index Setup runs THEN STEP25 defines path AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX.PATH, so transactions can be read by processed timestamp (UP-C11-AC-01; UP-BR-052)
