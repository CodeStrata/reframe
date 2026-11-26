# Implementation plan: Load reference data into keyed files (TTRDM-C24)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C24-T1 [api] Build the scheduled job
  - TTRDM-BR-172: A scheduled job does a full replace of the transaction category lookup store from the category flat file. The store is cleared, then every 60-character record is loaded, keyed by its first 6 characters (type code plus category code). Other writers are kept out while it loads, and the source file is read without locking it.
  - TTRDM-BR-173: A scheduled job does a full replace of the transaction type lookup store from the transaction type flat file. The store is cleared, then every 60-character record is loaded, keyed by its first 2 characters (the type code), so readers get a keyed lookup by type code. Other writers are kept out while it loads.
  - _Requirements: TTRDM-REQ-F-160, TTRDM-REQ-F-161_
  - _Rules: TTRDM-BR-172, TTRDM-BR-173_
- [ ] 2. TTRDM-C24-T2 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-160, TTRDM-REQ-F-161_
  - _Criteria: TTRDM-C24-AC-01, TTRDM-C24-AC-02, TTRDM-C24-AC-03_
  - _After: TTRDM-C24-T1_
