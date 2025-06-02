from aiogram import Router

from .deactivate_user import router as deactivate_user_router
from .state import router as state_router


router: Router = Router(
    name=__name__
)

router.include_router(deactivate_user_router)
router.include_router(state_router)

__all__ = ['router']