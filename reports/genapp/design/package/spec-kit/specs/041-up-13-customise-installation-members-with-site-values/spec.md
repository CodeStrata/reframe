# Feature specification: Customise installation members with site values

**Feature:** UP-C13 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C13)

As an installer, I want the installation customisation edit macro to replace the placeholders in each installation member with the values I set, so that the members are tailored to my site's subsystems and libraries without manual editing.

Tailors the installation members to one site before the application is installed: every placeholder in each member is replaced with the value the installer set for that site, such as the Db2 subsystem, the CICSPlex SM address space and Web User Interface identifiers, and the Language Environment library qualifier. It serves the installer or platform team setting up an environment, so nobody has to edit members by hand. It must never leave a placeholder unreplaced, and never put a different setting's value in its place. One trap to keep: '<PDSLOAD>' gets the Workload Simulator qualifier, not the GenApp load library name.

**Acceptance scenarios:**

1. **Given** member line: DSN=<PDSLOAD>; WSIMHLQ: PP.WSIM.V110, **when** an installation member is customised, **then** The customised copy contains DSN=PP.WSIM.V110, not userid.GENAPP.LOAD. (UP-C13-AC-01)
2. **Given** member line: SYSIDNT=<WUISYSID>; WUISYSID: IWUI, **when** an installation member is customised, **then** The customised copy of the member contains SYSIDNT=IWUI. (UP-C13-AC-02)
3. **Given** member line: DSN SYSTEM(<DB2SSID>); DB2SSID: DKM1, **when** an installation member is customised, **then** The customised copy contains DSN SYSTEM(DKM1). (UP-C13-AC-03)
4. **Given** member line: no '<DB2SSID>' in the member, **when** an installation member is customised, **then** The member's text is not changed by this substitution. (UP-C13-AC-04)
5. **Given** member line: SYSIDNT=<CMASYSID>; CMASYSID: ICMA, **when** an installation member is customised, **then** The customised copy of the member contains SYSIDNT=ICMA. (UP-C13-AC-05)
6. **Given** member line: DSN=<CEEHLQ>.SCEERUN; CEEHLQ: CEE, **when** an installation member is customised, **then** The customised copy contains DSN=CEE.SCEERUN. (UP-C13-AC-06)

## Requirements

### Functional requirements

- **UP-REQ-F-096** (historical artifact): When an installation member is customised, the system shall replace every occurrence of '<PDSLOAD>' with the Workload Simulator product qualifier (WSIMHLQ, shipped as 'PP.WSIM.V110'), not with the GenApp load library name. Rules: UP-BR-121.
- **UP-REQ-F-097** (design note): When an installation member is customised, the system shall replace every occurrence of '<WUISYSID>' with the CICSPlex SM Web User Interface system identifier the installer set (WUISYSID, shipped as 'IWUI'). Rules: UP-BR-122.
- **UP-REQ-F-098** (design note): When an installation member is customised, the system shall replace every occurrence of '<DB2SSID>' with the Db2 subsystem identifier the installer set (DB2SSID, shipped as 'DKM1'). Rules: UP-BR-123.
- **UP-REQ-F-099** (design note): When an installation member is customised, the system shall replace every occurrence of '<CMASYSID>' with the CICSPlex SM address space (CMAS) system identifier the installer set (CMASYSID, shipped as 'ICMA'). Rules: UP-BR-124.
- **UP-REQ-F-100** (design note): When an installation member is customised, the system shall replace every occurrence of '<CEEHLQ>' with the Language Environment runtime library qualifier the installer set (CEEHLQ, shipped as 'CEE'). Rules: UP-BR-125.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-121 | Replace load-library placeholder with qualifier | historical artifact | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<PDSLOAD>' with the Workload Simulator product qualifier (WSIMHLQ, shipped as 'PP.WSIM.V110'), not with the GenApp load library name; no shipped member contains this placeholder. | medium | base/exec/mac1.rexx:13, base/exec/mac1.rexx:43, base/exec/cust1.rexx:21, base/exec/cust1.rexx:50 |
| UP-BR-122 | Replace wui system identifier placeholder | design note | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<WUISYSID>' with the CICSPlex SM Web User Interface system identifier the installer set (WUISYSID, shipped as 'IWUI'). | medium | base/exec/mac1.rexx:12, base/exec/mac1.rexx:39, base/exec/cust1.rexx:32, base/exec/cust1.rexx:38 |
| UP-BR-123 | Substitute subsystem placeholder in member | design note | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<DB2SSID>' with the Db2 subsystem identifier the installer set (DB2SSID, shipped as 'DKM1'). | medium | base/exec/mac1.rexx:10, base/exec/mac1.rexx:26, base/exec/cust1.rexx:17, base/exec/cust1.rexx:36 |
| UP-BR-124 | Substitute cmas system identifier placeholder | design note | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<CMASYSID>' with the CICSPlex SM address space (CMAS) system identifier the installer set (CMASYSID, shipped as 'ICMA'). | medium | base/exec/mac1.rexx:12, base/exec/mac1.rexx:37, base/exec/cust1.rexx:30, base/exec/cust1.rexx:38 |
| UP-BR-125 | Replace runtime qualifier placeholders | design note | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<CEEHLQ>' with the Language Environment runtime library qualifier the installer set (CEEHLQ, shipped as 'CEE'). | medium | base/exec/mac1.rexx:9, base/exec/mac1.rexx:22, base/exec/cust1.rexx:13, base/exec/cust1.rexx:35 |

### Key entities

None found in the source.

### Needs clarification

- DEF-049: Is this intended? '<PDSLOAD>' is replaced with the Workload Simulator qualifier WSIMHLQ, not with the GenApp load library that CUST1 builds and passes (PDSLOAD, for example 'userid.GENAPP.LOAD'). This is part of the same pattern as the other PDS*/WSIM* placeholders in MAC1 lines 41-46. No shipped member uses the placeholder today. (Subject-matter expert) On UP-BR-121.

### Decision table gaps

- Placeholder substitution when an installation member is customised: No rule says what happens to a placeholder in a member that is not one of these five; confirm whether it is left unchanged or must be substituted.
- Placeholder substitution when an installation member is customised: R1 maps '<PDSLOAD>' to the Workload Simulator qualifier rather than the GenApp load library, and no shipped member contains it; confirm whether this substitution is still needed.
