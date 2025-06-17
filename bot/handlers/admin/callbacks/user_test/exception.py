from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram.utils.i18n import gettext as _

from .exception_factory import NotFoundCompeletedException


router: Router = Router(name=__name__)


@router.error(ExceptionTypeFilter(NotFoundCompeletedException))
async def not_found_exception_handler(event: ErrorEvent):
    if hasattr(event, "update") and event.update.message:
        await event.update.message.answer(_("not_found_test_completed_exception"))

        return

    if hasattr(event, "update") and event.update.callback_query:
        await event.update.callback_query.answer(
            _("not_found_test_completed_exception"), show_alert=True
        )

        return


__all__ = ["router"]
