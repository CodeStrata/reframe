# Tasks: Save card changes (CCLDV-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CCLDV-C11-T1 [data] Model the data the capability reads and writes. Requirements: CCLDV-REQ-F-104, CCLDV-REQ-F-105.
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
- [ ] CCLDV-C11-T2 [business-rules] Implement the business rules. Requirements: CCLDV-REQ-F-104. Rules: CCLDV-BR-121. After: CCLDV-C11-T1.
  - Keep each business rule exactly as specified.
- [ ] CCLDV-C11-T3 [business-rules] Implement error handling and messages. Requirements: CCLDV-REQ-F-105. Rules: CCLDV-BR-122. After: CCLDV-C11-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CCLDV-C11-T4 [ui-modernization] Build the screen Card details (S-CARD-DETAIL). Requirements: CCLDV-REQ-F-104. Rules: CCLDV-BR-121. After: CCLDV-C11-T2, CCLDV-C11-T3.
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - **primary button** "Save card": Nothing differs from the stored values (ignoring case): 'No change detected with respect to values fetched.' Fields are checked in the order name, status, expiry month, expiry year.
- [ ] CCLDV-C11-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CCLDV-REQ-F-104, CCLDV-REQ-F-105. Criteria: CCLDV-C11-AC-01, CCLDV-C11-AC-02. After: CCLDV-C11-T1, CCLDV-C11-T2, CCLDV-C11-T3, CCLDV-C11-T4.
  - 2 acceptance criteria, each a test named by its ID.
- [ ] CCLDV-C11-T6 [compliance] Review the handling of card data, personal data. Requirements: CCLDV-REQ-F-104, CCLDV-REQ-F-105. After: CCLDV-C11-T1, CCLDV-C11-T2, CCLDV-C11-T3, CCLDV-C11-T4.
  - Check storage, logs, screens and audit against the rules.
