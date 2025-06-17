from sqlalchemy import Boolean, BigInteger, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from typing import Any

from infrastructure.database.mixins import (
    IdPkMixin,
    CreatedAtPkMixin,
    LastUpdatedAtPkMixin,
)

from .base import Base


class Test(IdPkMixin, CreatedAtPkMixin, LastUpdatedAtPkMixin, Base):
    __tablename__ = "tests"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id"), nullable=False
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=expression.false()
    )
    completed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    score_test_1: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_2: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_3: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_4: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_5: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_6: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_7: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_8: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_9: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_10: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_11: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_12: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_13: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_test_14: Mapped[Integer] = mapped_column(Integer, nullable=True)
    score_all: Mapped[Integer] = mapped_column(Integer, nullable=True)

    def __setattr__(self, name: str, value: Any):
        super().__setattr__(name, value)
        if name.startswith('score_test_'):
            self.score_all = sum(
                getattr(self, f'score_test_{i}') or 0 
                for i in range(1, 15))
            
    def get_last_filled_score(self) -> int | None:
        last_test = 0
        
        for i in range(1, 15):
            score = getattr(self, f'score_test_{i}', None)
            if score is not None:
                last_test = i
        
        return last_test if last_test > 0 else None


    __all__ = ["Test"]
