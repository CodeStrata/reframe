# Implementation plan: Delete a transaction type (TTRDM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C19-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-133, TTRDM-REQ-F-134, TTRDM-REQ-F-135, TTRDM-REQ-F-136, TTRDM-REQ-F-137, TTRDM-REQ-F-138, TTRDM-REQ-F-139_
- [ ] 2. TTRDM-C19-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-133, TTRDM-REQ-F-134, TTRDM-REQ-F-135, TTRDM-REQ-F-138_
  - _Rules: TTRDM-BR-145, TTRDM-BR-146, TTRDM-BR-147, TTRDM-BR-150_
  - _After: TTRDM-C19-T1_
- [ ] 3. TTRDM-C19-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-136, TTRDM-REQ-F-137, TTRDM-REQ-F-139_
  - _Rules: TTRDM-BR-148, TTRDM-BR-149, TTRDM-BR-151_
  - _After: TTRDM-C19-T1_
- [ ] 4. TTRDM-C19-T4 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **data table** "Transaction types": In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes.
  - _Requirements: TTRDM-REQ-F-134, TTRDM-REQ-F-136_
  - _Rules: TTRDM-BR-146, TTRDM-BR-148_
  - _After: TTRDM-C19-T2, TTRDM-C19-T3_
- [ ] 5. TTRDM-C19-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-133, TTRDM-REQ-F-134, TTRDM-REQ-F-135, TTRDM-REQ-F-136, TTRDM-REQ-F-137, TTRDM-REQ-F-138, TTRDM-REQ-F-139_
  - _Criteria: TTRDM-C19-AC-01, TTRDM-C19-AC-02, TTRDM-C19-AC-03, TTRDM-C19-AC-04, TTRDM-C19-AC-05, TTRDM-C19-AC-06, TTRDM-C19-AC-07_
  - _After: TTRDM-C19-T1, TTRDM-C19-T2, TTRDM-C19-T3, TTRDM-C19-T4_
