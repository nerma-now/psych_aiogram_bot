from aiogram import Router

from .files import router as files_router


router: Router = Router(name=__name__)


router.include_router(files_router)

__all__ = ["router"]
