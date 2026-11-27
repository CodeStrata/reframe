# Feature specification: Validate and look up an account for viewing

**Feature:** OATM-C16 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C16)

As a user, I want the account number I enter to be checked and the account and its customer looked up, so that I see the right account or a clear reason why it could not be shown.

Checks the 11-digit account number a user enters on the Account View screen. It then finds the account's linked card and customer, the account itself and the customer's profile. It must never show details for an invalid or unknown number, and every lookup that fails must give a clear message naming which record could not be found or read.

**Acceptance scenarios:**

1. **Given** Account number: '*', **when** the account number entered on the Account View screen is '*' or blank, **then** Handled exactly like a blank account number (OATM-C16-AC-01)
2. **Given** Account number: blank, **when** no account number is supplied, **then** Message 'No input received'; the account field shows '*' in red; no file is read (OATM-C16-AC-02)
3. **Given** Account number: ABC12345678, **when** the account number supplied is not all digits (including one shorter than 11 digits) or is all zeros, **then** Message 'Account Filter must be a non-zero 11 digit number' (OATM-C16-AC-03)
4. **Given** Account number: 00000000000, **when** the account number supplied is not all digits (including one shorter than 11 digits) or is all zeros, **then** Message 'Account Filter must be a non-zero 11 digit number' (OATM-C16-AC-04)
5. **Given** Account number: 00000012345, **when** the account number is 11 digits and not all zeros, **then** Accepted; the card cross-reference is read for account 00000012345 (OATM-C16-AC-05)
6. **Given** Account number: 00000012345; Cross-reference entry: customer 000000123, card 4111111111111111, **when** an account number passes validation on the Account View screen, **then** Customer 000000123 and card 4111111111111111 are kept for the session and the account master is read next (OATM-C16-AC-06)
7. **Given** Account number: 00000012345; Account master: record exists, **when** the account is found in the cross-reference, **then** The account is marked as found and its status, balances, limits and dates are displayed (OATM-C16-AC-07)
8. **Given** Account master: no record for 00000012345; Customer master: customer 000000123 exists, **when** reading the account master does not succeed, **then** The customer is still read and shown, the account fields are shown from an empty record, and the account 'not found' message is still shown (OATM-C16-AC-08)
9. **Given** Cross-reference customer: 000000123; Customer master: record exists, **when** account view runs, **then** The customer's name, address, phones, SSN and FICO score are displayed (OATM-C16-AC-09)
10. **Given** program context: 1; account number: 00000000000, **when** PF3 was not pressed and the program context is re-entry (1), **then** Screen redisplayed with 'Account number must be a non zero 11 digit number' (OATM-C16-AC-10)
11. **Given** program context: 1; account number: 00000012345; cross-reference, account, customer: all found, **when** PF3 was not pressed and the program context is re-entry (1), **then** Screen shows account and customer details (OATM-C16-AC-11)
12. **Given** Account number 00000012345 passes validation but has no entry in the card cross-reference by account, **when** The user submits the Account View screen, **then** The lookup stops without reading the account or customer, the request is treated as an input error, the account number is shown in red, and the message 'Account:00000012345 not found in Cross ref file. Resp:<code> Reas:<code>' is shown with the response and reason codes from the failed read (OATM-C16-AC-12)
13. **Given** Account number 00000012345 passes validation and reading the card cross-reference fails for a reason other than not found, **when** The user submits the Account View screen, **then** The lookup stops, the request is treated as an input error, and the message 'File Error: READ on CXACAIX returned RESP <code>,RESP2 <code>' is shown with the codes from the failed read (OATM-C16-AC-13)
14. **Given** Account 00000012345 is found in the card cross-reference but is not in the account master, **when** The user submits the Account View screen, **then** The request is treated as an input error, the account number is shown in red and the message 'Account:00000012345 not found in Acct Master file.Resp:<code> Reas:<code>' is shown (OATM-C16-AC-14)
15. **Given** Account 00000012345 is found in the card cross-reference and reading the account master fails for a reason other than not found, **when** The user submits the Account View screen, **then** The message 'File Error: READ on ACCTDAT returned RESP <code>,RESP2 <code>' is shown with the codes from the failed read (OATM-C16-AC-15)
16. **Given** Account 00000012345 is found in the cross-reference and the account master, its cross-reference gives customer number 000000099, no message has been set yet, and that customer is not in the customer master, **when** The user submits the Account View screen, **then** The request is treated as an input error and the message 'CustId:000000099 not found in customer master.Resp: <code> REAS:<code>' is shown (OATM-C16-AC-16)
17. **Given** An earlier lookup step has already set a message, and the customer is then not found in the customer master, **when** The user submits the Account View screen, **then** The earlier message is kept and the customer-not-found message is not shown (OATM-C16-AC-17)
18. **Given** An earlier message is already set, and reading the customer master fails for a reason other than not found, **when** The user submits the Account View screen, **then** The request is treated as an input error and the earlier message is replaced by 'File Error: READ on CUSTDAT returned RESP <code>,RESP2 <code>' (OATM-C16-AC-18)

