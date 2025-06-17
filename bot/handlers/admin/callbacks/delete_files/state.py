from typing import Optional
from uuid import UUID

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import PraxiFilesRepository
from infrastructure.database.models import PraxiFiles

from .state_factory import DeleteFilesState

from bot.filters import IsAdmin, IsSuperadmin
from bot.handlers.exception_factory import (
    WrongTypeException,
    NotFoundException,
    DuplicativeActionException
)


router: Router = Router(name=__name__)


@router.message(DeleteFilesState.file_id, IsAdmin())
async def set_premium_state(message: Message, state: FSMContext, database: AsyncSession):
    if not isinstance(message.text, str):
        await state.clear()

        raise WrongTypeException()

    praxi_file: Optional[PraxiFiles] = await PraxiFilesRepository().get(
        session=database, target=PraxiFiles.id, value=UUID(message.text)
    )

    if not praxi_file:
        await state.clear()

        raise NotFoundException()

    await PraxiFilesRepository().delete(session=database, target=praxi_file)

    await message.answer(_("success"))

    await state.clear()


__all__ = ["router"]
