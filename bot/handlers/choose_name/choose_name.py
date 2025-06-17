from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import UserRepository
from infrastructure.database.models import User

from bot.handlers.test.callback_factory import TestAboutCallback, TestChooseCallback

from .callback_factory import ChooseNameCallback


router: Router = Router(name=__name__)


@router.callback_query(ChooseNameCallback.filter())
async def chose_name_callback(
    query: CallbackQuery,
    state: FSMContext,
    database: AsyncSession,
    user: Optional[User],
):
    await UserRepository().update(
        session=database, instance=user, name=query.from_user.first_name
    )

    await state.clear()

    await query.answer(_("success"))

    await query.message.answer(
        _("name_received").format(name=query.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=_("about_test_keyboard"),
                    callback_data=TestAboutCallback().pack(),
                )],
                [InlineKeyboardButton(
                    text=_("start_now_keyboard"),
                    callback_data=TestChooseCallback(answer=-1, job_id="0").pack(),
                )],
            ]
        ),
    )


__all__ = ["router"]
