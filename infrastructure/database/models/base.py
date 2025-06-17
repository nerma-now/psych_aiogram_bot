from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from bot.config import config


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=config.database.naming_convention)


__all__ = ["Base"]
