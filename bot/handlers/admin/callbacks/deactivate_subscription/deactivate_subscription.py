from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.filters import IsSuperadmin, IsAdmin
from bot.handlers.admin.callback_factory import DeactivateSubscriptionCallback

from .state_factory import DeactivateSubscriptionState


router: Router = Router(name=__name__)


@router.callback_query(
    DeactivateSubscriptionCallback.filter(), IsAdmin(), IsSuperadmin()
)
async def deactivate_subscription_callback(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=_("get_telegram_id"))

    await state.set_state(DeactivateSubscriptionState.telegram_id)


__all__ = ["router"]
