from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram.utils.i18n import gettext as _

from bot.handlers.exception_factory import (WrongTypeException,
                                            NotFoundException,
                                            NotRightsException,
                                            DuplicativeActionException)


router: Router = Router()

@router.error(ExceptionTypeFilter(WrongTypeException))
async def wrong_type_exception_handler(
    event: ErrorEvent
):
    if hasattr(event, 'update') and event.update.message:
        await event.update.message.answer(_('wrong_type_exception'))

        return

    if hasattr(event, 'update') and event.update.callback_query:
        await event.update.callback_query.answer(
            _('wrong_type_exception'),
            show_alert=True
        )

        return

@router.error(ExceptionTypeFilter(NotFoundException))
async def not_found_exception_handler(
    event: ErrorEvent
):
    if hasattr(event, 'update') and event.update.message:
        await event.update.message.answer(_('not_found_exception'))

        return

    if hasattr(event, 'update') and event.update.callback_query:
        await event.update.callback_query.answer(
            _('not_found_exception'),
            show_alert=True
        )

        return

@router.error(ExceptionTypeFilter(DuplicativeActionException))
async def duplicative_action_exception_handler(
    event: ErrorEvent
):
    if hasattr(event, 'update') and event.update.message:
        await event.update.message.answer(_('duplicative_action_exception'))

        return

    if hasattr(event, 'update') and event.update.callback_query:
        await event.update.callback_query.answer(
            _('duplicative_action_exception'),
            show_alert=True
        )

        return

@router.error(ExceptionTypeFilter(NotRightsException))
async def not_right_exception_handler(
    event: ErrorEvent
):
    if hasattr(event, 'update') and event.update.message:
        await event.update.message.answer(_('not_right_exception'))

        return

    if hasattr(event, 'update') and event.update.callback_query:
        await event.update.callback_query.answer(
            _('not_right_exception'),
            show_alert=True
        )

        return

__all__ = ['router']