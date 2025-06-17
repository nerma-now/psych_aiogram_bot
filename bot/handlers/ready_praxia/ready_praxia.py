from aiogram import Router
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BufferedInputFile,
)
from aiogram.utils.i18n import gettext as _

from random import randint
from typing import Optional, Sequence

from bot.filters import ExistUser

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from .callback_factory import ReadyPraxiaCallback, RatingPraxiaCallback

from bot.config import config
from bot.config.constants import MAIN_DIR
from bot.handlers.buy.callback_factory import BuyCallback
from bot.handlers.buy.exception_factory import PlansNotFoundException
from bot.handlers.free_subscription.callback_factory import FreeSubscriptionCallback

from infrastructure.database.crud import (
    ReceivePraxiRepository,
    SubscriptionPlanRepository,
)
from infrastructure.database.models import ReceivePraxi, SubscriptionPlan, Subscription
from infrastructure.database.models.receive_praxi import (
    ReceivePraxiRating,
    ReceivePraxiStatus,
)


router: Router = Router(name=__name__)


@router.callback_query(
    ReadyPraxiaCallback.filter(),
    ExistUser(),
)
async def ready_praxia_callback(query: CallbackQuery):
    await query.message.answer(
        _("choose_rate_praxi"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Норм",
                        callback_data=RatingPraxiaCallback(
                            rating=ReceivePraxiRating.OK
                        ).pack(),
                    ),
                    InlineKeyboardButton(
                        text="Сложно",
                        callback_data=RatingPraxiaCallback(
                            rating=ReceivePraxiRating.HARD
                        ).pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Прям в точку",
                        callback_data=RatingPraxiaCallback(
                            rating=ReceivePraxiRating.EXACT
                        ).pack(),
                    )
                ],
            ],
        ),
    )


@router.callback_query(
    RatingPraxiaCallback.filter(),
    ExistUser(),
)
async def rating_praxia_callback(
    query: CallbackQuery,
    callback_data: RatingPraxiaCallback,
    database: AsyncSession,
    subscription: Optional[Subscription],
):
    receive_praxi: Optional[ReceivePraxi] = await ReceivePraxiRepository().get_last(
        session=database, target=ReceivePraxi.telegram_id, value=query.from_user.id
    )

    if receive_praxi is None:
        return

    if receive_praxi.is_completed:
        return

    await ReceivePraxiRepository().update(
        session=database,
        instance=receive_praxi,
        is_completed=True,
        completed_at=func.now(),
        rating=callback_data.rating,
        status=ReceivePraxiStatus.STUDIED,
    )

    try:
        match callback_data.rating:
            case ReceivePraxiRating.OK:
                rand: int = randint(1, 5)

                with open(
                    MAIN_DIR.joinpath("resource").joinpath(f"norm{rand}.m4a"), "rb"
                ) as f:
                    audio_file: BufferedInputFile = BufferedInputFile(
                        file=f.read(), filename="audio.mp3"
                    )

                await query.message.answer_audio(audio=audio_file)
            case ReceivePraxiRating.HARD:
                rand: int = randint(1, 4)

                with open(
                    MAIN_DIR.joinpath("resource").joinpath(f"hard{rand}.m4a"), "rb"
                ) as f:
                    audio_file: BufferedInputFile = BufferedInputFile(
                        file=f.read(), filename="audio.mp3"
                    )

                await query.message.answer_audio(audio=audio_file)
            case ReceivePraxiRating.EXACT:
                rand: int = randint(1, 15)

                with open(
                    MAIN_DIR.joinpath("resource").joinpath(f"dot{rand}.m4a"), "rb"
                ) as f:
                    audio_file: BufferedInputFile = BufferedInputFile(
                        file=f.read(), filename="audio.mp3"
                    )

                await query.message.answer_audio(audio=audio_file)
            case _:
                pass
    except:
        pass

    if subscription is None:
        await query.message.answer(
            _("choose_subscription"),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=_("choose_subscription_keyboard"),
                            callback_data=FreeSubscriptionCallback().pack(),
                        )
                    ]
                ]
            ),
        )

        plans: Sequence[SubscriptionPlan] = await SubscriptionPlanRepository().get_all(
            session=database
        )

        if not plans:
            raise PlansNotFoundException()

        for plan in plans:
            await query.message.answer(
                text=_("plans_description").format(
                    name=f"{plan.title} ({plan.id})",
                    description=plan.description,
                    price=f"{plan.price//100}.{plan.price%100:02d}",
                    total_classes_monthly=plan.total_classes_monthly,
                    currency=config.payments.currency,
                ),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text=_("buy_keyboard"),
                                callback_data=BuyCallback(plan_id=str(plan.id)).pack(),
                            )
                        ]
                    ]
                ),
            )


__all__ = ["router"]
