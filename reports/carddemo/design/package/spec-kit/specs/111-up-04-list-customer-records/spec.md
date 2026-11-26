# Feature specification: List customer records

**Feature:** UP-C04 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C04)

As an operations user, I want a listing of every customer on the customer master file, so that I can review customer records.

A batch listing of every customer on the customer master, from first to last. Operations staff use it to review customer records. It must list every customer and stop cleanly at the end of the file. The legacy job prints each customer twice, which the team must either keep or consciously drop.

**Acceptance scenarios:**

1. **Given** Customer file: 3 customer records, **when** Customer Listing runs, **then** All 3 customer records are printed to the job output and the run ends with 'END OF EXECUTION OF PROGRAM CBCUS01C'. (UP-C04-AC-01)
2. **Given** Customer file: empty, **when** Customer Listing runs, **then** No customer record is printed; the first read returns end of file and the program ends. (UP-C04-AC-02)
3. **Given** Customer file: 1 customer record for customer 000000001, **when** a customer record is read successfully, **then** The record for customer 000000001 appears two times in the job output. (UP-C04-AC-03)
4. **Given** customer records: 5, **when** Customer Listing (CBCUS01C) runs, **then** The customer listing has 10 record lines. (UP-C04-AC-04)
5. **Given** card records: 5, **when** Customer Listing (CBCUS01C) runs, **then** The card listing has 5 record lines. (UP-C04-AC-05)

## Requirements

### Functional requirements

- **UP-REQ-F-013** (formatting): The system shall read the customer master file from start to end and print each customer record to the job output, stopping when the end of the file is reached (file status '10'). Rules: UP-BR-015.
- **UP-REQ-F-014** (formatting): When a customer record is read successfully, the system shall print that record twice, once in the read routine (1000-CUSTFILE-GET-NEXT) and once in the main loop. Rules: UP-BR-016, UP-BR-005.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-015 | List all customer records until end | formatting | THE Customer Listing SHALL read the customer master file from start to end and print each customer record to the job output, stopping when the end of the file is reached (file status '10'). | medium | app/cbl/CBCUS01C.cbl:70-87, app/cbl/CBCUS01C.cbl:92-116 |
| UP-BR-016 | List all customer records until end | formatting | WHEN a customer record is read successfully, THE Customer Listing SHALL print that record twice, once in the read routine (1000-CUSTFILE-GET-NEXT) and once in the main loop. | medium | app/cbl/CBCUS01C.cbl:70-87, app/cbl/CBCUS01C.cbl:92-116 |
| UP-BR-005 | Each record is printed twice in the cross-reference and customer dumps | historical artifact | THE Customer Listing (CBCUS01C) SHALL likewise print each customer record twice, while the Card Listing (CBACT02C) prints each card record once because its second print is commented out. | high | app/cbl/CBACT03C.cbl:74-81, app/cbl/CBACT03C.cbl:92-96, app/cbl/CBACT03C.cbl:98-108, app/cbl/CBCUS01C.cbl:78 |

### Key entities

- CVACT03Y (file record)
- CVCUS01Y (file record)

### Needs clarification

- SME-010: The cross-reference and customer listings print every record twice. Does anything rely on that, or should each record be printed once? (Batch operations) On UP-BR-005.
- DEF-097: Is this intended? Each record is displayed twice, once in the read paragraph and once in the main loop; CBACT02C has the same read-paragraph display commented out, suggesting the duplicate is debug output left in by mistake. (Subject-matter expert) On UP-BR-005.
- DEF-145: Is this intended? Each successfully read customer record is displayed twice: once inside 1000-CUSTFILE-GET-NEXT on status '00' and again in the main loop, doubling the listing. (Subject-matter expert) On UP-BR-016.

### Decision table gaps

None.
