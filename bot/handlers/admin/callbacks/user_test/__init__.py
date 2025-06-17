from aiogram import Router

from .last_user_test import router as last_user_test_router
from .state import router as state_router
from .exception import router as exception_router


router: Router = Router(name=__name__)


router.include_router(last_user_test_router)
router.include_router(state_router)
router.include_router(exception_router)

__all__ = ["router"]
