# Phase 1 — Requirements & System Planning

**Document Reference:** SRS-SPS-2026-V1.0  
**Status:** Approved Baseline / Frozen

## Vision

SPMS is a unified multi-tenant smart parking enterprise platform addressing fragmented parking operations, manual tracking errors, double bookings, underutilized capacity, and rigid user experience.

Core concepts:

- Manual Mode
- AI Mode
- Shared Session & Operation State (SOSS)
- Core enterprise business services
- Persistent database

## Objectives

- Unified enterprise platform
- Role-based multi-tenancy
- Organization → Location → Parking Area → Floor/Zone → Slot
- Dual execution modes
- Seamless state synchronization
- Strict authorization parity
- Ground-truth RAG + deterministic tooling

## MVP scope

In scope:

- Role-based multi-tenancy
- Vehicle-slot compatibility
- Slot/booking/payment/session state engine
- RAG knowledge engine
- Agentic multi-step tool execution
- synchronized manual/AI switching
- mock payment
- comprehensive audit logs

Future/out of scope:

- IoT barrier/camera/ANPR hardware
- direct payment gateway SDKs
- dynamic pricing ML training
- low-level DB engine selection

## OperationSession / SOSS

Key fields:

- session_id
- user_id
- organization_id
- location_id
- vehicle_id
- slot_id
- time_window
- estimated_cost
- booking_id
- step_status
- last_active_mode
- concurrency_version

Example statuses:

- SEARCHING
- SLOT_SELECTED
- PRICED
- PENDING_CONFIRMATION
- PAYMENT_PENDING
- COMPLETED

Rules:

- Rule-SWITCH-01: no loss when switching
- Rule-SWITCH-02: AI mutation triggers UI synchronization
- Rule-SWITCH-03: manual override dominates pending AI draft mutation
- Rule-SWITCH-04: inactive sessions expire after 15 minutes and draft/pending holds are released

## Organization hierarchy

Organization → Location → Parking Area → Floor → Zone → Slot

Constraints:

- Org Admin controls only own organization
- Location/Area may override organization pricing/operating/cancellation defaults
- Slot code is unique within the relevant hierarchy

## Roles

- Super Admin
- Org Admin
- Employee
- Customer/User

## Slot states

- AVAILABLE
- RESERVED
- OCCUPIED
- BLOCKED
- MAINTENANCE

Normal transitions:

- AVAILABLE → RESERVED
- RESERVED → OCCUPIED
- OCCUPIED → AVAILABLE
- RESERVED → AVAILABLE
- ANY → BLOCKED via admin override
- ANY → MAINTENANCE via service schedule

## Booking lifecycle

- DRAFT
- PENDING
- CONFIRMED
- ACTIVE
- COMPLETED
- CANCELLED
- EXPIRED

## Payment lifecycle

- PENDING
- SUCCESS
- FAILED
- REFUNDED

Booking and actual parking session remain distinct.

## Core business rules

- Vehicle must fit slot type/dimensions.
- EV slot fallback requires defined conditions and acknowledgement.
- No double booking for the same physical slot/time.
- Overstay must be calculated.
- AI permissions must equal the user's real permissions.
- AI cannot directly manipulate the database.
- Financial/irreversible AI actions require explicit confirmation.

## Entry / Exit

Entry:

- verify booking/license plate
- booking must be CONFIRMED
- current time must be within allowed arrival window
- booking becomes ACTIVE
- slot becomes OCCUPIED
- parking session is created

Exit:

- identify active session
- compare actual exit with booked end
- calculate overstay if required
- booking becomes COMPLETED
- slot becomes AVAILABLE
- parking session becomes COMPLETED

## AI architecture

RAG is used for factual knowledge:

- policies
- cancellation rules
- operating hours
- EV rules
- FAQs
- employee procedures

Transactional operations use tools.

Candidate tools:

1. search_parking_slots
2. create_booking_draft
3. confirm_and_pay_booking
4. cancel_booking
5. override_slot_status

## Functional requirements

- FR-AUTH-001
- FR-USER-001
- FR-ORG-001
- FR-SLOT-001
- FR-BOOK-001
- FR-PAY-001
- FR-MODE-001
- FR-AI-001
- FR-AI-002

## Non-functional requirements

Security includes:

- authorization at internal domain/service layer
- PII/payment tokens protected in transit and at rest
- license plates masked in external logs

Some numeric NFR values were intentionally left for Phase 2 clarification rather than invented.

## Audit and analytics

AuditRecord includes:

- audit_id
- timestamp
- actor_id
- actor_role
- execution_mode
- action_type
- target_entity_id
- tool_called
- masked input payload
- output status
- IP

Analytics include parking utilization, employee operational analytics, and AI performance.

## Phase 1 candidate technology options

Backend:

- Node.js/TypeScript
- Python/FastAPI
- Go
- Java/Spring Boot

Database:

- PostgreSQL/PostGIS
- MySQL
- MongoDB

Vector:

- pgvector
- Pinecone
- Qdrant
- Milvus

Agent framework candidates:

- LangChain
- LangGraph
- LlamaIndex
- Custom loop

## Phase 1 → Phase 2 handoff

Phase 2 translates these requirements into a technical architecture without implementing application code.
