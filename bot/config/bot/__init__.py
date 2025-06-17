from pydantic import Field
from pydantic_settings import BaseSettings

from typing import Optional

from bot.config.constants import ENV_FILE_PATH
from bot.config.components import (RedisConfig,
                                   DatabaseConfig,
                                   I18NConfig,
                                   PaymentsConfig)


class BotConfig(BaseSettings):
    debug: bool = Field(default=True)
    token: str = Field(default='<TOKEN>')
    parse_mode: str = Field(default='HTML')
    use_cache: bool = Field(default=True)

    description: Optional[str] = Field(default='Психологический бот')
    short_description: Optional[str] = Field(default='Психологический бот')

    i18n: I18NConfig = I18NConfig()
    redis: RedisConfig = RedisConfig()
    database: DatabaseConfig = DatabaseConfig()
    payments: PaymentsConfig = PaymentsConfig()

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'
        case_sensitive = False
        env_nested_delimiter = '__'
        env_prefix = 'CONFIG__'

__all__ = ['BotConfig']