from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.filters import IsAdmin
from .state_factory import AllFilesState

from bot.handlers.admin.callback_factory import AllSubscriptionFiles


router: Router = Router(name=__name__)


@router.callback_query(AllSubscriptionFiles.filter(), IsAdmin())
async def upload_files_callback(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=_("get_praxi"))

    await state.set_state(AllFilesState.praxi_id)


__all__ = ["router"]
