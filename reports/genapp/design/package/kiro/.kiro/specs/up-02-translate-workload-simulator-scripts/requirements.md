# Requirements: Translate workload simulator scripts (UP-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk low

## Introduction

Translates each of the 20 workload simulator scripts in the script library so they are ready to drive simulation runs. Each script's translation listing is kept for the operator to check. It must translate every listed script, never change the script or message libraries, and leave no work files behind.

**User story:** As a workload simulator operator, I want each simulator script member translated in the script translation job, so that the scripts are ready to drive simulation runs and their listings can be checked.

## Requirements

### Requirement 1: UP-REQ-F-003 (design note)

#### Acceptance criteria

1. When the script translation job (GENASTL) runs, the system shall run the workload simulator script translator (ITPSTL) in its own job step for each of the script members 'WSC1I1', 'STOP', 'SSP4D1', 'SSP2I1', 'SSC1A1', 'SSP4A1', 'SSP1I1', 'SSP3D1', '#SSVARS', 'SSP2U1', 'SSP3I1', 'SSC1I1', 'SSP2A1', 'SSP2D1', 'SSP1U1', 'SSP3A1', 'SSP4I1', 'SSP1A1', 'SSP1D1' and 'WSC1A1' of the script library (<WSIMWSX>). (rules UP-BR-003, UP-BR-004, UP-BR-005, UP-BR-006, UP-BR-007, UP-BR-008, UP-BR-009, UP-BR-010, UP-BR-011, UP-BR-012, UP-BR-013, UP-BR-014, UP-BR-015, UP-BR-016, UP-BR-017, UP-BR-018, UP-BR-019, UP-BR-020, UP-BR-021, UP-BR-022)
2. GIVEN script member (MEM): WSC1I1 WHEN script translation job (GENASTL, step WSC1I1) runs THEN ITPSTL translates member 'WSC1I1' and prints its listing and SEQOUT output (UP-C02-AC-01; UP-BR-003)
3. GIVEN script member (MEM): STOP WHEN script translation job (GENASTL, step STOP) runs THEN ITPSTL translates member 'STOP' and prints its listing and SEQOUT output (UP-C02-AC-02; UP-BR-004)
4. GIVEN script member (MEM): SSP4D1 WHEN script translation job (GENASTL, step SSP4D1) runs THEN ITPSTL translates member 'SSP4D1' and prints its listing and SEQOUT output (UP-C02-AC-03; UP-BR-005)
5. GIVEN script member (MEM): SSP2I1 WHEN script translation job (GENASTL, step SSP2I1) runs THEN ITPSTL translates member 'SSP2I1' and prints its listing and SEQOUT output (UP-C02-AC-04; UP-BR-006)
6. GIVEN script member (MEM): SSC1A1 WHEN script translation job (GENASTL, step SSC1A1) runs THEN ITPSTL translates member 'SSC1A1' and prints its listing and SEQOUT output (UP-C02-AC-05; UP-BR-007)
7. GIVEN script member (MEM): SSP4A1 WHEN script translation job (GENASTL, step SSP4A1) runs THEN ITPSTL translates member 'SSP4A1' and prints its listing and SEQOUT output (UP-C02-AC-06; UP-BR-008)
8. GIVEN script member (MEM): SSP1I1 WHEN script translation job (GENASTL, step SSP1I1) runs THEN ITPSTL translates member 'SSP1I1' and prints its listing and SEQOUT output (UP-C02-AC-07; UP-BR-009)
9. GIVEN script member (MEM): SSP3D1 WHEN script translation job (GENASTL, step SSP3D1) runs THEN ITPSTL translates member 'SSP3D1' and prints its listing and SEQOUT output (UP-C02-AC-08; UP-BR-010)
10. GIVEN script member (MEM): #SSVARS WHEN script translation job (GENASTL, step #SSVARS) runs THEN ITPSTL translates member '#SSVARS' and prints its listing and SEQOUT output (UP-C02-AC-09; UP-BR-011)
11. GIVEN script member (MEM): SSP2U1 WHEN script translation job (GENASTL, step SSP2U1) runs THEN ITPSTL translates member 'SSP2U1' and prints its listing and SEQOUT output (UP-C02-AC-10; UP-BR-012)
12. GIVEN script member (MEM): SSP3I1 WHEN script translation job (GENASTL, step SSP3I1) runs THEN ITPSTL translates member 'SSP3I1' and prints its listing and SEQOUT output (UP-C02-AC-11; UP-BR-013)
13. GIVEN script member (MEM): SSC1I1 WHEN script translation job (GENASTL, step SSC1I1) runs THEN ITPSTL translates member 'SSC1I1' and prints its listing and SEQOUT output (UP-C02-AC-12; UP-BR-014)
14. GIVEN step: SSP2A1; member (MEM): 'SSP2A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP2A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output; the SYSUT1 work area is not kept. (UP-C02-AC-13; UP-BR-015)
15. GIVEN step: SSP2D1; member (MEM): 'SSP2D1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP2D1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-14; UP-BR-016)
16. GIVEN step: SSP1U1; member (MEM): 'SSP1U1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1U1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-15; UP-BR-017)
17. GIVEN step: SSP3A1; member (MEM): 'SSP3A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP3A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-16; UP-BR-018)
18. GIVEN step: SSP4I1; member (MEM): 'SSP4I1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP4I1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-17; UP-BR-019)
19. GIVEN step: SSP1A1; member (MEM): 'SSP1A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-18; UP-BR-020)
20. GIVEN step: SSP1D1; member (MEM): 'SSP1D1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1D1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's message class (H). (UP-C02-AC-19; UP-BR-021)
21. GIVEN step: WSC1A1; member (MEM): 'WSC1A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(WSC1A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-20; UP-BR-022)

