# Phase 3 Gemini Master Prompt

Use the Phase 3 master prompt provided in the ChatGPT conversation as the authoritative implementation/design instruction.

Phase 3 scope:
- conceptual data model
- relational entities and relationships
- multi-tenancy
- constraints
- booking overlap protection
- draft holds
- parking sessions
- payments
- idempotency
- SOSS persistence boundary
- audit
- RAG/pgvector
- timezone
- money
- enums
- normalization
- indexes
- FK/delete behavior
- security/tenant isolation
- PostgreSQL DDL
- SQLAlchemy 2.0 mapping
- Alembic design
- transaction boundaries
- consistency rules
- state machines
- lifecycle
- sample data
- database query scenarios
- performance/failure handling
- decision/risk registers
- traceability
- ER diagram
- Phase 4 handoff

Strict boundary:
Do NOT implement FastAPI controllers, frontend, LangGraph agents, RAG runtime logic, or Phase 4 application services.

Before generating implementation code, resolve contradictions and ambiguous database decisions explicitly in the Phase 3 Data Decision Register.
