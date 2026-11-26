# Implementation plan: Mark a list row for update or delete (TTRDM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C08-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-056, TTRDM-REQ-F-057, TTRDM-REQ-F-058, TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-061, TTRDM-REQ-F-062, TTRDM-REQ-F-063, TTRDM-REQ-F-064_
- [ ] 2. TTRDM-C08-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-056, TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-061, TTRDM-REQ-F-062, TTRDM-REQ-F-063_
  - _Rules: TTRDM-BR-065, TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-070, TTRDM-BR-071, TTRDM-BR-072_
  - _After: TTRDM-C08-T1_
- [ ] 3. TTRDM-C08-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-064_
  - _Rules: TTRDM-BR-073_
  - _After: TTRDM-C08-T1_
- [ ] 4. TTRDM-C08-T4 [api] Build the services behind the screens
  - TTRDM-BR-066: When the filters are unchanged, go through the 7 submitted rows and count three things: rows with any non-blank action, rows marked 'D' and rows marked 'U'. The counts drive the 'only one action' and invalid-code checks.
  - TTRDM-BR-067: Record the index of the top-most row marked 'D' or 'U' (0 if none) as the selected row in session state. Compare it with the selected row saved from the previous screen and set a 'selection changed' flag, which the F10 confirmation step uses.
  - _Requirements: TTRDM-REQ-F-057, TTRDM-REQ-F-058_
  - _Rules: TTRDM-BR-066, TTRDM-BR-067_
  - _After: TTRDM-C08-T1, TTRDM-C08-T2, TTRDM-C08-T3_
- [ ] 5. TTRDM-C08-T5 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - form "Filter transaction types"
  - button "Edit description": One row action at a time, so the legacy errors 'Please select only 1 action' and 'Action code selected is invalid' cannot occur.
  - button "Save"
  - button "Delete"
  - _Requirements: TTRDM-REQ-F-056, TTRDM-REQ-F-057, TTRDM-REQ-F-058, TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-061, TTRDM-REQ-F-062, TTRDM-REQ-F-063, TTRDM-REQ-F-064_
  - _Rules: TTRDM-BR-065, TTRDM-BR-066, TTRDM-BR-067, TTRDM-BR-068, TTRDM-BR-069, TTRDM-BR-070, TTRDM-BR-071, TTRDM-BR-072, TTRDM-BR-073_
  - _After: TTRDM-C08-T2, TTRDM-C08-T3, TTRDM-C08-T4_
- [ ] 6. TTRDM-C08-T6 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-056, TTRDM-REQ-F-057, TTRDM-REQ-F-058, TTRDM-REQ-F-059, TTRDM-REQ-F-060, TTRDM-REQ-F-061, TTRDM-REQ-F-062, TTRDM-REQ-F-063, TTRDM-REQ-F-064_
  - _Criteria: TTRDM-C08-AC-01, TTRDM-C08-AC-02, TTRDM-C08-AC-03, TTRDM-C08-AC-04, TTRDM-C08-AC-05, TTRDM-C08-AC-06, TTRDM-C08-AC-07, TTRDM-C08-AC-08, TTRDM-C08-AC-09, TTRDM-C08-AC-10, TTRDM-C08-AC-11, TTRDM-C08-AC-12_
  - _After: TTRDM-C08-T1, TTRDM-C08-T2, TTRDM-C08-T3, TTRDM-C08-T4, TTRDM-C08-T5_
