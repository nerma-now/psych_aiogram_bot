from aiogram import Router

from .stats_subscription import router as stats_subscription_router


router: Router = Router(
    name=__name__
)

router.include_router(stats_subscription_router)

__all__ = ['router']