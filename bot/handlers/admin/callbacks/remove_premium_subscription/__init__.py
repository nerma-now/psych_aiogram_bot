from aiogram import Router

from .state import router as state_router
from .remove_premium_subscription import router as set_premium_subscription_router


router: Router = Router(name=__name__)


router.include_router(set_premium_subscription_router)
router.include_router(state_router)

__all__ = ["router"]
