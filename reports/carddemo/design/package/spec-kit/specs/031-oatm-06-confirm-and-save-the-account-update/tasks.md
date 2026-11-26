# Tasks: Confirm and save the account update (OATM-C06)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C06-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061.
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
- [ ] OATM-C06-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-059. Rules: OATM-BR-058. After: OATM-C06-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C06-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-060. Rules: OATM-BR-059. After: OATM-C06-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C06-T4 [api] Build the services behind the screens. Requirements: OATM-REQ-F-061. Rules: OATM-BR-060. After: OATM-C06-T1, OATM-C06-T2, OATM-C06-T3.
  - OATM-BR-060: This is a layout defect in the legacy program: it writes the account through a layout that has no ZIP field, so the account group lands in the ZIP position and the group field gets filler. The new account record must keep ZIP and account group as separate named fields and save each confirmed value to its own field. The acceptance criterion above only records the legacy result for reconciliation. The business owner must decide whether to keep it before anyone treats it as required. Data migration should expect ZIP values on rewritten accounts that are really group IDs.
- [ ] OATM-C06-T5 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT). Requirements: OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061. Rules: OATM-BR-058, OATM-BR-059, OATM-BR-060. After: OATM-C06-T2, OATM-C06-T3, OATM-C06-T4.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **primary button** "Save changes": If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved.
- [ ] OATM-C06-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061. Criteria: OATM-C06-AC-01, OATM-C06-AC-02, OATM-C06-AC-03, OATM-C06-AC-04, OATM-C06-AC-05, OATM-C06-AC-06, OATM-C06-AC-07. After: OATM-C06-T1, OATM-C06-T2, OATM-C06-T3, OATM-C06-T4, OATM-C06-T5.
  - 7 acceptance criteria, each a test named by its ID.
- [ ] OATM-C06-T7 [compliance] Review the handling of money, personal data. Requirements: OATM-REQ-F-059, OATM-REQ-F-060, OATM-REQ-F-061. After: OATM-C06-T1, OATM-C06-T2, OATM-C06-T3, OATM-C06-T4, OATM-C06-T5.
  - Check storage, logs, screens and audit against the rules.
