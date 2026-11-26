# Tasks: Reach and move around the transaction report screen (OATM-C22)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C22-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174, OATM-REQ-F-175, OATM-REQ-F-176.
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
- [ ] OATM-C22-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-N-007, OATM-REQ-F-175, OATM-REQ-F-176. Rules: OATM-BR-181, OATM-BR-184, OATM-BR-185. After: OATM-C22-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C22-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-173, OATM-REQ-F-174. Rules: OATM-BR-182, OATM-BR-183. After: OATM-C22-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C22-T4 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST). Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174, OATM-REQ-F-175, OATM-REQ-F-176. Rules: OATM-BR-181, OATM-BR-182, OATM-BR-183, OATM-BR-184, OATM-BR-185. After: OATM-C22-T2, OATM-C22-T3.
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - button "Submit for printing"
  - link "Back"
- [ ] OATM-C22-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: OATM-REQ-N-007. Rules: OATM-BR-181. After: OATM-C22-T2, OATM-C22-T3.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - header "CardDemo"
- [ ] OATM-C22-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174, OATM-REQ-F-175, OATM-REQ-F-176. Criteria: OATM-C22-AC-01, OATM-C22-AC-02, OATM-C22-AC-03, OATM-C22-AC-04, OATM-C22-AC-05. After: OATM-C22-T1, OATM-C22-T2, OATM-C22-T3, OATM-C22-T4, OATM-C22-T5.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] OATM-C22-T7 [compliance] Review the handling of security. Requirements: OATM-REQ-N-007, OATM-REQ-F-173, OATM-REQ-F-174, OATM-REQ-F-175, OATM-REQ-F-176. After: OATM-C22-T1, OATM-C22-T2, OATM-C22-T3, OATM-C22-T4, OATM-C22-T5.
  - Check storage, logs, screens and audit against the rules.
