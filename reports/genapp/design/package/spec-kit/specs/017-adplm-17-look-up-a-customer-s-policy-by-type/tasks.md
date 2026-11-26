# Tasks: Look up a customer's policy by type (ADPLM-C17)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C17-T1 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-107, ADPLM-REQ-F-108, ADPLM-REQ-N-002. Rules: ADPLM-BR-114, ADPLM-BR-115, ADPLM-BR-116.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: ADPLM-BR-114.
- [ ] ADPLM-C17-T2 [business-rules] Implement error handling and messages. Requirements: ADPLM-REQ-F-109, ADPLM-REQ-F-111. Rules: ADPLM-BR-117, ADPLM-BR-118, ADPLM-BR-120.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] ADPLM-C17-T3 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-105, ADPLM-REQ-F-106, ADPLM-REQ-F-110. Rules: ADPLM-BR-112, ADPLM-BR-113, ADPLM-BR-119. After: ADPLM-C17-T1, ADPLM-C17-T2.
  - ADPLM-BR-112: The interactive entry point takes the policy type and the customer number as separate input fields, instead of splitting a typed line at fixed offsets after a 5-character transaction code and space.
  - ADPLM-BR-113: The service entry point takes a request with a one-character policy type and a 10-digit customer number as named fields.
  - ADPLM-BR-119: Return a fresh response for service callers that holds the result label ('Policy Key=' or 'Policy Bad=') and the 21-character key. Nothing from the caller's request is echoed back.
- [ ] ADPLM-C17-T4 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-105, ADPLM-REQ-F-106, ADPLM-REQ-N-002, ADPLM-REQ-F-107, ADPLM-REQ-F-108, ADPLM-REQ-F-109, ADPLM-REQ-F-110, ADPLM-REQ-F-111. Criteria: ADPLM-C17-AC-01, ADPLM-C17-AC-02, ADPLM-C17-AC-03, ADPLM-C17-AC-04, ADPLM-C17-AC-05, ADPLM-C17-AC-06, ADPLM-C17-AC-07, ADPLM-C17-AC-08, ADPLM-C17-AC-09, ADPLM-C17-AC-10, ADPLM-C17-AC-11, ADPLM-C17-AC-12. After: ADPLM-C17-T1, ADPLM-C17-T2, ADPLM-C17-T3.
  - 12 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C17-T5 [compliance] Review the handling of personal data. Requirements: ADPLM-REQ-F-105, ADPLM-REQ-F-106, ADPLM-REQ-N-002, ADPLM-REQ-F-107, ADPLM-REQ-F-108, ADPLM-REQ-F-109, ADPLM-REQ-F-110, ADPLM-REQ-F-111. After: ADPLM-C17-T1, ADPLM-C17-T2, ADPLM-C17-T3.
  - Check storage, logs, screens and audit against the rules.
