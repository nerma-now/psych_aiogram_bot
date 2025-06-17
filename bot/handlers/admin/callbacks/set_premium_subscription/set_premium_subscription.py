from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.filters import IsSuperadmin, IsAdmin
from bot.handlers.admin.callback_factory import SetPremiumSubscriptionCallback

from .state_factory import SetPremiumState


router: Router = Router(name=__name__)


@router.callback_query(SetPremiumSubscriptionCallback.filter(), IsAdmin(), IsSuperadmin())
async def remove_admin_callback(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=_("get_subscription_plan_id"))

    await state.set_state(SetPremiumState.subscription_plan_id)


__all__ = ["router"]
