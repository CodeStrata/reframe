# Tasks: Select an authorization for detail (CAFM-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C11-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111.
  - File records: CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y, CVACT02Y.
- [ ] CAFM-C11-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111. Rules: CAFM-BR-115, CAFM-BR-116, CAFM-BR-117. After: CAFM-C11-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C11-T3 [ui-modernization] Build the screen Pending authorizations (S-PENDING-AUTHS). Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111. Rules: CAFM-BR-115, CAFM-BR-116, CAFM-BR-117. After: CAFM-C11-T2.
  - To the prototype: ui-reference/index.html#/S-PENDING-AUTHS.
  - table "Pending authorizations": Only a row's 'View details' action opens an authorization, so 'Invalid selection. Valid value is S' cannot arise; it is shown if a row without an authorization is opened. Previous is disabled on the first page and announces 'You are already at the top of the page...'; Next is disabled on the last page and announces 'You are already at the bottom of the page...'.
- [ ] CAFM-C11-T4 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111. Criteria: CAFM-C11-AC-01, CAFM-C11-AC-02, CAFM-C11-AC-03, CAFM-C11-AC-04. After: CAFM-C11-T1, CAFM-C11-T2, CAFM-C11-T3.
  - 4 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C11-T5 [compliance] Review the handling of card data. Requirements: CAFM-REQ-F-109, CAFM-REQ-F-110, CAFM-REQ-F-111. After: CAFM-C11-T1, CAFM-C11-T2, CAFM-C11-T3.
  - Check storage, logs, screens and audit against the rules.
