from typing import Awaitable, Callable, Any, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from infrastructure.database.crud import UserRepository
from infrastructure.database.models import User


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[None]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user: Optional[User] = await UserRepository().get(
            session=data['database'],
            target=User.telegram_id,
            value=event.from_user.id
        )

        if user is not None and not user.is_activated:
            return

        data['user'] = user

        return await handler(event, data)

__all__ = ['UserMiddleware']