from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.logging import logger


class BaseService:
    """Base service providing a shared async session and transaction helpers."""

    def __init__(self, db: AsyncSession | None):
        self.db = db

    async def commit(self) -> None:
        if self.db is None:
            raise RuntimeError("Database session is required for commit.")

        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            logger.exception("Transaction commit failed; transaction rolled back.")
            raise

    async def rollback(self) -> None:
        if self.db is not None:
            await self.db.rollback()