## Requirements

### Functional requirements

- **OATM-REQ-F-123** (business rule): When the account number entered on the Account View screen is '*' or blank, the system shall treat the account number as not supplied. Rules: OATM-BR-126.
- **OATM-REQ-F-124** (business rule): If no account number is supplied, then the system shall reject the request as an input error without reading any file, set the session account to zero, show 'No input received', and redisplay the account field as '*' in red. Rules: OATM-BR-127.
- **OATM-REQ-F-125** (business rule): If the account number supplied is not all digits (including one shorter than 11 digits) or is all zeros, then the system shall reject it as an input error without reading any file, set the session account to zero, show the account field in red and show 'Account Filter must be a non-zero 11 digit number'. Rules: OATM-BR-128.
- **OATM-REQ-F-126** (business rule): When the account number is 11 digits and not all zeros, the system shall accept it as the session account and go on to the account lookup. Rules: OATM-BR-129.
- **OATM-REQ-F-127** (design note): When an account number passes validation, the system shall look the account up in the card cross-reference by account number (CXACAIX) and, when it is found, keep that account's customer number and card number for the rest of the session. Rules: OATM-BR-130.
- **OATM-REQ-F-128** (business rule): If the account is not in the card cross-reference, then the system shall stop the lookup, treat it as an input error, show the account number in red and show 'Account:<account number> not found in Cross ref file. Resp:<code> Reas:<code>'. Rules: OATM-BR-131.
- **OATM-REQ-F-129** (error handling): If reading the card cross-reference fails for any reason other than 'not found', then the system shall stop the lookup, treat it as an input error and show 'File Error: READ on CXACAIX returned RESP <code>,RESP2 <code>'. Rules: OATM-BR-132.
- **OATM-REQ-F-130** (design note): When the account is found in the cross-reference, the system shall read the account master (ACCTDAT) by account number and, on success, mark the account as found so that its details are displayed. Rules: OATM-BR-133.
- **OATM-REQ-F-131** (error handling): If the account is not in the account master, then the system shall treat it as an input error, show the account number in red and show 'Account:<account number> not found in Acct Master file.Resp:<code> Reas:<code>', and for any other read failure show 'File Error: READ on ACCTDAT returned RESP <code>,RESP2 <code>'. Rules: OATM-BR-134.
- **OATM-REQ-F-132** (error handling): If reading the account master does not succeed, then the system shall still go on to read the customer master, because the stop check after the account read never triggers. Rules: OATM-BR-135.
- **OATM-REQ-F-133** (design note): The system shall read the customer master (CUSTDAT) using the customer number taken from the card cross-reference and, on success, mark the customer as found so that the customer details are displayed. Rules: OATM-BR-136.
- **OATM-REQ-F-134** (error handling): If the customer is not in the customer master, then the system shall treat it as an input error and show 'CustId:<customer number> not found in customer master.Resp: <code> REAS:<code>', unless an earlier message is already set. Rules: OATM-BR-137.
- **OATM-REQ-F-135** (error handling): If reading the customer master fails for any reason other than 'not found', then the system shall treat it as an input error and show 'File Error: READ on CUSTDAT returned RESP <code>,RESP2 <code>', replacing any earlier message. Rules: OATM-BR-138.
- **OATM-REQ-F-136** (business rule): While the program context is re-entry (1), when PF3 was not pressed, the system shall read and validate the entered account number, redisplay the screen with the error on an input error, and otherwise look up the card cross-reference, account master and customer master in turn (stopping at the first not found) and display the screen. Rules: OATM-BR-139.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-126 | Treat asterisk or blank account as unsupplied | business rule | WHEN the account number entered on the Account View screen is '*' or blank, THE account view SHALL treat the account number as not supplied. | high | app/cbl/COACTVWC.cbl:622-643, app/cbl/COACTVWC.cbl:649-685, app/cbl/COACTVWC.cbl:117-124, app/cbl/COACTVWC.cbl:362-367 |
| OATM-BR-127 | Reject missing account number | business rule | WHEN no account number is supplied, THE account view SHALL reject the request as an input error without reading any file, set the session account to zero, show 'No input received', and redisplay the account field as '*' in red. | high | app/cbl/COACTVWC.cbl:622-643, app/cbl/COACTVWC.cbl:649-685, app/cbl/COACTVWC.cbl:117-124, app/cbl/COACTVWC.cbl:362-367 |
| OATM-BR-128 | Validate account number is non-zero numeric | business rule | WHEN the account number supplied is not all digits (including one shorter than 11 digits) or is all zeros, THE account view SHALL reject it as an input error without reading any file, set the session account to zero, show the account field in red and show 'Account Filter must be a non-zero 11 digit number'. | high | app/cbl/COACTVWC.cbl:622-643, app/cbl/COACTVWC.cbl:649-685, app/cbl/COACTVWC.cbl:117-124, app/cbl/COACTVWC.cbl:362-367 |
| OATM-BR-129 | Validate account number is non-zero numeric | business rule | WHEN the account number is 11 digits and not all zeros, THE account view SHALL accept it as the session account and go on to the account lookup. | high | app/cbl/COACTVWC.cbl:622-643, app/cbl/COACTVWC.cbl:649-685, app/cbl/COACTVWC.cbl:117-124, app/cbl/COACTVWC.cbl:362-367 |
| OATM-BR-130 | Orchestrate account and customer retrieval | design note | WHEN an account number passes validation on the Account View screen, THE account view SHALL look the account up in the card cross-reference by account number (CXACAIX) and, when it is found, keep that account's customer number and card number for the rest of the session. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-131 | Look up customer via card cross-reference | business rule | WHEN the account is not in the card cross-reference, THE account view SHALL stop the lookup, treat it as an input error, show the account number in red and show 'Account:<account number> not found in Cross ref file. Resp:<code> Reas:<code>'. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-132 | Look up customer via card cross-reference | error handling | WHEN reading the card cross-reference fails for any reason other than 'not found', THE account view SHALL stop the lookup, treat it as an input error and show 'File Error: READ on CXACAIX returned RESP <code>,RESP2 <code>'. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-133 | Orchestrate account and customer retrieval | design note | WHEN the account is found in the cross-reference, THE account view SHALL read the account master (ACCTDAT) by account number and, on success, mark the account as found so that its details are displayed. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-134 | Read account master record | error handling | WHEN the account is not in the account master, THE account view SHALL treat it as an input error, show the account number in red and show 'Account:<account number> not found in Acct Master file.Resp:<code> Reas:<code>'; any other read failure SHALL show 'File Error: READ on ACCTDAT returned RESP <code>,RESP2 <code>'. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-135 | Orchestrate account and customer retrieval | error handling | WHEN reading the account master does not succeed, THE account view SHALL still go on to read the customer master, because the stop check after the account read never triggers (the 'not found' flag is never set). | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-136 | Orchestrate account and customer retrieval | design note | THE account view SHALL read the customer master (CUSTDAT) using the customer number taken from the card cross-reference and, on success, mark the customer as found so that the customer details are displayed. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-137 | Read customer master record | error handling | WHEN the customer is not in the customer master, THE account view SHALL treat it as an input error and show 'CustId:<customer number> not found in customer master.Resp: <code> REAS:<code>', unless an earlier message is already set. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-138 | Read customer master record | error handling | WHEN reading the customer master fails for any reason other than 'not found', THE account view SHALL treat it as an input error and show 'File Error: READ on CUSTDAT returned RESP <code>,RESP2 <code>', replacing any earlier message. | high | app/cbl/COACTVWC.cbl:687-722, app/cbl/COACTVWC.cbl:723-773, app/cbl/COACTVWC.cbl:774-823, app/cbl/COACTVWC.cbl:825-872 |
| OATM-BR-139 | Process entered account on re-entry | business rule | WHEN PF3 was not pressed and the program context is re-entry (1), THE Account View Screen Flow SHALL read and validate the entered account number; on an input error it SHALL redisplay the screen with the error, otherwise it SHALL look up the card cross-reference, account master and customer master in turn (stopping at the first not found) and display the screen. | high | app/cbl/COACTVWC.cbl:282-292, app/cbl/COACTVWC.cbl:353-383, app/cbl/COACTVWC.cbl:395-406, app/cbl/COACTVWC.cbl:578-581 |