### Requirement 2: UP-REQ-F-004 (design note)

#### Acceptance criteria

1. When a script translation step runs, the system shall read the script member and the script library (<WSIMWSX>) as reference library, together with the message library (<WSIMMSX>), all opened shared. (rules UP-BR-003, UP-BR-004, UP-BR-005, UP-BR-006, UP-BR-007, UP-BR-008, UP-BR-009, UP-BR-010, UP-BR-011, UP-BR-012, UP-BR-013, UP-BR-014, UP-BR-015, UP-BR-016, UP-BR-017, UP-BR-018, UP-BR-019, UP-BR-020, UP-BR-021, UP-BR-022)
2. GIVEN script member (MEM): WSC1I1 WHEN script translation job (GENASTL, step WSC1I1) runs THEN ITPSTL translates member 'WSC1I1' and prints its listing and SEQOUT output (UP-C02-AC-01; UP-BR-003)
3. GIVEN script member (MEM): STOP WHEN script translation job (GENASTL, step STOP) runs THEN ITPSTL translates member 'STOP' and prints its listing and SEQOUT output (UP-C02-AC-02; UP-BR-004)
4. GIVEN script member (MEM): SSP4D1 WHEN script translation job (GENASTL, step SSP4D1) runs THEN ITPSTL translates member 'SSP4D1' and prints its listing and SEQOUT output (UP-C02-AC-03; UP-BR-005)
5. GIVEN script member (MEM): SSP2I1 WHEN script translation job (GENASTL, step SSP2I1) runs THEN ITPSTL translates member 'SSP2I1' and prints its listing and SEQOUT output (UP-C02-AC-04; UP-BR-006)
6. GIVEN script member (MEM): SSC1A1 WHEN script translation job (GENASTL, step SSC1A1) runs THEN ITPSTL translates member 'SSC1A1' and prints its listing and SEQOUT output (UP-C02-AC-05; UP-BR-007)
7. GIVEN script member (MEM): SSP4A1 WHEN script translation job (GENASTL, step SSP4A1) runs THEN ITPSTL translates member 'SSP4A1' and prints its listing and SEQOUT output (UP-C02-AC-06; UP-BR-008)
8. GIVEN script member (MEM): SSP1I1 WHEN script translation job (GENASTL, step SSP1I1) runs THEN ITPSTL translates member 'SSP1I1' and prints its listing and SEQOUT output (UP-C02-AC-07; UP-BR-009)
9. GIVEN script member (MEM): SSP3D1 WHEN script translation job (GENASTL, step SSP3D1) runs THEN ITPSTL translates member 'SSP3D1' and prints its listing and SEQOUT output (UP-C02-AC-08; UP-BR-010)
10. GIVEN script member (MEM): #SSVARS WHEN script translation job (GENASTL, step #SSVARS) runs THEN ITPSTL translates member '#SSVARS' and prints its listing and SEQOUT output (UP-C02-AC-09; UP-BR-011)
11. GIVEN script member (MEM): SSP2U1 WHEN script translation job (GENASTL, step SSP2U1) runs THEN ITPSTL translates member 'SSP2U1' and prints its listing and SEQOUT output (UP-C02-AC-10; UP-BR-012)
12. GIVEN script member (MEM): SSP3I1 WHEN script translation job (GENASTL, step SSP3I1) runs THEN ITPSTL translates member 'SSP3I1' and prints its listing and SEQOUT output (UP-C02-AC-11; UP-BR-013)
13. GIVEN script member (MEM): SSC1I1 WHEN script translation job (GENASTL, step SSC1I1) runs THEN ITPSTL translates member 'SSC1I1' and prints its listing and SEQOUT output (UP-C02-AC-12; UP-BR-014)
14. GIVEN step: SSP2A1; member (MEM): 'SSP2A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP2A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output; the SYSUT1 work area is not kept. (UP-C02-AC-13; UP-BR-015)
15. GIVEN step: SSP2D1; member (MEM): 'SSP2D1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP2D1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-14; UP-BR-016)
16. GIVEN step: SSP1U1; member (MEM): 'SSP1U1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1U1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-15; UP-BR-017)
17. GIVEN step: SSP3A1; member (MEM): 'SSP3A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP3A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-16; UP-BR-018)
18. GIVEN step: SSP4I1; member (MEM): 'SSP4I1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP4I1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-17; UP-BR-019)
19. GIVEN step: SSP1A1; member (MEM): 'SSP1A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-18; UP-BR-020)
20. GIVEN step: SSP1D1; member (MEM): 'SSP1D1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1D1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's message class (H). (UP-C02-AC-19; UP-BR-021)
21. GIVEN step: WSC1A1; member (MEM): 'WSC1A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(WSC1A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-20; UP-BR-022)

