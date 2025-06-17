from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from .callback_factory import DiaryCallback
from .state_factory import DiaryState


router: Router = Router(name=__name__)


@router.callback_query(DiaryCallback.filter())
async def diary_callback(
    query: CallbackQuery,
    state: FSMContext
):
    await state.set_state(DiaryState.answer)

    await query.message.answer(_("get_diary_answer"))