### Key entities

- CSMSG02Y (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CVACT02Y (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-067: When an account number is entered on the account view screen and the account is not found, or the file cannot be read, should the lookup stop at that point? (Currently it stops only on one exact message, 'Did not find this account in account master file', and the real not-found path produces a different message.) (Business analyst) On OATM-BR-127, OATM-BR-129, OATM-BR-132, OATM-BR-135, OATM-BR-136, OATM-BR-138, OATM-BR-139.
- SME-068: On the account view screen, if the account number is left blank, which message should the operator see: 'Account number not provided' or 'No input received'? (Business analyst) On OATM-BR-127, OATM-BR-129, OATM-BR-132, OATM-BR-135, OATM-BR-136, OATM-BR-138, OATM-BR-139.
- SME-069: On the account view screen, the error message says the account number must be 'a non-zero 11 digit number', but only 'numeric and non-zero' is checked. Should exactly 11 digits be required? Should the message keep its current double space? (Business analyst) On OATM-BR-127, OATM-BR-129, OATM-BR-132, OATM-BR-135, OATM-BR-136, OATM-BR-138, OATM-BR-139.
- SME-070: On the account view screen, if the customer record is found but the account record is not, should the account's financial details still be shown? After a successful lookup, should the screen show a success message ('Displaying details of given Account') instead of the input prompt? (Customer service operations lead) On OATM-BR-127, OATM-BR-129, OATM-BR-132, OATM-BR-135, OATM-BR-136, OATM-BR-138, OATM-BR-139.
- SME-071: Please confirm the priority of the account view lookup chain (card cross-reference, then account master, then customer master). Is it critical to the system's core purpose, or a rule that would be costly if it were wrong? (Account servicing subject-matter expert) On OATM-BR-138.
- DEF-044: Is this intended? A blank account number first sets the message 'Account number not provided', which is then replaced at once with 'No input received', so the more specific message can never be shown. The 'only if no message yet' guard in front of it has no effect. (Subject-matter expert) On OATM-BR-127, OATM-BR-129.
- DEF-045: Is this intended? When the account is missing from the account master, or the read fails, the lookup does not stop: the stop check tests a message flag that is never set, so the customer master is still read. If the customer is found, the account fields are filled from an empty account record next to the account 'not found' message. (Subject-matter expert) On OATM-BR-132, OATM-BR-135, OATM-BR-136, OATM-BR-138.

### Decision table gaps

- Account and customer lookup outcome: R26 says lookup stops at the first not found, but R17 says the customer master is still read after an account master failure; which behaviour the business wants is not settled.
