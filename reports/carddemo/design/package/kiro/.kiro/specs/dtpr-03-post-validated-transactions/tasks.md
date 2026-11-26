# Implementation plan: Post validated transactions (DTPR-C03)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C03-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA01Y, CVTRA05Y, CVTRA06Y (see data-contracts.md).
  - _Requirements: DTPR-REQ-F-020, DTPR-REQ-F-021, DTPR-REQ-F-022, DTPR-REQ-F-023, DTPR-REQ-F-024, DTPR-REQ-F-025, DTPR-REQ-F-026, DTPR-REQ-F-027, DTPR-REQ-F-028, DTPR-REQ-F-029, DTPR-REQ-F-030, DTPR-REQ-F-031, DTPR-REQ-F-032_
- [ ] 2. DTPR-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: DTPR-BR-035.
  - _Requirements: DTPR-REQ-F-020, DTPR-REQ-F-022, DTPR-REQ-F-023, DTPR-REQ-F-025, DTPR-REQ-F-026, DTPR-REQ-F-027, DTPR-REQ-F-029_
  - _Rules: DTPR-BR-025, DTPR-BR-026, DTPR-BR-028, DTPR-BR-029, DTPR-BR-031, DTPR-BR-032, DTPR-BR-033, DTPR-BR-035_
  - _After: DTPR-C03-T1_
- [ ] 3. DTPR-C03-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-F-024, DTPR-REQ-F-032_
  - _Rules: DTPR-BR-025, DTPR-BR-030, DTPR-BR-038_
  - _After: DTPR-C03-T1_
- [ ] 4. DTPR-C03-T4 [api] Build the scheduled job
  - DTPR-BR-027: Look up the category balance by a composite key of account ID, transaction type and transaction category; a unique key or index on these three columns. 'Not found' must be told apart from other errors, because 'not found' leads to creating the record.
  - DTPR-BR-034: Save the account's new balance and cycle totals before writing the posted transaction. Ideally both happen in one database transaction, so an account is never updated without its transaction record, or the reverse.
  - DTPR-BR-036: Map the posted transaction field for field from the daily transaction: ID, type, category, source, description, amount, merchant ID, name, city, ZIP, card number and original timestamp. Only the processed timestamp is added by posting.
  - DTPR-BR-037: Take the processed timestamp from the run's clock and store it as a proper timestamp. Where it is exported or compared with legacy data, render it as YYYY-MM-DD-HH.MM.SS.hh0000 (hundredths of a second followed by '0000').
  - _Requirements: DTPR-REQ-F-021, DTPR-REQ-F-028, DTPR-REQ-F-030, DTPR-REQ-F-031_
  - _Rules: DTPR-BR-027, DTPR-BR-034, DTPR-BR-036, DTPR-BR-037_
  - _After: DTPR-C03-T1, DTPR-C03-T2, DTPR-C03-T3_
- [ ] 5. DTPR-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 17 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-020, DTPR-REQ-F-021, DTPR-REQ-F-022, DTPR-REQ-F-023, DTPR-REQ-F-024, DTPR-REQ-F-025, DTPR-REQ-F-026, DTPR-REQ-F-027, DTPR-REQ-F-028, DTPR-REQ-F-029, DTPR-REQ-F-030, DTPR-REQ-F-031, DTPR-REQ-F-032_
  - _Criteria: DTPR-C03-AC-01, DTPR-C03-AC-02, DTPR-C03-AC-03, DTPR-C03-AC-04, DTPR-C03-AC-05, DTPR-C03-AC-06, DTPR-C03-AC-07, DTPR-C03-AC-08, DTPR-C03-AC-09, DTPR-C03-AC-10, DTPR-C03-AC-11, DTPR-C03-AC-12, DTPR-C03-AC-13, DTPR-C03-AC-14, DTPR-C03-AC-15, DTPR-C03-AC-16, DTPR-C03-AC-17_
  - _After: DTPR-C03-T1, DTPR-C03-T2, DTPR-C03-T3, DTPR-C03-T4_
- [ ] 6. DTPR-C03-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-020, DTPR-REQ-F-021, DTPR-REQ-F-022, DTPR-REQ-F-023, DTPR-REQ-F-024, DTPR-REQ-F-025, DTPR-REQ-F-026, DTPR-REQ-F-027, DTPR-REQ-F-028, DTPR-REQ-F-029, DTPR-REQ-F-030, DTPR-REQ-F-031, DTPR-REQ-F-032_
  - _After: DTPR-C03-T1, DTPR-C03-T2, DTPR-C03-T3, DTPR-C03-T4_
