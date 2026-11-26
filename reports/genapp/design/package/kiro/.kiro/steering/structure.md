---
inclusion: always
---

# Structure

One module per business domain, each with its services, screens and tests; shared parts (the application shell, authentication, data access) in a common module.

- `application-deployment-lifecycle-managem/`: Application Deployment Lifecycle Management
- `customer-record-management/`: Customer Record Management
- `programs-not-in-a-business-function/`: Programs not in a business function
- `unassigned-programs/`: Unassigned programs
- `unclassified/`: Unclassified
- `web-service-interface-generation/`: Web Service Interface Generation

Tests mirror the acceptance criteria: one test per criterion, named by its ID.

## Conventions

- Keep every ID: name the requirement and rule IDs in a comment where they are implemented, and each acceptance criterion's ID in its test.
- A business rule is kept exactly; formatting may be restyled; error handling keeps its messages word for word; ask before carrying a historical artifact.
- The legacy source is read-only and only for reference. Use synthetic data only, never production or personal data.
- Build a draft capability only after the owner confirms it; build final ones first.
- Money is an exact decimal, never a float; keep each field's precision from the data contracts.
- The screens follow the prototype in the Claude Code form's ui-reference/ and the screen specifications; meet WCAG 2.2 AA.
