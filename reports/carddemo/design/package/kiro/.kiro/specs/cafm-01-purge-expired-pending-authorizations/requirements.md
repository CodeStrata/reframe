# Requirements: Purge expired pending authorizations (CAFM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as scheduled job · risk high

## Introduction

A scheduled job for the card operations team that works through every account's pending authorization summary, deletes each authorization detail that has reached the expiry age, and reduces the account's approved or declined counts and totals for each deleted detail. It deletes a summary once its adjusted approved count is zero or below. It must never delete an authorization younger than the expiry days, and it must stop the run if a deletion fails instead of carrying on with the store half purged.

**User story:** As a card operations team, I want pending authorizations that have reached their expiry age removed from the authorization database by a batch job, so that the pending authorization store holds only current authorizations.

## Requirements

### Requirement 1: CAFM-REQ-F-001 (design note)

#### Acceptance criteria

1. The system shall capture the current date, use the supplied expiry days when numeric or else default them to 5, and default the checkpoint frequency to 5 when it is spaces, 0 or low-values. (rules CAFM-BR-001)
2. GIVEN SYSIN: 00,00001,00001,Y WHEN Purge Parameter Setup runs THEN Expiry days is 0 (numeric, so used as given) and checkpoint frequency stays '00001'. (CAFM-C01-AC-01; CAFM-BR-001)
3. GIVEN P-EXPIRY-DAYS: 'AB'; P-CHKP-FREQ: spaces WHEN Purge Parameter Setup runs THEN Expiry days defaults to 5 and checkpoint frequency defaults to 5. (CAFM-C01-AC-02; CAFM-BR-001)
4. GIVEN P-EXPIRY-DAYS: 30; P-CHKP-FREQ: 00000 WHEN Purge Parameter Setup runs THEN Expiry days is 30 and checkpoint frequency is set to 5. (CAFM-C01-AC-03; CAFM-BR-001)

### Requirement 2: CAFM-REQ-N-001 (design note)

#### Acceptance criteria

1. The system shall run the purge program (CBPAUP0C) as an IMS batch message program with program specification block PSBPAUTB, using the IMS PSB and DBD libraries. (rules CAFM-BR-002)
2. GIVEN Job: CBPAUP0J WHEN expired-authorization purge job runs THEN Step STEP01 runs DFSRRC00 with PARM 'BMP,CBPAUP0C,PSBPAUTB'. (CAFM-C01-AC-04; CAFM-BR-002)

### Requirement 3: CAFM-REQ-F-002 (business rule)

#### Acceptance criteria

1. The system shall run the expired-authorization purge job with the control values '00,00001,00001,Y', meaning authorizations 0 or more days old count as expired, a checkpoint is taken after more than 1 authorization summary is processed, every checkpoint is reported, and debug messages are on. (rules CAFM-BR-003)
2. GIVEN Control values: 00,00001,00001,Y; Authorization age: 0 days (made today) WHEN expired-authorization purge job runs THEN The authorization qualifies for deletion, because its age is not less than 0 expiry days. (CAFM-C01-AC-05; CAFM-BR-003)
3. GIVEN Control values: 00,00001,00001,Y WHEN expired-authorization purge job runs THEN Debug lines such as 'DEBUG: AUTH SMRY READ : ' are printed and 'CHKP SUCCESS: AUTH COUNT - ' is shown after every checkpoint. (CAFM-C01-AC-06; CAFM-BR-003)

### Requirement 4: CAFM-REQ-F-003 (design note)

#### Acceptance criteria

1. The system shall read each account's pending authorization summary in turn until the end of the database, check every authorization detail under that summary for expiry, delete each detail that qualifies, and then move on to the next summary. (rules CAFM-BR-004)
2. GIVEN Summaries in database: 2; Details under first summary: 3, of which 1 expired WHEN pending authorization purge runs THEN All 3 details of the first summary are checked and 1 is deleted before the second summary is read; the run stops when the summary read returns end of database. (CAFM-C01-AC-07; CAFM-BR-004)

