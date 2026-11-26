# Implementation plan: Access to transaction type maintenance (TTRDM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C06-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003_
- [ ] 2. TTRDM-C06-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003_
  - _Rules: TTRDM-BR-059, TTRDM-BR-060_
  - _After: TTRDM-C06-T1_
- [ ] 3. TTRDM-C06-T3 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - link "Transaction types"
  - _Requirements: TTRDM-REQ-N-003_
  - _Rules: TTRDM-BR-060_
  - _After: TTRDM-C06-T2_
- [ ] 4. TTRDM-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003_
  - _Criteria: TTRDM-C06-AC-01, TTRDM-C06-AC-02_
  - _After: TTRDM-C06-T1, TTRDM-C06-T2, TTRDM-C06-T3_
- [ ] 5. TTRDM-C06-T5 [compliance] Review the handling of security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003_
  - _After: TTRDM-C06-T1, TTRDM-C06-T2, TTRDM-C06-T3_
