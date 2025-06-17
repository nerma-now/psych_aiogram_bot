import asyncio
import logging

from contextlib import suppress

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from bot.config import config
from bot.loader import BotLoader
from bot.middlewares import (
    DatabaseMiddleware,
    SchedulerMiddleware,
    UserMiddleware,
    SubscriptionMiddleware,
)

from infrastructure.database import database


async def on_startup_polling() -> None:
    await BotLoader().bot.set_my_description(description=config.description)
    await BotLoader().bot.set_my_short_description(
        short_description=config.short_description
    )
    await BotLoader().bot.set_my_commands(
        commands=[
            BotCommand(command="/start", description="Запуск бота и начального меню"),
            BotCommand(command="/admin", description="Управление ботом"),
            BotCommand(command="/test", description="Пройти тестирование"),
            BotCommand(
                command="/support", description="Контакты технической поддержки"
            ),
            BotCommand(command="/buy", description="Доступные подписки для покупки"),
            BotCommand(command="/diary", description="Личный дневник"),
        ],
        scope=BotCommandScopeDefault(),
    )

    BotLoader().dispatcher.include_router(router=BotLoader().router)

    BotLoader().dispatcher.message.outer_middleware(DatabaseMiddleware())
    BotLoader().dispatcher.callback_query.outer_middleware(DatabaseMiddleware())
    BotLoader().dispatcher.update.outer_middleware(DatabaseMiddleware())

    BotLoader().dispatcher.message.outer_middleware(UserMiddleware())
    BotLoader().dispatcher.callback_query.outer_middleware(UserMiddleware())

    BotLoader().dispatcher.message.outer_middleware(SubscriptionMiddleware())
    BotLoader().dispatcher.callback_query.outer_middleware(SubscriptionMiddleware())

    BotLoader().dispatcher.update.middleware(
        SchedulerMiddleware(scheduler=BotLoader().scheduler)
    )


async def on_shutdown_polling() -> None:
    await BotLoader().dispatcher.storage.close()
    await BotLoader().dispatcher.fsm.storage.close()

    await BotLoader().bot.delete_webhook()
    await BotLoader().bot.session.close()

    await database.dispose()


async def main() -> None:
    BotLoader().dispatcher.startup.register(on_startup_polling)
    BotLoader().dispatcher.shutdown.register(on_shutdown_polling)

    bot: Bot = BotLoader().bot

    await BotLoader().dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(**BotLoader().logging)

    with suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
