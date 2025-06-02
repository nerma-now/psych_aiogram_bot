from typing import Optional

from aiogram.filters import Filter
from aiogram.types import Message

from infrastructure.database.models import User


class IsActivated(Filter):
    async def __call__(
        self,
        message: Message,
        user: Optional[User]
    ) -> bool:
        if user is None:
            return False

        return bool(user.is_activated)

__all__ = ['IsActivated']