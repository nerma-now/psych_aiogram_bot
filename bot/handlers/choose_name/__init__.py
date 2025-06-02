from aiogram import Router

from .choose_name import router as choose_name_router
from .state import router as state_router
from .exception import router as exception_router


router: Router = Router(
    name=__name__
)
router.include_router(choose_name_router)
router.include_router(state_router)
router.include_router(exception_router)

__all__ = ['router']