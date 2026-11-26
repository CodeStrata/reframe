# Requirements: Maintain transaction types in batch (TTRDM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as scheduled job · risk medium

## Introduction

Lets operations apply a file of transaction type add, update and delete requests to the transaction type table in one batch run, writing a log of the run. Each line holds one request: an action code ('A', 'U', 'D', or '*' for a comment), a two-digit numeric type code and a description of up to 50 characters. The job must apply each request exactly as the file states and report what it did.

**User story:** As an operations user, I want to apply a file of transaction type add, update and delete requests in a batch job, so that many reference data changes can be made at once.

## Requirements

### Requirement 1: TTRDM-REQ-F-145 (design note)

#### Acceptance criteria

1. The system shall run the transaction type update program (COBTUPDT) under Db2 subsystem 'DAZ1' with plan 'CARDDEMO', reading the maintenance request file (INPFILE) as shared input and writing the run's messages to the job output. (rules TTRDM-BR-157)
2. GIVEN A maintenance request file (INPFILE) is available, and the database is the CARDDEMO plan on Db2 subsystem 'DAZ1' WHEN The transaction type maintenance job runs THEN The transaction type update program (COBTUPDT) reads the request file as shared input (other readers are not locked out) and writes the run's messages to the job output (TTRDM-C21-AC-02; TTRDM-BR-157)

### Requirement 2: TTRDM-REQ-F-146 (business rule)

#### Acceptance criteria

1. The system shall read the maintenance request file as one request per line, where column 1 is the action ('A' add, 'D' delete, 'U' update, '*' comment), columns 2-3 the numeric transaction type, and columns 4-53 the transaction description. (rules TTRDM-BR-158)
2. GIVEN request line: * weekly refresh WHEN maintenance request file runs THEN the line is treated as a comment (TTRDM-C21-AC-01; TTRDM-BR-158)
