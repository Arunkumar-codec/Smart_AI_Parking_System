# SPMS Phase 4 — Backend Foundation

This archive contains the Phase 4 backend-foundation overlay for the Smart Parking Management System (SPMS).

IMPORTANT:
- This is an overlay on top of the existing Phase 3 repository.
- It does not contain or recreate the Phase 3 database/models/repositories.
- Copy these files into the existing Phase 3 project and preserve the Phase 3 implementation.
- Authentication, complete RBAC, parking features, booking workflows, RAG, agents, and frontend remain future phases.

Expected Phase 3 dependencies include:
- FastAPI
- SQLAlchemy 2.x async
- Pydantic v2 / pydantic-settings
- PostgreSQL / asyncpg
- Alembic
- pytest / pytest-asyncio / httpx

Expected existing Phase 3 modules:
- backend.app.core.config
- backend.app.db.session
- backend.app.db.repositories

Run from the project root after merging with Phase 3:

    uvicorn backend.app.main:app --reload

API:
    GET /api/v1/health
    GET /api/v1/health/db
    GET /docs
    GET /api/v1/openapi.json

Note: database readiness requires a working Phase 3 PostgreSQL environment.


## Phase 3 + Phase 4 integration
- One package root is used everywhere: `backend.app`.
- Phase 4 dependencies use the Phase 3 `get_session` provider directly.
- Phase 3 and Phase 4 share the same `Settings` instance and async SQLAlchemy engine.
- Run the API from the project root with: `python -m uvicorn backend.app.main:app --reload`.
- Phase 5 authentication/RBAC is still intentionally not implemented.
