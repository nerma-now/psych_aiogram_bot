from sqlalchemy import String, Boolean, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from infrastructure.database.mixins import (
    IdPkMixin,
    CreatedAtPkMixin,
    LastUpdatedAtPkMixin,
)

from .base import Base


class SubscriptionPlan(IdPkMixin, CreatedAtPkMixin, LastUpdatedAtPkMixin, Base):
    __tablename__ = "subscription_plans"

    is_activated: Mapped[bool] = mapped_column(
        Boolean, server_default=expression.true(), nullable=False
    )
    is_flexible: Mapped[bool] = mapped_column(
        Boolean, server_default=expression.false(), nullable=False
    )
    is_premium: Mapped[bool] = mapped_column(
        Boolean, server_default=expression.false(), nullable=True
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(2048), nullable=False)
    price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    total_classes_monthly: Mapped[int] = mapped_column(Integer, nullable=False)


__all__ = ["SubscriptionPlan"]
