# Implementation plan: Back up and distribute the FTP test file (SOM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. SOM-C05-T1 [api] Build the scheduled job
  - SOM-BR-032: A batch step that copies every record of the FTP test file into its existing backup file (or object), replacing what is there. It must not stop other readers using either file while it runs, for example by copying to a temporary file and then renaming it, or by copying object to object in storage.
  - SOM-BR-033: Once the backup step finishes, the job must trigger the follow-on job (INTRDRJ2) using its stored job definition, unchanged. In the new application this is a dependency in the scheduler or workflow (backup, then distribute), or an event or message that starts the follow-on job, not a submission of job text.
  - SOM-BR-034: The follow-on job copies every record of the backup file into the existing second copy (the legacy '.INTRDR' copy). Like the first step, it must not lock out other jobs reading or writing these files while it runs.
  - _Requirements: SOM-REQ-F-028, SOM-REQ-F-029, SOM-REQ-F-030_
  - _Rules: SOM-BR-032, SOM-BR-033, SOM-BR-034_
- [ ] 2. SOM-C05-T2 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: SOM-REQ-F-028, SOM-REQ-F-029, SOM-REQ-F-030_
  - _Criteria: SOM-C05-AC-01, SOM-C05-AC-02, SOM-C05-AC-03_
  - _After: SOM-C05-T1_
