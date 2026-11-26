# Produce daily transaction report (DTPR-C06)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as online and scheduled job · risk high

## Introduction

Produces the Daily Transaction Report for a date range. It lists the transactions in range by card, with the transaction type and category descriptions, totals per account, and page totals every 20 lines. It serves operations analysts reviewing the day's activity. It must never print a transaction without its reference data (it stops instead), and it must put the right date range in the heading.

**User story:** As an operations analyst, I want a paginated daily transaction report with reference descriptions and account totals, so that I can review the day's transactions by card and account.

## Requirements

### Requirement 1: DTPR-REQ-F-052 (formatting)

#### Acceptance criteria

1. When the first transaction of the run is about to be printed, the system shall mark the report as started, put the reporting start and end dates into the heading, and print 'DALYREPT' 'Daily Transaction Report' 'Date Range: <start> to <end>', a blank line, the column headings and a dashed line. (rules DTPR-BR-057)
2. GIVEN a report run with start date 2022-06-01 and end date 2022-06-30 that has not yet printed anything WHEN the first transaction of the run is about to be printed THEN the report is marked as started, and before the transaction it prints 'DALYREPT' 'Daily Transaction Report' 'Date Range: 2022-06-01 to 2022-06-30', then a blank line, the column headings and a dashed line; later transactions do not print this heading again on first-write grounds (DTPR-C06-AC-08; DTPR-BR-057)

### Requirement 2: DTPR-REQ-F-053 (formatting)

#### Acceptance criteria

1. While transactions remain to be processed, when the transaction's card number differs from the current card number, the system shall write the account total and separator lines if the report has already started, reset the account total to zero, make the new card current and look up its cross-reference. (rules DTPR-BR-058)
2. GIVEN WS-CURR-CARD-NUM: 4111111111111111; TRAN-CARD-NUM: 4222222222222222; WS-FIRST-TIME: N; WS-ACCOUNT-TOTAL: 350.00 WHEN transactions remain to be processed (`END-OF-FILE` = 'N'), WHEN the transaction's card number differs from the current card number THEN An account total line of 350.00 and a separator line are written, the account total resets to 0, and card 4222222222222222 is looked up in the cross-reference. (DTPR-C06-AC-01; DTPR-BR-058)
3. GIVEN TRAN-CARD-NUM: 4111111111111111; WS-FIRST-TIME: Y WHEN transactions remain to be processed (`END-OF-FILE` = 'N'), WHEN the transaction's card number differs from the current card number THEN No account total line is written (first card of the report); the card becomes current and is looked up. (DTPR-C06-AC-02; DTPR-BR-058)
4. GIVEN WS-CURR-CARD-NUM: 4111111111111111; TRAN-CARD-NUM: 4111111111111111 WHEN transactions remain to be processed (`END-OF-FILE` = 'N'), WHEN the transaction's card number differs from the current card number THEN No account break: no total line, the total keeps accumulating. (DTPR-C06-AC-03; DTPR-BR-058)

### Requirement 3: DTPR-REQ-F-054 (design note)

#### Acceptance criteria

1. When an in-range transaction is ready for reporting, the system shall retrieve the account for the card, the transaction type description and the category description by type and category code. (rules DTPR-BR-059)
2. GIVEN TRAN-CARD-NUM: 4111111111111111 (in cross-reference); TRAN-TYPE-CD: 01; TRAN-CAT-CD: 0001 WHEN an in-range transaction is ready for reporting THEN The report line carries the account id, the type description and the category description for 01/0001. (DTPR-C06-AC-04; DTPR-BR-059)
3. GIVEN TRAN-CARD-NUM: 9999999999999999 (not in cross-reference) WHEN an in-range transaction is ready for reporting THEN 'INVALID CARD NUMBER : ' is displayed with the card number, IO status 23 is shown and the run abends. (DTPR-C06-AC-05; DTPR-BR-059)
4. GIVEN TRAN-TYPE-CD: 99 (not on file) WHEN an in-range transaction is ready for reporting THEN 'INVALID TRANSACTION TYPE : ' is displayed with the type, IO status 23 is shown and the run abends. (DTPR-C06-AC-06; DTPR-BR-059)

### Requirement 4: DTPR-REQ-F-055 (design note)

#### Acceptance criteria

