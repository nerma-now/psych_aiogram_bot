from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.filters import IsAdmin
from bot.handlers.admin.callback_factory import ActivateUserCallback

from .state_factory import ActivateUserState


router: Router = Router(name=__name__)


@router.callback_query(ActivateUserCallback.filter(), IsAdmin())
async def activate_callback(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=_("get_telegram_id"))

    await state.set_state(ActivateUserState.telegram_id)


__all__ = ["router"]
