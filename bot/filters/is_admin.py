from typing import Optional

from aiogram.filters import Filter
from aiogram.types import Message

from infrastructure.database.models import User


class IsAdmin(Filter):
    async def __call__(
        self,
        message: Message,
        user: Optional[User]
    ) -> bool:
        if user is None:
            return False

        return bool(user.is_admin)

__all__ = ['IsAdmin']