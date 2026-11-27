# Implementation plan: Show maintenance screen values and messages (TTRDM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C12-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-093, TTRDM-REQ-F-094, TTRDM-REQ-F-095, TTRDM-REQ-F-096, TTRDM-REQ-F-097, TTRDM-REQ-F-098, TTRDM-REQ-F-099_
- [ ] 2. TTRDM-C12-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-098_
  - _Rules: TTRDM-BR-109_
  - _After: TTRDM-C12-T1_
- [ ] 3. TTRDM-C12-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-093, TTRDM-REQ-F-094, TTRDM-REQ-F-095, TTRDM-REQ-F-096, TTRDM-REQ-F-097_
  - _Rules: TTRDM-BR-093, TTRDM-BR-103, TTRDM-BR-104, TTRDM-BR-105, TTRDM-BR-106, TTRDM-BR-107, TTRDM-BR-108_
  - _After: TTRDM-C12-T1_
- [ ] 4. TTRDM-C12-T4 [api] Build the services behind the screens
  - TTRDM-BR-110: The screen's controller has a default path: any action not handled by a dedicated step (exit, first entry, delete, save, cancel, or a key not allowed in the current state) binds the submitted form, validates it, works out the next state and re-renders the screen.
  - TTRDM-BR-111: Route requests by action and current edit state; when no specific action-and-state handler matches, fall through to the default bind, validate, decide-next-state and re-render path rather than raising an error.
  - _Requirements: TTRDM-REQ-F-099_
  - _Rules: TTRDM-BR-110, TTRDM-BR-111_
  - _After: TTRDM-C12-T1, TTRDM-C12-T2, TTRDM-C12-T3_
- [ ] 5. TTRDM-C12-T5 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-091, TTRDM-REQ-F-092, TTRDM-REQ-F-093, TTRDM-REQ-F-094, TTRDM-REQ-F-095, TTRDM-REQ-F-096, TTRDM-REQ-F-097, TTRDM-REQ-F-098, TTRDM-REQ-F-099_
  - _Criteria: TTRDM-C12-AC-01, TTRDM-C12-AC-02, TTRDM-C12-AC-03, TTRDM-C12-AC-04, TTRDM-C12-AC-05, TTRDM-C12-AC-06, TTRDM-C12-AC-07, TTRDM-C12-AC-08, TTRDM-C12-AC-09, TTRDM-C12-AC-10, TTRDM-C12-AC-11, TTRDM-C12-AC-12_
  - _After: TTRDM-C12-T1, TTRDM-C12-T2, TTRDM-C12-T3, TTRDM-C12-T4_
