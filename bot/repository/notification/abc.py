from abc import ABC, abstractmethod
from typing import Any


class AbstractRepository(ABC):
    provider: Any

    @abstractmethod
    def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def modify(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def send(self, *args, **kwargs):
        raise NotImplementedError

__all__ = ['AbstractRepository']