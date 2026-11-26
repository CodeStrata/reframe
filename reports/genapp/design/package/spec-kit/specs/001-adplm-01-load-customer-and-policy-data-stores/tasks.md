# Tasks: Load customer and policy data stores (ADPLM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C01-T1 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-001, ADPLM-REQ-F-002, ADPLM-REQ-F-003, ADPLM-REQ-F-004. Rules: ADPLM-BR-001, ADPLM-BR-002.
  - ADPLM-BR-001: A one-time bulk import step in the environment set-up pipeline. It copies every record from the supplied policy extract into the policy store and depends on the step that creates the store: run the import when that step succeeded (severity 7 or less) or was skipped, and skip it when that step failed with a severity above 7. Report how many records were read and how many were written so the load can be reconciled.
  - ADPLM-BR-002: The same guarded bulk import for customers. Copy every record from the supplied customer extract into the customer store, but only when the step that creates the store succeeded (severity 7 or less) or did not run. Skip the import when that step failed with a severity above 7. Report the record counts.
- [ ] ADPLM-C01-T2 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-001, ADPLM-REQ-F-002, ADPLM-REQ-F-003, ADPLM-REQ-F-004. Criteria: ADPLM-C01-AC-01, ADPLM-C01-AC-02, ADPLM-C01-AC-03, ADPLM-C01-AC-04. After: ADPLM-C01-T1.
  - 4 acceptance criteria, each a test named by its ID.
