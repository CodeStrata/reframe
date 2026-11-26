# Requirements: Endowment (life) policy inquire, add, delete and update (UP2-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unassigned programs · Unassigned programs · runs as online and scheduled job · risk high

## Introduction

Lets policy administrators look up, add, delete and update a customer's endowment (life) policy: fund, term, sum assured, life assured and the with-profits, managed-fund and equities indicators. Policies entered here always carry payment 0 and no broker, a failed add must be rolled back, and every failure must clear the screen ready for the next attempt. In the legacy screen the add-failure message ('Customer does not exist' or 'Error Adding Life Policy') goes to the motor screen's message field, so the user never sees it; the team must decide whether to keep that behaviour on purpose.

**User story:** As a policy administrator, I want to inquire on, add, delete and update endowment (life) policies from the endowment policy screen, so that customers' life cover is recorded correctly.

## Requirements

### Requirement 1: UP2-REQ-F-029 (business rule)

#### Acceptance criteria

1. The system shall treat endowment policy screen option '1' as inquire (LGIPOL01), '2' as add (LGAPOL01), '3' as delete (LGDPOL01) and '4' as inquire-then-update (LGIPOL01 then LGUPOL01). (rules UP2-BR-023)
2. GIVEN Option: 3; Customer number: 0000000001; Policy number: 0000000001 WHEN endowment policy screen runs THEN The delete program is called with request '01DEND'; on success 'Life Policy Deleted' is shown. (UP2-C03-AC-01; UP2-BR-023)

### Requirement 2: UP2-REQ-F-030 (business rule)

#### Acceptance criteria

1. If the operator presses Enter on the endowment policy screen with an option other than '1', '2', '3' or '4', then the system shall call no back-end program, show 'Please enter a valid option' with the cursor on the option field, and wait for the next input under transaction SSP2. (rules UP2-BR-024)
2. GIVEN Option: 7 WHEN the operator presses Enter on the endowment policy screen with an option other than '1', '2', '3' or '4' THEN 'Please enter a valid option' is shown and the cursor sits on the option field. (UP2-C03-AC-02; UP2-BR-024)
3. GIVEN Option: (blank) WHEN the operator presses Enter on the endowment policy screen with an option other than '1', '2', '3' or '4' THEN 'Please enter a valid option' is shown; nothing is inquired, added, deleted or updated. (UP2-C03-AC-03; UP2-BR-024)

### Requirement 3: UP2-REQ-F-031 (formatting)

#### Acceptance criteria

1. When the operator presses PF3 on the endowment policy screen, the system shall end the transaction with 'Transaction ended'. (rules UP2-BR-025)
2. GIVEN Key pressed: PF3 WHEN the operator presses PF3 THEN The screen is erased and 'Transaction ended' is shown. (UP2-C03-AC-04; UP2-BR-025)
3. GIVEN Key pressed: CLEAR WHEN the operator presses PF3 THEN A blank endowment screen is shown. (UP2-C03-AC-05; UP2-BR-025)

### Requirement 4: UP2-REQ-F-032 (formatting)

#### Acceptance criteria

1. When the operator presses CLEAR on the endowment policy screen, the system shall redisplay an empty endowment screen and continue under transaction SSP2. (rules UP2-BR-025)
2. GIVEN Key pressed: PF3 WHEN the operator presses PF3 THEN The screen is erased and 'Transaction ended' is shown. (UP2-C03-AC-04; UP2-BR-025)
3. GIVEN Key pressed: CLEAR WHEN the operator presses PF3 THEN A blank endowment screen is shown. (UP2-C03-AC-05; UP2-BR-025)

### Requirement 5: UP2-REQ-F-033 (business rule)

#### Acceptance criteria

