from datetime import datetime, timedelta
from uuid import uuid4

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import ExistUser, ActiveSubscription
from bot.repository.notification import NotificationRepository
from bot.repository.notification.notification import (
    NotificationButton,
    NotificationCreate,
)
from bot.handlers.remind.callback_factory import RemindStart3Hours

from infrastructure.database.models import User
from infrastructure.database.crud import UserRepository

from .callback_factory import StartNextCallback
from .schemas import UserCreate


router: Router = Router(name=__name__)


@router.message(CommandStart(), ActiveSubscription())
async def start_handler(message: Message):
    await message.answer(
        _("start_for_client"),
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text=_("menu_profile_keyboard")),
                    KeyboardButton(text=_("menu_problems_keyboard")),
                ],
                [
                    KeyboardButton(text=_("menu_test_keyboard")),
                    KeyboardButton(text=_("menu_diary_keyboard")),
                ],
                [KeyboardButton(text=_("menu_help_keyboard"))],
                [KeyboardButton(text=_("menu_praxi_keyboard"))]
            ],
        ),
    )


@router.message(CommandStart(), ExistUser())
async def start_handler(message: Message):
    await message.answer(text="😀", reply_markup=ReplyKeyboardRemove())

    await message.answer(
        _("start_for_guest"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("continue_keyboard"),
                        callback_data=StartNextCallback(job_id="0").pack(),
                    )
                ]
            ]
        ),
    )


@router.message(CommandStart())
async def start_handler(message: Message, database: AsyncSession):
    job_id: str = uuid4().hex

    notification_create = NotificationCreate(
        telegram_id=message.from_user.id,
        chat_id=message.chat.id,
        run_time=datetime.now() + timedelta(minutes=30),
        text=_("ignore_start_30_minutes"),
        button=[
            [
                NotificationButton(
                    callback_data=StartNextCallback(job_id="0").pack(),
                    text=_("continue_keyboard"),
                ),
                NotificationButton(
                    callback_data=RemindStart3Hours().pack(),
                    text=_("not_now_keyboard")
                )
            ]
        ],
    )

    job = NotificationRepository().add(
        id=job_id, notification_create=notification_create
    )

    await message.answer(text="😀", reply_markup=ReplyKeyboardRemove())

    await UserRepository().add(
        session=database,
        target=User(**UserCreate(telegram_id=message.from_user.id).model_dump()),
    )

    await message.answer(
        _("start_for_guest"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("continue_keyboard"),
                        callback_data=StartNextCallback(job_id=job.id).pack(),
                    )
                ]
            ]
        ),
    )


__all__ = ["router"]
