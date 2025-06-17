from datetime import timedelta
from typing import Sequence

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import config
from bot.filters import IsAdmin, IsSuperadmin
from bot.handlers.admin.callback_factory import SubscriptionStatsCallback

from infrastructure.database.crud import (
    SubscriptionRepository,
    SubscriptionPlanRepository,
)
from infrastructure.database.models import SubscriptionPlan, Subscription


router: Router = Router(name=__name__)


@router.callback_query(
    SubscriptionStatsCallback.filter(), IsAdmin(), IsSuperadmin()
)
async def subscription_stats_callback(query: CallbackQuery, database: AsyncSession):
    count = await SubscriptionRepository().get_count(session=database)
    count_hour = await SubscriptionRepository().get_count(
        session=database, time_period=timedelta(hours=1)
    )
    count_day = await SubscriptionRepository().get_count(
        session=database, time_period=timedelta(hours=24)
    )
    count_week = await SubscriptionRepository().get_count(
        session=database, time_period=timedelta(days=7)
    )
    count_month = await SubscriptionRepository().get_count(
        session=database, time_period=timedelta(days=31)
    )

    await query.message.answer(
        _("subscription_all_time_subscription").format(
            count=count,
            count_hour=count_hour,
            count_day=count_day,
            count_week=count_week,
            count_month=count_month,
        )
    )

    plans: Sequence[SubscriptionPlan] = await SubscriptionPlanRepository().get_all(
        session=database
    )

    if plans:
        for plan in plans:
            count = await SubscriptionRepository().get_count(
                session=database, target=Subscription.plan_id, value=plan.id
            )
            count_hour = await SubscriptionRepository().get_count(
                session=database,
                target=Subscription.plan_id,
                value=plan.id,
                time_period=timedelta(hours=1),
            )
            count_day = await SubscriptionRepository().get_count(
                session=database,
                target=Subscription.plan_id,
                value=plan.id,
                time_period=timedelta(hours=24),
            )
            count_week = await SubscriptionRepository().get_count(
                session=database,
                target=Subscription.plan_id,
                value=plan.id,
                time_period=timedelta(days=7),
            )
            count_month = await SubscriptionRepository().get_count(
                session=database,
                target=Subscription.plan_id,
                value=plan.id,
                time_period=timedelta(days=31),
            )

            await query.message.answer(
                _("subscription_for_current_subscription").format(
                    name=plan.title,
                    description=plan.description,
                    total_classes_monthly=plan.total_classes_monthly,
                    price=f"{plan.price//100}.{plan.price%100:02d}",
                    currency=config.payments.currency,
                    id=plan.id,
                    count=count,
                    count_hour=count_hour,
                    count_day=count_day,
                    count_week=count_week,
                    count_month=count_month,
                )
            )


__all__ = ["router"]
