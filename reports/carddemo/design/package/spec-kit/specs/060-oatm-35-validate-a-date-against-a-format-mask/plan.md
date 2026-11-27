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

### Transaction reports (S-REPORT-REQUEST)

Submit a monthly, yearly or custom-period transaction report for printing. The report type is a single choice, the custom dates appear only for Custom, and submission is confirmed in a dialog. Tab order: report type, start date, end date, Submit report.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Transactions (S-TRANSACTION-LIST)

Browse transactions in a sortable, paged table or jump to a transaction ID, and open one with Enter or a click instead of typing S beside it. Tab order: search, table, pager, Add transaction.

Prototype: `ui-reference/index.html#/S-TRANSACTION-LIST`. Replaces the legacy screens COTRN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Add transaction (S-TRANSACTION-ADD)

Record a new transaction against an account or card, every field checked before it is added. One field takes the account or the card number; the resolved account and card show at once. Tab order: account or card, transaction details, merchant, Add transaction.

Prototype: `ui-reference/index.html#/S-TRANSACTION-ADD`. Replaces the legacy screens COTRN2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data model

None found in the source.

## Design notes

- OATM-BR-303: Expose date validation as one shared function or service that takes a date string and a format mask and returns a structured result (severity, message code, reason). Implement it with the platform's standard date-parsing library instead of the mainframe date service, and keep the legacy severity/message codes (0000, 2508, 2513 and so on) only as far as callers need them to tell valid from invalid.
- OATM-BR-304: Callers need a result they can test: a severity/status, a message code, the reason text, and the tested date and mask for diagnostics. A typed result object replaces the fixed 80-character string and the program return code. Keep the layout only if a remaining legacy consumer still reads it.

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

