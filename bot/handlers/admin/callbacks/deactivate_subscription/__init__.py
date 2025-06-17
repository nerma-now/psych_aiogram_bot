from aiogram import Router

from .deactivate_subscription import router as deactivate_subscription_router
from .state import router as state_router


router: Router = Router(name=__name__)


router.include_router(deactivate_subscription_router)
router.include_router(state_router)

__all__ = ["router"]
