from aiogram import Router
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.filters import ExistUser


router: Router = Router(name=__name__)


@router.message(ExistUser())
async def message_handler(message: Message) -> None:
    await message.answer(_("not_found"))


@router.message()
async def message_handler(message: Message) -> None:
    await message.answer(_("not_exist_user"))


__all__ = ["router"]
