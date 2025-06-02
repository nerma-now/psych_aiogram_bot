from typing import Awaitable, Callable, Any, Dict

from apscheduler.schedulers.base import BaseScheduler

from aiogram import BaseMiddleware
from aiogram.types import Update


class SchedulerMiddleware(BaseMiddleware):
    def __init__(
        self,
        scheduler: BaseScheduler
    ) -> None:
        self.scheduler: BaseScheduler = scheduler

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[None]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        data['scheduler'] = self.scheduler

        return await handler(event, data)

__all__ = ['SchedulerMiddleware']