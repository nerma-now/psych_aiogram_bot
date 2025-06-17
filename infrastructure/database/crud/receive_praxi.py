from .base import BaseRepository

from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from typing import Optional, Any

from infrastructure.database.models import ReceivePraxi


class ReceivePraxiRepository(BaseRepository[ReceivePraxi]):
    model = ReceivePraxi

    async def get_last(
        self, session: AsyncSession, target: InstrumentedAttribute[Any], value: Any
    ) -> Optional[model]:
        result: Result = await session.execute(
            Select(self.model)
            .where(target == value)
            .order_by(self.model.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    async def get_last_uncompleted_test(
        self, session: AsyncSession, telegram_id: int
    ) -> Optional[model]:
        result: Result = await session.execute(
            Select(self.model)
            .where(
                (self.model.telegram_id == telegram_id) &
                (self.model.completed_at == None)
            )
            .order_by(self.model.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


__all__ = ["ReceivePraxiRepository"]
