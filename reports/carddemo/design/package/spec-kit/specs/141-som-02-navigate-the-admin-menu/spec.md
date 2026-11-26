# Feature specification: Navigate the Admin Menu

**Feature:** SOM-C02 · System Operations and Maintenance · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (SOM-C02)

As an administrator, I want to pick a numbered option from the Admin Menu, so that I am taken to the administration function I need.

The Admin Menu lets administrators pick a numbered option, 1 to 6, to reach the user-security screens (list, add, update and delete users) and the transaction-type maintenance screens. It must check every entry, reject keys and option numbers it does not support with the exact messages, and pass the session on to the chosen screen. Today the menu does not check that the user is an administrator, so the new application must decide on purpose where that admin-only check sits.

**Acceptance scenarios:**

1. **Given** Arriving from: COSGN00C after admin sign-on; Re-entry flag (CDEMO-PGM-CONTEXT): 0, **when** the Admin Menu is entered with session data and it is not a re-entry from its own screen, **then** Blank admin menu shown with options 1-6 and no message (SOM-C02-AC-01)
2. **Given** Option entered: '3 ', **when** the operator presses Enter on the Admin Menu, **then** Option treated as 03 and shown as '03' (SOM-C02-AC-02)
3. **Given** Option entered: blank, **when** the operator presses Enter on the Admin Menu, **then** Option treated as 00 (then rejected as invalid) (SOM-C02-AC-03)
4. **Given** Key pressed: Enter; Option entered: 4, **when** the operator presses Enter on the Admin Menu, **then** Option 4 (User Delete (Security)) is processed (SOM-C02-AC-04)
5. **Given** Key pressed: PF5, **when** the operator presses a key other than Enter or PF3 on the Admin Menu, **then** Menu redisplayed with 'Invalid key pressed. Please see below...' (SOM-C02-AC-05)
6. **Given** Option entered: 7, **when** the option entered on the Admin Menu is not numeric, is zero, or is greater than the number of admin options (6), **then** Menu redisplayed with 'Please enter a valid option number...' (SOM-C02-AC-06)
7. **Given** Option entered: AB, **when** the option entered on the Admin Menu is not numeric, is zero, or is greater than the number of admin options (6), **then** Menu redisplayed with 'Please enter a valid option number...' (SOM-C02-AC-07)
8. **Given** Option entered: 0, **when** the option entered on the Admin Menu is not numeric, is zero, or is greater than the number of admin options (6), **then** Menu redisplayed with 'Please enter a valid option number...' (SOM-C02-AC-08)
9. **Given** Option entered: 1, **when** an operator selects a valid Admin Menu option (1 to 6) whose program name does not start with 'DUMMY', **then** Control passes to 'COUSR00C' (User List (Security)) (SOM-C02-AC-09)
10. **Given** Option entered: 5, **when** an operator selects a valid Admin Menu option (1 to 6) whose program name does not start with 'DUMMY', **then** Control passes to 'COTRTLIC' (Transaction Type List/Update (Db2)) (SOM-C02-AC-10)
11. **Given** Option entered: 2; Option program: COUSR01C, **when** a selected Admin Menu option's program name starts with 'DUMMY', **then** The 'DUMMY' check does not match; control passes to 'COUSR01C' (SOM-C02-AC-11)
12. **Given** Session user type (CDEMO-USER-TYPE): U; Option entered: 1, **when** Admin Menu runs, **then** Control passes to 'COUSR00C' without any user-type check in the Admin Menu (SOM-C02-AC-12)
13. **Given** User signs on with type: A, **when** Admin Menu runs, **then** Sign-on transfers the user to the Admin Menu ('COADM01C'); type 'U' goes to 'COMEN01C' instead (SOM-C02-AC-13)
14. **Given** the admin option table holds 6 options, **when** the Admin Menu is displayed, **then** 6 option lines are shown, one per line, in order 1 to 6, each written as the option number followed by '. ' and the option name (for example '1. User List (Security)'), and no further option lines are shown (SOM-C02-AC-14)
15. **Given** an administrator is on the Admin Menu and the program for option 1 is not deployed or registered, **when** they enter option 1 and press Enter, **then** the Admin Menu is shown again with the green message 'This option is not installed ...', which does not include the option name; no screen change happens, and the menu waits for the next entry (SOM-C02-AC-15)

