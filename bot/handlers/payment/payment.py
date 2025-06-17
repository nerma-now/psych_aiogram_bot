import uuid
from typing import Optional
from datetime import timedelta, datetime

from aiogram import Router, F
from aiogram.types import (
    Message,
    PreCheckoutQuery,
    KeyboardButton,
    ReplyKeyboardMarkup,
    BufferedInputFile,
)
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import BotLoader
from bot.config.constants import MAIN_DIR

from infrastructure.database.crud import (
    SubscriptionPlanRepository,
    SubscriptionRepository,
)
from infrastructure.database.models import SubscriptionPlan, User, Subscription

from .exception_factory import (
    InvalidPayloadException,
    SubscriptionPlanNotFoundException,
    SubscriptionActiveException,
)

from .schemas import SubscriptionCreate


router: Router = Router(name=__name__)


@router.pre_checkout_query()
async def checkout_payment_query(
    pre_checkout: PreCheckoutQuery, database: AsyncSession
):
    subscription: Optional[Subscription] = await SubscriptionRepository().get_active(
        session=database, telegram_id=pre_checkout.from_user.id
    )

    if subscription is not None:
        raise SubscriptionActiveException()

    payload: str = pre_checkout.invoice_payload

    if not payload:
        await BotLoader().bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout.id,
            error_message=_("payment_invalid_payload"),
            ok=False,
        )

        raise InvalidPayloadException()

    plan: Optional[SubscriptionPlan] = await SubscriptionPlanRepository().get(
        session=database, target=SubscriptionPlan.id, value=uuid.UUID(payload)
    )

    if plan is None:
        await BotLoader().bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout.id,
            error_message=_("payment_not_found_subscription"),
            ok=False,
        )

        raise SubscriptionPlanNotFoundException()

    await BotLoader().bot.answer_pre_checkout_query(
        pre_checkout_query_id=pre_checkout.id, ok=True
    )


@router.message(F.successful_payment)
async def successful_payment_handler(
    message: Message, database: AsyncSession, user: User
):
    payload: str = message.successful_payment.invoice_payload

    if not payload:
        raise InvalidPayloadException()

    plan: Optional[SubscriptionPlan] = await SubscriptionPlanRepository().get(
        session=database, target=SubscriptionPlan.id, value=payload
    )

    if plan is None:
        raise SubscriptionPlanNotFoundException()

    subscription: Optional[Subscription] = await SubscriptionRepository().get_last(
        session=database, target=Subscription.telegram_id, value=message.from_user.id
    )

    note: str = "+7 дней бонуса" if subscription is None else "-"

    query: Subscription = await SubscriptionRepository().add(
        session=database,
        target=Subscription(
            **SubscriptionCreate(
                telegram_id=message.from_user.id,
                plan_id=uuid.UUID(payload),
                end_at=(
                    datetime.now() + timedelta(days=31)
                    if subscription is not None
                    else datetime.now() + timedelta(days=38)
                ),
            ).model_dump()
        ),
    )

    await message.answer(
        _("success_payment").format(
            name=user.name if User.name is not None else message.from_user.first_name,
            note=note,
            end_date=query.end_at.strftime("%m/%d/%Y, %H:%M:%S"),
        )
    )

    with open(MAIN_DIR.joinpath("resource").joinpath("document.pdf"), "rb") as f:
        document_file: BufferedInputFile = BufferedInputFile(
            file=f.read(), filename="document.pdf"
        )

    await message.answer_document(
        document=document_file
    )

    with open(MAIN_DIR.joinpath("resource").joinpath("praxi.png"), "rb") as f:
        photo_file: BufferedInputFile = BufferedInputFile(
            file=f.read(), filename="photo.png"
        )

    await message.answer_photo(
        photo=photo_file
    )

    if plan.is_premium:
        with open(MAIN_DIR.joinpath("resource").joinpath("premium_document.pdf"), "rb") as f:
            premium_document_file: BufferedInputFile = BufferedInputFile(
                file=f.read(), filename="document.pdf"
            )

        await message.answer_document(
            document=premium_document_file
        )

    await message.answer(
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
