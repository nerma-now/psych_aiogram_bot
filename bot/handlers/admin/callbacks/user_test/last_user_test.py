from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.filters import IsAdmin
from bot.handlers.admin.callback_factory import CheckUserTestCallback

from .state_factory import LastUserTestState


router: Router = Router(name=__name__)


@router.callback_query(CheckUserTestCallback.filter(), IsAdmin())
async def last_user_Test_callback(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=_("get_telegram_id"))

    await state.set_state(LastUserTestState.telegram_id)

__all__ = ["router"]