## Requirements

### Functional requirements

- **SOM-REQ-F-004** (formatting): When the Admin Menu is entered with session data and it is not a re-entry from its own screen, the system shall clear any error and message, mark the session as re-entry, and display a fresh, empty administration menu. Rules: SOM-BR-004.
- **SOM-REQ-F-005** (formatting): The system shall list each admin option (currently 6) on its own line in order, as the option number, '. ' and the option name, whenever the Admin Menu is displayed. Rules: SOM-BR-005.
- **SOM-REQ-F-006** (business rule): When the operator presses Enter on the Admin Menu, the system shall read the option entry ignoring trailing blanks, right-align it, turn remaining blanks into zeros, treat it as a two-digit option number, show that number back in the option field and process that option number. Rules: SOM-BR-006, SOM-BR-007.
- **SOM-REQ-F-007** (business rule): If the operator presses a key other than Enter or PF3 on the Admin Menu, then the system shall flag an error and redisplay the menu with the message 'Invalid key pressed. Please see below...'. Rules: SOM-BR-008.
- **SOM-REQ-F-008** (business rule): If the option entered on the Admin Menu is not numeric, is zero, or is greater than the number of admin options (6), then the system shall flag an error and redisplay the menu with the message 'Please enter a valid option number...'. Rules: SOM-BR-009.
- **SOM-REQ-F-009** (business rule): When an operator selects a valid Admin Menu option (1 to 6) whose program name does not start with 'DUMMY', the system shall record the Admin Menu as the origin (transaction 'CA00', program 'COADM01C'), reset the target screen's context to first entry, and transfer control to that option's program with the session data. Rules: SOM-BR-010.
- **SOM-REQ-F-010** (error handling): If the program of a selected Admin Menu option is not defined in CICS, then the system shall redisplay the menu with the green message 'This option is not installed ...' (without the option name) and wait for the next entry. Rules: SOM-BR-011.
- **SOM-REQ-F-011** (historical artifact): When a selected Admin Menu option's program name starts with 'DUMMY', the system shall redisplay the menu with the green message 'This option is not installed ...'. Rules: SOM-BR-012.
- **SOM-REQ-N-001** (business rule): The system shall not check the signed-on user's type within the Admin Menu, relying on sign-on to send only admin users ('A') to it, so that a session reaching it with user type 'U' can still open the user-security functions. Rules: SOM-BR-013.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| SOM-BR-004 | Show blank menu on first entry | formatting | WHEN the Admin Menu is entered with session data and it is not a re-entry from its own screen, THE Admin Menu SHALL clear any error and message, mark the session as re-entry, and display a fresh, empty administration menu. | medium | app/cbl/COADM01C.cbl:81-94 |
| SOM-BR-005 | Compose numbered administrative option labels | formatting | WHENEVER the Admin Menu is displayed, THE Admin Menu SHALL list each admin option (currently 6) on its own line in order, as the option number, '. ' and the option name. | medium | app/cbl/COADM01C.cbl:175-178, app/cbl/COADM01C.cbl:229-266, app/cpy/COADM02Y.cpy:22-59 |
| SOM-BR-006 | Normalize entered option number | design note | WHEN the operator presses Enter on the Admin Menu, THE Admin Menu SHALL read the option entry ignoring trailing blanks, right-align it, turn remaining blanks into zeros, treat it as a two-digit option number and show that number back in the option field. | medium | app/cbl/COADM01C.cbl:119-129, app/cbl/COADM01C.cbl:43-44 |
| SOM-BR-007 | Route Enter key to option processing | business rule | WHEN the operator presses Enter on the Admin Menu, THE Admin Menu SHALL process the option number entered. | medium | app/cbl/COADM01C.cbl:95-99 |
| SOM-BR-008 | Reject unsupported key press | business rule | WHEN the operator presses a key other than Enter or PF3 on the Admin Menu, THE Admin Menu SHALL flag an error and redisplay the menu with the message 'Invalid key pressed. Please see below...'. | medium | app/cbl/COADM01C.cbl:103-106, app/cpy/CSMSG01Y.cpy:20-21 |
| SOM-BR-009 | Reject invalid option number | business rule | WHEN the option entered on the Admin Menu is not numeric, is zero, or is greater than the number of admin options (6), THE Admin Menu SHALL flag an error and redisplay the menu with the message 'Please enter a valid option number...'. | medium | app/cbl/COADM01C.cbl:131-138, app/cpy/COADM02Y.cpy:22 |
| SOM-BR-010 | Transfer to selected option program | business rule | WHEN an operator selects a valid Admin Menu option (1 to 6) whose program name does not start with 'DUMMY', THE Admin Menu SHALL record itself as the origin (transaction 'CA00', program 'COADM01C'), reset the target screen's context to first entry, and transfer control to that option's program with the session data. | high | app/cbl/COADM01C.cbl:86-109, app/cbl/COADM01C.cbl:140-149, app/cpy/COADM02Y.cpy:22-59, app/cbl/COSGN00C.cbl:224-239 |
| SOM-BR-011 | Admin menu handles unavailable functions with a 'not installed' message | error handling | WHEN the program of a selected Admin Menu option is not defined in CICS (PGMIDERR on the transfer), THE Admin Menu SHALL redisplay the menu with the green message 'This option is not installed ...' (without the option name) and wait for the next entry. | high | app/cbl/COADM01C.cbl:77-79, app/cbl/COADM01C.cbl:140-158, app/cbl/COADM01C.cbl:270-283, app/cpy/COADM02Y.cpy:26-53 |
| SOM-BR-012 | Inform option not installed | historical artifact | WHEN a selected Admin Menu option's program name starts with 'DUMMY', THE Admin Menu SHALL redisplay the menu with the green message 'This option is not installed ...'; no option in the current option table starts with 'DUMMY', so this check never matches today. | high | app/cbl/COADM01C.cbl:77-79, app/cbl/COADM01C.cbl:140-158, app/cbl/COADM01C.cbl:270-283, app/cpy/COADM02Y.cpy:26-53 |
| SOM-BR-013 | Admin menu does not itself verify that the user is an admin | business rule | THE Admin Menu SHALL NOT check the signed-on user's type itself; it relies on sign-on sending only admin users ('A') to it, so a session that reaches it with user type 'U' can still open the user-security functions. | high | app/cbl/COADM01C.cbl:86-109, app/cbl/COADM01C.cbl:140-149, app/cpy/COADM02Y.cpy:22-59, app/cbl/COSGN00C.cbl:224-239 |

