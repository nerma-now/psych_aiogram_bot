from aiogram import Router

from .exception import router as exception_router
from .callback import router as callback_router
from .buy import router as buy_router

router: Router = Router(
    name=__name__
)
router.include_router(exception_router)
router.include_router(callback_router)
router.include_router(buy_router)

__all__ = ['router']