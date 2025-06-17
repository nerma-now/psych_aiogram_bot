from aiogram import Router
from aiogram.types import (
    CallbackQuery,
    BufferedInputFile,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.i18n import gettext as _

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .callback_factory import FreeSubscriptionCallback
from .exception_factory import (
    ExistSubscriptionException,
    SubscriptionPlanNotFoundException,
)
from .schemas import SubscriptionCreate

from bot.filters import ExistUser
from bot.config.constants import MAIN_DIR

from infrastructure.database.crud import (
    SubscriptionRepository,
    SubscriptionPlanRepository,
)
from infrastructure.database.models import Subscription, SubscriptionPlan, User


router: Router = Router(name=__name__)


@router.callback_query(
    FreeSubscriptionCallback.filter(),
    ExistUser(),
)
async def free_subscription_callback(
    query: CallbackQuery, database: AsyncSession, user: User
):
    subscription: Optional[Subscription] = await SubscriptionRepository().get(
        session=database, target=Subscription.telegram_id, value=query.from_user.id
    )

    if subscription is not None:
        raise ExistSubscriptionException()

    plan: Optional[SubscriptionPlan] = await SubscriptionPlanRepository().get(
        session=database, target=SubscriptionPlan.is_premium, value=True
    )

    if plan is None:
        raise SubscriptionPlanNotFoundException()

    note: str = "-"

    sub: Subscription = await SubscriptionRepository().add(
        session=database,
        target=Subscription(
            **SubscriptionCreate(
                telegram_id=query.from_user.id, plan_id=plan.id
            ).model_dump()
        ),
    )

    await query.message.answer(
        _("success_payment").format(
            name=user.name if User.name is not None else query.from_user.first_name,
            note=note,
            end_date=sub.end_at.strftime("%m/%d/%Y, %H:%M:%S"),
        )
    )

    try:
        with open(MAIN_DIR.joinpath("resource").joinpath("document.pdf"), "rb") as f:
            document_file: BufferedInputFile = BufferedInputFile(
                file=f.read(), filename="document.pdf"
            )

        await query.message.answer_document(document=document_file)

        with open(MAIN_DIR.joinpath("resource").joinpath("praxi.png"), "rb") as f:
            photo_file: BufferedInputFile = BufferedInputFile(
                file=f.read(), filename="photo.png"
            )

        await query.message.answer_photo(photo=photo_file)

        if plan.is_premium:
            with open(
                MAIN_DIR.joinpath("resource").joinpath("premium_document.pdf"), "rb"
            ) as f:
                premium_document_file: BufferedInputFile = BufferedInputFile(
                    file=f.read(), filename="document.pdf"
                )

            await query.message.answer_document(document=premium_document_file)
    except:
        pass

    await query.message.answer(
        "🤯",
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


__all__ = ["router"]
