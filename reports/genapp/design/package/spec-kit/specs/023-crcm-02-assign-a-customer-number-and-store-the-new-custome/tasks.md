# Tasks: Assign a customer number and store the new customer (CRCM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CRCM-C02-T1 [data] Model the data the capability reads and writes. Requirements: CRCM-REQ-F-005, CRCM-REQ-F-006, CRCM-REQ-F-007, CRCM-REQ-F-008, CRCM-REQ-F-009.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] CRCM-C02-T2 [business-rules] Implement the business rules. Requirements: CRCM-REQ-F-005, CRCM-REQ-F-006, CRCM-REQ-F-009. Rules: CRCM-BR-009, CRCM-BR-010, CRCM-BR-011, CRCM-BR-013, CRCM-BR-015. After: CRCM-C02-T1.
  - Keep each business rule exactly as specified.
- [ ] CRCM-C02-T3 [business-rules] Implement error handling and messages. Requirements: CRCM-REQ-F-008. Rules: CRCM-BR-013, CRCM-BR-014. After: CRCM-C02-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CRCM-C02-T4 [api] Build the scheduled job. Requirements: CRCM-REQ-F-007. Rules: CRCM-BR-010, CRCM-BR-012. After: CRCM-C02-T1, CRCM-C02-T2, CRCM-C02-T3.
  - CRCM-BR-010: When the shared customer-number counter supplies the number, insert the customer row under that explicit key, together with the supplied name, date of birth, address, phone numbers and email. The key must be unique, so a clash with an existing customer is rejected rather than overwritten.
  - CRCM-BR-012: Both numbering paths, counter-issued or database-generated, must write the same nine fields: first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email. A single insert routine, with the key either supplied or generated, keeps the two paths consistent.
- [ ] CRCM-C02-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CRCM-REQ-F-005, CRCM-REQ-F-006, CRCM-REQ-F-007, CRCM-REQ-F-008, CRCM-REQ-F-009. Criteria: CRCM-C02-AC-01, CRCM-C02-AC-02, CRCM-C02-AC-03, CRCM-C02-AC-04, CRCM-C02-AC-05, CRCM-C02-AC-06, CRCM-C02-AC-07. After: CRCM-C02-T1, CRCM-C02-T2, CRCM-C02-T3, CRCM-C02-T4.
  - 7 acceptance criteria, each a test named by its ID.
- [ ] CRCM-C02-T6 [compliance] Review the handling of audit, personal data. Requirements: CRCM-REQ-F-005, CRCM-REQ-F-006, CRCM-REQ-F-007, CRCM-REQ-F-008, CRCM-REQ-F-009. After: CRCM-C02-T1, CRCM-C02-T2, CRCM-C02-T3, CRCM-C02-T4.
  - Check storage, logs, screens and audit against the rules.
