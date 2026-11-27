# Requirements: Run the transaction report job (DTPR-C16)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Runs the transaction report over the period extract, looking up each card's account and the transaction type and category descriptions, and produces a new version of the formatted transaction report. When the analyst requests the report online, the dates they entered must be used instead of the stored date parameters. A failed run must never leave a partial report in place.

**User story:** As a card operations analyst, I want the transaction report produced from the period extract, using the dates I entered when I request it online, so that I receive a formatted report for the period I asked for.

## Requirements

### Requirement 1: DTPR-REQ-F-080 (design note)

#### Acceptance criteria

1. When the daily transaction extract for the run has been created, the system shall run the report program (CBTRN03C) against that extract and the card cross-reference, transaction type, transaction category and report date parameter files, and write a new generation of the transaction report (AWS.M2.CARDDEMO.TRANREPT) of 133-byte lines. (rules DTPR-BR-090)
2. GIVEN daily extract generation: created by the sort step; report step result: ends normally WHEN the daily transaction extract for the run has been created THEN A new generation of AWS.M2.CARDDEMO.TRANREPT is cataloged. (DTPR-C16-AC-01; DTPR-BR-090)

### Requirement 2: DTPR-REQ-F-081 (business rule)

#### Acceptance criteria

1. When the report is requested from the online report screen, the system shall take the report date parameters from the dates entered on that request instead of the stored date parameter file. (rules DTPR-BR-091)
2. GIVEN the stored report date parameters hold 2022-01-01 to 2022-07-06, and an analyst enters start date 2022-05-01 and end date 2022-05-31 on the online report screen WHEN the report is requested from the online report screen THEN the report runs with the date parameters 2022-05-01 to 2022-05-31 taken from that request, not the stored 2022-01-01 to 2022-07-06 (DTPR-C16-AC-03; DTPR-BR-091)

### Requirement 3: DTPR-REQ-N-012 (error handling)

#### Acceptance criteria

1. If the report step fails, then the system shall discard the new transaction report generation instead of cataloging it. (rules DTPR-BR-092)
2. GIVEN report step result: abends WHEN the report step fails THEN The new AWS.M2.CARDDEMO.TRANREPT generation is deleted. (DTPR-C16-AC-02; DTPR-BR-092)
