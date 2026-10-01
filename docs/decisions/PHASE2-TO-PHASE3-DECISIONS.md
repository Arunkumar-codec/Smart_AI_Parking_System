# Phase 2 → Phase 3 Decision Register

| ID | Decision | Phase 3 handling |
|---|---|---|
| CR-01 | Draft hold = 10 minutes | Model hold expiry explicitly |
| CR-02 | Early arrival = 15 minutes | Treat as business configuration |
| CR-03 | Cancellation grace = 2 hours for 100% refund | Store/configure policy; do not hard-code into schema |
| CR-04 | SOSS TTL = 15 minutes | Redis TTL; not automatically a relational retention period |
| CR-05 | Active DRAFT hold makes slot unavailable to search | Reconcile Redis hold and persistent booking correctness |

## Important architectural clarifications

1. Frontend must never directly write Redis.
2. AI Service should access SOSS through a controlled interface rather than unrestricted Redis access.
3. PostgreSQL is the permanent source of truth for bookings, payments, parking sessions and audit records.
4. Redis is transient/high-speed operational state.
5. Booking, ParkingSession, SOSS and Conversation History are separate concepts.
6. Payment records must not store raw payment credentials.
7. Booking overlap protection must be designed carefully for status-aware time ranges.
8. Slot physical state must remain distinct from time-based booking availability.
9. KnowledgeDocument may need a separate KnowledgeDocumentChunk entity.
10. OperationSession may remain Redis-only if persistence is not required.
