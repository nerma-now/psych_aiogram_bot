from typing import Optional

from aiogram.filters import Filter
from aiogram.types import Message

from infrastructure.database.models import User


class IsSuperadmin(Filter):
    async def __call__(
        self,
        message: Message,
        user: Optional[User]
    ) -> bool:
        if user is None:
            return False

        return bool(user.is_superadmin)

__all__ = ['IsSuperadmin']