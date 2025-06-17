from aiogram import Router

from .exception import router as exception_router
from .state import router as state_router
from .give_subscription import router as give_subscription_router 

router: Router = Router(name=__name__)


router.include_router(exception_router)
router.include_router(state_router)
router.include_router(give_subscription_router)

__all__ = ["router"]
