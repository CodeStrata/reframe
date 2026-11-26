# Implementation plan: Confirm and save the account update (OATM-C06)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C06-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061_
- [ ] 2. OATM-C06-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-059_
  - _Rules: OATM-BR-058_
  - _After: OATM-C06-T1_
- [ ] 3. OATM-C06-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-060_
  - _Rules: OATM-BR-059_
  - _After: OATM-C06-T1_
- [ ] 4. OATM-C06-T4 [api] Build the services behind the screens
  - OATM-BR-060: The legacy save writes the account from a layout without a ZIP field, so the entered group lands in the stored ZIP position (offsets 103-112) and the group field gets unset filler. The new account store should have distinct group and ZIP columns; whether to reproduce this shift for data compatibility (e.g. while the legacy file is still read by other jobs) or correct it is a decision to record, and any migration must account for existing records with the group in the ZIP position.
  - _Requirements: OATM-REQ-F-061_
  - _Rules: OATM-BR-060_
  - _After: OATM-C06-T1, OATM-C06-T2, OATM-C06-T3_
- [ ] 5. OATM-C06-T5 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - dialog "Save these changes?"
  - button "Save changes": If the stored record changed since it was fetched: 'Record changed by some one else. Please review' and nothing is saved.
  - _Requirements: OATM-REQ-F-059, OATM-REQ-F-060_
  - _Rules: OATM-BR-058, OATM-BR-059_
  - _After: OATM-C06-T2, OATM-C06-T3, OATM-C06-T4_
- [ ] 6. OATM-C06-T6 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061_
  - _Criteria: OATM-C06-AC-01, OATM-C06-AC-02, OATM-C06-AC-03, OATM-C06-AC-04, OATM-C06-AC-05, OATM-C06-AC-06, OATM-C06-AC-07_
  - _After: OATM-C06-T1, OATM-C06-T2, OATM-C06-T3, OATM-C06-T4, OATM-C06-T5_
- [ ] 7. OATM-C06-T7 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061_
  - _After: OATM-C06-T1, OATM-C06-T2, OATM-C06-T3, OATM-C06-T4, OATM-C06-T5_
