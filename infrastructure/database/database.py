from contextlib import asynccontextmanager

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncEngine,
                                    create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession)

from bot.config import config

from .abc import AbstractRepository


class DatabaseRepository(AbstractRepository):
    def __init__(
        self,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
        /,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.engine: AsyncEngine = create_async_engine(
            url=self.url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


database: DatabaseRepository = DatabaseRepository(
    echo=config.database.echo,
    echo_pool=config.database.echo_pool,
    pool_size=config.database.pool_size,
    max_overflow=config.database.max_overflow,
    url=config.database.build_url(
        host=config.database.host
    )
)

__all__ = ['database']