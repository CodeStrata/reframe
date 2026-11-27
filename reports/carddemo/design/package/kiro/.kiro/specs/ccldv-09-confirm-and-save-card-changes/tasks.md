# Implementation plan: Confirm and save card changes (CCLDV-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CCLDV-C09-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y, CVCUS01Y.
  - _Requirements: CCLDV-REQ-F-093, CCLDV-REQ-F-094, CCLDV-REQ-F-095, CCLDV-REQ-F-096, CCLDV-REQ-F-097, CCLDV-REQ-F-098, CCLDV-REQ-F-099_
- [ ] 2. CCLDV-C09-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-093, CCLDV-REQ-F-094, CCLDV-REQ-F-095, CCLDV-REQ-F-097, CCLDV-REQ-F-099_
  - _Rules: CCLDV-BR-105, CCLDV-BR-107, CCLDV-BR-108, CCLDV-BR-109, CCLDV-BR-110, CCLDV-BR-114, CCLDV-BR-115, CCLDV-BR-116_
  - _After: CCLDV-C09-T1_
- [ ] 3. CCLDV-C09-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-096, CCLDV-REQ-F-098_
  - _Rules: CCLDV-BR-111, CCLDV-BR-112, CCLDV-BR-113_
  - _After: CCLDV-C09-T1_
- [ ] 4. CCLDV-C09-T4 [ui-modernization] Build the screen Card details (S-CARD-DETAIL)
  - To the prototype: ui-reference/index.html#/S-CARD-DETAIL.
  - **primary button** "Save card": Nothing differs from the stored values (ignoring case): 'No change detected with respect to values fetched.' Fields are checked in the order name, status, expiry month, expiry year.
  - _Requirements: CCLDV-REQ-F-094, CCLDV-REQ-F-096, CCLDV-REQ-F-097, CCLDV-REQ-F-098, CCLDV-REQ-F-099_
  - _Rules: CCLDV-BR-109, CCLDV-BR-111, CCLDV-BR-112, CCLDV-BR-113, CCLDV-BR-114, CCLDV-BR-115, CCLDV-BR-116_
  - _After: CCLDV-C09-T2, CCLDV-C09-T3_
- [ ] 5. CCLDV-C09-T5 [test-generation] Write a test for every acceptance criterion
  - 14 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-093, CCLDV-REQ-F-094, CCLDV-REQ-F-095, CCLDV-REQ-F-096, CCLDV-REQ-F-097, CCLDV-REQ-F-098, CCLDV-REQ-F-099_
  - _Criteria: CCLDV-C09-AC-01, CCLDV-C09-AC-02, CCLDV-C09-AC-03, CCLDV-C09-AC-04, CCLDV-C09-AC-05, CCLDV-C09-AC-06, CCLDV-C09-AC-07, CCLDV-C09-AC-08, CCLDV-C09-AC-09, CCLDV-C09-AC-10, CCLDV-C09-AC-11, CCLDV-C09-AC-12, CCLDV-C09-AC-13, CCLDV-C09-AC-14_
  - _After: CCLDV-C09-T1, CCLDV-C09-T2, CCLDV-C09-T3, CCLDV-C09-T4_
- [ ] 6. CCLDV-C09-T6 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-093, CCLDV-REQ-F-094, CCLDV-REQ-F-095, CCLDV-REQ-F-096, CCLDV-REQ-F-097, CCLDV-REQ-F-098, CCLDV-REQ-F-099_
  - _After: CCLDV-C09-T1, CCLDV-C09-T2, CCLDV-C09-T3, CCLDV-C09-T4_
