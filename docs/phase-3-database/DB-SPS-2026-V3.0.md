# SPMS Database Specification — V3.0

## Phase boundary
Phase 3 is the database and data-model foundation. API handlers, full business services, authentication flows, and frontend behavior belong to later phases.

## Core entities
Organization, User, Role, Employee, Location, ParkingArea, Floor, Zone, ParkingSlot, Vehicle, Booking, Payment, ParkingSession, AuditRecord, KnowledgeDocument, KnowledgeDocumentChunk.

## Operational tracking
EmployeeLocationAssignment, IdempotencyRecord, BookingStatusHistory, PaymentAttempt.

## Tenant isolation
Operational, financial, audit, and vector records carry `organization_id` and are expected to be queried with organization scope.

## Booking concurrency
The database uses PostgreSQL `tstzrange` overlap protection for active booking states and repository-level row locking for mutation workflows.

## Draft holds
Draft bookings store `hold_expires_at`. Expiry is evaluated by the application/service layer while the booking row remains the authoritative persistent record.

## Money
Financial values use `NUMERIC(12,2)` and non-negative checks.

## Time
Timestamp values use timezone-aware PostgreSQL timestamps and should be persisted/displayed using UTC plus location IANA timezone for presentation.

## Vector storage
Knowledge chunks use `pgvector` 1536-dimensional embeddings with an HNSW cosine-distance index. Every chunk is organization-scoped.
