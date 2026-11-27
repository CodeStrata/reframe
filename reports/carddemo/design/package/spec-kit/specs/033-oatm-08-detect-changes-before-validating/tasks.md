# Tasks: Detect changes before validating (OATM-C08)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C08-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071, OATM-REQ-F-072.
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
- [ ] OATM-C08-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-072. Rules: OATM-BR-067, OATM-BR-068, OATM-BR-069, OATM-BR-070, OATM-BR-071, OATM-BR-073. After: OATM-C08-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C08-T3 [api] Build the services behind the screens. Requirements: OATM-REQ-F-071. Rules: OATM-BR-072. After: OATM-C08-T1, OATM-C08-T2.
  - OATM-BR-072: Before validating, decide from the update stage and the change-detection result: if nothing changed, or the update is awaiting confirmation or already completed, clear all field-error flags and skip every field and date check. Validation is a step the server runs only when a change is detected while editing.
- [ ] OATM-C08-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT). Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071, OATM-REQ-F-072. Rules: OATM-BR-067, OATM-BR-068, OATM-BR-069, OATM-BR-070, OATM-BR-071, OATM-BR-072, OATM-BR-073. After: OATM-C08-T2, OATM-C08-T3.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Status and group": Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values.
  - **summary card** "Phone and payments": A phone may be left wholly blank; otherwise '<Phone Number 1 or 2>: Area code must be supplied.', ': Area code must be A 3 digit number.', ': Area code cannot be zero', ': Not valid North America general purpose area code' (from the list of general-purpose codes), ': Prefix code must be supplied.', ': Prefix code must be A 3 digit number.', ': Prefix code cannot be zero', ': Line number code must be supplied.', ': Line number code must be A 4 digit number.', ': Line number code cannot be zero'. EFT account ID: 'EFT Account Id must be supplied.', all numeric, 10 digits, not zero. Primary card holder: 'Primary Card Holder must be supplied.' and must be Yes or No ('must be Y or N.').
  - **summary card** "Fix these before saving"
  - **primary button** "Save changes": If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved.
- [ ] OATM-C08-T5 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071, OATM-REQ-F-072. Criteria: OATM-C08-AC-01, OATM-C08-AC-02, OATM-C08-AC-03, OATM-C08-AC-04, OATM-C08-AC-05, OATM-C08-AC-06, OATM-C08-AC-07, OATM-C08-AC-08. After: OATM-C08-T1, OATM-C08-T2, OATM-C08-T3, OATM-C08-T4.
  - 8 acceptance criteria, each a test named by its ID.
- [ ] OATM-C08-T6 [compliance] Review the handling of personal data. Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071, OATM-REQ-F-072. After: OATM-C08-T1, OATM-C08-T2, OATM-C08-T3, OATM-C08-T4.
  - Check storage, logs, screens and audit against the rules.
