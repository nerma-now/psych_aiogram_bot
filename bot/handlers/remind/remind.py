from datetime import datetime, timedelta
from uuid import uuid4

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from bot.repository.notification import NotificationRepository
from bot.repository.notification.schemas import (
    NotificationButton,
    NotificationCreate,
    NotificationFile,
)
from bot.handlers.start.callback_factory import StartNextCallback

from .callback_factory import RemindStart3Hours


router: Router = Router(name=__name__)


@router.callback_query(RemindStart3Hours.filter())
async def remind_start_3_hours_callback(query: CallbackQuery):
    job_id: str = uuid4().hex

    await query.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("start_now_keyboard"),
                        callback_data=StartNextCallback(job_id=job_id).pack(),
                    )
                ]
            ]
        )
    )

    notification_create = NotificationCreate(
        telegram_id=query.from_user.id,
        chat_id=query.message.chat.id,
        run_time=datetime.now() + timedelta(hours=3),
        text=_("ignore_start_3_hours"),
        button=[
            [
                NotificationButton(
                    callback_data=StartNextCallback(job_id="0").pack(),
                    text=_("start_now_keyboard"),
                )
            ]
        ],
    )

    job = NotificationRepository().add(
        id=job_id, notification_create=notification_create
    )

    await query.answer(_("success"))


__all__ = ["router"]
