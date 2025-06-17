from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from typing import Optional, Any
from datetime import datetime, timedelta

from .base import BaseRepository, T

from infrastructure.database.models import Test


class TestRepository(BaseRepository[Test]):
    model = Test

    async def get_last_12h(
        self, 
        session: AsyncSession, 
        target: InstrumentedAttribute[Any], 
        value: Any
    ) -> Optional[model]:
        time_threshold = datetime.now() - timedelta(hours=12)
        
        query: Select = (
            Select(self.model)
            .where(target == value)
            .where(self.model.created_at >= time_threshold)
            .order_by(self.model.created_at.desc())
            .limit(1)
        )
        
        result: Result = await session.execute(query)
        return result.scalar_one_or_none()

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

    async def get_last_completed(
        self, session: AsyncSession, target: InstrumentedAttribute[Any], value: Any
    ) -> Optional[model]:
        result: Result = await session.execute(
            Select(self.model)
            .where(
                (target == value)
                & (self.model.is_completed == True)
                & (self.model.completed_at.is_not(None))
            )
            .order_by(self.model.completed_at.desc())
            .limit(1)
        )

        return result.scalar_one_or_none()


__all__ = ["TestRepository"]
