from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.filters import IsSuperadmin, IsAdmin
from .state_factory import SetAdminState

from bot.handlers.admin.callback_factory import SetAdminCallback


router: Router = Router(
    name=__name__
)

@router.callback_query(SetAdminCallback.filter(), IsAdmin(), IsSuperadmin())
async def set_admin_callback(
    query: CallbackQuery,
    state: FSMContext
):
    await query.message.answer(
        text=_('get_telegram_id')
    )

    await state.set_state(SetAdminState.telegram_id)


__all__ = ['router']