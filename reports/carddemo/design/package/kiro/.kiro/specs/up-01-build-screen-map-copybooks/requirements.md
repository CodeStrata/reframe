# Requirements: Build screen map copybooks (UP-C01)

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
