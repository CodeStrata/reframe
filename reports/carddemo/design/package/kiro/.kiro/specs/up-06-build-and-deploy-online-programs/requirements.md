# Requirements: Build and deploy online programs (UP-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk high

## Introduction

The build-and-deploy steps for online programs: compile, register the program's database access, and make the online system load the new version. Build engineers use it. It must never deploy or bind a program whose build failed, and online users must pick up the new version only after a successful build.

**User story:** As a CardDemo build engineer, I want online programs compiled, bound to the database and refreshed in the online region, so that online users run the newly built code.

## Requirements

### Requirement 1: UP-REQ-F-025 (design note)

#### Acceptance criteria

1. When the program compile step of the sample online build job ends with return code 4 or lower, the system shall send the online region (CICSAWSA) the console command 'CEMT SET PROG(CICSPGMN) NEWCOPY' so that the newly built program is loaded for online users. (rules UP-BR-027)
2. GIVEN compile step return code: 4 WHEN the program compile step of the sample online build job ends with return code 4 or lower THEN The NEWCOPY step runs and the region loads the new copy of program CICSPGMN. (UP-C06-AC-01; UP-BR-027)
3. GIVEN compile step return code: 8 WHEN the program compile step of the sample online build job ends with return code 4 or lower THEN The NEWCOPY step is bypassed; the online region keeps running the old copy. (UP-C06-AC-02; UP-BR-027)

### Requirement 2: UP-REQ-F-026 (design note)

#### Acceptance criteria

1. When the Db2 precompile, CICS translation, COBOL compile and link-edit steps have all ended with return code 0, the system shall bind the program's database request module into package collection 'CARDDEMO' with qualifier 'CARDDEMO', action 'REPLACE', isolation 'CS', current data 'YES', explain 'NO' and encoding 'EBCDIC'. (rules UP-BR-028)
2. GIVEN program name (MEMNAME): CICSDB2P; return code of every earlier build step: 0 WHEN the Db2 precompile, CICS translation, COBOL compile and link-edit steps have all ended with return code 0 THEN Package CARDDEMO.CICSDB2P is bound with qualifier 'CARDDEMO' and replaces any earlier version of that package (UP-C06-AC-03; UP-BR-028)
3. GIVEN COBOL compile return code: 8 WHEN the Db2 precompile, CICS translation, COBOL compile and link-edit steps have all ended with return code 0 THEN The package bind step does not run (UP-C06-AC-04; UP-BR-028)

### Requirement 3: UP-REQ-F-027 (design note)

#### Acceptance criteria

1. When the package bind ended with return code 4 or less, the system shall bind the application plan ('CARDDEMO' in the sample job) over package list 'CARDDEMO.*' with qualifier 'CARDDEMO', action 'REPLACE' keeping existing authorizations ('RETAIN'), isolation 'CS', current data 'YES' and encoding 'EBCDIC'. (rules UP-BR-029)
2. GIVEN package bind return code: 4; plan: CARDDEMO WHEN the package bind ended with return code 4 or less THEN Plan CARDDEMO is rebound over every package in collection CARDDEMO and keeps its existing grants (UP-C06-AC-05; UP-BR-029)
3. GIVEN package bind return code: 8 WHEN the package bind ended with return code 4 or less THEN The plan bind is skipped (UP-C06-AC-06; UP-BR-029)

### Requirement 4: UP-REQ-F-028 (error handling)

#### Acceptance criteria

1. If the package bind did not run because the link-edit failed, then the system shall still run the plan bind, because a return-code test on a step that did not run is ignored. (rules UP-BR-030)
2. GIVEN link-edit return code: 8; package bind: skipped WHEN the package bind did not run because the link-edit failed THEN The plan bind still runs over the existing packages in CARDDEMO (UP-C06-AC-07; UP-BR-030)
