from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.filters import IsAdmin
from .state_factory import UploadFilesState

from bot.handlers.admin.callback_factory import UploadSubscriptionFiles


router: Router = Router(name=__name__)


@router.callback_query(UploadSubscriptionFiles.filter(), IsAdmin())
async def upload_files_callback(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=_("get_praxi"))

    await state.set_state(UploadFilesState.praxi_id)


__all__ = ["router"]
