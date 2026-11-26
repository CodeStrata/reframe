# Implementation plan: Navigate from the transaction type list (TTRDM-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C10-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-078, TTRDM-REQ-F-079_
- [ ] 2. TTRDM-C10-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-078, TTRDM-REQ-F-079_
  - _Rules: TTRDM-BR-087, TTRDM-BR-088_
  - _After: TTRDM-C10-T1_
- [ ] 3. TTRDM-C10-T3 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **primary button** "Add transaction type"
  - _Requirements: TTRDM-REQ-F-079_
  - _Rules: TTRDM-BR-088_
  - _After: TTRDM-C10-T2_
- [ ] 4. TTRDM-C10-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Transaction types"
  - _Requirements: TTRDM-REQ-F-078_
  - _Rules: TTRDM-BR-087_
  - _After: TTRDM-C10-T2_
- [ ] 5. TTRDM-C10-T5 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-078, TTRDM-REQ-F-079_
  - _Criteria: TTRDM-C10-AC-01, TTRDM-C10-AC-02_
  - _After: TTRDM-C10-T1, TTRDM-C10-T2, TTRDM-C10-T3, TTRDM-C10-T4_
