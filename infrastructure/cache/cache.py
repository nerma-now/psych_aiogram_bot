from datetime import timedelta

from typing import Optional, Any

from redis.asyncio import Redis

from .abc import AbstractRepository

from bot.config import config


class CacheRepository(AbstractRepository):
    def __init__(
        self,
        redis: Redis
    ):
        self.redis: Redis = redis

    def __call__(self) -> Redis:
        return self.redis

    async def get(
        self,
        name: str | bytes
    ) -> Optional[Any]:
        value: Any = await self.redis.get(
            name=name
        )

        return value

    async def set(
        self,
        name: str | bytes,
        value: bytes | str | int | float,
        ex: Optional[int | timedelta]
    ) -> None:
        await self.redis.set(
            name=name,
            value=value,
            ex=ex
        )

    async def delete(
        self,
        name: str | bytes
    ) -> None:
        await self.redis.delete(
            name
        )

cache: CacheRepository = CacheRepository(
    redis=Redis(
        host=config.redis.host,
        port=config.redis.port,
        password=config.redis.password,
        encoding=config.redis.encoding,
        db=config.redis.database
    )
)

__all__ = ['cache']