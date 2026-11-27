# Tasks: Control maintenance screen keys and flow (TTRDM-C20)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C20-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142, TTRDM-REQ-F-143, TTRDM-REQ-F-144.
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
- [ ] TTRDM-C20-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142, TTRDM-REQ-F-143. Rules: TTRDM-BR-152, TTRDM-BR-153, TTRDM-BR-154, TTRDM-BR-155. After: TTRDM-C20-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C20-T3 [business-rules] Implement error handling and messages. Requirements: TTRDM-REQ-F-144. Rules: TTRDM-BR-156. After: TTRDM-C20-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] TTRDM-C20-T4 [ui-modernization] Build the screen Add or change a transaction type (S-TRANTYPE-EDIT). Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142. Rules: TTRDM-BR-152, TTRDM-BR-153, TTRDM-BR-154. After: TTRDM-C20-T2, TTRDM-C20-T3.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - **primary button** "Save transaction type": Code and description match what is stored (ignoring case and surrounding spaces): 'No change detected with respect to values fetched.'
- [ ] TTRDM-C20-T5 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-140, TTRDM-REQ-F-141, TTRDM-REQ-F-142, TTRDM-REQ-F-143, TTRDM-REQ-F-144. Criteria: TTRDM-C20-AC-01, TTRDM-C20-AC-02, TTRDM-C20-AC-03, TTRDM-C20-AC-04, TTRDM-C20-AC-05, TTRDM-C20-AC-06, TTRDM-C20-AC-07. After: TTRDM-C20-T1, TTRDM-C20-T2, TTRDM-C20-T3, TTRDM-C20-T4.
  - 7 acceptance criteria, each a test named by its ID.
