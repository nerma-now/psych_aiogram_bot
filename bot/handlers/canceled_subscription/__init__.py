from aiogram import Router

from .canceled_subscription import router as canceled_subscription_router


router: Router = Router(
    name=__name__
)

router.include_router(canceled_subscription_router)

__all__ = ['router']