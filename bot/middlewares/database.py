from typing import Awaitable, Callable, Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

from infrastructure.database import database


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[None]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        async with database.session() as session:
            data['database'] = session
            try:
                return await handler(event, data)
            finally:
                await session.close()

__all__ = ['DatabaseMiddleware']