### Requirement 5: CAFM-REQ-F-004 (business rule)

#### Acceptance criteria

1. The system shall work out each authorization's date as 99999 minus its stored inverted date key (Julian YYDDD), and its age as today's Julian date (YYDDD) minus that date. (rules CAFM-BR-005)
2. GIVEN Stored date key: 74964; Today (YYDDD): 25040 WHEN pending authorization purge runs THEN Authorization date is 25035 and age is 5 days. (CAFM-C01-AC-08; CAFM-BR-005)

### Requirement 6: CAFM-REQ-F-005 (business rule)

#### Acceptance criteria

1. When an authorization's age is at least the expiry days, the system shall mark it as qualified for deletion. (rules CAFM-BR-006)
2. GIVEN Expiry days: 5; Age: 5 WHEN an authorization's age is at least the expiry days THEN Qualified for deletion. (CAFM-C01-AC-09; CAFM-BR-006)
3. GIVEN Expiry days: 5; Age: 4 WHEN an authorization's age is at least the expiry days THEN Kept. (CAFM-C01-AC-10; CAFM-BR-006)

### Requirement 7: CAFM-REQ-F-006 (business rule)

#### Acceptance criteria

1. When an authorization's age is less than the expiry days, the system shall mark it as not qualified and keep it. (rules CAFM-BR-006)
2. GIVEN Expiry days: 5; Age: 5 WHEN an authorization's age is at least the expiry days THEN Qualified for deletion. (CAFM-C01-AC-09; CAFM-BR-006)
3. GIVEN Expiry days: 5; Age: 4 WHEN an authorization's age is at least the expiry days THEN Kept. (CAFM-C01-AC-10; CAFM-BR-006)

### Requirement 8: CAFM-REQ-F-007 (business rule)

#### Acceptance criteria

1. When an authorization detail qualifies for deletion, the system shall delete it from the pending authorization detail segment (PAUTDTL1) and add 1 to the details-deleted count. (rules CAFM-BR-007)
2. GIVEN Qualified for deletion: Yes; Delete status: blank (success) WHEN an authorization detail qualifies for deletion THEN Detail removed and '# DETAILS REC DELETED' count increases by 1. (CAFM-C01-AC-11; CAFM-BR-007)

### Requirement 9: CAFM-REQ-F-008 (error handling)

#### Acceptance criteria

1. If deleting an authorization detail fails, then the system shall display 'AUTH DETAIL DELETE FAILED :' with the status and 'AUTH APP ID :' with the account, then display 'CBPAUP0C ABENDING ...' and end the run with return code 16. (rules CAFM-BR-008)
2. GIVEN Delete status: any non-blank code WHEN deleting an authorization detail fails THEN Messages 'AUTH DETAIL DELETE FAILED :' and 'CBPAUP0C ABENDING ...' are shown and the job ends with return code 16. (CAFM-C01-AC-12; CAFM-BR-008)

### Requirement 10: CAFM-REQ-F-009 (business rule)

#### Acceptance criteria

1. When an authorization detail qualifies for purge and its response code is '00' (approved), the system shall subtract 1 from the account summary's approved count and subtract the detail's approved amount from the summary's approved total. (rules CAFM-BR-009)
2. GIVEN Summary approved count: 3; Summary approved total: $450.00; Detail response code: '00'; Detail approved amount: $120.00 WHEN an authorization detail qualifies for purge and its response code is '00' (approved) THEN Approved count becomes 2 and approved total becomes $330.00 in the run's working copy; the stored summary is unchanged. (CAFM-C01-AC-13; CAFM-BR-009)

### Requirement 11: CAFM-REQ-F-010 (business rule)

#### Acceptance criteria

