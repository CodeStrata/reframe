# Implementation plan: Validate a date against a format mask (OATM-C35)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as service.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

### Add transaction (S-TRANSACTION-ADD)

Enter a transaction against an account or card, see what to fix at each field, confirm the summary and record it.

Prototype: `ui-reference/index.html#/S-TRANSACTION-ADD`. Replaces the legacy screens COTRN2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Transaction reports (S-REPORT-REQUEST)

Choose a monthly, yearly or custom period and submit the transaction report for printing after confirming.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data model

None found in the source.

## Design notes

- OATM-BR-303: Provide a reusable date-validation function that takes a date string and a format pattern and returns a structured result: a 4-digit severity, a 4-digit message number and a reason. Implement it with the platform's standard strict date parsing, which rejects impossible dates. Map outcomes to the legacy message numbers (2507, 2508, 2509, 2513, 2517, 2518, 2521) where callers depend on them, for example the 2513 exception.
- OATM-BR-304: Return the result as a structured value (severity, message number, result text, tested date, mask used) with severity as the outcome code. Keep a formatter that renders the legacy 80-character text ('Mesg Code:', 'TstDate:', 'Mask used:') only if a consumer still needs that exact layout.

## Decision tables

#### Date validation result text by conversion feedback

| Date conversion feedback | Result text | Rule |
|---|---|---|
| All-zero feedback token | 'Date is valid' | OATM-BR-305 |
| X'000309CB59C3C5C5' (message 2507, insufficient data) | 'Insufficient' | OATM-BR-306 |
| X'000309CC59C3C5C5' (severity 3, message 2508, bad date value) | 'Datevalue error' | OATM-BR-307 |
| X'000309CD59C3C5C5' (message 2509, invalid era) | 'Invalid Era' | OATM-BR-308 |
| X'000309D159C3C5C5' (message 2513, unsupported range) | 'Unsupp. Range' | OATM-BR-309 |
| X'000309D559C3C5C5' (message 2517, invalid month) | 'Invalid month' | OATM-BR-310 |
| X'000309D659C3C5C5' (message 2518, bad format mask) | 'Bad Pic String' | OATM-BR-311 |
| X'000309D959C3C5C5' (message 2521, year-in-era zero) | 'YearInEra is 0' | OATM-BR-312 |
| Non-numeric characters in date | 'Nonnumeric data' with severity and message code | OATM-BR-313 |
| Any other feedback token | 'Date is invalid' | OATM-BR-314 |
| Non-numeric characters in date | **Gap:** The rules do not give the feedback token or message number for the non-numeric case; confirm which token the service returns. | |
| X'000309D159C3C5C5' (message 2513, unsupported range) | **Gap:** Callers accept message 2513 as not invalid even though the result text is 'Unsupp. Range'; confirm that dates outside the supported range should be accepted. | |