### Key entities

- COADM02Y (working storage)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSUSR01Y (working storage)

### Needs clarification

- SME-073: What should happen when the administration menu is opened without any information from the screen that called it (for example, return to sign-on)? (Application product owner) On SOM-BR-004, SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-005, SOM-BR-010, SOM-BR-012.
- SME-074: On the administration menu, where should pressing PF3 take the user? (Application product owner) On SOM-BR-004, SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-005, SOM-BR-010, SOM-BR-012.
- SME-075: Should the new administration menu keep a way to configure an option as 'not installed'? With today's setup no option uses it. (Application product owner) On SOM-BR-004, SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-005, SOM-BR-010, SOM-BR-012.
- SME-076: The administration menu has 6 options, but the option field takes 2 digits. Should the new system allow more than 6 (or more than 9) administrative options? (Application product owner) On SOM-BR-004, SOM-BR-006, SOM-BR-007, SOM-BR-008, SOM-BR-009, SOM-BR-005, SOM-BR-010, SOM-BR-012.
- SME-077: Today only sign-on checks that a user is an administrator before they reach the Admin Menu. Should the new system check for an administrator user on every admin function? (Security officer) On SOM-BR-013.
- DEF-019: Confirm this is deliberate: The Admin Menu performs no user-type check of its own; access control depends entirely on sign-on routing admins to it. (Subject-matter expert) On SOM-BR-010, SOM-BR-013.
- DEF-098: Confirm this is deliberate: The 'DUMMY' placeholder check is kept in code although no option in the table is a DUMMY entry, so the not-installed message after it can only appear via PGMIDERR. (Subject-matter expert) On SOM-BR-012.

### Decision table gaps

- Admin Menu entry and key handling: No rule says what the Admin Menu does when entered without session data.
- Admin Menu entry and key handling: PF3 is excluded from the invalid-key rule, but no rule says what PF3 does on the Admin Menu.
