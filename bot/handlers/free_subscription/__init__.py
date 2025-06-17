from aiogram import Router

from .free_subscription import router as free_subscription_router
from .exception import router as exception_router

router: Router = Router(name=__name__)


router.include_router(free_subscription_router)
router.include_router(exception_router)

__all__ = ['router']