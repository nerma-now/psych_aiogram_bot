from aiogram import Router

from .state import router as state_router
from .upload_files import router as upload_files_router


router: Router = Router(name=__name__)
router.include_router(upload_files_router)
router.include_router(state_router)


__all__ = ["router"]
