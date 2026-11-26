# Requirements: Customise installation members with site values (UP-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as service · risk low

## Introduction

Tailors the installation members to one site before the application is installed: every placeholder in each member is replaced with the value the installer set for that site, such as the Db2 subsystem, the CICSPlex SM address space and Web User Interface identifiers, and the Language Environment library qualifier. It serves the installer or platform team setting up an environment, so nobody has to edit members by hand. It must never leave a placeholder unreplaced, and never put a different setting's value in its place. One trap to keep: '<PDSLOAD>' gets the Workload Simulator qualifier, not the GenApp load library name.

**User story:** As an installer, I want the installation customisation edit macro to replace the placeholders in each installation member with the values I set, so that the members are tailored to my site's subsystems and libraries without manual editing.

## Requirements

### Requirement 1: UP-REQ-F-096 (historical artifact)

#### Acceptance criteria

1. When an installation member is customised, the system shall replace every occurrence of '<PDSLOAD>' with the Workload Simulator product qualifier (WSIMHLQ, shipped as 'PP.WSIM.V110'), not with the GenApp load library name. (rules UP-BR-121)
2. GIVEN member line: DSN=<PDSLOAD>; WSIMHLQ: PP.WSIM.V110 WHEN an installation member is customised THEN The customised copy contains DSN=PP.WSIM.V110, not userid.GENAPP.LOAD. (UP-C13-AC-01; UP-BR-121)

### Requirement 2: UP-REQ-F-097 (design note)

#### Acceptance criteria

1. When an installation member is customised, the system shall replace every occurrence of '<WUISYSID>' with the CICSPlex SM Web User Interface system identifier the installer set (WUISYSID, shipped as 'IWUI'). (rules UP-BR-122)
2. GIVEN member line: SYSIDNT=<WUISYSID>; WUISYSID: IWUI WHEN an installation member is customised THEN The customised copy of the member contains SYSIDNT=IWUI. (UP-C13-AC-02; UP-BR-122)

### Requirement 3: UP-REQ-F-098 (design note)

#### Acceptance criteria

1. When an installation member is customised, the system shall replace every occurrence of '<DB2SSID>' with the Db2 subsystem identifier the installer set (DB2SSID, shipped as 'DKM1'). (rules UP-BR-123)
2. GIVEN member line: DSN SYSTEM(<DB2SSID>); DB2SSID: DKM1 WHEN an installation member is customised THEN The customised copy contains DSN SYSTEM(DKM1). (UP-C13-AC-03; UP-BR-123)
3. GIVEN member line: no '<DB2SSID>' in the member WHEN an installation member is customised THEN The member's text is not changed by this substitution. (UP-C13-AC-04; UP-BR-123)

### Requirement 4: UP-REQ-F-099 (design note)

#### Acceptance criteria

1. When an installation member is customised, the system shall replace every occurrence of '<CMASYSID>' with the CICSPlex SM address space (CMAS) system identifier the installer set (CMASYSID, shipped as 'ICMA'). (rules UP-BR-124)
2. GIVEN member line: SYSIDNT=<CMASYSID>; CMASYSID: ICMA WHEN an installation member is customised THEN The customised copy of the member contains SYSIDNT=ICMA. (UP-C13-AC-05; UP-BR-124)

### Requirement 5: UP-REQ-F-100 (design note)

#### Acceptance criteria

1. When an installation member is customised, the system shall replace every occurrence of '<CEEHLQ>' with the Language Environment runtime library qualifier the installer set (CEEHLQ, shipped as 'CEE'). (rules UP-BR-125)
2. GIVEN member line: DSN=<CEEHLQ>.SCEERUN; CEEHLQ: CEE WHEN an installation member is customised THEN The customised copy contains DSN=CEE.SCEERUN. (UP-C13-AC-06; UP-BR-125)