### Requirement 3: UP-REQ-N-001 (design note)

#### Acceptance criteria

1. When a script translation step runs, the system shall use a temporary work file that is not kept after the step. (rules UP-BR-003, UP-BR-004, UP-BR-005, UP-BR-006, UP-BR-007, UP-BR-008, UP-BR-009, UP-BR-010, UP-BR-011, UP-BR-012, UP-BR-013, UP-BR-014, UP-BR-015, UP-BR-016, UP-BR-017, UP-BR-018, UP-BR-019, UP-BR-020, UP-BR-021, UP-BR-022)
2. GIVEN script member (MEM): WSC1I1 WHEN script translation job (GENASTL, step WSC1I1) runs THEN ITPSTL translates member 'WSC1I1' and prints its listing and SEQOUT output (UP-C02-AC-01; UP-BR-003)
3. GIVEN script member (MEM): STOP WHEN script translation job (GENASTL, step STOP) runs THEN ITPSTL translates member 'STOP' and prints its listing and SEQOUT output (UP-C02-AC-02; UP-BR-004)
4. GIVEN script member (MEM): SSP4D1 WHEN script translation job (GENASTL, step SSP4D1) runs THEN ITPSTL translates member 'SSP4D1' and prints its listing and SEQOUT output (UP-C02-AC-03; UP-BR-005)
5. GIVEN script member (MEM): SSP2I1 WHEN script translation job (GENASTL, step SSP2I1) runs THEN ITPSTL translates member 'SSP2I1' and prints its listing and SEQOUT output (UP-C02-AC-04; UP-BR-006)
6. GIVEN script member (MEM): SSC1A1 WHEN script translation job (GENASTL, step SSC1A1) runs THEN ITPSTL translates member 'SSC1A1' and prints its listing and SEQOUT output (UP-C02-AC-05; UP-BR-007)
7. GIVEN script member (MEM): SSP4A1 WHEN script translation job (GENASTL, step SSP4A1) runs THEN ITPSTL translates member 'SSP4A1' and prints its listing and SEQOUT output (UP-C02-AC-06; UP-BR-008)
8. GIVEN script member (MEM): SSP1I1 WHEN script translation job (GENASTL, step SSP1I1) runs THEN ITPSTL translates member 'SSP1I1' and prints its listing and SEQOUT output (UP-C02-AC-07; UP-BR-009)
9. GIVEN script member (MEM): SSP3D1 WHEN script translation job (GENASTL, step SSP3D1) runs THEN ITPSTL translates member 'SSP3D1' and prints its listing and SEQOUT output (UP-C02-AC-08; UP-BR-010)
10. GIVEN script member (MEM): #SSVARS WHEN script translation job (GENASTL, step #SSVARS) runs THEN ITPSTL translates member '#SSVARS' and prints its listing and SEQOUT output (UP-C02-AC-09; UP-BR-011)
11. GIVEN script member (MEM): SSP2U1 WHEN script translation job (GENASTL, step SSP2U1) runs THEN ITPSTL translates member 'SSP2U1' and prints its listing and SEQOUT output (UP-C02-AC-10; UP-BR-012)
12. GIVEN script member (MEM): SSP3I1 WHEN script translation job (GENASTL, step SSP3I1) runs THEN ITPSTL translates member 'SSP3I1' and prints its listing and SEQOUT output (UP-C02-AC-11; UP-BR-013)
13. GIVEN script member (MEM): SSC1I1 WHEN script translation job (GENASTL, step SSC1I1) runs THEN ITPSTL translates member 'SSC1I1' and prints its listing and SEQOUT output (UP-C02-AC-12; UP-BR-014)
14. GIVEN step: SSP2A1; member (MEM): 'SSP2A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP2A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output; the SYSUT1 work area is not kept. (UP-C02-AC-13; UP-BR-015)
15. GIVEN step: SSP2D1; member (MEM): 'SSP2D1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP2D1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-14; UP-BR-016)
16. GIVEN step: SSP1U1; member (MEM): 'SSP1U1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1U1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-15; UP-BR-017)
17. GIVEN step: SSP3A1; member (MEM): 'SSP3A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP3A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-16; UP-BR-018)
18. GIVEN step: SSP4I1; member (MEM): 'SSP4I1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP4I1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-17; UP-BR-019)
19. GIVEN step: SSP1A1; member (MEM): 'SSP1A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-18; UP-BR-020)
20. GIVEN step: SSP1D1; member (MEM): 'SSP1D1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1D1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's message class (H). (UP-C02-AC-19; UP-BR-021)
21. GIVEN step: WSC1A1; member (MEM): 'WSC1A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(WSC1A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-20; UP-BR-022)

