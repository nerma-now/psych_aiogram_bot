from .base import BaseRepository

from infrastructure.database.models import User


class UserRepository(BaseRepository[User]):
    model = User


__all__ = ["UserRepository"]
