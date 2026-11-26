# Tasks: Save confirmed account and customer changes (OATM-C13)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C13-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-107, OATM-REQ-F-108, OATM-REQ-F-109, OATM-REQ-F-110, OATM-REQ-F-111, OATM-REQ-N-004, OATM-REQ-F-112, OATM-REQ-F-113.
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
- [ ] OATM-C13-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-109, OATM-REQ-F-111. Rules: OATM-BR-111, OATM-BR-113. After: OATM-C13-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C13-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-107, OATM-REQ-F-108, OATM-REQ-F-110, OATM-REQ-N-004, OATM-REQ-F-113, OATM-REQ-F-112. Rules: OATM-BR-110, OATM-BR-112, OATM-BR-114, OATM-BR-115, OATM-BR-116. After: OATM-C13-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C13-T4 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT). Requirements: OATM-REQ-F-107, OATM-REQ-N-004, OATM-REQ-F-112, OATM-REQ-F-113. Rules: OATM-BR-110, OATM-BR-114, OATM-BR-115, OATM-BR-116. After: OATM-C13-T2, OATM-C13-T3.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - button "Save changes": If the stored record changed since it was fetched: 'Record changed by some one else. Please review' and nothing is saved.
  - message "Save result"
- [ ] OATM-C13-T5 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-107, OATM-REQ-F-108, OATM-REQ-F-109, OATM-REQ-F-110, OATM-REQ-F-111, OATM-REQ-N-004, OATM-REQ-F-112, OATM-REQ-F-113. Criteria: OATM-C13-AC-01, OATM-C13-AC-02, OATM-C13-AC-03, OATM-C13-AC-04, OATM-C13-AC-05, OATM-C13-AC-06, OATM-C13-AC-07, OATM-C13-AC-08. After: OATM-C13-T1, OATM-C13-T2, OATM-C13-T3, OATM-C13-T4.
  - 8 acceptance criteria, each a test named by its ID.
- [ ] OATM-C13-T6 [compliance] Review the handling of money, personal data. Requirements: OATM-REQ-F-107, OATM-REQ-F-108, OATM-REQ-F-109, OATM-REQ-F-110, OATM-REQ-F-111, OATM-REQ-N-004, OATM-REQ-F-112, OATM-REQ-F-113. After: OATM-C13-T1, OATM-C13-T2, OATM-C13-T3, OATM-C13-T4.
  - Check storage, logs, screens and audit against the rules.
