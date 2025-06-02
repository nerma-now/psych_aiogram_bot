from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram.utils.i18n import gettext as _

from .exception_factory import (InvalidPayloadException,
                                SubscriptionPlanNotFoundException,
                                SubscriptionActiveException)


router: Router = Router(
    name=__name__
)

@router.error(ExceptionTypeFilter(InvalidPayloadException))
async def invalid_payload_exception_handler(
    event: ErrorEvent
):
    if hasattr(event, 'update') and event.update.message:
        await event.update.message.answer(
            _('payment_error').format(
                reason=_('payment_invalid_payload')
            )
        )

        return

    if hasattr(event, 'update') and event.update.callback_query:
        await event.update.callback_query.answer(
            _('duplicative_action_exception'),
            show_alert=True
        )

        return

@router.error(ExceptionTypeFilter(SubscriptionPlanNotFoundException))
async def plan_not_found_exception_handler(
    event: ErrorEvent
):
    if hasattr(event, 'update') and event.update.message:
        await event.update.message.answer(
            _('payment_error').format(
                reason=_('plans_not_found_exception')
            )
        )

        return

    if hasattr(event, 'update') and event.update.callback_query:
        await event.update.callback_query.answer(
            _('payment_error').format(
                reason=_('plans_not_found_exception')
            ),
            show_alert=True
        )

        return

@router.error(ExceptionTypeFilter(SubscriptionActiveException))
async def subscription_active_exception_handler(
    event: ErrorEvent
):
    if hasattr(event, 'update') and event.update.message:
        await event.update.message.answer(
            _('payment_error').format(
                reason=_('subscription_active_exception')
            )
        )

        return

    if hasattr(event, 'update') and event.update.callback_query:
        await event.update.callback_query.answer(
            _('payment_error').format(
                reason=_('subscription_active_exception')
            ),
            show_alert=True
        )

        return

__all__ = ['router']