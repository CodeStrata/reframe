# Implementation plan: Run the transaction report job (DTPR-C16)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C16-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-081_
  - _Rules: DTPR-BR-091_
- [ ] 2. DTPR-C16-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-012_
  - _Rules: DTPR-BR-092_
- [ ] 3. DTPR-C16-T3 [api] Build the scheduled job
  - DTPR-BR-090: Run the report as a job step that starts only after the period extract exists. It reads the extract and does keyed lookups on the card cross-reference (card to account), transaction types and transaction categories, plus the report date parameters. It writes a new numbered version of the transaction report as 133-character print lines.
  - _Requirements: DTPR-REQ-F-080_
  - _Rules: DTPR-BR-090_
  - _After: DTPR-C16-T1, DTPR-C16-T2_
- [ ] 4. DTPR-C16-T4 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - **primary button** "Submit report": The dialog offers only Submit or Cancel, replacing the typed confirmation and its messages 'Please confirm to print the <report name> report...' and '"<value>" is not a valid value to confirm...'. If the job cannot be queued, the message says the report was not submitted and to try again.
  - _Requirements: DTPR-REQ-F-081_
  - _Rules: DTPR-BR-091_
  - _After: DTPR-C16-T1, DTPR-C16-T2, DTPR-C16-T3_
- [ ] 5. DTPR-C16-T5 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-080, DTPR-REQ-F-081, DTPR-REQ-N-012_
  - _Criteria: DTPR-C16-AC-01, DTPR-C16-AC-02, DTPR-C16-AC-03_
  - _After: DTPR-C16-T1, DTPR-C16-T2, DTPR-C16-T3, DTPR-C16-T4_
- [ ] 6. DTPR-C16-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-080, DTPR-REQ-F-081, DTPR-REQ-N-012_
  - _After: DTPR-C16-T1, DTPR-C16-T2, DTPR-C16-T3, DTPR-C16-T4_
