# Requirements: Commercial property policy inquire, add and delete (UP2-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unassigned programs · Unassigned programs · runs as online and scheduled job · risk high

## Introduction

Lets policy administrators find, add and delete commercial property policies, including location, property type, the fire, crime, flood and weather perils and premiums, status and reject reason. A search uses the most specific key given: customer and policy number first, then policy number alone, then customer number alone, then postcode. A policy can only be added for an existing customer, and a failed add or delete must be rolled back.

**User story:** As a policy administrator, I want to find, add and delete commercial property policies from the commercial policy screen, so that commercial cover, perils and premiums for customers are recorded correctly.

## Requirements

### Requirement 1: UP2-REQ-F-054 (formatting)

#### Acceptance criteria

1. When the commercial policy transaction starts with no prior conversation data, the system shall show a fresh form with customer and policy numbers '0000000000' and empty peril, premium and status fields. (rules UP2-BR-045)
2. GIVEN prior conversation data: none WHEN the commercial policy transaction starts with no prior conversation data THEN Form shown with customer '0000000000' and policy '0000000000' (UP2-C05-AC-01; UP2-BR-045)

### Requirement 2: UP2-REQ-F-055 (business rule)

#### Acceptance criteria

1. If the user enters any option other than '1', '2' or '3' on the Commercial Policy menu, including a blank option, then the system shall show 'Please enter a valid option', put the cursor on the option field, and call no back-end service. (rules UP2-BR-046)
2. GIVEN option: 4 WHEN the user enters any option other than '1', '2' or '3' on the Commercial Policy menu (including a blank option) THEN 'Please enter a valid option' is shown with the cursor on the option field (UP2-C05-AC-02; UP2-BR-046)
3. GIVEN option: (blank) WHEN the user enters any option other than '1', '2' or '3' on the Commercial Policy menu (including a blank option) THEN 'Please enter a valid option' is shown; no policy service is called (UP2-C05-AC-03; UP2-BR-046)

### Requirement 3: UP2-REQ-F-056 (business rule)

#### Acceptance criteria

1. When option '1' is entered with both a customer number and a policy number (neither blank nor zero), the system shall ask the policy inquiry service (LGIPOL01) for that customer's policy using request type '01ICOM'. (rules UP2-BR-047)
2. GIVEN option: 1; customer number: 0000000123; policy number: 0000000456 WHEN option '1' is entered with both a customer number and a policy number (neither blank nor zero) THEN Request '01ICOM' is sent with both numbers (UP2-C05-AC-04; UP2-BR-047)

### Requirement 4: UP2-REQ-F-057 (business rule)

#### Acceptance criteria

1. When option '1' is entered with a policy number but no customer number, the system shall search by policy number using request type '02ICOM'. (rules UP2-BR-048)
2. GIVEN option: 1; customer number: 0000000000; policy number: 0000000456 WHEN option '1' is entered with a policy number but no customer number THEN Request '02ICOM' is sent with the policy number (UP2-C05-AC-05; UP2-BR-048)

### Requirement 5: UP2-REQ-F-058 (business rule)

#### Acceptance criteria

1. When option '1' is entered with a customer number but no policy number, the system shall search by customer number using request type '03ICOM'. (rules UP2-BR-049)
2. GIVEN option: 1; customer number: 0000000123; policy number: (blank) WHEN option '1' is entered with a customer number but no policy number THEN Request '03ICOM' is sent with customer 0000000123 (UP2-C05-AC-06; UP2-BR-049)
3. GIVEN option: 1; customer number: (blank); policy number: (blank); postcode: SO212JN WHEN option '1' is entered with a customer number but no policy number THEN Request '05ICOM' is sent with the postcode (UP2-C05-AC-07; UP2-BR-049)

### Requirement 6: UP2-REQ-F-059 (business rule)

#### Acceptance criteria

1. When option '1' is entered with neither a customer number nor a policy number but with a postcode, the system shall search by postcode using request type '05ICOM'. (rules UP2-BR-049)
2. GIVEN option: 1; customer number: 0000000123; policy number: (blank) WHEN option '1' is entered with a customer number but no policy number THEN Request '03ICOM' is sent with customer 0000000123 (UP2-C05-AC-06; UP2-BR-049)
3. GIVEN option: 1; customer number: (blank); policy number: (blank); postcode: SO212JN WHEN option '1' is entered with a customer number but no policy number THEN Request '05ICOM' is sent with the postcode (UP2-C05-AC-07; UP2-BR-049)

### Requirement 7: UP2-REQ-F-060 (formatting)

#### Acceptance criteria

1. When the policy inquiry succeeds, the system shall show the policy number, customer number, issue and expiry dates, address, postcode, latitude, longitude, customer name, property type, the fire, crime, flood and weather peril and premium values, status and reject reason. (rules UP2-BR-050)
2. GIVEN option: 1; inquiry return code: 00 WHEN the policy inquiry succeeds THEN All returned commercial policy details are displayed (UP2-C05-AC-08; UP2-BR-050)

### Requirement 8: UP2-REQ-F-061 (error handling)

#### Acceptance criteria

