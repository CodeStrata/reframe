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

- J01 View an account: Look up an account by number and see its balances, limits, dates and the customer's profile while the caller waits.
- J02 Update an account: Change an account's and its customer's details after confirming the caller, saving only valid, confirmed changes.
- J03 Pay an account balance: Pay off the full balance owed on an account and have the payment recorded as a transaction.
- J04 Find and view a transaction: Browse transactions page by page, or look one up by ID, and see its full details.
- J05 Add a transaction: Record a new transaction against an account or card, with every field checked before it is added.
- J06 Request a transaction report: Submit a monthly, yearly or custom-period transaction report for printing.
- J07 Find and view a card: Find a caller's card in the card list by account or card number and check its embossed name, status and expiry date.
- J08 Update a card: Change a card's embossed name, active status or expiry date after confirming the caller, and save it safely.
- J09 Review and correct transaction types in the list: Browse and filter the transaction types, then correct a description or delete an obsolete type straight from the list.
- J10 Add a transaction type: Add a new transaction type code with its description so new kinds of transactions can be classified.
- J11 Change or delete a transaction type: Look up a transaction type by code and either correct its description or delete it, confirming before anything is changed.
- J12 Review an account's pending authorizations: Look up an account's recent card authorizations, page through them and open one to see its full details while the caller waits.
- J13 Report or clear fraud on an authorization: Find a suspect authorization on an account and mark it as fraud, or remove a fraud mark set in error, so the authorization and the fraud register agree.
- J14 Sign in and choose a function: Sign in to CardDemo with a user ID and password, get to the main menu, pick the function needed and sign off at the end.
- J15 Find a user and update their profile: Find a user in the user list and correct their name, password or user type.
- J16 Add a new user: Create a user profile with a name, user ID, password and user type so the new person can sign in to CardDemo.
- J17 Remove a user: Find a user who should no longer have access and delete their profile so they can no longer sign in.

## Personas

# Card services agent

Works in the card issuer's contact centre and serves cardholders on the phone. Looks up an account or card while the caller waits, so every lookup must be quick from the keyboard and every error must say what to fix. Updates account and card details only after confirming who the caller is. Uses the system all day on a desktop browser.
