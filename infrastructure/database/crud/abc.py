from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic, Optional

from sqlalchemy.orm import DeclarativeBase


T: TypeVar = TypeVar("T", bound=DeclarativeBase)


class AbstractRepository(ABC, Generic[T]):
    model: Type[T]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "model") or cls.model is None:
            raise TypeError(f'{cls.__name__} must define "model" class attribute')

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def add(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError()


__all__ = ["AbstractRepository", "T"]
