import uuid
from typing import Optional

from aiogram import Router
from aiogram.types import CallbackQuery, LabeledPrice

from sqlalchemy.ext.asyncio import AsyncSession

from .callback_factory import BuyCallback
from .exception_factory import SubscriptionActiveException

from bot.config import config
from bot.loader import BotLoader
from bot.filters import ExistUser, IsActivated
from bot.handlers.exception_factory import NotFoundException

from infrastructure.database.crud import SubscriptionPlanRepository, SubscriptionRepository
from infrastructure.database.models import SubscriptionPlan, Subscription


router: Router = Router(
    name=__name__
)

@router.callback_query(BuyCallback.filter(), ExistUser(), IsActivated())
async def buy_callback(
    query: CallbackQuery,
    callback_data: BuyCallback,
    database: AsyncSession
):
    subscription: Optional[Subscription] = await SubscriptionRepository().get_active(
        session=database,
        telegram_id=query.from_user.id
    )

    if subscription is not None:
        raise SubscriptionActiveException()

    plan: Optional[SubscriptionPlan] = await SubscriptionPlanRepository().get(
        session=database,
        target=SubscriptionPlan.id,
        value=uuid.UUID(callback_data.plan_id)
    )

    if plan is None:
        raise NotFoundException()

    await BotLoader().bot.send_invoice(
        chat_id=query.message.chat.id,
        title=plan.title,
        description=plan.description,
        payload=callback_data.plan_id,
        currency=config.payments.currency,
        prices=[
            LabeledPrice(
                label=plan.title,
                amount=plan.price
            )
        ],
        is_flexible=plan.is_flexible,
        provider_token=config.payments.test_token if config.payments.test_token else config.payments.live_token
    )