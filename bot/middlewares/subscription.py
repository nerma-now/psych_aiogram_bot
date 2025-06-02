from typing import Awaitable, Callable, Any, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from infrastructure.database.crud import SubscriptionRepository
from infrastructure.database.models import Subscription


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[None]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        subscription: Optional[Subscription] = await SubscriptionRepository().get_active(
            session=data['database'],
            telegram_id=event.from_user.id,
        )

        data['subscription'] = subscription

        return await handler(event, data)

__all__ = ['SubscriptionMiddleware']