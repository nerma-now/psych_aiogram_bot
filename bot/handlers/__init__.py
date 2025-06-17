from aiogram import Router

from .exception import router as exception_router
from .start import router as start_router
from .mini_exercises import router as mini_exercises_router
from .choose_name import router as choose_name_router
from .test import router as test_router
from .remind import router as remind_router
#from .files import router as files_router
from .profile import router as profile_router
from .support import router as support_router
from .admin import router as admin_router
from .buy import router as buy_router
from .payment import router as payment_router
from .canceled_subscription import router as canceled_subscription_router
from .diary import router as diary_router
from .free_subscription import router as free_subscription_router
from .get_praxia import router as get_praxia_router
from .ready_praxia import router as ready_praxia_router
from .other import router as other_router


router: Router = Router(name=__name__)


router.include_router(exception_router)
router.include_router(start_router)
router.include_router(choose_name_router)
router.include_router(mini_exercises_router)
router.include_router(test_router)
router.include_router(remind_router)
#router.include_router(files_router)
router.include_router(support_router)
router.include_router(profile_router)
router.include_router(admin_router)
router.include_router(buy_router)
router.include_router(payment_router)
router.include_router(canceled_subscription_router)
router.include_router(diary_router)
router.include_router(free_subscription_router)
router.include_router(get_praxia_router)
router.include_router(ready_praxia_router)
router.include_router(other_router)

__all__ = ["router"]
