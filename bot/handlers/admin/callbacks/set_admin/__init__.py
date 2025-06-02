from aiogram import Router

from .set_admin import router as set_admin_router
from .state import router as state_router


router: Router = Router()
router.include_router(set_admin_router)
router.include_router(state_router)

__all__ = ['router']