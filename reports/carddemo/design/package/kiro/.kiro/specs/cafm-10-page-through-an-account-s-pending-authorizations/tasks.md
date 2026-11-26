# Implementation plan: Page through an account's pending authorizations (CAFM-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C10-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSMSG02Y, CVACT02Y.
  - _Requirements: CAFM-REQ-F-101, CAFM-REQ-F-102, CAFM-REQ-F-103, CAFM-REQ-F-104, CAFM-REQ-F-105, CAFM-REQ-F-106, CAFM-REQ-F-107, CAFM-REQ-F-108_
- [ ] 2. CAFM-C10-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-101, CAFM-REQ-F-103, CAFM-REQ-F-104, CAFM-REQ-F-105, CAFM-REQ-F-106, CAFM-REQ-F-107_
  - _Rules: CAFM-BR-105, CAFM-BR-107, CAFM-BR-108, CAFM-BR-109, CAFM-BR-110, CAFM-BR-111, CAFM-BR-112_
  - _After: CAFM-C10-T1_
- [ ] 3. CAFM-C10-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-108_
  - _Rules: CAFM-BR-113, CAFM-BR-114_
  - _After: CAFM-C10-T1_
- [ ] 4. CAFM-C10-T4 [api] Build the services behind the screens
  - CAFM-BR-106: Use keyset (cursor) pagination over the account's authorizations in newest-first order. For a forward page, start after the last authorization key shown, or from the beginning when there is none. Keep the cursor in session state, not as a page offset.
  - CAFM-BR-108: For the next page, fetch up to 5 authorizations after the cursor and replace the list rows entirely, so rows from the previous page never remain. Fetch one more to work out whether a further page exists, and keep each page's first key so backward paging works.
  - _Requirements: CAFM-REQ-F-102_
  - _Rules: CAFM-BR-106_
  - _After: CAFM-C10-T1, CAFM-C10-T2, CAFM-C10-T3_
- [ ] 5. CAFM-C10-T5 [ui-modernization] Build the screen Pending authorizations (S-PENDING-AUTHS)
  - To the prototype: ui-reference/index.html#/S-PENDING-AUTHS.
  - table "Pending authorizations": Only a row's 'View details' action opens an authorization, so 'Invalid selection. Valid value is S' cannot arise; it is shown if a row without an authorization is opened. Previous is disabled on the first page and announces 'You are already at the top of the page...'; Next is disabled on the last page and announces 'You are already at the bottom of the page...'.
  - _Requirements: CAFM-REQ-F-101, CAFM-REQ-F-102, CAFM-REQ-F-103, CAFM-REQ-F-104, CAFM-REQ-F-105, CAFM-REQ-F-106, CAFM-REQ-F-107, CAFM-REQ-F-108_
  - _Rules: CAFM-BR-105, CAFM-BR-106, CAFM-BR-107, CAFM-BR-108, CAFM-BR-109, CAFM-BR-110, CAFM-BR-111, CAFM-BR-112, CAFM-BR-113, CAFM-BR-114_
  - _After: CAFM-C10-T2, CAFM-C10-T3, CAFM-C10-T4_
- [ ] 6. CAFM-C10-T6 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-101, CAFM-REQ-F-102, CAFM-REQ-F-103, CAFM-REQ-F-104, CAFM-REQ-F-105, CAFM-REQ-F-106, CAFM-REQ-F-107, CAFM-REQ-F-108_
  - _Criteria: CAFM-C10-AC-01, CAFM-C10-AC-02, CAFM-C10-AC-03, CAFM-C10-AC-04, CAFM-C10-AC-05, CAFM-C10-AC-06, CAFM-C10-AC-07, CAFM-C10-AC-08, CAFM-C10-AC-09, CAFM-C10-AC-10, CAFM-C10-AC-11, CAFM-C10-AC-12, CAFM-C10-AC-13_
  - _After: CAFM-C10-T1, CAFM-C10-T2, CAFM-C10-T3, CAFM-C10-T4, CAFM-C10-T5_
- [ ] 7. CAFM-C10-T7 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-101, CAFM-REQ-F-102, CAFM-REQ-F-103, CAFM-REQ-F-104, CAFM-REQ-F-105, CAFM-REQ-F-106, CAFM-REQ-F-107, CAFM-REQ-F-108_
  - _After: CAFM-C10-T1, CAFM-C10-T2, CAFM-C10-T3, CAFM-C10-T4, CAFM-C10-T5_
