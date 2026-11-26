# Requirements: Save customised installation members as copies (UP-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as service · risk low

## Introduction

Saves each customised installation member as a separate copy, so installers can re-run the customisation at any time. The member ONCICS is saved as '#ONCICS', and every other member as '@' followed by its name. The shipped templates must never be changed, and each re-run replaces the earlier customised copy.

**User story:** As an installer, I want each customised member saved as a separate copy while the original template stays unchanged, so that I can re-run the customisation and keep the shipped templates intact.

## Requirements

### Requirement 1: UP-REQ-F-093 (design note)

#### Acceptance criteria

1. When the substitutions have been made in a member named 'ONCICS', the system shall save the whole customised text as a new member named '#ONCICS', replacing any existing member of that name. (rules UP-BR-115, UP-BR-116)
2. GIVEN member being edited: ONCICS WHEN the customisation macro has made its substitutions in a member named ONCICS THEN The customised text is saved as member #ONCICS (UP-C12-AC-01; UP-BR-116)

### Requirement 2: UP-REQ-F-094 (historical artifact)

#### Acceptance criteria

1. When the substitutions have been made in a member with any name other than 'ONCICS', the system shall save the whole customised text as a member named '@' followed by the original member name, replacing any existing member of that name. (rules UP-BR-117, UP-BR-118, UP-BR-079, UP-BR-080, UP-BR-081, UP-BR-082, UP-BR-083, UP-BR-084, UP-BR-085, UP-BR-086, UP-BR-087, UP-BR-088, UP-BR-089, UP-BR-090)
2. GIVEN member being edited: DB2CRE WHEN the customisation macro has made its substitutions in any member other than ONCICS THEN The customised text is saved as member @DB2CRE (UP-C12-AC-02; UP-BR-118)

### Requirement 3: UP-REQ-F-095 (design note)

#### Acceptance criteria

1. The system shall leave the original template member unchanged, discarding the edit session after the customised copy has been saved under the prefixed name. (rules UP-BR-119, UP-BR-120)
2. GIVEN member being edited: DB2CRE; member text: DSN=<DB2HLQ>.SDSNLOAD WHEN installation customisation macro runs THEN DB2CRE still contains <DB2HLQ>; @DB2CRE contains the substituted value (UP-C12-AC-03; UP-BR-120)
