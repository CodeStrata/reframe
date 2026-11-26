# Implementation plan: View authorization detail and mark fraud (CAFM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C12-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y.
  - _Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114_
- [ ] 2. CAFM-C12-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-114_
  - _Rules: CAFM-BR-120_
  - _After: CAFM-C12-T1_
- [ ] 3. CAFM-C12-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113_
  - _Rules: CAFM-BR-118, CAFM-BR-119_
  - _After: CAFM-C12-T1_
- [ ] 4. CAFM-C12-T4 [ui-modernization] Build the screen Authorization details (S-AUTH-DETAIL)
  - To the prototype: ui-reference/index.html#/S-AUTH-DETAIL.
  - display "Response"
  - display "Reason"
  - button "Mark as fraud / Remove fraud mark"
  - _Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114_
  - _Rules: CAFM-BR-118, CAFM-BR-119, CAFM-BR-120_
  - _After: CAFM-C12-T2, CAFM-C12-T3_
- [ ] 5. CAFM-C12-T5 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114_
  - _Criteria: CAFM-C12-AC-01, CAFM-C12-AC-02, CAFM-C12-AC-03, CAFM-C12-AC-04, CAFM-C12-AC-05, CAFM-C12-AC-06_
  - _After: CAFM-C12-T1, CAFM-C12-T2, CAFM-C12-T3, CAFM-C12-T4_
- [ ] 6. CAFM-C12-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114_
  - _After: CAFM-C12-T1, CAFM-C12-T2, CAFM-C12-T3, CAFM-C12-T4_
