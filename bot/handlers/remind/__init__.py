from aiogram import Router

from .remind import router as remind_router


router: Router = Router(name=__name__)

router.include_router(remind_router)

__all__ = ["router"]
