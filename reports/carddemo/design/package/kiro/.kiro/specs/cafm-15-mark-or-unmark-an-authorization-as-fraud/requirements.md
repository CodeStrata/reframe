# Requirements: Mark or unmark an authorization as fraud (CAFM-C15)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

Lets a card operations user mark a pending authorization as fraud, or remove that mark, with a single action on the detail screen. The change is recorded in two places, the authorization itself and the fraud register, and they must never disagree: both are saved together or neither is. The user is told plainly whether the authorization was marked or cleared, or why the change failed.

**User story:** As a card operations user, I want to press PF5 on an authorization to report fraud or remove a fraud mark, so that suspected fraudulent authorizations are flagged consistently in the authorization record and the fraud register.

## Requirements

### Requirement 1: CAFM-REQ-F-133 (business rule)

#### Acceptance criteria

1. When the user presses PF5 on the authorization detail screen and the selected authorization is marked fraud ('F'), the system shall set its fraud flag to 'R' (fraud removed) and request the fraud action 'R' (remove fraud). (rules CAFM-BR-143, CAFM-BR-144, CAFM-BR-145)
2. GIVEN key pressed: PF5; current fraud flag: F WHEN the user presses PF5 on the authorization detail screen and the selected authorization is marked fraud ('F') THEN The flag becomes 'R' and action 'R' (remove fraud) is requested. (CAFM-C15-AC-01; CAFM-BR-143)
3. GIVEN key: PF5; fraud flag: (blank) WHEN the user presses PF5 on the detail screen THEN The fraud marking process runs for the selected authorization and the screen is redisplayed. (CAFM-C15-AC-02; CAFM-BR-144)
4. GIVEN current fraud flag: 'F'; key: PF5 WHEN a user presses PF5 on the authorization detail screen THEN Action 'R' is sent to the fraud program (CAFM-C15-AC-03; CAFM-BR-145)
5. GIVEN current fraud flag: blank; key: PF5 WHEN a user presses PF5 on the authorization detail screen THEN Action 'F' is sent to the fraud program (CAFM-C15-AC-04; CAFM-BR-145)

### Requirement 2: CAFM-REQ-F-134 (business rule)

#### Acceptance criteria

1. When the user presses PF5 on the authorization detail screen and the selected authorization is not marked fraud (blank or 'R'), the system shall set its fraud flag to 'F' (fraud confirmed) and request the fraud action 'F' (report fraud). (rules CAFM-BR-146, CAFM-BR-144, CAFM-BR-145)
2. GIVEN key: PF5; fraud flag: (blank) WHEN the user presses PF5 on the detail screen THEN The fraud marking process runs for the selected authorization and the screen is redisplayed. (CAFM-C15-AC-02; CAFM-BR-144)
3. GIVEN current fraud flag: 'F'; key: PF5 WHEN a user presses PF5 on the authorization detail screen THEN Action 'R' is sent to the fraud program (CAFM-C15-AC-03; CAFM-BR-145)
4. GIVEN current fraud flag: blank; key: PF5 WHEN a user presses PF5 on the authorization detail screen THEN Action 'F' is sent to the fraud program (CAFM-C15-AC-04; CAFM-BR-145)
5. GIVEN key pressed: PF5; current fraud flag: (blank) WHEN the user presses PF5 on the authorization detail screen and the selected authorization is not marked fraud (blank or 'R') THEN The flag becomes 'F' and action 'F' (report fraud) is requested. (CAFM-C15-AC-05; CAFM-BR-146)
6. GIVEN key pressed: PF5; current fraud flag: R WHEN the user presses PF5 on the authorization detail screen and the selected authorization is not marked fraud (blank or 'R') THEN The flag becomes 'F' again and action 'F' is requested. (CAFM-C15-AC-06; CAFM-BR-146)

### Requirement 3: CAFM-REQ-F-135 (design note)

#### Acceptance criteria

1. The system shall send the whole authorization record, the account number, the customer number and the fraud action to the fraud update program (COPAUS2C). (rules CAFM-BR-147)
2. GIVEN a selected authorization with fraud flag blank, for account 00000000123 and customer 000000456 WHEN the user presses PF5 THEN the fraud update service receives the whole authorization record, account number 00000000123, customer number 000000456 and fraud action 'F' (CAFM-C15-AC-15; CAFM-BR-147)

### Requirement 4: CAFM-REQ-F-136 (business rule)

#### Acceptance criteria

1. The system shall set the fraud report date on the authorization record returned by the fraud update program to today's date in MM/DD/YY form with separators, which the detail screen then saves on the pending authorization and displays. (rules CAFM-BR-147, CAFM-BR-148)
2. GIVEN today's date is 26 November 2026 and a selected authorization not marked fraud WHEN the user presses PF5 and the fraud update succeeds THEN the authorization record returned by the fraud update carries the fraud report date 11/26/26, that date is saved on the pending authorization, and the screen shows the flag F, '-', and 11/26/26 (CAFM-C15-AC-16; CAFM-BR-147, CAFM-BR-148)

### Requirement 5: CAFM-REQ-F-137 (business rule)

#### Acceptance criteria

