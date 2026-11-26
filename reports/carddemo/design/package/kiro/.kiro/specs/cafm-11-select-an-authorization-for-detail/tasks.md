# Implementation plan: Select an authorization for detail (CAFM-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C11-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y, CVACT02Y.
  - _Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111_
- [ ] 2. CAFM-C11-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111_
  - _Rules: CAFM-BR-115, CAFM-BR-116, CAFM-BR-117_
  - _After: CAFM-C11-T1_
- [ ] 3. CAFM-C11-T3 [ui-modernization] Build the screen Pending authorizations (S-PENDING-AUTHS)
  - To the prototype: ui-reference/index.html#/S-PENDING-AUTHS.
  - table "Pending authorizations": Only a row's 'View details' action opens an authorization, so 'Invalid selection. Valid value is S' cannot arise; it is shown if a row without an authorization is opened. Previous is disabled on the first page and announces 'You are already at the top of the page...'; Next is disabled on the last page and announces 'You are already at the bottom of the page...'.
  - _Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111_
  - _Rules: CAFM-BR-115, CAFM-BR-116, CAFM-BR-117_
  - _After: CAFM-C11-T2_
- [ ] 4. CAFM-C11-T4 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111_
  - _Criteria: CAFM-C11-AC-01, CAFM-C11-AC-02, CAFM-C11-AC-03, CAFM-C11-AC-04_
  - _After: CAFM-C11-T1, CAFM-C11-T2, CAFM-C11-T3_
- [ ] 5. CAFM-C11-T5 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111_
  - _After: CAFM-C11-T1, CAFM-C11-T2, CAFM-C11-T3_
