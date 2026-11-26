# Design: List card cross-reference records (UP-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

A read-only batch listing of every card cross-reference record, showing which card belongs to which account and customer. Operations staff use it for review. It must never change the cross-reference. The legacy job prints each record twice, which the team must either keep or consciously drop.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

#### CVACT03Y

File record of CBACT03C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |


## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-012 | Read the card cross-reference master | design note | THE Card Cross-Reference Master Read job SHALL run the program CBACT03C against the card cross-reference master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS) in shared read-only access, leaving the master unchanged and printing every cross-reference record to the job's output listing. | medium | app/jcl/READXREF.jcl:22-28, app/cbl/CBACT03C.cbl:70-86, app/cbl/CBACT03C.cbl:92-96 |
| UP-BR-013 | List all card cross-reference records | formatting | THE Card Cross-Reference Listing (CBACT03C) SHALL read the card cross-reference file from start to end and print every record, stopping when the end of the file is reached. | high | app/cbl/CBACT03C.cbl:74-81, app/cbl/CBACT03C.cbl:92-96, app/cbl/CBACT03C.cbl:98-108, app/cbl/CBCUS01C.cbl:78 |
| UP-BR-014 | Each record is printed twice in the cross-reference and customer dumps | historical artifact | THE Card Cross-Reference Listing SHALL print each cross-reference record twice in a row, once when it is read and again in the main loop. | high | app/cbl/CBACT03C.cbl:74-81, app/cbl/CBACT03C.cbl:92-96, app/cbl/CBACT03C.cbl:98-108, app/cbl/CBCUS01C.cbl:78 |

### Worked examples

- UP-BR-012: cross-reference master = 3 card cross-reference records → The job listing shows 'START OF EXECUTION OF PROGRAM CBACT03C', the 3 records, and 'END OF EXECUTION OF PROGRAM CBACT03C'; the master still holds the same 3 records.
- UP-BR-013: cross-reference records = 3 → All 3 records are printed, then 'END OF EXECUTION OF PROGRAM CBACT03C'.
- UP-BR-014: cross-reference records = 2 → The output has 4 record lines, each record appearing twice in succession.

## Decision tables

None.

## Design notes

- UP-BR-012: A report job that reads the full card-to-account/customer link table through a read-only connection, from start to end, and writes every link to the job's report output. It changes nothing.

## Open questions

- SME-010: The cross-reference and customer listings print every record twice. Does anything rely on that, or should each record be printed once? (Batch operations) On UP-BR-014.
- DEF-097: Is this intended? Each record is displayed twice, once in the read paragraph and once in the main loop; CBACT02C has the same read-paragraph display commented out, suggesting the duplicate is debug output left in by mistake. (Subject-matter expert) On UP-BR-013, UP-BR-014.
- DEF-141: Is this intended? CBACT03C prints each cross-reference record twice: once in the read routine on a successful read and again in the main loop, so the listing shows every record duplicated. (Subject-matter expert) On UP-BR-012.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).