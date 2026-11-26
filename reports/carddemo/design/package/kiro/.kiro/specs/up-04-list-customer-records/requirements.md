# Requirements: List customer records (UP-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk medium

## Introduction

A batch listing of every customer on the customer master, from first to last. Operations staff use it to review customer records. It must list every customer and stop cleanly at the end of the file. The legacy job prints each customer twice, which the team must either keep or consciously drop.

**User story:** As an operations user, I want a listing of every customer on the customer master file, so that I can review customer records.

## Requirements

### Requirement 1: UP-REQ-F-013 (formatting)

#### Acceptance criteria

1. The system shall read the customer master file from start to end and print each customer record to the job output, stopping when the end of the file is reached (file status '10'). (rules UP-BR-015)
2. GIVEN Customer file: 3 customer records WHEN Customer Listing runs THEN All 3 customer records are printed to the job output and the run ends with 'END OF EXECUTION OF PROGRAM CBCUS01C'. (UP-C04-AC-01; UP-BR-015)
3. GIVEN Customer file: empty WHEN Customer Listing runs THEN No customer record is printed; the first read returns end of file and the program ends. (UP-C04-AC-02; UP-BR-015)

### Requirement 2: UP-REQ-F-014 (formatting)

#### Acceptance criteria

1. When a customer record is read successfully, the system shall print that record twice, once in the read routine (1000-CUSTFILE-GET-NEXT) and once in the main loop. (rules UP-BR-016, UP-BR-005)
2. GIVEN Customer file: 1 customer record for customer 000000001 WHEN a customer record is read successfully THEN The record for customer 000000001 appears two times in the job output. (UP-C04-AC-03; UP-BR-016)
3. GIVEN customer records: 5 WHEN Customer Listing (CBCUS01C) runs THEN The customer listing has 10 record lines. (UP-C04-AC-04; UP-BR-005)
4. GIVEN card records: 5 WHEN Customer Listing (CBCUS01C) runs THEN The card listing has 5 record lines. (UP-C04-AC-05; UP-BR-005)