1. If the card cross-reference, transaction type or transaction category record is not found for a reported transaction, then the system shall abend the run. (rules DTPR-BR-059)
2. GIVEN TRAN-CARD-NUM: 4111111111111111 (in cross-reference); TRAN-TYPE-CD: 01; TRAN-CAT-CD: 0001 WHEN an in-range transaction is ready for reporting THEN The report line carries the account id, the type description and the category description for 01/0001. (DTPR-C06-AC-04; DTPR-BR-059)
3. GIVEN TRAN-CARD-NUM: 9999999999999999 (not in cross-reference) WHEN an in-range transaction is ready for reporting THEN 'INVALID CARD NUMBER : ' is displayed with the card number, IO status 23 is shown and the run abends. (DTPR-C06-AC-05; DTPR-BR-059)
4. GIVEN TRAN-TYPE-CD: 99 (not on file) WHEN an in-range transaction is ready for reporting THEN 'INVALID TRANSACTION TYPE : ' is displayed with the type, IO status 23 is shown and the run abends. (DTPR-C06-AC-06; DTPR-BR-059)

### Requirement 5: DTPR-REQ-F-056 (formatting)

#### Acceptance criteria

1. When a detail line is about to be printed and the count of lines printed so far, headings, totals and separators included, is an exact multiple of 20, the system shall first print the 'Page Total' line and a dashed line, then the report title line, a blank line, the column headings and a dashed line. (rules DTPR-BR-060)
2. GIVEN lines printed so far: 19; next transaction: for a new card, so 2 account-total lines are printed first WHEN a detail line is about to be printed and the count of lines printed so far (headings, totals and separators included) is an exact multiple of 20 THEN The count passes from 19 to 21 without being checked at 20, so no page break occurs until the count reaches 40. (DTPR-C06-AC-07; DTPR-BR-060)

## Screens and components

No screens: it runs as online and scheduled job.

## Data models

#### CVACT03Y

File record of CBTRN03C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVTRA03Y

File record of CBTRN03C. Source: `app/cpy/CVTRA03Y.cpy`.

Record `TRAN-TYPE-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-TYPE |  | X(02) | text, 2 characters |  |  |  |
| TRAN-TYPE-DESC |  | X(50) | text, 50 characters |  |  |  |
| FILLER |  | X(08) | text, 8 characters |  |  |  |

#### CVTRA04Y

File record of CBTRN03C. Source: `app/cpy/CVTRA04Y.cpy`.

Record `TRAN-CAT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-CAT-KEY |  |  | group |  |  |  |
| TRAN-TYPE-CD | TRAN-CAT-KEY | X(02) | text, 2 characters |  |  |  |
| TRAN-CAT-CD | TRAN-CAT-KEY | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-CAT-TYPE-DESC |  | X(50) | text, 50 characters |  |  |  |
| FILLER |  | X(04) | text, 4 characters |  |  |  |

#### CVTRA05Y

File record of CBTRN03C. Source: `app/cpy/CVTRA05Y.cpy`.

