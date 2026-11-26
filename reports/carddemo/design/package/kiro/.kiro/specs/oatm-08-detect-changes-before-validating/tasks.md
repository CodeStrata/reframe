# Implementation plan: Detect changes before validating (OATM-C08)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C08-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071, OATM-REQ-F-072_
- [ ] 2. OATM-C08-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-072_
  - _Rules: OATM-BR-067, OATM-BR-068, OATM-BR-069, OATM-BR-070, OATM-BR-071, OATM-BR-073_
  - _After: OATM-C08-T1_
- [ ] 3. OATM-C08-T3 [api] Build the services behind the screens
  - OATM-BR-072: Validation is a step gated by update state: when no change is detected or the update is awaiting confirmation or completed, reset all per-field error flags and skip the validators entirely, including date checks.
  - _Requirements: OATM-REQ-F-071_
  - _Rules: OATM-BR-072_
  - _After: OATM-C08-T1, OATM-C08-T2_
- [ ] 4. OATM-C08-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - message "Fix these fields"
  - form "Account and customer details": If nothing differs from the fetched values (ignoring case): 'No change detected with respect to values fetched.' and nothing is checked or saved.
  - _Requirements: OATM-REQ-F-072_
  - _Rules: OATM-BR-070, OATM-BR-071, OATM-BR-073_
  - _After: OATM-C08-T2, OATM-C08-T3_
- [ ] 5. OATM-C08-T5 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071, OATM-REQ-F-072_
  - _Criteria: OATM-C08-AC-01, OATM-C08-AC-02, OATM-C08-AC-03, OATM-C08-AC-04, OATM-C08-AC-05, OATM-C08-AC-06, OATM-C08-AC-07, OATM-C08-AC-08_
  - _After: OATM-C08-T1, OATM-C08-T2, OATM-C08-T3, OATM-C08-T4_
- [ ] 6. OATM-C08-T6 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071, OATM-REQ-F-072_
  - _After: OATM-C08-T1, OATM-C08-T2, OATM-C08-T3, OATM-C08-T4_
