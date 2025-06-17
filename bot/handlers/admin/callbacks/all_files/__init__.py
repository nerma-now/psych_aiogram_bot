from aiogram import Router
from .all_files import router as all_files_router
from .state import router as state_router

router: Router = Router()

router.include_router(all_files_router)
router.include_router(state_router)

__all__ = ["router"]