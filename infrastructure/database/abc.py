from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    def __init__(
        self,
        url: str,
        *args,
        **kwargs
    ):
        self.url: str = url

    @abstractmethod
    async def dispose(self, *args, **kwargs):
        raise NotImplementedError()

    @property
    @abstractmethod
    async def session(self, *args, **kwargs):
        raise NotImplementedError()

__all__ = ['AbstractRepository']