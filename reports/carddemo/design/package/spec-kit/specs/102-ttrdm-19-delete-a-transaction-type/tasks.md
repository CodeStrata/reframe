# Tasks: Delete a transaction type (TTRDM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C19-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-133, TTRDM-REQ-F-134, TTRDM-REQ-F-135, TTRDM-REQ-F-136, TTRDM-REQ-F-137, TTRDM-REQ-F-138, TTRDM-REQ-F-139.
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
- [ ] TTRDM-C19-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-133, TTRDM-REQ-F-134, TTRDM-REQ-F-135, TTRDM-REQ-F-138. Rules: TTRDM-BR-145, TTRDM-BR-146, TTRDM-BR-147, TTRDM-BR-150. After: TTRDM-C19-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C19-T3 [business-rules] Implement error handling and messages. Requirements: TTRDM-REQ-F-136, TTRDM-REQ-F-137, TTRDM-REQ-F-139. Rules: TTRDM-BR-148, TTRDM-BR-149, TTRDM-BR-151. After: TTRDM-C19-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] TTRDM-C19-T4 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST). Requirements: TTRDM-REQ-F-134, TTRDM-REQ-F-136. Rules: TTRDM-BR-146, TTRDM-BR-148. After: TTRDM-C19-T2, TTRDM-C19-T3.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **data table** "Transaction types": In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes.
- [ ] TTRDM-C19-T5 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-133, TTRDM-REQ-F-134, TTRDM-REQ-F-135, TTRDM-REQ-F-136, TTRDM-REQ-F-137, TTRDM-REQ-F-138, TTRDM-REQ-F-139. Criteria: TTRDM-C19-AC-01, TTRDM-C19-AC-02, TTRDM-C19-AC-03, TTRDM-C19-AC-04, TTRDM-C19-AC-05, TTRDM-C19-AC-06, TTRDM-C19-AC-07. After: TTRDM-C19-T1, TTRDM-C19-T2, TTRDM-C19-T3, TTRDM-C19-T4.
  - 7 acceptance criteria, each a test named by its ID.
