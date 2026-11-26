# Feature specification: List card cross-reference records

**Feature:** UP-C03 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C03)

As an operations user, I want a listing of every card cross-reference record, so that I can review which cards link to which accounts and customers without changing the master.

A read-only batch listing of every card cross-reference record, showing which card belongs to which account and customer. Operations staff use it for review. It must never change the cross-reference. The legacy job prints each record twice, which the team must either keep or consciously drop.

**Acceptance scenarios:**

1. **Given** cross-reference master: 3 card cross-reference records, **when** Card Cross-Reference Master Read job runs, **then** The job listing shows 'START OF EXECUTION OF PROGRAM CBACT03C', the 3 records, and 'END OF EXECUTION OF PROGRAM CBACT03C'; the master still holds the same 3 records. (UP-C03-AC-01)
2. **Given** cross-reference records: 3, **when** Card Cross-Reference Listing (CBACT03C) runs, **then** All 3 records are printed, then 'END OF EXECUTION OF PROGRAM CBACT03C'. (UP-C03-AC-02)
3. **Given** cross-reference records: 2, **when** Card Cross-Reference Listing runs, **then** The output has 4 record lines, each record appearing twice in succession. (UP-C03-AC-03)

## Requirements

### Functional requirements

- **UP-REQ-F-010** (design note): The system shall run the program CBACT03C against the card cross-reference master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS) in shared read-only access, leaving the master unchanged and printing every cross-reference record to the job's output listing. Rules: UP-BR-012.
- **UP-REQ-F-011** (formatting): The system shall read the card cross-reference file from start to end and print every record, stopping when the end of the file is reached. Rules: UP-BR-013.
- **UP-REQ-F-012** (historical artifact): The system shall print each cross-reference record twice in a row, once when it is read and again in the main loop. Rules: UP-BR-014.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-012 | Read the card cross-reference master | design note | THE Card Cross-Reference Master Read job SHALL run the program CBACT03C against the card cross-reference master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS) in shared read-only access, leaving the master unchanged and printing every cross-reference record to the job's output listing. | medium | app/jcl/READXREF.jcl:22-28, app/cbl/CBACT03C.cbl:70-86, app/cbl/CBACT03C.cbl:92-96 |
| UP-BR-013 | List all card cross-reference records | formatting | THE Card Cross-Reference Listing (CBACT03C) SHALL read the card cross-reference file from start to end and print every record, stopping when the end of the file is reached. | high | app/cbl/CBACT03C.cbl:74-81, app/cbl/CBACT03C.cbl:92-96, app/cbl/CBACT03C.cbl:98-108, app/cbl/CBCUS01C.cbl:78 |
| UP-BR-014 | Each record is printed twice in the cross-reference and customer dumps | historical artifact | THE Card Cross-Reference Listing SHALL print each cross-reference record twice in a row, once when it is read and again in the main loop. | high | app/cbl/CBACT03C.cbl:74-81, app/cbl/CBACT03C.cbl:92-96, app/cbl/CBACT03C.cbl:98-108, app/cbl/CBCUS01C.cbl:78 |

### Key entities

- CVACT03Y (file record)

### Needs clarification

- SME-010: The cross-reference and customer listings print every record twice. Does anything rely on that, or should each record be printed once? (Batch operations) On UP-BR-014.
- DEF-097: Is this intended? Each record is displayed twice, once in the read paragraph and once in the main loop; CBACT02C has the same read-paragraph display commented out, suggesting the duplicate is debug output left in by mistake. (Subject-matter expert) On UP-BR-013, UP-BR-014.
- DEF-141: Is this intended? CBACT03C prints each cross-reference record twice: once in the read routine on a successful read and again in the main loop, so the listing shows every record duplicated. (Subject-matter expert) On UP-BR-012.

### Decision table gaps

None.
