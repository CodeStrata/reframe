# Feature specification: Commercial property policy inquire, add and delete

**Feature:** UP2-C05 · Unassigned programs · Unassigned programs

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP2-C05)

As a policy administrator, I want to find, add and delete commercial property policies from the commercial policy screen, so that commercial cover, perils and premiums for customers are recorded correctly.

Lets policy administrators find, add and delete commercial property policies, including location, property type, the fire, crime, flood and weather perils and premiums, status and reject reason. A search uses the most specific key given: customer and policy number first, then policy number alone, then customer number alone, then postcode. A policy can only be added for an existing customer, and a failed add or delete must be rolled back.

**Acceptance scenarios:**

1. **Given** prior conversation data: none, **when** the commercial policy transaction starts with no prior conversation data, **then** Form shown with customer '0000000000' and policy '0000000000' (UP2-C05-AC-01)
2. **Given** option: 4, **when** the user enters any option other than '1', '2' or '3' on the Commercial Policy menu (including a blank option), **then** 'Please enter a valid option' is shown with the cursor on the option field (UP2-C05-AC-02)
3. **Given** option: (blank), **when** the user enters any option other than '1', '2' or '3' on the Commercial Policy menu (including a blank option), **then** 'Please enter a valid option' is shown; no policy service is called (UP2-C05-AC-03)
4. **Given** option: 1; customer number: 0000000123; policy number: 0000000456, **when** option '1' is entered with both a customer number and a policy number (neither blank nor zero), **then** Request '01ICOM' is sent with both numbers (UP2-C05-AC-04)
5. **Given** option: 1; customer number: 0000000000; policy number: 0000000456, **when** option '1' is entered with a policy number but no customer number, **then** Request '02ICOM' is sent with the policy number (UP2-C05-AC-05)
6. **Given** option: 1; customer number: 0000000123; policy number: (blank), **when** option '1' is entered with a customer number but no policy number, **then** Request '03ICOM' is sent with customer 0000000123 (UP2-C05-AC-06)
7. **Given** option: 1; customer number: (blank); policy number: (blank); postcode: SO212JN, **when** option '1' is entered with a customer number but no policy number, **then** Request '05ICOM' is sent with the postcode (UP2-C05-AC-07)
8. **Given** option: 1; inquiry return code: 00, **when** the policy inquiry succeeds, **then** All returned commercial policy details are displayed (UP2-C05-AC-08)
9. **Given** option: 1; inquiry return code: 01, **when** the policy inquiry service returns a non-zero code, **then** 'No data was returned.' is shown (UP2-C05-AC-09)
10. **Given** option: 2; customer number: 0000000123; fire premium: 150, **when** option '2' is entered, **then** Request '01ACOM' is sent to LGAPOL01 with the entered details (UP2-C05-AC-10)
11. **Given** option: 2; add return code: 00, **when** the add-policy service returns code 0, **then** 'New Commercial Policy Inserted' is shown with the new policy number (UP2-C05-AC-11)
12. **Given** add return code: 70, **when** the add-policy service returns a non-zero code, **then** Work rolled back; 'Customer does not exist' shown (UP2-C05-AC-12)
13. **Given** add return code: 90, **when** the add-policy service returns a non-zero code, **then** Work rolled back; 'Error Adding Commercial Policy' shown (UP2-C05-AC-13)
14. **Given** option: 3; customer number: 0000000123; policy number: 0000000456, **when** option '3' is entered, **then** Request '01DCOM' is sent to LGDPOL01 (UP2-C05-AC-14)
15. **Given** option: 3; delete return code: 00, **when** the delete succeeds (code 0), **then** 'Commercial Policy Deleted' is shown and the detail fields are blanked (UP2-C05-AC-15)
16. **Given** option: 3; delete return code: 81, **when** the delete-policy service returns a code above 0, **then** Work rolled back; 'Error Deleting Commercial Policy' shown (UP2-C05-AC-16)
17. **Given** option: 1, **when** an option has been processed, **then** After the result is shown, the next input runs transaction 'SSP4' (UP2-C05-AC-17)
18. **Given** key pressed: PF3, **when** the user presses PF3, or the screen is received with no data, **then** 'Transaction ended' shown; session ends (UP2-C05-AC-18)
19. **Given** key pressed: Clear, **when** the user presses PF3, or the screen is received with no data, **then** Empty form redisplayed; transaction 'SSP4' continues (UP2-C05-AC-19)

## Requirements

### Functional requirements

