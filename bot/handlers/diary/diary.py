from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import TextOrCommandFilter, ActiveSubscription

from infrastructure.database.crud import DiaryRepository
from infrastructure.database.models import User, Diary

from .exception_factory import CooldownException
from .constants import SELF_DISCOVERY_PROGRAM
from .callback_factory import DiaryCallback


router: Router = Router(name=__name__)


@router.message(
    TextOrCommandFilter(text_key="menu_diary_keyboard", command="diary"),
    ActiveSubscription(),
)
async def diary_command(message: Message, user: User, database: AsyncSession):
    diary: Optional[Diary] = await DiaryRepository().get_last_12h(
        session=database, target=Diary.telegram_id, value=message.from_user.id
    )

    if diary is not None:
        raise CooldownException()

    diary: Optional[Diary] = await DiaryRepository().get_last(
        session=database, target=Diary.telegram_id, value=message.from_user.id
    )

    if diary is None:
        reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("answer_keyboard"),
                        callback_data=DiaryCallback().pack(),
                    )
                ]
            ]
        )

        await message.answer(
            _("diary").format(
                week=1,
                title=SELF_DISCOVERY_PROGRAM[0]["title"],
                question=SELF_DISCOVERY_PROGRAM[0]["points"][0]
            ),
            reply_markup=reply_markup,
        )

        return

    week: int = diary.week
    line: int = diary.line

    if line >= 3:
        week += 1
        line = 0
    else:
        line = line + 1

    if week == 40:
        reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("answer_keyboard"),
                        callback_data=DiaryCallback().pack(),
                    )
                ]
            ]
        )

        await message.answer(
            _("diary").format(
                week=1,
                title=SELF_DISCOVERY_PROGRAM[0]["title"],
                question=SELF_DISCOVERY_PROGRAM[0]["points"][0]
            ),
            reply_markup=reply_markup,
        )

        return

    reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("answer_keyboard"),
                    callback_data=DiaryCallback().pack(),
                )
            ]
        ]
    )

    await message.answer(
        _("diary").format(
            week=week + 1,
            title=SELF_DISCOVERY_PROGRAM[week]["title"],
            question=SELF_DISCOVERY_PROGRAM[week]["points"][line]
        ),
        reply_markup=reply_markup,
    )


__all__ = ["router"]
