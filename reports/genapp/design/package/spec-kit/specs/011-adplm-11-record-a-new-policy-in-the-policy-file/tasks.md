# Tasks: Record a new policy in the policy file (ADPLM-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C11-T1 [data] Model the data the capability reads and writes. Requirements: ADPLM-REQ-F-062, ADPLM-REQ-F-063, ADPLM-REQ-F-064, ADPLM-REQ-F-065, ADPLM-REQ-F-066, ADPLM-REQ-F-067, ADPLM-REQ-F-068, ADPLM-REQ-F-069.
  - Working records it passes or builds: LGCMAREA.
- [ ] ADPLM-C11-T2 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-069. Rules: ADPLM-BR-074. After: ADPLM-C11-T1.
  - Keep each business rule exactly as specified.
- [ ] ADPLM-C11-T3 [business-rules] Implement error handling and messages. Requirements: ADPLM-REQ-F-068. Rules: ADPLM-BR-073. After: ADPLM-C11-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] ADPLM-C11-T4 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-062, ADPLM-REQ-F-063, ADPLM-REQ-F-064, ADPLM-REQ-F-065, ADPLM-REQ-F-066, ADPLM-REQ-F-067. Rules: ADPLM-BR-067, ADPLM-BR-068, ADPLM-BR-069, ADPLM-BR-070, ADPLM-BR-071, ADPLM-BR-072. After: ADPLM-C11-T1, ADPLM-C11-T2, ADPLM-C11-T3.
  - ADPLM-BR-067: Build a composite key: the policy type letter, the customer number zero-padded to 10 digits, and the policy number zero-padded to 10 digits, 21 characters in all. Records are then found by keyed lookup on the full key, or by prefix (type, or type plus customer) for range browsing.
  - ADPLM-BR-068: Map the endowment summary into fixed-width fields: with-profits, equities and managed-fund indicators of 1 character each, fund name of 10 characters and life assured of 30 characters. Values are padded or truncated to those widths.
  - ADPLM-BR-069: Map the house summary into fixed-width fields: property type of 15 characters, bedrooms of 3 digits, value of 8 digits, postcode of 8 characters, and only the first 9 characters of the house name (truncated on purpose).
  - ADPLM-BR-070: Map the motor summary into fixed-width fields: make of 15 characters, model of 15 characters, value of 6 digits and registration of 7 characters.
  - ADPLM-BR-071: Map the commercial summary into fixed-width fields: postcode of 8 characters, status of 4 digits, and the first 31 characters of the customer name.
  - ADPLM-BR-072: Insert the 64-character summary record into the policy key-value or index store under the 21-character key, using insert-only semantics, so an existing key is never overwritten and the write fails instead.
- [ ] ADPLM-C11-T5 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-062, ADPLM-REQ-F-063, ADPLM-REQ-F-064, ADPLM-REQ-F-065, ADPLM-REQ-F-066, ADPLM-REQ-F-067, ADPLM-REQ-F-068, ADPLM-REQ-F-069. Criteria: ADPLM-C11-AC-01, ADPLM-C11-AC-02, ADPLM-C11-AC-03, ADPLM-C11-AC-04, ADPLM-C11-AC-05, ADPLM-C11-AC-06, ADPLM-C11-AC-07, ADPLM-C11-AC-08, ADPLM-C11-AC-09, ADPLM-C11-AC-10. After: ADPLM-C11-T1, ADPLM-C11-T2, ADPLM-C11-T3, ADPLM-C11-T4.
  - 10 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C11-T6 [compliance] Review the handling of audit, money, personal data. Requirements: ADPLM-REQ-F-062, ADPLM-REQ-F-063, ADPLM-REQ-F-064, ADPLM-REQ-F-065, ADPLM-REQ-F-066, ADPLM-REQ-F-067, ADPLM-REQ-F-068, ADPLM-REQ-F-069. After: ADPLM-C11-T1, ADPLM-C11-T2, ADPLM-C11-T3, ADPLM-C11-T4.
  - Check storage, logs, screens and audit against the rules.
