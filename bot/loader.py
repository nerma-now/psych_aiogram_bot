import sys

from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.base import BaseStorage, DefaultKeyBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n.middleware import ConstI18nMiddleware

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import BaseScheduler

from bot.config import config

from infrastructure.cache import cache


class BaseBotLoader(ABC):
    _bot: Optional[Bot] = None
    _storage: Optional[BaseStorage] = None
    _dispatcher: Optional[Dispatcher] = None
    _i18n: Optional[I18n] = None
    _router: Optional[Router] = None
    _scheduler: Optional[BaseScheduler] = None

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @property
    @abstractmethod
    def bot(self, *args, **kwargs) -> Bot:
        raise NotImplementedError

    @property
    @abstractmethod
    def storage(self, *args, **kwargs) -> BaseStorage:
        raise NotImplementedError

    @property
    @abstractmethod
    def dispatcher(self, *args, **kwargs) -> Dispatcher:
        raise NotImplementedError

    @property
    @abstractmethod
    def logging(self, *args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError

    @property
    @abstractmethod
    def i18n(self, *args, **kwargs) -> I18n:
        raise NotImplementedError

    @property
    @abstractmethod
    def router(self, *args, **kwargs) -> Router:
        raise NotImplementedError

    @property
    @abstractmethod
    def scheduler(self, *args, **kwargs) -> BaseScheduler:
        raise NotImplementedError

class BotLoader(BaseBotLoader):
    @property
    def bot(self) -> Bot:
        if self._bot is not None:
            return self._bot

        bot: Bot = Bot(
            token=config.token,
            default=DefaultBotProperties(
                parse_mode=config.parse_mode
            )
        )

        self._bot = bot

        return bot

    @property
    def storage(self) -> BaseStorage:
        if self._storage is not None:
            return self._storage

        if config.use_cache:
            storage: RedisStorage = RedisStorage(
                redis=cache.redis,
                key_builder=DefaultKeyBuilder(
                    with_bot_id=True
                )
            )

            self._storage = storage

            return storage

        storage: MemoryStorage = MemoryStorage()
        self._storage = storage

        return storage

    @property
    def dispatcher(self) -> Dispatcher:
        if self._dispatcher is not None:
            return self._dispatcher

        dispatcher: Dispatcher = Dispatcher(
            storage=self.storage,
        )

        ConstI18nMiddleware(
            locale=config.i18n.default_locale,
            i18n=self.i18n,
            middleware_key='i18n'
        ).setup(dispatcher)

        self._dispatcher = dispatcher

        return dispatcher

    @property
    def logging(self) -> Dict[str, Any]:
        return {
            'level': 'DEBUG' if config.debug else 'INFO',
            'format': '%(name)s | %(asctime)s | %(levelname)s | %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
            'stream': sys.stdout
        }

    @property
    def i18n(self) -> I18n:
        if self._i18n is not None:
            return self._i18n

        i18n: I18n = I18n(
            path=config.i18n.path,
            default_locale=config.i18n.default_locale,
            domain=config.i18n.domain,
        )
        self._i18n = i18n

        return i18n

    @property
    def router(self) -> Router:
        if self._router is not None:
            return self._router

        router: Router = Router(
            name=__name__
        )

        from bot.handlers import router as handlers_router

        router.include_router(handlers_router)

        self._router = router

        return router

    @property
    def scheduler(self) -> BaseScheduler:
        if self._scheduler is not None:
            return self._scheduler

        scheduler: AsyncIOScheduler = AsyncIOScheduler()

        if config.use_cache:
            scheduler.add_jobstore(
                jobstore=RedisJobStore(
                    host=config.redis.host,
                    port=config.redis.port,
                    password=config.redis.password,
                    encoding=config.redis.encoding,
                    db=config.redis.database
                )
            )
            scheduler.start()

            self._scheduler = scheduler

            return scheduler

        scheduler.add_jobstore(
            jobstore=MemoryJobStore()
        )
        scheduler.start()

        self._scheduler = scheduler

        return scheduler

__all__ = ['BotLoader']