1. When an authorization detail qualifies for purge and its response code is anything other than '00', the system shall subtract 1 from the account summary's declined count and subtract the detail's transaction amount from the summary's declined total. (rules CAFM-BR-010)
2. GIVEN An account summary in the purge job's working copy has declined count 3 and declined total 200.00, and one of its authorization details has response code '05' and transaction amount 40.00 and has qualified for purge WHEN The purge processes that detail THEN The working copy shows declined count 2 and declined total 160.00, the approved count and approved total are unchanged, and the stored summary record is not rewritten (CAFM-C01-AC-18; CAFM-BR-010)

### Requirement 12: CAFM-REQ-F-011 (business rule)

#### Acceptance criteria

1. The system shall make the approved and declined count and total reductions in its working copy of the summary only and shall never rewrite the summary record. (rules CAFM-BR-009, CAFM-BR-010)
2. GIVEN Summary approved count: 3; Summary approved total: $450.00; Detail response code: '00'; Detail approved amount: $120.00 WHEN an authorization detail qualifies for purge and its response code is '00' (approved) THEN Approved count becomes 2 and approved total becomes $330.00 in the run's working copy; the stored summary is unchanged. (CAFM-C01-AC-13; CAFM-BR-009)

### Requirement 13: CAFM-REQ-F-012 (business rule)

#### Acceptance criteria

1. When all of an account summary's details have been checked and the adjusted approved authorization count is zero or below, the system shall delete the pending authorization summary from the summary store (DLI:PAUTSUM0). (rules CAFM-BR-011, CAFM-BR-012)
2. GIVEN Approved count after purge: 0; Declined count after purge: 2 WHEN all of an account summary's details have been checked THEN The summary is deleted even though declined authorizations remain. (CAFM-C01-AC-14; CAFM-BR-011)
3. GIVEN PA-APPROVED-AUTH-CNT: 0; DIBSTAT: spaces WHEN the approved authorization count (`PA-APPROVED-AUTH-CNT`) of the processed summary is zero or below THEN The summary segment is deleted and '# SUMMARY REC DELETED :' at end of run counts it. (CAFM-C01-AC-15; CAFM-BR-012)
4. GIVEN PA-APPROVED-AUTH-CNT: 2 WHEN the approved authorization count (`PA-APPROVED-AUTH-CNT`) of the processed summary is zero or below THEN The summary is kept. (CAFM-C01-AC-16; CAFM-BR-012)
5. GIVEN PA-APPROVED-AUTH-CNT: 0; DIBSTAT: GE WHEN the approved authorization count (`PA-APPROVED-AUTH-CNT`) of the processed summary is zero or below THEN 'AUTH SUMMARY DELETE FAILED :' is displayed with the account id, then 'CBPAUP0C ABENDING ...' and the run ends with return code 16. (CAFM-C01-AC-17; CAFM-BR-012)

### Requirement 14: CAFM-REQ-F-013 (business rule)

#### Acceptance criteria

1. If deleting the pending authorization summary fails, then the system shall abend the run. (rules CAFM-BR-012)
2. GIVEN PA-APPROVED-AUTH-CNT: 0; DIBSTAT: spaces WHEN the approved authorization count (`PA-APPROVED-AUTH-CNT`) of the processed summary is zero or below THEN The summary segment is deleted and '# SUMMARY REC DELETED :' at end of run counts it. (CAFM-C01-AC-15; CAFM-BR-012)
3. GIVEN PA-APPROVED-AUTH-CNT: 2 WHEN the approved authorization count (`PA-APPROVED-AUTH-CNT`) of the processed summary is zero or below THEN The summary is kept. (CAFM-C01-AC-16; CAFM-BR-012)
4. GIVEN PA-APPROVED-AUTH-CNT: 0; DIBSTAT: GE WHEN the approved authorization count (`PA-APPROVED-AUTH-CNT`) of the processed summary is zero or below THEN 'AUTH SUMMARY DELETE FAILED :' is displayed with the account id, then 'CBPAUP0C ABENDING ...' and the run ends with return code 16. (CAFM-C01-AC-17; CAFM-BR-012)
