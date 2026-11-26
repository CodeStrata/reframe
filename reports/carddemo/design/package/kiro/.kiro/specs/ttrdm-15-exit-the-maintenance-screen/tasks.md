# Implementation plan: Exit the maintenance screen (TTRDM-C15)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C15-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-106, TTRDM-REQ-F-107_
- [ ] 2. TTRDM-C15-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-107_
  - _Rules: TTRDM-BR-120_
  - _After: TTRDM-C15-T1_
- [ ] 3. TTRDM-C15-T3 [api] Build the services behind the screens
  - TTRDM-BR-119: On exit, the new application must commit or close any open database transaction for the session before navigating. It then redirects to the return route stored in the session, falling back to the Admin menu route when none is stored. No unit of work may be left open across the navigation.
  - _Requirements: TTRDM-REQ-F-106_
  - _Rules: TTRDM-BR-119_
  - _After: TTRDM-C15-T1, TTRDM-C15-T2_
- [ ] 4. TTRDM-C15-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL)
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Transaction types"
  - _Requirements: TTRDM-REQ-F-106_
  - _Rules: TTRDM-BR-119_
  - _After: TTRDM-C15-T2, TTRDM-C15-T3_
- [ ] 5. TTRDM-C15-T5 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-106, TTRDM-REQ-F-107_
  - _Criteria: TTRDM-C15-AC-01, TTRDM-C15-AC-02, TTRDM-C15-AC-03_
  - _After: TTRDM-C15-T1, TTRDM-C15-T2, TTRDM-C15-T3, TTRDM-C15-T4_
