from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _


router: Router = Router(
    name=__name__
)

@router.message(F.text.func(lambda text: text == _('menu_help_keyboard')))
async def support_command(message: Message):
    await message.answer(_('support'))

@router.message(Command('support'))
async def support_command(message: Message):
    await message.answer(_('support'))


__all__ = ['router']