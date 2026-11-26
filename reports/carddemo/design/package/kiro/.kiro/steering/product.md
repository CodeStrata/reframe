---
inclusion: always
---

# Product: aws-carddemo, modernized

The modernized application, designed by Reframe from the legacy source's reconciled requirements and rules. Signed-off functions are final; the rest are draft.

## Functions

- **Customer Account Self-Service: Account Statement Generation and Delivery (ASGD)**, draft: 8 capabilities
- **Customer Account Self-Service: Daily Transaction Processing and Reporting (DTPR)**, final: 17 capabilities
- **Customer Account Self-Service: Online Account and Transaction Management (OATM)**, final: 35 capabilities
- **Customer Data Setup: Credit Card List Detail View and Update (CCLDV)**, draft: 11 capabilities
- **Customer Data Setup: Customer Profile Branch Migration (CPBM)**, draft: 8 capabilities
- **Customer Data Setup: Master Data File Initialization (MDFI)**, draft: 4 capabilities
- **Customer Data Setup: Transaction Type Reference Data Maintenance (TTRDM)**, draft: 24 capabilities
- **Programs not in a business function: Unassigned-Programs (UP)**, draft: 11 capabilities
- **Unclassified: Card Authorization and Fraud Management (CAFM)**, draft: 21 capabilities
- **User Access Control: System Operations and Maintenance (SOM)**, draft: 6 capabilities
- **User Access Control: User Security Profile Management (USPM)**, draft: 9 capabilities

## Journeys

- J01 Find and view an account: Look up an account by its number and review its financial details and the cardholder's profile.
- J02 Update an account: Change an account's details and its customer's details, checked and saved together only after confirmation.
- J03 Find and view a transaction: Browse the transaction list, pick a transaction and see its full details.
- J04 Add a transaction: Enter a new transaction against an account or card and have it validated, confirmed and recorded.
- J05 Pay an account balance: See the balance owed on an account and pay it in full.
- J06 Request a transaction report: Submit a monthly, yearly or custom-period transaction report for printing.
- J07 Find and view a card: Browse or filter the card list, pick a card and check its embossed name, expiry date and active status.
- J08 Look up a card by number: Go straight to a card by entering its account and card number and see its details.
- J09 Update a card from the card list: Pick a card from the list and change its embossed name, active status or expiry date, saving the change safely.
- J10 Update a card by number: Find a card by account and card number and update its embossed name, active status or expiry date.
- J11 Review and maintain transaction types from the list: Find transaction types in the list and correct a description or delete an obsolete type, confirming each change.
- J12 Add a transaction type: Add a new transaction type code with its description so new kinds of transactions can be classified.
- J13 Change or delete a transaction type: Look up a transaction type by code and change its description or delete it, with confirmation and the option to cancel.
- J14 Review an account's pending authorizations: Look up an account to see its customer, limits and pending-authorization totals, page through its pending authorizations and open any one to review its full details.
- J15 Report or clear fraud on an authorization: Find a suspect authorization on an account, mark it as fraud (or remove an earlier fraud mark) and have the action recorded in the fraud register.
- J16 Sign in and sign out: Sign on with a User ID and password, land on the menu that matches the user type, and later sign out.
- J17 Choose a function from the Main Menu: Pick a numbered option on the Main Menu to reach an allowed business function, and come back to the menu when done.
- J18 Add a user: Create a new CardDemo user with name, User ID, password and user type so the person can sign on.
- J19 Find and update a user: Find a user in the user list and change their name, password or user type.
- J20 Delete a user: Find a user and remove them from the user security file so they can no longer sign on.
