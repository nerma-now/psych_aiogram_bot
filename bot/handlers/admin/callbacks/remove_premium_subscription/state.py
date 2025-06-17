from typing import Optional
from uuid import UUID

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import SubscriptionPlanRepository
from infrastructure.database.models import SubscriptionPlan

from .state_factory import RemovePremiumState

from bot.filters import IsAdmin, IsSuperadmin
from bot.handlers.exception_factory import (
    WrongTypeException,
    NotFoundException,
    DuplicativeActionException
)


router: Router = Router(name=__name__)


@router.message(RemovePremiumState.subscription_plan_id, IsAdmin(), IsSuperadmin())
async def set_premium_state(message: Message, state: FSMContext, database: AsyncSession):
    if not isinstance(message.text, str):
        await state.clear()

        raise WrongTypeException()

    subscription_plan: Optional[SubscriptionPlan] = await SubscriptionPlanRepository().get(
        session=database, target=SubscriptionPlan.id, value=UUID(message.text)
    )

    if not subscription_plan:
        await state.clear()

        raise NotFoundException()

    if not subscription_plan.is_premium:
        await state.clear()

        raise DuplicativeActionException()

    await SubscriptionPlanRepository().update(session=database, instance=subscription_plan, is_premium=False)

    await message.answer(_("success"))

    await state.clear()


__all__ = ["router"]
