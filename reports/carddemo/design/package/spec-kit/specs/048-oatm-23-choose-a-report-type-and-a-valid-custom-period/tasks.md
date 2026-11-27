# Tasks: Choose a report type and a valid custom period (OATM-C23)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C23-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-177, OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-180, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186.
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVTRA05Y.
- [ ] OATM-C23-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-177, OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186. Rules: OATM-BR-186, OATM-BR-187, OATM-BR-188, OATM-BR-190, OATM-BR-191, OATM-BR-192, OATM-BR-193, OATM-BR-194, OATM-BR-195. After: OATM-C23-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C23-T3 [api] Build the services behind the screens. Requirements: OATM-REQ-F-180. Rules: OATM-BR-189. After: OATM-C23-T1, OATM-C23-T2.
  - OATM-BR-189: Before validating, normalise the custom date inputs: pad month and day to two digits (for example '3' becomes '03') and year to four digits, so that the range checks and the calendar-date check see a consistent YYYY-MM-DD value. A typed date input or a date-parsing library in the new application can do this step.
- [ ] OATM-C23-T4 [ui-modernization] Build the screen Transaction reports (S-REPORT-REQUEST). Requirements: OATM-REQ-F-177, OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-180, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186. Rules: OATM-BR-186, OATM-BR-187, OATM-BR-188, OATM-BR-189, OATM-BR-190, OATM-BR-191, OATM-BR-192, OATM-BR-193, OATM-BR-194, OATM-BR-195. After: OATM-C23-T2, OATM-C23-T3.
  - To the prototype: ui-reference/index.html#/S-REPORT-REQUEST.
  - **summary card** "Report type": None chosen: 'Select a report type to print report...' - choose Monthly, Yearly or Custom.
  - **summary card** "Custom period": Every part is required, checked start month, day, year then end month, day, year ('Start Date - Month can NOT be empty...' and so on). 'Start Date - Not a valid Month...' / 'End Date - Not a valid Month...' (1 to 12); 'Start Date - Not a valid Day...' / 'End Date - Not a valid Day...' (1 to 31); 'Start Date - Not a valid Year...' / 'End Date - Not a valid Year...'; 'Start Date - Not a valid date...' / 'End Date - Not a valid date...' for a date not on the calendar. The message sits under the part to fix.
- [ ] OATM-C23-T5 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-177, OATM-REQ-F-178, OATM-REQ-F-179, OATM-REQ-F-180, OATM-REQ-F-181, OATM-REQ-F-182, OATM-REQ-F-183, OATM-REQ-F-184, OATM-REQ-F-185, OATM-REQ-F-186. Criteria: OATM-C23-AC-01, OATM-C23-AC-02, OATM-C23-AC-03, OATM-C23-AC-04, OATM-C23-AC-05, OATM-C23-AC-06, OATM-C23-AC-07, OATM-C23-AC-08, OATM-C23-AC-09, OATM-C23-AC-10, OATM-C23-AC-11, OATM-C23-AC-12, OATM-C23-AC-13. After: OATM-C23-T1, OATM-C23-T2, OATM-C23-T3, OATM-C23-T4.
  - 13 acceptance criteria, each a test named by its ID.
