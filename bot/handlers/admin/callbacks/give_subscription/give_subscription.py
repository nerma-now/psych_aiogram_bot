from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.filters import IsAdmin, IsSuperadmin
from bot.handlers.admin.callback_factory import GiveSubscriptionCallback

from .state_factory import GiveSubscriptionState


router: Router = Router(name=__name__)


@router.callback_query(GiveSubscriptionCallback.filter(), IsAdmin(), IsSuperadmin())
async def last_user_Test_callback(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=_("get_telegram_id"))

    await state.set_state(GiveSubscriptionState.telegram_id)

__all__ = ["router"]
