from aiogram import Router

from .test import router as test_router
from .callback import router as callback_router
from .exception import router as exception_router


router: Router = Router(name=__name__)


router.include_router(test_router)
router.include_router(callback_router)
router.include_router(exception_router)

__all__ = ["router"]
