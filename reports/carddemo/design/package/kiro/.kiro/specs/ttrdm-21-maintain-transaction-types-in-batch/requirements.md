# Requirements: Maintain transaction types in batch (TTRDM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as scheduled job · risk medium

## Introduction

Operations staff can apply a file of transaction type add, update and delete requests in one batch run instead of keying them in one at a time. Each line of the file carries an action, a two-digit type code and a description, and the run reports its messages in the job output. The run must apply each request exactly as the line states.

**User story:** As an operations user, I want to apply a file of transaction type add, update and delete requests in a batch job, so that many reference data changes can be made at once.

## Requirements

### Requirement 1: TTRDM-REQ-F-145 (design note)

#### Acceptance criteria

1. The system shall run the transaction type update program (COBTUPDT) under Db2 subsystem 'DAZ1' with plan 'CARDDEMO', reading the maintenance request file (INPFILE) as shared input and writing the run's messages to the job output. (rules TTRDM-BR-157)
2. GIVEN A maintenance request file (INPFILE) is available and the transaction type update program (COBTUPDT) is configured against Db2 subsystem 'DAZ1' with plan 'CARDDEMO' WHEN The transaction type maintenance job is run THEN The program reads the request file as shared input, so other readers are not locked out, applies the requests to the transaction type table, and the run's messages appear in the job output (TTRDM-C21-AC-02; TTRDM-BR-157)

### Requirement 2: TTRDM-REQ-F-146 (business rule)

#### Acceptance criteria

1. The system shall read the maintenance request file as one request per line, where column 1 is the action ('A' add, 'D' delete, 'U' update, '*' comment), columns 2-3 the numeric transaction type, and columns 4-53 the transaction description. (rules TTRDM-BR-158)
2. GIVEN request line: * weekly refresh WHEN maintenance request file runs THEN the line is treated as a comment (TTRDM-C21-AC-01; TTRDM-BR-158)
