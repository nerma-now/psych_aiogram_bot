from aiogram import Router

from .diary import router as diary_router
from .exception import router as exception_router
from .callback import router as callback_router
from .state import router as state_router


router: Router = Router(name=__name__)


router.include_router(diary_router)
router.include_router(exception_router)
router.include_router(callback_router)
router.include_router(state_router)

__all__ = ["router"]
