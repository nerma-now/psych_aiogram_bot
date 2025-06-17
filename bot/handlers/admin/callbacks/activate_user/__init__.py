from aiogram import Router

from .activate_user import router as activate_user_router
from .state import router as state_router


router: Router = Router(name=__name__)


router.include_router(activate_user_router)
router.include_router(state_router)

__all__ = ["router"]
