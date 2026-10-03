from datetime import datetime, timezone
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ResponseEnvelope(BaseModel, Generic[T]):
    data: T
    message: str = "Operation successful"


class HealthCheckResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str = Field(..., examples=["healthy"])
    environment: str
    version: str
    timestamp: datetime


class DatabaseHealthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str
    database: str
    latency_ms: float
    extensions: list[str]
    timestamp: datetime
