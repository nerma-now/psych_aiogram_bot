from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram.utils.i18n import gettext as _

from bot.config import config

from .exception_factory import AmountException


router: Router = Router(name=__name__)


@router.error(ExceptionTypeFilter(AmountException))
async def amount_exception_handler(event: ErrorEvent):
    if hasattr(event, "update") and event.update.message:
        await event.update.message.answer(
            _("subscription_count_days_amount_exception")
        )

        return

    if hasattr(event, "update") and event.update.callback_query:
        await event.update.callback_query.answer(
            _("subscription_count_days_amount_exception")
        )

        return


__all__ = ["router"]
