# Implementation plan: Build screen map copybooks (UP-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C01-T1 [api] Build the scheduled job
  - UP-BR-001: A build-pipeline step that generates the screen's field-layout (view model / DTO) definition from the screen source. It produces only that definition, not an executable artefact. In the new stack this belongs in the UI build or code generation, not in a runtime job.
  - UP-BR-002: Write the generated layout to the shared source location under the screen's name, replacing the previous version atomically so nothing else writes it at the same time. Keep the build log or listing as a build artefact named after the screen.
  - _Requirements: UP-REQ-F-001, UP-REQ-F-002_
  - _Rules: UP-BR-001, UP-BR-002_
- [ ] 2. UP-C01-T2 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-001, UP-REQ-F-002_
  - _Criteria: UP-C01-AC-01, UP-C01-AC-02_
  - _After: UP-C01-T1_
