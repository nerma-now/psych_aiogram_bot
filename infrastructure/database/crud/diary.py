from .base import BaseRepository

from typing import Any, Optional
from datetime import datetime, timedelta

from sqlalchemy import Result, Select, and_, or_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from infrastructure.database.models import Diary


class DiaryRepository(BaseRepository[Diary]):
    model = Diary

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
    
    async def get_count(
        self,
        session: AsyncSession,
        target: Optional[InstrumentedAttribute[Any]] = None,
        value: Optional[Any] = None,
        time_period: Optional[timedelta] = None
    ) -> Optional[int]:
        if target is not None:
            if value is not None:
                stmt = select(func.count()).where(target == value)
            else:
                stmt = select(func.count(target.distinct()))
        else:
            stmt = select(func.count())

        stmt = stmt.select_from(self.model)

        if time_period is not None:
            stmt = stmt.where(self.model.created_at >= datetime.now() - time_period)

        result = await session.execute(stmt)
        return result.scalar()


__all__ = ["DiaryRepository"]
