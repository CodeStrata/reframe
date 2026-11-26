# Print the daily transaction report with totals (DTPR-C17)

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

## Screens and components

No screens: it runs as scheduled job.

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
| DTPR-BR-093 | Filter transactions by reporting period | business rule | THE Daily Transaction Report SHALL take its reporting period from the date parameter record, with the start date in positions 1-10 and the end date in positions 12-21 (YYYY-MM-DD), and SHALL treat a transaction as in range when the date part of its processing timestamp is between them inclusive, compared as text. | high | app/cbl/CBTRN03C.cbl:122-125, app/cbl/CBTRN03C.cbl:170-178, app/cbl/CBTRN03C.cbl:206-213, app/cpy/CVTRA05Y.cpy:4-19 |
| DTPR-BR-094 | Write transaction detail line | business rule | WHEN an in-range transaction is reported, THE Daily Transaction Report SHALL add its amount to the current page total and the current card's account total before printing its detail line. | high | app/cbl/CBTRN03C.cbl:181-196, app/cbl/CBTRN03C.cbl:287-289, app/cbl/CBTRN03C.cbl:361-374, app/cpy/CVTRA07Y.cpy:15-31 |
| DTPR-BR-095 | Write transaction detail line | formatting | THE Daily Transaction Report SHALL print each detail line with the transaction ID, the account ID from the card cross-reference, the type code and description joined by '-', the category code and description joined by '-', the source, and the amount (a minus sign shows only for negatives). | high | app/cbl/CBTRN03C.cbl:181-196, app/cbl/CBTRN03C.cbl:287-289, app/cbl/CBTRN03C.cbl:361-374, app/cpy/CVTRA07Y.cpy:15-31 |
| DTPR-BR-096 | Print page total and roll into grand total | business rule | WHEN a page is closed, either at a page break or at the end of the transaction file, THE Daily Transaction Report SHALL print a 'Page Total' line with the page's amount (signed, e.g. +1,000.00), add that amount to the grand total, reset the page total to zero and print a dashed separator line. | high | app/cbl/CBTRN03C.cbl:197-204, app/cbl/CBTRN03C.cbl:282-289, app/cbl/CBTRN03C.cbl:293-304, app/cbl/CBTRN03C.cbl:318-322 |
| DTPR-BR-097 | Print final page and grand totals | business rule | WHEN the end of the transaction file is reached, THE Daily Transaction Report SHALL add the amount of the last transaction read to the page and account totals a second time, print the final 'Page Total' line, then print a 'Grand Total' line showing the sum of all page totals. | high | app/cbl/CBTRN03C.cbl:197-204, app/cbl/CBTRN03C.cbl:282-289, app/cbl/CBTRN03C.cbl:293-304, app/cbl/CBTRN03C.cbl:318-322 |
| DTPR-BR-098 | Filter transactions by reporting period | business rule | WHEN a transaction read has a processing date outside the reporting period, THE Daily Transaction Report SHALL stop processing at once, skipping that and all later transactions, and SHALL close its files without printing the final page total, account total or grand total. | high | app/cbl/CBTRN03C.cbl:122-125, app/cbl/CBTRN03C.cbl:170-178, app/cbl/CBTRN03C.cbl:206-213, app/cpy/CVTRA05Y.cpy:4-19 |

### Worked examples

- DTPR-BR-093: date parameters = 2022-01-01 2022-07-06; processing timestamp = 2022-03-15-10.22.33.000000 → 2022-03-15 is in range, so the transaction is reported.
- DTPR-BR-093: date parameters = 2022-01-01 2022-07-06; processing timestamp = 2022-07-06-23.59.59.000000 → 2022-07-06 equals the end date, so the transaction is reported.
- DTPR-BR-094: page total so far = 100.00; account total so far = 20.00; transaction amount = 50.00 → The page total becomes 150.00, the account total becomes 70.00 and the detail line is printed.
- DTPR-BR-095: amount = -25.00 → The amount column shows -25.00.
- DTPR-BR-096: detail amounts printed on page 1 = 600.00, 400.00; event = page break before the next detail → A 'Page Total' line showing +1,000.00 is printed, followed by a dashed line; the grand total becomes 1,000.00 and the page total restarts at 0.
- DTPR-BR-097: page 1 total = 1,000.00; page 2 details = 200.00, 50.00 (50.00 is the last transaction in the file) → The final 'Page Total' shows +300.00 (250.00 plus 50.00 counted again) and the 'Grand Total' shows +1,300.00, not +1,250.00.

## Decision tables

#### Report handling of each read

| Read result | Processing date within reporting period | Report action | Rule |
|---|---|---|---|
| Transaction read | Yes | Add amount to page total and account total, then print detail line | DTPR-BR-094 |
| Transaction read | No | Stop at once, skip this and all later transactions, close files without final page, account or grand totals | DTPR-BR-098 |
| End of transaction file | Not applicable | Add last transaction's amount to page and account totals a second time, print final 'Page Total', then 'Grand Total' | DTPR-BR-097 |
| End of transaction file | No transaction read at all | **Gap:** No rule says what amount is added a second time, or what totals print, when the file is empty. | |


## Design notes

None.

## Open questions

- SME-043: The transaction report extract selects transactions using fixed dates (2022-01-01 to 2022-07-06), but the report itself takes its start and end dates from the run's date parameter. Should the extract period come from the same run parameter, and what should happen if the two periods differ? (Reporting owner) On DTPR-BR-096, DTPR-BR-097, DTPR-BR-098, DTPR-BR-095.
- SME-044: When the transaction report meets a transaction outside the reporting period, the program stops reading entirely, so later in-range transactions and the grand total are lost (the input is sorted by card, not date). Should out-of-range transactions just be skipped instead? Is it acceptable to rely only on the earlier sort step's date filter? (Reporting owner / batch operations lead) On DTPR-BR-096, DTPR-BR-097, DTPR-BR-098, DTPR-BR-095.
- SME-045: At the end of the transaction report, the last transaction's amount is added to the page, account and grand totals a second time, which overstates them. Is this double-counting intended, or should it be corrected? How critical are these totals? (Finance reporting owner) On DTPR-BR-096, DTPR-BR-097, DTPR-BR-098, DTPR-BR-095.
- SME-046: Should the transaction report print an 'Account Total' line for the last card at the end of the report? (Reporting owner) On DTPR-BR-096, DTPR-BR-097, DTPR-BR-098, DTPR-BR-095.
- SME-047: What page size does the transaction report need? Is 20 lines per page a business requirement, and should a page break happen whenever that size is reached, rather than only on exact multiples? (Reporting owner) On DTPR-BR-096, DTPR-BR-097, DTPR-BR-098, DTPR-BR-095.
- DEF-010: Is this intended? At end of file the last transaction's amount is added to the page and account totals a second time. The end-of-file read leaves the previous record in place, so the final page total and the grand total are overstated by that amount. The last card's account total is never printed at end of file. If the file is empty, the totals are printed without any heading. (Subject-matter expert) On DTPR-BR-096, DTPR-BR-097.
- DEF-035: Is this intended? An out-of-range transaction ends the whole report run without totals, when the IF/CONTINUE structure shows the intent was only to skip it. In practice the preceding SORT step filters by the same dates, so this only happens when the DATEPARM record and the SORT dates differ. That can happen in the standalone TRANREPT job, which hard-codes the SORT dates. (Subject-matter expert) On DTPR-BR-098.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).
