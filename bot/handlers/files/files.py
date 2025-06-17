from aiogram import Router
from aiogram.types import Message


router: Router = Router(name=__name__)


@router.message()
async def files_handler(message: Message):
    if message.document:
        file_id = message.document.file_id
        await message.answer(f"Document file_id: {file_id}")

    elif message.photo:
        file_id = message.photo[-1].file_id
        await message.answer(f"Photo file_id: {file_id}")

    elif message.audio:
        file_id = message.audio.file_id
        await message.answer(f"Audio file_id: {file_id}")

    elif message.video:
        file_id = message.video.file_id
        await message.answer(f"Video file_id: {file_id}")

    elif message.voice:
        file_id = message.voice.file_id
        await message.answer(f"Voice file_id: {file_id}")

    elif message.video_note:
        file_id = message.video_note.file_id
        await message.answer(f"Video note file_id: {file_id}")

    elif message.sticker:
        file_id = message.sticker.file_id
        await message.answer(f"Sticker file_id: {file_id}")

    elif message.animation:
        file_id = message.animation.file_id
        await message.answer(f"Animation (GIF) file_id: {file_id}")

    else:
        pass


__all__ = ["router"]
