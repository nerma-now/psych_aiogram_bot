from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import TestRepository
from infrastructure.database.models import Test

from bot.filters import ExistUser, TextOrCommandFilter

from .schemas import TestCreate
from .constants import QUESTIONS, OPTIONS
from .callback_factory import TestChooseCallback
from .exception_factory import CooldownException


router: Router = Router(name=__name__)


@router.message(
    TextOrCommandFilter(text_key="menu_test_keyboard", command="test"), ExistUser()
)
async def test_command(message: Message, database: AsyncSession):
    test: Optional[Test] = await TestRepository().get_last_12h(
        session=database, target=Test.telegram_id, value=message.from_user.id
    )

    if test is not None and test.is_completed:
        raise CooldownException()

    test: Optional[Test] = await TestRepository().get_last(
        session=database, target=Test.telegram_id, value=message.from_user.id
    )

    if test is None or test.is_completed:
        await message.answer(_("instruction_test"))
        test = await TestRepository().add(
            session=database,
            target=Test(**TestCreate(telegram_id=message.from_user.id).model_dump()),
        )

    await message.answer(
        QUESTIONS[
            (
                test.get_last_filled_score()
                if test.get_last_filled_score() is not None
                else 0
            )
        ],
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=option,
                    callback_data=TestChooseCallback(
                        answer=OPTIONS[
                            (
                                test.get_last_filled_score()
                                if test.get_last_filled_score() is not None
                                else 0
                            )
                        ].index(option),
                        job_id="0"
                    ).pack(),
                )]
                for option in OPTIONS[
                    (
                        test.get_last_filled_score()
                        if test.get_last_filled_score() is not None
                        else 0
                    )
                ]
            ]
        ),
    )
