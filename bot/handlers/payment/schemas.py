import uuid

from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class SubscriptionCreate(BaseModel):
    telegram_id: int
    plan_id: uuid.UUID
    end_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta(days=31))