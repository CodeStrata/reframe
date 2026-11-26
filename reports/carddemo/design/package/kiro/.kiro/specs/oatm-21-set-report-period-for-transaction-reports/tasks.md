# Implementation plan: Set report period for transaction reports (OATM-C21)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C21-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
  - _Requirements: OATM-REQ-F-171, OATM-REQ-F-172_
- [ ] 2. OATM-C21-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-171, OATM-REQ-F-172_
  - _Rules: OATM-BR-179, OATM-BR-180_
  - _After: OATM-C21-T1_
- [ ] 3. OATM-C21-T3 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - radio "Report period": Required: 'Select a report type to print report...'.
  - _Requirements: OATM-REQ-F-171, OATM-REQ-F-172_
  - _Rules: OATM-BR-179, OATM-BR-180_
  - _After: OATM-C21-T2_
- [ ] 4. OATM-C21-T4 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-171, OATM-REQ-F-172_
  - _Criteria: OATM-C21-AC-01, OATM-C21-AC-02, OATM-C21-AC-03_
  - _After: OATM-C21-T1, OATM-C21-T2, OATM-C21-T3_
