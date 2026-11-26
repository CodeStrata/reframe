# Requirements: Produce daily transaction report (DTPR-C06)

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
