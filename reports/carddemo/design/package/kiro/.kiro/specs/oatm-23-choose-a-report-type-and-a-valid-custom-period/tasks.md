# Implementation plan: Choose a report type and a valid custom period (OATM-C23)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C23-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
  - _Requirements: OATM-REQ-F-177, OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-180, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186_
- [ ] 2. OATM-C23-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-177, OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186_
  - _Rules: OATM-BR-186, OATM-BR-187, OATM-BR-188, OATM-BR-190, OATM-BR-191, OATM-BR-192, OATM-BR-193, OATM-BR-194, OATM-BR-195_
  - _After: OATM-C23-T1_
- [ ] 3. OATM-C23-T3 [api] Build the services behind the screens
  - OATM-BR-189: Before validating, turn the entered month and day into two-digit numbers and the year into a four-digit number (for example, '3' becomes '03'). This makes the range checks and the YYYY-MM-DD calendar check work on a consistent form. A standard date-parsing library can then do the calendar check.
  - _Requirements: OATM-REQ-F-180_
  - _Rules: OATM-BR-189_
  - _After: OATM-C23-T1, OATM-C23-T2_
- [ ] 4. OATM-C23-T4 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST)
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - radio "Report period": Required: 'Select a report type to print report...'.
  - date "Start date": Month, day and year required: 'Start Date - Month can NOT be empty...', 'Start Date - Day can NOT be empty...', 'Start Date - Year can NOT be empty...'; 'Start Date - Not a valid Month...'; 'Start Date - Not a valid Day...'; 'Start Date - Not a valid Year...'; must be a real date: 'Start Date - Not a valid date...'.
  - date "End date": Month, day and year required: 'End Date - Month can NOT be empty...', 'End Date - Day can NOT be empty...', 'End Date - Year can NOT be empty...'; 'End Date - Not a valid Month...'; 'End Date - Not a valid Day...'; 'End Date - Not a valid Year...'; must be a real date: 'End Date - Not a valid date...'.
  - _Requirements: OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-181, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186_
  - _Rules: OATM-BR-187, OATM-BR-188, OATM-BR-190, OATM-BR-193, OATM-BR-194, OATM-BR-195_
  - _After: OATM-C23-T2, OATM-C23-T3_
- [ ] 5. OATM-C23-T5 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-177, OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-180, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186_
  - _Criteria: OATM-C23-AC-01, OATM-C23-AC-02, OATM-C23-AC-03, OATM-C23-AC-04, OATM-C23-AC-05, OATM-C23-AC-06, OATM-C23-AC-07, OATM-C23-AC-08, OATM-C23-AC-09, OATM-C23-AC-10, OATM-C23-AC-11, OATM-C23-AC-12, OATM-C23-AC-13_
  - _After: OATM-C23-T1, OATM-C23-T2, OATM-C23-T3, OATM-C23-T4_
