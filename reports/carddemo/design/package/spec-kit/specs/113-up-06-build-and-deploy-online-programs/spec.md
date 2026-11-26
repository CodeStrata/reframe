# Feature specification: Build and deploy online programs

**Feature:** UP-C06 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C06)

As a CardDemo build engineer, I want online programs compiled, bound to the database and refreshed in the online region, so that online users run the newly built code.

The build-and-deploy steps for online programs: compile, register the program's database access, and make the online system load the new version. Build engineers use it. It must never deploy or bind a program whose build failed, and online users must pick up the new version only after a successful build.

**Acceptance scenarios:**

1. **Given** compile step return code: 4, **when** the program compile step of the sample online build job ends with return code 4 or lower, **then** The NEWCOPY step runs and the region loads the new copy of program CICSPGMN. (UP-C06-AC-01)
2. **Given** compile step return code: 8, **when** the program compile step of the sample online build job ends with return code 4 or lower, **then** The NEWCOPY step is bypassed; the online region keeps running the old copy. (UP-C06-AC-02)
3. **Given** program name (MEMNAME): CICSDB2P; return code of every earlier build step: 0, **when** the Db2 precompile, CICS translation, COBOL compile and link-edit steps have all ended with return code 0, **then** Package CARDDEMO.CICSDB2P is bound with qualifier 'CARDDEMO' and replaces any earlier version of that package (UP-C06-AC-03)
4. **Given** COBOL compile return code: 8, **when** the Db2 precompile, CICS translation, COBOL compile and link-edit steps have all ended with return code 0, **then** The package bind step does not run (UP-C06-AC-04)
5. **Given** package bind return code: 4; plan: CARDDEMO, **when** the package bind ended with return code 4 or less, **then** Plan CARDDEMO is rebound over every package in collection CARDDEMO and keeps its existing grants (UP-C06-AC-05)
6. **Given** package bind return code: 8, **when** the package bind ended with return code 4 or less, **then** The plan bind is skipped (UP-C06-AC-06)
7. **Given** link-edit return code: 8; package bind: skipped, **when** the package bind did not run because the link-edit failed, **then** The plan bind still runs over the existing packages in CARDDEMO (UP-C06-AC-07)

## Requirements

### Functional requirements

- **UP-REQ-F-025** (design note): When the program compile step of the sample online build job ends with return code 4 or lower, the system shall send the online region (CICSAWSA) the console command 'CEMT SET PROG(CICSPGMN) NEWCOPY' so that the newly built program is loaded for online users. Rules: UP-BR-027.
- **UP-REQ-F-026** (design note): When the Db2 precompile, CICS translation, COBOL compile and link-edit steps have all ended with return code 0, the system shall bind the program's database request module into package collection 'CARDDEMO' with qualifier 'CARDDEMO', action 'REPLACE', isolation 'CS', current data 'YES', explain 'NO' and encoding 'EBCDIC'. Rules: UP-BR-028.
- **UP-REQ-F-027** (design note): When the package bind ended with return code 4 or less, the system shall bind the application plan ('CARDDEMO' in the sample job) over package list 'CARDDEMO.*' with qualifier 'CARDDEMO', action 'REPLACE' keeping existing authorizations ('RETAIN'), isolation 'CS', current data 'YES' and encoding 'EBCDIC'. Rules: UP-BR-029.
- **UP-REQ-F-028** (error handling): If the package bind did not run because the link-edit failed, then the system shall still run the plan bind, because a return-code test on a step that did not run is ignored. Rules: UP-BR-030.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-027 | Refresh the program in the online region | design note | WHEN the program compile step of the sample online build job ends with return code 4 or lower, THE Online Program Deployment SHALL send the online region (CICSAWSA) the console command 'CEMT SET PROG(CICSPGMN) NEWCOPY' so the newly built program is loaded for online users. | medium | samples/jcl/CICCMP.jcl:32-33, samples/jcl/CICCMP.jcl:41, samples/jcl/CICCMP.jcl:45-50 |
| UP-BR-028 | Bind the CardDemo database package | design note | WHEN the Db2 precompile, CICS translation, COBOL compile and link-edit steps have all ended with return code 0, THE CICS-Db2 build job SHALL bind the program's database request module into package collection 'CARDDEMO' with qualifier 'CARDDEMO', action 'REPLACE', isolation 'CS', current data 'YES', explain 'NO' and encoding 'EBCDIC'. | medium | samples/proc/BLDCIDB2.prc:80-81, samples/proc/BLDCIDB2.prc:109, samples/proc/BLDCIDB2.prc:114, samples/proc/BLDCIDB2.prc:135-153 |
| UP-BR-029 | Rebind the application plan over packages | design note | WHEN the package bind ended with return code 4 or less, THE CICS-Db2 build job SHALL bind the application plan (PLAN, 'CARDDEMO' in the sample job) over package list 'CARDDEMO.*' with qualifier 'CARDDEMO', action 'REPLACE' keeping existing authorizations ('RETAIN'), isolation 'CS', current data 'YES' and encoding 'EBCDIC'. | medium | samples/proc/BLDCIDB2.prc:109, samples/proc/BLDCIDB2.prc:114, samples/proc/BLDCIDB2.prc:135, samples/proc/BLDCIDB2.prc:158-176 |
| UP-BR-030 | Rebind the application plan over packages | error handling | WHEN the package bind did not run because the link-edit failed, THE CICS-Db2 build job SHALL still run the plan bind, because a return-code test on a step that did not run is ignored. | medium | samples/proc/BLDCIDB2.prc:109, samples/proc/BLDCIDB2.prc:114, samples/proc/BLDCIDB2.prc:135, samples/proc/BLDCIDB2.prc:158-176 |

### Key entities

None found in the source.

### Needs clarification

- DEF-142: Is this intended? The bind step loads its Db2 libraries from the fixed names OEM.DB2.DAZ1.SDSNEXIT and OEMA.DB2.VERSIONA.SDSNLOAD. It ignores the SSID and SDSNLOAD settings the procedure takes, so a build against any subsystem other than DAZ1 still uses DAZ1's libraries. (Subject-matter expert) On UP-BR-028.
- DEF-147: Is this intended? BINDPL tests only BINDPK's return code. When the link-edit fails inside the IF RC = 0 block, BINDPK is bypassed and its test is ignored, so the plan is rebound even though the build failed. (Subject-matter expert) On UP-BR-030.

### Decision table gaps

- CICS-Db2 build bind steps: No rule states whether the plan bind is skipped or run when the package bind fails.
- CICS-Db2 build bind steps: No rule states whether the plan bind runs when an earlier step than link-edit fails.
