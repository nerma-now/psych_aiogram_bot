from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.filters import IsAdmin
from bot.handlers.admin.callback_factory import CreatePraxiCallback

from .state_factory import CreatePraxiState


router: Router = Router(name=__name__)


@router.callback_query(CreatePraxiCallback.filter(), IsAdmin())
async def remove_admin_callback(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=_("subscription_get_title"))

    await state.set_state(CreatePraxiState.title)


__all__ = ["router"]
