# Customise installation members with site values (UP-C13)

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

## Screens and components

No screens: it runs as service.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-121 | Replace load-library placeholder with qualifier | historical artifact | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<PDSLOAD>' with the Workload Simulator product qualifier (WSIMHLQ, shipped as 'PP.WSIM.V110'), not with the GenApp load library name; no shipped member contains this placeholder. | medium | base/exec/mac1.rexx:13, base/exec/mac1.rexx:43, base/exec/cust1.rexx:21, base/exec/cust1.rexx:50 |
| UP-BR-122 | Replace wui system identifier placeholder | design note | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<WUISYSID>' with the CICSPlex SM Web User Interface system identifier the installer set (WUISYSID, shipped as 'IWUI'). | medium | base/exec/mac1.rexx:12, base/exec/mac1.rexx:39, base/exec/cust1.rexx:32, base/exec/cust1.rexx:38 |
| UP-BR-123 | Substitute subsystem placeholder in member | design note | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<DB2SSID>' with the Db2 subsystem identifier the installer set (DB2SSID, shipped as 'DKM1'). | medium | base/exec/mac1.rexx:10, base/exec/mac1.rexx:26, base/exec/cust1.rexx:17, base/exec/cust1.rexx:36 |
| UP-BR-124 | Substitute cmas system identifier placeholder | design note | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<CMASYSID>' with the CICSPlex SM address space (CMAS) system identifier the installer set (CMASYSID, shipped as 'ICMA'). | medium | base/exec/mac1.rexx:12, base/exec/mac1.rexx:37, base/exec/cust1.rexx:30, base/exec/cust1.rexx:38 |
| UP-BR-125 | Replace runtime qualifier placeholders | design note | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<CEEHLQ>' with the Language Environment runtime library qualifier the installer set (CEEHLQ, shipped as 'CEE'). | medium | base/exec/mac1.rexx:9, base/exec/mac1.rexx:22, base/exec/cust1.rexx:13, base/exec/cust1.rexx:35 |

### Worked examples

- UP-BR-121: member line = DSN=<PDSLOAD>; WSIMHLQ = PP.WSIM.V110 → The customised copy contains DSN=PP.WSIM.V110, not userid.GENAPP.LOAD.
- UP-BR-122: member line = SYSIDNT=<WUISYSID>; WUISYSID = IWUI → The customised copy of the member contains SYSIDNT=IWUI.
- UP-BR-123: member line = DSN SYSTEM(<DB2SSID>); DB2SSID = DKM1 → The customised copy contains DSN SYSTEM(DKM1).
- UP-BR-123: member line = no '<DB2SSID>' in the member → The member's text is not changed by this substitution.
- UP-BR-124: member line = SYSIDNT=<CMASYSID>; CMASYSID = ICMA → The customised copy of the member contains SYSIDNT=ICMA.
- UP-BR-125: member line = DSN=<CEEHLQ>.SCEERUN; CEEHLQ = CEE → The customised copy contains DSN=CEE.SCEERUN.

## Decision tables

#### Placeholder substitution when an installation member is customised

| Placeholder found in member | Value that replaces every occurrence | Rule |
|---|---|---|
| <PDSLOAD> | Workload Simulator product qualifier WSIMHLQ (shipped as 'PP.WSIM.V110'), not the GenApp load library name; no shipped member contains this placeholder | UP-BR-121 |
| <WUISYSID> | CICSPlex SM Web User Interface system identifier WUISYSID (shipped as 'IWUI') | UP-BR-122 |
| <DB2SSID> | Db2 subsystem identifier DB2SSID (shipped as 'DKM1') | UP-BR-123 |
| <CMASYSID> | CICSPlex SM address space (CMAS) system identifier CMASYSID (shipped as 'ICMA') | UP-BR-124 |
| <CEEHLQ> | Language Environment runtime library qualifier CEEHLQ (shipped as 'CEE') | UP-BR-125 |
| any other placeholder | **Gap:** No rule says what happens to a placeholder in a member that is not one of these five; confirm whether it is left unchanged or must be substituted. | |
| <PDSLOAD> | **Gap:** R1 maps '<PDSLOAD>' to the Workload Simulator qualifier rather than the GenApp load library, and no shipped member contains it; confirm whether this substitution is still needed. | |


## Design notes

- UP-BR-122: The CICSPlex SM Web User Interface system identifier becomes a per-environment deployment setting (default 'IWUI'). The deployment templating step fills every '<WUISYSID>' in the configuration and install templates with it. The step fails if the setting is missing, so no template is left with the placeholder.
- UP-BR-123: The Db2 subsystem identifier becomes a per-environment setting (default 'DKM1'), and the same templating step fills every '<DB2SSID>' with it. In the new application this is the database connection target in environment configuration. It must not be hard-coded in any member or in code.
- UP-BR-124: The CICSPlex SM address space (CMAS) system identifier becomes a per-environment setting (default 'ICMA'). The templating step fills every '<CMASYSID>' with it. It is only needed while the target environment still runs CICSPlex SM; if the new platform has no CMAS, the setting and its placeholder can be dropped.
- UP-BR-125: The Language Environment runtime library qualifier becomes a per-environment setting (default 'CEE'). The templating step fills every '<CEEHLQ>' with it. On a non-mainframe runtime this maps to the location of the runtime libraries, or it is not needed at all.

## Open questions

- DEF-049: Is this intended? '<PDSLOAD>' is replaced with the Workload Simulator qualifier WSIMHLQ, not with the GenApp load library that CUST1 builds and passes (PDSLOAD, for example 'userid.GENAPP.LOAD'). This is part of the same pattern as the other PDS*/WSIM* placeholders in MAC1 lines 41-46. No shipped member uses the placeholder today. (Subject-matter expert) On UP-BR-121.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).
