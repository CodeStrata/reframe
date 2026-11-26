# Requirements: Access to transaction type maintenance (TTRDM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Transaction Type Reference Data Maintenance · runs as online · risk high

## Introduction

This records how access to transaction type update and delete works today: when the list is started directly with no sign-on context, the user is treated as an administrator, and update or delete is never checked against the user's type. The new application must not copy this gap silently; who may change transaction type reference data needs an explicit decision and enforcement.

**User story:** As a security officer, I want to know how access to transaction type update and delete is controlled, so that only authorised users can change reference data.

## Requirements

### Requirement 1: TTRDM-REQ-N-002 (business rule)

#### Acceptance criteria

1. When transaction CTLI is started directly with no carried sign-on context, the system shall mark the user as an administrator (user type 'A') and offer list, update and delete without checking who signed on. (rules TTRDM-BR-059)
2. GIVEN Start: CTLI typed at a blank terminal; Signed-on user type: none WHEN transaction CTLI is started directly with no carried sign-on context THEN The full list/update/delete screen is shown and the user is treated as 'A' (TTRDM-C06-AC-01; TTRDM-BR-059)

### Requirement 2: TTRDM-REQ-N-003 (business rule)

#### Acceptance criteria

1. The system shall not check the user type before allowing updates or deletes of transaction types on the Transaction Type List screen. (rules TTRDM-BR-060)
2. GIVEN Carried user type: 'U'; Action: D on a row, then F10 WHEN Transaction Type List screen runs THEN The delete is carried out; user type is not checked (TTRDM-C06-AC-02; TTRDM-BR-060)
