from aiogram import Router
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

from bot.filters import ActiveSubscription

from .callback_factory import CanceledSubscriptionCallback

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from infrastructure.database.models import Subscription
from infrastructure.database.crud import SubscriptionRepository


router: Router = Router(name=__name__)


@router.callback_query(
    CanceledSubscriptionCallback.filter(), ActiveSubscription()
)
async def canceled_subscription_callback(
    query: CallbackQuery, subscription: Subscription, database: AsyncSession
):
    await query.message.answer("😭", reply_markup=ReplyKeyboardRemove())
    await query.message.delete()

    await SubscriptionRepository().update(
        session=database,
        instance=subscription,
        is_activated=False,
        canceled_at=func.now(),
    )

    await query.message.answer(_("success"))
