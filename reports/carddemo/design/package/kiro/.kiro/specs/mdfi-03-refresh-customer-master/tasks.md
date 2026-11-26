# Implementation plan: Refresh customer master (MDFI-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. MDFI-C03-T1 [api] Build the scheduled job
  - MDFI-BR-006: Before the reload starts, the job must tell the online application to stop serving customer data, for example with a maintenance flag, a message, or an admin API call that makes customer reads return 'temporarily unavailable'. When the load is done it must turn customer access back on. Alternatively, the job can load into a staging table and swap it in atomically, so online users never see a partial store.
  - MDFI-BR-007: Recreate or empty the customer store with the 9-character customer ID as its unique key. Each customer record holds the fields of the 500-byte legacy layout. A store that does not exist yet must not make the job fail.
  - MDFI-BR-008: A bulk import of every record in the customer extract file into the new customer store. It must produce a run report, at least the records read and written plus any errors, and keep it as the job's output or log for operations.
  - _Requirements: MDFI-REQ-F-006, MDFI-REQ-F-007, MDFI-REQ-F-008_
  - _Rules: MDFI-BR-006, MDFI-BR-007, MDFI-BR-008_
- [ ] 2. MDFI-C03-T2 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: MDFI-REQ-F-006, MDFI-REQ-F-007, MDFI-REQ-F-008_
  - _Criteria: MDFI-C03-AC-01, MDFI-C03-AC-02, MDFI-C03-AC-03, MDFI-C03-AC-04_
  - _After: MDFI-C03-T1_
- [ ] 3. MDFI-C03-T3 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: MDFI-REQ-F-006, MDFI-REQ-F-007, MDFI-REQ-F-008_
  - _After: MDFI-C03-T1_
