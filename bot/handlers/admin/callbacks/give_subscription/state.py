from typing import Optional
from uuid import UUID
from datetime import datetime, timedelta

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import (
    UserRepository,
    SubscriptionPlanRepository,
    SubscriptionRepository,
)
from infrastructure.database.models import User, SubscriptionPlan, Subscription

from bot.filters import IsAdmin, IsSuperadmin
from bot.handlers.exception_factory import (
    WrongTypeException,
    NotFoundException,
    DuplicativeActionException,
)
from .exception_factory import AmountException
from .state_factory import GiveSubscriptionState
from .schemas import SubscriptionCreate


router: Router = Router(name=__name__)


@router.message(GiveSubscriptionState.telegram_id, IsAdmin(), IsSuperadmin())
async def give_subscription_id_state(
    message: Message, state: FSMContext, database: AsyncSession
):
    if not isinstance(message.text, str) or not message.text.isdigit():
        await state.clear()

        raise WrongTypeException()

    user: Optional[User] = await UserRepository().get(
        session=database, target=User.telegram_id, value=int(message.text)
    )

    if not user:
        await state.clear()

        raise NotFoundException()

    subscription: Optional[Subscription] = await SubscriptionRepository().get_active(
        session=database,
        telegram_id=user.telegram_id,
    )

    if subscription is not None:
        await state.clear()

        raise DuplicativeActionException()

    await state.update_data(telegram_id=int(user.telegram_id))
    await state.set_state(GiveSubscriptionState.subscription_id)
    await message.answer(_("get_subscription_plan"))


@router.message(GiveSubscriptionState.subscription_id, IsAdmin(), IsSuperadmin())
async def give_subscription_plan_state(
    message: Message, state: FSMContext, database: AsyncSession
):
    if not isinstance(message.text, str):
        await state.clear()

        raise WrongTypeException()

    subscription_plan: Optional[
        SubscriptionPlan
    ] = await SubscriptionPlanRepository().get(
        session=database, target=SubscriptionPlan.id, value=UUID(message.text)
    )

    if not subscription_plan:
        await state.clear()

        raise NotFoundException()

    await state.update_data(subscription_id=message.text)
    await state.set_state(GiveSubscriptionState.count_days)
    await message.answer(_("get_subscription_count_days"))


@router.message(GiveSubscriptionState.count_days, IsAdmin(), IsSuperadmin())
async def give_subscription_count_days_state(
    message: Message, state: FSMContext, database: AsyncSession
):
    if not isinstance(message.text, str) or not message.text.isdigit():
        await state.clear()

        raise WrongTypeException()

    if int(message.text) < 1 or int(message.text) > 365:
        await state.clear()

        raise AmountException()

    telegram_id: int = int(await state.get_value(key="telegram_id"))
    subscription_id: UUID = UUID(await state.get_value(key="subscription_id"))
    count_days: int = int(message.text)

    await SubscriptionRepository().add(
        session=database,
        target=Subscription(
            **SubscriptionCreate(
                telegram_id=telegram_id,
                plan_id=subscription_id,
                end_at=datetime.now() + timedelta(days=count_days),
            ).model_dump()
        ),
    )

    await message.answer(_("success"))

    await state.clear()


__all__ = ["router"]
