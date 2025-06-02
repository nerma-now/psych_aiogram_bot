from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.filters import IsSuperadmin
from bot.handlers.admin.callback_factory import CreateSubscriptionPlanCallback
from bot.handlers.admin.callbacks.create_subscription_plan.state_factory import CreateSubscriptionPlanState


router: Router = Router(
    name=__name__
)

@router.callback_query(CreateSubscriptionPlanCallback.filter(), IsSuperadmin())
async def create_subscription_callback(
    query: CallbackQuery,
    state: FSMContext
):
    await query.message.answer(
        text=_('subscription_get_title')
    )

    await state.set_state(CreateSubscriptionPlanState.title)

__all__ = ['router']