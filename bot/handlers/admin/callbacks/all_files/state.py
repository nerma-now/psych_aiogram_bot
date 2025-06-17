import uuid
from typing import Optional, Sequence

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import PraxiFilesRepository
from infrastructure.database.models import PraxiFiles

from bot.loader import BotLoader
from bot.filters import IsAdmin
from bot.handlers.exception_factory import (
    WrongTypeException,
    NotFoundException,
)

from .state_factory import AllFilesState
from .utils import send_praxi_file


router: Router = Router(name=__name__)


@router.message(AllFilesState.praxi_id, IsAdmin())
async def subscription_id_state(message: Message, state: FSMContext, database: AsyncSession):
    if not isinstance(message.text, str):
        await state.clear()

        raise WrongTypeException()

    praxi: Optional[Sequence[PraxiFiles]] = None

    try:
        praxi = await PraxiFilesRepository().get_current_all(
            session=database, target=PraxiFiles.praxi_id, value=uuid.UUID(message.text)
        )
    except Exception as e:
        print(e, praxi)

        await state.clear()

        raise NotFoundException()

    if not praxi:
        await state.clear()

        raise NotFoundException()

    for pr in praxi:
        await message.answer(f"""<b>Вложение ({pr.id})</b>:

Дата создания: {pr.created_at.strftime("%m/%d/%Y, %H:%M:%S")}
""")
        await send_praxi_file(BotLoader().bot, message.chat.id, pr)

    await state.clear()