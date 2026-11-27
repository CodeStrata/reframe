---
name: write-acceptance-tests
description: Write an automated test for each acceptance criterion of a capability, named by its ID.
---

# write-acceptance-tests

Write an automated test for each acceptance criterion of a capability, named by its ID.

## Steps

1. For each criterion (GIVEN, WHEN, THEN, with its ID), write one test named by the ID, using the values the criterion gives.
2. Assert the THEN exactly; messages word for word.
3. Test framework: [FILL IN: test frameworks]. Tests live in: [FILL IN: test folders]. Run them with `[FILL IN: the test command]`.
4. A criterion that cannot be tested as written is reported, not changed.
