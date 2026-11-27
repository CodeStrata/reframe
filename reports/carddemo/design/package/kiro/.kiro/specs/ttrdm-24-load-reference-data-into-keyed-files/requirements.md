# Requirements: Load reference data into keyed files (TTRDM-C24)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as scheduled job · risk medium

## Introduction

A scheduled job for operations that rebuilds the keyed transaction type and transaction category stores from their flat extract files, so that online screens and batch programs read current reference data. Each store is emptied and reloaded with every record from its file. No record may be lost or left over from the previous load.

**User story:** As an operations user, I want to reload the keyed transaction type and category files from their flat files, so that online and batch programs read current reference data.

## Requirements

### Requirement 1: TTRDM-REQ-F-160 (design note)

#### Acceptance criteria

1. The system shall copy every record of the transaction category flat file (AWS.M2.CARDDEMO.TRANCATG.PS, read shared) into the keyed transaction category file (AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS, held exclusively), which the same job has just deleted and redefined empty, keyed on the first 6 characters of each 60-character record. (rules TTRDM-BR-172)
2. GIVEN transaction category flat file: 18 category records; keyed category file before the run: exists with older records WHEN Transaction Category Reference Load runs THEN The keyed file is deleted, redefined empty and loaded with exactly the 18 records from the flat file; the older records are gone. (TTRDM-C24-AC-01; TTRDM-BR-172)
3. GIVEN keyed category file before the run: does not exist WHEN Transaction Category Reference Load runs THEN The failed delete is ignored (return code reset to 0), the file is defined and the flat-file records are loaded. (TTRDM-C24-AC-02; TTRDM-BR-172)

### Requirement 2: TTRDM-REQ-F-161 (design note)

#### Acceptance criteria

1. The system shall copy every record of the transaction type flat file (AWS.M2.CARDDEMO.TRANTYPE.PS, read shared) into the keyed transaction type file (AWS.M2.CARDDEMO.TRANTYPE.VSAM.KSDS, held exclusively), which the same job has just deleted and redefined empty, keyed on the first 2 characters of each 60-character record. (rules TTRDM-BR-173)
2. GIVEN transaction type flat file: 7 type records (codes 01 to 07); keyed type file before the run: exists with older records WHEN Transaction Type Reference Load runs THEN The keyed file is deleted, redefined empty and loaded with exactly the 7 records; earlier contents are not kept. (TTRDM-C24-AC-03; TTRDM-BR-173)
