from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram.utils.i18n import gettext as _

from .exception_factory import CooldownException


router: Router = Router(name=__name__)


@router.error(ExceptionTypeFilter(CooldownException))
async def invalid_payload_exception_handler(event: ErrorEvent):
    if hasattr(event, "update") and event.update.message:
        await event.update.message.answer(_("cooldown_test_exception"))

        return

    if hasattr(event, "update") and event.update.callback_query:
        await event.update.callback_query.answer(_("cooldown_test_exception"))

        return


__all__ = ["router"]
