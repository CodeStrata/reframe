# Requirements: View pending authorization details (CAFM-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

Lets a card operations user open one pending authorization from an account's list and see all of it: card, date and time, approved amount, expiry, transaction and merchant details, and fraud status. It must always show the authorization that was selected for that account, with dates, times and amounts formatted exactly. When the account or selection is invalid, or the data cannot be read, it must show blank fields instead of stale or partial data.

**User story:** As a card operations user, I want to open a selected pending authorization and see its full details, so that I can review the transaction, merchant and fraud status of the authorization.

## Requirements

### Requirement 1: CAFM-REQ-F-115 (business rule)

#### Acceptance criteria

1. When the authorization detail screen is first opened from the pending authorization list, or the user presses Enter, the system shall read the selected authorization for the account and display its details. (rules CAFM-BR-121, CAFM-BR-122, CAFM-BR-123)
2. GIVEN account id: 00000012345; selected authorization key: K1; action: first entry from the list WHEN the authorization detail screen is first opened from the pending authorization list, or the user presses Enter THEN Authorization K1 of account 00000012345 is read and its card number, date, time, amount, response and merchant details are shown. (CAFM-C13-AC-01; CAFM-BR-121)
3. GIVEN selection on summary list: S WHEN the detail screen is entered for the first time from the summary list THEN The selected authorization's details are displayed. (CAFM-C13-AC-02; CAFM-BR-122)
4. GIVEN key: Enter WHEN the user presses Enter on the detail screen THEN The same authorization is shown again, freshly read. (CAFM-C13-AC-03; CAFM-BR-123)

### Requirement 2: CAFM-REQ-F-116 (formatting)

#### Acceptance criteria

1. When a selected authorization has been read without error, the system shall show the card number, the original authorization date (stored as YYMMDD) as MM/DD/YY and the original time (stored as HHMMSS) as HH:MM:SS. (rules CAFM-BR-124)
2. GIVEN a selected pending authorization for a numeric account, read without error, with card number 4111111111111111, original authorization date stored as 250315 and original time stored as 143005 WHEN the authorization detail screen is displayed THEN the card number shows as 4111111111111111, the authorization date shows as 03/15/25 and the authorization time shows as 14:30:05 (CAFM-C13-AC-10; CAFM-BR-124)

### Requirement 3: CAFM-REQ-F-117 (formatting)

#### Acceptance criteria

1. When a selected authorization has been read without error, the system shall show the approved amount right-aligned with two decimals and a leading '-' when it is negative. (rules CAFM-BR-125)
2. GIVEN a selected pending authorization read without error with approved amount -125.5, and another with approved amount 1234.5 WHEN each authorization's details are displayed THEN the first amount shows right-aligned as -125.50 with a leading '-', and the second shows right-aligned as 1234.50 with no '-' (CAFM-C13-AC-11; CAFM-BR-125)

### Requirement 4: CAFM-REQ-F-118 (formatting)

#### Acceptance criteria

1. When a selected authorization has been read without error, the system shall show the card expiry date (stored as four characters) as the first two characters, '/', and the last two characters. (rules CAFM-BR-126)
2. GIVEN a selected pending authorization read without error whose card expiry date is stored as the four characters 1227 WHEN the authorization details are displayed THEN the expiry date shows as 12/27 (CAFM-C13-AC-12; CAFM-BR-126)

### Requirement 5: CAFM-REQ-F-119 (formatting)

#### Acceptance criteria

1. When a selected authorization has been read without error, the system shall show the processing code, POS entry mode, message source, merchant category code, authorization type, transaction ID, match status, and the merchant name, ID, city, state and ZIP as stored. (rules CAFM-BR-127)
2. GIVEN a selected pending authorization read without error with stored processing code, POS entry mode, message source, merchant category code, authorization type, transaction ID, match status and merchant name, ID, city, state and ZIP WHEN the authorization details are displayed THEN each of those fields shows exactly the stored value, with no reformatting (CAFM-C13-AC-13; CAFM-BR-127)

### Requirement 6: CAFM-REQ-F-120 (formatting)

#### Acceptance criteria

