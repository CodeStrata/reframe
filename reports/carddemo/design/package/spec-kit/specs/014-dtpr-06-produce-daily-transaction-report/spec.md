# Feature specification: Produce daily transaction report

**Feature:** DTPR-C06 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C06)

As an operations analyst, I want a paginated daily transaction report with reference descriptions and account totals, so that I can review the day's transactions by card and account.

Produces the Daily Transaction Report for a date range. It lists the transactions in range by card, with the transaction type and category descriptions, totals per account, and page totals every 20 lines. It serves operations analysts reviewing the day's activity. It must never print a transaction without its reference data (it stops instead), and it must put the right date range in the heading.

**Acceptance scenarios:**

1. **Given** WS-CURR-CARD-NUM: 4111111111111111; TRAN-CARD-NUM: 4222222222222222; WS-FIRST-TIME: N; WS-ACCOUNT-TOTAL: 350.00, **when** transactions remain to be processed (`END-OF-FILE` = 'N'), WHEN the transaction's card number differs from the current card number, **then** An account total line of 350.00 and a separator line are written, the account total resets to 0, and card 4222222222222222 is looked up in the cross-reference. (DTPR-C06-AC-01)
2. **Given** TRAN-CARD-NUM: 4111111111111111; WS-FIRST-TIME: Y, **when** transactions remain to be processed (`END-OF-FILE` = 'N'), WHEN the transaction's card number differs from the current card number, **then** No account total line is written (first card of the report); the card becomes current and is looked up. (DTPR-C06-AC-02)
3. **Given** WS-CURR-CARD-NUM: 4111111111111111; TRAN-CARD-NUM: 4111111111111111, **when** transactions remain to be processed (`END-OF-FILE` = 'N'), WHEN the transaction's card number differs from the current card number, **then** No account break: no total line, the total keeps accumulating. (DTPR-C06-AC-03)
4. **Given** TRAN-CARD-NUM: 4111111111111111 (in cross-reference); TRAN-TYPE-CD: 01; TRAN-CAT-CD: 0001, **when** an in-range transaction is ready for reporting, **then** The report line carries the account id, the type description and the category description for 01/0001. (DTPR-C06-AC-04)
5. **Given** TRAN-CARD-NUM: 9999999999999999 (not in cross-reference), **when** an in-range transaction is ready for reporting, **then** 'INVALID CARD NUMBER : ' is displayed with the card number, IO status 23 is shown and the run abends. (DTPR-C06-AC-05)
6. **Given** TRAN-TYPE-CD: 99 (not on file), **when** an in-range transaction is ready for reporting, **then** 'INVALID TRANSACTION TYPE : ' is displayed with the type, IO status 23 is shown and the run abends. (DTPR-C06-AC-06)
7. **Given** lines printed so far: 19; next transaction: for a new card, so 2 account-total lines are printed first, **when** a detail line is about to be printed and the count of lines printed so far (headings, totals and separators included) is an exact multiple of 20, **then** The count passes from 19 to 21 without being checked at 20, so no page break occurs until the count reaches 40. (DTPR-C06-AC-07)
8. **Given** a report run with start date 2022-06-01 and end date 2022-06-30 that has not yet printed anything, **when** the first transaction of the run is about to be printed, **then** the report is marked as started, and before the transaction it prints 'DALYREPT' 'Daily Transaction Report' 'Date Range: 2022-06-01 to 2022-06-30', then a blank line, the column headings and a dashed line; later transactions do not print this heading again on first-write grounds (DTPR-C06-AC-08)

## Requirements

### Functional requirements

