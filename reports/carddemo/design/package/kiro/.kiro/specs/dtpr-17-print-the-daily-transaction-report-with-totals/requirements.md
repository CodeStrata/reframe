# Requirements: Print the daily transaction report with totals (DTPR-C17)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Prints the daily transaction report for card operations analysts. Each in-period transaction gets a line with its ID, account, type, category, source and signed amount, followed by page totals, account totals and a grand total for reconciliation. The totals must add up exactly as the rules state, including the last transaction being counted a second time at end of file. Reporting must stop without any final totals as soon as a transaction outside the period is read.

**User story:** As a card operations analyst, I want each in-period transaction listed with its account, type, category, source and amount, with page, account and grand totals, so that I can review and reconcile the period's activity.

## Requirements

### Requirement 1: DTPR-REQ-F-082 (business rule)

#### Acceptance criteria

1. The system shall take the reporting period from the date parameter record, with the start date in positions 1-10 and the end date in positions 12-21 (YYYY-MM-DD), and treat a transaction as in range when the date part of its processing timestamp is between them inclusive, compared as text. (rules DTPR-BR-093)
2. GIVEN date parameters: 2022-01-01 2022-07-06; processing timestamp: 2022-03-15-10.22.33.000000 WHEN Daily Transaction Report runs THEN 2022-03-15 is in range, so the transaction is reported. (DTPR-C17-AC-01; DTPR-BR-093)
3. GIVEN date parameters: 2022-01-01 2022-07-06; processing timestamp: 2022-07-06-23.59.59.000000 WHEN Daily Transaction Report runs THEN 2022-07-06 equals the end date, so the transaction is reported. (DTPR-C17-AC-02; DTPR-BR-093)

### Requirement 2: DTPR-REQ-F-083 (business rule)

#### Acceptance criteria

1. When an in-range transaction is reported, the system shall add its amount to the current page total and the current card's account total before printing its detail line. (rules DTPR-BR-094)
2. GIVEN page total so far: 100.00; account total so far: 20.00; transaction amount: 50.00 WHEN an in-range transaction is reported THEN The page total becomes 150.00, the account total becomes 70.00 and the detail line is printed. (DTPR-C17-AC-03; DTPR-BR-094)

### Requirement 3: DTPR-REQ-F-084 (formatting)

#### Acceptance criteria

1. The system shall print each detail line with the transaction ID, the account ID from the card cross-reference, the type code and description joined by '-', the category code and description joined by '-', the source, and the amount, with a minus sign shown only for negatives. (rules DTPR-BR-095)
2. GIVEN amount: -25.00 WHEN Daily Transaction Report runs THEN The amount column shows -25.00. (DTPR-C17-AC-04; DTPR-BR-095)

### Requirement 4: DTPR-REQ-F-085 (business rule)

#### Acceptance criteria

1. When a page is closed, either at a page break or at the end of the transaction file, the system shall print a 'Page Total' line with the page's signed amount (e.g. +1,000.00), add that amount to the grand total, reset the page total to zero and print a dashed separator line. (rules DTPR-BR-096)
2. GIVEN detail amounts printed on page 1: 600.00, 400.00; event: page break before the next detail WHEN a page is closed, either at a page break or at the end of the transaction file THEN A 'Page Total' line showing +1,000.00 is printed, followed by a dashed line; the grand total becomes 1,000.00 and the page total restarts at 0. (DTPR-C17-AC-05; DTPR-BR-096)

### Requirement 5: DTPR-REQ-F-086 (business rule)

#### Acceptance criteria

1. When the end of the transaction file is reached, the system shall add the amount of the last transaction read to the page and account totals a second time, print the final 'Page Total' line, then print a 'Grand Total' line showing the sum of all page totals. (rules DTPR-BR-097)
2. GIVEN page 1 total: 1,000.00; page 2 details: 200.00, 50.00 (50.00 is the last transaction in the file) WHEN the end of the transaction file is reached THEN The final 'Page Total' shows +300.00 (250.00 plus 50.00 counted again) and the 'Grand Total' shows +1,300.00, not +1,250.00. (DTPR-C17-AC-06; DTPR-BR-097)

### Requirement 6: DTPR-REQ-F-087 (business rule)

#### Acceptance criteria

1. If a transaction read has a processing date outside the reporting period, then the system shall stop processing at once, skipping that and all later transactions, and close its files without printing the final page total, account total or grand total. (rules DTPR-BR-098)
2. GIVEN the date parameter record is '2022-01-01 2022-07-06', and the transaction file holds a transaction processed 2022-03-15-10.22.33.000000, then one processed 2022-07-07-09.00.00.000000, then one processed 2022-04-01-08.00.00.000000 WHEN the daily transaction report reads the 2022-07-07 transaction THEN processing stops at once: the 2022-03-15 transaction has its detail line, neither the 2022-07-07 transaction nor the later 2022-04-01 transaction is printed, the files are closed, and no final 'Page Total', account total or 'Grand Total' line is printed (DTPR-C17-AC-07; DTPR-BR-098)
