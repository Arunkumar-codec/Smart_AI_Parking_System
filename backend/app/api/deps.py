from typing import AsyncGenerator

from fastapi import Header, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Expose the Phase 3 async SQLAlchemy session to FastAPI dependencies."""
    async for session in get_session():
        yield session


async def get_request_correlation_id(request: Request) -> str:
    return getattr(request.state, "correlation_id", "N/A")


class UserContextPlaceholder(BaseModel):
    """Phase 5 authentication/tenant context placeholder; not authentication."""
    user_id: str | None = None
    role: str = "ANONYMOUS"
    organization_id: str | None = None


async def get_current_user_context(
    x_organization_id: str | None = Header(None, alias="X-Organization-ID"),
) -> UserContextPlaceholder:
    return UserContextPlaceholder(organization_id=x_organization_id)
