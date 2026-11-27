# Tasks: Validate customer phone numbers (OATM-C10)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C10-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-082, OATM-REQ-F-083, OATM-REQ-F-084, OATM-REQ-F-085, OATM-REQ-F-086, OATM-REQ-F-087, OATM-REQ-F-088, OATM-REQ-F-089, OATM-REQ-F-090, OATM-REQ-F-091, OATM-REQ-F-092, OATM-REQ-F-093, OATM-REQ-F-094.
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
- [ ] OATM-C10-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-083, OATM-REQ-F-084, OATM-REQ-F-085, OATM-REQ-F-086, OATM-REQ-F-087, OATM-REQ-F-088, OATM-REQ-F-089, OATM-REQ-F-090, OATM-REQ-F-091, OATM-REQ-F-092, OATM-REQ-F-093. Rules: OATM-BR-086, OATM-BR-087, OATM-BR-088, OATM-BR-089, OATM-BR-090, OATM-BR-091, OATM-BR-092, OATM-BR-093, OATM-BR-094, OATM-BR-095, OATM-BR-096, OATM-BR-097. After: OATM-C10-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C10-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-094. Rules: OATM-BR-073. After: OATM-C10-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C10-T4 [api] Build the services behind the screens. Requirements: OATM-REQ-F-082. Rules: OATM-BR-085. After: OATM-C10-T1, OATM-C10-T2, OATM-C10-T3.
  - OATM-BR-085: Capture phone numbers 1 and 2 as three optional parts each (area code, prefix, line number). Blank or '*' parts are absent before validation, so a phone with all parts absent counts as omitted. Area-code validation needs a reference list of the North American general-purpose area codes.
- [ ] OATM-C10-T5 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT). Requirements: OATM-REQ-F-082, OATM-REQ-F-083, OATM-REQ-F-084, OATM-REQ-F-085, OATM-REQ-F-086, OATM-REQ-F-087, OATM-REQ-F-088, OATM-REQ-F-089, OATM-REQ-F-090, OATM-REQ-F-091, OATM-REQ-F-092, OATM-REQ-F-093, OATM-REQ-F-094. Rules: OATM-BR-073, OATM-BR-085, OATM-BR-086, OATM-BR-087, OATM-BR-088, OATM-BR-089, OATM-BR-090, OATM-BR-091, OATM-BR-092, OATM-BR-093, OATM-BR-094, OATM-BR-095, OATM-BR-096, OATM-BR-097. After: OATM-C10-T2, OATM-C10-T3, OATM-C10-T4.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **summary card** "Phone and payments": A phone may be left wholly blank; otherwise '<Phone Number 1 or 2>: Area code must be supplied.', ': Area code must be A 3 digit number.', ': Area code cannot be zero', ': Not valid North America general purpose area code' (from the list of general-purpose codes), ': Prefix code must be supplied.', ': Prefix code must be A 3 digit number.', ': Prefix code cannot be zero', ': Line number code must be supplied.', ': Line number code must be A 4 digit number.', ': Line number code cannot be zero'. EFT account ID: 'EFT Account Id must be supplied.', all numeric, 10 digits, not zero. Primary card holder: 'Primary Card Holder must be supplied.' and must be Yes or No ('must be Y or N.').
- [ ] OATM-C10-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-082, OATM-REQ-F-083, OATM-REQ-F-084, OATM-REQ-F-085, OATM-REQ-F-086, OATM-REQ-F-087, OATM-REQ-F-088, OATM-REQ-F-089, OATM-REQ-F-090, OATM-REQ-F-091, OATM-REQ-F-092, OATM-REQ-F-093, OATM-REQ-F-094. Criteria: OATM-C10-AC-01, OATM-C10-AC-02, OATM-C10-AC-03, OATM-C10-AC-04, OATM-C10-AC-05, OATM-C10-AC-06, OATM-C10-AC-07, OATM-C10-AC-08, OATM-C10-AC-09, OATM-C10-AC-10, OATM-C10-AC-11, OATM-C10-AC-12, OATM-C10-AC-13. After: OATM-C10-T1, OATM-C10-T2, OATM-C10-T3, OATM-C10-T4, OATM-C10-T5.
  - 13 acceptance criteria, each a test named by its ID.
- [ ] OATM-C10-T7 [compliance] Review the handling of personal data. Requirements: OATM-REQ-F-082, OATM-REQ-F-083, OATM-REQ-F-084, OATM-REQ-F-085, OATM-REQ-F-086, OATM-REQ-F-087, OATM-REQ-F-088, OATM-REQ-F-089, OATM-REQ-F-090, OATM-REQ-F-091, OATM-REQ-F-092, OATM-REQ-F-093, OATM-REQ-F-094. After: OATM-C10-T1, OATM-C10-T2, OATM-C10-T3, OATM-C10-T4, OATM-C10-T5.
  - Check storage, logs, screens and audit against the rules.