1. If the policy inquiry service returns a non-zero code, then the system shall show 'No data was returned.' and clear the screen data for the next entry. (rules UP2-BR-051)
2. GIVEN option: 1; inquiry return code: 01 WHEN the policy inquiry service returns a non-zero code THEN 'No data was returned.' is shown (UP2-C05-AC-09; UP2-BR-051)

### Requirement 9: UP2-REQ-F-062 (business rule)

#### Acceptance criteria

1. When option '2' is entered, the system shall send the customer number, issue and expiry dates, address, postcode, latitude, longitude, customer name, property type, peril and premium values, status and reject reason to the add-policy service (LGAPOL01) as request '01ACOM'. (rules UP2-BR-052)
2. GIVEN option: 2; customer number: 0000000123; fire premium: 150 WHEN option '2' is entered THEN Request '01ACOM' is sent to LGAPOL01 with the entered details (UP2-C05-AC-10; UP2-BR-052)

### Requirement 10: UP2-REQ-F-063 (formatting)

#### Acceptance criteria

1. When the add-policy service returns code 0, the system shall show the customer number and the newly assigned policy number, clear the option field and show 'New Commercial Policy Inserted'. (rules UP2-BR-053)
2. GIVEN option: 2; add return code: 00 WHEN the add-policy service returns code 0 THEN 'New Commercial Policy Inserted' is shown with the new policy number (UP2-C05-AC-11; UP2-BR-053)

### Requirement 11: UP2-REQ-F-064 (error handling)

#### Acceptance criteria

1. If the add-policy service returns a non-zero code, then the system shall roll back the work and show 'Customer does not exist' if the code is 70, or 'Error Adding Commercial Policy' for any other code. (rules UP2-BR-054)
2. GIVEN add return code: 70 WHEN the add-policy service returns a non-zero code THEN Work rolled back; 'Customer does not exist' shown (UP2-C05-AC-12; UP2-BR-054)
3. GIVEN add return code: 90 WHEN the add-policy service returns a non-zero code THEN Work rolled back; 'Error Adding Commercial Policy' shown (UP2-C05-AC-13; UP2-BR-054)

### Requirement 12: UP2-REQ-F-065 (business rule)

#### Acceptance criteria

1. When option '3' is entered, the system shall ask the delete-policy service (LGDPOL01) to delete the given customer's policy using request '01DCOM'. (rules UP2-BR-055)
2. GIVEN option: 3; customer number: 0000000123; policy number: 0000000456 WHEN option '3' is entered THEN Request '01DCOM' is sent to LGDPOL01 (UP2-C05-AC-14; UP2-BR-055)

### Requirement 13: UP2-REQ-F-066 (formatting)

#### Acceptance criteria

1. When the commercial policy delete succeeds (code 0), the system shall blank the expiry date, address, postcode, latitude, longitude, customer name, property type, peril and premium values, status and reject reason, clear the option field and show 'Commercial Policy Deleted'. (rules UP2-BR-056)
2. GIVEN option: 3; delete return code: 00 WHEN the delete succeeds (code 0) THEN 'Commercial Policy Deleted' is shown and the detail fields are blanked (UP2-C05-AC-15; UP2-BR-056)

### Requirement 14: UP2-REQ-F-067 (error handling)

#### Acceptance criteria

1. If the delete-policy service returns a code above 0, then the system shall roll back the work and show 'Error Deleting Commercial Policy'. (rules UP2-BR-057)
2. GIVEN option: 3; delete return code: 81 WHEN the delete-policy service returns a code above 0 THEN Work rolled back; 'Error Deleting Commercial Policy' shown (UP2-C05-AC-16; UP2-BR-057)

### Requirement 15: UP2-REQ-N-001 (design note)

#### Acceptance criteria

1. When an option has been processed, the system shall return control so the next Enter continues under transaction 'SSP4'. (rules UP2-BR-058)
2. GIVEN option: 1 WHEN an option has been processed THEN After the result is shown, the next input runs transaction 'SSP4' (UP2-C05-AC-17; UP2-BR-058)

### Requirement 16: UP2-REQ-F-068 (formatting)

#### Acceptance criteria

1. When the user presses PF3, or the commercial policy screen is received with no data, the system shall show 'Transaction ended' and end the session. (rules UP2-BR-059)
2. GIVEN key pressed: PF3 WHEN the user presses PF3, or the screen is received with no data THEN 'Transaction ended' shown; session ends (UP2-C05-AC-18; UP2-BR-059)
3. GIVEN key pressed: Clear WHEN the user presses PF3, or the screen is received with no data THEN Empty form redisplayed; transaction 'SSP4' continues (UP2-C05-AC-19; UP2-BR-059)

### Requirement 17: UP2-REQ-F-069 (formatting)

#### Acceptance criteria

1. When the user presses Clear on the commercial policy screen, the system shall redisplay an empty form and continue under 'SSP4'. (rules UP2-BR-059)
2. GIVEN key pressed: PF3 WHEN the user presses PF3, or the screen is received with no data THEN 'Transaction ended' shown; session ends (UP2-C05-AC-18; UP2-BR-059)
3. GIVEN key pressed: Clear WHEN the user presses PF3, or the screen is received with no data THEN Empty form redisplayed; transaction 'SSP4' continues (UP2-C05-AC-19; UP2-BR-059)
