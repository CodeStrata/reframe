# Tasks: Prepare monitoring and workload simulation (ADPLM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C06-T1 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-034, ADPLM-REQ-F-035, ADPLM-REQ-F-036. Rules: ADPLM-BR-036, ADPLM-BR-037.
  - ADPLM-BR-036: An environment set-up step that initialises the monitoring console's repository with the console and system names and identifiers, daylight saving off, the time zone setting 'B' and a zone offset of 0, and prints a report. In the new application this is provisioning of the monitoring or observability tooling. It runs only when no earlier set-up step failed with a severity above 8.
  - ADPLM-BR-037: An on-demand load-test job that plays the GENAPP scripted scenarios (initialisation definitions plus message scripts) against the application, with the tool's own automatic logging off and its results and diagnostics sent to the job output. In the new application, use a load-testing tool with the scenario scripts kept in version control.
- [ ] ADPLM-C06-T2 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-034, ADPLM-REQ-F-035, ADPLM-REQ-F-036. Criteria: ADPLM-C06-AC-01, ADPLM-C06-AC-02, ADPLM-C06-AC-03. After: ADPLM-C06-T1.
  - 3 acceptance criteria, each a test named by its ID.
