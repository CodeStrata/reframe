# Implementation plan: Control maintenance screen keys and flow (TTRDM-C20)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C20-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142, TTRDM-REQ-F-143, TTRDM-REQ-F-144_
- [ ] 2. TTRDM-C20-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142, TTRDM-REQ-F-143_
  - _Rules: TTRDM-BR-152, TTRDM-BR-153, TTRDM-BR-154, TTRDM-BR-155_
  - _After: TTRDM-C20-T1_
- [ ] 3. TTRDM-C20-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-144_
  - _Rules: TTRDM-BR-156_
  - _After: TTRDM-C20-T1_
- [ ] 4. TTRDM-C20-T4 [ui-modernization] Build the screen Transaction type (S-TRANTYPE-EDIT)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - button "Find"
  - button "Add as new type"
  - button "Save": Actions not available in the current step are disabled rather than rejected (legacy 'Invalid key pressed').
  - button "Delete"
  - button "Cancel"
  - message "Result"
  - _Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142, TTRDM-REQ-F-143, TTRDM-REQ-F-144_
  - _Rules: TTRDM-BR-152, TTRDM-BR-153, TTRDM-BR-154, TTRDM-BR-155, TTRDM-BR-156_
  - _After: TTRDM-C20-T2, TTRDM-C20-T3_
- [ ] 5. TTRDM-C20-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142, TTRDM-REQ-F-143, TTRDM-REQ-F-144_
  - _Criteria: TTRDM-C20-AC-01, TTRDM-C20-AC-02, TTRDM-C20-AC-03, TTRDM-C20-AC-04, TTRDM-C20-AC-05, TTRDM-C20-AC-06, TTRDM-C20-AC-07_
  - _After: TTRDM-C20-T1, TTRDM-C20-T2, TTRDM-C20-T3, TTRDM-C20-T4_
