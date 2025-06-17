from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from infrastructure.database.mixins import (
    IdPkMixin,
    CreatedAtPkMixin,
    LastUpdatedAtPkMixin,
)

from .base import Base


class Praxi(IdPkMixin, CreatedAtPkMixin, LastUpdatedAtPkMixin, Base):
    __tablename__ = "praxis"

    is_activated: Mapped[bool] = mapped_column(
        Boolean, server_default=expression.true(), nullable=False
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    text: Mapped[str] = mapped_column(String(2048), nullable=False)



__all__ = ["Praxi"]
