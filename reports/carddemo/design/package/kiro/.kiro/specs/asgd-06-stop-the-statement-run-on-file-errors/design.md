# Design: Stop the statement run on file errors (ASGD-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

If any statement data cannot be opened, read or closed, the run stops with a clear message naming the file and the return code, and no statements from that run are issued. Its main audience is the statement operations team. It must never issue a statement built from missing customer or account data, and it must never carry on after a file error.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- COSTM01 (working storage of CBSTM03A): see data-contracts.md.
- CUSTREC (working storage of CBSTM03A): see data-contracts.md.
- CVACT01Y (working storage of CBSTM03A): see data-contracts.md.
- CVACT03Y (working storage of CBSTM03A): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-027 | Customer and account master records must exist for every card or the run aborts | error handling | WHEN the customer record for a cross-reference card cannot be read (any result other than '00'), THE statement batch SHALL display 'ERROR READING CUSTFILE' with the return code and abend, producing no further statements. | medium | app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/jcl/CREASTMT.JCL:87-96 |
| ASGD-BR-028 | Produce one statement per card | error handling | WHEN reading the cross-reference, customer or account file fails (anything other than success, or end of file for the cross-reference), THE statement job SHALL display 'ERROR READING XREFFILE', 'ERROR READING CUSTFILE' or 'ERROR READING ACCTFILE' with the return code, then 'ABENDING PROGRAM', and abend. | high | app/cbl/CBSTM03A.CBL:316-329, app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/cbl/CBSTM03B.CBL:37-52 |
| ASGD-BR-029 | Customer and account master records must exist for every card or the run aborts | error handling | WHEN the account record for a cross-reference card cannot be read (any result other than '00'), THE statement batch SHALL display 'ERROR READING ACCTFILE' with the return code and abend. | medium | app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/jcl/CREASTMT.JCL:87-96 |
| ASGD-BR-030 | Customer and account master records must exist for every card or the run aborts | error handling | WHEN reading the next cross-reference record returns anything other than '00' or end of file '10', THE statement batch SHALL display 'ERROR READING XREFFILE' with the return code and abend. | medium | app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/jcl/CREASTMT.JCL:87-96 |
| ASGD-BR-031 | File open/read/close outcome acceptance policy | error handling | WHEN opening, closing or making the first read of the transaction file, or opening or closing the cross-reference, customer or account file, returns anything other than '00' or '04', THE statement batch SHALL display 'ERROR OPENING <file>', 'ERROR READING TRNXFILE' or 'ERROR CLOSING <file>' with the return code and abend. | medium | app/cbl/CBSTM03A.CBL:730-754, app/cbl/CBSTM03A.CBL:765-815, app/cbl/CBSTM03A.CBL:837-847, app/cbl/CBSTM03A.CBL:856-919 |
| ASGD-BR-032 | File open/read/close outcome acceptance policy | error handling | WHEN a later read of the transaction file during loading returns anything other than '00' or end of file '10', THE statement batch SHALL display 'ERROR READING TRNXFILE' with the return code and abend. | medium | app/cbl/CBSTM03A.CBL:730-754, app/cbl/CBSTM03A.CBL:765-815, app/cbl/CBSTM03A.CBL:837-847, app/cbl/CBSTM03A.CBL:856-919 |
| ASGD-BR-012 | Customer and account master records must exist for every card or the run aborts | error handling | WHEN the statement step abends, THE job SHALL delete the text and HTML statement files, so no statements from that run are kept. | medium | app/cbl/CBSTM03A.CBL:345-414, app/cbl/CBSTM03A.CBL:921-923, app/jcl/CREASTMT.JCL:87-96 |

### Worked examples

- ASGD-BR-012: statements written before failure = 40 → Both statement files are deleted at abnormal end

## Decision tables

#### Statement run file outcome handling

| File | Operation | Result code | Message and run outcome | Rule |
|---|---|---|---|---|
| CUSTFILE | Keyed read | Other than '00' | Display 'ERROR READING CUSTFILE' with return code; abend | ASGD-BR-027 |
| ACCTFILE | Keyed read | Other than '00' | Display 'ERROR READING ACCTFILE' with return code; abend | ASGD-BR-029 |
| XREFFILE | Next read | Other than '00' or '10' | Display 'ERROR READING XREFFILE' with return code; abend | ASGD-BR-030 |
| XREFFILE, CUSTFILE or ACCTFILE | Read | Failure | Display read error with return code, then 'ABENDING PROGRAM'; abend | ASGD-BR-028 |
| Any statement file | Open or close | Other than '00' or '04' | Display 'ERROR OPENING <file>' or 'ERROR CLOSING <file>' with return code; abend | ASGD-BR-031 |
| TRNXFILE | First read | Other than '00' or '04' | Display 'ERROR READING TRNXFILE' with return code; abend | ASGD-BR-031 |
| TRNXFILE | Later read during loading | Other than '00' or '10' | Display 'ERROR READING TRNXFILE' with return code; abend | ASGD-BR-032 |
| Any statement file | Open, close or first transaction read | '04' | **Gap:** '04' is accepted and the run continues; no rule says what '04' means or whether the statement is still complete. | |
| TRNXFILE | First read | '10' (empty transaction file) | **Gap:** Empty transaction file abends under R7; confirm whether that is intended or statements without transactions should be produced. | |


## Design notes

None.

## Open questions

- SME-030: When producing statements, if the customer or account for a card cannot be found, should that statement be skipped, the run stopped, or an exception recorded? (Statement operations business owner) On ASGD-BR-028.
- SME-031: On statements, should address line 3, state, country and ZIP each be cut off at their first space, even when the value has more than one word? (Statement operations business owner) On ASGD-BR-028.
- SME-032: Statement production assumes card cross-references are processed in ascending card number order, matching the sorted transactions. Must the new system guarantee that order? (Data architecture team) On ASGD-BR-028.
- DEF-162: Is this intended? An empty transaction extract makes the whole run abend instead of producing statements with no transactions, and a '04' result is accepted on the first transaction read but causes an abend on later reads. (Subject-matter expert) On ASGD-BR-032.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).