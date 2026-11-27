# Design: List customer records (UP-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

A batch listing of every customer on the customer master, from first to last. Operations staff use it to review customer records. It must list every customer and stop cleanly at the end of the file. The legacy job prints each customer twice, which the team must either keep or consciously drop.

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

#### CVCUS01Y

File record of CBCUS01C. Source: `app/cpy/CVCUS01Y.cpy`.

Record `CUSTOMER-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-FIRST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-MIDDLE-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-LAST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-ADDR-LINE-1 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-2 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-3 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-STATE-CD |  | X(02) | text, 2 characters |  |  |  |
| CUST-ADDR-COUNTRY-CD |  | X(03) | text, 3 characters |  |  |  |
| CUST-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| CUST-PHONE-NUM-1 |  | X(15) | text, 15 characters |  |  |  |
| CUST-PHONE-NUM-2 |  | X(15) | text, 15 characters |  |  |  |
| CUST-SSN |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-GOVT-ISSUED-ID |  | X(20) | text, 20 characters |  |  |  |
| CUST-DOB-YYYY-MM-DD |  | X(10) | text, 10 characters |  |  |  |
| CUST-EFT-ACCOUNT-ID |  | X(10) | text, 10 characters |  |  |  |
| CUST-PRI-CARD-HOLDER-IND |  | X(01) | text, 1 character |  |  |  |
| CUST-FICO-CREDIT-SCORE |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| FILLER |  | X(168) | text, 168 characters |  |  |  |


## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-015 | List all customer records until end | formatting | THE Customer Listing SHALL read the customer master file from start to end and print each customer record to the job output, stopping when the end of the file is reached (file status '10'). | medium | app/cbl/CBCUS01C.cbl:70-87, app/cbl/CBCUS01C.cbl:92-116 |
| UP-BR-016 | List all customer records until end | formatting | WHEN a customer record is read successfully, THE Customer Listing SHALL print that record twice, once in the read routine (1000-CUSTFILE-GET-NEXT) and once in the main loop. | medium | app/cbl/CBCUS01C.cbl:70-87, app/cbl/CBCUS01C.cbl:92-116 |
| UP-BR-005 | Each record is printed twice in the cross-reference and customer dumps | historical artifact | THE Customer Listing (CBCUS01C) SHALL likewise print each customer record twice, while the Card Listing (CBACT02C) prints each card record once because its second print is commented out. | high | app/cbl/CBACT03C.cbl:74-81, app/cbl/CBACT03C.cbl:92-96, app/cbl/CBACT03C.cbl:98-108, app/cbl/CBCUS01C.cbl:78 |

### Worked examples

- UP-BR-015: Customer file = 3 customer records → All 3 customer records are printed to the job output and the run ends with 'END OF EXECUTION OF PROGRAM CBCUS01C'.
- UP-BR-015: Customer file = empty → No customer record is printed; the first read returns end of file and the program ends.
- UP-BR-016: Customer file = 1 customer record for customer 000000001 → The record for customer 000000001 appears two times in the job output.
- UP-BR-005: customer records = 5 → The customer listing has 10 record lines.
- UP-BR-005: card records = 5 → The card listing has 5 record lines.

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-010: The cross-reference and customer listings print every record twice. Does anything rely on that, or should each record be printed once? (Batch operations) On UP-BR-005.
- DEF-097: Is this intended? Each record is displayed twice, once in the read paragraph and once in the main loop; CBACT02C has the same read-paragraph display commented out, suggesting the duplicate is debug output left in by mistake. (Subject-matter expert) On UP-BR-005.
- DEF-145: Is this intended? Each successfully read customer record is displayed twice: once inside 1000-CUSTFILE-GET-NEXT on status '00' and again in the main loop, doubling the listing. (Subject-matter expert) On UP-BR-016.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).