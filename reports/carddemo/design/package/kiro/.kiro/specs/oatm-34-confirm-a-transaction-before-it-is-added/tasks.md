# Implementation plan: Confirm a transaction before it is added (OATM-C34)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C34-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
  - _Requirements: OATM-REQ-F-284, OATM-REQ-F-285_
- [ ] 2. OATM-C34-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-284, OATM-REQ-F-285_
  - _Rules: OATM-BR-301, OATM-BR-302_
  - _After: OATM-C34-T1_
- [ ] 3. OATM-C34-T3 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - **primary button** "Add transaction": The dialog offers only Add or Cancel, replacing the typed confirmation and its messages 'Confirm to add this transaction...' and 'Invalid value. Valid values are (Y/N)...'. If the ID already exists: 'Tran ID already exist...'; other failures: 'Unable to Add Transaction...'.
  - _Requirements: OATM-REQ-F-284, OATM-REQ-F-285_
  - _Rules: OATM-BR-301, OATM-BR-302_
  - _After: OATM-C34-T2_
- [ ] 4. OATM-C34-T4 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-284, OATM-REQ-F-285_
  - _Criteria: OATM-C34-AC-01, OATM-C34-AC-02, OATM-C34-AC-03_
  - _After: OATM-C34-T1, OATM-C34-T2, OATM-C34-T3_
