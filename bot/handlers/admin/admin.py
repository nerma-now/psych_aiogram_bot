from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from .callback_factory import (
    CreateSubscriptionCallback,
    SubscriptionStatsCallback,
    SetAdminCallback,
    RemoveAdminCallback,
    ActivateUserCallback,
    DeactivateUserCallback,
    CheckUserTestCallback,
    GiveSubscriptionCallback,
    DeactivateSubscriptionCallback,
    SetPremiumSubscriptionCallback,
    RemovePremiumSubscriptionCallback,
    CreatePraxiCallback,
    AllSubscriptionFiles,
    DeleteSubscriptionFiles,
    UploadSubscriptionFiles
)

from bot.filters import IsAdmin

router: Router = Router(name=__name__)


@router.message(Command("admin"), IsAdmin())
async def admin_handler(
    message: Message,
):
    await message.answer(
        text=_("admin_menu"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("set_admin_keyboard"),
                        callback_data=SetAdminCallback().pack(),
                    ),
                    InlineKeyboardButton(
                        text=_("remove_admin_keyboard"),
                        callback_data=RemoveAdminCallback().pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=_("create_subscription_keyboard"),
                        callback_data=CreateSubscriptionCallback().pack(),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_("stats_subscription_keyboard"),
                        callback_data=SubscriptionStatsCallback().pack(),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_("activate_user_keyboard"),
                        callback_data=ActivateUserCallback().pack(),
                    ),
                    InlineKeyboardButton(
                        text=_("deactivate_user_keyboard"),
                        callback_data=DeactivateUserCallback().pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=_("last_user_test_keyboard"),
                        callback_data=CheckUserTestCallback().pack(),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_("give_subscription_keyboard"),
                        callback_data=GiveSubscriptionCallback().pack(),
                    ),
                    InlineKeyboardButton(
                        text=_("deactivate_subscription_keyboard"),
                        callback_data=DeactivateSubscriptionCallback().pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=_("set_premium_subscription_keyboard"),
                        callback_data=SetPremiumSubscriptionCallback().pack(),
                    ),
                    InlineKeyboardButton(
                        text=_("remove_premium_subscription_keyboard"),
                        callback_data=RemovePremiumSubscriptionCallback().pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=_("create_praxi_keyboard"),
                        callback_data=CreatePraxiCallback().pack(),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_("upload_subscription_files_keyboard"),
                        callback_data=UploadSubscriptionFiles().pack()
                    ),
                    InlineKeyboardButton(
                        text=_("delete_subscription_files_keyboard"),
                        callback_data=DeleteSubscriptionFiles().pack()
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_("all_subscription_files_keyboard"),
                        callback_data=AllSubscriptionFiles().pack()
                    )
                ]
            ]
        ),
    )


__all__ = ["router"]
