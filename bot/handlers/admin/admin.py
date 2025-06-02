from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from .callback_factory import (CreateSubscriptionPlanCallback,
                               DeleteSubscriptionPlanCallback,
                                StatsSubscriptionCallback,
                               SetAdminCallback,
                               RemoveAdminCallback,
                               ActivateUserCallback,
                               DeactivateUserCallback)

from bot.filters import IsAdmin, IsActivated

router: Router = Router(
    name=__name__
)

@router.message(Command('admin'), IsAdmin(), IsActivated())
async def admin_handler(
    message: Message,
):
    await message.answer(
        text=_('admin_menu'),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_('set_admin_keyboard'),
                        callback_data=SetAdminCallback().pack()
                    ),
                    InlineKeyboardButton(
                        text=_('remove_admin_keyboard'),
                        callback_data=RemoveAdminCallback().pack()
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_('create_subscription_keyboard'),
                        callback_data=CreateSubscriptionPlanCallback().pack()
                    ),
                    InlineKeyboardButton(
                        text=_('delete_subscription_keyboard'),
                        callback_data=DeleteSubscriptionPlanCallback().pack()
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_('stats_subscription_keyboard'),
                        callback_data=StatsSubscriptionCallback().pack()
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_('activate_user_keyboard'),
                        callback_data=ActivateUserCallback().pack()
                    ),
                    InlineKeyboardButton(
                        text=_('deactivate_user_keyboard'),
                        callback_data=DeactivateUserCallback().pack()
                    )
                ]
            ]
        )
    )

__all__ = ['router']