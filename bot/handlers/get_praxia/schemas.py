from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

from infrastructure.database.models.receive_praxi import ReceivePraxiRating, ReceivePraxiStatus


class ReceivePraxiCreate(BaseModel):
    telegram_id: int
    praxi_id: UUID
    status: ReceivePraxiStatus = Field(default=ReceivePraxiStatus.SENT)
    rating: Optional[ReceivePraxiRating] = Field(default=None)