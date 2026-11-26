# Tasks: Define online files and transactions (ADPLM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C02-T1 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-005, ADPLM-REQ-F-006, ADPLM-REQ-F-007, ADPLM-REQ-F-008, ADPLM-REQ-F-009, ADPLM-REQ-F-010, ADPLM-REQ-F-011. Rules: ADPLM-BR-003, ADPLM-BR-004, ADPLM-BR-005, ADPLM-BR-006, ADPLM-BR-007, ADPLM-BR-008, ADPLM-BR-009, ADPLM-BR-010, ADPLM-BR-011.
  - ADPLM-BR-003: Declare the policy store in deployment configuration. It holds 64-character records under a 21-character key and is available as soon as it is first used. The application's data-access role may create, read, browse by key range, update and delete policy records.
  - ADPLM-BR-004: Declare the customer store in deployment configuration. It holds 82-character records keyed by the 10-digit customer number. The application's data-access role may create, read, browse and update customer records but has no delete permission, so a customer delete is refused by the store itself.
  - ADPLM-BR-005: This is the same policy-store definition used by another environment's set-up. Keep one shared definition (64-character records, 21-character key, full create/read/browse/update/delete) in configuration that every environment applies, rather than a copy per environment.
  - ADPLM-BR-006: A duplicate of the shared policy-store definition (64-character records, 21-character key, full maintenance) for the second environment set-up. Apply the same single definition.
  - ADPLM-BR-007: This is the same customer-store definition for another environment: 82-character records and a 10-character key, with create, read, browse and update allowed and delete not allowed. Use the shared definition so the no-delete restriction cannot differ between environments.
  - ADPLM-BR-008: A duplicate of the shared customer-store definition (82-character records, 10-character key, delete not allowed) for the second environment set-up. Apply the same single definition.
  - ADPLM-BR-009: A routing table that maps each entry code to its handler: SSC1 to customer menu (LGTESTC1), SSP1 to LGTESTP1, SSP2 to LGTESTP2, SSP3 to LGTESTP3, SSP4 to LGTESTP4, LGSE to set-up (LGSETUP), LGCF to the customer counter (LGICVS01) and LGPF to the policy counter (LGIPVS01). In the new application these become registered routes or endpoints that run with ordinary user privileges.
  - ADPLM-BR-010: The same eight-route mapping (SSC1, SSP1 to SSP4, LGSE, LGCF and LGPF to their handlers) for the front-end that users connect to. Keep one route registry shared by the front-end and the services, with no elevated privileges.
  - ADPLM-BR-011: Deployment must replace the configuration, not add to it. Remove the previous application definitions before applying the new routes, so that a redeploy is repeatable and leaves no stale routes or store definitions behind.
- [ ] ADPLM-C02-T2 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-005, ADPLM-REQ-F-006, ADPLM-REQ-F-007, ADPLM-REQ-F-008, ADPLM-REQ-F-009, ADPLM-REQ-F-010, ADPLM-REQ-F-011. Criteria: ADPLM-C02-AC-01, ADPLM-C02-AC-02, ADPLM-C02-AC-03, ADPLM-C02-AC-04, ADPLM-C02-AC-05, ADPLM-C02-AC-06, ADPLM-C02-AC-07, ADPLM-C02-AC-08, ADPLM-C02-AC-09, ADPLM-C02-AC-10, ADPLM-C02-AC-11, ADPLM-C02-AC-12, ADPLM-C02-AC-13. After: ADPLM-C02-T1.
  - 13 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C02-T3 [compliance] Review the handling of security. Requirements: ADPLM-REQ-F-005, ADPLM-REQ-F-006, ADPLM-REQ-F-007, ADPLM-REQ-F-008, ADPLM-REQ-F-009, ADPLM-REQ-F-010, ADPLM-REQ-F-011. After: ADPLM-C02-T1.
  - Check storage, logs, screens and audit against the rules.
