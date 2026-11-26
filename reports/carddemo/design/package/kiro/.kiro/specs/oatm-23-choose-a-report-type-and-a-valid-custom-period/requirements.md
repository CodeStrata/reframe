# Requirements: Choose a report type and a valid custom period (OATM-C23)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk low

## Introduction

Lets a user pick a Monthly, Yearly or Custom transaction report. If more than one is marked, the first in that order wins. For Custom, every start and end date part is checked as present, numeric, in range and a real calendar date. It must never submit a report with no type selected or with an invalid custom date, and it always points the user to the first field in error.

**User story:** As a user requesting a transaction report, I want to pick Monthly, Yearly or Custom and have my custom start and end dates checked, so that only a report with a clear, valid period is submitted.

## Requirements

### Requirement 1: OATM-REQ-F-177 (business rule)

#### Acceptance criteria

1. When more than one report type is marked, the system shall process only the first in the order Monthly, Yearly, Custom and ignore the others. (rules OATM-BR-186)
2. GIVEN Monthly: X; Yearly: X; Custom: (blank) WHEN more than one report type is marked THEN Only the Monthly report is processed (OATM-C23-AC-01; OATM-BR-186)
3. GIVEN Yearly: X; Custom: X WHEN more than one report type is marked THEN Only the Yearly report is processed (OATM-C23-AC-02; OATM-BR-186)

### Requirement 2: OATM-REQ-F-178 (business rule)

#### Acceptance criteria

1. If none of Monthly, Yearly or Custom is marked, then the system shall show 'Select a report type to print report...' with the cursor on Monthly and submit nothing. (rules OATM-BR-187)
2. GIVEN Monthly: (blank); Yearly: (blank); Custom: (blank) WHEN none of Monthly, Yearly or Custom is marked THEN Message 'Select a report type to print report...' shown, cursor on Monthly (OATM-C23-AC-03; OATM-BR-187)

### Requirement 3: OATM-REQ-F-179 (business rule)

#### Acceptance criteria

1. If a Custom report is requested and a start or end month, day or year is blank, then the system shall check the parts in the order start month, start day, start year, end month, end day, end year, show the message for the first blank part, put the cursor on that part and submit nothing. (rules OATM-BR-188)
2. GIVEN Report type: Custom; Start month: (blank); End day: (blank) WHEN a Custom report is requested and a start or end month, day or year is blank THEN Message 'Start Date - Month can NOT be empty...' is shown, cursor on start month, no job submitted (OATM-C23-AC-04; OATM-BR-188)
3. GIVEN Report type: Custom; Start date: 03/01/2024; End year: (blank) WHEN a Custom report is requested and a start or end month, day or year is blank THEN Message 'End Date - Year can NOT be empty...' is shown, cursor on end year (OATM-C23-AC-05; OATM-BR-188)

### Requirement 4: OATM-REQ-F-180 (design note)

#### Acceptance criteria

1. When all custom date parts are entered, the system shall convert each month and day to a two-digit number and each year to a four-digit number before checking them. (rules OATM-BR-189)
2. GIVEN Start month: 3; Start day: 5 WHEN all custom date parts are entered THEN The start month is treated as '03' and the start day as '05' (OATM-C23-AC-06; OATM-BR-189)

### Requirement 5: OATM-REQ-F-181 (business rule)

#### Acceptance criteria

1. If a custom start or end month is above '12' or not numeric, then the system shall show 'Start Date - Not a valid Month...' or 'End Date - Not a valid Month...', put the cursor on that month and submit nothing. (rules OATM-BR-190)
2. GIVEN Start month: 13; Start day: 01; Start year: 2024 WHEN a custom start or end month is above '12' or not numeric THEN Message 'Start Date - Not a valid Month...' is shown, cursor on start month (OATM-C23-AC-07; OATM-BR-190)

### Requirement 6: OATM-REQ-F-182 (business rule)

#### Acceptance criteria

1. If a custom start or end day is above '31' or not numeric, then the system shall show 'Start Date - Not a valid Day...' or 'End Date - Not a valid Day...', put the cursor on that day and submit nothing. (rules OATM-BR-191)
2. GIVEN End month: 04; End day: 32; End year: 2024 WHEN a custom start or end day is above '31' or not numeric THEN Message 'End Date - Not a valid Day...' is shown, cursor on end day (OATM-C23-AC-08; OATM-BR-191)

### Requirement 7: OATM-REQ-F-183 (business rule)

#### Acceptance criteria

1. If a custom start or end year is not numeric, then the system shall show 'Start Date - Not a valid Year...' or 'End Date - Not a valid Year...', put the cursor on that year and submit nothing. (rules OATM-BR-192)
2. GIVEN Start year: (not a number after conversion) WHEN a custom start or end year is not numeric THEN Message 'Start Date - Not a valid Year...' is shown, cursor on start year (OATM-C23-AC-09; OATM-BR-192)

### Requirement 8: OATM-REQ-F-184 (business rule)

#### Acceptance criteria

1. If the custom start date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date, then the system shall show 'Start Date - Not a valid date...', put the cursor on the start month and submit nothing, while accepting a date the utility reports only as outside its supported range (message number '2513'). (rules OATM-BR-193)
2. GIVEN Start date: 02/30/2024; End date: 03/15/2024 WHEN the custom start date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date THEN Message 'Start Date - Not a valid date...' is shown, cursor on start month, no job submitted (OATM-C23-AC-10; OATM-BR-193)
3. GIVEN Start date: 02/29/2024; End date: 03/15/2024 WHEN the custom start date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date THEN Start date accepted; end date is checked next (OATM-C23-AC-11; OATM-BR-193)

### Requirement 9: OATM-REQ-F-185 (business rule)

#### Acceptance criteria

1. If the custom end date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date, then the system shall show 'End Date - Not a valid date...', put the cursor on the end month and submit nothing, while accepting a date reported only as outside the supported range (message number '2513'). (rules OATM-BR-194)
2. GIVEN Start date: 01/01/2023; End date: 02/29/2023 WHEN the custom end date, checked as YYYY-MM-DD by the date utility (CSUTLDTC), is not a real calendar date THEN Message 'End Date - Not a valid date...' is shown, cursor on end month, no job submitted (OATM-C23-AC-12; OATM-BR-194)

### Requirement 10: OATM-REQ-F-186 (business rule)

#### Acceptance criteria

1. When a Custom report's dates pass every check, the system shall use the entered start and end dates as the report period, name the report 'Custom' and go on to submit the report job. (rules OATM-BR-195)
2. GIVEN Report type: Custom; Start date: 01/15/2024; End date: 02/15/2024 WHEN a Custom report's dates pass every check THEN Report period 2024-01-15 to 2024-02-15 is passed to the 'Custom' report job (OATM-C23-AC-13; OATM-BR-195)
