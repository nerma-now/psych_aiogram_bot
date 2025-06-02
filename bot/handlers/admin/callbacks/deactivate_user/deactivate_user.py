from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.filters import IsAdmin
from bot.handlers.admin.callback_factory import DeactivateUserCallback

from .state_factory import DeactivateUserState


router: Router = Router(
    name=__name__
)

@router.callback_query(DeactivateUserCallback.filter(), IsAdmin())
async def deactivate_callback(
    query: CallbackQuery,
    state: FSMContext
):
    await query.message.answer(
        text=_('get_telegram_id')
    )

    await state.set_state(DeactivateUserState.telegram_id)


__all__ = ['router']