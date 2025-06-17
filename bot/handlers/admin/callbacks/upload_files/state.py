import uuid
from typing import Optional

from aiogram import Router
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import PraxiRepository, PraxiFilesRepository
from infrastructure.database.models import PraxiFiles, Praxi

from bot.loader import BotLoader
from bot.filters import IsAdmin
from bot.handlers.exception_factory import (
    WrongTypeException,
    NotFoundException,
)

from .schemas import FileCreate
from .state_factory import UploadFilesState
from .utils import detect_file_type, download_content


router: Router = Router(name=__name__)


@router.message(UploadFilesState.praxi_id, IsAdmin())
async def subscription_id_state(message: Message, state: FSMContext, database: AsyncSession):
    if not isinstance(message.text, str):
        await state.clear()

        raise WrongTypeException()

    try:
        praxi: Optional[Praxi] = await PraxiRepository().get(
            session=database, target=Praxi.id, value=uuid.UUID(message.text)
        )
    except:
        await state.clear()

        raise NotFoundException()

    if not praxi:
        await state.clear()

        raise NotFoundException()

    await state.update_data(praxi_id=message.text)
    await state.set_state(UploadFilesState.file)

    await message.answer(_("get_file"))

@router.message(UploadFilesState.file, IsAdmin())
async def file_state(message: Message, state: FSMContext, database: AsyncSession):
    content_type = message.content_type
    
    is_file = content_type in [
        ContentType.DOCUMENT,
        ContentType.PHOTO,
        ContentType.VIDEO,
        ContentType.AUDIO,
        ContentType.VOICE,
        ContentType.VIDEO_NOTE,
        ContentType.STICKER,
    ]
    
    if isinstance(message.text, str) or not is_file:
        await state.clear()

        raise WrongTypeException()
    
    try:
        file_data, file_name, mime_type, category, file_size = await detect_file_type(message, state)
        
        if not file_data:
            await state.clear()

            await message.answer("Не удалось обработать файл. Попробуйте другой формат.")

            return
        
        if file_data.file_size > 20 * 1024 * 1024:
            await state.clear()

            await message.answer("Файл не может быть больше 20 МБ")

            return
        
        try:
            content = await download_content(BotLoader().bot, file_data.file_id)
        except Exception as e:
            await state.clear()

            await message.answer("Ошибка при обработке файла")

            return


        praxi_id: uuid.UUID = uuid.UUID(await state.get_value("praxi_id"))

        file_create = FileCreate(
            praxi_id=praxi_id,
            file_name=file_name,
            file_type=mime_type,
            file_size=file_size,
            category=category,
            content=content
        )

        await PraxiFilesRepository().add(
            session=database,
            target=PraxiFiles(**file_create.model_dump())
        )

        await message.answer(_("success"))
    except Exception as ex:
        await state.clear()

        await message.answer("Ошибка при обработке файла")

        return

__all__ = ["router"]
