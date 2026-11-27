# Requirements: Stop the statement run on file errors (ASGD-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Account Self-Service · Account Statement Generation and Delivery · runs as scheduled job · risk high

## Introduction

If any statement data cannot be opened, read or closed, the run stops with a clear message naming the file and the return code, and no statements from that run are issued. Its main audience is the statement operations team. It must never issue a statement built from missing customer or account data, and it must never carry on after a file error.

**User story:** As a statement operations team, I want the statement run to stop with a clear message when a file cannot be opened, read or closed, so that no incomplete statements are issued.

## Requirements

### Requirement 1: ASGD-REQ-F-026 (error handling)

#### Acceptance criteria

1. If the customer record for a cross-reference card cannot be read (any result other than '00'), then the system shall display 'ERROR READING CUSTFILE' with the return code and abend, producing no further statements. (rules ASGD-BR-027, ASGD-BR-028)
2. GIVEN A cross-reference card whose customer ID has no customer record, so the read returns '23' WHEN The statement run processes that card THEN The run displays 'ERROR READING CUSTFILE' with return code 23, then 'ABENDING PROGRAM', and abends. No statement is produced for that card or any card after it. (ASGD-C06-AC-02; ASGD-BR-027, ASGD-BR-028)

### Requirement 2: ASGD-REQ-F-027 (error handling)

#### Acceptance criteria

1. If the account record for a cross-reference card cannot be read (any result other than '00'), then the system shall display 'ERROR READING ACCTFILE' with the return code and abend. (rules ASGD-BR-029, ASGD-BR-028)
2. GIVEN A cross-reference card whose account ID has no account record, so the read returns '23' WHEN The statement run looks up the account THEN The run displays 'ERROR READING ACCTFILE' with return code 23, then 'ABENDING PROGRAM', and abends (ASGD-C06-AC-03; ASGD-BR-029, ASGD-BR-028)

### Requirement 3: ASGD-REQ-F-028 (error handling)

#### Acceptance criteria

1. If reading the next cross-reference record returns anything other than '00' or end of file '10', then the system shall display 'ERROR READING XREFFILE' with the return code and abend. (rules ASGD-BR-030, ASGD-BR-028)
2. GIVEN Reading the next cross-reference record returns a status other than '00' or '10' WHEN The statement run reads the cross-reference THEN The run displays 'ERROR READING XREFFILE' with that return code, then 'ABENDING PROGRAM', and abends. A status of '10' (end of file) ends the run normally, with no error. (ASGD-C06-AC-04; ASGD-BR-030, ASGD-BR-028)

### Requirement 4: ASGD-REQ-F-029 (error handling)

#### Acceptance criteria

1. If reading the cross-reference, customer or account file fails, then the system shall display the read error message with the return code, then 'ABENDING PROGRAM', and abend. (rules ASGD-BR-028)
2. GIVEN A read of the cross-reference, customer or account file fails WHEN The failure is detected THEN The matching message ('ERROR READING XREFFILE', 'ERROR READING CUSTFILE' or 'ERROR READING ACCTFILE') is displayed with the return code, followed by 'ABENDING PROGRAM', and the run abends (ASGD-C06-AC-05; ASGD-BR-028)

### Requirement 5: ASGD-REQ-F-030 (error handling)

#### Acceptance criteria

1. If opening, closing or making the first read of the transaction file, or opening or closing the cross-reference, customer or account file, returns anything other than '00' or '04', then the system shall display 'ERROR OPENING <file>', 'ERROR READING TRNXFILE' or 'ERROR CLOSING <file>' with the return code and abend. (rules ASGD-BR-031)
2. GIVEN Opening the account file returns a status other than '00' or '04'. Separately, the first read of the transaction file returns such a status, or closing the customer file does. WHEN The statement run performs that operation THEN The run displays 'ERROR OPENING <file>', 'ERROR READING TRNXFILE' or 'ERROR CLOSING <file>' respectively, with the return code, and abends. A status of '00' or '04' lets the run continue. (ASGD-C06-AC-06; ASGD-BR-031)

### Requirement 6: ASGD-REQ-F-031 (error handling)

#### Acceptance criteria

1. If a later read of the transaction file during loading returns anything other than '00' or end of file '10', then the system shall display 'ERROR READING TRNXFILE' with the return code and abend. (rules ASGD-BR-032)
2. GIVEN While the transactions are loading, a read after the first one returns a status other than '00' or '10' WHEN The statement run reads that transaction THEN The run displays 'ERROR READING TRNXFILE' with the return code and abends. A status of '10' ends loading normally. (ASGD-C06-AC-07; ASGD-BR-032)

### Requirement 7: ASGD-REQ-F-032 (error handling)

#### Acceptance criteria

1. If the statement step abends, then the system shall delete the text and HTML statement files, so no statements from that run are kept. (rules ASGD-BR-012)
2. GIVEN statements written before failure: 40 WHEN the statement step abends THEN Both statement files are deleted at abnormal end (ASGD-C06-AC-01; ASGD-BR-012)
