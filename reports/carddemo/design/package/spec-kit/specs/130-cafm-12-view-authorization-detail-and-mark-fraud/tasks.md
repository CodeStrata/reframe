# Tasks: View authorization detail and mark fraud (CAFM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C12-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114.
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y.
- [ ] CAFM-C12-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-114. Rules: CAFM-BR-120. After: CAFM-C12-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C12-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113. Rules: CAFM-BR-118, CAFM-BR-119. After: CAFM-C12-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C12-T4 [ui-modernization] Build the screen Authorization details (S-AUTH-DETAIL). Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114. Rules: CAFM-BR-118, CAFM-BR-119, CAFM-BR-120. After: CAFM-C12-T2, CAFM-C12-T3.
  - To the prototype: ui-reference/index.html#/S-AUTH-DETAIL.
  - display "Response"
  - display "Reason"
  - button "Mark as fraud / Remove fraud mark"
- [ ] CAFM-C12-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114. Criteria: CAFM-C12-AC-01, CAFM-C12-AC-02, CAFM-C12-AC-03, CAFM-C12-AC-04, CAFM-C12-AC-05, CAFM-C12-AC-06. After: CAFM-C12-T1, CAFM-C12-T2, CAFM-C12-T3, CAFM-C12-T4.
  - 6 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C12-T6 [compliance] Review the handling of card data. Requirements: CAFM-REQ-F-112, CAFM-REQ-F-113, CAFM-REQ-F-114. After: CAFM-C12-T1, CAFM-C12-T2, CAFM-C12-T3, CAFM-C12-T4.
  - Check storage, logs, screens and audit against the rules.
