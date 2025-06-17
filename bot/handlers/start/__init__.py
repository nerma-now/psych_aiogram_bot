from aiogram import Router

from .start import router as start_router
from .callback import router as callback_router


router: Router = Router(
    name=__name__
)

router.include_router(start_router)
router.include_router(callback_router)

__all__ = ['router']