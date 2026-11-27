# Implementation plan: Extract transactions for a reporting period (DTPR-C15)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C15-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-075, DTPR-REQ-F-076, DTPR-REQ-F-077, DTPR-REQ-F-078_
  - _Rules: DTPR-BR-084, DTPR-BR-085, DTPR-BR-086, DTPR-BR-088_
- [ ] 2. DTPR-C15-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-011_
  - _Rules: DTPR-BR-087_
- [ ] 3. DTPR-C15-T3 [api] Build the scheduled job
  - DTPR-BR-083: Start each reporting run by copying every transaction record into a new numbered backup version, a point-in-time snapshot. Keep the version only if the copy completes, and discard it on failure so later steps never read a partial backup.
  - DTPR-BR-089: The sort test job needs a sorted extract: the selected transactions, in ascending card number order and with the same record layout as the backup, written as a new numbered version of the daily transaction file. Keep the version when the step succeeds and delete it when the step fails.
  - _Requirements: DTPR-REQ-F-074, DTPR-REQ-F-079_
  - _Rules: DTPR-BR-083, DTPR-BR-089_
  - _After: DTPR-C15-T1, DTPR-C15-T2_
- [ ] 4. DTPR-C15-T4 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - **primary button** "Submit report": The dialog offers only Submit or Cancel, replacing the typed confirmation and its messages 'Please confirm to print the <report name> report...' and '"<value>" is not a valid value to confirm...'. If the job cannot be queued, the message says the report was not submitted and to try again.
  - _Requirements: DTPR-REQ-F-077_
  - _Rules: DTPR-BR-086_
  - _After: DTPR-C15-T1, DTPR-C15-T2, DTPR-C15-T3_
- [ ] 5. DTPR-C15-T5 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-074, DTPR-REQ-F-075, DTPR-REQ-F-076, DTPR-REQ-F-077, DTPR-REQ-N-011, DTPR-REQ-F-078, DTPR-REQ-F-079_
  - _Criteria: DTPR-C15-AC-01, DTPR-C15-AC-02, DTPR-C15-AC-03, DTPR-C15-AC-04, DTPR-C15-AC-05, DTPR-C15-AC-06, DTPR-C15-AC-07, DTPR-C15-AC-08, DTPR-C15-AC-09, DTPR-C15-AC-10, DTPR-C15-AC-11_
  - _After: DTPR-C15-T1, DTPR-C15-T2, DTPR-C15-T3, DTPR-C15-T4_
- [ ] 6. DTPR-C15-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-074, DTPR-REQ-F-075, DTPR-REQ-F-076, DTPR-REQ-F-077, DTPR-REQ-N-011, DTPR-REQ-F-078, DTPR-REQ-F-079_
  - _After: DTPR-C15-T1, DTPR-C15-T2, DTPR-C15-T3, DTPR-C15-T4_
