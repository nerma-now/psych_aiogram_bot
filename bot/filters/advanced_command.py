from aiogram.filters import Filter
from aiogram.types import Message



class TextOrCommandFilter(Filter):
    def __init__(self, text_key: str, command: str):
        self.text_key = text_key  
        self.command = command

    async def __call__(self, message: Message) -> bool:
        from aiogram.utils.i18n import gettext as _
        translated_text = _(self.text_key)
        return (
            message.text == translated_text or
            message.text == f"/{self.command}"
        )


__all__ = ["TextOrCommandFilter"]
