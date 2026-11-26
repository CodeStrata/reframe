# Implementation plan: Customise installation members with site values (UP-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as service.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as service.

## Data model

None found in the source.

## Design notes

- UP-BR-122: The CICSPlex SM Web User Interface system identifier becomes a per-environment deployment setting (default 'IWUI'). The deployment templating step fills every '<WUISYSID>' in the configuration and install templates with it. The step fails if the setting is missing, so no template is left with the placeholder.
- UP-BR-123: The Db2 subsystem identifier becomes a per-environment setting (default 'DKM1'), and the same templating step fills every '<DB2SSID>' with it. In the new application this is the database connection target in environment configuration. It must not be hard-coded in any member or in code.
- UP-BR-124: The CICSPlex SM address space (CMAS) system identifier becomes a per-environment setting (default 'ICMA'). The templating step fills every '<CMASYSID>' with it. It is only needed while the target environment still runs CICSPlex SM; if the new platform has no CMAS, the setting and its placeholder can be dropped.
- UP-BR-125: The Language Environment runtime library qualifier becomes a per-environment setting (default 'CEE'). The templating step fills every '<CEEHLQ>' with it. On a non-mainframe runtime this maps to the location of the runtime libraries, or it is not needed at all.

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

