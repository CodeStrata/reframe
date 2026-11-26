# Design: Build and deploy online programs (UP-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

The build-and-deploy steps for online programs: compile, register the program's database access, and make the online system load the new version. Build engineers use it. It must never deploy or bind a program whose build failed, and online users must pick up the new version only after a successful build.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-027 | Refresh the program in the online region | design note | WHEN the program compile step of the sample online build job ends with return code 4 or lower, THE Online Program Deployment SHALL send the online region (CICSAWSA) the console command 'CEMT SET PROG(CICSPGMN) NEWCOPY' so the newly built program is loaded for online users. | medium | samples/jcl/CICCMP.jcl:32-33, samples/jcl/CICCMP.jcl:41, samples/jcl/CICCMP.jcl:45-50 |
| UP-BR-028 | Bind the CardDemo database package | design note | WHEN the Db2 precompile, CICS translation, COBOL compile and link-edit steps have all ended with return code 0, THE CICS-Db2 build job SHALL bind the program's database request module into package collection 'CARDDEMO' with qualifier 'CARDDEMO', action 'REPLACE', isolation 'CS', current data 'YES', explain 'NO' and encoding 'EBCDIC'. | medium | samples/proc/BLDCIDB2.prc:80-81, samples/proc/BLDCIDB2.prc:109, samples/proc/BLDCIDB2.prc:114, samples/proc/BLDCIDB2.prc:135-153 |
| UP-BR-029 | Rebind the application plan over packages | design note | WHEN the package bind ended with return code 4 or less, THE CICS-Db2 build job SHALL bind the application plan (PLAN, 'CARDDEMO' in the sample job) over package list 'CARDDEMO.*' with qualifier 'CARDDEMO', action 'REPLACE' keeping existing authorizations ('RETAIN'), isolation 'CS', current data 'YES' and encoding 'EBCDIC'. | medium | samples/proc/BLDCIDB2.prc:109, samples/proc/BLDCIDB2.prc:114, samples/proc/BLDCIDB2.prc:135, samples/proc/BLDCIDB2.prc:158-176 |
| UP-BR-030 | Rebind the application plan over packages | error handling | WHEN the package bind did not run because the link-edit failed, THE CICS-Db2 build job SHALL still run the plan bind, because a return-code test on a step that did not run is ignored. | medium | samples/proc/BLDCIDB2.prc:109, samples/proc/BLDCIDB2.prc:114, samples/proc/BLDCIDB2.prc:135, samples/proc/BLDCIDB2.prc:158-176 |

### Worked examples

- UP-BR-027: compile step return code = 4 → The NEWCOPY step runs and the region loads the new copy of program CICSPGMN.
- UP-BR-027: compile step return code = 8 → The NEWCOPY step is bypassed; the online region keeps running the old copy.
- UP-BR-028: program name (MEMNAME) = CICSDB2P; return code of every earlier build step = 0 → Package CARDDEMO.CICSDB2P is bound with qualifier 'CARDDEMO' and replaces any earlier version of that package
- UP-BR-028: COBOL compile return code = 8 → The package bind step does not run
- UP-BR-029: package bind return code = 4; plan = CARDDEMO → Plan CARDDEMO is rebound over every package in collection CARDDEMO and keeps its existing grants
- UP-BR-029: package bind return code = 8 → The plan bind is skipped
- UP-BR-030: link-edit return code = 8; package bind = skipped → The plan bind still runs over the existing packages in CARDDEMO

## Decision tables

#### CICS-Db2 build bind steps

| Precompile, translation, compile and link-edit result | Package bind result | Bind action | Rule |
|---|---|---|---|
| all return code 0 | not yet run | Bind package into collection 'CARDDEMO' | UP-BR-028 |
| all return code 0 | return code 4 or less | Bind application plan over 'CARDDEMO.*' keeping authorizations ('RETAIN') | UP-BR-029 |
| link-edit failed | did not run | Plan bind still runs | UP-BR-030 |
| all return code 0 | return code above 4 | **Gap:** No rule states whether the plan bind is skipped or run when the package bind fails. | |
| precompile, translation or compile failed | did not run | **Gap:** No rule states whether the plan bind runs when an earlier step than link-edit fails. | |


## Design notes

- UP-BR-027: A CI/CD deploy step. When the build succeeds (warnings allowed, no errors), roll out the new version to the running online service, for example by a rolling restart or a hot reload, so new requests use the new code.
- UP-BR-028: Run this only when every build step succeeded without warnings. It registers or refreshes the program's database access against the CARDDEMO schema, replacing the previous version, using read-committed isolation. In a modern stack this is usually a schema migration or a step that grants database permissions, gated on a green build.
- UP-BR-029: After the database access step succeeds (warnings allowed), refresh the application-level database binding that covers all CARDDEMO programs. Keep the existing permissions and use the same CARDDEMO schema and isolation. In a modern stack this is the deploy-time database configuration or role setup, and it must not reset grants.

## Open questions

- DEF-142: Is this intended? The bind step loads its Db2 libraries from the fixed names OEM.DB2.DAZ1.SDSNEXIT and OEMA.DB2.VERSIONA.SDSNLOAD. It ignores the SSID and SDSNLOAD settings the procedure takes, so a build against any subsystem other than DAZ1 still uses DAZ1's libraries. (Subject-matter expert) On UP-BR-028.
- DEF-147: Is this intended? BINDPL tests only BINDPK's return code. When the link-edit fails inside the IF RC = 0 block, BINDPK is bypassed and its test is ignored, so the plan is rebound even though the build failed. (Subject-matter expert) On UP-BR-030.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).