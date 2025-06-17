import uuid
from pydantic import BaseModel, Field
from datetime import datetime, timedelta


class SubscriptionCreate(BaseModel):
    telegram_id: int
    plan_id: uuid.UUID
    end_at: datetime