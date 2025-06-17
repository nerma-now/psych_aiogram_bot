from .base import BaseRepository

from typing import Optional

from sqlalchemy import Result, Select, and_, or_, exists
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models import Praxi, ReceivePraxi


class PraxiRepository(BaseRepository[Praxi]):
    model = Praxi

    async def get_first(
        self, 
        session: AsyncSession
    ) -> Optional[model]:
        result: Result = await session.execute(
            Select(self.model)
            .order_by(self.model.created_at.asc())
            .limit(1)
        )

        return result.scalar_one_or_none()
    
    async def get_next_praxi(
        self, 
        session: AsyncSession, 
        telegram_id: int
    ) -> Optional[model]:
        
        last_completed_subq = (
            Select(self.model.created_at)
            .join(ReceivePraxi, ReceivePraxi.praxi_id == self.model.id)
            .where(
                and_(
                    ReceivePraxi.telegram_id == telegram_id,
                    ReceivePraxi.is_completed == True
                )
            )
            .order_by(ReceivePraxi.completed_at.desc())
            .limit(1)
        ).scalar_subquery()

        stmt = (
            Select(Praxi)
            .where(
                Praxi.is_activated == True,
                
                or_(
                    last_completed_subq == None,
                    Praxi.created_at > last_completed_subq
                ),
                
                ~exists().where(
                    and_(
                        ReceivePraxi.praxi_id == Praxi.id,
                        ReceivePraxi.telegram_id == telegram_id,
                        ReceivePraxi.is_completed == True
                    )
                )
            )
            .order_by(Praxi.created_at.asc(), Praxi.id.asc())
            .limit(1)
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()


__all__ = ["PraxiRepository"]
