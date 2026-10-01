from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import TSTZRANGE
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from backend.app.db.base import Base

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class Organization(TimestampMixin, Base):
    __tablename__='organizations'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default='UTC', nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class User(TimestampMixin, Base):
    __tablename__='users'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    __table_args__=(UniqueConstraint('organization_id','email', name='uq_users_org_email'),)

class Role(Base):
    __tablename__='roles'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    __table_args__=(UniqueConstraint('organization_id','name', name='uq_roles_org_name'),)

class Employee(TimestampMixin, Base):
    __tablename__='employees'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=False, unique=True)
    employee_code: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    __table_args__=(UniqueConstraint('organization_id','employee_code', name='uq_employees_org_code'),)

class Location(TimestampMixin, Base):
    __tablename__='locations'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    timezone: Mapped[str] = mapped_column(String(64), default='UTC', nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class ParkingArea(TimestampMixin, Base):
    __tablename__='parking_areas'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    location_id: Mapped[str] = mapped_column(ForeignKey('locations.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

class Floor(TimestampMixin, Base):
    __tablename__='floors'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    parking_area_id: Mapped[str] = mapped_column(ForeignKey('parking_areas.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

class Zone(TimestampMixin, Base):
    __tablename__='zones'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    floor_id: Mapped[str] = mapped_column(ForeignKey('floors.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

class ParkingSlot(TimestampMixin, Base):
    __tablename__='parking_slots'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    zone_id: Mapped[str] = mapped_column(ForeignKey('zones.id'), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    vehicle_type: Mapped[str] = mapped_column(String(40), default='ANY', nullable=False)
    status: Mapped[str] = mapped_column(String(30), default='AVAILABLE', nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    __table_args__=(UniqueConstraint('organization_id','code', name='uq_slots_org_code'), CheckConstraint("status IN ('AVAILABLE','RESERVED','OCCUPIED','BLOCKED','MAINTENANCE')", name='slot_status'),)

class Vehicle(TimestampMixin, Base):
    __tablename__='vehicles'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    registration_number: Mapped[str] = mapped_column(String(40), nullable=False)
    vehicle_type: Mapped[str] = mapped_column(String(40), nullable=False)
    model: Mapped[str] = mapped_column(String(120), nullable=True)
    is_ev: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    __table_args__=(UniqueConstraint('organization_id','registration_number', name='uq_vehicles_org_registration'),)

class Booking(TimestampMixin, Base):
    __tablename__='bookings'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    vehicle_id: Mapped[str] = mapped_column(ForeignKey('vehicles.id'), nullable=False, index=True)
    parking_slot_id: Mapped[str] = mapped_column(ForeignKey('parking_slots.id'), nullable=False, index=True)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default='DRAFT', nullable=False)
    hold_expires_at: Mapped[datetime|None] = mapped_column(DateTime(timezone=True), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default='INR', nullable=False)
    price_amount: Mapped[Decimal] = mapped_column(Numeric(12,2), default=0, nullable=False)
    price_snapshot: Mapped[str|None] = mapped_column(Text, nullable=True)
    booking_range = mapped_column(TSTZRANGE, nullable=True)
    __table_args__=(CheckConstraint('end_at > start_at', name='booking_time'), CheckConstraint('price_amount >= 0', name='booking_price_nonnegative'), CheckConstraint("status IN ('DRAFT','PENDING','CONFIRMED','ACTIVE','COMPLETED','CANCELLED','EXPIRED')", name='booking_status'),)

class Payment(TimestampMixin, Base):
    __tablename__='payments'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    booking_id: Mapped[str] = mapped_column(ForeignKey('bookings.id'), nullable=False, unique=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default='INR', nullable=False)
    status: Mapped[str] = mapped_column(String(30), default='PENDING', nullable=False)
    provider_reference: Mapped[str|None] = mapped_column(String(200), nullable=True)
    __table_args__=(CheckConstraint('amount >= 0', name='payment_amount_nonnegative'), CheckConstraint("status IN ('PENDING','SUCCESS','FAILED','REFUNDED')", name='payment_status'),)

class ParkingSession(TimestampMixin, Base):
    __tablename__='parking_sessions'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    booking_id: Mapped[str] = mapped_column(ForeignKey('bookings.id'), nullable=False, unique=True)
    vehicle_id: Mapped[str] = mapped_column(ForeignKey('vehicles.id'), nullable=False)
    parking_slot_id: Mapped[str] = mapped_column(ForeignKey('parking_slots.id'), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default='NOT_STARTED', nullable=False)
    entry_at: Mapped[datetime|None] = mapped_column(DateTime(timezone=True), nullable=True)
    expected_exit_at: Mapped[datetime|None] = mapped_column(DateTime(timezone=True), nullable=True)
    exit_at: Mapped[datetime|None] = mapped_column(DateTime(timezone=True), nullable=True)
    final_fee: Mapped[Decimal|None] = mapped_column(Numeric(12,2), nullable=True)
    __table_args__=(CheckConstraint("status IN ('NOT_STARTED','ACTIVE','COMPLETED')", name='session_status'), CheckConstraint('final_fee IS NULL OR final_fee >= 0', name='session_fee_nonnegative'),)

class AuditRecord(Base):
    __tablename__='audit_records'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    actor_user_id: Mapped[str|None] = mapped_column(ForeignKey('users.id'), nullable=True)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str|None] = mapped_column(String(100), nullable=True)
    details: Mapped[str|None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class KnowledgeDocument(TimestampMixin, Base):
    __tablename__='knowledge_documents'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    source_uri: Mapped[str|None] = mapped_column(Text, nullable=True)
    content_hash: Mapped[str|None] = mapped_column(String(128), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class KnowledgeDocumentChunk(Base):
    __tablename__='knowledge_document_chunks'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    document_id: Mapped[str] = mapped_column(ForeignKey('knowledge_documents.id'), nullable=False, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding = mapped_column(Vector(1536), nullable=True)
    __table_args__=(UniqueConstraint('document_id','chunk_index', name='uq_chunks_document_index'),)

class EmployeeLocationAssignment(Base):
    __tablename__='employee_location_assignments'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey('employees.id'), nullable=False, index=True)
    location_id: Mapped[str] = mapped_column(ForeignKey('locations.id'), nullable=False, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    __table_args__=(UniqueConstraint('employee_id','location_id', name='uq_employee_location'),)

class IdempotencyRecord(Base):
    __tablename__='idempotency_records'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    key: Mapped[str] = mapped_column(String(200), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    response_status: Mapped[int|None] = mapped_column(Integer, nullable=True)
    response_body: Mapped[str|None] = mapped_column(Text, nullable=True)
    __table_args__=(UniqueConstraint('organization_id','key', name='uq_idempotency_org_key'),)

class BookingStatusHistory(Base):
    __tablename__='booking_status_history'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    booking_id: Mapped[str] = mapped_column(ForeignKey('bookings.id'), nullable=False, index=True)
    old_status: Mapped[str|None] = mapped_column(String(30), nullable=True)
    new_status: Mapped[str] = mapped_column(String(30), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class PaymentAttempt(Base):
    __tablename__='payment_attempts'
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey('organizations.id'), nullable=False, index=True)
    payment_id: Mapped[str] = mapped_column(ForeignKey('payments.id'), nullable=False, index=True)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    provider_reference: Mapped[str|None] = mapped_column(String(200), nullable=True)
    __table_args__=(UniqueConstraint('payment_id','attempt_number', name='uq_payment_attempt'),)
