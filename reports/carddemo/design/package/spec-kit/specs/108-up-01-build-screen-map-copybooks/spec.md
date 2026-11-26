# Feature specification: Build screen map copybooks

**Feature:** UP-C01 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C01)

As a CardDemo developer, I want each screen map's symbolic map generated into the copybook library, so that programs can use the screen's field layout.

Turns each screen definition into a shared field-layout definition that the programs serving that screen use, and keeps a build listing for it. It is a developer build step, not a business function. It must always regenerate the layout from the current screen source, so a program and its screen never disagree on fields.

**Acceptance scenarios:**

1. **Given** MAPNAME: CICSMAP; HLQ: AWS.M2, **when** a screen map is built, **then** The map source AWS.M2.CARDDEMO.BMS(CICSMAP), staged in the temporary copy, is assembled in DSECT mode and no load module is produced by this step. (UP-C01-AC-01)
2. **Given** MAPNAME: CICSMAP; HLQ: AWS.M2, **when** Screen Map Build runs, **then** The copybook AWS.M2.CARDDEMO.CPY(CICSMAP) is replaced with 80-byte records and the listing goes to AWS.M2.CARDDEMO.LST(CICSMAP). (UP-C01-AC-02)

## Requirements

### Functional requirements

- **UP-REQ-F-001** (design note): When a screen map is built, the system shall, in its symbolic-map step (DSECT), assemble the staged copy of the map source (&&TEMPM) with the parameter 'SYSPARM(DSECT),DECK,NOLOAD' using the CICS, SYS1.MACLIB and CEE.SCEEMAC macro libraries and produce no object module. Rules: UP-BR-001.
- **UP-REQ-F-002** (design note): The system shall write the generated symbolic map as fixed-length 80-byte records, with exclusive access, to the map's member in the copybook library (&CPYBKS(&MAPNAME)) and write the assembler listing to the map's member in the listing library (&LISTING(&MAPNAME)). Rules: UP-BR-002.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-001 | Generate the symbolic map copybook | design note | WHEN a screen map is built, THE Screen Map Build SHALL, in its symbolic-map step (DSECT), assemble the staged copy of the map source (&&TEMPM) with the parameter 'SYSPARM(DSECT),DECK,NOLOAD' using the CICS, SYS1.MACLIB and CEE.SCEEMAC macro libraries, and produce no object module. | medium | samples/proc/BUILDBMS.prc:23-29, samples/proc/BUILDBMS.prc:36-43, samples/proc/BUILDBMS.prc:78-92 |
| UP-BR-002 | Generate the symbolic map copybook | design note | THE Screen Map Build SHALL write the generated symbolic map as fixed-length 80-byte records, with exclusive access, to the map's member in the copybook library (&CPYBKS(&MAPNAME)), and write the assembler listing to the map's member in the listing library (&LISTING(&MAPNAME)). | medium | samples/proc/BUILDBMS.prc:23-29, samples/proc/BUILDBMS.prc:36-43, samples/proc/BUILDBMS.prc:78-92 |

### Key entities

None found in the source.

### Needs clarification

None.

### Decision table gaps

None.
