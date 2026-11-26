# Implementation plan: Reach and move around the transaction report screen (OATM-C22)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C22-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174, OATM-REQ-F-175, OATM-REQ-F-176_
- [ ] 2. OATM-C22-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-175, OATM-REQ-F-176_
  - _Rules: OATM-BR-181, OATM-BR-184, OATM-BR-185_
  - _After: OATM-C22-T1_
- [ ] 3. OATM-C22-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-173, OATM-REQ-F-174_
  - _Rules: OATM-BR-182, OATM-BR-183_
  - _After: OATM-C22-T1_
- [ ] 4. OATM-C22-T4 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - **primary button** "Submit report": The dialog offers only Submit or Cancel, replacing the typed confirmation and its messages 'Please confirm to print the <report name> report...' and '"<value>" is not a valid value to confirm...'. If the job cannot be queued, the message says the report was not submitted and to try again.
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-175, OATM-REQ-F-176_
  - _Rules: OATM-BR-181, OATM-BR-184, OATM-BR-185_
  - _After: OATM-C22-T2, OATM-C22-T3_
- [ ] 5. OATM-C22-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **summary card** "CardDemo"
  - **primary button** "Transaction reports"
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174_
  - _Rules: OATM-BR-181, OATM-BR-182, OATM-BR-183_
  - _After: OATM-C22-T2, OATM-C22-T3_
- [ ] 6. OATM-C22-T6 [test-generation] Write a test for every acceptance criterion
  - 5 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174, OATM-REQ-F-175, OATM-REQ-F-176_
  - _Criteria: OATM-C22-AC-01, OATM-C22-AC-02, OATM-C22-AC-03, OATM-C22-AC-04, OATM-C22-AC-05_
  - _After: OATM-C22-T1, OATM-C22-T2, OATM-C22-T3, OATM-C22-T4, OATM-C22-T5_
- [ ] 7. OATM-C22-T7 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174, OATM-REQ-F-175, OATM-REQ-F-176_
  - _After: OATM-C22-T1, OATM-C22-T2, OATM-C22-T3, OATM-C22-T4, OATM-C22-T5_
