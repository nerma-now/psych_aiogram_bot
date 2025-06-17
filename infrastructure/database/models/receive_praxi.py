from sqlalchemy import Boolean, BigInteger, ForeignKey, DateTime, SmallInteger, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from infrastructure.database.mixins import (
    IdPkMixin,
    CreatedAtPkMixin,
    LastUpdatedAtPkMixin,
)

from .base import Base

import uuid
from enum import IntEnum


class ReceivePraxiStatus(IntEnum):
    SENT = 0
    STUDIED = 1

class ReceivePraxiRating(IntEnum):
    OK = 0
    HARD = 1
    EXACT = 2

class ReceivePraxi(IdPkMixin, CreatedAtPkMixin, LastUpdatedAtPkMixin, Base):
    __tablename__ = "receive_praxis"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id"), nullable=False
    )
    praxi_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("praxis.id"),
        nullable=False
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=expression.false()
    )
    completed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[ReceivePraxiStatus] = mapped_column(
        SmallInteger,
        nullable=False,
    )
    rating: Mapped[ReceivePraxiRating] = mapped_column(
        SmallInteger,
        nullable=True
    )


__all__ = ["ReceivePraxi"]
