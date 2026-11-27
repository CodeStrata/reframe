# Tasks: Back up and distribute the FTP test file (SOM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] SOM-C05-T1 [api] Build the scheduled job. Requirements: SOM-REQ-F-028, SOM-REQ-F-029, SOM-REQ-F-030. Rules: SOM-BR-032, SOM-BR-033, SOM-BR-034.
  - SOM-BR-032: A scheduled job step that copies the FTP test file record for record into the existing backup location, for example object-storage copy or file copy. It must not lock out other readers or writers while it runs, and it fails if the backup target does not already exist.
  - SOM-BR-033: After the backup step succeeds, the job triggers the follow-on job (INTRDRJ2) from its stored, unchanged definition. In a modern scheduler or workflow engine this is a job dependency or chained trigger, not the copying of a job definition to a reader. The legacy output class 'A' becomes the follow-on job's default log destination.
  - SOM-BR-034: A follow-on job that copies every record of the backup file into the already-existing secondary copy (the '.INTRDR' copy). Both files stay readable by other jobs while it runs. It runs only when the first job triggers it.
- [ ] SOM-C05-T2 [test-generation] Write a test for every acceptance criterion. Requirements: SOM-REQ-F-028, SOM-REQ-F-029, SOM-REQ-F-030. Criteria: SOM-C05-AC-01, SOM-C05-AC-02, SOM-C05-AC-03. After: SOM-C05-T1.
  - 3 acceptance criteria, each a test named by its ID.
