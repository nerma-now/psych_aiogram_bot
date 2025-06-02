from typing import Optional

from pydantic import Field, BaseModel


class RedisConfig(BaseModel):
    host: str = Field(default='redis')
    port: int = Field(default=6379)
    password: Optional[str] = Field(default=None)
    encoding: str = Field(default='utf-8')
    database: str | int = Field(default=0)

__all__ = ['RedisConfig']