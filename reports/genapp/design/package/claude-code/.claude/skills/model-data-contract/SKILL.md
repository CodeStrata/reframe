---
name: model-data-contract
description: Turn a data contract (a copybook record) into the target stack's entity and table.
---

# model-data-contract

Turn a data contract (a copybook record) into the target stack's entity and table.

## Steps

1. Read the record in data-contracts.md: each field's type, digits, scale, OCCURS, REDEFINES and 88-level values.
2. Keep the precision: a decimal stays an exact decimal; text keeps its length; an OCCURS becomes a child table or a list; 88-level values become an enumeration.
3. Persistence: [FILL IN: ORM or data access library]. Migrations: [FILL IN: migration tool]. Naming: [FILL IN: table and column naming].
4. Keep the copybook and field names in a comment or mapping for data migration.
