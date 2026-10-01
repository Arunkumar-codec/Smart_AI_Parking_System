from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.models.models import Payment, PaymentAttempt
from .base import BaseRepository

class PaymentRepository(BaseRepository):
    async def get_by_booking(self, booking_id, organization_id):
        stmt=select(Payment).where(Payment.booking_id==booking_id, Payment.organization_id==organization_id)
        return (await self.session.execute(stmt)).scalar_one_or_none()
    async def attempts(self, payment_id, organization_id):
        stmt=select(PaymentAttempt).where(PaymentAttempt.payment_id==payment_id, PaymentAttempt.organization_id==organization_id).order_by(PaymentAttempt.attempt_number)
        return list((await self.session.execute(stmt)).scalars())
