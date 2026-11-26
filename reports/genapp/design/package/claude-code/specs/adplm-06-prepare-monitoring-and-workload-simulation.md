# Prepare monitoring and workload simulation (ADPLM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk low

## Introduction

Prepares the monitoring console's data store and runs a scripted workload against the insurance application. Administrators use it to watch the environment and exercise it under load. Monitoring set-up must be skipped if an earlier set-up step failed badly, and the load run must not turn on its own automatic logging.

**User story:** As an application administrator, I want the WUI server repository initialised and the GENAPP workload simulation runnable, so that the environment can be monitored and exercised under load.

## Requirements

### Requirement 1: ADPLM-REQ-F-034 (design note)

#### Acceptance criteria

1. When no earlier step of the repository set-up job ended with a return code above 8, the system shall run EYU9XDUT against the new WUI data repository (EYUDREP) with 'CMASNAME=<CMASAPPL>', 'DAYLIGHT=N', 'TIMEZONE=B', 'SYSID=<CMASYSID>', 'ZONEOFFSET=0' and WUIAPPLID, WUINAME and WUISYSID values, printing a report. (rules ADPLM-BR-036)
2. GIVEN highest earlier step return code: 0 WHEN no earlier step of the repository set-up job ended with a return code above 8 THEN EYU9XDUT initialises the repository with the given CMAS and WUI identities and prints its report. (ADPLM-C06-AC-01; ADPLM-BR-036)
3. GIVEN highest earlier step return code: 12 WHEN no earlier step of the repository set-up job ended with a return code above 8 THEN The initialisation step is skipped. (ADPLM-C06-AC-02; ADPLM-BR-036)

### Requirement 2: ADPLM-REQ-F-035 (design note)

#### Acceptance criteria

1. If an earlier step of the repository set-up job ended with a return code above 8, then the system shall skip the WUI repository initialisation step. (rules ADPLM-BR-036)
2. GIVEN highest earlier step return code: 0 WHEN no earlier step of the repository set-up job ended with a return code above 8 THEN EYU9XDUT initialises the repository with the given CMAS and WUI identities and prints its report. (ADPLM-C06-AC-01; ADPLM-BR-036)
3. GIVEN highest earlier step return code: 12 WHEN no earlier step of the repository set-up job ended with a return code above 8 THEN The initialisation step is skipped. (ADPLM-C06-AC-02; ADPLM-BR-036)

### Requirement 3: ADPLM-REQ-F-036 (design note)

#### Acceptance criteria

1. The system shall run the workload simulator (ITPENTER) with parameter 'NTWRK=GENAPP', reading initialisation definitions, the concatenated message definitions and the simulation log data set in shared mode, with automatic logging turned off (AUTOLOG dummy) and dumps and printed output sent to the job output. (rules ADPLM-BR-037)
2. GIVEN job: GENAWSIM submitted WHEN Network Workload Simulation Run runs THEN ITPENTER runs the 'GENAPP' network simulation using the INITDD, MSGDD and LOGDD data sets; output goes to SYSPRINT and SYSUDUMP. (ADPLM-C06-AC-03; ADPLM-BR-037)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-036 | Initialize the WUI server repository | design note | WHEN no earlier step of the repository set-up job ended with a return code above 8, THE WUI Server Repository Initialization SHALL run EYU9XDUT against the new WUI data repository (EYUDREP) with 'CMASNAME=<CMASAPPL>', 'DAYLIGHT=N', 'TIMEZONE=B', 'SYSID=<CMASYSID>', 'ZONEOFFSET=0' and WUIAPPLID, WUINAME and WUISYSID values, printing a report; otherwise it SHALL skip the step. | medium | base/cntl/defdrep.jcl:9-15, base/cntl/defdrep.jcl:19-34, base/cntl/defdrep.jcl:37-51 |
| ADPLM-BR-037 | Run workload simulation for GENAPP network | design note | THE Network Workload Simulation Run SHALL run the workload simulator (ITPENTER) with parameter 'NTWRK=GENAPP', reading initialisation definitions, the concatenated message definitions and the simulation log data set in shared mode, with automatic logging turned off (AUTOLOG dummy) and dumps and printed output sent to the job output. | medium | base/cntl/itpentr.jcl:1-14 |

### Worked examples

- ADPLM-BR-036: highest earlier step return code = 0 → EYU9XDUT initialises the repository with the given CMAS and WUI identities and prints its report.
- ADPLM-BR-036: highest earlier step return code = 12 → The initialisation step is skipped.
- ADPLM-BR-037: job = GENAWSIM submitted → ITPENTER runs the 'GENAPP' network simulation using the INITDD, MSGDD and LOGDD data sets; output goes to SYSPRINT and SYSUDUMP.

## Decision tables

None.

## Design notes

- ADPLM-BR-036: An environment set-up step that initialises the monitoring console's repository with the console and system names and identifiers, daylight saving off, the time zone setting 'B' and a zone offset of 0, and prints a report. In the new application this is provisioning of the monitoring or observability tooling. It runs only when no earlier set-up step failed with a severity above 8.
- ADPLM-BR-037: An on-demand load-test job that plays the GENAPP scripted scenarios (initialisation definitions plus message scripts) against the application, with the tool's own automatic logging off and its results and diagnostics sent to the job output. In the new application, use a load-testing tool with the scenario scripts kept in version control.

## Open questions

- SME-016: The initialization step is described as setting up the web user interface repository, but the file it uses is the CMAS repository file. Which repository should the new system set up? (CICS/CPSM platform team) On ADPLM-BR-036.
- SME-017: The job removes and then recreates the repository before setting it up, but no business rule covers those steps or what happens if they fail. Should removing and recreating the repository be requirements of this process? (CICS/CPSM platform team) On ADPLM-BR-036.
- SME-018: What must the printed initialization report contain, and who uses it? (Batch operations) On ADPLM-BR-036.
- SME-019: The source code of the workload simulation program is not available. What does the simulation do with its initialization definitions, message definitions and log data set, and what does it produce? (Application owner / performance testing team) On ADPLM-BR-037.
- SME-020: Which data stores provide the workload simulation's initialization definitions, message set, definitions set and log data set? The likely candidates are the simulator message file, the script library file and the simulator log file. (Batch operations) On ADPLM-BR-037.
- SME-021: Does the new system need this workload simulation run, or is it a test activity that modern load-testing tools can replace? (Modernization lead) On ADPLM-BR-037.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).
