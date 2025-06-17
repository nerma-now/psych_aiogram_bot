from aiogram import Router

from .create_praxi import router as create_praxi_router
from .state import router as state_router

router: Router = Router()
router.include_router(create_praxi_router)
router.include_router(state_router)

__all__ = ["router"]