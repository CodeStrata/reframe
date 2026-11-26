# Requirements: Enter and leave the card detail screen (CCLDV-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Credit Card List Detail View and Update · runs as online · risk medium

## Introduction

Controls how users arrive at and leave the card detail screen: from the menu it opens an empty search, and from the card list it opens straight on the selected card. Leaving with PF3 returns the user to the screen they came from, or to the main menu. It must never carry stale card selections from an earlier session into a fresh entry.

**User story:** As a card operations user, I want the card detail screen to open with the right card or an empty search and to return me to where I came from, so that I can move between the menu, the card list and card details without losing my place.

## Requirements

### Requirement 1: CCLDV-REQ-F-054 (design note)

#### Acceptance criteria

1. When the card detail program (transaction CCDL) starts with no session context, or is entered from the main menu (COMEN01C) other than as a re-entry, the system shall clear the whole shared session context before going on. (rules CCLDV-BR-053)
2. GIVEN Caller: COMEN01C; Entry type: first entry WHEN the card detail program (transaction CCDL) starts with no session context, or is entered from the main menu (COMEN01C) other than as a re-entry THEN Session context is cleared, including any previously selected account and card (CCLDV-C05-AC-01; CCLDV-BR-053)

### Requirement 2: CCLDV-REQ-F-055 (formatting)

#### Acceptance criteria

1. When the card detail program is entered for the first time from any program other than the card list (COCRDLIC), or started with no session details, and PF3 was not pressed, the system shall show an empty search screen with 'Please enter Account and Card Number' and wait for the user's input. (rules CCLDV-BR-054, CCLDV-BR-055)
2. GIVEN Caller: COMEN01C (menu option 4 'Credit Card View') WHEN the program is entered for the first time from any program other than the card list (COCRDLIC) and PF3 was not pressed THEN Empty search screen with 'Please enter Account and Card Number' (CCLDV-C05-AC-02; CCLDV-BR-054)
3. GIVEN Started: CCDL typed directly, no session details WHEN the card detail transaction (CCDL) is started with no session details passed in THEN Prompt 'Please enter Account and Card Number'; fields empty (CCLDV-C05-AC-03; CCLDV-BR-055)

### Requirement 3: CCLDV-REQ-F-056 (business rule)

#### Acceptance criteria

1. When the card detail program is entered for the first time from the card list (COCRDLIC) and PF3 was not pressed, the system shall use the account and card number passed by the list as already valid, without checking them again, then look up the card and show its details. (rules CCLDV-BR-056)
2. GIVEN Caller: COCRDLIC; Account passed: 00000000001; Card passed: 4111111111111111 WHEN the program is entered for the first time from the card list (COCRDLIC) and PF3 was not pressed THEN Card 4111111111111111 is looked up and its details are shown with no input check (CCLDV-C05-AC-04; CCLDV-BR-056)

### Requirement 4: CCLDV-REQ-N-001 (design note)

#### Acceptance criteria

1. The system shall mark every card detail screen it sends as awaiting re-entry and return under transaction CCDL, so that the user's next action is treated as a re-entry. (rules CCLDV-BR-057)
2. GIVEN Entry type: first entry from COMEN01C WHEN card detail program runs THEN After the search screen is sent, the next Enter is handled as a re-entry with input checks (CCLDV-C05-AC-05; CCLDV-BR-057)

### Requirement 5: CCLDV-REQ-F-057 (business rule)

#### Acceptance criteria

1. When the user presses PF3 (or PF15) on the card detail screen, the system shall transfer control to the program and transaction that called it (for example the card list COCRDLIC with transaction CCLI), or to the main menu COMEN01C with transaction CM00 when no caller is recorded. (rules CCLDV-BR-058)
2. GIVEN Caller: COCRDLIC / CCLI; Key: PF3 WHEN the user presses PF3 (or PF15) on the card detail screen THEN Control goes to COCRDLIC with transaction CCLI (CCLDV-C05-AC-06; CCLDV-BR-058)
3. GIVEN Caller: main menu (shared details reset on entry, no caller recorded); Key: PF3 WHEN the user presses PF3 (or PF15) on the card detail screen THEN Control goes to COMEN01C with transaction CM00 (CCLDV-C05-AC-07; CCLDV-BR-058)

### Requirement 6: CCLDV-REQ-F-058 (design note)

#### Acceptance criteria

1. When control leaves the card detail screen on PF3, the system shall pass the shared session details showing COCRDSLC / CCDL as the sender, the user type as regular user ('U'), the last screen as COCRDSL / CCRDSLA, and the next program's entry as a first entry. (rules CCLDV-BR-059)
2. GIVEN Key: PF3 WHEN control leaves the card detail screen on PF3 THEN The next program receives sender 'COCRDSLC'/'CCDL', user type 'U', first entry (CCLDV-C05-AC-08; CCLDV-BR-059)
