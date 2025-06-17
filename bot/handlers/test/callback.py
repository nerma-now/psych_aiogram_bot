from uuid import uuid4
from typing import Optional
from datetime import datetime, timedelta

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import ExistUser, ActiveSubscription
from bot.repository import NotificationRepository
from bot.repository.notification.schemas import NotificationCreate, NotificationButton
from bot.handlers.get_praxia.callback_factory import GetPraxiaCallback

from .schemas import TestCreate
from .callback_factory import TestChooseCallback, TestAboutCallback
from .constants import OPTIONS, QUESTIONS
from .utils import generate_test_results, get_test_interpretation
from .exception_factory import CooldownException

from infrastructure.database.models import Test, User
from infrastructure.database.crud import TestRepository


router: Router = Router(name=__name__)


@router.callback_query(TestAboutCallback.filter())
async def about_test_callback(query: CallbackQuery, user: Optional[User]):
    await query.message.answer(
        _("about_test").format(
            name=user.name if user.name is not None else query.from_user.first_name
        ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("start_now_keyboard"),
                        callback_data=TestChooseCallback(answer=-1, job_id="0").pack(),
                    )
                ]
            ]
        ),
    )


@router.callback_query(TestChooseCallback.filter(), ActiveSubscription())
async def test_callback(
    query: CallbackQuery,
    callback_data: TestChooseCallback,
    database: AsyncSession,
    user: User,
):
    if callback_data.job_id != "0":
        try:
            NotificationRepository().delete(job_id=callback_data.job_id)
        except Exception as ex:
            pass

    test: Optional[Test] = await TestRepository().get_last(
        session=database, target=Test.telegram_id, value=query.from_user.id
    )

    if test is None or test.is_completed:
        if callback_data.answer == -1:
            test: Optional[Test] = await TestRepository().get_last_12h(
                session=database, target=Test.telegram_id, value=query.from_user.id
            )

            if test is not None and test.is_completed:
                raise CooldownException()

            await query.message.answer(_("instruction_test"))
            test = await TestRepository().add(
                session=database,
                target=Test(**TestCreate(telegram_id=query.from_user.id).model_dump()),
            )
        else:
            return

    if not callback_data.answer == -1:
        param = {
            f"score_test_{test.get_last_filled_score()+1 if test.get_last_filled_score() is not None else 1}": callback_data.answer
        }

        await TestRepository().update(session=database, instance=test, **param)

        if (
            isinstance(test.get_last_filled_score(), int)
            and test.get_last_filled_score() >= 14
        ):
            await TestRepository().update(
                session=database,
                instance=test,
                is_completed=True,
                completed_at=func.now(),
            )
            await query.message.answer(
                _("result_test_for_client").format(
                    name=(
                        user.name
                        if user.name is not None
                        else query.from_user.first_name
                    ),
                    result=generate_test_results(get_test_interpretation(test)),
                )
            )
            return

    await query.message.answer(
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
                        job_id="0",
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


@router.callback_query(TestChooseCallback.filter(), ExistUser())
async def test_callback(
    query: CallbackQuery,
    callback_data: TestChooseCallback,
    database: AsyncSession,
    user: User,
):
    if callback_data.job_id != "0":
        try:
            NotificationRepository().delete(job_id=callback_data.job_id)
        except Exception as ex:
            pass

    test: Optional[Test] = await TestRepository().get_last(
        session=database, target=Test.telegram_id, value=query.from_user.id
    )

    if test is None or test.is_completed:
        if callback_data.answer == -1:
            test: Optional[Test] = await TestRepository().get_last_12h(
                session=database, target=Test.telegram_id, value=query.from_user.id
            )

            if test is not None:
                raise CooldownException()

            await query.message.answer(_("instruction_test"))
            test = await TestRepository().add(
                session=database,
                target=Test(**TestCreate(telegram_id=query.from_user.id).model_dump()),
            )
        else:
            return

    if not callback_data.answer == -1:
        param = {
            f"score_test_{test.get_last_filled_score()+1 if test.get_last_filled_score() is not None else 1}": callback_data.answer
        }

        await TestRepository().update(session=database, instance=test, **param)

        if (
            isinstance(test.get_last_filled_score(), int)
            and test.get_last_filled_score() >= 14
        ):
            await TestRepository().update(
                session=database,
                instance=test,
                is_completed=True,
                completed_at=func.now(),
            )
            await query.message.answer(
                _("result_test").format(
                    name=(
                        user.name
                        if user.name is not None
                        else query.from_user.first_name
                    ),
                    result=generate_test_results(get_test_interpretation(test)),
                ),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(
                            text=_("free_praxia_keyboard"),
                            callback_data=GetPraxiaCallback().pack()
                        )]
                    ]
                )
            )
            return

    notification_create = NotificationCreate(
        telegram_id=query.from_user.id,
        chat_id=query.message.chat.id,
        run_time=datetime.now() + timedelta(hours=1),
        text=_("ignore_test_1_hours").format(
            name=user.name if user.name is not None else query.from_user.first_name,
            score=0 if test.get_last_filled_score() is None else test.get_last_filled_score(),
            max_score=14,
        ),
        button=[
            [
                NotificationButton(
                    callback_data=TestChooseCallback(answer=-1, job_id="0").pack(),
                    text=_("start_now_keyboard"),
                )
            ]
        ],
    )

    job = NotificationRepository().add(
        notification_create=notification_create
    )

    await query.message.answer(
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
                        job_id=job.id,
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


__all__ = ["router"]
