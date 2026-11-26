# Tasks: Confirm and apply a list update or delete (TTRDM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C09-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-065, TTRDM-REQ-F-066, TTRDM-REQ-F-067, TTRDM-REQ-F-068, TTRDM-REQ-F-069, TTRDM-REQ-F-070, TTRDM-REQ-F-071, TTRDM-REQ-F-072, TTRDM-REQ-F-073, TTRDM-REQ-F-074, TTRDM-REQ-F-075, TTRDM-REQ-F-076, TTRDM-REQ-F-077.
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
- [ ] TTRDM-C09-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-065, TTRDM-REQ-F-066, TTRDM-REQ-F-067, TTRDM-REQ-F-068, TTRDM-REQ-F-074, TTRDM-REQ-F-075. Rules: TTRDM-BR-074, TTRDM-BR-075, TTRDM-BR-076, TTRDM-BR-077, TTRDM-BR-078, TTRDM-BR-084. After: TTRDM-C09-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C09-T3 [business-rules] Implement error handling and messages. Requirements: TTRDM-REQ-F-071, TTRDM-REQ-F-072, TTRDM-REQ-F-073, TTRDM-REQ-F-076, TTRDM-REQ-F-077, TTRDM-REQ-F-069, TTRDM-REQ-F-070. Rules: TTRDM-BR-079, TTRDM-BR-080, TTRDM-BR-081, TTRDM-BR-082, TTRDM-BR-083, TTRDM-BR-085, TTRDM-BR-086. After: TTRDM-C09-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] TTRDM-C09-T4 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST). Requirements: TTRDM-REQ-F-065, TTRDM-REQ-F-066, TTRDM-REQ-F-067, TTRDM-REQ-F-068, TTRDM-REQ-F-069, TTRDM-REQ-F-070, TTRDM-REQ-F-071, TTRDM-REQ-F-072, TTRDM-REQ-F-073, TTRDM-REQ-F-074, TTRDM-REQ-F-075, TTRDM-REQ-F-076, TTRDM-REQ-F-077. Rules: TTRDM-BR-074, TTRDM-BR-075, TTRDM-BR-076, TTRDM-BR-077, TTRDM-BR-078, TTRDM-BR-079, TTRDM-BR-080, TTRDM-BR-081, TTRDM-BR-082, TTRDM-BR-083, TTRDM-BR-084, TTRDM-BR-085, TTRDM-BR-086. After: TTRDM-C09-T2, TTRDM-C09-T3.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - dialog "Update this transaction type?"
  - dialog "Delete this transaction type?"
  - message "Change result"
- [ ] TTRDM-C09-T5 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-065, TTRDM-REQ-F-066, TTRDM-REQ-F-067, TTRDM-REQ-F-068, TTRDM-REQ-F-069, TTRDM-REQ-F-070, TTRDM-REQ-F-071, TTRDM-REQ-F-072, TTRDM-REQ-F-073, TTRDM-REQ-F-074, TTRDM-REQ-F-075, TTRDM-REQ-F-076, TTRDM-REQ-F-077. Criteria: TTRDM-C09-AC-01, TTRDM-C09-AC-02, TTRDM-C09-AC-03, TTRDM-C09-AC-04, TTRDM-C09-AC-05, TTRDM-C09-AC-06, TTRDM-C09-AC-07, TTRDM-C09-AC-08, TTRDM-C09-AC-09, TTRDM-C09-AC-10, TTRDM-C09-AC-11, TTRDM-C09-AC-12, TTRDM-C09-AC-13, TTRDM-C09-AC-14, TTRDM-C09-AC-15. After: TTRDM-C09-T1, TTRDM-C09-T2, TTRDM-C09-T3, TTRDM-C09-T4.
  - 15 acceptance criteria, each a test named by its ID.
