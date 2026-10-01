import asyncio
from uuid import uuid4
from sqlalchemy import select
from backend.app.db.session import AsyncSessionLocal
from backend.app.db.models.models import Organization

async def main():
    async with AsyncSessionLocal() as session:
        org=(await session.execute(select(Organization).where(Organization.slug=='demo'))).scalar_one_or_none()
        if not org:
            org=Organization(id=str(uuid4()), name='SPMS Demo Organization', slug='demo', timezone='Asia/Kolkata')
            session.add(org); await session.commit()
        print('Seed organization:', org.id)

if __name__=='__main__': asyncio.run(main())
