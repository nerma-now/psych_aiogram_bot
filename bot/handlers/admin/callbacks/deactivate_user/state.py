from typing import Optional

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import UserRepository
from infrastructure.database.models import User

from bot.filters import IsAdmin
from bot.handlers.exception_factory import (WrongTypeException,
                                            NotFoundException,
                                            DuplicativeActionException,
                                            NotRightsException)

from .state_factory import DeactivateUserState


router: Router = Router(
    name=__name__
)

@router.message(DeactivateUserState.telegram_id, IsAdmin())
async def activate_user_state(
    message: Message,
    state: FSMContext,
    database: AsyncSession
):
    if not isinstance(message.text, str) or not message.text.isdigit():
        await state.clear()

        raise WrongTypeException()

    user: Optional[User] = await UserRepository().get(
        session=database,
        target=User.telegram_id,
        value=int(message.text)
    )

    if not user:
        await state.clear()

        raise NotFoundException()

    if not user.is_activated:
        await state.clear()

        raise DuplicativeActionException()

    if user.is_superadmin or user.is_admin:
        await state.clear()

        raise NotRightsException()

    await UserRepository().update(
        session=database,
        instance=user,
        is_activated=False
    )

    await message.answer(_('success'))

    await state.clear()

__all__ = ['router']