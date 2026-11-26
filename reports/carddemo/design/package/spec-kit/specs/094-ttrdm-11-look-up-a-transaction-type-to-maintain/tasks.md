# Tasks: Look up a transaction type to maintain (TTRDM-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C11-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-080, TTRDM-REQ-F-081, TTRDM-REQ-F-082, TTRDM-REQ-F-083, TTRDM-REQ-F-084, TTRDM-REQ-F-085, TTRDM-REQ-F-086, TTRDM-REQ-F-087, TTRDM-REQ-F-088, TTRDM-REQ-F-089, TTRDM-REQ-F-090.
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
- [ ] TTRDM-C11-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-080, TTRDM-REQ-F-081, TTRDM-REQ-F-082, TTRDM-REQ-F-084, TTRDM-REQ-F-088, TTRDM-REQ-F-089, TTRDM-REQ-F-090. Rules: TTRDM-BR-089, TTRDM-BR-090, TTRDM-BR-091, TTRDM-BR-094, TTRDM-BR-098, TTRDM-BR-099, TTRDM-BR-100, TTRDM-BR-101, TTRDM-BR-102. After: TTRDM-C11-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: TTRDM-BR-102.
- [ ] TTRDM-C11-T3 [business-rules] Implement error handling and messages. Requirements: TTRDM-REQ-F-083. Rules: TTRDM-BR-092, TTRDM-BR-093. After: TTRDM-C11-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] TTRDM-C11-T4 [api] Build the services behind the screens. Requirements: TTRDM-REQ-F-085, TTRDM-REQ-F-086, TTRDM-REQ-F-087. Rules: TTRDM-BR-095, TTRDM-BR-096, TTRDM-BR-097. After: TTRDM-C11-T1, TTRDM-C11-T2, TTRDM-C11-T3.
  - TTRDM-BR-095: Each lookup starts by clearing the 'original' snapshot and the information message held in the screen's state, so a failed lookup can never leave the previous type's values behind.
  - TTRDM-BR-096: A keyed read of the transaction type table by its two-digit code. On a hit, return a 'found' result with code and description; the description is used both for display and as the baseline for change detection.
  - TTRDM-BR-097: Hold the fetched code and description, at their stored length, as an 'original' snapshot in the edit session (or as a version/ETag) to compare against the user's later edits. On not-found or a read error, leave the snapshot empty.
  - TTRDM-BR-100: In the not-found state, if the same code is submitted again without choosing Add, keep the code and description already held in the edit session and ignore the submitted form values, including any description typed.
- [ ] TTRDM-C11-T5 [ui-modernization] Build the screen Add or change a transaction type (S-TRANTYPE-EDIT). Requirements: TTRDM-REQ-F-080, TTRDM-REQ-F-081, TTRDM-REQ-F-082, TTRDM-REQ-F-088. Rules: TTRDM-BR-089, TTRDM-BR-090, TTRDM-BR-091, TTRDM-BR-098. After: TTRDM-C11-T2, TTRDM-C11-T3, TTRDM-C11-T4.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - **lookup field** "Transaction type code": 'Tran Type code must be supplied. Enter a two-digit code.'; 'Tran Type code must be numeric. Enter digits only.'; 'Tran Type code must not be zero. Enter a code from 01 to 99.' Only the first failing check is shown.
- [ ] TTRDM-C11-T6 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-080, TTRDM-REQ-F-081, TTRDM-REQ-F-082, TTRDM-REQ-F-083, TTRDM-REQ-F-084, TTRDM-REQ-F-085, TTRDM-REQ-F-086, TTRDM-REQ-F-087, TTRDM-REQ-F-088, TTRDM-REQ-F-089, TTRDM-REQ-F-090. Criteria: TTRDM-C11-AC-01, TTRDM-C11-AC-02, TTRDM-C11-AC-03, TTRDM-C11-AC-04, TTRDM-C11-AC-05, TTRDM-C11-AC-06, TTRDM-C11-AC-07, TTRDM-C11-AC-08, TTRDM-C11-AC-09, TTRDM-C11-AC-10, TTRDM-C11-AC-11. After: TTRDM-C11-T1, TTRDM-C11-T2, TTRDM-C11-T3, TTRDM-C11-T4, TTRDM-C11-T5.
  - 11 acceptance criteria, each a test named by its ID.
