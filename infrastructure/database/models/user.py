from sqlalchemy import String, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from infrastructure.database.mixins import (
    IdPkMixin,
    CreatedAtPkMixin,
    LastUpdatedAtPkMixin
)

from .base import Base


class User(IdPkMixin,
           CreatedAtPkMixin,
           LastUpdatedAtPkMixin,
           Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True
    )
    name: Mapped[str] = mapped_column(
        String(128),
        nullable=True
    )
    is_activated: Mapped[bool] = mapped_column(
        Boolean,
        server_default=expression.true(),
        nullable=False
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        server_default=expression.false(),
        nullable=False
    )
    is_superadmin: Mapped[bool] = mapped_column(
        Boolean,
        server_default=expression.false(),
        nullable=False
    )
    language: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

__all__ = ['User']