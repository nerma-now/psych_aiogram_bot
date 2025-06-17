from typing import Sequence

from aiogram import Router
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import config
from bot.filters import ExistUser
from bot.handlers.buy.callback_factory import BuyCallback

from infrastructure.database.crud import SubscriptionPlanRepository
from infrastructure.database.models import SubscriptionPlan

from .exception_factory import PlansNotFoundException


router: Router = Router(name=__name__)


@router.message(Command("buy"), ExistUser())
async def buy_handler(message: Message, database: AsyncSession):
    plans: Sequence[SubscriptionPlan] = await SubscriptionPlanRepository().get_all(
        session=database
    )

    if not plans:
        raise PlansNotFoundException()

    for plan in plans:
        await message.answer(
            text=_("plans_description").format(
                name=f"{plan.title} ({plan.id})",
                description=plan.description,
                price=f"{plan.price//100}.{plan.price%100:02d}",
                total_classes_monthly=plan.total_classes_monthly,
                currency=config.payments.currency,
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=_("buy_keyboard"),
                            callback_data=BuyCallback(plan_id=str(plan.id)).pack(),
                        )
                    ]
                ]
            ),
        )


__all__ = ["router"]
