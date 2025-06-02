from aiogram import Router

from .exception import router as exception_router
from .start import router as start_router
from .mini_exercises import router as mini_exercises_router
from .choose_name import router as choose_name_router
from .test import router as test_router
from .support import router as support_router
from .admin import router as admin_router
from .buy import router as buy_router
from .payment import router as payment_router
from .other import router as other_router


router: Router = Router(
    name=__name__
)
router.include_router(exception_router)
router.include_router(start_router)
router.include_router(choose_name_router)
router.include_router(mini_exercises_router)
router.include_router(test_router)
router.include_router(support_router)
router.include_router(admin_router)
router.include_router(buy_router)
router.include_router(payment_router)
router.include_router(other_router)

__all__ = ['router']