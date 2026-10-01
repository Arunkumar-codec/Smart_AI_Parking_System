# Database Decisions

## Enum strategy
VARCHAR + CHECK constraints are used instead of PostgreSQL native ENUM types to keep status evolution straightforward for Alembic migrations.

## Double-booking
PostgreSQL `tstzrange` + GiST exclusion constraints provide atomic database-level overlap protection.

## Draft holds
Draft holds are persistent Booking records with `hold_expires_at`; Redis is not the authoritative booking store.

## SOSS
The Smart Operation Session State is transient application/conversation state and is intentionally not represented by a persistent PostgreSQL OperationSession table in Phase 3.

## Vector indexing
HNSW with `vector_cosine_ops` is used for the stated 1536-dimensional embedding workload.

## Money
`NUMERIC(12,2)` is used to avoid floating-point monetary rounding.

## Timezones
Timezone-aware timestamps are used; UTC is the storage convention and location IANA timezones are used for localized presentation.
