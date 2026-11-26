# Requirements: Prepare monitoring and workload simulation (ADPLM-C06)

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
