# Tasks: Confirm and submit a transaction report for printing (OATM-C24)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C24-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-189, OATM-REQ-F-190, OATM-REQ-F-191, OATM-REQ-F-192, OATM-REQ-F-193, OATM-REQ-F-194.
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
- [ ] OATM-C24-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-189, OATM-REQ-F-190, OATM-REQ-F-192. Rules: OATM-BR-196, OATM-BR-197, OATM-BR-198, OATM-BR-199, OATM-BR-201. After: OATM-C24-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C24-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-193, OATM-REQ-F-194. Rules: OATM-BR-202, OATM-BR-203, OATM-BR-204. After: OATM-C24-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C24-T4 [api] Build the services behind the screens. Requirements: OATM-REQ-F-191. Rules: OATM-BR-200. After: OATM-C24-T1, OATM-C24-T2, OATM-C24-T3.
  - OATM-BR-200: The report job needs the start and end dates as YYYY-MM-DD parameters, plus a combined 'YYYY-MM-DD YYYY-MM-DD' date value. The new application should pass these as named parameters on the job submission request (for example, a message to the batch scheduler or a job-run API). It should not edit a job script text.
- [ ] OATM-C24-T5 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST). Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-190, OATM-REQ-F-193, OATM-REQ-F-194. Rules: OATM-BR-196, OATM-BR-197, OATM-BR-199, OATM-BR-202, OATM-BR-203, OATM-BR-204. After: OATM-C24-T2, OATM-C24-T3, OATM-C24-T4.
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - dialog "Print this report?"
  - message "Submission result"
- [ ] OATM-C24-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-189, OATM-REQ-F-190, OATM-REQ-F-191, OATM-REQ-F-192, OATM-REQ-F-193, OATM-REQ-F-194. Criteria: OATM-C24-AC-01, OATM-C24-AC-02, OATM-C24-AC-03, OATM-C24-AC-04, OATM-C24-AC-05, OATM-C24-AC-06, OATM-C24-AC-07, OATM-C24-AC-08, OATM-C24-AC-09. After: OATM-C24-T1, OATM-C24-T2, OATM-C24-T3, OATM-C24-T4, OATM-C24-T5.
  - 9 acceptance criteria, each a test named by its ID.
