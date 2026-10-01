from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.models.models import Booking
from .base import BaseRepository

ACTIVE_STATUSES = ('DRAFT','PENDING','CONFIRMED','ACTIVE')

class BookingRepository(BaseRepository):
    def __init__(self, session: AsyncSession): super().__init__(session)
    async def get_for_update(self, booking_id, organization_id):
        stmt=select(Booking).where(Booking.id==booking_id, Booking.organization_id==organization_id).with_for_update()
        return (await self.session.execute(stmt)).scalar_one_or_none()
    async def active_for_slot(self, slot_id, start_at: datetime, end_at: datetime, organization_id):
        stmt=select(Booking).where(
            Booking.organization_id==organization_id,
            Booking.parking_slot_id==slot_id,
            Booking.status.in_(ACTIVE_STATUSES),
            Booking.start_at < end_at,
            Booking.end_at > start_at,
        )
        return list((await self.session.execute(stmt)).scalars())
