# Tasks: Access to transaction type maintenance (TTRDM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C06-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003.
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
- [ ] TTRDM-C06-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003. Rules: TTRDM-BR-059, TTRDM-BR-060. After: TTRDM-C06-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C06-T3 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003. Rules: TTRDM-BR-059, TTRDM-BR-060. After: TTRDM-C06-T2.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Transaction types"
- [ ] TTRDM-C06-T4 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003. Criteria: TTRDM-C06-AC-01, TTRDM-C06-AC-02. After: TTRDM-C06-T1, TTRDM-C06-T2, TTRDM-C06-T3.
  - 2 acceptance criteria, each a test named by its ID.
- [ ] TTRDM-C06-T5 [compliance] Review the handling of security. Requirements: TTRDM-REQ-N-002, TTRDM-REQ-N-003. After: TTRDM-C06-T1, TTRDM-C06-T2, TTRDM-C06-T3.
  - Check storage, logs, screens and audit against the rules.
