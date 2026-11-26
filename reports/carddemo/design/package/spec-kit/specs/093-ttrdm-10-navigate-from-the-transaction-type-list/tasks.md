# Tasks: Navigate from the transaction type list (TTRDM-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C10-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-078, TTRDM-REQ-F-079.
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
- [ ] TTRDM-C10-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-078, TTRDM-REQ-F-079. Rules: TTRDM-BR-087, TTRDM-BR-088. After: TTRDM-C10-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C10-T3 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST). Requirements: TTRDM-REQ-F-079. Rules: TTRDM-BR-088. After: TTRDM-C10-T2.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **primary button** "Add transaction type"
- [ ] TTRDM-C10-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: TTRDM-REQ-F-078. Rules: TTRDM-BR-087. After: TTRDM-C10-T2.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Transaction types"
- [ ] TTRDM-C10-T5 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-078, TTRDM-REQ-F-079. Criteria: TTRDM-C10-AC-01, TTRDM-C10-AC-02. After: TTRDM-C10-T1, TTRDM-C10-T2, TTRDM-C10-T3, TTRDM-C10-T4.
  - 2 acceptance criteria, each a test named by its ID.
