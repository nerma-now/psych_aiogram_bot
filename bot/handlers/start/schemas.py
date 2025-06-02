from pydantic import BaseModel

from bot.config import config


class UserCreate(BaseModel):
    telegram_id: int
    language: str = config.i18n.default_locale