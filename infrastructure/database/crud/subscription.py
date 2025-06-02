from datetime import timedelta, datetime
from typing import Optional, Any

from sqlalchemy import Result, Select, and_, or_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from .base import BaseRepository

from infrastructure.database.models import Subscription


class SubscriptionRepository(BaseRepository[Subscription]):
    model = Subscription

    async def get_active(
        self,
        session: AsyncSession,
        telegram_id: int
    ) -> Optional[model]:
        result: Result = await session.execute(
            Select(self.model).where(
                and_(
                    self.model.telegram_id == telegram_id,
                    self.model.is_activated == True,
                    self.model.canceled_at == None,
                    or_(
                        self.model.end_at > func.now()
                    )
                )
            )
        )

        return result.scalar_one_or_none()


    async def get_count(
        self,
        session: AsyncSession,
        target: Optional[InstrumentedAttribute[Any]] = None,
        value: Optional[Any] = None,
        time_period: Optional[timedelta] = None,
        only_active: bool = True,
    ):
        if target is not None:
            if value is not None:
                stmt = select(func.count()).where(target == value)
            else:
                stmt = select(func.count(target.distinct()))
        else:
            stmt = select(func.count())

        stmt = stmt.select_from(self.model)

        if time_period is not None:
            stmt = stmt.where(
                self.model.created_at >= datetime.now() - time_period
            )

        if only_active:
            stmt = stmt.where(self.model.is_activated == True)

        result = await session.execute(stmt)
        return result.scalar()

__all__ = ['SubscriptionRepository']