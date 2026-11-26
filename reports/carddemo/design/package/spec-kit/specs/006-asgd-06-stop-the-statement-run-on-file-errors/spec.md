# Feature specification: Stop the statement run on file errors

**Feature:** ASGD-C06 · Account Statement Generation and Delivery · Customer Account Self-Service

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ASGD-C06)

As a statement operations team, I want the statement run to stop with a clear message when a file cannot be opened, read or closed, so that no incomplete statements are issued.

If any statement data cannot be opened, read or closed, the run stops with a clear message naming the file and the return code, and no statements from that run are issued. Its main audience is the statement operations team. It must never issue a statement built from missing customer or account data, and it must never carry on after a file error.

**Acceptance scenarios:**

1. **Given** statements written before failure: 40, **when** the statement step abends, **then** Both statement files are deleted at abnormal end (ASGD-C06-AC-01)
2. **Given** A cross-reference card whose customer ID has no customer record, so the read returns '23', **when** The statement run processes that card, **then** The run displays 'ERROR READING CUSTFILE' with return code 23, then 'ABENDING PROGRAM', and abends. No statement is produced for that card or any card after it. (ASGD-C06-AC-02)
3. **Given** A cross-reference card whose account ID has no account record, so the read returns '23', **when** The statement run looks up the account, **then** The run displays 'ERROR READING ACCTFILE' with return code 23, then 'ABENDING PROGRAM', and abends (ASGD-C06-AC-03)
4. **Given** Reading the next cross-reference record returns a status other than '00' or '10', **when** The statement run reads the cross-reference, **then** The run displays 'ERROR READING XREFFILE' with that return code, then 'ABENDING PROGRAM', and abends. A status of '10' (end of file) ends the run normally, with no error. (ASGD-C06-AC-04)
5. **Given** A read of the cross-reference, customer or account file fails, **when** The failure is detected, **then** The matching message ('ERROR READING XREFFILE', 'ERROR READING CUSTFILE' or 'ERROR READING ACCTFILE') is displayed with the return code, followed by 'ABENDING PROGRAM', and the run abends (ASGD-C06-AC-05)
6. **Given** Opening the account file returns a status other than '00' or '04'. Separately, the first read of the transaction file returns such a status, or closing the customer file does., **when** The statement run performs that operation, **then** The run displays 'ERROR OPENING <file>', 'ERROR READING TRNXFILE' or 'ERROR CLOSING <file>' respectively, with the return code, and abends. A status of '00' or '04' lets the run continue. (ASGD-C06-AC-06)
7. **Given** While the transactions are loading, a read after the first one returns a status other than '00' or '10', **when** The statement run reads that transaction, **then** The run displays 'ERROR READING TRNXFILE' with the return code and abends. A status of '10' ends loading normally. (ASGD-C06-AC-07)

## Requirements

### Functional requirements

