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
- [ ] 4. CAFM-C12-T4 [ui-modernization] Build the screen Account authorizations (S-ACCOUNT-AUTHORIZATIONS)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-AUTHORIZATIONS.
  - **status badge** "Response"
  - **summary card** "Authorization": Not read: 'System error while reading Auth Summary: Code <code>' or 'System error while reading Auth Details: Code <code>' - reopen the authorization, and report the code if it repeats. The detail fields stay blank when the account ID is not numeric, no authorization is selected, or a read failed.
  - **primary button** "Report fraud / Remove fraud mark": Fraud register update failed: the fraud program's message (for example 'SYSTEM ERROR DB2: CODE <code>') and 'Nothing was changed - try again, and report the code if it repeats.' Authorization save failed: 'System error while FRAUD Tagging, ROLLBACK <code>' and 'Nothing was changed - try again.' Fraud service did not respond: 'The fraud update did not complete. Nothing was changed - try again.'
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
