from aiogram import Router

from .admin import router as admin_router
from .callbacks import router as callback_router


router: Router = Router(name=__name__)


router.include_router(admin_router)
router.include_router(callback_router)

__all__ = ["router"]
