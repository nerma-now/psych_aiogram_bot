from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import UserRepository
from infrastructure.database.models import User

from .callback_factory import ChooseNameCallback


router: Router = Router(
    name=__name__
)

@router.callback_query(ChooseNameCallback.filter())
async def chose_name_callback(
    query: CallbackQuery,
    state: FSMContext,
    database: AsyncSession,
    user: Optional[User]
):
    await UserRepository().update(
        session=database,
        instance=user,
        name=query.from_user.first_name
    )

    await state.clear()

__all__ = ['router']