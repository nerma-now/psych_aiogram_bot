from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from bot.handlers.choose_name.state_factory import ChooseNameState
from bot.handlers.choose_name.callback_factory import ChooseNameCallback

from infrastructure.database.models import User

from .callback_factory import NextCallbackData


router: Router = Router(
    name=__name__
)

@router.callback_query(NextCallbackData.filter())
async def next_callback(
    query: CallbackQuery,
    state: FSMContext,
    user: Optional[User]
):
    if user.name is None:
        await query.message.answer(
            _('choose_name'),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=_('name_from_telegram_keyboard'),
                            callback_data=ChooseNameCallback().pack()
                        )
                    ]
                ]
            )
        )
        await state.set_state(ChooseNameState.name)

        return

__all__ = ['router']