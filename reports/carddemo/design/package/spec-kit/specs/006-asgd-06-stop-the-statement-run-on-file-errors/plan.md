# Implementation plan: Stop the statement run on file errors (ASGD-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as scheduled job.

## Data model

- COSTM01 (working storage of CBSTM03A): see data-contracts.md.
- CUSTREC (working storage of CBSTM03A): see data-contracts.md.
- CVACT01Y (working storage of CBSTM03A): see data-contracts.md.
- CVACT03Y (working storage of CBSTM03A): see data-contracts.md.

## Design notes

None.

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

