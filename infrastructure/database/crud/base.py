from typing import Any, Optional, Sequence

from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from infrastructure.database.models import Base

from .abc import AbstractRepository, T


class BaseRepository(AbstractRepository[T]):
    model = Base

    async def get_all(
        self, session: AsyncSession, limit: Optional[int] = None
    ) -> Sequence[T]:
        result: Result = await session.execute(Select(self.model).limit(limit))

        return result.scalars().all()

    async def get(
        self, session: AsyncSession, target: InstrumentedAttribute[Any], value: Any
    ) -> Optional[T]:
        result: Result = await session.execute(
            Select(self.model).where(target == value)
        )

        return result.scalar_one_or_none()

    async def add(self, session: AsyncSession, target: T) -> Optional[T]:
        session.add(target)

        await session.commit()

        return target

    async def update(self, session: AsyncSession, instance: T, **update_data: Any) -> T:
        for key, value in update_data.items():
            setattr(instance, key, value)

        session.add(instance)
        await session.commit()
        await session.refresh(instance)

        return instance

    async def delete(self, session: AsyncSession, target: T) -> T:
        await session.delete(target)

        await session.commit()

        return target


__all__ = ["BaseRepository"]
