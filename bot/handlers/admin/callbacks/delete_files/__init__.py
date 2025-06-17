from aiogram import Router

from .delete_files import router as delete_files_router
from .state import router as state_router


router: Router = Router()

router.include_router(delete_files_router)
router.include_router(state_router)

__all__ = ["router"]