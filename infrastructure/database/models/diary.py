from sqlalchemy import String, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.mixins import (
    IdPkMixin,
    CreatedAtPkMixin,
    LastUpdatedAtPkMixin,
)

from .base import Base


class Diary(IdPkMixin, CreatedAtPkMixin, LastUpdatedAtPkMixin, Base):
    __tablename__ = "diarys"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id"), nullable=False
    )
    week: Mapped[Integer] = mapped_column(Integer, nullable=False)
    line: Mapped[Integer] = mapped_column(Integer, nullable=False)
    answer: Mapped[String] = mapped_column(String(2048), nullable=False)

__all__ = ["Diary"]
