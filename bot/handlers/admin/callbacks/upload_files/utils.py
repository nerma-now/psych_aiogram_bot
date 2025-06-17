import io

from aiogram import Bot
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext

from bot.loader import BotLoader

from infrastructure.database.models.praxi_file import FileCategory


async def detect_file_type(message: Message, state: FSMContext) -> tuple:
    content_type = message.content_type
    file_data = None
    file_size = 0
    file_name = "unknown"
    mime_type = "application/octet-stream"
    category = FileCategory.OTHER
    
    # Обработка разных типов контента
    if content_type == ContentType.DOCUMENT:
        file_data = message.document
        file_size = file_data.file_size
        file_name = file_data.file_name
        mime_type = file_data.mime_type
        category = FileCategory.DOCUMENT
        
    elif content_type == ContentType.PHOTO:
        file_data = message.photo[-1]
        file_size = file_data.file_size
        file_name = f"photo_{file_data.file_id}.jpg"
        mime_type = "image/jpeg"
        category = FileCategory.PHOTO
        
    elif content_type == ContentType.VIDEO:
        file_data = message.video
        file_size = file_data.file_size
        file_name = file_data.file_name or f"video_{file_data.file_id}.mp4"
        mime_type = file_data.mime_type
        category = FileCategory.VIDEO
        
    elif content_type == ContentType.AUDIO:
        file_data = message.audio
        file_size = file_data.file_size
        file_name = file_data.file_name or f"audio_{file_data.file_id}.mp3"
        mime_type = file_data.mime_type
        category = FileCategory.AUDIO
        
    elif content_type == ContentType.VOICE:
        file_data = message.voice
        file_size = file_data.file_size
        file_name = f"voice_{file_data.file_id}.ogg"
        mime_type = "audio/ogg"
        category = FileCategory.AUDIO
        
    elif content_type == ContentType.VIDEO_NOTE:
        file_data = message.video_note
        file_size = file_data.file_size
        file_name = f"video_note_{file_data.file_id}.mp4"
        mime_type = "video/mp4"
        category = FileCategory.VIDEO

    return file_data, file_name, mime_type, category, file_size

async def download_content(
    bot: Bot, 
    file_id: str
) -> bytes:
    file_io = await bot.download(file_id)
    file_bytes = file_io.getvalue()
    file_io.close()
    
    return file_bytes