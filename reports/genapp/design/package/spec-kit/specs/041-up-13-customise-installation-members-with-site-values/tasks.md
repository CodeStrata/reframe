# Tasks: Customise installation members with site values (UP-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C13-T1 [business-rules] Implement the business rules. Requirements: UP-REQ-F-096. Rules: UP-BR-121.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: UP-BR-121.
- [ ] UP-C13-T2 [api] Build the service. Requirements: UP-REQ-F-097, UP-REQ-F-098, UP-REQ-F-099, UP-REQ-F-100. Rules: UP-BR-122, UP-BR-123, UP-BR-124, UP-BR-125. After: UP-C13-T1.
  - UP-BR-122: The CICSPlex SM Web User Interface system identifier becomes a per-environment deployment setting (default 'IWUI'). The deployment templating step fills every '<WUISYSID>' in the configuration and install templates with it. The step fails if the setting is missing, so no template is left with the placeholder.
  - UP-BR-123: The Db2 subsystem identifier becomes a per-environment setting (default 'DKM1'), and the same templating step fills every '<DB2SSID>' with it. In the new application this is the database connection target in environment configuration. It must not be hard-coded in any member or in code.
  - UP-BR-124: The CICSPlex SM address space (CMAS) system identifier becomes a per-environment setting (default 'ICMA'). The templating step fills every '<CMASYSID>' with it. It is only needed while the target environment still runs CICSPlex SM; if the new platform has no CMAS, the setting and its placeholder can be dropped.
  - UP-BR-125: The Language Environment runtime library qualifier becomes a per-environment setting (default 'CEE'). The templating step fills every '<CEEHLQ>' with it. On a non-mainframe runtime this maps to the location of the runtime libraries, or it is not needed at all.
- [ ] UP-C13-T3 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-096, UP-REQ-F-097, UP-REQ-F-098, UP-REQ-F-099, UP-REQ-F-100. Criteria: UP-C13-AC-01, UP-C13-AC-02, UP-C13-AC-03, UP-C13-AC-04, UP-C13-AC-05, UP-C13-AC-06. After: UP-C13-T1, UP-C13-T2.
  - 6 acceptance criteria, each a test named by its ID.
