# ER / Hierarchy Overview

```text
Organization
 ├── Users ── Vehicles
 ├── Roles
 ├── Employees ── EmployeeLocationAssignment ── Locations
 └── Locations
      └── ParkingArea
           └── Floor
                └── Zone
                     └── ParkingSlot

User + Vehicle + ParkingSlot + time window
                 │
                 └── Booking ── Payment
                        │
                        └── ParkingSession

Organization ── KnowledgeDocument ── KnowledgeDocumentChunk ── Vector
Organization ── AuditRecord
Organization ── IdempotencyRecord
Organization ── BookingStatusHistory
Organization ── PaymentAttempt
```
