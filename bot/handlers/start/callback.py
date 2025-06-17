from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.choose_name.state_factory import ChooseNameState
from bot.handlers.choose_name.callback_factory import ChooseNameCallback
from bot.repository.notification import NotificationRepository
from bot.handlers.test.callback_factory import TestAboutCallback, TestChooseCallback

from infrastructure.database.models import User, Test
from infrastructure.database.crud import TestRepository

from .callback_factory import StartNextCallback


router: Router = Router(name=__name__)


@router.callback_query(StartNextCallback.filter())
async def next_callback(
    query: CallbackQuery,
    callback_data: StartNextCallback,
    state: FSMContext,
    database: AsyncSession,
    user: Optional[User],
):
    if callback_data.job_id != '0':
        try:
            NotificationRepository().delete(
                job_id=callback_data.job_id
            )
        except Exception as ex:
            pass

    if user.name is None:
        await query.message.answer(
            _("choose_name"),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=_("name_from_telegram_keyboard"),
                            callback_data=ChooseNameCallback().pack(),
                        )
                    ]
                ]
            ),
        )
        await state.set_state(ChooseNameState.name)

        return

    test: Optional[Test] = await TestRepository().get_last(
        session=database, target=Test.telegram_id, value=query.from_user.id
    )

    if test is None:
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

        return
    
    await query.message.answer(_("continue_for_guest"))

__all__ = ["router"]
