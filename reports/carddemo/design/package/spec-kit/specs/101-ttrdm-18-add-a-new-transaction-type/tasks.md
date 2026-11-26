# Tasks: Add a new transaction type (TTRDM-C18)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C18-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131, TTRDM-REQ-F-132.
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
- [ ] TTRDM-C18-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131. Rules: TTRDM-BR-143, TTRDM-BR-144. After: TTRDM-C18-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C18-T3 [business-rules] Implement error handling and messages. Requirements: TTRDM-REQ-F-132. Rules: TTRDM-BR-140. After: TTRDM-C18-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] TTRDM-C18-T4 [ui-modernization] Build the screen Transaction type (S-TRANTYPE-EDIT). Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131, TTRDM-REQ-F-132. Rules: TTRDM-BR-140, TTRDM-BR-143, TTRDM-BR-144. After: TTRDM-C18-T2, TTRDM-C18-T3.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - button "Add as new type"
  - dialog "Save this transaction type?"
  - message "Result"
- [ ] TTRDM-C18-T5 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-130, TTRDM-REQ-F-131, TTRDM-REQ-F-132. Criteria: TTRDM-C18-AC-01, TTRDM-C18-AC-02, TTRDM-C18-AC-03. After: TTRDM-C18-T1, TTRDM-C18-T2, TTRDM-C18-T3, TTRDM-C18-T4.
  - 3 acceptance criteria, each a test named by its ID.