1. When the operator chooses option '1' with a customer number and policy number, the system shall look up the policy (request '01IEND') and, on success, show its issue date, expiry date, fund name, term, sum assured, life assured, with-profits, managed fund and equities. (rules UP2-BR-026)
2. GIVEN Option: 1; Customer number: 0000000001; Policy number: 0000000001; Return code: 0 WHEN the operator chooses option '1' with a customer number and policy number THEN The policy's dates, fund name, term, sum assured, life assured and fund flags are shown. (UP2-C03-AC-06; UP2-BR-026)

### Requirement 6: UP2-REQ-F-034 (error handling)

#### Acceptance criteria

1. If the endowment policy inquiry returns a non-zero code, then the system shall show 'No data was returned.' and clear the screen and conversation data. (rules UP2-BR-027)
2. GIVEN Option: 1; Policy number: 0000009999 (not on file); Return code: 01 WHEN the endowment policy inquiry returns a non-zero code THEN 'No data was returned.' is shown. (UP2-C03-AC-07; UP2-BR-027)

### Requirement 7: UP2-REQ-F-035 (business rule)

#### Acceptance criteria

1. When the operator chooses option '2', the system shall send the customer number, issue and expiry dates, fund name, term, sum assured, life assured, with-profits, managed fund and equities for a new policy (request '01AEND'), with payment 0, broker 0 and a blank broker reference. (rules UP2-BR-028, UP2-BR-029)
2. GIVEN Option: 2; Customer number: 0000000001; Fund name: GROWTH; Term: 20; Sum assured: 100000 WHEN the operator chooses option '2' THEN A new endowment policy is requested with payment 0 and no broker. (UP2-C03-AC-08; UP2-BR-028)
3. GIVEN Request: 01UHOU; Stored broker id: 1234 WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND) THEN The update is sent with broker id 0, payment 0 and a blank broker reference (UP2-C03-AC-09; UP2-BR-029)
4. GIVEN Request: 01AEND WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND) THEN The new endowment policy is sent with payment 0, broker id 0 and a blank broker reference (UP2-C03-AC-10; UP2-BR-029)

### Requirement 8: UP2-REQ-F-036 (formatting)

#### Acceptance criteria

1. When adding the endowment policy succeeds, the system shall show the customer number, the newly assigned policy number and the fund name, clear the option field and show 'New Life Policy Inserted'. (rules UP2-BR-030)
2. GIVEN Option: 2; Return code: 0; New policy number: 0000000042 WHEN adding the endowment policy succeeds THEN Policy number 0000000042 and 'New Life Policy Inserted' are shown. (UP2-C03-AC-11; UP2-BR-030)

### Requirement 9: UP2-REQ-F-037 (error handling)

#### Acceptance criteria

1. If adding the endowment policy returns a non-zero code, then the system shall roll back the unit of work and take the add-error path. (rules UP2-BR-031)
2. GIVEN Option: 2; Return code: 70 WHEN adding the endowment policy returns a non-zero code THEN The add is rolled back and the screen is reset. (UP2-C03-AC-12; UP2-BR-031)

### Requirement 10: UP2-REQ-F-038 (error handling)

#### Acceptance criteria

1. If adding an endowment policy fails because the customer is not on file (return code 70), then the system shall roll back the unit of work, redisplay the endowment screen and clear the screen and conversation data for the next attempt. (rules UP2-BR-032)
2. GIVEN Option: 2; Customer number: 9999999999 (not on file); Back-end return code: 70 WHEN adding an endowment policy fails because the customer is not on file (return code 70) THEN The add is rolled back and the endowment screen is shown again; the next Enter starts from a cleared screen. (UP2-C03-AC-13; UP2-BR-032)

### Requirement 11: UP2-REQ-F-039 (formatting)

#### Acceptance criteria

1. If adding an endowment policy fails, then the system shall put the message 'Customer does not exist' (return code 70) or 'Error Adding Life Policy' (any other code) in the message field of the motor policy screen (ERP1FLDO), so the message does not appear on the endowment screen. (rules UP2-BR-033)
2. GIVEN Option: 2; Back-end return code: 70 WHEN adding an endowment policy fails THEN 'Customer does not exist' is not shown; the endowment screen message line stays as it was. (UP2-C03-AC-14; UP2-BR-033)
3. GIVEN Option: 2; Back-end return code: 90 WHEN adding an endowment policy fails THEN 'Error Adding Life Policy' is not shown on the endowment screen. (UP2-C03-AC-15; UP2-BR-033)

