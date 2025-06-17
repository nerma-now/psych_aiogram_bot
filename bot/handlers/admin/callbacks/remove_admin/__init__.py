from aiogram import Router

from .remove_admin import router as remove_admin_router
from .state import router as state_router


router: Router = Router()


router.include_router(remove_admin_router)
router.include_router(state_router)

__all__ = ['router']