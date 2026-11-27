# Feature specification: Print the daily transaction report with totals

**Feature:** DTPR-C17 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C17)

As a card operations analyst, I want each in-period transaction listed with its account, type, category, source and amount, with page, account and grand totals, so that I can review and reconcile the period's activity.

Prints the daily transaction report for card operations analysts. Each in-period transaction gets a line with its ID, account, type, category, source and signed amount, followed by page totals, account totals and a grand total for reconciliation. The totals must add up exactly as the rules state, including the last transaction being counted a second time at end of file. Reporting must stop without any final totals as soon as a transaction outside the period is read.

**Acceptance scenarios:**

1. **Given** date parameters: 2022-01-01 2022-07-06; processing timestamp: 2022-03-15-10.22.33.000000, **when** Daily Transaction Report runs, **then** 2022-03-15 is in range, so the transaction is reported. (DTPR-C17-AC-01)
2. **Given** date parameters: 2022-01-01 2022-07-06; processing timestamp: 2022-07-06-23.59.59.000000, **when** Daily Transaction Report runs, **then** 2022-07-06 equals the end date, so the transaction is reported. (DTPR-C17-AC-02)
3. **Given** page total so far: 100.00; account total so far: 20.00; transaction amount: 50.00, **when** an in-range transaction is reported, **then** The page total becomes 150.00, the account total becomes 70.00 and the detail line is printed. (DTPR-C17-AC-03)
4. **Given** amount: -25.00, **when** Daily Transaction Report runs, **then** The amount column shows -25.00. (DTPR-C17-AC-04)
5. **Given** detail amounts printed on page 1: 600.00, 400.00; event: page break before the next detail, **when** a page is closed, either at a page break or at the end of the transaction file, **then** A 'Page Total' line showing +1,000.00 is printed, followed by a dashed line; the grand total becomes 1,000.00 and the page total restarts at 0. (DTPR-C17-AC-05)
6. **Given** page 1 total: 1,000.00; page 2 details: 200.00, 50.00 (50.00 is the last transaction in the file), **when** the end of the transaction file is reached, **then** The final 'Page Total' shows +300.00 (250.00 plus 50.00 counted again) and the 'Grand Total' shows +1,300.00, not +1,250.00. (DTPR-C17-AC-06)
7. **Given** the date parameter record is '2022-01-01 2022-07-06', and the transaction file holds a transaction processed 2022-03-15-10.22.33.000000, then one processed 2022-07-07-09.00.00.000000, then one processed 2022-04-01-08.00.00.000000, **when** the daily transaction report reads the 2022-07-07 transaction, **then** processing stops at once: the 2022-03-15 transaction has its detail line, neither the 2022-07-07 transaction nor the later 2022-04-01 transaction is printed, the files are closed, and no final 'Page Total', account total or 'Grand Total' line is printed (DTPR-C17-AC-07)

## Requirements

### Functional requirements

