from pathlib import Path
from typing import List

from pydantic import Field, BaseModel

from bot.config.constants import LOCALE_FILE_PATH


class I18NConfig(BaseModel):
    default_locale: str = Field(default='ru')
    domain: str = Field(default='messages')
    locales: List[str] = Field(default=['ru'])
    path: Path = Field(default=LOCALE_FILE_PATH)

__all__ = ['I18NConfig']