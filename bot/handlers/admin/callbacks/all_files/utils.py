import io

from aiogram import Bot
from aiogram.types import Message, BufferedInputFile
from infrastructure.database.models.praxi_file import FileCategory, PraxiFiles


async def send_praxi_file(
    bot: Bot,
    chat_id: int,
    praxi_file: PraxiFiles,
    caption: str = None,
    **kwargs
) -> Message:
    if praxi_file.category == FileCategory.PHOTO:
        return await bot.send_photo(
            chat_id=chat_id,
            photo=BufferedInputFile(file=praxi_file.content, filename=praxi_file.file_name),
            caption=caption,
            **kwargs
        )
        
    elif praxi_file.category == FileCategory.VIDEO:
        return await bot.send_video(
            chat_id=chat_id,
            video=BufferedInputFile(file=praxi_file.content, filename=praxi_file.file_name),
            caption=caption,
            **kwargs
        )
        
    elif praxi_file.category == FileCategory.AUDIO:
        return await bot.send_audio(
            chat_id=chat_id,
            audio=BufferedInputFile(file=praxi_file.content, filename=praxi_file.file_name),
            caption=caption,
            **kwargs
        )
        
    else:
        return await bot.send_document(
            chat_id=chat_id,
            document=BufferedInputFile(file=praxi_file.content, filename=praxi_file.file_name),
            caption=caption,
            **kwargs
        )