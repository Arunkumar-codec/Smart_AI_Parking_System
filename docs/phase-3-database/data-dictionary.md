# Data Dictionary

| Table | Purpose |
|---|---|
| organizations | Tenant/root organization |
| users | Authenticated organization users |
| roles | Organization-scoped roles |
| employees | Employee profile and organization membership |
| locations | Physical parking locations |
| parking_areas | Areas within a location |
| floors | Floors within an area |
| zones | Zones within a floor |
| parking_slots | Individual parking spaces |
| vehicles | Customer-owned vehicles |
| bookings | Reservation and draft-hold record |
| payments | Booking payment state |
| parking_sessions | Actual parking usage |
| audit_records | Append-oriented operational audit events |
| knowledge_documents | RAG source documents |
| knowledge_document_chunks | Chunked RAG content and vectors |
| employee_location_assignments | Employee location scope |
| idempotency_records | Duplicate mutation protection |
| booking_status_history | Booking state transitions |
| payment_attempts | Payment retry/attempt history |
