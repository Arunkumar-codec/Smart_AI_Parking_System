from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository:
    def __init__(self, session: AsyncSession): self.session=session
    async def get(self, model, entity_id, organization_id=None):
        stmt=select(model).where(model.id==entity_id)
        if organization_id is not None and hasattr(model,'organization_id'):
            stmt=stmt.where(model.organization_id==organization_id)
        return (await self.session.execute(stmt)).scalar_one_or_none()
