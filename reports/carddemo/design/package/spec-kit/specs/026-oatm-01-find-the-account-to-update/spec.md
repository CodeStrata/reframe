# Feature specification: Find the account to update

**Feature:** OATM-C01 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C01)

As an operator, I want to enter an account id and have the system fetch the linked card, account and customer records, so that I can review and update the right account and customer details.

Lets an operator enter an account number and brings up that account with its linked card and customer, so they can review and update the right records. The account is found through the card cross-reference, which gives the customer and card for the session. After that the account and customer records are read. It must never show or update a customer who is not linked to the account entered. When a lookup fails, it must stop and say which record was missing or could not be read.

**Acceptance scenarios:**

1. **Given** entry: first entry from the main menu, **when** the account update screen is shown on first entry to the function, **then** Message 'Enter or update id of account to update' (OATM-C01-AC-01)
2. **Given** account id entered: 00000000099 (not found); update stage: not fetched, **when** the account update screen is shown, it is not a first entry, and no account details have been fetched yet, **then** Message 'Enter or update id of account to update' (OATM-C01-AC-02)
3. **Given** update stage: unrecognised value; information message: blank, **when** no update stage matches and the information message is blank, **then** Message 'Enter or update id of account to update' (OATM-C01-AC-03)
4. **Given** Account ID: 00000000011; Cross-reference: found, customer 000000011, **when** the account is found in the card cross-reference (by account ID), **then** Customer 000000011 and its card number become the session customer and card. (OATM-C01-AC-04)
5. **Given** account id: 00000000001; account master: record exists, **when** the account master read (ACCTDAT) succeeds, **then** Account marked found (OATM-C01-AC-05)
6. **Given** customer id from cross-reference: 000000001; customer master: record exists, **when** the customer master read (CUSTDAT) for the account's customer succeeds, **then** Customer marked found (OATM-C01-AC-06)
7. **Given** account id: 00000000001; cross-reference: found, **when** the account is found in the card cross-reference, **then** The session context holds the account, customer and card number for later screens (OATM-C01-AC-07)
8. **Given** stored expiry date: 2027-08-31, **when** the account is found in the card cross-reference, **then** Snapshot expiry year 2027, month 08, day 31 (OATM-C01-AC-08)
9. **Given** no card cross-reference entry exists for account 00000000099, **when** the operator enters account 00000000099 on the Update account screen and submits, **then** the account is flagged invalid, the account and customer are not read, and the screen shows 'Account:00000000099 not found in Cross ref file. Resp:<resp> Reas:<reason>' with the lookup's response and reason codes filled in (OATM-C01-AC-09)
10. **Given** the card cross-reference lookup for a valid account number fails for a reason other than not found (for example, the store is unavailable), **when** the operator submits the account number, **then** the account is flagged invalid, the lookup stops, and the screen shows 'File Error: READ on CXACAIX returned RESP <resp>,RESP2 <reason>' with the returned codes (OATM-C01-AC-10)
11. **Given** account 00000000099 is in the card cross-reference but has no account master record, and no message is set yet, **when** the operator submits the account number, **then** an input error is flagged, the account search is marked invalid, and the screen shows 'Account:00000000099 not found in Acct Master file.Resp:<resp> Reas:<reason>'; if a message was already set, that earlier message stays (OATM-C01-AC-11)
12. **Given** the account master read for a cross-referenced account fails for a reason other than not found, **when** the operator submits the account number, **then** an input error is flagged, the account search is marked invalid, and the message starts 'File Error: READ on ACCTDAT returned RESP <resp>' with the returned code (OATM-C01-AC-12)
13. **Given** the cross-reference for the account names customer 000000123 and no customer master record exists for it, and no message is set yet, **when** the operator submits the account number, **then** an input error is flagged, the customer search is marked invalid, and the screen shows 'CustId:000000123 not found in customer master.Resp: <resp> REAS:<reason>'; if a message was already set, that earlier message stays (OATM-C01-AC-13)
14. **Given** the customer master read for the account's customer fails for a reason other than not found, **when** the operator submits the account number, **then** an input error is flagged, the customer search is marked invalid, and the message starts 'File Error: READ on CUSTDAT returned RESP <resp>' with the returned code (OATM-C01-AC-14)

## Requirements

### Functional requirements