1. When the authorization is shown and its fraud flag is 'F' (fraud confirmed) or 'R' (fraud removed), the system shall show the flag, '-', and the fraud report date, and otherwise shall show '-'. (rules CAFM-BR-128)
2. GIVEN fraud flag: (blank) WHEN the authorization's fraud flag is 'F' (fraud confirmed) or 'R' (fraud removed) THEN Fraud shows '-'. (CAFM-C13-AC-04; CAFM-BR-128)

### Requirement 7: CAFM-REQ-F-121 (business rule)

#### Acceptance criteria

1. If the account id passed in is not numeric or no authorization is selected (spaces or low-values), then the system shall not read the database, set the error flag and show the screen with all authorization detail fields blank and no message. (rules CAFM-BR-129, CAFM-BR-130)
2. GIVEN selected authorization: (blank) WHEN the account number passed in is not numeric or no authorization is selected, or a database read error occurred (error flag on) THEN The detail screen is sent with no authorization details filled in. (CAFM-C13-AC-05; CAFM-BR-129)
3. GIVEN account id: ABC; selected authorization key: K1 WHEN the account id is not numeric or no authorization is selected (spaces or low-values) THEN No read is made; the screen is shown with blank detail fields. (CAFM-C13-AC-06; CAFM-BR-130)
4. GIVEN account id: 00000012345; selected authorization key: spaces WHEN the account id is not numeric or no authorization is selected (spaces or low-values) THEN No read is made; the screen is shown with blank detail fields. (CAFM-C13-AC-07; CAFM-BR-130)

### Requirement 8: CAFM-REQ-F-122 (business rule)

#### Acceptance criteria

1. If a database read error occurred (error flag on), then the system shall leave the authorization detail fields blank. (rules CAFM-BR-129)
2. GIVEN selected authorization: (blank) WHEN the account number passed in is not numeric or no authorization is selected, or a database read error occurred (error flag on) THEN The detail screen is sent with no authorization details filled in. (CAFM-C13-AC-05; CAFM-BR-129)

### Requirement 9: CAFM-REQ-F-123 (design note)

#### Acceptance criteria

1. The system shall first read the account's pending authorization summary by account id and, only when that read succeeds (status blank or 'FW'), read the authorization detail under that account whose key matches the selected key. (rules CAFM-BR-131)
2. GIVEN account id: 00000012345; summary read status: ' '; selected authorization key: K1 WHEN Pending Authorization Retrieval runs THEN The detail with key K1 under account 00000012345 is read. (CAFM-C13-AC-08; CAFM-BR-131)

### Requirement 10: CAFM-REQ-F-124 (error handling)

#### Acceptance criteria

1. If the summary or the detail is not found (status 'GE') or the end of the database is reached (status 'GB'), then the system shall mark that no authorizations remain and skip any further read, without an error message. (rules CAFM-BR-132)
2. GIVEN account id: 00000099999; summary read status: 'GE' WHEN the summary or the detail is not found (status 'GE') or the end of the database is reached (status 'GB') THEN The detail is not read and no error message is shown. (CAFM-C13-AC-09; CAFM-BR-132)

### Requirement 11: CAFM-REQ-F-125 (error handling)

#### Acceptance criteria

1. If reading the authorization summary returns any status other than success, not found or end of database, then the system shall set the error flag and show ' System error while reading Auth Summary: Code:' followed by the status code. (rules CAFM-BR-133)
2. GIVEN a numeric account id and a selected authorization key, and reading the account's pending authorization summary returns status 'AJ' (not blank, 'FW', 'GE' or 'GB') WHEN the authorization detail screen reads the selected authorization THEN the error flag is set, the detail is not read, and the message ' System error while reading Auth Summary: Code:' followed by AJ is shown (CAFM-C13-AC-14; CAFM-BR-133)

### Requirement 12: CAFM-REQ-F-126 (error handling)

#### Acceptance criteria

1. If reading the authorization detail returns any status other than success, not found or end of database, then the system shall set the error flag and show ' System error while reading Auth Details: Code:' followed by the status code. (rules CAFM-BR-134)
2. GIVEN the account's pending authorization summary is read successfully, and reading the authorization detail with the selected key returns status 'AJ' (not success, 'GE' or 'GB') WHEN the authorization detail screen reads the selected authorization THEN the error flag is set and the message ' System error while reading Auth Details: Code:' followed by AJ is shown (CAFM-C13-AC-15; CAFM-BR-134)
