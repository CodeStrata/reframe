# Tasks: Detect unchanged card details on update (CCLDV-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CCLDV-C06-T1 [data] Model the data the capability reads and writes. Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060.
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
- [ ] CCLDV-C06-T2 [business-rules] Implement the business rules. Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060. Rules: CCLDV-BR-060. After: CCLDV-C06-T1.
  - Keep each business rule exactly as specified.
- [ ] CCLDV-C06-T3 [ui-modernization] Build the screen Card (S-CARD-DETAIL). Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060. Rules: CCLDV-BR-060. After: CCLDV-C06-T2.
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - form "Edit card": Something must change (ignoring upper/lower case): 'No changes to save. The details match the stored values.' (legacy 'No change detected with respect to values fetched.') Errors are reported in the order name, status, expiry month, expiry year.
- [ ] CCLDV-C06-T4 [test-generation] Write a test for every acceptance criterion. Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060. Criteria: CCLDV-C06-AC-01, CCLDV-C06-AC-02, CCLDV-C06-AC-03. After: CCLDV-C06-T1, CCLDV-C06-T2, CCLDV-C06-T3.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] CCLDV-C06-T5 [compliance] Review the handling of card data, personal data. Requirements: CCLDV-REQ-F-059, CCLDV-REQ-F-060. After: CCLDV-C06-T1, CCLDV-C06-T2, CCLDV-C06-T3.
  - Check storage, logs, screens and audit against the rules.