### Requirement 12: UP2-REQ-F-040 (business rule)

#### Acceptance criteria

1. When the operator chooses option '4', the system shall first show the current policy details (request '01IEND'), wait for the operator to change them and press Enter, then send the changed details for update (request '01UEND') with payment 0, broker 0 and a blank broker reference, whatever values the policy held before. (rules UP2-BR-034, UP2-BR-029)
2. GIVEN Request: 01UHOU; Stored broker id: 1234 WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND) THEN The update is sent with broker id 0, payment 0 and a blank broker reference (UP2-C03-AC-09; UP2-BR-029)
3. GIVEN Request: 01AEND WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND) THEN The new endowment policy is sent with payment 0, broker id 0 and a blank broker reference (UP2-C03-AC-10; UP2-BR-029)
4. GIVEN Option: 4; Customer number: 0000000001; Policy number: 0000000001; Term (changed): 20 to 25 WHEN the operator chooses option '4' THEN The update is sent with term 25 and the other fields as shown on the screen. (UP2-C03-AC-16; UP2-BR-034)

### Requirement 13: UP2-REQ-F-041 (error handling)

#### Acceptance criteria

1. If the first inquiry for option '4' fails, then the system shall show 'No data was returned.'. (rules UP2-BR-035)
2. GIVEN Option: 4; Update return code: 02 WHEN the endowment policy update returns a non-zero code THEN 'Error Updating Life Policy' is shown. (UP2-C03-AC-17; UP2-BR-035)
3. GIVEN Option: 4; Inquiry return code: 01 WHEN the endowment policy update returns a non-zero code THEN 'No data was returned.' is shown and no update is attempted. (UP2-C03-AC-18; UP2-BR-035)

### Requirement 14: UP2-REQ-F-042 (formatting)

#### Acceptance criteria

1. When the endowment policy update succeeds, the system shall show the customer and policy numbers, clear the option field and show 'Life Policy Updated'. (rules UP2-BR-036)
2. GIVEN Option: 4; Update return code: 0 WHEN the endowment policy update succeeds THEN 'Life Policy Updated' is shown and the option field is blank. (UP2-C03-AC-19; UP2-BR-036)

### Requirement 15: UP2-REQ-F-043 (error handling)

#### Acceptance criteria

1. If the endowment policy update returns a non-zero code, then the system shall show 'Error Updating Life Policy' and clear the screen and conversation data, without issuing a rollback. (rules UP2-BR-035)
2. GIVEN Option: 4; Update return code: 02 WHEN the endowment policy update returns a non-zero code THEN 'Error Updating Life Policy' is shown. (UP2-C03-AC-17; UP2-BR-035)
3. GIVEN Option: 4; Inquiry return code: 01 WHEN the endowment policy update returns a non-zero code THEN 'No data was returned.' is shown and no update is attempted. (UP2-C03-AC-18; UP2-BR-035)

### Requirement 16: UP2-REQ-F-044 (error handling)

#### Acceptance criteria

1. If an inquiry, add, delete or update of an endowment policy fails, then the system shall redisplay the screen with the error message, then clear the screen data and conversation data and wait for the next input under transaction SSP2. (rules UP2-BR-037)
2. GIVEN Option: 3; Delete return code: 01 WHEN an inquiry, add, delete or update of an endowment policy fails THEN 'Error Deleting Life Policy' is shown; the next Enter starts with empty conversation data. (UP2-C03-AC-20; UP2-BR-037)
3. GIVEN Option: 1; Inquiry return code: 01 WHEN an inquiry, add, delete or update of an endowment policy fails THEN 'No data was returned.' is shown and the conversation data is cleared. (UP2-C03-AC-21; UP2-BR-037)
