---
inclusion: always
---

# House conventions

What your team builds to. Reframe cannot know these; fill them in.

- Coding standards: [FILL IN: style guide, linters and formatters]
- Naming: [FILL IN: packages, modules, classes, endpoints, tables]
- Error handling and logging: [FILL IN: exception policy, log format, what is never logged (card numbers, personal data)]
- Style reference: [FILL IN: path or link to the house's example screens and code, or its design system]
- Branching and review: [FILL IN: branch naming, pull request rules, who reviews]
- Definition of done: [FILL IN: the checks a task must pass: tests, coverage, review, security scan]

## From the design

- Keep every ID: name the requirement and rule IDs in a comment where they are implemented, and each acceptance criterion's ID in its test.
- A business rule is kept exactly; formatting may be restyled; error handling keeps its messages word for word; ask before carrying a historical artifact.
- The legacy source is read-only and only for reference. Use synthetic data only, never production or personal data.
- Build a draft capability only after the owner confirms it; build final ones first.
- Money is an exact decimal, never a float; keep each field's precision from the data contracts.
- The screens follow the prototype in the Claude Code form's ui-reference/ and the screen specifications; meet WCAG 2.2 AA.
