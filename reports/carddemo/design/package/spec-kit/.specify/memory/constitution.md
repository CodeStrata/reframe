# aws-carddemo modernization constitution

## Non-negotiables

1. The legacy source is read-only; it is the reference, never changed.
2. Data is synthetic only; no production or personal data in code, tests or logs.
3. Every requirement, rule, acceptance criterion and task keeps its ID, so the build stays traceable to the legacy source (traceability.md).
4. The target stack is the engineer's: not given yet; nothing that depends on it is built until it is.
5. Final capabilities (signed off) are built to as written; draft ones are confirmed with the owner first.
6. Order of replacement: final capabilities first; the risk-ranked order (P4-12) will replace this when it exists.
7. A business rule is kept exactly; a historical artifact is carried only after asking.

## Roles

- `business-rules`: Implements the capability's business rules and requirements exactly as specified, in the service layer.
- `ui-modernization`: Builds the modern screens to the prototype in ui-reference/ and the screen specifications.
- `data`: Models the data contracts on the target stack: tables, entities and their types.
- `api`: Builds the services and scheduled jobs the capability runs as, from the design notes.
- `test-generation`: Writes an automated test for every acceptance criterion, named by its ID.
- `compliance`: Reviews capabilities that touch money, card data, personal data, security or audit.

## Technical context

- **Language and version:** [FILL IN: language and version]
- **Primary dependencies:** [FILL IN: frameworks and libraries]
- **Storage:** [FILL IN: database and version]
- **Front end:** [FILL IN: UI framework and component library]
- **Testing:** [FILL IN: test frameworks]
- **Target platform:** [FILL IN: runtime and hosting]
- **Performance goals:** [FILL IN: response times and batch windows]
- **Constraints:** [FILL IN: limits the build must respect]
- **Scale and scope:** [FILL IN: users, volumes, data size]

## House conventions

- Coding standards: [FILL IN: style guide, linters and formatters]
- Naming: [FILL IN: packages, modules, classes, endpoints, tables]
- Error handling and logging: [FILL IN: exception policy, log format, what is never logged (card numbers, personal data)]
- Style reference: [FILL IN: path or link to the house's example screens and code, or its design system]
- Branching and review: [FILL IN: branch naming, pull request rules, who reviews]
- Definition of done: [FILL IN: the checks a task must pass: tests, coverage, review, security scan]

## Conventions

- Keep every ID: name the requirement and rule IDs in a comment where they are implemented, and each acceptance criterion's ID in its test.
- A business rule is kept exactly; formatting may be restyled; error handling keeps its messages word for word; ask before carrying a historical artifact.
- The legacy source is read-only and only for reference. Use synthetic data only, never production or personal data.
- Build a draft capability only after the owner confirms it; build final ones first.
- Money is an exact decimal, never a float; keep each field's precision from the data contracts.
- The screens follow the prototype in the Claude Code form's ui-reference/ and the screen specifications; meet WCAG 2.2 AA.
