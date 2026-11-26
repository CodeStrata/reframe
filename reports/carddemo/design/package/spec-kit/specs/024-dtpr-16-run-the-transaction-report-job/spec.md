# Feature specification: Run the transaction report job

**Feature:** DTPR-C16 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C16)

As a card operations analyst, I want the transaction report produced from the period extract, using the dates I entered when I request it online, so that I receive a formatted report for the period I asked for.

Runs the transaction report over the period extract, looking up each card's account and the transaction type and category descriptions, and produces a new version of the formatted transaction report. When the analyst requests the report online, the dates they entered must be used instead of the stored date parameters. A failed run must never leave a partial report in place.

**Acceptance scenarios:**

1. **Given** daily extract generation: created by the sort step; report step result: ends normally, **when** the daily transaction extract for the run has been created, **then** A new generation of AWS.M2.CARDDEMO.TRANREPT is cataloged. (DTPR-C16-AC-01)
2. **Given** report step result: abends, **when** the report step fails, **then** The new AWS.M2.CARDDEMO.TRANREPT generation is deleted. (DTPR-C16-AC-02)
3. **Given** the stored report date parameters hold 2022-01-01 to 2022-07-06, and an analyst enters start date 2022-05-01 and end date 2022-05-31 on the online report screen, **when** the report is requested from the online report screen, **then** the report runs with the date parameters 2022-05-01 to 2022-05-31 taken from that request, not the stored 2022-01-01 to 2022-07-06 (DTPR-C16-AC-03)

## Requirements

### Functional requirements

- **DTPR-REQ-F-080** (design note): When the daily transaction extract for the run has been created, the system shall run the report program (CBTRN03C) against that extract and the card cross-reference, transaction type, transaction category and report date parameter files, and write a new generation of the transaction report (AWS.M2.CARDDEMO.TRANREPT) of 133-byte lines. Rules: DTPR-BR-090.
- **DTPR-REQ-F-081** (business rule): When the report is requested from the online report screen, the system shall take the report date parameters from the dates entered on that request instead of the stored date parameter file. Rules: DTPR-BR-091.
- **DTPR-REQ-N-012** (error handling): If the report step fails, then the system shall discard the new transaction report generation instead of cataloging it. Rules: DTPR-BR-092.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-090 | Produce the formatted transaction report | design note | WHEN the daily transaction extract for the run has been created, THE Transaction Reporting Run SHALL run the report program (CBTRN03C) against that extract, the card cross-reference, transaction type, transaction category and report date parameter files, and write a new generation of the transaction report (AWS.M2.CARDDEMO.TRANREPT) of 133-byte lines. | medium | app/jcl/TRANREPT.jcl:59-80, app/proc/TRANREPT.prc:57-78, app/cbl/CORPT00C.cbl:84-125 |
| DTPR-BR-091 | Produce the formatted transaction report | business rule | WHEN the report is requested from the online report screen, THE Transaction Reporting Run SHALL take the report date parameters from the dates entered on that request instead of the stored date parameter file. | medium | app/jcl/TRANREPT.jcl:59-80, app/proc/TRANREPT.prc:57-78, app/cbl/CORPT00C.cbl:84-125 |
| DTPR-BR-092 | Produce the formatted transaction report | error handling | WHEN the report step fails, THE Transaction Reporting Run SHALL discard the new transaction report generation instead of cataloging it. | medium | app/jcl/TRANREPT.jcl:59-80, app/proc/TRANREPT.prc:57-78, app/cbl/CORPT00C.cbl:84-125 |

### Key entities

None found in the source.

### Needs clarification

- SME-043: The transaction report extract selects transactions using fixed dates (2022-01-01 to 2022-07-06), but the report itself takes its start and end dates from the run's date parameter. Should the extract period come from the same run parameter, and what should happen if the two periods differ? (Reporting owner) On DTPR-BR-092.
- SME-044: When the transaction report meets a transaction outside the reporting period, the program stops reading entirely, so later in-range transactions and the grand total are lost (the input is sorted by card, not date). Should out-of-range transactions just be skipped instead? Is it acceptable to rely only on the earlier sort step's date filter? (Reporting owner / batch operations lead) On DTPR-BR-092.
- SME-045: At the end of the transaction report, the last transaction's amount is added to the page, account and grand totals a second time, which overstates them. Is this double-counting intended, or should it be corrected? How critical are these totals? (Finance reporting owner) On DTPR-BR-092.
- SME-046: Should the transaction report print an 'Account Total' line for the last card at the end of the report? (Reporting owner) On DTPR-BR-092.
- SME-047: What page size does the transaction report need? Is 20 lines per page a business requirement, and should a page break happen whenever that size is reached, rather than only on exact multiples? (Reporting owner) On DTPR-BR-092.

### Decision table gaps

None.