- **DTPR-REQ-F-052** (formatting): When the first transaction of the run is about to be printed, the system shall mark the report as started, put the reporting start and end dates into the heading, and print 'DALYREPT' 'Daily Transaction Report' 'Date Range: <start> to <end>', a blank line, the column headings and a dashed line. Rules: DTPR-BR-057.
- **DTPR-REQ-F-053** (formatting): While transactions remain to be processed, when the transaction's card number differs from the current card number, the system shall write the account total and separator lines if the report has already started, reset the account total to zero, make the new card current and look up its cross-reference. Rules: DTPR-BR-058.
- **DTPR-REQ-F-054** (design note): When an in-range transaction is ready for reporting, the system shall retrieve the account for the card, the transaction type description and the category description by type and category code. Rules: DTPR-BR-059.
- **DTPR-REQ-F-055** (design note): If the card cross-reference, transaction type or transaction category record is not found for a reported transaction, then the system shall abend the run. Rules: DTPR-BR-059.
- **DTPR-REQ-F-056** (formatting): When a detail line is about to be printed and the count of lines printed so far, headings, totals and separators included, is an exact multiple of 20, the system shall first print the 'Page Total' line and a dashed line, then the report title line, a blank line, the column headings and a dashed line. Rules: DTPR-BR-060.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-057 | Print report heading on first write | formatting | WHEN the first transaction of the run is about to be printed, THE Daily Transaction Report SHALL mark the report as started, put the reporting start and end dates into the heading, and print the headings: 'DALYREPT' 'Daily Transaction Report' 'Date Range: <start> to <end>', a blank line, the column headings and a dashed line. | medium | app/cbl/CBTRN03C.cbl:274-280, app/cbl/CBTRN03C.cbl:324-341, app/cpy/CVTRA07Y.cpy:4-48 |
| DTPR-BR-058 | Print account total on card change | formatting | WHILE transactions remain to be processed (`END-OF-FILE` = 'N'), WHEN the transaction's card number differs from the current card number, THE Account Break Reporting SHALL write the account total and separator lines when the report has already started ('N'), reset the account total to zero, make the new card current, and look up its cross-reference | medium | app/cbl/CBTRN03C.cbl:179,181-188,306-314, app/cbl/CBTRN03C.cbl:181-188 |
| DTPR-BR-059 | Enrich transaction with reference data | design note | WHEN an in-range transaction is ready for reporting, THE Transaction Reference Enrichment SHALL retrieve the account for the card, the transaction type description and the category description by type and category code, and abend the run when any reference record is not found (physical stores: `TRANCATG-FILE`, `TRANTYPE-FILE`, `XREF-FILE`) | medium | app/cbl/CBTRN03C.cbl:189-195,484-486,490-491,494-496,500-501,504-506,510-511, app/cbl/CBTRN03C.cbl:484-512 |
| DTPR-BR-060 | Report pagination every 20 lines | formatting | WHEN a detail line is about to be printed and the count of lines printed so far (headings, totals and separators included) is an exact multiple of 20, THE Daily Transaction Report SHALL first print the 'Page Total' line and a dashed line, then the report title line, a blank line, the column headings and a dashed line. | medium | app/cbl/CBTRN03C.cbl:129-132, app/cbl/CBTRN03C.cbl:181-184, app/cbl/CBTRN03C.cbl:282-289, app/cbl/CBTRN03C.cbl:293-341 |

### Key entities

- CVACT03Y (file record)
- CVTRA03Y (file record)
- CVTRA04Y (file record)
- CVTRA05Y (file record)
- CVTRA07Y (working storage)

### Needs clarification

- SME-043: The transaction report extract selects transactions using fixed dates (2022-01-01 to 2022-07-06), but the report itself takes its start and end dates from the run's date parameter. Should the extract period come from the same run parameter, and what should happen if the two periods differ? (Reporting owner) On DTPR-BR-058, DTPR-BR-059, DTPR-BR-057.
- SME-044: When the transaction report meets a transaction outside the reporting period, the program stops reading entirely, so later in-range transactions and the grand total are lost (the input is sorted by card, not date). Should out-of-range transactions just be skipped instead? Is it acceptable to rely only on the earlier sort step's date filter? (Reporting owner / batch operations lead) On DTPR-BR-058, DTPR-BR-059, DTPR-BR-057.
- SME-045: At the end of the transaction report, the last transaction's amount is added to the page, account and grand totals a second time, which overstates them. Is this double-counting intended, or should it be corrected? How critical are these totals? (Finance reporting owner) On DTPR-BR-058, DTPR-BR-059, DTPR-BR-057.
- SME-046: Should the transaction report print an 'Account Total' line for the last card at the end of the report? (Reporting owner) On DTPR-BR-058, DTPR-BR-059, DTPR-BR-057.
- SME-047: What page size does the transaction report need? Is 20 lines per page a business requirement, and should a page break happen whenever that size is reached, rather than only on exact multiples? (Reporting owner) On DTPR-BR-058, DTPR-BR-059, DTPR-BR-057, DTPR-BR-060.
- DEF-182: Is this intended? Account-total and page-total blocks add 2 lines at once, so the counter can skip over a multiple of 20 and a page runs on to the next multiple. Page length is therefore irregular, at up to about 40 lines. (Subject-matter expert) On DTPR-BR-060.

### Decision table gaps

None.