### Requirement 4: UP-REQ-F-005 (design note)

#### Acceptance criteria

1. When a script translation step runs, the system shall print the translator listing and its sequential output (SEQOUT) to the job output. (rules UP-BR-003, UP-BR-004, UP-BR-005, UP-BR-006, UP-BR-007, UP-BR-008, UP-BR-009, UP-BR-010, UP-BR-011, UP-BR-012, UP-BR-013, UP-BR-014, UP-BR-015, UP-BR-016, UP-BR-017, UP-BR-018, UP-BR-019, UP-BR-020, UP-BR-021, UP-BR-022)
2. GIVEN script member (MEM): WSC1I1 WHEN script translation job (GENASTL, step WSC1I1) runs THEN ITPSTL translates member 'WSC1I1' and prints its listing and SEQOUT output (UP-C02-AC-01; UP-BR-003)
3. GIVEN script member (MEM): STOP WHEN script translation job (GENASTL, step STOP) runs THEN ITPSTL translates member 'STOP' and prints its listing and SEQOUT output (UP-C02-AC-02; UP-BR-004)
4. GIVEN script member (MEM): SSP4D1 WHEN script translation job (GENASTL, step SSP4D1) runs THEN ITPSTL translates member 'SSP4D1' and prints its listing and SEQOUT output (UP-C02-AC-03; UP-BR-005)
5. GIVEN script member (MEM): SSP2I1 WHEN script translation job (GENASTL, step SSP2I1) runs THEN ITPSTL translates member 'SSP2I1' and prints its listing and SEQOUT output (UP-C02-AC-04; UP-BR-006)
6. GIVEN script member (MEM): SSC1A1 WHEN script translation job (GENASTL, step SSC1A1) runs THEN ITPSTL translates member 'SSC1A1' and prints its listing and SEQOUT output (UP-C02-AC-05; UP-BR-007)
7. GIVEN script member (MEM): SSP4A1 WHEN script translation job (GENASTL, step SSP4A1) runs THEN ITPSTL translates member 'SSP4A1' and prints its listing and SEQOUT output (UP-C02-AC-06; UP-BR-008)
8. GIVEN script member (MEM): SSP1I1 WHEN script translation job (GENASTL, step SSP1I1) runs THEN ITPSTL translates member 'SSP1I1' and prints its listing and SEQOUT output (UP-C02-AC-07; UP-BR-009)
9. GIVEN script member (MEM): SSP3D1 WHEN script translation job (GENASTL, step SSP3D1) runs THEN ITPSTL translates member 'SSP3D1' and prints its listing and SEQOUT output (UP-C02-AC-08; UP-BR-010)
10. GIVEN script member (MEM): #SSVARS WHEN script translation job (GENASTL, step #SSVARS) runs THEN ITPSTL translates member '#SSVARS' and prints its listing and SEQOUT output (UP-C02-AC-09; UP-BR-011)
11. GIVEN script member (MEM): SSP2U1 WHEN script translation job (GENASTL, step SSP2U1) runs THEN ITPSTL translates member 'SSP2U1' and prints its listing and SEQOUT output (UP-C02-AC-10; UP-BR-012)
12. GIVEN script member (MEM): SSP3I1 WHEN script translation job (GENASTL, step SSP3I1) runs THEN ITPSTL translates member 'SSP3I1' and prints its listing and SEQOUT output (UP-C02-AC-11; UP-BR-013)
13. GIVEN script member (MEM): SSC1I1 WHEN script translation job (GENASTL, step SSC1I1) runs THEN ITPSTL translates member 'SSC1I1' and prints its listing and SEQOUT output (UP-C02-AC-12; UP-BR-014)
14. GIVEN step: SSP2A1; member (MEM): 'SSP2A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP2A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output; the SYSUT1 work area is not kept. (UP-C02-AC-13; UP-BR-015)
15. GIVEN step: SSP2D1; member (MEM): 'SSP2D1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP2D1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-14; UP-BR-016)
16. GIVEN step: SSP1U1; member (MEM): 'SSP1U1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1U1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-15; UP-BR-017)
17. GIVEN step: SSP3A1; member (MEM): 'SSP3A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP3A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-16; UP-BR-018)
18. GIVEN step: SSP4I1; member (MEM): 'SSP4I1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP4I1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-17; UP-BR-019)
19. GIVEN step: SSP1A1; member (MEM): 'SSP1A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-18; UP-BR-020)
20. GIVEN step: SSP1D1; member (MEM): 'SSP1D1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(SSP1D1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's message class (H). (UP-C02-AC-19; UP-BR-021)
21. GIVEN step: WSC1A1; member (MEM): 'WSC1A1' WHEN the script translation job (GENASTL) runs THEN ITPSTL reads <WSIMWSX>(WSC1A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output. (UP-C02-AC-20; UP-BR-022)