1. When the fraud update program completes normally and reports success ('S'), the system shall replace the pending authorization detail record (PAUTDTL1) with the record carrying the toggled fraud flag and the fraud report date set by the fraud update program. (rules CAFM-BR-149, CAFM-BR-150)
2. GIVEN fraud update status: S; new fraud flag: F WHEN the fraud update program completes normally and reports success ('S') THEN The detail is saved and 'AUTH MARKED FRAUD...' is shown. (CAFM-C15-AC-07; CAFM-BR-149)
3. GIVEN fraud update status: S; new fraud flag: R WHEN the fraud update program completes normally and reports success ('S') THEN The detail is saved and 'AUTH FRAUD REMOVED...' is shown. (CAFM-C15-AC-08; CAFM-BR-149)
4. GIVEN key pressed: PF5; fraud processor update status: S; fraud flag before: blank WHEN the user presses PF5 on the authorization detail screen and the fraud processor (COPAUS2C) reports update status 'S' THEN The IMS authorization detail record is rewritten with fraud flag 'F' and today's fraud report date. (CAFM-C15-AC-09; CAFM-BR-150)

### Requirement 6: CAFM-REQ-F-138 (business rule)

#### Acceptance criteria

1. When the replace of the authorization detail succeeds (status blank or 'FW'), the system shall commit the fraud register change and the authorization detail change together and show 'AUTH FRAUD REMOVED...' if the flag is now 'R', otherwise 'AUTH MARKED FRAUD...'. (rules CAFM-BR-149, CAFM-BR-151)
2. GIVEN fraud update status: S; new fraud flag: F WHEN the fraud update program completes normally and reports success ('S') THEN The detail is saved and 'AUTH MARKED FRAUD...' is shown. (CAFM-C15-AC-07; CAFM-BR-149)
3. GIVEN fraud update status: S; new fraud flag: R WHEN the fraud update program completes normally and reports success ('S') THEN The detail is saved and 'AUTH FRAUD REMOVED...' is shown. (CAFM-C15-AC-08; CAFM-BR-149)
4. GIVEN IMS replace status: blank; new fraud flag: F WHEN the IMS replace succeeds (status blank or 'FW') THEN Both changes are committed and 'AUTH MARKED FRAUD...' is shown. (CAFM-C15-AC-10; CAFM-BR-151)
5. GIVEN IMS replace status: FW; new fraud flag: R WHEN the IMS replace succeeds (status blank or 'FW') THEN Both changes are committed and 'AUTH FRAUD REMOVED...' is shown. (CAFM-C15-AC-11; CAFM-BR-151)

### Requirement 7: CAFM-REQ-N-003 (error handling)

#### Acceptance criteria

1. If the replace of the authorization detail returns any other status, then the system shall roll back both the fraud register change and the authorization detail change, set the error flag and show ' System error while FRAUD Tagging, ROLLBACK\|\|' followed by the database status code. (rules CAFM-BR-152, CAFM-BR-153)
2. GIVEN a selected authorization marked fraud ('F'), the fraud update program reports success ('S'), and the replace of the authorization detail returns a status other than blank or 'FW', for example 'AI' WHEN the user presses PF5 THEN both the fraud register change and the authorization detail change are rolled back, the error flag is set, the message ' System error while FRAUD Tagging, ROLLBACK\|\|' followed by AI is shown, and the stored authorization keeps fraud flag 'F' (CAFM-C15-AC-17; CAFM-BR-152, CAFM-BR-153)

### Requirement 8: CAFM-REQ-F-139 (error handling)

#### Acceptance criteria

1. If the fraud update program completes but reports failure, then the system shall roll back, leave the authorization detail unchanged and show the fraud program's message (for example ' SYSTEM ERROR DB2: CODE:…'). (rules CAFM-BR-154)
2. GIVEN fraud update status: F; fraud program message: UPDT ERROR DB2: CODE:-911, STATE: 40001 WHEN the fraud update program completes but reports failure THEN The change is rolled back and that message is shown. (CAFM-C15-AC-12; CAFM-BR-154)

### Requirement 9: CAFM-REQ-F-140 (error handling)

#### Acceptance criteria

1. If the link to the fraud update program does not complete normally, then the system shall roll back and leave the authorization detail unchanged, without setting any message. (rules CAFM-BR-155)
2. GIVEN link result: not NORMAL WHEN the link to the fraud update program does not complete normally THEN The change is rolled back and no message is shown. (CAFM-C15-AC-13; CAFM-BR-155)

### Requirement 10: CAFM-REQ-F-141 (business rule)

#### Acceptance criteria

1. When a PF5 fraud action finishes, the system shall redisplay the same authorization's details. (rules CAFM-BR-156, CAFM-BR-144)
2. GIVEN key: PF5; fraud flag: (blank) WHEN the user presses PF5 on the detail screen THEN The fraud marking process runs for the selected authorization and the screen is redisplayed. (CAFM-C15-AC-02; CAFM-BR-144)
3. GIVEN key pressed: PF5 WHEN a PF5 fraud action finishes THEN The detail screen is shown again for the same authorization, with the result message. (CAFM-C15-AC-14; CAFM-BR-156)
