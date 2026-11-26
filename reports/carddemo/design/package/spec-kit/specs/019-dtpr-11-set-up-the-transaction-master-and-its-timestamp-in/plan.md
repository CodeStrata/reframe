# Implementation plan: Set up the transaction master and its timestamp index (DTPR-C11)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

No screens: it runs as scheduled job.

## Data model

None found in the source.

## Design notes

- DTPR-BR-072: Provide a setup or seeding job that empties the transaction store (drop and recreate, or truncate) and bulk-loads every record from the initial daily transaction file. It is for environment setup only and must never be part of the regular daily schedule.
- DTPR-BR-073: Add a secondary, non-unique index on the transaction's processed timestamp, the 26-character value at offset 304 in the legacy record, alongside the primary key on transaction ID. In a relational store this is an ordinary database index kept up to date automatically rather than rebuilt after loading.

## Decision tables

None.
