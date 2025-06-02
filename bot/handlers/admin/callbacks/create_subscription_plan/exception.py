from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram.utils.i18n import gettext as _

from bot.config import config

from .exception_factory import LengthException, AmountException


router: Router = Router(
    name=__name__
)

@router.error(ExceptionTypeFilter(LengthException))
async def length_exception_handler(
    event: ErrorEvent
):
    if hasattr(event, 'update') and event.update.message:
        await event.update.message.answer(_('subscription_length_exception'))

        return

    if hasattr(event, 'update') and event.update.callback_query:
        await event.update.callback_query.answer(
            _('subscription_length_exception'),
            show_alert=True
        )

        return

@router.error(ExceptionTypeFilter(AmountException))
async def amount_exception_handler(
    event: ErrorEvent
):
    if hasattr(event, 'update') and event.update.message:
        await event.update.message.answer(
            _('subscription_amount_exception').format(
                min_amount=config.payments.min_amount,
                max_amount=config.payments.max_amount,
                currency=config.payments.currency
            )
        )

        return

    if hasattr(event, 'update') and event.update.callback_query:
        await event.update.callback_query.answer(
            _('subscription_amount_exception').format(
                min_amount=config.payments.min_amount,
                max_amount=config.payments.max_amount,
                currency=config.payments.currency
            ),
            show_alert=True
        )

        return

__all__ = ['router']