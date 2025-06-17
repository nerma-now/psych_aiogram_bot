from aiogram import Router

from .exception import router as exception_router
from .payment import router as payment_router


router: Router = Router(
    name=__name__
)


router.include_router(exception_router)
router.include_router(payment_router)

__all__ = ['router']