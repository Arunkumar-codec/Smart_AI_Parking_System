from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.models.models import KnowledgeDocumentChunk

class KnowledgeRepository:
    def __init__(self, session: AsyncSession): self.session=session
    async def similarity_search(self, organization_id, embedding, limit=5):
        distance = KnowledgeDocumentChunk.embedding.cosine_distance(embedding)
        stmt=(select(KnowledgeDocumentChunk)
              .where(KnowledgeDocumentChunk.organization_id==organization_id)
              .order_by(distance).limit(limit))
        return list((await self.session.execute(stmt)).scalars())
