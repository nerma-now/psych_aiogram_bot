from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from typing import Optional
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import TextOrCommandFilter, ActiveSubscription
from bot.handlers.canceled_subscription.callback_factory import (
    CanceledSubscriptionCallback,
)

from infrastructure.database.crud import SubscriptionPlanRepository, DiaryRepository
from infrastructure.database.models import User, Subscription, SubscriptionPlan, Diary


router: Router = Router(name=__name__)


@router.message(
    TextOrCommandFilter(text_key="menu_profile_keyboard", command="profile"),
    ActiveSubscription(),
)
async def support_command(
    message: Message, user: User, subscription: Subscription, database: AsyncSession
):
    subscription: Subscription = subscription
    subscription_plan: Optional[
        SubscriptionPlan
    ] = await SubscriptionPlanRepository().get(
        session=database, target=SubscriptionPlan.id, value=subscription.plan_id
    )
    subs: str = "-"

    if subscription_plan is not None:
        subs: str = f"""- Наиманование подписки: <b>{subscription_plan.title}</b> (<b>{subscription_plan.id}</b>)
- Дата завершения действия подписки: <b>{subscription.end_at.strftime("%m/%d/%Y, %H:%M:%S")}</b>"""

    await message.answer(
        _("profile_menu").format(
            telegram_id=message.from_user.id,
            user_id=str(user.id),
            name=user.name if user.name is not None else message.from_user.first_name,
            created_at=user.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            subscription=subs,
            diary_count=await DiaryRepository().get_count(
                session=database,
                target=Diary.telegram_id,
                value=message.from_user.id,
                time_period=timedelta(days=31),
            ),
        ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("profile_canceled_subscription_keyboard"),
                        callback_data=CanceledSubscriptionCallback().pack(),
                    )
                ]
            ]
        ),
    )


__all__ = ["router"]
