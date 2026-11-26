# Feature specification: Enter and leave the card detail screen

**Feature:** CCLDV-C05 · Credit Card List Detail View and Update · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CCLDV-C05)

As a card operations user, I want the card detail screen to open with the right card or an empty search and to return me to where I came from, so that I can move between the menu, the card list and card details without losing my place.

Controls how users arrive at and leave the card detail screen: from the menu it opens an empty search, and from the card list it opens straight on the selected card. Leaving with PF3 returns the user to the screen they came from, or to the main menu. It must never carry stale card selections from an earlier session into a fresh entry.

**Acceptance scenarios:**

1. **Given** Caller: COMEN01C; Entry type: first entry, **when** the card detail program (transaction CCDL) starts with no session context, or is entered from the main menu (COMEN01C) other than as a re-entry, **then** Session context is cleared, including any previously selected account and card (CCLDV-C05-AC-01)
2. **Given** Caller: COMEN01C (menu option 4 'Credit Card View'), **when** the program is entered for the first time from any program other than the card list (COCRDLIC) and PF3 was not pressed, **then** Empty search screen with 'Please enter Account and Card Number' (CCLDV-C05-AC-02)
3. **Given** Started: CCDL typed directly, no session details, **when** the card detail transaction (CCDL) is started with no session details passed in, **then** Prompt 'Please enter Account and Card Number'; fields empty (CCLDV-C05-AC-03)
4. **Given** Caller: COCRDLIC; Account passed: 00000000001; Card passed: 4111111111111111, **when** the program is entered for the first time from the card list (COCRDLIC) and PF3 was not pressed, **then** Card 4111111111111111 is looked up and its details are shown with no input check (CCLDV-C05-AC-04)
5. **Given** Entry type: first entry from COMEN01C, **when** card detail program runs, **then** After the search screen is sent, the next Enter is handled as a re-entry with input checks (CCLDV-C05-AC-05)
6. **Given** Caller: COCRDLIC / CCLI; Key: PF3, **when** the user presses PF3 (or PF15) on the card detail screen, **then** Control goes to COCRDLIC with transaction CCLI (CCLDV-C05-AC-06)
7. **Given** Caller: main menu (shared details reset on entry, no caller recorded); Key: PF3, **when** the user presses PF3 (or PF15) on the card detail screen, **then** Control goes to COMEN01C with transaction CM00 (CCLDV-C05-AC-07)
8. **Given** Key: PF3, **when** control leaves the card detail screen on PF3, **then** The next program receives sender 'COCRDSLC'/'CCDL', user type 'U', first entry (CCLDV-C05-AC-08)

## Requirements

### Functional requirements

