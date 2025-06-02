from typing import Optional

from aiogram.filters import Filter
from aiogram.types import Message

from infrastructure.database.models import Subscription, User


class ActiveSubscription(Filter):
    async def __call__(
        self,
        message: Message,
        user: Optional[User],
        subscription: Optional[Subscription]
    ) -> bool:
        if user is None:
            return False

        return bool(subscription)

__all__ = ['ActiveSubscription']