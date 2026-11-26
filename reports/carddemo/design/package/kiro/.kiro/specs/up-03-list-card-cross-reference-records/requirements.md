# Requirements: List card cross-reference records (UP-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk medium

## Introduction

A read-only batch listing of every card cross-reference record, showing which card belongs to which account and customer. Operations staff use it for review. It must never change the cross-reference. The legacy job prints each record twice, which the team must either keep or consciously drop.

**User story:** As an operations user, I want a listing of every card cross-reference record, so that I can review which cards link to which accounts and customers without changing the master.

## Requirements

### Requirement 1: UP-REQ-F-010 (design note)

#### Acceptance criteria

1. The system shall run the program CBACT03C against the card cross-reference master (AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS) in shared read-only access, leaving the master unchanged and printing every cross-reference record to the job's output listing. (rules UP-BR-012)
2. GIVEN cross-reference master: 3 card cross-reference records WHEN Card Cross-Reference Master Read job runs THEN The job listing shows 'START OF EXECUTION OF PROGRAM CBACT03C', the 3 records, and 'END OF EXECUTION OF PROGRAM CBACT03C'; the master still holds the same 3 records. (UP-C03-AC-01; UP-BR-012)

### Requirement 2: UP-REQ-F-011 (formatting)

#### Acceptance criteria

1. The system shall read the card cross-reference file from start to end and print every record, stopping when the end of the file is reached. (rules UP-BR-013)
2. GIVEN cross-reference records: 3 WHEN Card Cross-Reference Listing (CBACT03C) runs THEN All 3 records are printed, then 'END OF EXECUTION OF PROGRAM CBACT03C'. (UP-C03-AC-02; UP-BR-013)

### Requirement 3: UP-REQ-F-012 (historical artifact)

#### Acceptance criteria

1. The system shall print each cross-reference record twice in a row, once when it is read and again in the main loop. (rules UP-BR-014)
2. GIVEN cross-reference records: 2 WHEN Card Cross-Reference Listing runs THEN The output has 4 record lines, each record appearing twice in succession. (UP-C03-AC-03; UP-BR-014)
