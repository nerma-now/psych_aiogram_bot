import uuid
from typing import Optional

from aiogram import Router, F
from aiogram.types import Message, PreCheckoutQuery
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import BotLoader
from bot.filters import IsActivated

from infrastructure.database.crud import SubscriptionPlanRepository, SubscriptionRepository
from infrastructure.database.models import SubscriptionPlan, Subscription

from .exception_factory import (InvalidPayloadException,
                                SubscriptionPlanNotFoundException,
                                SubscriptionActiveException)

from .schemas import SubscriptionCreate


router: Router = Router(
    name=__name__
)

@router.pre_checkout_query()
async def checkout_payment_query(
    pre_checkout: PreCheckoutQuery,
    database: AsyncSession
):
    subscription: Optional[Subscription] = await SubscriptionRepository().get_active(
        session=database,
        telegram_id=pre_checkout.from_user.id
    )

    if subscription is not None:
        raise SubscriptionActiveException()

    payload: str = pre_checkout.invoice_payload

    if not payload:
        await BotLoader().bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout.id,
            error_message=_('payment_invalid_payload'),
            ok=False
        )

        raise InvalidPayloadException()

    plan: Optional[SubscriptionPlan] = await SubscriptionPlanRepository().get(
        session=database,
        target=SubscriptionPlan.id,
        value=uuid.UUID(payload)
    )

    if plan is None:
        await BotLoader().bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout.id,
            error_message=_('payment_not_found_subscription'),
            ok=False
        )

        raise SubscriptionPlanNotFoundException()

    await BotLoader().bot.answer_pre_checkout_query(
        pre_checkout_query_id=pre_checkout.id,
        ok=True
    )

@router.message(F.successful_payment, IsActivated())
async def successful_payment_handler(
    message: Message,
    database: AsyncSession
):
    payload: str = message.successful_payment.invoice_payload

    if not payload:
        raise InvalidPayloadException()

    plan: Optional[SubscriptionPlan] = await SubscriptionPlanRepository().get(
        session=database,
        target=SubscriptionPlan.id,
        value=payload
    )

    if plan is None:
        raise SubscriptionPlanNotFoundException()

    await SubscriptionRepository().add(
        session=database,
        target=Subscription(
            **SubscriptionCreate(
                telegram_id=message.from_user.id,
                plan_id=uuid.UUID(payload),
            ).model_dump()
        )
    )


__all__ = ['router']