- **CCLDV-REQ-F-054** (design note): When the card detail program (transaction CCDL) starts with no session context, or is entered from the main menu (COMEN01C) other than as a re-entry, the system shall clear the whole shared session context before going on. Rules: CCLDV-BR-053.
- **CCLDV-REQ-F-055** (formatting): When the card detail program is entered for the first time from any program other than the card list (COCRDLIC), or started with no session details, and PF3 was not pressed, the system shall show an empty search screen with 'Please enter Account and Card Number' and wait for the user's input. Rules: CCLDV-BR-054, CCLDV-BR-055.
- **CCLDV-REQ-F-056** (business rule): When the card detail program is entered for the first time from the card list (COCRDLIC) and PF3 was not pressed, the system shall use the account and card number passed by the list as already valid, without checking them again, then look up the card and show its details. Rules: CCLDV-BR-056.
- **CCLDV-REQ-N-001** (design note): The system shall mark every card detail screen it sends as awaiting re-entry and return under transaction CCDL, so that the user's next action is treated as a re-entry. Rules: CCLDV-BR-057.
- **CCLDV-REQ-F-057** (business rule): When the user presses PF3 (or PF15) on the card detail screen, the system shall transfer control to the program and transaction that called it (for example the card list COCRDLIC with transaction CCLI), or to the main menu COMEN01C with transaction CM00 when no caller is recorded. Rules: CCLDV-BR-058.
- **CCLDV-REQ-F-058** (design note): When control leaves the card detail screen on PF3, the system shall pass the shared session details showing COCRDSLC / CCDL as the sender, the user type as regular user ('U'), the last screen as COCRDSL / CCRDSLA, and the next program's entry as a first entry. Rules: CCLDV-BR-059.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CCLDV-BR-053 | Card detail screen entry routing and context reset | design note | WHEN the card detail program (transaction CCDL) starts with no session context, or is entered from the main menu (COMEN01C) other than as a re-entry, THE card detail program SHALL clear the whole shared session context before going on. | high | app/cbl/COCRDSLC.cbl:268-279, app/cbl/COCRDSLC.cbl:339-371, app/cbl/COCRDSLC.cbl:254-256, app/cbl/COCRDSLC.cbl:457-496 |
| CCLDV-BR-054 | Show screen to gather selection criteria | formatting | WHEN the program is entered for the first time from any program other than the card list (COCRDLIC) and PF3 was not pressed, THE card detail program SHALL show an empty search screen with 'Please enter Account and Card Number' and wait for the user's input. | high | app/cbl/COCRDSLC.cbl:268-279, app/cbl/COCRDSLC.cbl:339-371, app/cbl/COCRDSLC.cbl:254-256, app/cbl/COCRDSLC.cbl:457-496 |
| CCLDV-BR-055 | Show entered search criteria | formatting | WHEN the card detail transaction (CCDL) is started with no session details passed in, THE card detail screen SHALL show the prompt 'Please enter Account and Card Number' with empty search fields. | medium | app/cbl/COCRDSLC.cbl:457-472, app/cbl/COCRDSLC.cbl:268-272, app/cbl/COCRDSLC.cbl:714-716, app/cbl/COCRDSLC.cbl:676-677 |
| CCLDV-BR-056 | Show card selected from card list | business rule | WHEN the program is entered for the first time from the card list (COCRDLIC) and PF3 was not pressed, THE card detail program SHALL use the account and card number passed by the list as already valid, without checking them again, then look up the card and show its details. | high | app/cbl/COCRDSLC.cbl:268-279, app/cbl/COCRDSLC.cbl:339-371, app/cbl/COCRDSLC.cbl:254-256, app/cbl/COCRDSLC.cbl:457-496 |
| CCLDV-BR-057 | Card detail screen entry routing and context reset | design note | THE card detail program SHALL mark every screen it sends as awaiting re-entry and return under transaction CCDL, so that the user's next action is treated as a re-entry. | high | app/cbl/COCRDSLC.cbl:268-279, app/cbl/COCRDSLC.cbl:339-371, app/cbl/COCRDSLC.cbl:254-256, app/cbl/COCRDSLC.cbl:457-496 |
| CCLDV-BR-058 | Exit to the destination program | business rule | WHEN the user presses PF3 (or PF15) on the card detail screen, THE card detail screen SHALL transfer control to the program and transaction that called it (for example the card list COCRDLIC with transaction CCLI), or to the main menu COMEN01C with transaction CM00 when no caller is recorded. | high | app/cbl/COCRDSLC.cbl:304-335, app/cbl/COCRDSLC.cbl:163-182, app/cbl/COCRDSLC.cbl:268-272, app/cpy/CSSTRPFY.cpy:35 |
| CCLDV-BR-059 | Exit to the destination program | design note | WHEN control leaves the card detail screen on PF3, THE card detail screen SHALL pass the shared session details showing COCRDSLC / CCDL as the sender, the user type as regular user ('U'), the last screen as COCRDSL / CCRDSLA, and the next program's entry as a first entry. | high | app/cbl/COCRDSLC.cbl:304-335, app/cbl/COCRDSLC.cbl:163-182, app/cbl/COCRDSLC.cbl:268-272, app/cpy/CSSTRPFY.cpy:35 |

### Key entities

- CSMSG02Y (file record)
- CVACT02Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CVCRD01Y (working storage)
- CVCUS01Y (working storage)

### Needs clarification

- SME-103: On the card search screen, the error messages say the account number must be 11 digits and the card number 16 digits, but the rules only check that each is numeric. Should the new system require exactly 11 digits for the account number and 16 for the card number? (Business analyst) On CCLDV-BR-055, CCLDV-BR-054, CCLDV-BR-056, CCLDV-BR-059.
- SME-104: The card search finds the card by card number only and does not use the account number entered. Should the new system check that the card found belongs to the account entered? (Business analyst) On CCLDV-BR-055, CCLDV-BR-054, CCLDV-BR-056, CCLDV-BR-059.
- SME-105: On the card search screen, when both the account and card number are blank, should the message 'No input received' replace an earlier message such as 'Account number not provided', or should the first message stay? (Business analyst) On CCLDV-BR-055, CCLDV-BR-054, CCLDV-BR-056, CCLDV-BR-059.
- SME-106: When a card is found, should the operator see the message 'Displaying requested details'? (Business analyst) On CCLDV-BR-055, CCLDV-BR-054, CCLDV-BR-056, CCLDV-BR-059.
- SME-107: When a user leaves the card detail screen, the system always resets their user type to regular user, even for an administrator. Is this intended, or should the user keep their type (admin or regular)? (Security and access-control owner) On CCLDV-BR-059.
- DEF-076: Is this intended? Clearing the whole shared context on entry from the main menu also erases the signed-on user's ID and user type, so PF3 then returns to the menu with a blank user ID and the user type forced to regular user. (Subject-matter expert) On CCLDV-BR-054, CCLDV-BR-056, CCLDV-BR-057.
- DEF-077: Confirm this is deliberate: On PF3 the user type is always set to regular user ('U'), even if the session belonged to an administrator. (Subject-matter expert) On CCLDV-BR-059.
- DEF-122: Is this intended? An invalid (non-numeric) account or card entry is cleared from the screen because the saved value is reset to zero, so the user cannot see what they typed. On resubmission a blank field shows '*' instead. (Subject-matter expert) On CCLDV-BR-055.

### Decision table gaps

None.
