from aiogram import Router

from .support import router as support_router


router: Router = Router(
    name=__name__
)
router.include_router(support_router)

__all__ = ['router']