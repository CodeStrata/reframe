# Implementation plan: Detect unchanged card details on update (CCLDV-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CCLDV-C06-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060_
- [ ] 2. CCLDV-C06-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060_
  - _Rules: CCLDV-BR-060_
  - _After: CCLDV-C06-T1_
- [ ] 3. CCLDV-C06-T3 [ui-modernization] Build the screen Card details (S-CARD-DETAIL)
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - **primary button** "Save card": Nothing differs from the stored values (ignoring case): 'No change detected with respect to values fetched.' Fields are checked in the order name, status, expiry month, expiry year.
  - _Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060_
  - _Rules: CCLDV-BR-060_
  - _After: CCLDV-C06-T2_
- [ ] 4. CCLDV-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060_
  - _Criteria: CCLDV-C06-AC-01, CCLDV-C06-AC-02, CCLDV-C06-AC-03_
  - _After: CCLDV-C06-T1, CCLDV-C06-T2, CCLDV-C06-T3_
- [ ] 5. CCLDV-C06-T5 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060_
  - _After: CCLDV-C06-T1, CCLDV-C06-T2, CCLDV-C06-T3_
