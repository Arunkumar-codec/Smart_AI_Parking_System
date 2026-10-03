# Transaction Pattern

Phase 4 establishes a service-level transaction boundary.

Normal pattern:

Service
→ repository operations
→ commit

On failure:

Service
→ rollback
→ propagate error

The implementation uses the existing Phase 3 SQLAlchemy AsyncSession.
It does not introduce a second database/session mechanism.
