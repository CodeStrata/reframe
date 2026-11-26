# Implementation plan: Confirm and submit a transaction report for printing (OATM-C24)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C24-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
  - _Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-189, OATM-REQ-F-190, OATM-REQ-F-191, OATM-REQ-F-192, OATM-REQ-F-193, OATM-REQ-F-194_
- [ ] 2. OATM-C24-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-189, OATM-REQ-F-190, OATM-REQ-F-192_
  - _Rules: OATM-BR-196, OATM-BR-197, OATM-BR-198, OATM-BR-199, OATM-BR-201_
  - _After: OATM-C24-T1_
- [ ] 3. OATM-C24-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-193, OATM-REQ-F-194_
  - _Rules: OATM-BR-202, OATM-BR-203, OATM-BR-204_
  - _After: OATM-C24-T1_
- [ ] 4. OATM-C24-T4 [api] Build the services behind the screens
  - OATM-BR-200: The report job needs the start and end dates as YYYY-MM-DD parameters, plus a combined 'YYYY-MM-DD YYYY-MM-DD' date value. The new application should pass these as named parameters on the job submission request (for example, a message to the batch scheduler or a job-run API). It should not edit a job script text.
  - _Requirements: OATM-REQ-F-191_
  - _Rules: OATM-BR-200_
  - _After: OATM-C24-T1, OATM-C24-T2, OATM-C24-T3_
- [ ] 5. OATM-C24-T5 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - dialog "Print this report?"
  - message "Submission result"
  - _Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-190, OATM-REQ-F-193, OATM-REQ-F-194_
  - _Rules: OATM-BR-196, OATM-BR-197, OATM-BR-199, OATM-BR-202, OATM-BR-203, OATM-BR-204_
  - _After: OATM-C24-T2, OATM-C24-T3, OATM-C24-T4_
- [ ] 6. OATM-C24-T6 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-187, OATM-REQ-F-188, OATM-REQ-F-189, OATM-REQ-F-190, OATM-REQ-F-191, OATM-REQ-F-192, OATM-REQ-F-193, OATM-REQ-F-194_
  - _Criteria: OATM-C24-AC-01, OATM-C24-AC-02, OATM-C24-AC-03, OATM-C24-AC-04, OATM-C24-AC-05, OATM-C24-AC-06, OATM-C24-AC-07, OATM-C24-AC-08, OATM-C24-AC-09_
  - _After: OATM-C24-T1, OATM-C24-T2, OATM-C24-T3, OATM-C24-T4, OATM-C24-T5_
