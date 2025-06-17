from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import PraxiRepository
from infrastructure.database.models import Praxi

from .state_factory import CreatePraxiState
from .schemas import PraxiCreate

from bot.filters import IsAdmin


router: Router = Router(name=__name__)


@router.message(CreatePraxiState.title, IsAdmin())
async def create_praxi_title_state(
    message: Message, state: FSMContext, database: AsyncSession
):
    if not isinstance(message.text, str) or not message.text or len(message.text) > 256:
        await state.clear()

        await message.answer(_("subscription_get_title"))
        return

    await state.update_data(title=message.text)

    await message.answer(_("subscription_get_description"))
    await state.set_state(CreatePraxiState.text)


@router.message(CreatePraxiState.text, IsAdmin())
async def create_praxi_text_state(
    message: Message, state: FSMContext, database: AsyncSession
):
    if (
        not isinstance(message.text, str)
        or not message.text
        or len(message.text) >= 2048
    ):
        await state.clear()

        await message.answer(_("subscription_get_description"))
        return

    title: str = await state.get_value("title")
    text: str = message.text

    await PraxiRepository().add(
        session=database,
        target=Praxi(**PraxiCreate(title=title, text=text).model_dump()),
    )

    await state.clear()

    await message.answer(_("success"))


__all__ = ["router"]
