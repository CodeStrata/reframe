# Requirements: Retain dataset generations (UP-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk low

## Introduction

Keeps a limited, rolling history of the batch files: daily transactions, rejects, combined and system-generated transactions, backups and the transaction report. Old copies are removed automatically. Operators rely on it to keep the most recent runs (five, or ten for the report history set-up) and never to let old copies pile up. Re-running the set-up must be harmless.

**User story:** As a CardDemo operator, I want transaction, reject, report and backup files kept as limited generation groups, so that recent history is kept and old generations are removed automatically.

## Requirements

### Requirement 1: UP-REQ-F-038 (design note)

#### Acceptance criteria

1. The system shall define the generation group for the daily rejected transactions (AWS.M2.CARDDEMO.DALYREJS) so that at most 5 generations are kept and each generation that ages out of the group is scratched. (rules UP-BR-041)
2. GIVEN existing generations: 5; event: transaction posting writes a new rejects generation (+1) WHEN Daily Rejects setup job runs THEN The oldest generation is removed from the group and scratched, leaving the 5 newest. (UP-C09-AC-01; UP-BR-041)

### Requirement 2: UP-REQ-F-039 (design note)

#### Acceptance criteria

1. The system shall define the combined transaction file (AWS.M2.CARDDEMO.TRANSACT.COMBINED, the transaction backup merged with system-generated transactions) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. (rules UP-BR-042)
2. GIVEN combined transaction files already kept: 5; event: combine job writes a new combined file (+1) WHEN CardDemo setup job (DEFGDGB) runs THEN The new combined file is kept and the oldest is removed and erased, leaving 5 generations. (UP-C09-AC-02; UP-BR-042)

### Requirement 3: UP-REQ-F-040 (design note)

#### Acceptance criteria

1. The system shall define the daily transaction file (AWS.M2.CARDDEMO.TRANSACT.DALY) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. (rules UP-BR-043)
2. GIVEN generations of AWS.M2.CARDDEMO.TRANSACT.DALY already kept: 5; event: transaction report job writes a new daily file (+1) WHEN CardDemo setup job (DEFGDGB) runs THEN The new daily file is kept and the oldest is removed and erased, leaving 5 generations. (UP-C09-AC-03; UP-BR-043)

### Requirement 4: UP-REQ-F-041 (design note)

#### Acceptance criteria

1. The CardDemo setup job (DEFGDGB) shall define the transaction report (AWS.M2.CARDDEMO.TRANREPT) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest report's data when a new one pushes it past the limit. (rules UP-BR-044)
2. GIVEN transaction reports already kept: 5; event: transaction report job writes a new report (+1) WHEN CardDemo setup job (DEFGDGB) runs THEN The new report is kept and the oldest report is removed and erased, leaving 5 reports. (UP-C09-AC-04; UP-BR-044)

### Requirement 5: UP-REQ-F-042 (design note)

#### Acceptance criteria

1. The Transaction Report History setup job shall define the transaction report generation group (AWS.M2.CARDDEMO.TRANREPT) so that at most 10 generations of the daily transaction report are kept catalogued, the oldest dropping off when an eleventh is created. (rules UP-BR-045)
2. GIVEN catalogued report generations: 10; new daily transaction report: written as generation (+1) WHEN Transaction Report History setup job runs THEN The new report is catalogued and the oldest of the 10 earlier generations is no longer kept in the group. (UP-C09-AC-05; UP-BR-045)

### Requirement 6: UP-REQ-F-043 (design note)

#### Acceptance criteria

1. The system shall define the transaction category balance backup (AWS.M2.CARDDEMO.TCATBALF.BKUP) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. (rules UP-BR-046)
2. GIVEN category balance backups already kept: 5; event: category balance print job writes a new backup (+1) WHEN CardDemo setup job (DEFGDGB) runs THEN The new backup is kept and the oldest is removed and erased, leaving 5 generations. (UP-C09-AC-06; UP-BR-046)

### Requirement 7: UP-REQ-F-044 (design note)

#### Acceptance criteria

1. The system shall define the transaction master backup file (AWS.M2.CARDDEMO.TRANSACT.BKUP) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. (rules UP-BR-047)
2. GIVEN generations of AWS.M2.CARDDEMO.TRANSACT.BKUP already kept: 5; event: transaction backup job writes a new generation (+1) WHEN CardDemo setup job (DEFGDGB) runs THEN The new backup is kept and the oldest of the five is removed from the catalog and its data erased, leaving 5 generations. (UP-C09-AC-07; UP-BR-047)
3. GIVEN generations already kept: 3; event: new backup written WHEN CardDemo setup job (DEFGDGB) runs THEN All 4 generations are kept; nothing is deleted. (UP-C09-AC-08; UP-BR-047)

### Requirement 8: UP-REQ-F-045 (design note)

#### Acceptance criteria

1. The system shall define the system-generated transaction file (AWS.M2.CARDDEMO.SYSTRAN) as a generation group that keeps at most 5 generations and deletes (SCRATCH) the oldest generation's data when a new one pushes it past the limit. (rules UP-BR-048)
2. GIVEN system transaction files already kept: 5; event: interest calculation job writes a new file (+1) WHEN CardDemo setup job (DEFGDGB) runs THEN The new file is kept and the oldest is removed and erased, leaving 5 generations. (UP-C09-AC-09; UP-BR-048)

### Requirement 9: UP-REQ-F-046 (error handling)

#### Acceptance criteria

1. If a generation group definition in the setup job ends with return code 12 (for example because the group already exists), then the system shall reset the job's highest return code to 0 and continue with the next definition. (rules UP-BR-049)
2. GIVEN AWS.M2.CARDDEMO.TRANSACT.BKUP: already defined; DEFINE return code: 12 WHEN a generation group definition in the setup job ends with return code 12 (for example because the group already exists) THEN The job's return code is set back to 0 and it goes on to define AWS.M2.CARDDEMO.TRANSACT.DALY. (UP-C09-AC-10; UP-BR-049)
