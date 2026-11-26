# Implementation plan: Add a new transaction type (TTRDM-C18)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C18-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131, TTRDM-REQ-F-132_
- [ ] 2. TTRDM-C18-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131_
  - _Rules: TTRDM-BR-143, TTRDM-BR-144_
  - _After: TTRDM-C18-T1_
- [ ] 3. TTRDM-C18-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-132_
  - _Rules: TTRDM-BR-140_
  - _After: TTRDM-C18-T1_
- [ ] 4. TTRDM-C18-T4 [ui-modernization] Build the screen Transaction type (S-TRANTYPE-EDIT)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - button "Add as new type"
  - dialog "Save this transaction type?"
  - message "Result"
  - _Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131, TTRDM-REQ-F-132_
  - _Rules: TTRDM-BR-140, TTRDM-BR-143, TTRDM-BR-144_
  - _After: TTRDM-C18-T2, TTRDM-C18-T3_
- [ ] 5. TTRDM-C18-T5 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131, TTRDM-REQ-F-132_
  - _Criteria: TTRDM-C18-AC-01, TTRDM-C18-AC-02, TTRDM-C18-AC-03_
  - _After: TTRDM-C18-T1, TTRDM-C18-T2, TTRDM-C18-T3, TTRDM-C18-T4_