- **DTPR-REQ-F-082** (business rule): The system shall take the reporting period from the date parameter record, with the start date in positions 1-10 and the end date in positions 12-21 (YYYY-MM-DD), and treat a transaction as in range when the date part of its processing timestamp is between them inclusive, compared as text. Rules: DTPR-BR-093.
- **DTPR-REQ-F-083** (business rule): When an in-range transaction is reported, the system shall add its amount to the current page total and the current card's account total before printing its detail line. Rules: DTPR-BR-094.
- **DTPR-REQ-F-084** (formatting): The system shall print each detail line with the transaction ID, the account ID from the card cross-reference, the type code and description joined by '-', the category code and description joined by '-', the source, and the amount, with a minus sign shown only for negatives. Rules: DTPR-BR-095.
- **DTPR-REQ-F-085** (business rule): When a page is closed, either at a page break or at the end of the transaction file, the system shall print a 'Page Total' line with the page's signed amount (e.g. +1,000.00), add that amount to the grand total, reset the page total to zero and print a dashed separator line. Rules: DTPR-BR-096.
- **DTPR-REQ-F-086** (business rule): When the end of the transaction file is reached, the system shall add the amount of the last transaction read to the page and account totals a second time, print the final 'Page Total' line, then print a 'Grand Total' line showing the sum of all page totals. Rules: DTPR-BR-097.
- **DTPR-REQ-F-087** (business rule): If a transaction read has a processing date outside the reporting period, then the system shall stop processing at once, skipping that and all later transactions, and close its files without printing the final page total, account total or grand total. Rules: DTPR-BR-098.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-093 | Filter transactions by reporting period | business rule | THE Daily Transaction Report SHALL take its reporting period from the date parameter record, with the start date in positions 1-10 and the end date in positions 12-21 (YYYY-MM-DD), and SHALL treat a transaction as in range when the date part of its processing timestamp is between them inclusive, compared as text. | high | app/cbl/CBTRN03C.cbl:122-125, app/cbl/CBTRN03C.cbl:170-178, app/cbl/CBTRN03C.cbl:206-213, app/cpy/CVTRA05Y.cpy:4-19 |
| DTPR-BR-094 | Write transaction detail line | business rule | WHEN an in-range transaction is reported, THE Daily Transaction Report SHALL add its amount to the current page total and the current card's account total before printing its detail line. | high | app/cbl/CBTRN03C.cbl:181-196, app/cbl/CBTRN03C.cbl:287-289, app/cbl/CBTRN03C.cbl:361-374, app/cpy/CVTRA07Y.cpy:15-31 |
| DTPR-BR-095 | Write transaction detail line | formatting | THE Daily Transaction Report SHALL print each detail line with the transaction ID, the account ID from the card cross-reference, the type code and description joined by '-', the category code and description joined by '-', the source, and the amount (a minus sign shows only for negatives). | high | app/cbl/CBTRN03C.cbl:181-196, app/cbl/CBTRN03C.cbl:287-289, app/cbl/CBTRN03C.cbl:361-374, app/cpy/CVTRA07Y.cpy:15-31 |
| DTPR-BR-096 | Print page total and roll into grand total | business rule | WHEN a page is closed, either at a page break or at the end of the transaction file, THE Daily Transaction Report SHALL print a 'Page Total' line with the page's amount (signed, e.g. +1,000.00), add that amount to the grand total, reset the page total to zero and print a dashed separator line. | high | app/cbl/CBTRN03C.cbl:197-204, app/cbl/CBTRN03C.cbl:282-289, app/cbl/CBTRN03C.cbl:293-304, app/cbl/CBTRN03C.cbl:318-322 |
| DTPR-BR-097 | Print final page and grand totals | business rule | WHEN the end of the transaction file is reached, THE Daily Transaction Report SHALL add the amount of the last transaction read to the page and account totals a second time, print the final 'Page Total' line, then print a 'Grand Total' line showing the sum of all page totals. | high | app/cbl/CBTRN03C.cbl:197-204, app/cbl/CBTRN03C.cbl:282-289, app/cbl/CBTRN03C.cbl:293-304, app/cbl/CBTRN03C.cbl:318-322 |
| DTPR-BR-098 | Filter transactions by reporting period | business rule | WHEN a transaction read has a processing date outside the reporting period, THE Daily Transaction Report SHALL stop processing at once, skipping that and all later transactions, and SHALL close its files without printing the final page total, account total or grand total. | high | app/cbl/CBTRN03C.cbl:122-125, app/cbl/CBTRN03C.cbl:170-178, app/cbl/CBTRN03C.cbl:206-213, app/cpy/CVTRA05Y.cpy:4-19 |

### Key entities

- CVACT03Y (file record)
- CVTRA03Y (file record)
- CVTRA04Y (file record)
- CVTRA05Y (file record)
- CVTRA07Y (working storage)

### Needs clarification

- SME-043: The transaction report extract selects transactions using fixed dates (2022-01-01 to 2022-07-06), but the report itself takes its start and end dates from the run's date parameter. Should the extract period come from the same run parameter, and what should happen if the two periods differ? (Reporting owner) On DTPR-BR-096, DTPR-BR-097, DTPR-BR-098, DTPR-BR-095.
- SME-044: When the transaction report meets a transaction outside the reporting period, the program stops reading entirely, so later in-range transactions and the grand total are lost (the input is sorted by card, not date). Should out-of-range transactions just be skipped instead? Is it acceptable to rely only on the earlier sort step's date filter? (Reporting owner / batch operations lead) On DTPR-BR-096, DTPR-BR-097, DTPR-BR-098, DTPR-BR-095.
- SME-045: At the end of the transaction report, the last transaction's amount is added to the page, account and grand totals a second time, which overstates them. Is this double-counting intended, or should it be corrected? How critical are these totals? (Finance reporting owner) On DTPR-BR-096, DTPR-BR-097, DTPR-BR-098, DTPR-BR-095.
- SME-046: Should the transaction report print an 'Account Total' line for the last card at the end of the report? (Reporting owner) On DTPR-BR-096, DTPR-BR-097, DTPR-BR-098, DTPR-BR-095.
- SME-047: What page size does the transaction report need? Is 20 lines per page a business requirement, and should a page break happen whenever that size is reached, rather than only on exact multiples? (Reporting owner) On DTPR-BR-096, DTPR-BR-097, DTPR-BR-098, DTPR-BR-095.
- DEF-010: Is this intended? At end of file the last transaction's amount is added to the page and account totals a second time. The end-of-file read leaves the previous record in place, so the final page total and the grand total are overstated by that amount. The last card's account total is never printed at end of file. If the file is empty, the totals are printed without any heading. (Subject-matter expert) On DTPR-BR-096, DTPR-BR-097.
- DEF-035: Is this intended? An out-of-range transaction ends the whole report run without totals, when the IF/CONTINUE structure shows the intent was only to skip it. In practice the preceding SORT step filters by the same dates, so this only happens when the DATEPARM record and the SORT dates differ. That can happen in the standalone TRANREPT job, which hard-codes the SORT dates. (Subject-matter expert) On DTPR-BR-098.

### Decision table gaps

- Report handling of each read: No rule says what amount is added a second time, or what totals print, when the file is empty.
