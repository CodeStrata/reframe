# Translate workload simulator scripts (UP-C02)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-003 | Process script member WSC1I1 | design note | THE script translation job (GENASTL, step WSC1I1) SHALL run the workload simulator script translator (ITPSTL) on script member 'WSC1I1' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:38 |
| UP-BR-004 | Process the STOP script member | design note | THE script translation job (GENASTL, step STOP) SHALL run the workload simulator script translator (ITPSTL) on script member 'STOP' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:36 |
| UP-BR-005 | Process source member SSP4D1 | design note | THE script translation job (GENASTL, step SSP4D1) SHALL run the workload simulator script translator (ITPSTL) on script member 'SSP4D1' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:34 |
| UP-BR-006 | Run script processor for member SSP2I1 | design note | THE script translation job (GENASTL, step SSP2I1) SHALL run the workload simulator script translator (ITPSTL) on script member 'SSP2I1' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:27 |
| UP-BR-007 | Run the script processor for member SSC1A1 | design note | THE script translation job (GENASTL, step SSC1A1) SHALL run the workload simulator script translator (ITPSTL) on script member 'SSC1A1' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:19 |
| UP-BR-008 | Run program for member SSP4A1 | design note | THE script translation job (GENASTL, step SSP4A1) SHALL run the workload simulator script translator (ITPSTL) on script member 'SSP4A1' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:33 |
| UP-BR-009 | Run script processor for member SSP1I1 | design note | THE script translation job (GENASTL, step SSP1I1) SHALL run the workload simulator script translator (ITPSTL) on script member 'SSP1I1' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:23 |
| UP-BR-010 | Process script member SSP3D1 | design note | THE script translation job (GENASTL, step SSP3D1) SHALL run the workload simulator script translator (ITPSTL) on script member 'SSP3D1' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:30 |
| UP-BR-011 | Process the selected script member | design note | THE script translation job (GENASTL, step #SSVARS) SHALL run the workload simulator script translator (ITPSTL) on script member '#SSVARS' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:18 |
| UP-BR-012 | Process script member SSP2U1 with ITPSTL | design note | THE script translation job (GENASTL, step SSP2U1) SHALL run the workload simulator script translator (ITPSTL) on script member 'SSP2U1' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:28 |
| UP-BR-013 | Process script member SSP3I1 | design note | THE script translation job (GENASTL, step SSP3I1) SHALL run the workload simulator script translator (ITPSTL) on script member 'SSP3I1' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:31 |
| UP-BR-014 | Process script member SSC1I1 | design note | THE script translation job (GENASTL, step SSC1I1) SHALL run the workload simulator script translator (ITPSTL) on script member 'SSC1I1' of the script library (<WSIMWSX>), reading that library and the message library (<WSIMMSX>) shared, with a temporary work file, printing its listing and sequential output (SEQOUT). | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:20 |
| UP-BR-015 | Process script member SSP2A1 | design note | WHEN the script translation job (GENASTL) runs, THE job step SSP2A1 SHALL run the script translator (ITPSTL) for script member 'SSP2A1', reading that member and the script library <WSIMWSX> as reference library, plus the message library <WSIMMSX>, all shared, with a temporary work area, and printing its listing and sequential output to the job output. | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:25 |
| UP-BR-016 | Run script processor for member SSP2D1 | design note | WHEN the script translation job (GENASTL) runs, THE job step SSP2D1 SHALL run the script translator (ITPSTL) for script member 'SSP2D1', reading that member and the script library <WSIMWSX> as reference library, plus the message library <WSIMMSX>, all shared, with a temporary work area, and printing its listing and sequential output (SEQOUT) to the job output. | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:26 |
| UP-BR-017 | Process script member SSP1U1 | design note | WHEN the script translation job (GENASTL) runs, THE job step SSP1U1 SHALL run the script translator (ITPSTL) for script member 'SSP1U1', reading that member and the script library <WSIMWSX> as include library, plus the message library <WSIMMSX>, all shared, with a temporary work file, and printing its listing and sequential output (SEQOUT) to the job output. | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:24 |
| UP-BR-018 | Process script member SSP3A1 | design note | WHEN the script translation job (GENASTL) runs, THE job step SSP3A1 SHALL run the script translator (ITPSTL) for script member 'SSP3A1', reading that member and the script library <WSIMWSX> as reference library, plus the message library <WSIMMSX>, all shared, with a temporary work area, and printing its listing and sequential output to the job output. | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:29 |
| UP-BR-019 | Process script member SSP4I1 | design note | WHEN the script translation job (GENASTL) runs, THE job step SSP4I1 SHALL run the script translator (ITPSTL) for script member 'SSP4I1', reading that member and the script library <WSIMWSX> as reference library, plus the message library <WSIMMSX>, all shared, with a temporary work area that is not kept, and printing its listing and sequential output to the job output. | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:35 |
| UP-BR-020 | Run the script processor for member SSP1A1 | design note | WHEN the script translation job (GENASTL) runs, THE job step SSP1A1 SHALL run the script translator (ITPSTL) for script member 'SSP1A1', reading that member as control input and the script library <WSIMWSX> as reference library, plus the message library <WSIMMSX>, all shared, with a temporary work data set, and printing its listing and sequential output (SEQOUT) to the job output. | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:21 |
| UP-BR-021 | Run the processor for member SSP1D1 | design note | WHEN the script translation job (GENASTL) runs, THE job step SSP1D1 SHALL run the script translator (ITPSTL) for script member 'SSP1D1', reading that member and the script library <WSIMWSX> as reference library, plus the message library <WSIMMSX>, all shared, with a temporary work file, and printing its listing and sequential output to the job's default output class. | medium | base/cntl/itpstl.jcl:1-2, base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:22 |
| UP-BR-022 | Process the selected input member | design note | WHEN the script translation job (GENASTL) runs, THE job step WSC1A1 SHALL run the script translator (ITPSTL) for member 'WSC1A1', reading that member and the source library <WSIMWSX> as reference library, plus the message library <WSIMMSX>, all shared, with a temporary work area, and printing its report and sequential output to the job output. | medium | base/cntl/itpstl.jcl:6-15, base/cntl/itpstl.jcl:37 |

### Worked examples

- UP-BR-003: script member (MEM) = WSC1I1 → ITPSTL translates member 'WSC1I1' and prints its listing and SEQOUT output
- UP-BR-004: script member (MEM) = STOP → ITPSTL translates member 'STOP' and prints its listing and SEQOUT output
- UP-BR-005: script member (MEM) = SSP4D1 → ITPSTL translates member 'SSP4D1' and prints its listing and SEQOUT output
- UP-BR-006: script member (MEM) = SSP2I1 → ITPSTL translates member 'SSP2I1' and prints its listing and SEQOUT output
- UP-BR-007: script member (MEM) = SSC1A1 → ITPSTL translates member 'SSC1A1' and prints its listing and SEQOUT output
- UP-BR-008: script member (MEM) = SSP4A1 → ITPSTL translates member 'SSP4A1' and prints its listing and SEQOUT output
- UP-BR-009: script member (MEM) = SSP1I1 → ITPSTL translates member 'SSP1I1' and prints its listing and SEQOUT output
- UP-BR-010: script member (MEM) = SSP3D1 → ITPSTL translates member 'SSP3D1' and prints its listing and SEQOUT output
- UP-BR-011: script member (MEM) = #SSVARS → ITPSTL translates member '#SSVARS' and prints its listing and SEQOUT output
- UP-BR-012: script member (MEM) = SSP2U1 → ITPSTL translates member 'SSP2U1' and prints its listing and SEQOUT output
- UP-BR-013: script member (MEM) = SSP3I1 → ITPSTL translates member 'SSP3I1' and prints its listing and SEQOUT output
- UP-BR-014: script member (MEM) = SSC1I1 → ITPSTL translates member 'SSC1I1' and prints its listing and SEQOUT output
- UP-BR-015: step = SSP2A1; member (MEM) = 'SSP2A1' → ITPSTL reads <WSIMWSX>(SSP2A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output; the SYSUT1 work area is not kept.
- UP-BR-016: step = SSP2D1; member (MEM) = 'SSP2D1' → ITPSTL reads <WSIMWSX>(SSP2D1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output.
- UP-BR-017: step = SSP1U1; member (MEM) = 'SSP1U1' → ITPSTL reads <WSIMWSX>(SSP1U1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output.
- UP-BR-018: step = SSP3A1; member (MEM) = 'SSP3A1' → ITPSTL reads <WSIMWSX>(SSP3A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output.
- UP-BR-019: step = SSP4I1; member (MEM) = 'SSP4I1' → ITPSTL reads <WSIMWSX>(SSP4I1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output.
- UP-BR-020: step = SSP1A1; member (MEM) = 'SSP1A1' → ITPSTL reads <WSIMWSX>(SSP1A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output.
- UP-BR-021: step = SSP1D1; member (MEM) = 'SSP1D1' → ITPSTL reads <WSIMWSX>(SSP1D1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's message class (H).
- UP-BR-022: step = WSC1A1; member (MEM) = 'WSC1A1' → ITPSTL reads <WSIMWSX>(WSC1A1), uses <WSIMWSX> and <WSIMMSX> as libraries, and writes SYSPRINT and SEQOUT to the job's printed output.

## Decision tables

None.

## Design notes

- UP-BR-003: One independent step of the translation job translates script 'WSC1I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-004: One independent step of the translation job translates script 'STOP' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-005: One independent step of the translation job translates script 'SSP4D1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-006: One independent step of the translation job translates script 'SSP2I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-007: One independent step of the translation job translates script 'SSC1A1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-008: One independent step of the translation job translates script 'SSP4A1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-009: One independent step of the translation job translates script 'SSP1I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-010: One independent step of the translation job translates script 'SSP3D1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-011: One independent step of the translation job translates script '#SSVARS' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator. The job must accept a script name that starts with '#'.
- UP-BR-012: One independent step of the translation job translates script 'SSP2U1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-013: One independent step of the translation job translates script 'SSP3I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-014: One independent step of the translation job translates script 'SSC1I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-015: One independent step of the translation job translates script 'SSP2A1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-016: One independent step of the translation job translates script 'SSP2D1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-017: One independent step of the translation job translates script 'SSP1U1' from the script library, using that library as its include library and taking message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-018: One independent step of the translation job translates script 'SSP3A1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-019: One independent step of the translation job translates script 'SSP4I1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is not kept after the step, and keeps its listing and sequential output for the operator.
- UP-BR-020: One independent step of the translation job translates script 'SSP1A1', read as the step's control input, from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its listing and sequential output for the operator.
- UP-BR-021: One independent step of the translation job translates script 'SSP1D1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and writes its listing and sequential output to the job's default output.
- UP-BR-022: One independent step of the translation job translates script 'WSC1A1' from the script library. It resolves references against that library and takes message texts from the message library, both read-only and shared. It uses a scratch work file that is deleted when the step ends, and keeps its report and sequential output for the operator.

## Open questions

- SME-023: What does the script processing program do with its member, library and message inputs, and what should its listing and output file contain? (Workload simulation team) On UP-BR-003, UP-BR-004, UP-BR-005, UP-BR-006, UP-BR-007, UP-BR-008, UP-BR-009, UP-BR-010, UP-BR-011, UP-BR-012, UP-BR-013, UP-BR-014, UP-BR-015, UP-BR-016, UP-BR-017, UP-BR-018, UP-BR-019, UP-BR-020, UP-BR-021, UP-BR-022.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (20 in all).
