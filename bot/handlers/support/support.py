from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.filters import TextOrCommandFilter


router: Router = Router(name=__name__)


@router.message(TextOrCommandFilter(text_key="menu_help_keyboard", command="support"))
async def support_command(message: Message):
    await message.answer(_("support"))


__all__ = ["router"]
