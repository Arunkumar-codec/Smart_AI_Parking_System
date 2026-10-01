# Database Query Patterns

## Tenant-scoped lookup
Always include `organization_id` when reading or mutating organization-owned records.

## Active booking overlap
Use `start_at < requested_end` and `end_at > requested_start` for application-level availability checks. The PostgreSQL exclusion constraint remains the final concurrency guard.

## Row locking
Use `SELECT ... FOR UPDATE` around mutation workflows that need pessimistic locking.

## Vector retrieval
Filter by `organization_id` before ordering by cosine distance and applying the result limit.
