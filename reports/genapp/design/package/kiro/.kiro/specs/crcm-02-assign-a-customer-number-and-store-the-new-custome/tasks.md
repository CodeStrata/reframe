# Implementation plan: Assign a customer number and store the new customer (CRCM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CRCM-C02-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: CRCM-REQ-F-005, CRCM-REQ-F-006, CRCM-REQ-F-007, CRCM-REQ-F-008, CRCM-REQ-F-009_
- [ ] 2. CRCM-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CRCM-REQ-F-005, CRCM-REQ-F-006, CRCM-REQ-F-009_
  - _Rules: CRCM-BR-009, CRCM-BR-010, CRCM-BR-011, CRCM-BR-013, CRCM-BR-015_
  - _After: CRCM-C02-T1_
- [ ] 3. CRCM-C02-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CRCM-REQ-F-008_
  - _Rules: CRCM-BR-013, CRCM-BR-014_
  - _After: CRCM-C02-T1_
- [ ] 4. CRCM-C02-T4 [api] Build the scheduled job
  - CRCM-BR-010: When the shared customer-number counter supplies the number, insert the customer row under that explicit key, together with the supplied name, date of birth, address, phone numbers and email. The key must be unique, so a clash with an existing customer is rejected rather than overwritten.
  - CRCM-BR-012: Both numbering paths, counter-issued or database-generated, must write the same nine fields: first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email. A single insert routine, with the key either supplied or generated, keeps the two paths consistent.
  - _Requirements: CRCM-REQ-F-007_
  - _Rules: CRCM-BR-010, CRCM-BR-012_
  - _After: CRCM-C02-T1, CRCM-C02-T2, CRCM-C02-T3_
- [ ] 5. CRCM-C02-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: CRCM-REQ-F-005, CRCM-REQ-F-006, CRCM-REQ-F-007, CRCM-REQ-F-008, CRCM-REQ-F-009_
  - _Criteria: CRCM-C02-AC-01, CRCM-C02-AC-02, CRCM-C02-AC-03, CRCM-C02-AC-04, CRCM-C02-AC-05, CRCM-C02-AC-06, CRCM-C02-AC-07_
  - _After: CRCM-C02-T1, CRCM-C02-T2, CRCM-C02-T3, CRCM-C02-T4_
- [ ] 6. CRCM-C02-T6 [compliance] Review the handling of audit, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CRCM-REQ-F-005, CRCM-REQ-F-006, CRCM-REQ-F-007, CRCM-REQ-F-008, CRCM-REQ-F-009_
  - _After: CRCM-C02-T1, CRCM-C02-T2, CRCM-C02-T3, CRCM-C02-T4_
