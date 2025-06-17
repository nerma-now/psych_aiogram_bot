from typing import Optional

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from infrastructure.database.crud import SubscriptionRepository, UserRepository
from infrastructure.database.models import Subscription, User

from .state_factory import DeactivateSubscriptionState

from bot.filters import IsAdmin, IsSuperadmin
from bot.handlers.exception_factory import (
    WrongTypeException,
    NotFoundException,
    DuplicativeActionException,
    NotRightsException,
)


router: Router = Router(name=__name__)


@router.message(DeactivateSubscriptionState.telegram_id, IsAdmin(), IsSuperadmin())
async def deactivate_subscription_state(
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

    if subscription is None:
        await state.clear()

        raise DuplicativeActionException()

    if user.is_superadmin:
        await state.clear()

        raise NotRightsException()

    await SubscriptionRepository().update(
        session=database,
        instance=subscription,
        is_activated=False,
        canceled_at=func.now(),
    )

    await message.answer(_("success"))

    await state.clear()


__all__ = ["router"]