Record `TRAN-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-ID |  | X(16) | text, 16 characters |  |  |  |
| TRAN-TYPE-CD |  | X(02) | text, 2 characters |  |  |  |
| TRAN-CAT-CD |  | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-SOURCE |  | X(10) | text, 10 characters |  |  |  |
| TRAN-DESC |  | X(100) | text, 100 characters |  |  |  |
| TRAN-AMT |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-NAME |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-CITY |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-ZIP |  | X(10) | text, 10 characters |  |  |  |
| TRAN-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| TRAN-ORIG-TS |  | X(26) | text, 26 characters |  |  |  |
| TRAN-PROC-TS |  | X(26) | text, 26 characters |  |  |  |
| FILLER |  | X(20) | text, 20 characters |  |  |  |

- CVTRA07Y (working storage of CBTRN03C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-057 | Print report heading on first write | formatting | WHEN the first transaction of the run is about to be printed, THE Daily Transaction Report SHALL mark the report as started, put the reporting start and end dates into the heading, and print the headings: 'DALYREPT' 'Daily Transaction Report' 'Date Range: <start> to <end>', a blank line, the column headings and a dashed line. | medium | app/cbl/CBTRN03C.cbl:274-280, app/cbl/CBTRN03C.cbl:324-341, app/cpy/CVTRA07Y.cpy:4-48 |
| DTPR-BR-058 | Print account total on card change | formatting | WHILE transactions remain to be processed (`END-OF-FILE` = 'N'), WHEN the transaction's card number differs from the current card number, THE Account Break Reporting SHALL write the account total and separator lines when the report has already started ('N'), reset the account total to zero, make the new card current, and look up its cross-reference | medium | app/cbl/CBTRN03C.cbl:179,181-188,306-314, app/cbl/CBTRN03C.cbl:181-188 |
| DTPR-BR-059 | Enrich transaction with reference data | design note | WHEN an in-range transaction is ready for reporting, THE Transaction Reference Enrichment SHALL retrieve the account for the card, the transaction type description and the category description by type and category code, and abend the run when any reference record is not found (physical stores: `TRANCATG-FILE`, `TRANTYPE-FILE`, `XREF-FILE`) | medium | app/cbl/CBTRN03C.cbl:189-195,484-486,490-491,494-496,500-501,504-506,510-511, app/cbl/CBTRN03C.cbl:484-512 |
| DTPR-BR-060 | Report pagination every 20 lines | formatting | WHEN a detail line is about to be printed and the count of lines printed so far (headings, totals and separators included) is an exact multiple of 20, THE Daily Transaction Report SHALL first print the 'Page Total' line and a dashed line, then the report title line, a blank line, the column headings and a dashed line. | medium | app/cbl/CBTRN03C.cbl:129-132, app/cbl/CBTRN03C.cbl:181-184, app/cbl/CBTRN03C.cbl:282-289, app/cbl/CBTRN03C.cbl:293-341 |

### Worked examples

- DTPR-BR-058: WS-CURR-CARD-NUM = 4111111111111111; TRAN-CARD-NUM = 4222222222222222; WS-FIRST-TIME = N; WS-ACCOUNT-TOTAL = 350.00 → An account total line of 350.00 and a separator line are written, the account total resets to 0, and card 4222222222222222 is looked up in the cross-reference.
- DTPR-BR-058: TRAN-CARD-NUM = 4111111111111111; WS-FIRST-TIME = Y → No account total line is written (first card of the report); the card becomes current and is looked up.
- DTPR-BR-058: WS-CURR-CARD-NUM = 4111111111111111; TRAN-CARD-NUM = 4111111111111111 → No account break: no total line, the total keeps accumulating.
- DTPR-BR-059: TRAN-CARD-NUM = 4111111111111111 (in cross-reference); TRAN-TYPE-CD = 01; TRAN-CAT-CD = 0001 → The report line carries the account id, the type description and the category description for 01/0001.
- DTPR-BR-059: TRAN-CARD-NUM = 9999999999999999 (not in cross-reference) → 'INVALID CARD NUMBER : ' is displayed with the card number, IO status 23 is shown and the run abends.
- DTPR-BR-059: TRAN-TYPE-CD = 99 (not on file) → 'INVALID TRANSACTION TYPE : ' is displayed with the type, IO status 23 is shown and the run abends.
- DTPR-BR-060: lines printed so far = 19; next transaction = for a new card, so 2 account-total lines are printed first → The count passes from 19 to 21 without being checked at 20, so no page break occurs until the count reaches 40.

## Decision tables

None.

## Design notes

- DTPR-BR-059: For each in-range transaction, look up the card's cross-reference (giving the account) by card number, the type description by type code, and the category description by type and category code. A missing reference record must fail the report run rather than print a blank. The type and category tables are small and can be cached for the run.

## Open questions

- SME-043: The transaction report extract selects transactions using fixed dates (2022-01-01 to 2022-07-06), but the report itself takes its start and end dates from the run's date parameter. Should the extract period come from the same run parameter, and what should happen if the two periods differ? (Reporting owner) On DTPR-BR-058, DTPR-BR-059, DTPR-BR-057.
- SME-044: When the transaction report meets a transaction outside the reporting period, the program stops reading entirely, so later in-range transactions and the grand total are lost (the input is sorted by card, not date). Should out-of-range transactions just be skipped instead? Is it acceptable to rely only on the earlier sort step's date filter? (Reporting owner / batch operations lead) On DTPR-BR-058, DTPR-BR-059, DTPR-BR-057.
- SME-045: At the end of the transaction report, the last transaction's amount is added to the page, account and grand totals a second time, which overstates them. Is this double-counting intended, or should it be corrected? How critical are these totals? (Finance reporting owner) On DTPR-BR-058, DTPR-BR-059, DTPR-BR-057.
- SME-046: Should the transaction report print an 'Account Total' line for the last card at the end of the report? (Reporting owner) On DTPR-BR-058, DTPR-BR-059, DTPR-BR-057.
- SME-047: What page size does the transaction report need? Is 20 lines per page a business requirement, and should a page break happen whenever that size is reached, rather than only on exact multiples? (Reporting owner) On DTPR-BR-058, DTPR-BR-059, DTPR-BR-057, DTPR-BR-060.
- DEF-182: Is this intended? Account-total and page-total blocks add 2 lines at once, so the counter can skip over a multiple of 20 and a page runs on to the next multiple. Page length is therefore irregular, at up to about 40 lines. (Subject-matter expert) On DTPR-BR-060.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).
