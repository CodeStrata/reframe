# Implementation plan: Receive and prepare card authorization requests (CAFM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C04-T1 [data] Model the data the capability reads and writes
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
  - _Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-046, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-049, CAFM-REQ-F-050, CAFM-REQ-F-051_
- [ ] 2. CAFM-C04-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-050_
  - _Rules: CAFM-BR-046, CAFM-BR-047, CAFM-BR-049, CAFM-BR-050, CAFM-BR-052_
  - _After: CAFM-C04-T1_
- [ ] 3. CAFM-C04-T3 [api] Build the services behind the screens
  - CAFM-BR-042: Consume authorization requests from the request queue one at a time, committing after each. Stop after 501 messages in one activation (the limit is 500, checked as 'more than') and leave the rest for the next activation. Make the limit a configuration value.
  - CAFM-BR-043: Wait up to 5 seconds for each next request, and end the consumer cleanly when none arrives.
  - CAFM-BR-044: Read the request as comma-separated text in this field order: auth date, auth time, card number, auth type, card expiry, message type, message source, processing code, amount, merchant category code, acquirer country code, POS entry mode, merchant id, merchant name, merchant city, merchant state, merchant zip, transaction id. Convert the amount text to a decimal number.
  - CAFM-BR-045: Once the card is found, look up the account by the account id from the card cross-reference (a keyed lookup by account id) and record whether it was found.
  - CAFM-BR-048: Once the card is found, look up the customer by the customer id from the card cross-reference (a keyed lookup by customer id) and record whether it was found.
  - CAFM-BR-051: Look up the pending-authorization summary by the card's account id. Keep three outcomes apart: found, not found (a valid state, after which a new summary is created) and read failure (critical error 'I002').
  - CAFM-BR-053: Authorization details must list newest first under their account. The legacy key does this with an inverted date (99999 minus YYDDD) and an inverted time (999999999 minus time×1000+milliseconds). A modern store can order by a full timestamp descending instead, but the purge's age calculation and the paging keys must use the same date.
  - _Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-046, CAFM-REQ-F-049, CAFM-REQ-F-051_
  - _Rules: CAFM-BR-042, CAFM-BR-043, CAFM-BR-044, CAFM-BR-045, CAFM-BR-048, CAFM-BR-051, CAFM-BR-053_
  - _After: CAFM-C04-T1, CAFM-C04-T2_
- [ ] 4. CAFM-C04-T4 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-046, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-049, CAFM-REQ-F-050, CAFM-REQ-F-051_
  - _Criteria: CAFM-C04-AC-01, CAFM-C04-AC-02, CAFM-C04-AC-03, CAFM-C04-AC-04, CAFM-C04-AC-05, CAFM-C04-AC-06, CAFM-C04-AC-07, CAFM-C04-AC-08, CAFM-C04-AC-09, CAFM-C04-AC-10, CAFM-C04-AC-11, CAFM-C04-AC-12, CAFM-C04-AC-13, CAFM-C04-AC-14, CAFM-C04-AC-15_
  - _After: CAFM-C04-T1, CAFM-C04-T2, CAFM-C04-T3_
- [ ] 5. CAFM-C04-T5 [compliance] Review the handling of card data, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-046, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-049, CAFM-REQ-F-050, CAFM-REQ-F-051_
  - _After: CAFM-C04-T1, CAFM-C04-T2, CAFM-C04-T3_
