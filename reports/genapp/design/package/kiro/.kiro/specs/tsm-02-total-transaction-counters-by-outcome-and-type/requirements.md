# Requirements: Total transaction counters by outcome and type (TSM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Transaction Statistics and Monitoring · runs as scheduled job · risk low

## Introduction

Each run totals the GENA transaction counters by outcome and by type: a successful-transaction total, an error total, and inquiry, add, update and delete totals. Business monitor users read these totals to follow throughput. The new application must not get the membership of each total wrong: success totals use only the 17 counters ending '00', the error total uses only the 17 ending '99', 'GENAOTHER' is in neither, update has no customer or commercial counter, and delete has no customer counter.

**User story:** As a business monitor user, I want the transaction counters in pool 'GENA' totalled into successful, error, inquiry, add, update and delete totals, so that I can see transaction throughput by outcome and type.

## Requirements

### Requirement 1: TSM-REQ-F-005 (business rule)

#### Acceptance criteria

1. The system shall add up the 17 success counters in pool 'GENA' (the counters ending '00': ICUS, ACUS, IMOT, AMOT, DMOT, UMOT, IEND, AEND, DEND, UEND, IHOU, AHOU, DHOU, UHOU, ICOM, ACOM, DCOM) into one successful-transaction total, leaving out the error counters ending '99' and the 'GENAOTHER' counter. (rules TSM-BR-003)
2. GIVEN GENA01ICUS00: 100; GENA01ACUS00: 20; GENA01ICUS99: 3; all other '00' counters: 0 WHEN Statistics Collector runs THEN Successful-transaction total is 120; the 3 errors are not included (TSM-C02-AC-01; TSM-BR-003)

### Requirement 2: TSM-REQ-F-006 (business rule)

#### Acceptance criteria

1. The system shall add up the 17 error counters in pool 'GENA' (the counters ending '99', from 'GENA01ICUS99' to 'GENA01DCOM99') into an error total, not including the 'GENAOTHER' counter. (rules TSM-BR-004)
2. GIVEN GENA01ICUS99: 3; GENAOTHER: 4; all other '99' counters: 0 WHEN Statistics Collector runs THEN Error total is 3 (TSM-C02-AC-02; TSM-BR-004)

### Requirement 3: TSM-REQ-F-007 (business rule)

#### Acceptance criteria

1. The system shall compute the inquiry total as the sum of counters 'GENA01ICUS00', 'GENA01IMOT00', 'GENA01IEND00', 'GENA01IHOU00' and 'GENA01ICOM00'. (rules TSM-BR-005)
2. GIVEN GENA01ICUS00: 50; GENA01IMOT00: 10; GENA01IEND00: 5; GENA01IHOU00: 3; GENA01ICOM00: 2 WHEN Statistics Collector runs THEN Inquiry total is 70 (TSM-C02-AC-03; TSM-BR-005)

### Requirement 4: TSM-REQ-F-008 (business rule)

#### Acceptance criteria

1. The system shall compute the add total as the sum of counters 'GENA01ACUS00', 'GENA01AMOT00', 'GENA01AEND00', 'GENA01AHOU00' and 'GENA01ACOM00'. (rules TSM-BR-006)
2. GIVEN GENA01ACUS00: 8; GENA01AMOT00: 4; GENA01AEND00: 2; GENA01AHOU00: 1; GENA01ACOM00: 0 WHEN Statistics Collector runs THEN Add total is 15 (TSM-C02-AC-04; TSM-BR-006)

### Requirement 5: TSM-REQ-F-009 (business rule)

#### Acceptance criteria

1. The system shall compute the update total as the sum of 'GENA01UMOT00', 'GENA01UEND00' and 'GENA01UHOU00', with no customer or commercial update counter included. (rules TSM-BR-007)
2. GIVEN GENA01UMOT00: 6; GENA01UEND00: 3; GENA01UHOU00: 1 WHEN Statistics Collector runs THEN Update total is 10 (TSM-C02-AC-05; TSM-BR-007)

### Requirement 6: TSM-REQ-F-010 (business rule)

#### Acceptance criteria

1. The system shall compute the delete total as the sum of 'GENA01DMOT00', 'GENA01DEND00', 'GENA01DHOU00' and 'GENA01DCOM00', with no customer delete counter included. (rules TSM-BR-008)
2. GIVEN GENA01DMOT00: 2; GENA01DEND00: 1; GENA01DHOU00: 1; GENA01DCOM00: 1 WHEN Statistics Collector runs THEN Delete total is 5 (TSM-C02-AC-06; TSM-BR-008)
