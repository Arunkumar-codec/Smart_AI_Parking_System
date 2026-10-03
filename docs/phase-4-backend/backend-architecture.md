# Phase 4 Backend Architecture

SPMS Phase 4 establishes:

Client
→ FastAPI Middleware
→ API Router (/api/v1)
→ Service Layer
→ Phase 3 Repository Layer
→ SQLAlchemy AsyncSession
→ PostgreSQL

Cross-cutting concerns:
- configuration
- correlation IDs
- request logging
- exception handling
- dependency injection
- API schema validation

AI compatibility:
Future AI tools must call the same service layer used by normal API requests.
AI must not access PostgreSQL directly.
