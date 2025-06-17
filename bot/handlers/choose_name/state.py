import re
from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.test.callback_factory import TestChooseCallback, TestAboutCallback

from infrastructure.database.crud import UserRepository
from infrastructure.database.models import User

from .state_factory import ChooseNameState
from .exception_factory import WrongNameException


router: Router = Router(
    name=__name__
)


@router.message(ChooseNameState.name)
async def choose_name_state(
    message: Message,
    state: FSMContext,
    database: AsyncSession,
    user: Optional[User]
):
    if not re.fullmatch(
        pattern=r'^[^\W_0-9-][\w -]{0,127}$' if len(message.text) > 1 else r'^[^\W_0-9-]$',
        string=message.text,
        flags=re.UNICODE,
    ):
        raise WrongNameException

    await UserRepository().update(
        session=database,
        instance=user,
        name=message.text
    )

    await state.clear()

    await message.answer(
        _("name_received").format(name=message.text),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("about_test_keyboard"),
                        callback_data=TestAboutCallback().pack(),
                    ),
                    InlineKeyboardButton(
                        text=_("start_now_keyboard"),
                        callback_data=TestChooseCallback(answer=-1, job_id="0").pack(),
                    ),
                ]
            ]
        ),
    )


__all__ = ['router']