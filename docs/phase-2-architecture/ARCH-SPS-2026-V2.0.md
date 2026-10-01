# Phase 2 — System Architecture & Technical Design

**Document Reference:** ARCH-SPS-2026-V2.0  
**Baseline:** SRS-SPS-2026-V1.0  
**Status:** Frozen Baseline Architecture Specification

## Objective

Translate Phase 1 requirements into an enterprise-grade deterministic and scalable technical blueprint.

Strict boundary:

- Phase 1 = WHAT
- Phase 2 = HOW system structure
- Phase 3 = HOW data persistence

No implementation code, controllers, React components, migrations, or SQL are part of the architecture baseline.

## Architecture decision

Evaluated:

A. Traditional Monolith  
B. Modular Monolith  
C. Microservices  
D. Modular Backend + Dedicated AI Service  
E. Full Microservices + Independent AI Platform

**Selected: Option D — Modular Backend + Dedicated AI Service**

Reasons:

- isolates resource-heavy AI workloads
- separates Python-centric AI tooling from transactional core
- AI Service is an untrusted client of Core Backend
- AI has no direct PostgreSQL business DB access
- AI calls Core Application interfaces with short-lived user JWT
- operational complexity remains manageable for the project

## High-level topology

### Frontend

- React 18+ / TypeScript / Vite
- Tailwind CSS
- SSE

### Core Backend

- API Gateway / routing / rate limiting
- Authentication & RBAC
- SOSS synchronizer
- Application Services:
  - Organization
  - Parking/Slot
  - Booking
  - Parking Session
  - Payment
  - Pricing
  - Vehicle
  - User/Employee
  - Notification
  - Audit/Report
- Domain/business logic
- Data access/ORM

### AI Service

- NLI ingress / SSE
- conversation context
- intent/entity parser
- LangGraph agentic orchestrator
- RAG retrieval engine
- AI tool execution proxy
- no direct core DB access

### Persistence / infrastructure

- PostgreSQL 16 + pgvector
- Redis 7
- external LLM / Ollama
- background worker
- payment provider abstraction
- notification adapters
- future IoT adapter

## Layered architecture

1. Presentation
2. API/Ingress
3. Authentication & Authorization
4. AI & RAG Orchestration
5. Application Services
6. Domain / Business Logic
7. Data Access
8. Infrastructure

Lower layers cannot depend on higher layers.

## Module boundaries

Modules:

- Auth
- User
- Organization
- Employee
- ParkingFacility
- Availability
- Booking
- Pricing
- Payment
- Parking Session
- Notification
- Audit
- Report
- OperationSession/SOSS
- AI Orchestration
- RAG
- Agent
- Tool Registry

Important dependency rules:

- Organization does not depend on Booking/Payment/ParkingSession.
- ParkingFacility does not depend on Payment/Notification/RAG.
- Booking does not directly use vector store or LLM.
- Pricing is a calculation engine receiving rate DTOs.
- OperationSession/SOSS is transient and does not own permanent payment processing or audit logs.
- AI orchestration does not use core DB repositories directly.

## Domain hierarchy

Organization → Location → Parking Area → Floor → Zone → Parking Slot

Rules:

- operational queries resolve through organization_id
- employee belongs to organization and assigned locations
- employee cannot operate outside assigned locations
- slot has system UUID and human-readable display code

## RBAC

Authorization chain:

1. Authenticate JWT
2. Extract user/role/org/locations
3. Validate role
4. Validate tenant scope
5. Validate location/ownership scope
6. Check domain permission
7. Execute

Roles:

- CUSTOMER
- EMPLOYEE
- ORG_ADMIN
- SUPER_ADMIN

## Manual Mode

Search → availability → select slot → draft + Redis lock → price → payment → confirmed → entry → active session → exit/overstay → complete/release.

Draft hold:

- Redis distributed lock
- 10 minute TTL
- persistent booking after successful payment

## AI Mode

Natural language → AI ingress → conversation context + SOSS → intent/entity extraction → missing parameter evaluation → LangGraph → tool authorization proxy → Core Application Service → structured result → natural language + action card

Guarantees:

- no AI direct DB access
- Pydantic validation
- mutating actions produce structured UI cards and explicit confirmation

## RAG

Ingestion:

- official PDF/Markdown policy documents
- recursive character chunking
- chunk size 512
- overlap 64
- embedding dimension currently 1536
- PostgreSQL pgvector
- organization_id isolation

Runtime:

- policy query
- embedding
- cosine similarity
- threshold >= 0.75
- top K = 3
- tenant isolation
- grounded response with source references

## Agentic architecture

LangGraph state graph:

START/IDLE → intent/state understanding → planning → clarification/HITL → tool execution → success synthesis/error recovery

Guardrails:

- mutating/financial actions pause for confirmation
- maximum 5 graph loops per turn

