from aiogram import Router

from .set_admin import router as set_admin_router
from .remove_admin import router as remove_admin_router
from .stats_subscription import router as stats_subscription_router
from .create_subscription_plan import router as create_subscription_router
from .activate_user import router as activate_user_router
from .deactivate_user import router as deactivate_user_router


router: Router = Router(
    name=__name__
)
router.include_router(set_admin_router)
router.include_router(remove_admin_router)
router.include_router(create_subscription_router)
router.include_router(stats_subscription_router)
router.include_router(activate_user_router)
router.include_router(deactivate_user_router)

__all__ = ['router']