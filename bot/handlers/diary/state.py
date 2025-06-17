from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession 

from .state_factory import DiaryState
from .schemas import DiaryCreate

from infrastructure.database.models import Diary
from infrastructure.database.crud import DiaryRepository

from bot.repository.notification import NotificationRepository
from bot.repository.notification.schemas import NotificationButton, NotificationCreate



router: Router = Router(name=__name__)


@router.message(DiaryState.answer)
async def diary_state(
    message: Message,
    state: FSMContext,
    database: AsyncSession
):
    if (
        not isinstance(message.text, str)
        or not message.text
        or len(message.text) >= 2048
    ):
        await state.clear()

        await message.answer(_("get_diary_answer"))

        return

    diary: Optional[Diary] = await DiaryRepository().get_last(
        session=database, target=Diary.telegram_id, value=message.from_user.id
    )

    week: int = 0
    line: int = 0

    if diary is not None:
        week: int = diary.week
        line: int = diary.line

        if line >= 3:
            week += 1
            line = 0
        else:
            line = line + 1

    diary_create: DiaryCreate = DiaryCreate(
        telegram_id=message.from_user.id,
        week=0 if week >= 40 else week,
        line=0 if week >= 40 else line,
        answer=message.text
    ) 

    next_date: datetime = datetime.now() + timedelta(hours=36)

    await DiaryRepository().add(
        session=database,
        target=Diary(**diary_create.model_dump())
    )

    await state.clear()

    line = line + 1 

    if line >= 3:
        week += 1
        line = 0
    else:
        line = line + 1

    if week == 40:
        await message.answer(_("reload_diary"))

        return

    await message.answer(_("success_diary").format(date=next_date.strftime("%m/%d/%Y, %H:%M:%S")))

    NotificationRepository().add(
        notification_create=NotificationCreate(
            telegram_id=message.from_user.id,
            chat_id=message.chat.id,
            run_time=next_date,
            text=_("remind_diary")
        )
    )