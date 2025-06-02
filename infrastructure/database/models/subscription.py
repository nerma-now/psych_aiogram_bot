import uuid

from sqlalchemy import Boolean, BigInteger, ForeignKey, DateTime, func, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from infrastructure.database.mixins import (
    IdPkMixin,
    CreatedAtPkMixin,
    LastUpdatedAtPkMixin
)

from .base import Base


class Subscription(IdPkMixin,
           CreatedAtPkMixin,
           LastUpdatedAtPkMixin,
           Base):
    __tablename__ = 'subscriptions'

    is_activated: Mapped[bool] = mapped_column(
        Boolean,
        server_default=expression.true(),
        nullable=False
    )
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.telegram_id'),
        nullable=False
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('subscription_plans.id'),
        nullable=False
    )
    start_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    end_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    canceled_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    @property
    def is_active(self) -> bool:
        return self.is_activated

    @property
    def is_valid(self) -> bool:
        if self.canceled_at is not None:
            return False

        return self.end_at > func.now()

__all__ = ['Subscription']