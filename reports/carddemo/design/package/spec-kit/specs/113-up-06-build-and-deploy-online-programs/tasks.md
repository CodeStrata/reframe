# Tasks: Build and deploy online programs (UP-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C06-T1 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-028. Rules: UP-BR-030.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C06-T2 [api] Build the scheduled job. Requirements: UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027. Rules: UP-BR-027, UP-BR-028, UP-BR-029. After: UP-C06-T1.
  - UP-BR-027: A CI/CD deploy step. When the build succeeds (warnings allowed, no errors), roll out the new version to the running online service, for example by a rolling restart or a hot reload, so new requests use the new code.
  - UP-BR-028: Run this only when every build step succeeded without warnings. It registers or refreshes the program's database access against the CARDDEMO schema, replacing the previous version, using read-committed isolation. In a modern stack this is usually a schema migration or a step that grants database permissions, gated on a green build.
  - UP-BR-029: After the database access step succeeds (warnings allowed), refresh the application-level database binding that covers all CARDDEMO programs. Keep the existing permissions and use the same CARDDEMO schema and isolation. In a modern stack this is the deploy-time database configuration or role setup, and it must not reset grants.
- [ ] UP-C06-T3 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028. Criteria: UP-C06-AC-01, UP-C06-AC-02, UP-C06-AC-03, UP-C06-AC-04, UP-C06-AC-05, UP-C06-AC-06, UP-C06-AC-07. After: UP-C06-T1, UP-C06-T2.
  - 7 acceptance criteria, each a test named by its ID.
- [ ] UP-C06-T4 [compliance] Review the handling of security. Requirements: UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028. After: UP-C06-T1, UP-C06-T2.
  - Check storage, logs, screens and audit against the rules.
