# Requirements: House policy add, delete and update (UP2-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unassigned programs · Unassigned programs · runs as online and scheduled job · risk high

## Introduction

Lets policy administrators add, delete and update a customer's house policy: property type, bedrooms, value, house name, number and postcode. Policies entered here always carry payment 0 and no broker, replacing whatever was stored before, and a failed add or delete must be rolled back. In the legacy screen a failed add resets the screen without showing 'Customer does not exist' or 'Error Adding House Policy'; the team must decide whether to keep that.

**User story:** As a policy administrator, I want to add, delete and update house policies from the house policy screen, so that customers' property cover is recorded correctly.

## Requirements

### Requirement 1: UP2-REQ-F-045 (business rule)

#### Acceptance criteria

1. When option '2' is entered on the house policy screen, the system shall add a house policy (request 01AHOU to LGAPOL01) from the entered customer number, dates, property type, bedrooms, value, house name, house number and postcode, with payment 0, broker id 0 and a blank broker reference. (rules UP2-BR-038, UP2-BR-029)
2. GIVEN Customer number: 0000000001; Property type: DETACHED; Bedrooms: 003; Value: 00250000; Option: 2 WHEN option '2' is entered on the house policy screen THEN A house policy is added for customer 0000000001 (UP2-C04-AC-01; UP2-BR-038)
3. GIVEN Request: 01UHOU; Stored broker id: 1234 WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND) THEN The update is sent with broker id 0, payment 0 and a blank broker reference (UP2-C04-AC-02; UP2-BR-029)
4. GIVEN Request: 01AEND WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND) THEN The new endowment policy is sent with payment 0, broker id 0 and a blank broker reference (UP2-C04-AC-03; UP2-BR-029)

### Requirement 2: UP2-REQ-F-046 (formatting)

#### Acceptance criteria

1. When the house policy add succeeds, the system shall show the customer number, the newly assigned policy number and 'New House Policy Inserted', and clear the option. (rules UP2-BR-039)
2. GIVEN Option: 2; Return code: 00 WHEN the house policy add succeeds THEN The assigned policy number and 'New House Policy Inserted' are shown (UP2-C04-AC-04; UP2-BR-039)

### Requirement 3: UP2-REQ-F-047 (error handling)

#### Acceptance criteria

1. If the house policy add returns a non-zero code, then the system shall roll back the unit of work and reset the screen, without the intended message 'Customer does not exist' (code 70) or 'Error Adding House Policy' being shown on the house screen. (rules UP2-BR-040)
2. GIVEN Customer number: 0000000999; Return code: 70 WHEN the house policy add returns a non-zero code THEN The add is rolled back; the house screen is redisplayed without the 'Customer does not exist' message (UP2-C04-AC-05; UP2-BR-040)

### Requirement 4: UP2-REQ-F-048 (business rule)

#### Acceptance criteria

1. When option '3' is entered on the house policy screen (transaction SSP3), the system shall delete the house policy (request 01DHOU to LGDPOL01) and on success blank the dates and property details, clear the option and show 'House Policy Deleted'. (rules UP2-BR-041)
2. GIVEN Customer number: 0000000001; Policy number: 0000000002; Option: 3; Return code: 00 WHEN option '3' is entered on the house policy screen (transaction SSP3) THEN 'House Policy Deleted' is shown with the policy details blank (UP2-C04-AC-06; UP2-BR-041)

### Requirement 5: UP2-REQ-F-049 (error handling)

#### Acceptance criteria

1. If the house policy delete returns a non-zero code, then the system shall roll back the unit of work, show 'Error Deleting House Policy' and reset the screen and request data. (rules UP2-BR-042)
2. GIVEN Option: 3; Return code: 81 WHEN the house policy delete returns a non-zero code THEN The delete is rolled back and 'Error Deleting House Policy' is shown (UP2-C04-AC-07; UP2-BR-042)

### Requirement 6: UP2-REQ-F-050 (business rule)

#### Acceptance criteria

1. When option '4' is entered on the house policy screen, the system shall first display the current house policy (request 01IHOU), then send the edited values as an update (request 01UHOU to LGUPOL01) with payment 0, broker id 0 and a blank broker reference, whatever values the policy held before. (rules UP2-BR-043, UP2-BR-029)
2. GIVEN Request: 01UHOU; Stored broker id: 1234 WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND) THEN The update is sent with broker id 0, payment 0 and a blank broker reference (UP2-C04-AC-02; UP2-BR-029)
3. GIVEN Request: 01AEND WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND) THEN The new endowment policy is sent with payment 0, broker id 0 and a blank broker reference (UP2-C04-AC-03; UP2-BR-029)
4. GIVEN Policy number: 0000000002; Value: 00250000 edited to 00275000; Option: 4 WHEN option '4' is entered on the house policy screen THEN The update is sent with value 00275000 (UP2-C04-AC-08; UP2-BR-043)

### Requirement 7: UP2-REQ-F-051 (business rule)

#### Acceptance criteria

1. If the current house policy cannot be read for option '4', then the system shall show 'No data was returned.'. (rules UP2-BR-043)
2. GIVEN Policy number: 0000000002; Value: 00250000 edited to 00275000; Option: 4 WHEN option '4' is entered on the house policy screen THEN The update is sent with value 00275000 (UP2-C04-AC-08; UP2-BR-043)

### Requirement 8: UP2-REQ-F-052 (error handling)

#### Acceptance criteria

1. When the house policy update succeeds, the system shall show 'House Policy Updated' and clear the option. (rules UP2-BR-044)
2. GIVEN Return code: 00 WHEN the house policy update succeeds THEN 'House Policy Updated' is shown (UP2-C04-AC-09; UP2-BR-044)
3. GIVEN Return code: 02 WHEN the house policy update succeeds THEN 'Error Updating House Policy' is shown (UP2-C04-AC-10; UP2-BR-044)

### Requirement 9: UP2-REQ-F-053 (error handling)

#### Acceptance criteria

1. If the house policy update returns a non-zero code, then the system shall show 'Error Updating House Policy' and reset the screen, without a rollback. (rules UP2-BR-044)
2. GIVEN Return code: 00 WHEN the house policy update succeeds THEN 'House Policy Updated' is shown (UP2-C04-AC-09; UP2-BR-044)
3. GIVEN Return code: 02 WHEN the house policy update succeeds THEN 'Error Updating House Policy' is shown (UP2-C04-AC-10; UP2-BR-044)
