from aiogram import Router

from .exception import router as exception_router
from .create_subscription_plan import router as create_subscription_router
from .state import router as state_router


router: Router = Router(
    name=__name__
)

router.include_router(exception_router)
router.include_router(create_subscription_router)
router.include_router(state_router)

__all__ = ['router']