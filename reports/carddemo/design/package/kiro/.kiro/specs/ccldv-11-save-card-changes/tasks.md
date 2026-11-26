# Implementation plan: Save card changes (CCLDV-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CCLDV-C11-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-104, CCLDV-REQ-F-105_
- [ ] 2. CCLDV-C11-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-104_
  - _Rules: CCLDV-BR-121_
  - _After: CCLDV-C11-T1_
- [ ] 3. CCLDV-C11-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-105_
  - _Rules: CCLDV-BR-122_
  - _After: CCLDV-C11-T1_
- [ ] 4. CCLDV-C11-T4 [ui-modernization] Build the screen Card details (S-CARD-DETAIL)
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - **primary button** "Save card": Nothing differs from the stored values (ignoring case): 'No change detected with respect to values fetched.' Fields are checked in the order name, status, expiry month, expiry year.
  - _Requirements: CCLDV-REQ-F-104_
  - _Rules: CCLDV-BR-121_
  - _After: CCLDV-C11-T2, CCLDV-C11-T3_
- [ ] 5. CCLDV-C11-T5 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-104, CCLDV-REQ-F-105_
  - _Criteria: CCLDV-C11-AC-01, CCLDV-C11-AC-02_
  - _After: CCLDV-C11-T1, CCLDV-C11-T2, CCLDV-C11-T3, CCLDV-C11-T4_
- [ ] 6. CCLDV-C11-T6 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-104, CCLDV-REQ-F-105_
  - _After: CCLDV-C11-T1, CCLDV-C11-T2, CCLDV-C11-T3, CCLDV-C11-T4_
