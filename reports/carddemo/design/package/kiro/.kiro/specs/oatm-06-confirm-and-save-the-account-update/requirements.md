# Requirements: Confirm and save the account update (OATM-C06)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Lets the operator confirm validated changes and saves them to the account and customer records. The save goes through only if nobody else has changed those records since they were shown. It must never overwrite another user's update. Every confirmed value, including the account group, must be saved to its own field and never into another field.

**User story:** As an operator, I want to confirm validated changes and have them saved only if nobody else has changed the record meanwhile, so that I do not overwrite another user's update.

## Requirements

### Requirement 1: OATM-REQ-F-059 (business rule)

#### Acceptance criteria

1. When the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation ('N'), and not PF12 after the account details are fetched, the system shall reject the requested key operation and treat the request as Enter, while allowed keys keep their requested operation. (rules OATM-BR-058)
2. GIVEN key pressed: PF5; update state: changes not yet validated (not 'N') WHEN the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation (`'N'`), and not PF12 after the account details are fetched THEN PF5 is not allowed; the request is treated as Enter and the screen is processed again (OATM-C06-AC-01; OATM-BR-058)
3. GIVEN key pressed: PF5; update state: 'N' (changes OK, awaiting confirmation) WHEN the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation (`'N'`), and not PF12 after the account details are fetched THEN PF5 is valid and the save goes ahead (OATM-C06-AC-02; OATM-BR-058)
4. GIVEN key pressed: PF12; account details: not yet fetched WHEN the operator presses a key that is not Enter, not PF3, not PF5 while changes are pending confirmation (`'N'`), and not PF12 after the account details are fetched THEN PF12 is not allowed; the request is treated as Enter (OATM-C06-AC-03; OATM-BR-058)

### Requirement 2: OATM-REQ-F-060 (error handling)

#### Acceptance criteria

1. If any stored account or customer value differs from the value fetched when the details were shown, then the system shall flag 'Record changed by some one else. Please review' and stop the save. (rules OATM-BR-059)
2. GIVEN credit limit when details were shown: 5000.00; credit limit in file at save (PF5): 7000.00 WHEN any stored account or customer value differs from the value fetched when the details were shown THEN Save stops, nothing is rewritten, the details are shown again with 'Record changed by some one else. Please review' (OATM-C06-AC-04; OATM-BR-059)
3. GIVEN customer last name when shown: SMITH; customer last name in file at save: smith WHEN any stored account or customer value differs from the value fetched when the details were shown THEN Treated as unchanged (case is ignored) and the save continues (OATM-C06-AC-05; OATM-BR-059)
4. GIVEN all account and customer values: same as when shown WHEN any stored account or customer value differs from the value fetched when the details were shown THEN Save continues to rewrite the account and customer records (OATM-C06-AC-06; OATM-BR-059)

### Requirement 3: OATM-REQ-F-061 (design note)

#### Acceptance criteria

1. When a confirmed account update is saved, the system shall rewrite the account record from a layout that has no ZIP field, so that the entered account group ID goes into the stored ZIP position (offsets 103-112) and the stored group-ID position is overwritten with whatever the unset filler area holds. (rules OATM-BR-060)
2. GIVEN account 00000000099 has stored ZIP and account group values, and the operator has changed the account group to 'GOLDGROUP1' and confirmed the update WHEN the update is saved THEN legacy behaviour to reconcile against: the stored ZIP position (offsets 103-112) holds 'GOLDGROUP1', and the stored group-ID position holds the content of the unset filler area instead of the entered group (OATM-C06-AC-07; OATM-BR-060)
