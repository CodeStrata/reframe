# Tasks: Cancel a pending maintenance change (TTRDM-C14)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C14-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-103, TTRDM-REQ-F-104, TTRDM-REQ-F-105.
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
- [ ] TTRDM-C14-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-103, TTRDM-REQ-F-104, TTRDM-REQ-F-105. Rules: TTRDM-BR-116, TTRDM-BR-117, TTRDM-BR-118. After: TTRDM-C14-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: TTRDM-BR-118.
- [ ] TTRDM-C14-T3 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-103, TTRDM-REQ-F-104, TTRDM-REQ-F-105. Criteria: TTRDM-C14-AC-01, TTRDM-C14-AC-02, TTRDM-C14-AC-03. After: TTRDM-C14-T1, TTRDM-C14-T2.
  - 3 acceptance criteria, each a test named by its ID.