- **OATM-REQ-F-001** (formatting): When the account update screen is shown on first entry to the function, the system shall set the information message to 'Enter or update id of account to update'. Rules: OATM-BR-001.
- **OATM-REQ-F-002** (formatting): When the account update screen is shown, it is not a first entry, and no account details have been fetched yet, the system shall set the information message to 'Enter or update id of account to update'. Rules: OATM-BR-002.
- **OATM-REQ-F-003** (historical artifact): If no update stage matches and the information message is blank, then the system shall default the information message to 'Enter or update id of account to update'. Rules: OATM-BR-003.
- **OATM-REQ-F-004** (design note): When the account is found in the card cross-reference by account ID, the system shall take the customer ID and card number from it for the session and go on to read the account and customer. Rules: OATM-BR-004.
- **OATM-REQ-F-005** (business rule): If the account is not in the card cross-reference, then the system shall flag the account as invalid, stop the lookup and show 'Account:<account> not found in Cross ref file. Resp:<resp> Reas:<reason>'. Rules: OATM-BR-005.
- **OATM-REQ-F-006** (error handling): If the card cross-reference read fails for any other reason, then the system shall flag the account as invalid, stop the lookup and show 'File Error: READ on CXACAIX returned RESP <resp>,RESP2 <reason>'. Rules: OATM-BR-006.
- **OATM-REQ-F-007** (design note): When the account master read succeeds, the system shall mark the account as found. Rules: OATM-BR-007.
- **OATM-REQ-F-008** (error handling): If the account is not on the account master, then the system shall flag an input error, mark the account search invalid and, if no message is already set, report 'Account:<id> not found in Acct Master file.Resp:<resp> Reas:<reason>'. Rules: OATM-BR-008.
- **OATM-REQ-F-009** (error handling): If the account master read fails for any other reason, then the system shall flag an input error, mark the account search invalid and report 'File Error: READ on ACCTDAT returned RESP <resp>...'. Rules: OATM-BR-009.
- **OATM-REQ-F-010** (design note): When the customer master read for the account's customer succeeds, the system shall mark the customer as found. Rules: OATM-BR-010.
- **OATM-REQ-F-011** (error handling): If the customer is not on the customer master, then the system shall flag an input error, mark the customer search invalid and, if no message is already set, report 'CustId:<id> not found in customer master.Resp: <resp> REAS:<reason>'. Rules: OATM-BR-011.
- **OATM-REQ-F-012** (error handling): If the customer master read fails for any other reason, then the system shall flag an input error, mark the customer search invalid and report 'File Error: READ on CUSTDAT returned RESP <resp>...'. Rules: OATM-BR-012.
- **OATM-REQ-F-013** (design note): When the account is found in the card cross-reference, the system shall save the account id, customer id, customer names, account status and card number as the session context. Rules: OATM-BR-013.
- **OATM-REQ-F-014** (design note): When the account is found in the card cross-reference, the system shall copy the fetched account and customer values into the original snapshot, splitting the open, expiry, reissue and birth dates (YYYY-MM-DD) into year, month and day. Rules: OATM-BR-014.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-001 | Prompt for account id on first entry | formatting | WHEN the account update screen is shown on first entry to the function, THE Account Update messaging SHALL set the information message to 'Enter or update id of account to update'. | medium | app/cbl/COACTUPC.cbl:2955-2959, app/cbl/COACTUPC.cbl:468-469 |
| OATM-BR-002 | Prompt for account id when details missing | formatting | WHEN the account update screen is shown, it is not a first entry, and no account details have been fetched yet, THE Account Update messaging SHALL set the information message to 'Enter or update id of account to update'. | medium | app/cbl/COACTUPC.cbl:2955-2961, app/cbl/COACTUPC.cbl:656-658 |
| OATM-BR-003 | Default to search prompt and show messages | historical artifact | WHEN no update stage matches and the information message is blank, THE Account Update messaging SHALL default it to 'Enter or update id of account to update'; every valid stage is matched earlier, so this fallback does not normally apply. | medium | app/cbl/COACTUPC.cbl:2955-2982, app/cbl/COACTUPC.cbl:656-668 |
| OATM-BR-004 | Resolve customer from card cross-reference | design note | WHEN the account is found in the card cross-reference (by account ID), THE account update SHALL take the customer ID and card number from it for the session and go on to read the account and customer. | medium | app/cbl/COACTUPC.cbl:3608-3626, app/cbl/COACTUPC.cbl:3650-3696, app/cbl/COACTUPC.cbl:389-404, app/cbl/COACTUPC.cbl:581 |
| OATM-BR-005 | Resolve customer from card cross-reference | business rule | WHEN the account is not in the card cross-reference, THE account update SHALL flag the account as invalid, stop the lookup and show 'Account:<account> not found in Cross ref file. Resp:<resp> Reas:<reason>'. | medium | app/cbl/COACTUPC.cbl:3608-3626, app/cbl/COACTUPC.cbl:3650-3696, app/cbl/COACTUPC.cbl:389-404, app/cbl/COACTUPC.cbl:581 |
| OATM-BR-006 | Resolve customer from card cross-reference | error handling | WHEN the cross-reference read fails for any other reason, THE account update SHALL flag the account as invalid, stop the lookup and show 'File Error: READ on CXACAIX returned RESP <resp>,RESP2 <reason>'. | medium | app/cbl/COACTUPC.cbl:3608-3626, app/cbl/COACTUPC.cbl:3650-3696, app/cbl/COACTUPC.cbl:389-404, app/cbl/COACTUPC.cbl:581 |
| OATM-BR-007 | Read account master record | design note | WHEN the account master read (ACCTDAT) succeeds, THE Account Update retrieval SHALL mark the account as found. | medium | app/cbl/COACTUPC.cbl:3701-3748, app/cbl/COACTUPC.cbl:389-400 |
| OATM-BR-008 | Read account master record | error handling | WHEN the account is not on the account master, THE Account Update retrieval SHALL flag an input error, mark the account search invalid and, if no message is already set, report 'Account:<id> not found in Acct Master file.Resp:<resp> Reas:<reason>'. | medium | app/cbl/COACTUPC.cbl:3701-3748, app/cbl/COACTUPC.cbl:389-400 |
| OATM-BR-009 | Read account master record | error handling | WHEN the account master read fails for any other reason, THE Account Update retrieval SHALL flag an input error, mark the account search invalid and report 'File Error: READ on ACCTDAT returned RESP <resp>...'. | medium | app/cbl/COACTUPC.cbl:3701-3748, app/cbl/COACTUPC.cbl:389-400 |
| OATM-BR-010 | Read customer master record | design note | WHEN the customer master read (CUSTDAT) for the account's customer succeeds, THE Account Update retrieval SHALL mark the customer as found. | medium | app/cbl/COACTUPC.cbl:3752-3797, app/cbl/COACTUPC.cbl:3631-3634 |
| OATM-BR-011 | Read customer master record | error handling | WHEN the customer is not on the customer master, THE Account Update retrieval SHALL flag an input error, mark the customer search invalid and, if no message is already set, report 'CustId:<id> not found in customer master.Resp: <resp> REAS:<reason>'. | medium | app/cbl/COACTUPC.cbl:3752-3797, app/cbl/COACTUPC.cbl:3631-3634 |
| OATM-BR-012 | Read customer master record | error handling | WHEN the customer master read fails for any other reason, THE Account Update retrieval SHALL flag an input error, mark the customer search invalid and report 'File Error: READ on CUSTDAT returned RESP <resp>...'. | medium | app/cbl/COACTUPC.cbl:3752-3797, app/cbl/COACTUPC.cbl:3631-3634 |
| OATM-BR-013 | Store fetched details as original snapshot | design note | WHEN the account is found in the card cross-reference, THE Account Update retrieval SHALL save the account id, customer id, customer names, account status and card number as the session context. | medium | app/cbl/COACTUPC.cbl:3801-3885, app/cbl/COACTUPC.cbl:3608-3647 |
| OATM-BR-014 | Store fetched details as original snapshot | design note | WHEN the account is found in the card cross-reference, THE Account Update retrieval SHALL copy the fetched account and customer values into the original snapshot, splitting the open, expiry, reissue and birth dates (YYYY-MM-DD) into year, month and day. | medium | app/cbl/COACTUPC.cbl:3801-3885, app/cbl/COACTUPC.cbl:3608-3647 |

### Key entities

- CSMSG02Y (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSLKPCDY (working storage)
- CSMSG01Y (working storage)
- CSSETATY (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CSUTLDPY (working storage)
- CSUTLDWY (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-055: When the customer for an account cannot be found during account update, a 'not found' message is shown but the customer is not marked as not found. Should the new system explicitly mark the customer as not found? (Account servicing business owner) On OATM-BR-006, OATM-BR-009, OATM-BR-012, OATM-BR-014.
- DEF-116: Is this intended? When the account is not on the account master, the 'not found' state is never set (that line is commented out), so the check at 3627 never stops processing. The program goes on to read the customer, stores account data it never read, and can show the screen as if details were found. (Subject-matter expert) On OATM-BR-009.
- DEF-117: Is this intended? The 'customer not found' state is never set (that line is commented out), so the program still stores the unread customer record as the original snapshot and in the shared context. The screen stays in 'not fetched' because the customer was not found. (Subject-matter expert) On OATM-BR-012.

### Decision table gaps

- Outcome of each record read during account lookup: No rule says whether the customer master is still read after the account master read fails, or whether the screen then shows details.
