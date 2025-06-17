from .base import BaseRepository

from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from typing import Sequence, Optional, Any

from infrastructure.database.models import PraxiFiles


class PraxiFilesRepository(BaseRepository[PraxiFiles]):
    model = PraxiFiles

    async def get_current_all(
        self, session: AsyncSession, target: InstrumentedAttribute[Any], value: Any,  limit: Optional[int] = None, 
    ) -> Sequence[model]:
        result: Result = await session.execute(Select(self.model).where(target == value).limit(limit))

        return result.scalars().all()

__all__ = ["PraxiFilesRepository"]
