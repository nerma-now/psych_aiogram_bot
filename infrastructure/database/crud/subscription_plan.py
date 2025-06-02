from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository

from infrastructure.database.models import SubscriptionPlan


class SubscriptionPlanRepository(BaseRepository[SubscriptionPlan]):
    model = SubscriptionPlan

__all__ = ['SubscriptionPlanRepository']