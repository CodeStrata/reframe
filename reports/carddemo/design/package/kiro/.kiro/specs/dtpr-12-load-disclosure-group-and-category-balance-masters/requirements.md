# Requirements: Load disclosure group and category balance masters (DTPR-C12)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Loads the disclosure group master (interest rates by group, type and category) and the transaction category balance file from their flat files. The disclosure master is fully replaced on each load. It serves the card operations team, so interest and posting work from current data. It must replace the disclosure groups completely rather than merge them, it must not fail when there is no previous master, and nothing else may write to these files during the load.

**User story:** As a card operations team, I want the disclosure group master and the transaction category balance file loaded from their flat files, so that interest calculation and posting work from current reference and balance data.

## Requirements

### Requirement 1: DTPR-REQ-F-067 (design note)

#### Acceptance criteria

1. Before loading, the system shall delete any existing disclosure group master and define it afresh as a keyed file of 50-byte records with a 16-byte key, so that the master is fully replaced rather than updated. (rules DTPR-BR-074)
2. GIVEN Existing master: 10 records; Flat file: 4 records WHEN Load disclosure group master from flat file applies THEN After the job the master holds only the 4 records from the flat file (DTPR-C12-AC-01; DTPR-BR-074)
3. GIVEN Existing master: none WHEN Load disclosure group master from flat file applies THEN The delete step ends with return code 0 and the master is defined and loaded (DTPR-C12-AC-02; DTPR-BR-074)

### Requirement 2: DTPR-REQ-N-006 (design note)

#### Acceptance criteria

1. If no disclosure group master exists when the load deletes it, then the system shall not treat this as an error. (rules DTPR-BR-074)
2. GIVEN Existing master: 10 records; Flat file: 4 records WHEN Load disclosure group master from flat file applies THEN After the job the master holds only the 4 records from the flat file (DTPR-C12-AC-01; DTPR-BR-074)
3. GIVEN Existing master: none WHEN Load disclosure group master from flat file applies THEN The delete step ends with return code 0 and the master is defined and loaded (DTPR-C12-AC-02; DTPR-BR-074)

### Requirement 3: DTPR-REQ-F-068 (design note)

#### Acceptance criteria

1. The system shall copy every record of the disclosure group flat file (AWS.M2.CARDDEMO.DISCGRP.PS, read shared) into the disclosure group master (AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS), holding the master for exclusive use during the load. (rules DTPR-BR-075)
2. GIVEN Disclosure group flat file: 3 records of 50 bytes WHEN Disclosure Group Master Load runs THEN The disclosure group master holds the same 3 records after the job (DTPR-C12-AC-03; DTPR-BR-075)

### Requirement 4: DTPR-REQ-F-069 (design note)

#### Acceptance criteria

1. The system shall copy every transaction category balance record from the flat file (AWS.M2.CARDDEMO.TCATBALF.PS, read shared with other jobs) into the keyed category balance file (AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS), holding the keyed file for exclusive use during the load. (rules DTPR-BR-076)
2. GIVEN Records in flat category balance file: 120 WHEN Transaction Category Balance Load runs THEN The keyed category balance file holds the same 120 records after the load. (DTPR-C12-AC-04; DTPR-BR-076)
3. GIVEN Another job using the keyed file: yes WHEN Transaction Category Balance Load runs THEN The load waits for or is refused exclusive use of the keyed file; the flat file can still be read by others. (DTPR-C12-AC-05; DTPR-BR-076)
