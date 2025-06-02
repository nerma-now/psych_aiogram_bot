from abc import ABC, abstractmethod

class AbstractRepository(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def set(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError

__all__ = ['AbstractRepository']