## Tool architecture

LLM Agent → Tool Validation Schema → Forward JWT → Core REST API

Tools:

- search_parking_slots
- calculate_parking_fee
- create_booking_draft
- confirm_and_pay_booking
- cancel_booking
- override_slot_status

Tool security:

- prompt injection filter
- Pydantic schema validation
- JWT pass-through
- backend RBAC
- financial HITL
- tool allowlist
- Redis token bucket rate limit: 10 calls/minute/session

## SOSS

Redis-backed transient state:

Key:

`soss:{organization_id}:{user_id}:{session_id}`

TTL:

15 minutes

Optimistic locking:

`concurrency_version`

State includes:

- user/org/location
- mode
- step
- vehicle
- slot
- times
- pricing
- booking
- hold expiry

Conversation history is separate from SOSS.

## Mode switching

Manual → AI:

- GUI state syncs to SOSS
- AI reads active SOSS

AI → Manual:

- AI updates SOSS
- GUI receives latest state through SSE

Edge cases:

- manual edit during AI reasoning → optimistic version conflict
- AI update while UI is open → SSE synchronization
- payment in progress → state lock
- SOSS expiry → release draft holds/reset UI

## Slot lifecycle

States:

- AVAILABLE
- RESERVED
- OCCUPIED
- BLOCKED
- MAINTENANCE

Important rule:

OCCUPIED → BLOCKED is forbidden.

BLOCKED → OCCUPIED is forbidden unless returned to AVAILABLE first.

## Booking concurrency

Redis is the performance/pre-check layer.

PostgreSQL exclusion constraints using GiST/range logic are the final mathematical protection against overlapping bookings.

Phase 3 must decide exactly which booking states participate.

## Parking session

Booking CONFIRMED → check-in → ParkingSession ACTIVE → overstay evaluation → checkout → ParkingSession COMPLETED and slot AVAILABLE.

## Payment

Adapter:

`IPaymentProvider`

Current driver:

- Mock

Future example:

- Stripe

Payment operations use unique idempotency keys.

## Notifications

Asynchronous worker-based notification architecture:

- email
- SMS
- in-app
- SSE

## Audit

Separate audit categories:

- manual action
- AI action
- security/RBAC

Sensitive data is masked.

## API categories

- /api/v1/auth
- /api/v1/users
- /api/v1/vehicles
- /api/v1/organizations
- /api/v1/employees
- /api/v1/locations
- /api/v1/slots
- /api/v1/availability
- /api/v1/bookings
- /api/v1/payments
- /api/v1/sessions
- /api/v1/notifications
- /api/v1/reports
- /api/v1/audit
- /api/v1/ai
- /api/v1/operation-sessions

## Frontend

React component modules for:

- authentication
- customer/workflow UI
- admin/management
- AI assistant
- SSE/SOSS synchronization

## Real-time

SOSS update → Redis Pub/Sub → SSE controller → browser EventSource → React re-render

Frontend must NOT directly access Redis.

## Background workers

- booking hold expiration every 30 seconds
- SOSS cleanup every 5 minutes
- notification worker continuously
- overstay detection every 60 seconds

## Adapter interfaces

- ILLMProvider
- IVectorStore
- IPaymentProvider
- INotificationProvider

## Selected stack

Frontend:

- React 18+ / TypeScript / Vite
- Tailwind
- Lucide
- Formik / Zod

Backend:

- Python 3.11+
- FastAPI
- asyncio
- PostgreSQL 16
- pgvector
- SQLAlchemy 2.0 async
- Alembic
- Redis 7
- LangGraph
- LangChain Core
- OpenAI API / Ollama local
- SSE
- ARQ / Celery
- Docker / Docker Compose

## Conceptual Phase 3 entities

1. Organization
2. User
3. Role
4. Employee
5. Location
6. ParkingArea
7. Floor
8. Zone
9. ParkingSlot
10. Vehicle
11. Booking
12. Payment
13. ParkingSession
14. OperationSession
15. AuditRecord
16. KnowledgeDocument

Phase 3 must decide whether supporting entities such as KnowledgeDocumentChunk, role assignments, employee-location assignments, and durable idempotency records are necessary.

## Phase 2 decisions

- Draft hold = 10 minutes
- Early arrival = 15 minutes
- Cancellation grace = 2 hours for 100% refund
- SOSS TTL = 15 minutes
- RAG threshold = 0.75
- RAG top K = 3

These should be treated as configuration/business constraints, not scattered hard-coded database assumptions.

## Phase 3 handoff

Phase 3 must deliver:

- relational schema
- relationships
- tenant boundaries
- attributes
- PK/FK
- constraints
- indexes
- booking overlap model
- SOSS persistence boundary
- audit model
- payment model
- RAG/pgvector model
- SQLAlchemy mapping
- Alembic baseline migration
