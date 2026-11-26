# Build screen map copybooks (UP-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk low

## Introduction

Turns each screen definition into a shared field-layout definition that the programs serving that screen use, and keeps a build listing for it. It is a developer build step, not a business function. It must always regenerate the layout from the current screen source, so a program and its screen never disagree on fields.

**User story:** As a CardDemo developer, I want each screen map's symbolic map generated into the copybook library, so that programs can use the screen's field layout.

## Requirements

### Requirement 1: UP-REQ-F-001 (design note)

#### Acceptance criteria

1. When a screen map is built, the system shall, in its symbolic-map step (DSECT), assemble the staged copy of the map source (&&TEMPM) with the parameter 'SYSPARM(DSECT),DECK,NOLOAD' using the CICS, SYS1.MACLIB and CEE.SCEEMAC macro libraries and produce no object module. (rules UP-BR-001)
2. GIVEN MAPNAME: CICSMAP; HLQ: AWS.M2 WHEN a screen map is built THEN The map source AWS.M2.CARDDEMO.BMS(CICSMAP), staged in the temporary copy, is assembled in DSECT mode and no load module is produced by this step. (UP-C01-AC-01; UP-BR-001)

### Requirement 2: UP-REQ-F-002 (design note)

#### Acceptance criteria

1. The system shall write the generated symbolic map as fixed-length 80-byte records, with exclusive access, to the map's member in the copybook library (&CPYBKS(&MAPNAME)) and write the assembler listing to the map's member in the listing library (&LISTING(&MAPNAME)). (rules UP-BR-002)
2. GIVEN MAPNAME: CICSMAP; HLQ: AWS.M2 WHEN Screen Map Build runs THEN The copybook AWS.M2.CARDDEMO.CPY(CICSMAP) is replaced with 80-byte records and the listing goes to AWS.M2.CARDDEMO.LST(CICSMAP). (UP-C01-AC-02; UP-BR-002)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-001 | Generate the symbolic map copybook | design note | WHEN a screen map is built, THE Screen Map Build SHALL, in its symbolic-map step (DSECT), assemble the staged copy of the map source (&&TEMPM) with the parameter 'SYSPARM(DSECT),DECK,NOLOAD' using the CICS, SYS1.MACLIB and CEE.SCEEMAC macro libraries, and produce no object module. | medium | samples/proc/BUILDBMS.prc:23-29, samples/proc/BUILDBMS.prc:36-43, samples/proc/BUILDBMS.prc:78-92 |
| UP-BR-002 | Generate the symbolic map copybook | design note | THE Screen Map Build SHALL write the generated symbolic map as fixed-length 80-byte records, with exclusive access, to the map's member in the copybook library (&CPYBKS(&MAPNAME)), and write the assembler listing to the map's member in the listing library (&LISTING(&MAPNAME)). | medium | samples/proc/BUILDBMS.prc:23-29, samples/proc/BUILDBMS.prc:36-43, samples/proc/BUILDBMS.prc:78-92 |

### Worked examples

- UP-BR-001: MAPNAME = CICSMAP; HLQ = AWS.M2 → The map source AWS.M2.CARDDEMO.BMS(CICSMAP), staged in the temporary copy, is assembled in DSECT mode and no load module is produced by this step.
- UP-BR-002: MAPNAME = CICSMAP; HLQ = AWS.M2 → The copybook AWS.M2.CARDDEMO.CPY(CICSMAP) is replaced with 80-byte records and the listing goes to AWS.M2.CARDDEMO.LST(CICSMAP).

## Decision tables

None.

## Design notes

- UP-BR-001: A build-pipeline step that generates the screen's field-layout (view model / DTO) definition from the screen source. It produces only that definition, not an executable artefact. In the new stack this belongs in the UI build or code generation, not in a runtime job.
- UP-BR-002: Write the generated layout to the shared source location under the screen's name, replacing the previous version atomically so nothing else writes it at the same time. Keep the build log or listing as a build artefact named after the screen.

## Open questions

None.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).