- **ASGD-REQ-F-026** (error handling): If the customer record for a cross-reference card cannot be read (any result other than '00'), then the system shall display 'ERROR READING CUSTFILE' with the return code and abend, producing no further statements. Rules: ASGD-BR-027, ASGD-BR-028.
- **ASGD-REQ-F-027** (error handling): If the account record for a cross-reference card cannot be read (any result other than '00'), then the system shall display 'ERROR READING ACCTFILE' with the return code and abend. Rules: ASGD-BR-029, ASGD-BR-028.
- **ASGD-REQ-F-028** (error handling): If reading the next cross-reference record returns anything other than '00' or end of file '10', then the system shall display 'ERROR READING XREFFILE' with the return code and abend. Rules: ASGD-BR-030, ASGD-BR-028.
- **ASGD-REQ-F-029** (error handling): If reading the cross-reference, customer or account file fails, then the system shall display the read error message with the return code, then 'ABENDING PROGRAM', and abend. Rules: ASGD-BR-028.
- **ASGD-REQ-F-030** (error handling): If opening, closing or making the first read of the transaction file, or opening or closing the cross-reference, customer or account file, returns anything other than '00' or '04', then the system shall display 'ERROR OPENING <file>', 'ERROR READING TRNXFILE' or 'ERROR CLOSING <file>' with the return code and abend. Rules: ASGD-BR-031.
- **ASGD-REQ-F-031** (error handling): If a later read of the transaction file during loading returns anything other than '00' or end of file '10', then the system shall display 'ERROR READING TRNXFILE' with the return code and abend. Rules: ASGD-BR-032.
- **ASGD-REQ-F-032** (error handling): If the statement step abends, then the system shall delete the text and HTML statement files, so no statements from that run are kept. Rules: ASGD-BR-012.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-027 | Customer and account master records must exist for every card or the run aborts | error handling | WHEN the customer record for a cross-reference card cannot be read (any result other than '00'), THE statement batch SHALL display 'ERROR READING CUSTFILE' with the return code and abend, producing no further statements. | medium | app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/jcl/CREASTMT.JCL:87-96 |
| ASGD-BR-028 | Produce one statement per card | error handling | WHEN reading the cross-reference, customer or account file fails (anything other than success, or end of file for the cross-reference), THE statement job SHALL display 'ERROR READING XREFFILE', 'ERROR READING CUSTFILE' or 'ERROR READING ACCTFILE' with the return code, then 'ABENDING PROGRAM', and abend. | high | app/cbl/CBSTM03A.CBL:316-329, app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/cbl/CBSTM03B.CBL:37-52 |
| ASGD-BR-029 | Customer and account master records must exist for every card or the run aborts | error handling | WHEN the account record for a cross-reference card cannot be read (any result other than '00'), THE statement batch SHALL display 'ERROR READING ACCTFILE' with the return code and abend. | medium | app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/jcl/CREASTMT.JCL:87-96 |
| ASGD-BR-030 | Customer and account master records must exist for every card or the run aborts | error handling | WHEN reading the next cross-reference record returns anything other than '00' or end of file '10', THE statement batch SHALL display 'ERROR READING XREFFILE' with the return code and abend. | medium | app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/jcl/CREASTMT.JCL:87-96 |
| ASGD-BR-031 | File open/read/close outcome acceptance policy | error handling | WHEN opening, closing or making the first read of the transaction file, or opening or closing the cross-reference, customer or account file, returns anything other than '00' or '04', THE statement batch SHALL display 'ERROR OPENING <file>', 'ERROR READING TRNXFILE' or 'ERROR CLOSING <file>' with the return code and abend. | medium | app/cbl/CBSTM03A.CBL:730-754, app/cbl/CBSTM03A.CBL:765-815, app/cbl/CBSTM03A.CBL:837-847, app/cbl/CBSTM03A.CBL:856-919 |
| ASGD-BR-032 | File open/read/close outcome acceptance policy | error handling | WHEN a later read of the transaction file during loading returns anything other than '00' or end of file '10', THE statement batch SHALL display 'ERROR READING TRNXFILE' with the return code and abend. | medium | app/cbl/CBSTM03A.CBL:730-754, app/cbl/CBSTM03A.CBL:765-815, app/cbl/CBSTM03A.CBL:837-847, app/cbl/CBSTM03A.CBL:856-919 |
| ASGD-BR-012 | Customer and account master records must exist for every card or the run aborts | error handling | WHEN the statement step abends, THE job SHALL delete the text and HTML statement files, so no statements from that run are kept. | medium | app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/jcl/CREASTMT.JCL:87-96 |

### Key entities

- COSTM01 (working storage)
- CUSTREC (working storage)
- CVACT01Y (working storage)
- CVACT03Y (working storage)

### Needs clarification

- SME-030: When producing statements, if the customer or account for a card cannot be found, should that statement be skipped, the run stopped, or an exception recorded? (Statement operations business owner) On ASGD-BR-028.
- SME-031: On statements, should address line 3, state, country and ZIP each be cut off at their first space, even when the value has more than one word? (Statement operations business owner) On ASGD-BR-028.
- SME-032: Statement production assumes card cross-references are processed in ascending card number order, matching the sorted transactions. Must the new system guarantee that order? (Data architecture team) On ASGD-BR-028.
- DEF-162: Is this intended? An empty transaction extract makes the whole run abend instead of producing statements with no transactions, and a '04' result is accepted on the first transaction read but causes an abend on later reads. (Subject-matter expert) On ASGD-BR-032.

### Decision table gaps

- Statement run file outcome handling: '04' is accepted and the run continues; no rule says what '04' means or whether the statement is still complete.
- Statement run file outcome handling: Empty transaction file abends under R7; confirm whether that is intended or statements without transactions should be produced.