- **UP2-REQ-F-054** (formatting): When the commercial policy transaction starts with no prior conversation data, the system shall show a fresh form with customer and policy numbers '0000000000' and empty peril, premium and status fields. Rules: UP2-BR-045.
- **UP2-REQ-F-055** (business rule): If the user enters any option other than '1', '2' or '3' on the Commercial Policy menu, including a blank option, then the system shall show 'Please enter a valid option', put the cursor on the option field, and call no back-end service. Rules: UP2-BR-046.
- **UP2-REQ-F-056** (business rule): When option '1' is entered with both a customer number and a policy number (neither blank nor zero), the system shall ask the policy inquiry service (LGIPOL01) for that customer's policy using request type '01ICOM'. Rules: UP2-BR-047.
- **UP2-REQ-F-057** (business rule): When option '1' is entered with a policy number but no customer number, the system shall search by policy number using request type '02ICOM'. Rules: UP2-BR-048.
- **UP2-REQ-F-058** (business rule): When option '1' is entered with a customer number but no policy number, the system shall search by customer number using request type '03ICOM'. Rules: UP2-BR-049.
- **UP2-REQ-F-059** (business rule): When option '1' is entered with neither a customer number nor a policy number but with a postcode, the system shall search by postcode using request type '05ICOM'. Rules: UP2-BR-049.
- **UP2-REQ-F-060** (formatting): When the policy inquiry succeeds, the system shall show the policy number, customer number, issue and expiry dates, address, postcode, latitude, longitude, customer name, property type, the fire, crime, flood and weather peril and premium values, status and reject reason. Rules: UP2-BR-050.
- **UP2-REQ-F-061** (error handling): If the policy inquiry service returns a non-zero code, then the system shall show 'No data was returned.' and clear the screen data for the next entry. Rules: UP2-BR-051.
- **UP2-REQ-F-062** (business rule): When option '2' is entered, the system shall send the customer number, issue and expiry dates, address, postcode, latitude, longitude, customer name, property type, peril and premium values, status and reject reason to the add-policy service (LGAPOL01) as request '01ACOM'. Rules: UP2-BR-052.
- **UP2-REQ-F-063** (formatting): When the add-policy service returns code 0, the system shall show the customer number and the newly assigned policy number, clear the option field and show 'New Commercial Policy Inserted'. Rules: UP2-BR-053.
- **UP2-REQ-F-064** (error handling): If the add-policy service returns a non-zero code, then the system shall roll back the work and show 'Customer does not exist' if the code is 70, or 'Error Adding Commercial Policy' for any other code. Rules: UP2-BR-054.
- **UP2-REQ-F-065** (business rule): When option '3' is entered, the system shall ask the delete-policy service (LGDPOL01) to delete the given customer's policy using request '01DCOM'. Rules: UP2-BR-055.
- **UP2-REQ-F-066** (formatting): When the commercial policy delete succeeds (code 0), the system shall blank the expiry date, address, postcode, latitude, longitude, customer name, property type, peril and premium values, status and reject reason, clear the option field and show 'Commercial Policy Deleted'. Rules: UP2-BR-056.
- **UP2-REQ-F-067** (error handling): If the delete-policy service returns a code above 0, then the system shall roll back the work and show 'Error Deleting Commercial Policy'. Rules: UP2-BR-057.
- **UP2-REQ-N-001** (design note): When an option has been processed, the system shall return control so the next Enter continues under transaction 'SSP4'. Rules: UP2-BR-058.
- **UP2-REQ-F-068** (formatting): When the user presses PF3, or the commercial policy screen is received with no data, the system shall show 'Transaction ended' and end the session. Rules: UP2-BR-059.
- **UP2-REQ-F-069** (formatting): When the user presses Clear on the commercial policy screen, the system shall redisplay an empty form and continue under 'SSP4'. Rules: UP2-BR-059.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP2-BR-045 | Commercial policy screen session flow and exit keys | formatting | WHEN the commercial policy transaction starts with no prior conversation data, THE commercial policy screen SHALL show a fresh form with customer and policy numbers '0000000000' and empty peril, premium and status fields. | medium | base/src/lgtestp4.cbl:32-68, base/src/lgtestp4.cbl:257-284 |
| UP2-BR-046 | Commercial policy menu option validation | business rule | WHEN the user enters any option other than '1', '2' or '3' on the Commercial Policy menu (including a blank option), THE commercial policy screen SHALL show 'Please enter a valid option', put the cursor on the option field, and call no back-end service. | medium | base/src/lgtestp4.cbl:236-247 |
| UP2-BR-047 | Commercial policy inquiry search-key precedence | business rule | WHEN option '1' is entered with both a customer number and a policy number (neither blank nor zero), THE commercial policy screen SHALL ask the policy inquiry service (LGIPOL01) for that customer's policy using request type '01ICOM'. | medium | base/src/lgtestp4.cbl:71-154, base/src/lgtestp4.cbl:304-318 |
| UP2-BR-048 | Commercial policy inquiry search-key precedence | business rule | WHEN option '1' is entered with a policy number but no customer number, THE commercial policy screen SHALL search by policy number using request type '02ICOM'. | medium | base/src/lgtestp4.cbl:71-154, base/src/lgtestp4.cbl:304-318 |
| UP2-BR-049 | Commercial policy inquiry search-key precedence | business rule | WHEN option '1' is entered with a customer number but no policy number, THE commercial policy screen SHALL search by customer number using request type '03ICOM'; WHEN neither is given but a postcode is, it SHALL search by postcode using request type '05ICOM'. | medium | base/src/lgtestp4.cbl:71-154, base/src/lgtestp4.cbl:304-318 |
| UP2-BR-050 | Commercial policy inquiry search-key precedence | formatting | WHEN the policy inquiry succeeds, THE commercial policy screen SHALL show the policy number, customer number, issue and expiry dates, address, postcode, latitude, longitude, customer name, property type, the fire, crime, flood and weather peril and premium values, status and reject reason. | medium | base/src/lgtestp4.cbl:71-154, base/src/lgtestp4.cbl:304-318 |
| UP2-BR-051 | Commercial policy inquiry search-key precedence | error handling | WHEN the policy inquiry service returns a non-zero code, THE commercial policy screen SHALL show 'No data was returned.' and clear the screen data for the next entry. | medium | base/src/lgtestp4.cbl:71-154, base/src/lgtestp4.cbl:304-318 |
| UP2-BR-052 | Add commercial property policy with rollback on failure | business rule | WHEN option '2' is entered, THE commercial policy screen SHALL send the customer number, issue and expiry dates, address, postcode, latitude, longitude, customer name, property type, peril and premium values, status and reject reason to the add-policy service (LGAPOL01) as request '01ACOM'. | medium | base/src/lgtestp4.cbl:156-195, base/src/lgtestp4.cbl:286-294 |
| UP2-BR-053 | Add commercial property policy with rollback on failure | formatting | WHEN the add-policy service returns code 0, THE commercial policy screen SHALL show the customer number and the newly assigned policy number, clear the option field and show 'New Commercial Policy Inserted'. | medium | base/src/lgtestp4.cbl:156-195, base/src/lgtestp4.cbl:286-294 |
| UP2-BR-054 | Add commercial property policy with rollback on failure | error handling | WHEN the add-policy service returns a non-zero code, THE commercial policy screen SHALL roll back the work and show 'Customer does not exist' if the code is 70, or 'Error Adding Commercial Policy' for any other code. | medium | base/src/lgtestp4.cbl:156-195, base/src/lgtestp4.cbl:286-294 |
| UP2-BR-055 | Delete commercial property policy with rollback on failure | business rule | WHEN option '3' is entered, THE commercial policy screen SHALL ask the delete-policy service (LGDPOL01) to delete the given customer's policy using request '01DCOM'. | medium | base/src/lgtestp4.cbl:197-234, base/src/lgtestp4.cbl:300-302 |
| UP2-BR-056 | Delete commercial property policy with rollback on failure | formatting | WHEN the delete succeeds (code 0), THE commercial policy screen SHALL blank the expiry date, address, postcode, latitude, longitude, customer name, property type, peril and premium values, status and reject reason, clear the option field and show 'Commercial Policy Deleted'. | medium | base/src/lgtestp4.cbl:197-234, base/src/lgtestp4.cbl:300-302 |
| UP2-BR-057 | Delete commercial property policy with rollback on failure | error handling | WHEN the delete-policy service returns a code above 0, THE commercial policy screen SHALL roll back the work and show 'Error Deleting Commercial Policy'. | medium | base/src/lgtestp4.cbl:197-234, base/src/lgtestp4.cbl:300-302 |
| UP2-BR-058 | Commercial policy screen session flow and exit keys | design note | WHEN an option has been processed, THE commercial policy screen SHALL return control so the next Enter continues under transaction 'SSP4'. | medium | base/src/lgtestp4.cbl:32-68, base/src/lgtestp4.cbl:257-284 |
| UP2-BR-059 | Commercial policy screen session flow and exit keys | formatting | WHEN the user presses PF3, or the screen is received with no data, THE commercial policy screen SHALL show 'Transaction ended' and end the session; WHEN the user presses Clear, it SHALL redisplay an empty form and continue under 'SSP4'. | medium | base/src/lgtestp4.cbl:32-68, base/src/lgtestp4.cbl:257-284 |

### Key entities

- LGCMAREA (working storage)

### Needs clarification

- SME-086: Adding a commercial property policy is undone (rolled back) if it fails. Is this rule critical to the business, or costly if it were wrong, so that it must be preserved exactly? (Commercial underwriting business owner) On UP2-BR-054.
- SME-087: Deleting a commercial property policy is undone (rolled back) if it fails. Is this rule critical to the business, or costly if it were wrong, so that it must be preserved exactly? (Commercial underwriting business owner) On UP2-BR-057.
- DEF-059: Is this intended? When option '1' is entered with no customer number, policy number or postcode, no request type is set and LGIPOL01 is still called with whatever request id the communication area holds, so the user sees 'No data was returned.' (or an unexpected result) instead of a prompt to enter a search key. (Subject-matter expert) On UP2-BR-051.
- DEF-065: Is this intended? After a successful delete the issue date is left on the screen while every other policy detail is blanked. (Subject-matter expert) On UP2-BR-057.

### Decision table gaps

- Commercial policy inquiry search key: No rule says what happens when option '1' is entered with no customer number, policy number or postcode.
