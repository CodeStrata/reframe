# Tasks: Set report period for transaction reports (OATM-C21)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C21-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-171, OATM-REQ-F-172.
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
- [ ] OATM-C21-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-171, OATM-REQ-F-172. Rules: OATM-BR-179, OATM-BR-180. After: OATM-C21-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C21-T3 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST). Requirements: OATM-REQ-F-171, OATM-REQ-F-172. Rules: OATM-BR-179, OATM-BR-180. After: OATM-C21-T2.
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - radio "Report period": Required: 'Select a report type to print report...'.
- [ ] OATM-C21-T4 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-171, OATM-REQ-F-172. Criteria: OATM-C21-AC-01, OATM-C21-AC-02, OATM-C21-AC-03. After: OATM-C21-T1, OATM-C21-T2, OATM-C21-T3.
  - 3 acceptance criteria, each a test named by its ID.
